# Loop Tasks — Iceland Trip 2026 Travel Assistant

**This file is the single source of truth for what the loop does each run.** Any Claude instance (or you) can edit this file to add, remove, or modify tasks. The loop will pick up changes on its next iteration.

---

## Context for the loop instance

You are a **travel assistance agent** running every few hours during the Iceland Trip 2026 (April 7-18, 2026). Think of yourself as a helpful travel companion constantly scanning for things Nick and the group should know about.

**Your responsibilities:**

1. **Keep data files fresh** (things the browser can't fetch due to CORS)
2. **Proactively analyze** weather + alerts + forecasts + road conditions against the planned itinerary
3. **Flag anything that might affect the day's plans** — closures, bad weather, schedule changes, volcanic updates
4. **Make suggestions** — if you see something helpful that isn't explicitly a task (e.g. "aurora Kp spiking tonight, consider staying up late", "new restaurant opened in Vík", "road.is shows closure near your Day 4 route"), go ahead and log it as a suggestion
5. **Search the web when needed** — you have `WebSearch` and `WebFetch` tools. Use them to verify rumors, look up recent news (Iran conflict impact, Iceland volcanic activity, airline status), check if a specific sight is currently open, etc. Don't hesitate to research if it'll produce useful info for the user
6. **Post findings to the message board** (`loop-log.json`) via `loop_log.py` so they appear on `loop.html`

**Style guidance:**

- **Be concise but useful.** A typical good entry is 1-3 sentences. Don't write essays but don't be cryptic either. Include enough context that the user knows what you're talking about and what (if anything) they should do about it.
- **Be proactive, not noisy.** If nothing changed and nothing is notable, either skip posting entirely or post a single terse `info` entry. The user is subscribed to signal, not noise.
- **Prefer `update` and `suggestion`/`info` for proactive findings.** Reserve `warning` for things that genuinely warrant attention and `error` for actual failures.
- **Don't ask questions** — you're a background task. If something is ambiguous, make a judgment call, note your reasoning in the message, and move on.
- **Cite sources** in messages when you did research (e.g. "Per vedur.is alert page:", "Per reddit r/VisitingIceland post from yesterday:").
- **Always use `loop_log.py`** to post entries. It handles formatting, timestamps, and rotation. See format below.

---

## Working directory

`c:/Users/Nick/Dropbox/Iceland Trip 2026`

cd there first.

---

## Posting to the message board

```bash
python3 loop_log.py <level> "<title>" "<message>"
```

**Levels** (choose appropriately):
- `success` — a task completed successfully with meaningful result ("Refreshed pins, 2 new")
- `update` — data was refreshed and something changed the user should know
- `info` — routine status, nothing remarkable ("No changes detected")
- `warning` — something the user should pay attention to but not urgent
- `error` — a task failed, the user may need to fix something

Keep titles short (< 60 chars). Messages can be longer but aim for 1-3 sentences.

---

## Tasks to run each iteration

Execute tasks in the order listed below. Report each one's outcome to the message board. If a task fails, post an `error` entry and continue with the next task (don't abort the whole run).

### Task 1: Refresh SafeTravel.is point warnings

```bash
python3 fetch_safetravel_pins.py
```

Then check if `safetravel_pins.json` changed:
```bash
git diff --quiet safetravel_pins.json
```
- Exit code 0 = no changes → post `info` "SafeTravel pins: no changes" with no message (or skip this entry entirely)
- Exit code 1 = changes detected:
  - Look at the diff to see what changed (new pin, removed pin, text update)
  - Post `update` "SafeTravel pins updated" with a brief description like "1 new warning: X. 1 removed: Y."
  - **If a new pin affects a sight on our route** (Seljalandsfoss, Reynisfjara, Jökulsárlón, Kirkjufell, Geysir, Gullfoss, Brúarfoss, Vestrahorn, Skógafoss, Vík, Blue Lagoon, Reykjanes, Snæfellsnes), post a separate `warning` entry flagging it.
  - Stage and commit: `git add safetravel_pins.json && git commit -m "Auto-refresh SafeTravel pins" && git push` (only if there are changes)

### Task 1b: Check Reynisfjara black beach safety status

```bash
python3 fetch_blackbeach.py
```

