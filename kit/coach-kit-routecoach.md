# RouteCoach: route-based targets for the Garmin Edge 530

**Status:** new (version 1.0.1, submitted to the Connect IQ Store on 2026-11-15, review pending, so it may not be in the public store yet); supported device: Edge 530 only; so far tested in the simulator only, not yet on a real Edge 530.

**Purpose:** an optional extra for an athlete who has an Edge 530, rides outdoors with power or heart rate and would like route-based targets (for example "threshold intervals on the long climb"). Everything else in the kit works without it. This document tells the coach what RouteCoach is, how to set it up with the athlete, and how to write a plan for it. The three tools in `kit/routecoach/tools/` (Python 3.8+, standard library only) build the plan; `kit/routecoach/examples/` holds a small synthetic route and a matching plan to try them on.

## What RouteCoach is

A free Connect IQ **data field** for the Garmin Edge 530. The coach splits a GPX route into segments by distance along the route, each with a target: power, heart rate, cadence or a combination. During the ride the field shows:
- an elevation profile of the route window (750 m behind, 3250 m ahead) with the target above each segment;
- the current target, and the current power, heart rate and cadence against it;
- the actual average power and normalized power (NP) inside the current segment.

Progress comes from GPS map-matching to the route, not from ride distance, so starting elsewhere or riding a detour works. More than 50 m off the route it shows OFF ROUTE and pauses. It only **displays**: it never starts workouts, changes alerts or navigates.

**Usage rule:** the athlete loads the route as a Garmin Course and rides EITHER with the Garmin workout OR with RouteCoach, never both: their power alerts could disagree.

**How a plan reaches the Edge** (the athlete chooses; a stored or pasted plan is always preferred over a fetched one):
- **Pasted:** the athlete pastes the `[[RP1:...]]` line into the app's **Pasted plan** setting in Garmin Connect. Works right away.
- **Fetched:** the field reads the plan from the description of today's workout (or, as a fallback, from a NOTE) on intervals.icu. This needs the athlete's intervals.icu API key in the app's settings (typed by the athlete, never in the chat). Unlike a device app, a data field cannot make web requests itself; it asks the Edge for a background fetch, scheduled about 15 seconds after the field starts, and the Edge may take longer (up to about 5 minutes; not yet measured on a real Edge). Once fetched, the plan is stored on the Edge. Pasting the plan is the instant alternative.

## When to offer it

Only when the athlete has an Edge 530 and rides outdoors with power or heart rate and would like route-based targets. The setup prompt (2.7) and the weekly kit-news step say when and how often to mention it. RouteCoach may not be in the public store yet (see Status): check availability first (next section). If it is not listed for the athlete's Edge 530, say so plainly and skip it for now; do not record it as offered.

## When to write a route plan (trigger rule)

**Only when the athlete brings a route.** A route plan is written only after the athlete has put a GPX file in the chat (or named a route that is already in the route library) for a ride. Then ask once, in one line, whether you should also write a RouteCoach plan around that route, and build it only on a yes. If the athlete doesn't mention a route, write the normal workout and nothing else: no RouteCoach NOTE, no `[[RP1:...]]` line, no question about routes, no request for GPX files, and no mention of RouteCoach in check-ins or when planning rides. Never pick a route yourself, and never turn a normal planned ride into a route plan unasked. A GPX that arrives for another reason (for example "what do you think of this route?") is not a request for a plan: answer the question, and offer the plan once only if it fits.

## Checking availability

**Store link:** https://apps.garmin.com/apps/67fb8f49-f0b9-4346-8994-d30bec5c6ad9?tid=1 (the listing is not public yet while the review is pending: until it opens for you, treat RouteCoach as not yet in store; remove this note once it is live).

- **With a web tool:** open the store link above if there is one, otherwise search the Connect IQ Store (apps.garmin.com) for "RouteCoach". It counts as available when its public listing is found and names the Edge 530 among the compatible devices. A search that finds nothing is not proof: say "I could not find it yet", never "it does not exist".
- **Without a web tool:** ask the athlete to search for RouteCoach in the Garmin Connect IQ phone app with the Edge 530 selected, and don't claim it is available.
- **Not available yet:** say so in one or two lines (it is announced and submitted for review, not public yet), set the checklist status to `not yet in store`, and re-check only in the weekly kit-news step (setup prompt 2.6, step 5) or when the athlete asks; never in daily check-ins. When it appears, tell the athlete once, set the status to `offered` and ask whether to set it up.

## How to set it up with the athlete

