# Coach data extension

A Claude Desktop extension that is the kit's connection to your training data: one compact digest instead of many separate calls, intervals.icu and Garmin merged, calendar changes with safety limits, and your kit data files kept up to date on your own computer. From kit 2026-11-12.3 it is required: it replaces the separate intervals.icu connector (icuvisor) and the Garmin extension. The old kit version keeps working with those, but receives no updates.

**File:** [`coach-data.mcpb`](https://github.com/mhingerl/ai-coach-kit/releases/latest/download/coach-data.mcpb) (the latest GitHub release) · **Version:** 0.13.2 · **SHA-256:** `660e7447d7df15cc26b8e253353e56ba0db2efc028c2a48f264afe8ddb61de65`

It runs only in the Claude desktop app (Mac or Windows), not on the phone or the web. For phone and web chats the extension writes a small snapshot your coach saves into your Project (see below).

## Install

1. Download [`coach-data.mcpb`](https://github.com/mhingerl/ai-coach-kit/releases/latest/download/coach-data.mcpb).
2. In the Claude desktop app open **Settings → Extensions → Advanced settings → Install Extension…** and choose the file. (Dragging it onto the Claude window also works.)
3. Fill in the settings screen:
   - **intervals.icu API key** and **athlete ID** (recommended; leave both empty if you use only Garmin or FIT files; one source of the three is enough) (intervals.icu → Settings → Developer Settings; the ID looks like `i12345`). Claude Desktop keeps the key in the system keychain. Never paste it into a chat.
   - **Garmin API key** (optional): from Garmin Connect on the web, Settings → Personal API.
   - **Write mode** (leave it as it is unless you want less): `full` (default) lets the coach create and update planned workouts and notes, pair activities, set carbs, update thresholds and delete single future events it created; `safe` is the same without deleting; `off` makes it read-only. You can change it any time in Settings → Extensions → this extension; restart the app afterwards.
   - **Time zone**, for example `Europe/Vienna`.
   - **Data folder** (optional): pick an empty folder on your computer. The extension keeps your kit's data CSV files there and writes only inside it.
4. Quit the Claude app completely and reopen it. Then ask your coach: "check the coach data extension" (it runs `coach_status`).

Check the file first if you like: on a Mac, `shasum -a 256 ~/Downloads/coach-data.mcpb` must print the SHA-256 above.

## What it does

| Tool | What you get |
|---|---|
| `coach_digest` | Last days of activities, recovery, baselines, fitness and planned sessions in one small answer |
| `coach_thresholds`, `coach_activity` | FTP and other thresholds; one activity in detail |
| `coach_events` | Calendar events and notes with their full text |
| `coach_event_save`, `coach_event_delete` | Create or update one planned workout or note (dry run first); delete one future event the coach created (Write mode `full`, the default) |
| `coach_link`, `coach_activity_update`, `coach_thresholds_update` | Pair an activity with its planned event; carbs taken; update FTP or threshold values (never zones) |
| `coach_sync` | Brings `wellness`, `fitness`, `activities` and `sleep_timing` CSV files in your data folder up to date (dry run first; never deletes) |
| `coach_snapshot` | A 3 KB summary of those files for phone and web chats |
| `coach_status`, `coach_selftest` | What is connected and whether the data looks right |
| `coach_wellness_update`, `coach_weighins` | Write any wellness field of a day (weight, mood, food totals, comments; overwrite protection, read-back); read Scale Linker weigh-ins |
| `coach_strength_save`, `coach_watch_log` | Write a strength session in the Strength Coach watch app's format; compare the plan with the Watch log |
| `coach_streams`, `coach_best_efforts`, `coach_power_curve` | Second-by-second data of an activity; best efforts; power curve for threshold checks |
| `coach_season`, `coach_season_propose`, `coach_season_apply` | Season view; a deterministic season plan (phases, weekly load); write it to the calendar as notes |
| `coach_library`, `coach_workout_save`, `coach_workout_delete`, `coach_plan_apply` | The intervals.icu workout library and library plans |
| `coach_icu_get` | Read-only access to other intervals.icu data (allowlisted paths, your own data only) |

Your keys stay in the system keychain and the extension talks only to intervals.icu and, if you added a key, Garmin. It can change your calendar only in the ways listed above, and only events it created can be edited or deleted.

## If you used icuvisor or the Garmin extension before

After the new extension works (ask your coach to run `coach_status` and `coach_digest`), you can remove icuvisor and the Garmin extension in Settings → Extensions. Keep both until you have seen one full check-in work.

## Phone and web chats

Ask your coach to "update my snapshot" on the computer. It runs `coach_sync` and `coach_snapshot` and saves the result in your Project as `claude/data/snapshot.md`, which chats on your phone can read. The snapshot covers the last 14 days plus baselines; it is a copy, so it is only as fresh as the last update.

## Updating

When a new version is announced in the changelog, download the latest file from the [releases page](https://github.com/mhingerl/ai-coach-kit/releases/latest) (the link at the top always points to it) and install it the same way; your settings stay.
