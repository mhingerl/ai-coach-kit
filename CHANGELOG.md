# Changelog

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
