# CCAR-F study deck: how it is built and how to run it

Study here: **https://dogthathunts.github.io/ccarf-anki-web/** — 508 notes, 518 cards, six decks. No install, no account; it runs entirely in your browser.
Editable source: `CCAR-F_cards_source.json` (and its flat twin `CCAR-F_cards_source.csv`)

---

## 1. The method, and why this deck is shaped the way it is

The deck used to ship as an Anki `.apkg`. It is now a web app, because the scheduling settings below matter more than the tooling and the web app arrives with all of them already set. `CCAR-F_Foundations.apkg` is kept as an archive and is no longer rebuilt.

Spaced repetition works on one mechanism: retrieving a fact just as you are about to forget it strengthens the memory more than re-reading it ever will. The scheduler places each card at the point where recall is effortful but still possible, and pushes the interval out each time you succeed. The learning gain comes from the effort of retrieval, so anything that lets you answer without retrieving is wasted review time.

That constraint drives two design rules, both from Piotr Wozniak's formulation of the minimum information principle.

**One card, one retrievable fact.** A card holding four facts cannot be scheduled. You know two of them, half-know one, miss one, and the algorithm has no way to represent that state, so it keeps showing you material you already know while the gap stays open. Every card in this deck answers in under ten seconds.

**No multiple choice.** This is the design decision worth arguing about, because the obvious move was to put the 60 mock exam questions straight into the deck. Recognising the right option out of four is a weaker task than producing the answer from nothing, and after two or three passes over a fixed question set you stop reasoning and start recognising the wording. You end up with a deck that returns 95% correct and an exam that returns 441.

So the material is split by what each tool does well:

| Tool | Trains | Use it for |
|---|---|---|
| This deck | Retrieval of the atomic layer: mechanisms, trigger conditions, the reason each anti-pattern fails | Daily, in short sessions |
| The exam simulator | Applying that layer under scenario pressure and a 120-minute clock | Weekly, full form, timed |

The simulator is at https://dogthathunts.github.io/ccarf-exam-simulator/. The deck is what makes the simulator's explanations stick. The simulator is what tells you whether the deck is working.

---

## 2. What is in the deck

508 notes across six decks.

| Deck | Notes |
|---|---|
| D1 Agentic architecture and orchestration | 104 |
| D2 Tool design and MCP integration | 97 |
| D3 Claude Code configuration and workflows | 106 |
| D4 Prompt engineering and structured output | 94 |
| D5 Context management and reliability | 99 |
| D6 Exam technique and scoring | 8 |

All 30 task statements from the exam guide are covered. Card counts do not mirror the blueprint's domain weights: they are weighted toward the objectives where candidates most often score zero, which is why D3 carries the most cards despite being a 20% domain.

Five card shapes are in use. Mechanism cards ask what something does. Trigger cards ask when to reach for it. Discrimination cards put two workable-sounding approaches side by side and ask which condition separates them. Anti-pattern cards name a flawed approach and ask what breaks. Cloze cards handle paths, parameter names, and enumerable sets.

The discrimination and anti-pattern cards are the ones that move the score. 187 of the 508 are one or the other, and they are drawn from the mock exam rubric's explanations of why each distractor fails, generalised so no exam question is reproduced.

### Tags

Every note carries four tags, and a few carry a fifth.

- `ts::1_1` through `ts::5_6`, plus `ts::exam`. Filter to one objective after a weak simulator result.
- `domain::D1` to `domain::D5`, `domain::EXAM`.
- `priority::high` (325 notes) and `priority::normal` (183). High marks the objectives with the worst historical pass rates.
- `class::mechanism`, `class::trigger`, `class::discrimination`, `class::antipattern`, `class::definition`, `class::technique`.
- `scope::background` (5 notes). MCP protocol architecture that is accurate but sits outside what the exam guide scopes as testable. Search `-scope::background` to leave them out if you are short on time.

---

## 3. Settings

These are already configured. They are listed so you know what the schedule is doing, and so you can tell whether a change you make in Settings is an improvement or a mistake.

1. New cards per day: **20**. Raise it to **35** if you have only two to three weeks. Above 35 the review load compounds past what is sustainable.
2. Maximum reviews per day: **200**. Leave headroom; a cap that bites creates a backlog you never clear.
3. Learning steps: **25m, then 1d**. The usual `1m 10m` default is tuned for vocabulary, and these cards need a longer first gap.
4. Relearning steps: **20m, then 1d**.
5. Leech threshold: **6 lapses**, tagged rather than suspended. A leech in this deck is a signal to go read the source, not to drop the card.
6. FSRS with desired retention **0.90**. Change it before you start, not partway through — it reshapes every future interval.
7. Sibling burying: **on**. Stops the two halves of a cloze card appearing in the same session.

