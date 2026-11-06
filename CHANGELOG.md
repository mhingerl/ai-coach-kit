# Changelog

The newest kit version is also in the one-line [`VERSION`](VERSION) file. Entries from 2026-11-05 on start with a *Touches:* line (what the change affects) and an *If you already use the kit:* line.

## 2026-11-06

*Touches:* setup prompt (section 3, "Writing workouts to intervals.icu": strength event format and the check after writing) and the check-in skill template (the same strength event format bullets).
*If you already use the kit:* only if you use the Strength Coach watch app (version 1.2.x). Replace the strength event format bullets and the "After writing a strength event" check in your saved check-in skill with the new text from the template. No data files, datasets or dashboard changes.

- Strength event format rewritten for Strength Coach 1.2.x: the line syntax is unchanged (`N. EXERCISE NAME | TARGET | LOAD | SIDE`), but the watch now reads the lines differently. Same-exercise sets are bundled into one overview row, supersets are detected from the line order (a cycle of 2 to 4 different exercises that repeats at least twice) and drawn with a bracket, left and right sets share an L/R row, and the overview header shows the duration from the prose.
- Four example sessions added as templates (straight sets, superset with a one-sided exercise, timed and one-sided superset, failure sets with a three-exercise circuit).
- The prose above or below the set lines should carry a duration such as `~35 min`, and must never contain the character `|`.
- Failure sets are written exactly `max`. An extra set for one side is simply one more `left` line where it should be done; it does not break the superset detection.
- Two new checks after writing a strength event: a planned superset repeats in the same order at least twice, and the first prose line carries the duration.
- The duration goes in the first prose line (for example `Strength D, ~40 min.`): the watch uses the first `N min` it finds in the prose, so an earlier or later mention such as `5 min warm-up` could be shown instead.

## 2026-11-05.2

*Touches:* dashboard template only (`kit/coach-kit-dashboard.html`: the colour helpers in the `tdb` object and the drawings for muscle maps, muscle load bars, workout blocks, recovery trends, fitness/form, weekly hours, intensity split and the season timeline; one sentence in the Recovery intro).
*If you already use the kit:* optional, visual only. Replace your dashboard page with the new template (keep your SETUP lines), or ask Claude to "apply the 2026-11-05.2 colour update to my dashboard". No data files, datasets or other documents change.

- Zone colours as in intervals.icu's zone table (Z1 teal, Z2 green, Z3 yellow, Z4 orange, Z5 pink, Z6 purple, Z7 grey) for workout blocks; weekly hours and the easy/moderate/hard split use Z2, Z3 and Z4.
- Muscle maps use the inferno heat scale instead of one blue.
- Muscle load bars and the sessions-per-area dots use traffic-light colours (green at target, amber from 70%, red below).
- Recovery charts colour each reading green, amber or red against your own band, baseline or typical value (HRV, resting heart rate, sleep, heart rate and breathing asleep, stress, Body Battery, steps). Weight stays neutral.
- Fitness, fatigue and form: fitness blue, fatigue pink, form bars and bands in the usual zone colours (high risk, optimal, grey zone, fresh, transition).
- Season timeline: one colour per phase, the current phase outlined, finished phases faded, milestones in gold.

## 2026-11-05

*Touches:* setup prompt (2.6 step 5, 2.8, section 3 "Dashboard refresh" and the new "Keeping runs cheap"), check-in skill template ("Dashboard sync", "Dashboard refresh", "Logging"), new `VERSION` file.
*If you already use the kit:* copy the new "Dashboard refresh (cheap flow)" text into your saved check-in skill in place of its old dashboard-refresh bullet, and change your weekly review's kit-news step to read `VERSION` first. No data files or dashboard changes needed.

- Cheaper dashboard sync: the check-in no longer reads whole CSV files through the chat to add a row. It saves the dashboard's current file to disk, merges the new rows with a script, uploads the result by file path, updates all changed dataset documents in one batch and backs the file up to the project from disk. Only files that changed are touched, once per check-in, and old uploaded files are cleaned up about every ten syncs instead of on every sync. Without disk access it falls back to the old way.
- Cheaper kit-news check: the weekly review reads only the one-line `VERSION` file first and stops when it matches the version you set up from. Only when there is something newer does it read `CHANGELOG.md`, and only as far as your version. Every entry now starts with a *Touches:* line, so an update means fetching just the named files, not redoing the setup.
- New "Keeping runs cheap" guidance: read only what the task needs, never pass whole data files through the chat, weekly scheduled runs with short prompts that stop early when nothing changed.

