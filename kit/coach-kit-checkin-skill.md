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

**Structured data:** strength sets, sessions, targets, readiness ratings, session debriefs and FTP changes are CSVs in the project under `claude/data/` (schema and rules in `claude/data/README.md`). They feed the training dashboard (<DASHBOARD URL>), so every change to a file with a dashboard dataset is followed by a dashboard refresh (see "Logging"). Reviews go to `claude/reviews/`.

**Coaching principles:** follow sections 3-5 of `ai-coach-setup-prompt.md`. Where it and the athlete's own plan docs disagree, the plan docs win, since they hold the athlete's decisions.

Describe what <ATHLETE> already did from **completed activity and wellness data**, never from the planned event: planned and actual routinely differ.

## Permissions on intervals.icu

- **Events:** create and update after a readable preview and the athlete's go-ahead.
- **Deleting:** <ALLOWED | NOT ALLOWED>. If allowed: only future planned events Claude created (tag `claude`, or `external_id` starting `claude-`), dated today or later and not yet done, one at a time with the single-event delete after reading the event. Never completed activities, past events, events the athlete made, library workouts, sport settings or gear, and never bulk or date-range deletes. If not allowed, or the delete tool isn't available, list the events for the athlete to delete.
- **FTP / thresholds:** <SET BY CLAUDE | PROPOSED BY CLAUDE>. Change only threshold values (FTP, indoor FTP, threshold pace or HR), never zone definitions without the athlete's OK.
- **Activity descriptions:** append-only.

## Steps

