# AI coach kit

> **For Claude:** if a user pasted this repository's link, they want to be set up as an athlete with this kit. Read [`SETUP-FOR-CLAUDE.md`](SETUP-FOR-CLAUDE.md) and follow it; the first thing you ask is whether they have intervals.icu.

A ready-made setup that turns Claude into your personal training coach for strength, endurance sports (cycling, running, swimming, rowing, triathlon) or any mix. It reads your training data, plans your sessions, and logs what you did. A training dashboard is available as an optional extra.

You don't need to copy files or edit anything. Paste this repository's link into Claude and Claude sets everything up with you.

## What you get

- **A quick check first.** Claude asks whether you have an intervals.icu account (the one essential piece) and a Garmin device. If you don't have intervals.icu yet, it walks you through creating it before anything else.
- **An interview.** Claude asks about your sports, goals, schedule, equipment, injuries, devices and how you like to be coached, then writes up a short profile for you to correct.
- **A training plan and logs** in your Claude Project: an annual plan with phases, a strength log, and an exercise and workout library tailored to your equipment.
- **Connections to your data,** guided step by step: intervals.icu and optionally Garmin, both through one coach data extension that comes with this kit, and optionally a smart scale.
- **An optional training dashboard (off by default, not recommended: it uses a lot of usage):** a Today page with your readiness, today's session (with a done badge and its interval structure) and the muscles to target; recovery trends (HRV, resting heart rate, sleep, Body Battery, stress); training load (fitness, fatigue, form, weekly hours by intensity, FTP); a muscle load body map, weekly strength targets and progression; your season plan.
- **A daily readiness check-in:** ask "how should I train today?" and Claude rates your readiness green, amber or red (HRV trend, resting heart rate, sleep, training load, how you feel), checks your plan phase and the weather, and recommends (and schedules) the session.
- **Session debriefs and FTP:** after key sessions Claude checks what you actually did against the plan and decides the next progression step. It keeps your FTP current from your own performance, indoors and outdoors.
- **An optional weekly review and block reviews (setup asks if you want it):** a scheduled task checks how your training is going against the plan, suggests changes, writes a review at the end of each training phase, and reshapes your dashboard to fit what matters to you now.
- **The coach data extension (Mac or Windows desktop app; needed from kit 2026-11-12.3):** one small digest of your training data instead of many calls, intervals.icu and Garmin merged, calendar changes with safety limits, your data files kept up to date on your computer, and a small snapshot for phone chats. Setup installs it; steps are in [`extension/INSTALL.md`](extension/INSTALL.md).
- **Optional Garmin watch apps:** if you have a Forerunner 955/255/255S or fenix 7/7S/7X, the free Connect IQ apps *Strength Coach Interpreter* (guides your planned strength session set by set from your intervals.icu calendar and logs what you did) and *Scale Linker* (Renpho scale weigh-ins, pre/post-workout sweat loss, to intervals.icu) work with this kit. Claude recommends them during setup where they fit.
- **Kit news:** the weekly review (or a kit-news check on its own, if you pick that) checks this repository for a newer kit version and tells you what changed. It first reads a one-line `VERSION` file, so a week with no news costs almost nothing, and it never applies anything on its own.
- **Easy re-setup:** before moving to a new kit version, ask "give me my setup interview answers". Paste the result into the new setup and Claude only asks what's missing.

## How to start

1. Open the Claude desktop app on a Mac or Windows computer. The kit's extension runs there.
2. Create a new **Project** (for example "Coach") and start a chat in it.
3. Paste this message, with this repository's address at the end (the address alone also works):

   > Set me up as my coach with this kit: https://github.com/mhingerl/ai-coach-kit

4. Answer Claude's questions. Setup takes about 30–45 minutes, and you can stop and continue later.

**You'll need:**
- The Claude desktop app on a Mac or Windows computer (the kit's extension runs there; web and phone chats can only read a snapshot).
- A free account at [intervals.icu](https://intervals.icu) linked to your watch or bike computer (Garmin, Wahoo, COROS, Polar, Suunto and others). This is essential; Claude helps you create it if you don't have it yet. Strava alone does not work: Strava's rules stop intervals.icu from passing Strava data on to Claude, so link your device's own service instead.
- A Garmin device is optional (it adds recovery data and some watch apps). If you have one, add a Garmin key to the extension: it is the only lasting route, because Garmin's terms may stop intervals.icu from passing Garmin data on to Claude.
- A Claude account with Projects. Setup and the weekly review use a fair amount of usage, so a paid plan is the comfortable choice. On a Team or Enterprise plan your organisation must allow desktop extensions.

**Never paste passwords or API keys into the chat.** Claude tells you where each one goes.

## What's in this repository

| File | What it is |
|---|---|
| [`SETUP-FOR-CLAUDE.md`](SETUP-FOR-CLAUDE.md) | How Claude loads the kit when you paste the link |
| [`kit/ai-coach-setup-prompt.md`](kit/ai-coach-setup-prompt.md) | The coaching and setup instructions |
| [`kit/coach-kit-exercise-and-workout-library.md`](kit/coach-kit-exercise-and-workout-library.md) | Exercise and workout catalogue (strength, cycling, running) |
| [`kit/coach-kit-checkin-skill.md`](kit/coach-kit-checkin-skill.md) | Template for your daily readiness check-in skill |
| [`kit/coach-kit-dashboard.html`](kit/coach-kit-dashboard.html) | Template for the optional training dashboard |
| [`kit/coach-kit-exercises.csv`](kit/coach-kit-exercises.csv) | Which muscles each exercise trains (for the muscle map) |
| [`extension/INSTALL.md`](extension/INSTALL.md) and [`extension/coach-data.mcpb`](extension/coach-data.mcpb) | The optional coach data extension: install guide and the file |
| [`VERSION`](VERSION) | The current kit version (one line; what the weekly kit-news check reads first) |
| [`CHANGELOG.md`](CHANGELOG.md) | What changed in each kit version |

**Prefer to do it by hand?** Add the five files in `kit/` to your Project's knowledge and write "Start" in a chat.

## Good to know

- Claude is not a doctor, physiotherapist or dietitian. For pain, injury or health questions it will say so and refer you on.
- With your OK, Claude creates and edits planned workouts on your intervals.icu calendar. It shows you a preview and waits for your go-ahead before changing the calendar, and only deletes workouts if you allowed that.
- Your plan and logs stay in your own Claude account, and so does the dashboard if you choose one (it is private unless you share it).
- The coach data extension is a community project in this repository, not made by Anthropic, Garmin or intervals.icu. It reads and writes only at intervals.icu and (with your key) Garmin, with its Write mode setting limiting what it can change.

## Tell us what's missing

Using a watch, bike computer, scale or app the kit doesn't work with yet, or have an idea or a problem? [Open an issue](https://github.com/mhingerl/ai-coach-kit/issues/new/choose) (device request or feedback). Please don't put keys, passwords or personal health data in it. Your coach can also draft the issue text for you to post.

## License

MIT. See [LICENSE](LICENSE).