1. **Install** RouteCoach from the Connect IQ Store (search "RouteCoach" in the Garmin Connect IQ phone app; Edge 530 only). If the search does not show it yet, or not for the Edge 530, say so, follow "Checking availability" above and stop here.
2. **Add it on the Edge** to a full-page data screen of the cycling profile. It shows "No plan" until it has one.
3. **Choose how plans arrive** and fill in the settings below in Garmin Connect (phone, app settings). The athlete types the key; never ask for it in the chat.

   | Setting | Needed? | Default | Notes |
   |---|---|---|---|
   | **API key** | REQUIRED for the fetch path (not needed if the plan is always pasted) | empty | intervals.icu API key; password-style field |
   | **Athlete ID** | REQUIRED for the fetch path, but the default is fine | 0 (= the key owner) | only change it for another athlete |
   | **Pasted plan** | OPTIONAL | empty | manual alternative to the fetch: paste the `[[RP1:...]]` line; works right away and overrides a stored plan |
   | **Demo mode** | OPTIONAL | off | simulates a ride on a built-in route |
   | **Window behind / ahead** | OPTIONAL | 750 m / 3250 m | size of the elevation profile window |
   | **Off-route threshold** | OPTIONAL | 50 m | distance from the route that shows OFF ROUTE |
4. **Routes:** don't ask for a list of routes. Tell the athlete that whenever they send a GPX file in a chat, you will offer to write a route plan for it (see "When to write a route plan"). Routes the athlete sends are added to the route library (below), with the Garmin Course name.
5. **For a ride:** load the Garmin Course on the Edge and ride with RouteCoach and WITHOUT the Garmin workout (or the other way round).
6. **Optional:** switch on **Demo mode** to see what the screen looks like (see the table).

## What to write for a route ride (three things, always together)

Only after the trigger rule above is met (the athlete brought a route and said yes).

1. **The normal time-based workout**, exactly as always (intervals.icu workout syntax, same date), with the plan block as the **last line of its description**: after the step lines, a blank line, then ONE line `[[RP1:...]]` (`encode_plan.py --workout-line` prints exactly that, ready to append). Never put the block inside or between the step lines and nothing after it. **Add the tag `routecoach`** to that workout (next to your usual tags): the watch reads tagged events first and otherwise only looks at ride-type workouts and the NOTE, so a block in a strength workout without the tag is not found. Whenever you rewrite or update that workout's description, keep the block as the last line or regenerate it, otherwise the plan disappears from the watch. Load, TSS, steps and the sync to the device are unchanged by the block (tested in intervals.icu); that Garmin Connect shows the long line in the workout notes without problems is not yet verified: if the athlete reports a problem there, use the NOTE (2) instead.
2. **Fallback, still supported: a separate NOTE event** on the same date, category NOTE, named exactly `RouteCoach plan`, whose description is ONE line, `[[RP1:...]]`, and nothing else. Use it only when the workout carries no block. If both exist, the watch uses the workout block.
3. **One line for the athlete** naming the Garmin Course to load, for example: "Load the course 'Local loop' (74 km) on the Edge, then add the RouteCoach field to a data page. Ride either with the Garmin workout OR with RouteCoach, not both."

Never edit the block by hand: it has a checksum, and a damaged block is rejected ("No plan"). Always regenerate it with the encoder and use its output unchanged.

## How to build the plan

1. **Route:** the one the athlete sent or named (from the route library below). The encoder needs its GPX file; if the athlete named a library route whose GPX is not saved, ask for that file. Never choose a route on your own.
2. **Segments** are measured by DISTANCE ALONG THE ROUTE in metres from the route start (not ride distance).
   - Sorted, non-overlapping, `start_m < end_m`, the last `end_m` at most the route length.
   - Gaps are allowed but show "no target"; prefer contiguous segments covering the whole route.
   - Put the work intervals on the climbs (or flats) that fit the session: a 20-minute threshold block needs a climb or flat stretch long enough at the athlete's expected speed; use `find_climbs.py` for the climb table. Recoveries go on descents and flats between.
   - Keep labels short (24 bytes at most; about 12 characters read well): "Threshold 1", "Recover".
3. **Targets:** a segment has one or more of `P` (power, watts), `H` (heart rate, bpm), `C` (cadence, rpm), each a single number or `[low, high]`: `"targets": {"P": [280, 300], "C": [85, 95]}` is a threshold climb at 85 to 95 rpm; `"targets": {"P": [150, 170], "H": [0, 140]}` is easy riding with heart rate kept under 140 (low 0 means upper limit only).
   - Power for efforts at or above sweet spot; heart rate for endurance and long steady rides where power would be noisy (hills); cadence as a second target for cadence drills.
   - The first target present (P, then H, then C) is the big number; every other target gets its own row with the current value and the segment average.
   - **Take watts and heart rates from the athlete's own thresholds in intervals.icu; never guess them.** The short form `"kind": "P", "low": 280, "high": 300` still works.
