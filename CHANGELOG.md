# Changelog

The newest kit version is also in the one-line [`VERSION`](VERSION) file. Entries from 2026-11-05 on start with a *Touches:* line (what the change affects) and an *If you already use the kit:* line.

## 2026-11-12.3

**Read first: this version needs the coach data extension. You can stay on your current version.** From here the kit works only through its own extension (a Claude desktop app on a Mac or Windows computer), which replaces icuvisor and the separate Garmin extension. Your current kit keeps working with icuvisor and the Garmin extension, but it receives no more updates. Choose one: (a) **update**: install the extension first ([download `coach-data.mcpb`](https://github.com/mhingerl/ai-coach-kit/releases/latest/download/coach-data.mcpb), then the steps below); or (b) **stay on the old kit**: but first bring it up to date, because 2026-11-12.2 is the last version that works without the extension and you may not have it yet. Update to 2026-11-12.2 by applying the changelog entries below this one, up to and including 2026-11-12.2, **and fetch every file for those versions from the `kit-legacy` tag, not from main** (for example `https://raw.githubusercontent.com/mhingerl/ai-coach-kit/kit-legacy/kit/ai-coach-setup-prompt.md`), because main now holds the new files. Once you are on 2026-11-12.2, tell your coach "stay on my kit version" and it stops reminding you. Do not apply this entry (2026-11-12.3) unless you chose (a). Nothing changes in your project until you say so.

*Touches:* the whole connection layer: README, setup prompt (what you need, interview items 3 and Garmin, 2.2 items 2 and 3, weekly connection check, pairing), the check-in skill template (data pull, permissions, debriefs, thresholds, logging, dashboard sync) and a new `extension/` folder. The "Writing workouts to intervals.icu" subsection changed, so regenerate `coaching-principles.md`.

Install steps for the extension: in the Claude desktop app open Settings → Extensions → Advanced settings → Install Extension…, choose the file and fill in its settings (details in `extension/INSTALL.md`).

The extension in this version (0.10.1) can also write any wellness field (with overwrite protection), manage the workout library and apply library plans, build a season plan, and ties in with the Strength Coach and Scale Linker watch apps (writes strength sessions in the watch's format, reads the Watch log and weigh-ins, never overwrites the Watch log). It also reads activity streams, best efforts and power curves (so debriefs and threshold checks no longer need icuvisor), can read your own `.fit` files from a folder, fills `strength_plan` in `planned.csv` from your strength events when `exercises.csv` is in the data folder, and has an optional hosted HTTP version for phone and web chats (see `docs/hosted.md` in the extension's repo; not deployed yet).

*If you already use the kit (ask your coach "update me to kit 2026-11-12.3"; it should say the notice above first, follow these steps and ask before changing anything):*
1. **Install the coach data extension** (see above): intervals.icu API key, athlete ID, time zone; optional Garmin key (the one you already created, or a new one; no separate Garmin extension any more), data folder and Write mode. Ask the coach to run `coach_status` and `coach_digest` and show you the result.
2. **Update your saved check-in skill card** from the new template (`kit/coach-kit-checkin-skill.md`): keep your athlete-specific rules; take the new "Background" tool line, the Deleting, pairing and threshold lines and the data-pull note. Easiest: let the coach redo the template with your existing rules and offer it as one skill card.
3. **Write mode:** the extension ships with Write mode `full` (create and update workouts and notes, pair activities, carbs, thresholds, delete single future events the coach created). If you don't want the coach to delete, set it to `safe`, or to `off` for read-only, in Settings → Extensions → the extension → Write mode.
4. **After one full check-in worked with the extension,** remove icuvisor and the Garmin extension in Settings → Extensions.
5. **Regenerate `claude/coaching-principles.md`** from the new setup prompt (2.5, item 3), overwriting the old file.
6. **Keep the project tidy (replace, don't duplicate):** save the five kit files from `kit/` over the old ones under the same names, replace the old check-in skill card instead of adding a second one, and delete nothing else without asking. With a data folder set, `wellness.csv`, `fitness.csv`, `activities.csv`, `sleep_timing.csv`, `planned.csv` and `planned_steps.csv` now live in that folder: once `coach_sync` has filled them and `coach_status` shows at least as many rows as your project copies, the coach lists the project copies (in `claude/data/`) and, after you say yes, deletes them. Also copy `exercises.csv` into the data folder. Your own files (strength sets, sessions, readiness, key sessions, threshold history, `activity_extras.csv`, calendar, targets) stay where they are. Old instructions for icuvisor and the Garmin extension in your own notes or scheduled-task prompts are listed for you to replace.
7. **Phone and web chats:** they cannot use the extension and cannot change your calendar any more. Ask the coach on the computer to "update my snapshot"; it saves `claude/data/snapshot.md` in your Project, which chats on your phone read for recent data.

- Changed: intervals.icu is recommended, not required. One data source is enough: intervals.icu, a Garmin Personal API key, or your own FIT files; more is better. Without intervals.icu the coach reads your data but cannot write to a calendar, so it gives sessions in the chat.
- Changed: the kit's connection to intervals.icu and Garmin is one extension that ships in this repository. It reads a compact digest, reads and writes calendar events and notes (only events the coach created can be changed or deleted), pairs activities, sets carbs and thresholds, and keeps the kit's data files (wellness, fitness, activities, sleep timing, planned sessions and their steps) up to date in a folder on your computer.
- Changed: setup installs the extension instead of icuvisor and the Garmin extension. The weekly connection check runs `coach_status` and reports newer extension versions from this changelog.
- Removed: the hosted intervals.icu connector option (it worked on the phone). Chats on the phone now read a snapshot and cannot change the calendar.
- New: a 3 KB snapshot (`claude/data/snapshot.md`) for chats on the web or phone.

## 2026-11-12.2

*Touches:* setup prompt (section 4/5, "Writing workouts to intervals.icu": new rule on event names) and the check-in skill template ("intervals.icu workout rules"). Section 4/5 changed, so regenerate `coaching-principles.md`.
*If you already use the kit (ask your coach "update me to kit 2026-11-12.2"; it should follow these steps and ask before changing anything):*
1. **Garmin bike computer or watch users: shorten the names of your planned workouts.** Look at the events on your intervals.icu calendar from today on that the coach created. Rename any whose name is longer than about 25 characters or has colons, brackets or suffixes like `(outdoor)` (for example `Endurance 80 min + primers (outdoor)` becomes `Endurance 80 + primers`), keeping the description and steps unchanged. Show the new names and ask before changing them.
2. **Update your saved check-in skill card:** in the intervals.icu workout rules add: keep event names short and plain (about 25 characters, no colons, brackets or `(outdoor)` suffixes).
3. **Regenerate `claude/coaching-principles.md`** from the new setup prompt (2.5, item 3).

- New: a rule for event names. Long names with symbols synced from intervals.icu to a Garmin Edge 530 with the name shown as a line or underscores and no steps, although intervals.icu showed the event and its steps correctly. Renaming to a short plain name and saving again fixed it. Whether length, the colon or the brackets is the cause is not confirmed, so the rule limits all three; a 22-character name with a plus sign worked. If a device shows a blank name or missing steps, the coach checks the event in intervals.icu first, then shortens the name and re-saves it.

## 2026-11-12.1

*Touches:* setup prompt (what you need, Step 0 interview item 1 and its actions, 2.2 items 1 and 3, the check-in's data pull in section 3) and README. No change to section 4 or 5, so `coaching-principles.md` stays as it is.
*If you already use the kit (ask your coach "update me to kit 2026-11-12.1"; it should follow these steps and ask before changing anything):*
1. **Garmin users: connect Claude to Garmin directly if you haven't** (setup prompt 2.2 item 3, the Garmin Personal API extension). Since October 2026 Garmin's terms may stop intervals.icu from passing Garmin-sourced data (activities, FIT files, streams, wellness) on to other apps, including Claude. As of 2026-11-12 intervals.icu still returns full Garmin data, so nothing breaks today, but the direct connection is the only lasting route.
2. **Update your saved check-in skill card:** in the data-pull step, add: if activities recorded by a Garmin device come back from intervals.icu without their data (no power, heart rate or streams), say so and read them from the Garmin connection.
3. **If any of your activities reach intervals.icu only through Strava:** their data is withheld from Claude. Link the device's own service to intervals.icu (Settings → Connections) or upload the files.

- New: Strava alone is not enough. Strava's rules stop intervals.icu from passing Strava data on to other apps, so activities that arrive in intervals.icu only via Strava never reach the coach. Setup now says this up front and, if someone only uses Strava, walks them through linking the device's own service instead.
- New: the direct Garmin connection is no longer "optional but recommended" for Garmin users; setup explains that long term it is the only route, and the check-in falls back to it when intervals.icu returns a Garmin activity without its data.

## 2026-11-11.7

*Touches:* the whole kit: setup prompt (interview item 1, 10, 11, plan contents, data files table, section 3 "Thresholds", debriefs, section 4 new subsections), check-in skill template (sports line, thresholds section, file name), library (new swimming and rowing parts), README, and one data file rename.
*If you already use the kit (do this once; ask your coach "update me to kit 2026-11-11.7" and it should follow these steps, asking you before it changes anything):*
1. **Rename the threshold file.** `claude/data/ftp_history.csv` becomes `claude/data/threshold_history.csv` with the header `date,sport,setting,unit,old_value,new_value,change_pct,method,estimates,evidence_activities,applied,notes`. Convert each old row: `sport` Ride for `ftp` and `indoor_ftp` (for `threshold_pace` or `threshold_hr` the sport it applied to), `unit` W for FTP (otherwise from the notes), `old_w` and `new_w` become `old_value` and `new_value`. Check the new file, then delete the old one. Update the file table in `claude/data/README.md`. If your dashboard is on, its dataset id stays `ftp_history`: build it from the Ride rows of the new file, with `old_value` and `new_value` renamed `old_w` and `new_w` (the FTP panel is cycling only).
2. **Update your saved check-in skill.** Replace every `ftp_history.csv` with `threshold_history.csv` and tell it to log `sport`, `setting` and `unit`. Add a "Sports" line (your sports and how they combine). If you want the new names, rename the "FTP" section to "Thresholds" and the "FTP check" step to "Threshold check". Easiest: let the coach redo the template (`coach-kit-checkin-skill.md`) with your existing athlete-specific rules and offer it as one skill card.
3. **Regenerate `claude/coaching-principles.md`** from the new setup prompt (setup prompt 2.5, item 3): section 4 gained "Strength only", "Several sports", "Swimming" and "Rowing".
4. **Add a sport profile per sport** to your plan (setup prompt 2.1, replaces the earlier "intensity method" line): what you measure, which signal leads, threshold and how it is tested, key sessions, how progress is judged.
5. **Library:** if you swim or row, copy Parts 4 and 5 of the new library into yours. Delete the parts for sports you don't do, if you like.
6. Look through your own documents (registry, notes, scheduled task prompts) for the old file name and the word "FTP" where thresholds in general are meant, and update them.

- New: the kit no longer assumes a sport. The interview starts from which sports you do (strength only, one endurance sport, several, triathlon) and builds only what applies: a strength-only athlete gets no endurance zones, threshold tests or interval debriefs.
- New: a short sport profile per sport (what you measure, which signal leads, threshold, key sessions, how progress is judged). Cycling is one profile among others.
- New: swimming (CSS-based zones and workouts) and rowing (2 km-based zones and workouts) in the library, with swim and rowing thresholds in the threshold rules, and principles for strength-only training, multi-sport mixes and triathlon.
- Changed: `ftp_history.csv` is now `threshold_history.csv` with `sport` and `unit` columns, so thresholds of any sport fit. The dashboard stays built around cycling and strength.

## 2026-11-11.6

*Touches:* setup prompt 2.2 (icuvisor connection options), interview item 11, and the "Choosing the signal" subsection; the check-in skill template's Signals line.
*If you already use the kit:* nothing is required. If you want to change the signal your workouts are written in, tell the coach; to switch to the extension, install it as 2.2 describes. Regenerate `coaching-principles.md` (section 4 changed).

- New: icuvisor as a Claude Desktop extension (`.mcpb`: Settings → Extensions → Advanced settings → Install Extension…, paste API key, athlete ID, time zone, toolset full) is the recommended local route, so no config-file editing. It is macOS only at the moment; Windows keeps the local app with the env block, and the hosted connector remains the phone route.
- New: with both power and HR, the athlete chooses which signal is written into workouts (power first, HR first, or coach decides). With power first the coach schedules in watts and says when HR or feel should lead.

## 2026-11-11.5

*Touches:* setup prompt (interview item 11, 2.1 plan contents, section 4 new "Choosing the signal" subsection, the FTP and thresholds rules, the benchmark marker), the check-in skill template (recommend line, FTP section, Signals line) and the workout library (zones note).
*If you already use the kit:* optional but useful if you have no power meter or want the coach to switch signals: add a Signals line to your saved check-in skill (which signal leads for which session, power doesn't automatically win), and tell the coach what you can measure. Regenerate `coaching-principles.md` from the new section 4.

- New: the coach asks what you can measure per sport (power meter, trainer power, HR strap or wrist HR, GPS, pace) and records an intensity method per sport in the plan. No power meter is a normal case.
- New: a "Choosing the signal" principle. The coach decides per session whether power, heart rate, pace or feel leads (power for intervals and short efforts, HR for long steady sessions and when power is distorted, pace for flat running, RPE as the tiebreaker), and names the weak points of each signal (HR lag, wrist HR errors, cardiac drift, heat).
- Thresholds without power: threshold HR and pace are kept and logged the same way as FTP. The library has HR and RPE stand-ins for the power zones, and the benchmark marker works with pace.

## 2026-11-11.4

*Touches:* setup prompt 2.3 (the "Dashboard off" rule) and the Logging dashboard-sync bullet, and the check-in skill template's "Dashboard sync" intro.
*If you already use the kit:* only if you run with the dashboard off: add one sentence to your saved check-in skill saying quality ratings, ride carbs and weigh-ins still go into `activity_extras.csv`. Nothing changes if the dashboard is on.

- Fix: with the dashboard off, `activity_extras.csv` is kept after all (rows only when you give a session quality rating, ride carbs or weigh-ins), because that information is stored nowhere else. Everything else dashboard-only stays skipped.

## 2026-11-11.3

*Touches:* setup prompt 2.5 (new item 3) and "Keeping runs cheap", and the check-in skill template (the "Coaching principles" line and the Food logging reference).
*If you already use the kit:* optional, saves roughly 15-20k tokens per check-in. Create `claude/coaching-principles.md` as 2.5 item 3 describes (a script copy of section 4, section 5 and three subsections of section 3, about 20 KB), then change the "Coaching principles" line in your saved check-in skill to read that file instead of sections 3-5 of the setup prompt.

- Check-ins no longer read the full kit prompt. Setup creates a small `claude/coaching-principles.md` from it (principles, communication style, food logging, workout writing rules) and the check-in skill reads only that. The skill already carries the rest of the ongoing-coaching rules, so section 3 was being read twice.

## 2026-11-11.2

*Touches:* setup prompt (athlete intro, Step 0 capability line, interview item 12, 2.3 data files, 2.4, 2.5, 2.6, 2.8, and the dashboard sync and refresh parts of section 3) and the check-in skill template (dashboard sync steps).
*If you already use the kit:* nothing to do; your dashboard and weekly review keep working. If you want to cut your usage, tell Claude to stop the dashboard sync (set your saved check-in skill's dashboard link to "none") and to pause the weekly review.

- The training dashboard is now optional and off by default. Setup says it is not recommended because building and refreshing it uses a lot of usage, and builds it only if you clearly say yes. With it off, the dashboard-only data files (wellness, fitness, activities, planned, planned_steps, activity_extras, sleep_timing) are not created and check-ins skip the sync, which makes every check-in cheaper.
- The weekly review is optional too: setup asks once and offers the full weekly review (recommended), a kit-news check only (reads one small file), or none. Without it you can ask for "the weekly review" or "kit news" in a chat.

## 2026-11-11

*Touches:* setup prompt (new Step 0 before the interview; interview items 7, 11 and the new item 13; 2.2 intervals.icu items; 2.4 and 2.6 fallbacks), `SETUP-FOR-CLAUDE.md` and the README. The check-in skill template only has its version line bumped.
*If you already use the kit:* nothing to do. This only changes how a new setup starts.

- New Step 0, before the interview: Claude asks first whether you have an intervals.icu account with your device linked (the essential piece), then whether you have a Garmin device and which Claude app you use. The intervals.icu question also asks which service feeds it (Garmin Connect, COROS, Polar Flow, Suunto, Wahoo, Strava or hand-uploaded files), because the account stays empty until that service is linked. Without intervals.icu, or with no service linked, it guides you through creating and linking it and waits before starting the interview (you can still choose to go on without it; the setup says what is lost). Without Garmin, all Garmin steps are skipped.
- Step 0 also checks silently which tools the session has (projects, Dashboard type, scheduling, connectors) and tells you in one line what is missing and what that changes. The dashboard and the weekly review now have a stated fallback when the tool is missing.
- New interview item 13 (name, language, units, home town, age, body weight) and a doctor-clearance question in item 7.
- Connector steps use the current menu path (Customize → Connectors) and mention the Team and Enterprise owner requirement and the one-connector limit on the free plan.
- The README starts with a note for Claude, so pasting only the link is enough; `SETUP-FOR-CLAUDE.md` covers link-only messages and fetching long files without a clone.

## 2026-11-10.2

*Touches:* the strength event format bullet in the setup prompt (section 3) and in the check-in skill template.
*If you already use the kit:* if you use the Strength Coach watch app and wrote tempo into exercise names, change names like `3s down` to `3 count down` in your saved check-in skill and in your planned strength events.

- Exercise names must not contain a digit directly followed by `s`, `m` or `h` (`3s down`): intervals.icu reads it as a duration and creates a step of that many seconds, so the event's moving time dropped to a few seconds (28 s and 18 s on two 40 min sessions). Write the tempo as `3 count down` instead. The 2026-11-10 example is corrected.

## 2026-11-10

*Touches:* setup prompt (2.1 living documents, section 3 "Keeping runs cheap" and the strength event format bullets, section 4 strength principles, export list) and the check-in skill template (step 2 and the same two strength event format bullets).
*If you already use the kit:* optional, but it lowers the reading cost of every check-in. Split any document above about 30 KB (move a special program into its own document, move old session tables into `claude/archive/`), then copy the three sentences below into your saved check-in skill. No data files, datasets or dashboard changes.

- Leaner documents: each document has one job (plan = strategy, strength log = rules, pools and one progression line per lift, a special program = its own document with a short pointer in the plan, library = catalogue). History lives in the data files or in `claude/archive/`, never in a document read at every check-in; a table of past sessions that grows past about a page is moved out. A special-program document is read only when composing sessions, after a trigger event or at a re-test. Sizes are checked at each block review (split above roughly 30 KB).
- Extra sets go to the side that failed: equal sets on both sides, and one extra set only for a side that stopped short while the other finished (or that you call clearly weaker), judged from the last two exposures and dropped once both sides are level for two exposures. This replaces a blanket "one extra set for the weaker side" in the strength event format.
- Tempo goes into the exercise name on every line when using the Strength Coach watch app (for example `Bulgarian split squat 3s down + 1s pause`), because the watch shows only name, target and load, never the prose. A tempo written only in the description was missed again and again in practice. Names also must not contain `.`, `|` or a comma.

## 2026-11-09

*Touches:* setup prompt (interview item 9; 2.3 data files table and rules; section 3 readiness step 5, food logging rules, "Logging what actually happened"; section 4 endurance, strength and recovery principles) and the check-in skill template ("Readiness", "Dashboard sync", "Logging").
*If you already use the kit:* optional. Create the two new files with their header rows in `claude/data/` and add the README lines for them, then copy the late-session paragraph, the "Dashboard sync" step 4, the session-quality bullet and the logged-day sentence into your saved check-in skill (the benchmark row only if you repeat one route often). No dashboard or dataset changes.

These come from a season audit: questions that took many connector calls to answer, and rules that turned out to matter.

- Late sessions: last night's HRV no longer counts on its own after a session that ended late in the evening (within about 3 hours of going to sleep; end = start + elapsed time) or a late big meal. A one-night dip there is expected; it counts only when another marker agrees. The 7-day HRV rule is unchanged. The dashboard can't see end times, so its data-only rating doesn't apply this; the check-in's rating, which takes precedence there, does.
- Optional benchmark marker: for athletes who repeat one route often with power and HR (a climbing commute, a fixed climb or loop), heart rate 6 bpm or more above their own HR-against-power line on that route is a supporting readiness marker, counted only with another flag. The line is kept in the plan's monitoring section and refitted at each block review and after a break.
- Two new data files, filled by the check-in's sync and kept only in the project (no dashboard dataset): `activity_extras.csv` (activity_id, date, start_local, elapsed_min, carbs_g, quality, pre_kg, post_kg, drank_ml, note) and `sleep_timing.csv` (date, sleep_start, sleep_end, source). With start times, ride carbs, session ratings and sleep times on file, a review can test timing, fuelling and feel-against-markers questions without pulling every activity and night again.
- Session quality: after rides, runs and key sessions the coach asks once for a 1-5 rating of how it went for the effort (5 better than expected, 3 as expected, 1 far worse) if you didn't say, and logs it with any weigh-ins before and after a long session.
- Food logging: a logged day is complete by default (the interview asks). A meal not logged was skipped and is written as such ("No breakfast."); logged days are real totals, not lower bounds; days with no entries stay out of averages.
- Two principles: protect the week's long ride or run as the volume anchor (weekly shortfalls mostly come from shortening it), and put priority minimums (rehab or prehab work, a weaker side, calves or balance) in the core strength sessions, not in optional ones that get dropped first.

## 2026-11-06.2

*Touches:* setup prompt (section 3, strength event format: prose and Watch log bullets, one new App version bullet) and the check-in skill template (same bullets).
*If you already use the kit:* only if you use the Strength Coach watch app. Add the three sentences below to your saved check-in skill. No data files, datasets or dashboard changes.

- Never start a prose line with the words `Watch log`: the watch stops reading sets there.
- Find the Watch log by its `Watch log (...)` line, not by the app name (the watch header says `Strength Coach`, the store listing is `Strength Coach Interpreter`).
- App version note: 1.2.x, current store version 1.2.2, which shows an unequal left/right count as `+1 L` / `+1 R` in the overview.

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