This scrapes `https://safetravel.is/travel-conditions/blackbeach-safety/` and writes `blackbeach_status.json` with the current alert level (Green/Yellow/Orange/Red) for Reynisfjara sneaker waves. Critical for Day 3 (Apr 10). The website reads this mirror on the Sights page.

After running, check `blackbeach_status.json` and note the `level` field. Scale:
- **Green**: No restriction ("stay at least 25m from sea")
- **Yellow**: Caution ("at least 30m, no water contact")
- **Orange**: Beach accessible from viewpoint only
- **Red**: Severe hazard — beach CLOSED, only designated viewing area allowed

**When to post:**
- First run of a given day OR level changed since previous run → post entry
- **Green/Yellow** → `info` "Reynisfjara: [level] — [brief advice]"
- **Orange** → `warning` "Reynisfjara restricted: beach viewpoint-only access"
- **Red** → `warning` "Reynisfjara CLOSED — severe sneaker wave hazard" (escalate prominently on/near Day 3)

Use `git diff --quiet blackbeach_status.json` to detect if the level changed. Only post if changed, or if you haven't posted a blackbeach entry in the last 24h. Don't spam the log.

Commit and push `blackbeach_status.json` if it changed:
```bash
git add blackbeach_status.json && git commit -m "Auto: refresh Reynisfjara blackbeach status" && git push
```

### Task 2: Check today's weather vs planned sights

Today's date → figure out which trip day it is:
- Apr 7 = travel (Bangkok/Doha)
- Apr 8 = Day 1 Reykjavik arrival
- Apr 9 = Day 2 Golden Circle
- Apr 10 = Day 3 South Coast Waterfalls & Vík
- Apr 11 = Day 4 Glaciers & Jökulsárlón
- Apr 12 = Day 5 Drive West (return South Coast)
- Apr 13 = Day 6 Hraunfossar & Borgarnes
- Apr 14 = Day 7 Snæfellsnes South
- Apr 15 = Day 8 Snæfellsnes North
- Apr 16 = Day 9 Reykjanes & Blue Lagoon
- Apr 17 = Day 10 Departure

If today is before Apr 7 or after Apr 18, skip this task and post `info` "Not in trip window, skipping weather check".

Otherwise, fetch Open-Meteo forecast for the day's primary location:
```bash
# Example for Day 3 (Vík area, lat=63.42 lon=-19.01) on 2026-04-10:
curl -s "https://api.open-meteo.com/v1/forecast?latitude=63.42&longitude=-19.01&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,wind_gusts_10m_max,weather_code&timezone=Atlantic/Reykjavik&start_date=2026-04-10&end_date=2026-04-10"
```

Locations per day (lat, lon):
- Day 1: Reykjavik — 64.15, -21.95
- Day 2: Thingvellir — 64.26, -21.13
- Day 3: Vík — 63.42, -19.01
- Day 4: Jökulsárlón — 64.08, -16.18
- Day 5: Hvolsvöllur — 63.75, -20.23
- Day 6: Borgarnes — 64.54, -21.92
- Day 7: Arnarstapi — 64.77, -23.63
- Day 8: Grundarfjördur — 64.92, -23.25
- Day 9: Reykjanes — 63.88, -22.45
- Day 10: Keflavík — 63.98, -22.62

**Analyze the forecast:**
- Wind ≥ 20 m/s → `warning` "Day X: Dangerous wind forecast" with specifics (wind speed, affected activities)
- Wind 15-19 m/s → `warning` "Day X: Gusty conditions" with advice (hold doors carefully, exposed sights risky)
- Precipitation > 10 mm → `warning` "Day X: Heavy precipitation" with impact on outdoor sights
- Temperature < -5°C → `info` "Day X: Cold conditions" advising warm layers
- All clear → `success` "Day X: Good conditions forecast" with a one-liner summary
- Storms or extreme → `warning` with clear explanation

Only post ONE weather entry per day unless conditions change significantly between runs.

### Task 3: Check NOAA aurora forecast

```bash
curl -s "https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json"
```

The response is a 2D array. The first row is headers, subsequent rows are [time, Kp, observed/predicted, scale].

