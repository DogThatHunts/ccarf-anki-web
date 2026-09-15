# CCAR-F Study Deck

A spaced-repetition deck for the **Claude Certified Architect – Foundations (CCAR-F)** certification. 518 cards over 508 notes, covering all 30 task statements of the exam guide.

**Study here:** https://dogthathunts.github.io/ccarf-anki-web/

- Six decks by domain, five card shapes: mechanism, trigger, discrimination, anti-pattern, cloze
- FSRS-5 scheduling with the deck's settings already applied — 20 new cards a day, learning steps of 25 minutes and 1 day, desired retention 0.90, leeches tagged at six lapses
- Custom study by task statement, priority, or card class: `tag:ts::3_1`, `priority::high`, `class::discrimination`, `-scope::background`, `is:leech`. **Drill all** walks a whole tag whether or not the cards are due, weakest first
- Stats: retention, four-week forecast, and first-attempt accuracy per objective, with a one-tap drill on anything under 70%
- Named profiles, so several people can share a machine, with backup and restore as a JSON file
- Keyboard: space reveals, 1–4 grade, `u` undoes

Everything runs client-side in a single HTML file. No account, no install, no data leaves your browser — which also means progress is per-browser, so use **Back up** in Settings before switching machines.

Pair it with the [mock exam simulator](https://dogthathunts.github.io/ccarf-exam-simulator/): the simulator locates the gap, the deck fills it, the next run tests whether it held.

`CCAR-F_study_protocol.md` explains why the deck is shaped this way and how to run a four-week schedule.

## Building

`CCAR-F_cards_source.json` is the source of record; `CCAR-F_cards_source.csv` is the same content flat, for spreadsheet editing.

```
python3 build_web.py        # writes index.html
```

No dependencies. The script formats each note, expands cloze notes into their individual holes, and injects the result into `web_template.html` at its `__DATA__` placeholder.

Add new cards at the end of the source rather than inserting them mid-file: schedules are keyed by note index, so reordering shifts what people have already learned.

*Unofficial study material — not affiliated with or endorsed by Anthropic.*