## 2026-11-03

- Pairing planned and actual activities is stricter: the coach checks every completed activity of the day (commutes and short rides too), not only the one being discussed, and sanity-checks pairs that already exist by sport, duration and load, because intervals.icu sometimes attaches a short commute to the evening's planned ride or leaves a strength session unpaired. Clear matches are linked with `link_activity_to_event` without asking. The coach has no unlink tool, so when a wrong pair blocks the right one it says so plainly and asks you to unlink it in intervals.icu. It re-checks after calendar changes and when a later activity is uploaded. Events with a date but no start time make same-day mismatches more likely.
- Regular foods and supplements are remembered: the interview asks for the foods and supplements you use regularly (products and usual portions), the coach saves them in memory (or a `claude/regular-foods.md` document without memory) and uses them for "my usual scoop" or "same as last time" instead of asking again. It asks only when a portion differs or a product is new.
- Block reviews get a summary file and a dashboard panel: each block review adds one row to `claude/reviews/block_reviews.csv` (phase, dates, bike hours, strength sessions, fitness start and end, easy share, headline, first suggested change, review file), and a new Block reviews panel on the Season and logs page lists them. The weekly review and the check-in both add the row when they write a review.
- Dashboard template catches up with the 2026-10-31 readiness rules: the wellness file uses `sleep_hr_bpm`, `resp_sleep`, `sleep_stress` and `body_battery_peak` (replacing `body_battery_wake`, which the template still reads if an old file has it); readiness gets a heart rate asleep marker against the 30-night median with the possible-illness flag (8+ bpm above, or 5+ with breathing 1.5+ breaths/min faster or stress asleep 10+ higher), which makes the day red; overnight stress and Body Battery peak count only together with another flag; the Recovery page adds heart rate, breathing rate and stress asleep.
- Strength events: put the whole session in one `WeightTraining` event per day. A companion watch app reads only the first strength event of the day.

## 2026-11-01

- Food logging is itemised: for every meal the coach writes each item with its amount and its own kcal, carbs (sugars), fibre, protein, fat (saturated) and salt, then subtotals, a meal total, a "main contributors" line for bigger meals and the running total for the day, into one "Nutrition log" note per day on the intervals.icu calendar (replacing the earlier daily-totals-only CSV idea). The numbers must add up, fibre and protein are tracked as priorities, and ride fuel is its own entry plus `carbs_ingested_g` on the activity. This is what lets you go back and see what to improve.
- Strength events can now ask for a set to failure: write `max` in the target field (`3. Push-ups | max | bodyweight`; `amrap` and `to failure` also work) and a companion watch app shows MAX instead of a rep count. The reps actually done come back in the Watch log as a normal `N reps`. Never write a placeholder rep count for a failure set. MAX is for reps only: a timed hold stays `N s`.
- Pairing planned and actual sessions: whenever a completed session is checked or reported, the coach checks that intervals.icu has paired the planned event with the actual activity and pairs them itself (`link_activity_to_event`) when auto-pairing missed, which happens for strength sessions uploaded from a watch. It does this before reading a Watch log or computing compliance, and needs no go-ahead.
- Strength events are now written as numbered per-set lines (`n. exercise | target | load | side`) so a watch app can read them: one line per set in the order they are done, supersets and side switches expressed by line order, no set counts, labels or rest fields. The `external_id` date must match the event's start date.
- After writing a strength event the coach re-reads it and validates the format.
- Optional Watch log handling: if a companion watch app appends a log of the sets actually done to the event description, the coach uses it as the primary source when logging and debriefing, and never overwrites or shortens a description that has one.
- Rep shorthand is only for how sessions are reported in chat, not for events. `planned.csv` `strength_plan` stays `exercise_id:sets` joined by `|` (a CSV column, not the event text).
- Setup now adds a kit-news step to the weekly review: it reads this repository's CHANGELOG, compares it with the kit version you set up from and reports what changed (it applies nothing without your say-so).
- Setup recommends the free Connect IQ watch apps where they fit: Strength Coach Interpreter (guides the planned strength session from your intervals.icu calendar and writes the Watch log) and Scale Linker (Renpho scale weigh-ins to intervals.icu).

## 2026-10-31

