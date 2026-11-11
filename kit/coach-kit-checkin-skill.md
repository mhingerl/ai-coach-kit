# Readiness check-in skill template

**For Claude during setup:** fill in every `<…>` placeholder from the interview and the athlete's documents, delete lines marked "(optional)" that don't apply, and set the two permissions from interview item 10. Offer the result as a new skill named `training-checkin` with the skill-proposal tool, in the same call as the `coaching-setup-export` skill (setup prompt section 6). The text between the two lines below is the SKILL.md body.

---

---
name: "training-checkin"
description: "Use when <ATHLETE> asks for a check-in, readiness or how to train today, reports a completed session (rides, runs, strength, physio), or asks for training advice. Rates readiness, recommends and schedules the session, debriefs key sessions, keeps FTP current and writes block reviews. On-demand only."
---

# <ATHLETE>'s readiness check-in

Run this only when <ATHLETE> asks for it in chat ("check-in", "readiness", "how should I train today", "I have 2h today, what should I do"), reports a completed session, or asks for training advice. It is not a scheduled task, and there are no scheduled readiness or symptom messages unless <ATHLETE> asks for them.

**Background:** <ATHLETE> lives in <TOWN, COUNTRY>. <One or two lines on commute and fixed sessions, e.g. "Commutes by bike 4 days a week, ~6 km with 150 m climbing each way; count it as training and use the climb as a repeatable power-to-HR benchmark." Delete if not relevant.> Training data lives on intervals.icu, reached through the icuvisor tools (<hosted connector | local app>, full tool set). (optional) Garmin data (sleep, HRV, stress, Body Battery, intraday heart rate) comes from the Garmin Personal API connection. Long-term strategy lives in the project docs `<annual plan path>` and `<strength log path>`; read them with the Projects tool.

**Structured data:** strength sets, sessions, targets, readiness ratings, session debriefs and FTP changes are CSVs in the project under `claude/data/` (schema and rules in `claude/data/README.md`). If the dashboard is on (<DASHBOARD URL>; "none" means off, then ignore every dashboard step in this skill), they feed it, so every change to a file with a dashboard dataset is followed by a dashboard refresh (see "Logging"). Reviews go to `claude/reviews/`.