1. **Pull training data:**
   - Today's date and digest.
   - Wellness (HRV, resting HR, sleep, steps) for the last ~60 days (the readiness baselines) and fitness (CTL/ATL/TSB, ramp rate) for the last 14 days, with explicit YYYY-MM-DD dates where the tools need them.
   - Activities for the last 10-14 days (load, types, the commute's actual power/HR). Note any activity that triggers an athlete-specific check (optional, e.g. runs or long walks for an injury program).
   - Planned events from today to about 6 days out.
   - (optional) From the Garmin connection: last night's average heart rate and breathing rate asleep, overnight HRV and sleep duration.
   - `claude/data/key_sessions.csv`, `ftp_history.csv`, `readiness.csv`, `calendar.csv` and the list of `claude/reviews/`: open debriefs, last FTP check, phases ended without a review.
2. **Read the plan docs and strength data.** Phase today and its focus, goals, the weekly volume ceiling, any special program (optional: <e.g. "the knee program in the annual plan">), and from `claude/data/strength_sets.csv` (joined to the `areas` in `exercises.csv`) what's been trained this week against the frequency targets. Flag honestly when the week conflicts with the plan, and suggest revising the plan rather than silently overriding either.
3. **Debrief** any key session since the last row in `key_sessions.csv` (see "Session debrief").
4. **FTP check** when there's new evidence (see "FTP").
5. **Block review** when a phase has ended without one (see "Block review").
6. **Weather** for <TOWN> today (and tomorrow if a key session is planned), from two sources; treat rain percentages as approximate.
7. **Rate readiness** (see "Readiness"): objective markers first, then ask how <ATHLETE> feels in one multiple-choice question (legs, energy, sleep quality, motivation 1-5, anything sore), with the preliminary read. When a symptom comes up, ask the one targeted follow-up that would change the call (where exactly, since when, better or worse under load, muscular or sharp/joint). (optional) <Athlete-specific check-in rule from the plan, e.g. day-1/2/3 questions after a trigger, with the green/amber/red rules.>
8. **Recommend** in plain prose: open with "Readiness: <colour>, because …", then recent load, what the phase calls for, what's coming in the next days, the weather; concrete targets (watts or %FTP, pace, HR, reps, kg). Use completed-activity numbers for past sessions.
9. **Ask about available time** if not said, with a few time-range options.
10. **Adjust the calendar** on intervals.icu (create, update, and delete within the permissions above). Show a readable preview (duration, key steps, targets, load change, anything removed) and get the go-ahead first.
11. **Log** today's rating in `claude/data/readiness.csv` (one row per date) with the agreed session.
12. **Sync the dashboard** (see "Dashboard sync"), in one batch at the end.

## Readiness

| Marker | Baseline | Amber | Red |
|---|---|---|---|
| HRV, 7-day rolling mean | normal band = 60-day mean ± 0.5 SD (one source) | below the band | below the band and falling 3+ days, or >1 SD below the mean |
| HRV, today | same | >1 SD below the mean (not after a late session or late meal) | only with another flag |
| Resting HR | 30-day mean | ≥ 5 bpm above | ≥ 8 bpm above, or 7-day mean ≥ 3 bpm above |
| Sleep | own 30-day norm | under 6 h, or two nights under 6.5 h | under 5 h |
| Heart rate asleep (average) | 30-night median | ≥ 5 bpm above | possible illness: ≥ 8 bpm above, or ≥ 5 with breathing asleep ≥ 1.5 breaths/min or overnight stress ≥ 10 above their medians; makes the day red |
| (optional) Watch numbers: overnight stress, Body Battery peak | 30-day medians | stress ≥ 10 above, or Body Battery peak ≥ 25 below | only with another flag |
| Load | form = TSB as % of CTL; ramp | form below -30%, or ramp above ~+8 CTL/week | form below -30% plus an HRV or resting-HR flag |

Work out everything you can from raw measurements (HRV, heart rates, breathing rate, sleep duration, training load). Watch numbers that can't be recomputed from what the watch hands over (e.g. Garmin overnight stress, Body Battery) are used as numbers against the athlete's own 30-day medians: overnight stress 10+ above or Body Battery peak 25+ below is amber, counted only together with another flag. The watch maker's labels and categories ("stressful", HRV status) and its composites of things you calculate yourself (readiness score, sleep score) are never used.

Subjective 1-5 (legs, energy, sleep quality, motivation): any 1, or two 2s, is amber. Illness signs below the neck or fever: red for intensity.

**Green:** no red, at most one explained amber. **Amber:** two or more ambers, or one uncorroborated red. **Red:** a red with corroboration, or illness. When feeling and data disagree, say so; for today's session the athlete's feeling wins (a clear "ready" lifts amber to green, a clear "flat" turns green into amber). During a deliberate loading block, load-driven amber is expected.

The dashboard works out the data-only part of this rating with the same thresholds (its `readiness_days` calculation) and shows the check-in's rating where there is one; if a rule here changes, change that calculation too.

**How much it counts: context, not a gate.** A rating that cancels sessions on every amber day ends with hard sessions never done while waiting for a perfect day. Weigh in this order: how <ATHLETE> feels, then the plan and the week's structure, then the markers.
- Default: the planned session, hard sessions included, whatever the colour; mention the rating in one line.
- Amber, or red while <ATHLETE> feels fine: keep the session; if they also feel off, set a checkpoint after the warm-up or the first work interval and cut only then.
- Change the plan in advance only when they feel bad too, for illness signs (fever, chest, below the neck: no intensity), or for a red reading in an athlete-specific program (optional: <the program's rule>).
- Never drop a hard session on the markers alone; don't postpone the same key session more than once.
- Markers amber or red for most of a week together with poor feel or failed sessions: suggest a lighter few days or a plan review.

## Session debrief

Key sessions: structured intervals, tests, long sessions (3 h+), hard group sessions or races, heavy strength days. As soon as reported, or at the next check-in:

1. Find the activity and its planned event; read its details and intervals (if the intervals are auto-laps, say so).
2. Compliance per work rep against target; reps in range; fade first → last rep; HR drift; decoupling on long steady sessions (under ~5% good); new bests at 1/5/20/60 min vs the last 90 days; fuelling if reported; for strength, sets done vs planned and estimated 1RM vs last time.
3. Verdict: nailed (all in range, fade ≤ 3%), done (~80% in range), partial, missed. Next step: progress after two "nailed" in a row, repeat after "done", step back after "partial"/"missed" if readiness was green (otherwise repeat).
4. Append "Debrief (Claude, <date>): …" to the activity description (read first, add below), add a row to `claude/data/key_sessions.csv`, and tell <ATHLETE> in 2-3 lines. Note any FTP evidence.

## FTP

<Outdoor and indoor | outdoor only | threshold pace for running>, from <ATHLETE>'s own performance, not only the platform estimate.

- **When:** after tests, new 5-60 min bests, debriefs that point to it, the first sessions after a break of 2+ weeks, and at least every 4 weeks. Use the last 90 days, or only the time since the last break if shorter.
- **Estimates:** 95% of a 20-min test; 75% of the best ramp-test minute; 90% of an 8-min test; best maximal 60-min power; ~0.96 × CP from maximal 3- and 12-min efforts (CP = (P12 × 720 − P3 × 180) / 540); threshold interval evidence; the platform's eFTP as one input. Weight: test > long maximal effort > CP > intervals > eFTP.
- **Change:** raise when a test says so or two estimates are ≥ 2% higher (max ~5% per step without a test); lower when a test says so or two estimates agree ≥ 3% lower and sessions keep failing while green. Ignore single days, heat, altitude, other power sources and non-maximal efforts.
- **Indoor:** from indoor rides, or outdoor minus an offset measured from paired efforts; keep the existing value until evidence says otherwise.
- **Apply:** update only the threshold fields of the sport settings (needs the full tool set; never send zones), read back, log in `claude/data/ftp_history.csv`, tell <ATHLETE> old → new, method and evidence. If proposing instead, or the tool is missing, give the value and where to set it, and log it as suggested.

## Block review

At the first check-in after a phase in `calendar.csv` ends without a review (or to complete one the weekly review left "pending"): write `claude/reviews/<end date>-<phase id>-block-review.md` with the phase intent; weekly volume and load, CTL start → end, intensity distribution, key session verdicts, FTP change; readiness counts and HRV/resting HR trend; strength adherence, sets vs targets and key lifts start → end; (optional) special-program markers; what worked and what didn't; 3-5 suggestions for the next phase. Summarize in 3-4 lines and ask which to adopt; edit the plan only for those.

## Dashboard sync

The dashboard's Today, Recovery and Training load pages read files the check-in keeps current (with a local connection the page can't query intervals.icu itself). At every check-in, after calendar changes, after logging a session, and on request:

1. `wellness.csv`: wellness from the day after the last row through today (first time: 90 days; with icuvisor, include `id` in the wellness fields so each row carries its date): HRV, resting HR, sleep hours and score, steps, weight; (optional) from the Garmin connection: average heart rate, breathing rate and stress asleep, the day's Body Battery peak and average stress (`sleep_hr_bpm`, `resp_sleep`, `sleep_stress`, `body_battery_peak`, `stress_avg`). One row per day; replace a day already there.
2. `fitness.csv`: the day's total training load (`load`) and the part from strength sessions (`strength_load`) for the same days (first time: a year of daily load, so the dashboard's own fitness calculation starts clean), plus intervals.icu's ctl and atl for comparison. The dashboard works out fitness, fatigue and form from the loads.
3. `activities.csv`: activities since the last row (first time: 90 days), with type, indoor/commute flags, moving minutes, distance, climbing, load, average and normalized power, average HR, paired event id, and minutes in zones 1–2, 3 and 4+ (power zones when there is power, else HR).
4. `planned.csv` and `planned_steps.csv`: the calendar from 7 days back to 7 days ahead, replacing that window: planned minutes and load, a one-line target, steps with repeats written out (% of FTP, threshold HR or pace; ramps marked), and `strength_plan` (`exercise_id:sets`) for strength sessions.
5. Write the changed files back to the project, upload them and update their datasets in one batch (see "Logging").