4. **Link to the workout:** give each segment `step` = the 0-based index of the workout step it represents, and pass the workout's targets as `workout_steps`. The encoder prints "TARGET MISMATCH" if a segment's power or heart rate target differs from the linked workout step: fix the segment (or the workout) until the warning is gone. Extra targets that exist only on the segment (cadence, for example) are fine and are only noted.
5. **`ftp` and `lthr`** go into the plan JSON so the encoder colours the segments by intensity zone.
6. **Run the encoder**, check the size report and the preview, then create the NOTE (below).

### plan.json (input of `encode_plan.py`)

```json
{"plan_name": "Threshold climbs", "date": "2026-11-17", "route_name": "Synthetic 20", "ftp": 250, "lthr": 165,
 "segments": [{"start_m": 0, "end_m": 4200, "targets": {"P": [130, 160]}, "label": "Warm-up", "step": 0},
              {"start_m": 4200, "end_m": 8700, "targets": {"P": [235, 255], "C": [85, 95]}, "label": "Threshold 1", "step": 1}],
 "workout_steps": [{"index": 0, "targets": {"P": [130, 160]}}, {"index": 1, "targets": {"P": [235, 255]}}]}
```

A complete five-segment example for a synthetic 20 km route is in `kit/routecoach/examples/` (`plan-example.json` with `synthetic-20.gpx`). `route_name` must be identical to the Garmin Course name and to the library name: the field keys plans by date plus route name.

## Running the tools

The GPX file must be on disk where the tools run: the athlete attaches it, or it is saved in the project. Python 3.8 or newer, nothing to install.

```
python3 kit/routecoach/tools/find_climbs.py route.gpx 40        # climbs of at least 40 m gain: km range, length, gain, average %
python3 kit/routecoach/tools/encode_plan.py route.gpx plan.json --png preview.png --out block.txt
```

- `find_climbs.py` helps place the segments. `encode_plan.py` validates the plan (overlaps, ranges, target mismatch), prints a size report and a text preview, and writes the single `[[RP1:...]]` line (the last line on standard output, also in `--out`). Exit code 0 is fine (warnings allowed); 2 means invalid input.
- Run it from wherever the tools are saved; the paths above are the repository's.

## Size limits

The block (and a NOTE description) must stay **under 5,000 characters**: the Edge 530 fetches it in the background and cannot safely handle more. As a guide the encoder produces about 40 to 70 bytes of binary per km and the text block is about 1.33 times that; a real 98.8 km route with 7 segments came to 4,682 characters. A route too long for the limit needs section plans (one plan per ride section, one NOTE each): ask the athlete before splitting.

## Writing the block into the workout

If the coach can create intervals.icu events with a tool, write the workout itself with the block as its last line; otherwise give the athlete the one line to append.
- With the coach data extension use `coach_event_save` (dry run first): the normal workout description (step lines as always), a blank line, then the single `[[RP1:...]]` line as the very last line; tags: the usual ones plus `routecoach`. Do not shorten or reflow the block.
- Read the event back (`coach_events`) and confirm the steps and the load are as without the block and the last line is the block, unchanged. Offer the line in the chat too, so the athlete can paste it into the **Pasted plan** setting.
- Fallback only if the workout cannot carry the block: a NOTE named exactly `RouteCoach plan` on the ride date, description = the single `[[RP1:...]]` line and nothing else, tag `claude`, `external_id` `claude-YYYY-MM-DD-routecoach`. The NOTE is an extra, separate event.
- What the watch reads (so you know what is and is not found): first a tiny list of today's events (names and tags only), then the descriptions of at most 5 candidates: workouts tagged `routecoach`, then up to 2 other ride workouts, then NOTEs tagged `routecoach` or named `RouteCoach plan`. Strength, nutrition and other events are never read.

## Route library

Keep the athlete's own copy of this table in the project, filled only with routes the athlete sent (for example `claude/routecoach/route-library.md`, with the GPX files next to it). Fill it from the GPX files with `find_climbs.py`; the route name is the Garmin Course name.

| Route name (= Garmin Course name) | Length km | Total ascent m | Longest climb (km, avg %) | Start (lat, lon) | GPX file |
|---|---|---|---|---|---|
| | | | | | |

After a ride nothing special is needed: RouteCoach never writes to the activity, so debriefs work as always. When a segment's target is discussed, give the km marks it covered.
