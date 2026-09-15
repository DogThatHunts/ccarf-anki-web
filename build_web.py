#!/usr/bin/env python3
"""Build the single-file CCAR-F study deck web app.

    python3 build_web.py [--out index.html]

Reads CCAR-F_cards_source.json (the record; the CSV is its flat twin), formats
each note the same way build_deck.py formats it for Anki, expands cloze notes
into their individual holes, and injects the result into web_template.html at
the __DATA__ placeholder. No dependencies, no CDN: the output is one
self-contained HTML file suitable for GitHub Pages.
"""
import argparse, datetime, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'CCAR-F_cards_source.json')
TPL = os.path.join(HERE, 'web_template.html')

DOMAINS = [
    ('D1', 'D1 Agentic Architecture & Orchestration'),
    ('D2', 'D2 Tool Design & MCP Integration'),
    ('D3', 'D3 Claude Code Configuration & Workflows'),
    ('D4', 'D4 Prompt Engineering & Structured Output'),
    ('D5', 'D5 Context Management & Reliability'),
    ('EXAM', 'D6 Exam Technique & Scoring'),
]


def fmt(s):
    """Backtick spans -> <code>, everything else escaped. Mirrors build_deck.py."""
    out = []
    for p in re.split(r'(`[^`]+`)', s or ''):
        if len(p) > 1 and p.startswith('`') and p.endswith('`'):
            out.append('<code>' + html.escape(p[1:-1]) + '</code>')
        else:
            out.append(html.escape(p))
    return ''.join(out).replace('\n', '<br>')


CLOZE_RE = re.compile(r'\{\{c(\d+)::(.*?)\}\}', re.S)


def split_cloze(text):
    """-> (parts, ords). Parts are html strings, or [ord, html, hint]."""
    parts, ords, pos = [], [], 0
    for m in CLOZE_RE.finditer(text):
        if m.start() > pos:
            parts.append(fmt(text[pos:m.start()]))
        ord_ = int(m.group(1))
        body = m.group(2)
        hint = ''
        if '::' in body:                      # {{c1::answer::hint}}
            body, hint = body.rsplit('::', 1)
        parts.append([ord_, fmt(body), fmt(hint)] if hint else [ord_, fmt(body)])
        if ord_ not in ords:
            ords.append(ord_)
        pos = m.end()
    if pos < len(text):
        parts.append(fmt(text[pos:]))
    return parts, sorted(ords)


def build(out_path):
    rows = json.load(open(SRC))
    notes, cards, high = [], 0, 0
    for r in rows:
        n = {
            'ty': 'c' if r['type'] == 'cloze' else 'b',
            'b': fmt(r.get('back', '')),
            'r': fmt(r.get('ref', '')),
            'd': r['domain'],
            'ts': r['ts'],
            'p': r['priority'],
            'c': r.get('cardclass', 'concept'),
        }
        if r.get('scope'):
            n['sc'] = r['scope']
        if n['ty'] == 'c':
            n['f'], n['o'] = split_cloze(r['front'])
            if not n['o']:
                sys.exit('cloze note with no {{cN::}} hole: ' + r['front'][:70])
            cards += len(n['o'])
        else:
            n['f'] = fmt(r['front'])
            cards += 1
        if n['p'] == 'high':
            high += 1
        notes.append(n)

    data = {
        'built': datetime.date.today().isoformat(),
        'high': high,
        'domains': [{'k': k, 'name': v} for k, v in DOMAINS
                    if any(n['d'] == k for n in notes)],
        'tslist': sorted({n['ts'] for n in notes},
                         key=lambda t: (t == 'exam', t)),
        'classes': sorted({'class::' + n['c'] for n in notes}),
        'notes': notes,
    }

    tpl = open(TPL).read()
    if '__DATA__' not in tpl:
        sys.exit('template is missing the __DATA__ placeholder')
    blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', r'<\/')
    open(out_path, 'w').write(tpl.replace('__DATA__', blob))

    size = os.path.getsize(out_path) / 1024
    print('notes: %d  cards: %d  high-priority notes: %d' % (len(notes), cards, high))
    for d in data['domains']:
        print('  %-44s %3d notes' % (d['name'], sum(1 for n in notes if n['d'] == d['k'])))
    print('wrote %s (%.0f KB)' % (out_path, size))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(HERE, 'index.html'))
    build(ap.parse_args().out)