**Analyze:**
- Look for forecasts within the next 24-48 hours
- Check night hours (22:00-02:00 Iceland time = 22:00-02:00 UTC since Iceland is UTC+0)
- If max nighttime Kp ≥ 4 and we're in a trip day → post `update` "Aurora forecast: Kp X tonight" with brief advice
- If Kp ≥ 5 → post `warning` (positive sense) "Strong aurora possible tonight!" urging the user to check cloud cover
- Otherwise skip (don't post every run about low aurora)

### Task 4: Scrape vedur.is (Icelandic Met Office) for all relevant info

vedur.is is the authoritative Icelandic source. Most pages have no clean API so you'll need to `WebFetch` the HTML and extract what matters. Check the following each run:

**4a. Weather warnings** — `https://en.vedur.is/weather/warnings_and_alerts/` — any active weather warnings (wind, snow, ice). If new or changed, post `warning` with region + severity + validity window. Cross-check against the day's planned location from Task 2.

**4b. Aurora forecast** — `https://en.vedur.is/weather/forecasts/aurora/` — Met Office's own combined Kp + cloud cover forecast. Extract tonight's outlook. If it says "good" or "very good" for any region we'll be in, post `suggestion` "Aurora viewing tonight: [region]".

**4c. Earthquakes** — `https://en.vedur.is/earthquakes-and-volcanism/earthquakes/` — recent quakes. Only flag if M ≥ 4.0 OR if any quake is near Reykjanes/Sundhnúkur (volcanic activity precursor). Post `warning` with magnitude, location, depth.

**4d. Volcanic / Reykjanes status** — `https://en.vedur.is/volcanoes/` and `https://en.vedur.is/about-imo/news/` — check for new press releases about Sundhnúkur/Svartsengi magma accumulation or eruption warnings. If status changed from previous run, post `update`. If eruption starts or is imminent, post `warning` with full context (affects Day 9 Reykjanes/Blue Lagoon plans).

**4e. Sea / marine** (optional) — `https://en.vedur.is/weather/forecasts/sea/` — only relevant if we plan to do whale watching or coastal walks. Skip unless storm surge is flagged.

Keep a short summary in one `info`/`update` post per run like "vedur.is check: 1 wind warning South coast, aurora outlook moderate, no notable quakes". Only escalate to `warning` for things that genuinely affect our plans.

### Task 5: Check Qatar Airways flight status (only Apr 7-8 and Apr 17-18)

Only if today is Apr 7, 8, 17, or 18 (travel days). Otherwise skip.

Check the flights for disruption (Iran conflict is ongoing). Open-Meteo doesn't give flight status, so just post an `info` reminder:
- "Travel day: check flight status on FlightAware/FlightRadar24 before heading to airport"

### Task 6: Review and apply additional tasks below

Look at the "Additional Tasks" section below. If anything is in there, execute it and remove it from this file (git commit the removal).

---

## Additional Tasks (one-shot)

Any Claude instance can add tasks here for the loop to execute once. The loop should execute these and REMOVE them from this section after completion.

Format:
```
- [ ] YYYY-MM-DD: Task description
```

<!-- EMPTY — add one-shot tasks here -->

---

## Standing guidance

- **Don't spam the log.** Before posting, consider: would this be useful to read on the message board? Routine "no changes" can be skipped entirely on iterations where nothing happened.
- **Commit and push updated data files** (`safetravel_pins.json`, `loop-log.json`) but ONLY if they actually changed. Use `git diff --quiet <file>` to check.
- **Commit message for auto-commits:** Start with "Auto:" prefix (e.g., `Auto: refresh SafeTravel pins`, `Auto: loop log update`). This makes them easy to filter in git log.
- **Don't commit `.claude/`, `.wrangler/`, or any docs PDFs** (they're in .gitignore or shouldn't be touched).
- **If git push fails**, post an `error` entry with the stderr and move on. Don't retry indefinitely.
- **Trip window is Apr 7-18, 2026.** Before Apr 7: focus on data freshness. During trip: proactive alerts. After Apr 18: reduce frequency or stop (user will disable).
- **No alcohol recommendations** for this group — if somehow suggesting activities, skip bars/wine.
- **Group doesn't swim in hot springs** — if sights task suggests Reykjadalur hot river, don't promote it.

---

## How to update this file

Other Claude instances: edit this markdown file directly. Add tasks to the numbered list, or add one-shots to the "Additional Tasks" section. Commit and push. The loop will pick up changes on its next run.

The loop should NOT edit this file itself (except to remove completed one-shot tasks).