Only the first three, retention, burying and the theme are exposed in Settings; the steps and the leech threshold are fixed.

Answer honestly. Pressing Good on a card you half-knew is the single fastest way to make the schedule useless.

### Profiles and backups

The first screen asks who is studying. Each name keeps its own schedule, so several people can share one machine, and nothing is uploaded — progress lives in that browser's storage alone. Two consequences worth taking seriously:

- Clearing site data for the domain erases the schedule. So does studying on a different machine, which starts from zero.
- **Back up** in Settings writes a JSON file holding your whole schedule; **Restore** reads it back on any machine. Do this before you switch devices, and once a week regardless.

---

## 4. Running it

**Daily, 20 to 30 minutes.** Clear the review queue first, then take the day's new cards. Two sessions of 15 minutes beat one of 30. If a day's reviews exceed 30 minutes, drop new cards to zero for two days rather than skipping reviews; reviews are the part that holds the deck together.

**Keyboard:** space reveals the answer, then 1 to 4 grade it (Again, Hard, Good, Easy); space again is Good. `u` undoes the last answer.

**When you miss a card,** say the correct answer out loud before pressing Again. Recall attempted and failed, then corrected, is worth more than recall not attempted.

**Weekly, one timed simulator run.** Take the full 60-question form under the clock. The score report gives a per-objective breakdown.

**After each run,** take every objective below 70% and study those cards specifically. Under Custom study, tap the task statement — TS 3.1, say — then **Drill all**, which walks the whole tag whether or not those cards are due, weakest first. The search box takes the same tags directly: `tag:ts::3_1`, `priority::high`, `class::discrimination`, `-scope::background`, `is:leech`, and combinations of them. The Stats page surfaces the same thing from the other side: any objective under 70% on first-attempt recall gets a chip you can tap straight into a drill.

This closes the loop: the simulator locates the gap, the deck fills it, the next run tests whether it held.

**A suggested four-week shape**, if you have four weeks:

1. Week 1: 25 new cards a day, D1 and D3 first. One simulator run at the end of the week to get a baseline.
2. Week 2: continue new cards, second simulator run mid-week, targeted study on whatever came back under 70%.
3. Week 3: new cards finish. Two simulator runs. Reviews plus targeted tag sessions.
4. Week 4: reviews only, no new cards. One simulator run early in the week, then leave the last two days for reviews alone. Do not take a fresh mock exam the day before.

---

## 5. Editing and rebuilding

`CCAR-F_cards_source.json` is the record, and `CCAR-F_cards_source.csv` is the same content flat, for editing in a spreadsheet. Columns: `type`, `front_or_cloze_text`, `back_or_extra`, `domain`, `task_statement`, `priority`, `card_class`, `reference`.

To change cards, edit the source and rebuild:

```
python3 build_web.py        # writes index.html
```

No dependencies and no build toolchain: the script formats each note, expands cloze notes into their individual holes, and injects the result into `web_template.html` at its `__DATA__` placeholder. The output is one self-contained file. Commit it and GitHub Pages serves the new version.

A rebuild does not touch anyone's schedule, which is keyed by note and hole index and lives in the browser. Reordering or deleting notes will shift those keys, so add new cards at the end rather than inserting them mid-file.

If you edit the CSV rather than the JSON, convert it back before building — the JSON is what `build_web.py` reads.

## 6. What to be careful about

Four claims in the first draft asserted detail that appears only in the study videos and not in the exam guide. They were corrected or removed before this build, and two patterns are worth carrying forward if you extend the deck.

Video summaries condense the guide and add their own framing. One video presents a named "five-field error schema" that the guide does not use; the guide names a category, a retryable flag, and a human-readable description. Another video gives 95% and 50% as confidence tier boundaries; the guide gives no fixed percentages and says the boundaries come from calibration against a labelled validation set. Both cards now teach the concept without the invented specifics.

The guide's appendix lists out-of-scope topics by name. One card taught MCP transport mechanisms including server-sent events, which the appendix excludes explicitly. It was deleted.

The rule for anything added later: if a claim cannot be defended from the exam guide's own text, it does not go on a card, whatever a video says.

---

## 7. Sources

- `Claude_Certified_Architect_Foundations_Exam_Guide.md` (v1.0, July 2026), sections 3, 5, 6, 9, 10, 12 and 17
- `summaries/` and `transcripts/`: EP01 to EP12, and Zero to Claude Certified Architect parts 1 to 32
- `mock_exams/exam_A_rubric.md` and `mock_exams/blueprint_map.md`