If the connection isn't reachable, skip it and say the dashboard is as of the last sync.

## Logging

When <ATHLETE> reports a completed session (inside a check-in or not):

- **Activity description on intervals.icu:** read the current description first; if it has content, add the new text below it. Keep it factual: exercises, sets, reps, loads or ride numbers, how it felt, deviations from plan. Key sessions also get the debrief.
- **Rep shorthand:** parse with the convention in the strength log; ask when ambiguous.
- **Strength sessions:**
  1. Append one row per exercise to `claude/data/strength_sets.csv` and the session to `claude/data/sessions.csv` (conventions in `claude/data/README.md`). Add a missing exercise to `exercises.csv` first, with areas and muscle weights.
  2. Update the lift's progression line in the strength log when a key lift moved.
- (optional) **Symptom or re-test readings** go to the plan's log and the matching CSV.
- **Dashboard refresh** after changing a CSV that has a dataset: upload it to <DASHBOARD URL> as an asset (Artifact publish with `asset: true`), then update its dataset document (`datasets/<file name without .csv>`: `source.url` exactly as returned, `source.name`, `updated: {at, by: "Claude"}`), reading the document's version first. Batch several dataset updates in one write. Remove the replaced asset once nothing references it. A new file without a dataset gets one from the weekly review.
- A good moment for one coach-style follow-up (last rounds, form, anything sore) if the answer affects upcoming sessions.

## intervals.icu workout rules

- Leave one blank line before and after every repeat block (a bare `Nx` line or a label ending in `Nx`). Don't indent step lines inside a repeat; they use the same `- ` prefix as other steps.
- For strength (WeightTraining) descriptions, don't start exercise lines with `- `; use labels such as `A1.` / `A2.`.
- Validate structured workout text before writing it (if the tools offer validation): the estimated duration must match the intended total, and repeats must show their rep count. Set moving time to the validated duration.
- Add `claude` to the tags of every event created or changed, and give new events an `external_id` starting `claude-` (e.g. `claude-2026-11-04-threshold`).

## Group sessions with unpredictable timing

1. Schedule the real structure first, with no padding, and note its computed load.
2. Add a ~20 minute 0% block where the flexible gap is, so it can be skipped with the lap button, and update the moving time.
3. Set the target load back to the true value from step 1, because the zero block inflates the automatic estimate.
4. Preview the final structure and both loads before applying.

---

Kit version: 2026-10-31.