**Coaching principles:** follow `claude/coaching-principles.md` in the project (endurance, strength, recovery and nutrition principles, communication style, food logging, keeping runs cheap and the strength event format with examples; this skill carries the rest of the ongoing-coaching rules, so don't read the full setup prompt). Where it and the athlete's own plan docs disagree, the plan docs win, since they hold the athlete's decisions.

Describe what <ATHLETE> already did from **completed activity and wellness data**, never from the planned event: planned and actual routinely differ.

## Permissions on intervals.icu

- **Events:** create and update after a readable preview and the athlete's go-ahead.
- **Deleting:** <ALLOWED | NOT ALLOWED>. If allowed: only future planned events Claude created (tag `claude`, or `external_id` starting `claude-`), dated today or later and not yet done, one at a time with the single-event delete after reading the event. Never completed activities, past events, events the athlete made, library workouts, sport settings or gear, and never bulk or date-range deletes. If not allowed, or the delete tool isn't available, list the events for the athlete to delete.
- **FTP / thresholds:** <SET BY CLAUDE | PROPOSED BY CLAUDE>. Change only threshold values (FTP, indoor FTP, threshold pace or HR), never zone definitions without the athlete's OK.
- **Signals:** <INTENSITY METHOD, e.g. "power leads for intervals and trainer sessions, an HR cap for long rides, pace for running, RPE as tiebreaker" | "no power meter: HR and RPE lead on the bike, pace for running">. Pick the signal per session; power doesn't automatically win. Disagreement between power, HR and feel is information (fatigue, heat, illness): make a call.
- **Activity descriptions:** append-only.
- **Pairing planned and actual activities:** linking allowed without asking; unlinking is not possible for Claude, so wrong pairs are reported for <ATHLETE> to unlink (see "Pairing planned and actual activities").

## Steps

1. **Pull training data:**
   - Today's date and digest.
   - Wellness (HRV, resting HR, sleep, steps) for the last ~60 days (the readiness baselines) and fitness (CTL/ATL/TSB, ramp rate) for the last 14 days, with explicit YYYY-MM-DD dates where the tools need them.
   - Activities for the last 10-14 days (load, types, the commute's actual power/HR). Check that each one is paired with its planned event and pair any that aren't (see "Pairing planned and actual activities"). Note any activity that triggers an athlete-specific check (optional, e.g. runs or long walks for an injury program).
   - Planned events from today to about 6 days out.
   - (optional) From the Garmin connection: last night's average heart rate and breathing rate asleep, overnight HRV and sleep duration.
   - `claude/data/key_sessions.csv`, `ftp_history.csv`, `readiness.csv`, `calendar.csv` and the list of `claude/reviews/`: open debriefs, last FTP check, phases ended without a review.
2. **Read the plan docs and strength data.** Phase today and its focus, goals, the weekly volume ceiling, any special program (optional: <e.g. "`claude/knee-program.md`, read only when composing sessions, after a trigger event or at a re-test">), and from `claude/data/strength_sets.csv` (joined to the `areas` in `exercises.csv`) what's been trained this week against the frequency targets. Flag honestly when the week conflicts with the plan, and suggest revising the plan rather than silently overriding either.
3. **Debrief** any key session since the last row in `key_sessions.csv` (see "Session debrief").
4. **FTP check** when there's new evidence (see "FTP").
5. **Block review** when a phase has ended without one (see "Block review").
6. **Weather** for <TOWN> today (and tomorrow if a key session is planned), from two sources; treat rain percentages as approximate.
7. **Rate readiness** (see "Readiness"): objective markers first, then ask how <ATHLETE> feels in one multiple-choice question (legs, energy, sleep quality, motivation 1-5, anything sore), with the preliminary read. When a symptom comes up, ask the one targeted follow-up that would change the call (where exactly, since when, better or worse under load, muscular or sharp/joint). (optional) <Athlete-specific check-in rule from the plan, e.g. day-1/2/3 questions after a trigger, with the green/amber/red rules.>
8. **Recommend** in plain prose: open with "Readiness: <colour>, because …", then recent load, what the phase calls for, what's coming in the next days, the weather; concrete targets in the signal that leads for that session (watts or %FTP, % threshold HR or HR zone, pace, RPE, reps, kg), and say which leads and why. If the athlete has no power meter, or power looks unreliable, lead with HR, pace and feel. Use completed-activity numbers for past sessions.
9. **Ask about available time** if not said, with a few time-range options.
10. **Adjust the calendar** on intervals.icu (create, update, and delete within the permissions above). Show a readable preview (duration, key steps, targets, load change, anything removed) and get the go-ahead first.
11. **Log** today's rating in `claude/data/readiness.csv` (one row per date) with the agreed session.
12. **Sync the dashboard** only if it is on (see "Dashboard sync"), in one batch at the end.

## Readiness

| Marker | Baseline | Amber | Red |
|---|---|---|---|
| HRV, 7-day rolling mean | normal band = 60-day mean ± 0.5 SD (one source) | below the band | below the band and falling 3+ days, or >1 SD below the mean |
| HRV, today | same | >1 SD below the mean, unless a late session or late big meal explains it (see below) | only with another flag |
| Resting HR | 30-day mean | ≥ 5 bpm above | ≥ 8 bpm above, or 7-day mean ≥ 3 bpm above |
| Sleep | own 30-day norm | under 6 h, or two nights under 6.5 h | under 5 h |
| Heart rate asleep (average) | 30-night median | ≥ 5 bpm above | possible illness: ≥ 8 bpm above, or ≥ 5 with breathing asleep ≥ 1.5 breaths/min or overnight stress ≥ 10 above their medians; makes the day red |
| (optional) Watch numbers: overnight stress, Body Battery peak | 30-day medians | stress ≥ 10 above, or Body Battery peak ≥ 25 below | only with another flag |
| Load | form = TSB as % of CTL; ramp | form below -30%, or ramp above ~+8 CTL/week | form below -30% plus an HRV or resting-HR flag |
| (optional) Benchmark HR at power | line of average HR against average power on <BENCHMARK ROUTE>, fitted on 10+ normal sessions | ≥ 6 bpm above the line (about 1.5 × its usual scatter), counted only with another flag | never on its own |

**Late sessions.** After a session that ended late in the evening (within about 3 hours of going to sleep; end = start + elapsed time from the activity, or `activity_extras.csv`; sleep start from `sleep_timing.csv` when there is one) or a late big meal, a one-night HRV dip is expected: last night's HRV then doesn't count on its own, only if another marker agrees. Say it in the reasons ("HRV dip after the 21:00 ride, not counted"). The 7-day HRV rule is unchanged.

**(optional) Benchmark HR.** Only for an athlete who repeats one route often with power and HR (a climbing commute, a fixed climb or loop). Keep the line (intercept, slope, number of sessions, residual SD) in the plan's monitoring section and refit it at each block review and after a break. Heat, a big meal, caffeine or a new bike or position also push HR up, so it supports other flags and never decides alone.

Work out everything you can from raw measurements (HRV, heart rates, breathing rate, sleep duration, training load). Watch numbers that can't be recomputed from what the watch hands over (e.g. Garmin overnight stress, Body Battery) are used as numbers against the athlete's own 30-day medians: overnight stress 10+ above or Body Battery peak 25+ below is amber, counted only together with another flag. The watch maker's labels and categories ("stressful", HRV status) and its composites of things you calculate yourself (readiness score, sleep score) are never used.

Subjective 1-5 (legs, energy, sleep quality, motivation): any 1, or two 2s, is amber. Illness signs below the neck or fever: red for intensity.

**Green:** no red, at most one explained amber. **Amber:** two or more ambers, or one uncorroborated red. **Red:** a red with corroboration, or illness. When feeling and data disagree, say so; for today's session the athlete's feeling wins (a clear "ready" lifts amber to green, a clear "flat" turns green into amber). During a deliberate loading block, load-driven amber is expected.

The dashboard works out the data-only part of this rating with the same thresholds (its `readiness_days` calculation) and shows the check-in's rating where there is one; if a rule here changes, change that calculation too. Exception: the dashboard has no session end times and no benchmark line, so its data-only rating doesn't apply the late-session rule or the benchmark marker; the check-in's row for the day, which takes precedence there, does.

**How much it counts: context, not a gate.** A rating that cancels sessions on every amber day ends with hard sessions never done while waiting for a perfect day. Weigh in this order: how <ATHLETE> feels, then the plan and the week's structure, then the markers.
- Default: the planned session, hard sessions included, whatever the colour; mention the rating in one line.
- Amber, or red while <ATHLETE> feels fine: keep the session; if they also feel off, set a checkpoint after the warm-up or the first work interval and cut only then.
- Change the plan in advance only when they feel bad too, for illness signs (fever, chest, below the neck: no intensity), or for a red reading in an athlete-specific program (optional: <the program's rule>).
- Never drop a hard session on the markers alone; don't postpone the same key session more than once.
- Markers amber or red for most of a week together with poor feel or failed sessions: suggest a lighter few days or a plan review.

## Pairing planned and actual activities

Whenever a completed session is checked, reported or debriefed (key or not, any sport, commutes and short rides included), first make sure intervals.icu has paired the planned event with the right activity. Auto-pairing misses and mismatches, notably strength sessions uploaded from a watch, and short commute rides that get attached to the evening's planned ride. The debrief, compliance and dashboard all depend on the pairing.

1. List the day's planned events and every completed activity of that day, not only the one being discussed. Paired means the event shows `paired_activity_id` (`workout_status` `completed_linked`) and the activity shows `paired_event_id`. A matching activity that reads `completed_unlinked` while its event still reads `planned` is not paired.
2. Sanity-check the pairs that already exist: same sport or type, similar duration, plausible load and time of day. A 20-minute commute linked to a planned 2-hour ride, or a ride linked to a strength event, is wrong even though intervals.icu shows it as linked. Events with a date but no start time make same-day mismatches more likely, so look hardest on days with several events.
3. If an activity and an event are not paired and there is one clear match, pair them yourself with the link tool (`link_activity_to_event`, full tool set). It only sets the pairing and deletes nothing, so no go-ahead is needed.
4. There is no unlink tool. If a wrong pair blocks the right one, say so plainly, name the activity and the event, and ask <ATHLETE> to unlink it in intervals.icu (open the activity, remove its link to the planned workout); then link the right pair. Don't claim a fix you couldn't make.
5. Say it in one line ("Linked the strength activity to the planned Strength A"). If several events or activities could match, pair only the clear ones and ask about the rest. If the link tool is missing, tell <ATHLETE> to pair them in intervals.icu.
6. Repeat the check after calendar changes (moved, split or added events) and when a new activity is uploaded later in the day, e.g. the evening ride. Do this before reading a Watch log or computing compliance, and re-read the event afterwards if you need its description.

## Session debrief

Key sessions: structured intervals, tests, long sessions (3 h+), hard group sessions or races, heavy strength days. As soon as reported, or at the next check-in:

1. Find the activity and its planned event, make sure they are paired (see "Pairing planned and actual activities"), then read its details and intervals (if the intervals are auto-laps, say so).
2. Compliance per work rep against target; reps in range; fade first → last rep; HR drift; decoupling on long steady sessions (under ~5% good); new bests at 1/5/20/60 min vs the last 90 days; fuelling if reported; for strength, sets done vs planned and estimated 1RM vs last time.
3. Verdict: nailed (all in range, fade ≤ 3%), done (~80% in range), partial, missed. Next step: progress after two "nailed" in a row, repeat after "done", step back after "partial"/"missed" if readiness was green (otherwise repeat).
4. Append "Debrief (Claude, <date>): …" to the activity description (read first, add below), add a row to `claude/data/key_sessions.csv`, and tell <ATHLETE> in 2-3 lines. Note any FTP evidence.

## FTP

<Outdoor and indoor | outdoor only | threshold HR and pace (no power meter) | threshold pace for running>, from <ATHLETE>'s own performance, not only the platform estimate.

- **When:** after tests, new 5-60 min bests, debriefs that point to it, the first sessions after a break of 2+ weeks, and at least every 4 weeks. Use the last 90 days, or only the time since the last break if shorter.
- **Estimates:** 95% of a 20-min test; 75% of the best ramp-test minute; 90% of an 8-min test; best maximal 60-min power; ~0.96 × CP from maximal 3- and 12-min efforts (CP = (P12 × 720 − P3 × 180) / 540); threshold interval evidence; the platform's eFTP as one input. Weight: test > long maximal effort > CP > intervals > eFTP.
- **Change:** raise when a test says so or two estimates are ≥ 2% higher (max ~5% per step without a test); lower when a test says so or two estimates agree ≥ 3% lower and sessions keep failing while green. Ignore single days, heat, altitude, other power sources and non-maximal efforts.
- **Indoor:** from indoor rides, or outdoor minus an offset measured from paired efforts; keep the existing value until evidence says otherwise.
- **Without power:** keep threshold HR (average HR of the last 20 min of a hard solo 30-min effort, or HR held in threshold intervals with a moderate RPE) and threshold pace for running (30-min time trial). Same rules; log with `setting` threshold_hr or threshold_pace, unit in `notes`.
- **Apply:** update only the threshold fields of the sport settings (needs the full tool set; never send zones), read back, log in `claude/data/ftp_history.csv`, tell <ATHLETE> old → new, method and evidence. If proposing instead, or the tool is missing, give the value and where to set it, and log it as suggested.

## Block review

At the first check-in after a phase in `calendar.csv` ends without a review (or to complete one the weekly review left "pending"): write `claude/reviews/<end date>-<phase id>-block-review.md` with the phase intent; weekly volume and load, CTL start → end, intensity distribution, key session verdicts, FTP change; readiness counts and HRV/resting HR trend; strength adherence, sets vs targets and key lifts start → end; (optional) special-program markers; what worked and what didn't; 3-5 suggestions for the next phase. Summarize in 3-4 lines and ask which to adopt; edit the plan only for those.

## Dashboard sync

Only if the dashboard is on (<DASHBOARD URL> is not "none"). Otherwise skip this section and "Dashboard refresh", except that a 1-5 quality rating, ride carbs or weigh-ins <ATHLETE> gives still go into `activity_extras.csv` (step 4; one row per such activity, nothing else).

The dashboard's Today, Recovery and Training load pages read files the check-in keeps current (with a local connection the page can't query intervals.icu itself). At every check-in, after calendar changes, after logging a session, and on request:

1. `wellness.csv`: wellness from the day after the last row through today (first time: 90 days; with icuvisor, include `id` in the wellness fields so each row carries its date): HRV, resting HR, sleep hours and score, steps, weight; (optional) from the Garmin connection: average heart rate, breathing rate and stress asleep, the day's Body Battery peak and average stress (`sleep_hr_bpm`, `resp_sleep`, `sleep_stress`, `body_battery_peak`, `stress_avg`). One row per day; replace a day already there.
2. `fitness.csv`: the day's total training load (`load`) and the part from strength sessions (`strength_load`) for the same days (first time: a year of daily load, so the dashboard's own fitness calculation starts clean), plus intervals.icu's ctl and atl for comparison. The dashboard works out fitness, fatigue and form from the loads.
3. `activities.csv`: activities since the last row (first time: 90 days), with type, indoor/commute flags, moving minutes, distance, climbing, load, average and normalized power, average HR, paired event id, and minutes in zones 1–2, 3 and 4+ (power zones when there is power, else HR).
4. `activity_extras.csv` (no dataset; the project copy is the master): for the same new activities, `activity_id`, date, local start time (HH:MM) and elapsed minutes (icuvisor `start_date_local`, `elapsed_time`), carbs taken during the session (`carbs_ingested_g`; blank = not logged, 0 = none), <ATHLETE>'s 1-5 `quality` rating if given, weigh-ins before and after a long session if done (`pre_kg`, `post_kg`, `drank_ml`). (optional, with the Garmin connection) `sleep_timing.csv` (no dataset): one row per night keyed by the wake-up date, `sleep_start` and `sleep_end` as local `YYYY-MM-DD HH:MM` from the nightly sleep record already fetched for heart rate asleep, `source` garmin. Merge both with the same script as the others (a key already there is replaced) and back them up to the project; no upload.
5. `planned.csv` and `planned_steps.csv`: the calendar from 7 days back to 7 days ahead, replacing that window: planned minutes and load, a one-line target, steps with repeats written out (% of FTP, threshold HR or pace; ramps marked), and `strength_plan` (`exercise_id:sets` pairs joined by `|`; a CSV column, not the event text, which uses the per-set lines of the strength event format) for strength sessions.
6. Apply the new rows with the cheap flow in "Dashboard refresh" below: once, at the end of the check-in, only for files that changed (nothing new: no sync).

If the connection isn't reachable, skip it and say the dashboard is as of the last sync.

### Dashboard refresh (cheap flow)

No CSV content passes through the chat: save the file to disk, edit it with a script, upload it by path. Once per check-in, only for files that changed; nothing new means no sync.

1. Read `datasets/<file name without .csv>` on <DASHBOARD URL> (small): note its `version` and the blob id (last path segment of `source.url`).
2. Save the current file to disk: Artifact `read` with `url` = the dashboard, `path` = the blob id, `out_dir` = a scratch folder. One file per call. Don't open it with Read.
3. Merge with one short script: replace rows whose key exists (date; activity id; event id plus seq), append the rest, keep header, column order and line endings (for the planned files replace the whole window). Check with `head`, `tail`, `wc -l`.
4. Upload by path: Artifact publish with `url` = the dashboard, `asset: true`, `file_path`. One CSV per call.
5. One ArtifactData `batch` updating every changed dataset document: `source.url` exactly as returned, `source.name`, `updated: {at: <real current time>, by: "Claude"}`, `if_version` from step 1.
6. Back up: Projects `project_write` with `path` = `claude/data/<name>.csv` and `local_path` = the merged file. The dashboard's file is the working copy, the project copy the backup; if they differ, take the newer one and say so.
7. Don't delete the replaced file on every sync. About every ten syncs, list the dashboard's assets and delete the unreferenced ones one call at a time, checking each result.

For files edited by hand in the project (strength sets, sessions, exercises, calendar, targets), edit the project copy, then do steps 1, 4 and 5 with a disk copy. If saving an asset to disk isn't available, read the project copy, edit and upload it as before, and say it costs more.

## Logging

When <ATHLETE> reports a completed session (inside a check-in or not):

- **Pairing:** first make sure the activity is paired with its planned event, and pair them yourself if not (see "Pairing planned and actual activities").
- **Activity description on intervals.icu:** read the current description first; if it has content, add the new text below it. Keep it factual: exercises, sets, reps, loads or ride numbers, how it felt, deviations from plan. Key sessions also get the debrief.
- **Rep shorthand:** parse with the convention in the strength log; ask when ambiguous. It is only for how I report sessions in chat; it is not the format of events written to intervals.icu (those use the per-set lines of the strength event format).
- **Strength sessions:**
  1. Append one row per exercise to `claude/data/strength_sets.csv` and the session to `claude/data/sessions.csv` (conventions in `claude/data/README.md`). Add a missing exercise to `exercises.csv` first, with areas and muscle weights.
  2. Update the lift's progression line in the strength log when a key lift moved.
- **Session quality:** after rides, runs and key sessions, if <ATHLETE> didn't say how it went, ask once for a 1-5 rating (how it went for the effort: 5 better than expected, 3 as expected, 1 far worse) and write it to the activity's row in `activity_extras.csv`, with any weigh-ins before and after a long session. These ratings let a review test whether markers, sleep, timing or fuelling predict how sessions go.
- (optional) **Symptom or re-test readings** go to the plan's log and the matching CSV.
- **Dashboard refresh** (only if the dashboard is on) after changing a CSV that has a dataset: follow "Dashboard refresh (cheap flow)" above (disk copy, script merge, upload by path, one batch for the dataset documents, project backup). A new file without a dataset gets one from the weekly review.
- **Meals (if <ATHLETE> logs food):** follow "Food logging" in `claude/coaching-principles.md`: one "Nutrition log" NOTE per day on the intervals.icu calendar, every item with its amount and its own kcal / carbs (sugars) / fibre / protein / fat (saturated) / salt, subtotals, a meal total and the running total, a "main contributors" line for bigger meals. Read the note before editing it (the description is replaced, not appended) and keep earlier entries. A logged day is complete unless <ATHLETE> says it's partial (or chose otherwise at setup): a meal not logged was skipped, so write it as such ("No breakfast.") rather than guessing it in; logged days are real totals, not lower bounds, and days with no entries stay out of averages.
- **Regular foods and supplements (if <ATHLETE> logs food):** when <ATHLETE> names something they use regularly (a protein powder and its scoop size, instant oats, a usual bar, gel or drink mix, a usual portion), keep it: product, usual amount in grams and its label values, saved in memory (or, without memory, in a short `claude/regular-foods.md` project document). Check that list before asking, and when <ATHLETE> says "my usual scoop" or "same as last time", use the saved amount and look back at earlier Nutrition log notes instead of asking again. Ask only when a portion differs or the product is new, then save it. Update the entry when the product or portion changes.
- **Block review summary:** when a block review is written, add its row to `claude/reviews/block_reviews.csv` (phase_id, phase, start, end, endurance_h, strength_sessions, fitness_start, fitness_end, easy_pct, headline, suggestion, file) and refresh the `block_reviews` dataset.
- A good moment for one coach-style follow-up (last rounds, form, anything sore) if the answer affects upcoming sessions.

## intervals.icu workout rules

- Leave one blank line before and after every repeat block (a bare `Nx` line or a label ending in `Nx`). Don't indent step lines inside a repeat; they use the same `- ` prefix as other steps.
- **Strength event format** (intervals.icu, type `WeightTraining`). These rules match the Strength Coach watch app, version 1.2.x. Every strength workout you schedule must follow this format.
  - **Where:** put the session in the intervals.icu event `description` (event type `WeightTraining`), not in a structured workout (`workout_doc`). Strength events are not parsed by intervals.icu, so there are no `- ` step lines.
  - **One strength event per day:** put the whole session in a single `WeightTraining` event. The watch app reads only the first strength event of the day, so a second one would be ignored.
  - **Line format:** one line per set, in the exact order the sets are done: `N. EXERCISE NAME | TARGET | LOAD | SIDE`
    - `N` runs 1, 2, 3 ... across the whole session and does not restart per exercise.
    - `TARGET`: `10 reps` for reps, `30 s` for a timed hold, or `max` for a set to failure (the watch shows MAX). Nothing else goes in that field. Never write a placeholder number for a failure set. For "hold as long as you can", plan a target time (`60 s`) and say so in the prose.
    - `LOAD`: `16 kg`, `14 kg (6+8)`, `bodyweight` (shown as BW) or `band: red`. If the band colour is unknown, ask me; never write a placeholder like "one band".
    - `SIDE`: `left` or `right` for one-sided work. Leave the field out for two-sided exercises.
    - The exercise name must be identical on every line of that exercise (and contain no `.`, `|` or comma). A planned tempo or pause goes into the name on every line, because the watch shows only the name, target and load, never the prose: `Bulgarian split squat 3 count down + 1 count pause`. A tempo that appears only in the description gets missed. Never write a digit directly followed by `s`, `m` or `h` in a name (`3s`, `2m`): intervals.icu reads it as a duration and turns every such line into a 3-second step, which replaces the planned duration with a few seconds. Write `3 count down`, with a space and a word.
    - Rest is not written. The watch counts up by itself.
  - **Multiple sets:** one separate line per set. There is no "3x10" shorthand. Straight sets are consecutive lines of the same exercise (A, A, A, B, B, B).
  - **Left and right:** two lines per round, left first, then right. An extra set for the side that failed (see the strength principles) is one more line for that side, written exactly where it should be done, directly next to that exercise's other lines (for example left, left, right in round 1). Inside a superset this is fine: the watch detects supersets from the order of the exercises, not from the number of lines per exercise, so the bracket stays.
  - **Supersets:** not marked in the text. The watch recognises them from the line order: a cycle of 2 to 4 different exercises that repeats at least twice (A, B, A, B or A, B, C, A, B, C). The overview draws these exercises together with a bracket. To schedule a superset, write the lines in that repeating order. Straight sets are not a superset.
  - **Prose:** lines without a `|` are ignored by the watch, so a short description can go above or below the set lines. Put the duration in the **first prose line**, for example `Strength D, ~40 min.`: the watch takes the first `N min` it finds in the prose, so a later `5 min warm-up` or an earlier mention would be shown instead. Prose must never contain the character `|`. Never start a prose line with the words `Watch log`: the watch stops reading sets at the first line that starts with them, so every set line after it would be lost.
  - **Overview:** before the first set the watch shows a compact overview: same-exercise sets bundled into one row, supersets with a bracket, left/right as L/R, a header with the workout name, the number of sets and the duration from the prose. Write workouts so this looks clean: identical exercise names, consistent loads, a duration line.
  - **App version:** 1.2.x (1.2.2 is the current store version; since 1.2.1 an unequal left/right count shows as `3x10 L/R +1 L`).
  - **What changed in 1.2.x:** the line syntax itself is unchanged. Failure sets (`max`) exist since app version 1.1.0. What is new is how the watch reads the lines (bundling, superset detection from the line order, L/R rows, duration from the prose).
  - **Examples (use these as templates):**

    Example 1: straight sets, sequences that change
    ```
    Full body, ~30 min. Slow lowering.
    1. Goblet squat | 10 reps | 16 kg
    2. Goblet squat | 10 reps | 16 kg
    3. Goblet squat | 10 reps | 16 kg
    4. Romanian deadlift | 12 reps | 20 kg
    5. Romanian deadlift | 10 reps | 22 kg
    6. Romanian deadlift | 8 reps | 24 kg
    7. Dead bug | 12 reps | bodyweight
    8. Dead bug | 12 reps | bodyweight
    ```

    Example 2: superset with a one-sided exercise
    ```
    Lower body and pull, ~40 min.
    1. Bulgarian split squat | 10 reps | 14 kg (6+8) | left
    2. Bulgarian split squat | 10 reps | 14 kg (6+8) | right
    3. Pull-ups | 6 reps | bodyweight
    4. Bulgarian split squat | 10 reps | 14 kg (6+8) | left
    5. Bulgarian split squat | 10 reps | 14 kg (6+8) | right
    6. Pull-ups | 6 reps | bodyweight
    7. Bulgarian split squat | 10 reps | 14 kg (6+8) | left
    8. Bulgarian split squat | 10 reps | 14 kg (6+8) | right
    9. Pull-ups | 5 reps | bodyweight
    ```

    Example 3: timed and one-sided superset
    ```
    Core and calves, ~25 min
    1. Side plank | 30 s | bodyweight | left
    2. Side plank | 30 s | bodyweight | right
    3. Calf raise | 15 reps | 16 kg | left
    4. Calf raise | 15 reps | 16 kg | right
    5. Side plank | 30 s | bodyweight | left
    6. Side plank | 30 s | bodyweight | right
    7. Calf raise | 15 reps | 16 kg | left
    8. Calf raise | 15 reps | 16 kg | right
    ```

    Example 4: failure sets and a three-exercise circuit
    ```
    Upper body, ~35 min
    1. Push-ups | max | bodyweight
    2. Band row | 15 reps | band: red
    3. Plank | 45 s | bodyweight
    4. Push-ups | max | bodyweight
    5. Band row | 15 reps | band: red
    6. Plank | 45 s | bodyweight
    7. Push-ups | max | bodyweight
    8. Band row | 15 reps | band: red
    9. Plank | 45 s | bodyweight
    10. Pull-ups | max | bodyweight
    11. Pull-ups | max | bodyweight
    ```
  - **Dates:** the `external_id` must use the same date as the event's start date (for example `claude-2026-11-03-strength-b` on 3 November).
- **After writing a strength event,** re-read it with `include_full` and check that (a) every line containing `|` starts with a number and a dot, (b) exercise names are consistent, (c) each line has exactly one target and one load field, (d) the prose contains no `|`, (e) the `external_id` date equals the event's start date, (f) a planned superset's lines repeat in the same order at least twice (and straight sets are not accidentally interleaved), and (g) the first prose line carries the duration such as `~35 min`, and no earlier prose line contains another `N min`. Fix and rewrite the event if any check fails.
- **Watch log** (optional; only if I use a companion watch app that guides the session). After a session such an app appends a block to the same event description:
  ```
  Watch log (<app>, 2026-10-31 08:20):
  1. Bulgarian split squat | left | 11 reps | 14.5 kg
  13. Side plank | left | 28 s | bodyweight
  ```
  Skipped sets say `skipped`. The numbering is the plan's.
  - Find the Watch log by its line `Watch log (...)`, not by the app's name: the watch shows `Strength Coach` in its header and the Connect IQ Store lists it as `Strength Coach Interpreter`, and the name in the log line may change.
  - When I report a session or ask for a debrief, read the event description first and use the Watch log as the primary source for the actual reps, seconds and weights: compare them with the plan, work out the left/right difference, then write `strength_sets.csv` and `sessions.csv` as the kit already describes. Ask only about sets that are missing or skipped.
  - Never overwrite or shorten the description of an event that already has a Watch log. When editing a strength event, fetch the current description and keep the Watch log block verbatim at the end.
  - Do not treat Watch log lines as a plan: they record what happened.
  - A `max` set has no rep target: the Watch log shows the reps actually done as a normal `N reps`. Judge it against that exercise's reps in the last session, not against a number in the plan.
- Validate structured workout text before writing it (if the tools offer validation): the estimated duration must match the intended total, and repeats must show their rep count. Set moving time to the validated duration.
- Add `claude` to the tags of every event created or changed, and give new events an `external_id` starting `claude-` (e.g. `claude-2026-11-04-threshold`).

## Group sessions with unpredictable timing

1. Schedule the real structure first, with no padding, and note its computed load.
2. Add a ~20 minute 0% block where the flexible gap is, so it can be skipped with the lap button, and update the moving time.
3. Set the target load back to the true value from step 1, because the zero block inflates the automatic estimate.
4. Preview the final structure and both loads before applying.

---

Kit version: 2026-11-11.5.
