#!/usr/bin/env python3
"""Build CCAR-F_video_links.json: task statement -> source video links.

    python3 build_links.py

Two kinds of link come out of this.

The "Zero to Claude Certified Architect" parts map one-to-one onto task
statements — Part 2 is TS 1.1, Part 3 is TS 1.2, and so on — so the whole video
is the chapter and the link carries no timestamp. That mapping is derived from
the card references, not assumed.

The EP episodes each cover several objectives, so they need a timestamp. Those
twelve entries in CHAPTERS below were located by scoring the transcript against
each objective's card text, then read by hand against the transcript to confirm
the moment is the explanation rather than the end-of-episode quiz. Each carries
the line it was verified against. Do not add an entry here without reading the
transcript at that second.

Needs the summaries/ and transcripts/ folders alongside; it reads the video ID
out of each summary and never copies transcript text into the output.
"""
import json, os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SUMM, TRANS = os.path.join(ROOT, 'summaries'), os.path.join(ROOT, 'transcripts')
SRC = os.path.join(HERE, 'CCAR-F_cards_source.json')
OUT = os.path.join(HERE, 'CCAR-F_video_links.json')

# (task statement, episode, start second, the transcript line it was checked against)
CHAPTERS = [
    ('1.1', 'EP02',  50, 'An agent is not magic. An agent is a loop. Four steps.'),
    ('1.2', 'EP03',  75, 'The fix is decomposition. One coordinator splits the work...'),
    ('1.3', 'EP03', 226, 'How does a coordinator actually create a sub-agent? With the Task tool.'),
    ('1.4', 'EP04',  78, 'Verify identity before a financial operation. That needs a guarantee.'),
    ('1.5', 'EP04', 145, 'A hook is code that sits on the wire between the agent and its tools.'),
    ('1.6', 'EP04', 324, 'One more design decision the exam tests. How to break a big task into steps.'),
    ('2.1', 'EP05', 118, 'A tool definition has three required parts. A name, a description and an input schema.'),
    ('3.1', 'EP06',  63, 'Start with memory, the CLAUDE.md file... there is a hierarchy. Four layers.'),
    ('4.2', 'EP08', 126, 'Technique 2, the highest leverage one on the list. Examples.'),
    ('4.3', 'EP09', 121, 'A tool is optional by default... you force it with the tool choice parameter.'),
    ('4.4', 'EP09', 265, 'Even with the perfect schema, validate what comes back.'),
    ('5.1', 'EP10', 128, 'Filling the window is not the goal. As context grows, accuracy degrades.'),
]

URL = re.compile(r'https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]{11})')


MDLINK = re.compile(r'\[([^\]]+)\]\(https?://[^)]*(?:youtube\.com|youtu\.be)[^)]*\)')


def clean_title(fname, label, body=''):
    """Human-readable topic, preferring the full title inside the summary over
    the on-disk filename, which is truncated."""
    m = MDLINK.search(body or '')
    t = m.group(1) if m else re.sub(r'_[0-9a-f]{8}$', '', re.sub(r'^\d+_', '', fname[:-3]))
    t = t.replace('：', ':').replace('｜', '|').replace('⧸', '/').replace('_', ' ')
    if label.startswith('Part'):
        m = re.search(r'Part\s*\d+\s*[:\-]\s*(.*)', t)
        t = m.group(1) if m else t.split('|')[-1]
    else:
        t = re.sub(r'^EP\s*\d+\s*[:\-]\s*', '', t).strip()
    t = re.sub(r'\s+', ' ', t).strip(' -:|')
    return (t[:58].rstrip() + '…') if len(t) > 59 else t


def catalogue():
    """label -> {vid, title}, from the summaries' own source links."""
    out = {}
    if not os.path.isdir(SUMM):
        sys.exit('summaries/ not found at ' + SUMM)
    for f in sorted(os.listdir(SUMM)):
        if not f.endswith('.md'):
            continue
        body = open(os.path.join(SUMM, f), errors='replace').read()
        m = URL.search(body)
        if not m:
            continue
        ep = re.search(r'EP(\d+)', f)
        pt = re.search(r'Part[ _](\d+)', f)
        label = 'EP%02d' % int(ep.group(1)) if ep else ('Part %d' % int(pt.group(1)) if pt else None)
        if label and os.path.exists(os.path.join(TRANS, f[:-3] + '.txt')):
            out[label] = {'vid': m.group(1), 'title': clean_title(f, label, body)}
    return out


def main():
    cat = catalogue()
    rows = json.load(open(SRC))

    # Which videos does each objective's cards actually cite?
    cited = collections.defaultdict(collections.Counter)
    for r in rows:
        ref = r.get('ref', '')
        labels = ['EP%02d' % int(m.group(1)) for m in re.finditer(r'EP(\d+)', ref)]
        labels += ['Part %d' % int(m.group(1)) for m in re.finditer(r'Part (\d+)', ref)]
        for l in labels:
            if l in cat:
                cited[r['ts']][l] += 1

    chap = {(ts, ep): (t, line) for ts, ep, t, line in CHAPTERS}
    links, stamped, whole = {}, 0, 0
    for ts, counter in cited.items():
        entries = []
        for label, n in counter.most_common():
            if n < 3 and len(entries) >= 1:
                continue                      # a passing mention, not a source
            e = {'label': label, 'title': cat[label]['title'], 'id': cat[label]['vid'], 'cards': n}
            if label.startswith('EP'):
                if (ts, label) not in chap:
                    continue                  # no verified chapter: do not guess a timestamp
                e['t'], e['checked'] = chap[(ts, label)][0], chap[(ts, label)][1]
                stamped += 1
            else:
                whole += 1                    # the part video is the lesson; no timestamp needed
            entries.append(e)
        if entries:
            links[ts] = entries

    json.dump({'links': links}, open(OUT, 'w'), ensure_ascii=False, indent=1)
    covered = sum(1 for r in rows if r['ts'] in links)
    print('objectives linked : %d of 30' % len([k for k in links if k != 'exam']))
    print('timestamped chapters: %d   whole-lesson links: %d' % (stamped, whole))
    print('cards reached     : %d of %d' % (covered, len(rows)))
    print('wrote', OUT)


if __name__ == '__main__':
    main()
