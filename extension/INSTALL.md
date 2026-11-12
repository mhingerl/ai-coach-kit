# Coach data extension (optional)

A Claude Desktop extension that gives your coach one compact digest of your training data instead of many separate calls, merges intervals.icu and Garmin, and can keep your kit data files up to date on your own computer. It is optional: the kit works without it, and your existing setup keeps working.

**File:** [`coach-data.mcpb`](coach-data.mcpb) · **Version:** 0.6.0 · **SHA-256:** `331e987c1ef82c80fba69813c8f6a985b7e46f0bce932ab0a156cd978a30a17a`

It runs only in the Claude desktop app (Mac or Windows), not on the phone or the web. For phone and web chats the extension writes a small snapshot your coach saves into your Project (see below).

## Install

1. Download [`coach-data.mcpb`](coach-data.mcpb) (on its GitHub page use the download button).
2. In the Claude desktop app open **Settings → Extensions → Advanced settings → Install Extension…** and choose the file. (Dragging it onto the Claude window also works.)
3. Fill in the settings screen:
   - **intervals.icu API key** and **athlete ID** (intervals.icu → Settings → Developer Settings; the ID looks like `i12345`). Claude Desktop keeps the key in the system keychain. Never paste it into a chat.
   - **Garmin API key** (optional): from Garmin Connect on the web, Settings → Personal API.
   - **Time zone**, for example `Europe/Vienna`.
   - **Data folder** (optional): pick an empty folder on your computer. The extension keeps your kit's data CSV files there and writes only inside it.
4. Quit the Claude app completely and reopen it. Then ask your coach: "check the coach data extension" (it runs `coach_status`).

Check the file first if you like: on a Mac, `shasum -a 256 ~/Downloads/coach-data.mcpb` must print the SHA-256 above.

## What it does

| Tool | What you get |
|---|---|
| `coach_digest` | Last days of activities, recovery, baselines, fitness and planned sessions in one small answer |
| `coach_thresholds`, `coach_activity` | FTP and other thresholds; one activity in detail |
| `coach_sync` | Brings `wellness`, `fitness`, `activities` and `sleep_timing` CSV files in your data folder up to date (dry run first; never deletes) |
| `coach_snapshot` | A 3 KB summary of those files for phone and web chats |
| `coach_status`, `coach_selftest` | What is connected and whether the data looks right |

Your keys and data stay on your computer. The extension talks only to intervals.icu and, if you added a key, Garmin.

## Phone and web chats

Ask your coach to "update my snapshot" on the computer. It runs `coach_sync` and `coach_snapshot` and saves the result in your Project as `claude/data/snapshot.md`, which chats on your phone can read. The snapshot covers the last 14 days plus baselines; it is a copy, so it is only as fresh as the last update.

## Updating

When a new version is announced in the changelog, download the new file from this folder and install it the same way; your settings stay.