- The dashboard works out fitness, fatigue and form itself from the daily training load (42-day and 7-day exponentially weighted averages), instead of showing intervals.icu's numbers; intervals.icu's values appear next to them for comparison. Strength load counts toward fatigue only by default (`STRENGTH_IN_FITNESS`). The fitness data file gains a `strength_load` column, and the first sync backfills a year of daily load so the calculation starts clean.
- Setup and dashboard state the principle: the page calculates its own metrics from raw data, provider scores are not inputs, and coaching decisions come from all the data and how the athlete feels, not one dashboard number.
- Walks no longer count as endurance hours or in the intensity split. The commute benchmark counts only the climb itself (at most `COMMUTE_MAX_KM`, default 8 km).
- Check-in skill: with icuvisor, wellness requests include the `id` field so each row carries its date.
- Readiness works out what it can from raw measurements; watch numbers that can't be recomputed (overnight stress, Body Battery) count against the athlete's own 30-day medians as supporting markers, while the watch maker's labels ("stressful"), readiness score and sleep score are not inputs. New marker: average heart rate asleep against its 30-night median, with a possible-illness flag (8+ bpm above, or 5+ with breathing 1.5+ breaths/min faster) that makes the day red. New wellness columns `sleep_hr_bpm`, `resp_sleep`, `sleep_stress` and `body_battery_peak` (replacing `body_battery_wake`); the Recovery page adds heart rate, breathing rate and stress asleep and shows Body Battery and daytime stress against the athlete's usual values.

## 2026-10-30

- The dashboard has pages now: Today, Recovery, Training load, Strength, and Season and logs.
- Today: readiness worked out on the page with the check-in's own rules (HRV 7-day average against your normal range, resting heart rate, sleep, form, Body Battery and stress), not the watch maker's readiness score; today's planned sessions with a done badge and the debrief verdict; the workout's block structure for cycling, running or other endurance sports; muscles to target today on the body map; the coming days.
- Recovery: HRV with its normal band, resting heart rate with baseline, sleep, Body Battery, stress, steps and weight. Training load: fitness, fatigue and form with form zones, weekly hours by intensity, the 28-day intensity split, FTP outdoor and indoor, session debriefs, and an optional commute benchmark.
- New data files filled by the check-in's dashboard sync: wellness, fitness, activities, planned sessions and planned workout steps. Every panel shows a short note until its data arrives.
- Readiness is context, not a gate: the athlete's feel and the plan decide the session, the planned session is the default whatever the colour, and poor markers lead to an in-session checkpoint rather than a cancelled session. Hard sessions are never dropped on markers alone.
- Today's muscles are two body maps side by side: what today's strength session works, and what's been missing from the weekly targets over the last 14 or 28 days.

## 2026-10-29

- Setup now covers the whole system: devices and dashboard questions in the interview, step-by-step connections (intervals.icu via icuvisor, hosted or local; Garmin Personal API extension with a reviewed version and checksum; smart scale via a free iOS Shortcuts automation), training data as CSV files, a training dashboard built from a template, and a daily check-in skill.
- New: check-in skill template, dashboard template (muscle load body map, weekly targets, strength progression, season plan, sessions; optional left-vs-right and asymmetry modules), exercise-to-muscle catalogue (77 exercises).
- Strength sets are logged as CSV rows instead of a table in the strength log.
- Repository entry point: paste the link into Claude and it loads the kit.
- Weekly review is part of every setup: a scheduled task that reviews the training approach (adherence, load, progression, readiness patterns, what's working), suggests plan changes, writes a block review when a training phase ends, and redesigns the dashboard for the athlete as needs change.
- The daily check-in is now a readiness check-in: a green/amber/red rating from HRV (7-day trend against a normal band), resting HR, sleep, training load, Garmin Body Battery and stress, and how the athlete feels, which then decides the session.
- New: session debriefs (compliance, fade, decoupling, new bests, a verdict that drives progression), FTP management from the athlete's own performance (outdoor and indoor separately, with clear rules for when to change), and block reviews at the end of each phase. New data files: readiness, key sessions, FTP history.
- New permissions asked in the interview: whether Claude may delete future workouts it created, and whether it sets FTP itself or proposes it. icuvisor setup now covers the matching write and delete settings.
- Setting up again: a setup-export skill writes one document with all interview answers, decisions and current numbers; a new setup imports it and only asks what's missing.

## 2026-09-28

- First version: coaching instructions and a blank exercise and workout library (strength, cycling, running).
