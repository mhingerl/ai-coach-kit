# AI coach kit

A ready-made setup that turns Claude into your personal endurance and strength coach. It reads your training data, plans your sessions, logs what you did and keeps a training dashboard for you.

You don't need to copy files or edit anything. Paste this repository's link into Claude and Claude sets everything up with you.

## What you get

- **An interview first.** Claude asks about your sports, goals, schedule, equipment, injuries, devices and how you like to be coached, then writes up a short profile for you to correct.
- **A training plan and logs** in your Claude Project: an annual plan with phases, a strength log, and an exercise and workout library tailored to your equipment.
- **Connections to your data,** guided step by step: intervals.icu (via icuvisor), and optionally Garmin's Personal API and a smart scale.
- **A training dashboard:** a Today page with your readiness, today's session (with a done badge and its interval structure) and the muscles to target; recovery trends (HRV, resting heart rate, sleep, Body Battery, stress); training load (fitness, fatigue, form, weekly hours by intensity, FTP); a muscle load body map, weekly strength targets and progression; your season plan.
- **A daily readiness check-in:** ask "how should I train today?" and Claude rates your readiness green, amber or red (HRV trend, resting heart rate, sleep, training load, how you feel), checks your plan phase and the weather, and recommends (and schedules) the session.
- **Session debriefs and FTP:** after key sessions Claude checks what you actually did against the plan and decides the next progression step. It keeps your FTP current from your own performance, indoors and outdoors.
- **A weekly review and block reviews:** a scheduled task checks how your training is going against the plan, suggests changes, writes a review at the end of each training phase, and reshapes your dashboard to fit what matters to you now.
- **Optional Garmin watch apps:** if you have a Forerunner 955/255/255S or fenix 7/7S/7X, the free Connect IQ apps *Strength Coach Interpreter* (guides your planned strength session set by set from your intervals.icu calendar and logs what you did) and *Scale Linker* (Renpho scale weigh-ins, pre/post-workout sweat loss, to intervals.icu) work with this kit. Claude recommends them during setup where they fit.
- **Kit news:** the weekly review checks this repository for a newer kit version and tells you what changed. It never applies anything on its own.
- **Easy re-setup:** before moving to a new kit version, ask "give me my setup interview answers". Paste the result into the new setup and Claude only asks what's missing.

## How to start

1. Open the Claude app. The desktop app on a Mac or Windows computer works best, because some connections run on your computer.
2. Create a new **Project** (for example "Coach") and start a chat in it.
3. Paste this message, with this repository's address at the end:

   > Set me up as my coach with this kit: https://github.com/mhingerl/ai-coach-kit

4. Answer Claude's questions. Setup takes about 30–45 minutes, and you can stop and continue later.

**You'll need:** a free account at [intervals.icu](https://intervals.icu) linked to your watch or bike computer (Garmin, Wahoo, COROS, Polar, Suunto and others). Claude helps you create one if you don't have it yet.

**Never paste passwords or API keys into the chat.** Claude tells you where each one goes.

## What's in this repository

| File | What it is |
|---|---|
| [`SETUP-FOR-CLAUDE.md`](SETUP-FOR-CLAUDE.md) | How Claude loads the kit when you paste the link |
| [`kit/ai-coach-setup-prompt.md`](kit/ai-coach-setup-prompt.md) | The coaching and setup instructions |
| [`kit/coach-kit-exercise-and-workout-library.md`](kit/coach-kit-exercise-and-workout-library.md) | Exercise and workout catalogue (strength, cycling, running) |
| [`kit/coach-kit-checkin-skill.md`](kit/coach-kit-checkin-skill.md) | Template for your daily readiness check-in skill |
| [`kit/coach-kit-dashboard.html`](kit/coach-kit-dashboard.html) | Template for your training dashboard |
| [`kit/coach-kit-exercises.csv`](kit/coach-kit-exercises.csv) | Which muscles each exercise trains (for the muscle map) |
| [`CHANGELOG.md`](CHANGELOG.md) | What changed in each kit version |

**Prefer to do it by hand?** Add the five files in `kit/` to your Project's knowledge and write "Start" in a chat.

## Good to know

- Claude is not a doctor, physiotherapist or dietitian. For pain, injury or health questions it will say so and refer you on.
- Your plan, logs and dashboard stay in your own Claude account. The dashboard is private unless you share it.
- Third-party connectors (icuvisor, the Garmin extension) are community projects, not made by Anthropic, Garmin or intervals.icu. The setup instructions name the version of the Garmin extension that was reviewed.

## License

MIT. See [LICENSE](LICENSE).
