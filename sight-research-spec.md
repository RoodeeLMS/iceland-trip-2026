# Sight Detail Page Research Spec

This document tells any Claude subagent **exactly** how to research and write a detail page for a single sight on the Iceland Trip 2026 website. Consistency across all 52 sights depends on everyone following this spec.

---

## Input you'll receive

The parent agent will give you:
- **slug** — the filename stem (e.g. `reynisfjara`)
- **name** — clean display name (e.g. "Reynisfjara Black Sand Beach")
- **lat, lon** — approximate coordinates
- **day(s)** — which trip day(s) this sight is planned for
- **short description** — one-line context from the main sights.html card

Example brief: *"Research sight: slug=`reynisfjara`, name=`Reynisfjara Black Sand Beach`, lat=63.40, lon=-19.04, day=3, desc=`Famous black sand beach with basalt columns; sneaker waves are deadly`."*

---

## What to research

Use `WebSearch` and `WebFetch` to gather **current, verifiable info**. Do NOT hallucinate. If you can't find something confidently, write "Information not available — check on arrival" rather than making it up.

Required sections (in this order):

### 1. Overview (2-3 sentences)
What it is, why it matters, why it's worth visiting. Keep it concrete.

### 2. Current Status (as of research date)
- Is it open? Any closures, construction, restrictions?
- Any active SafeTravel.is warnings? (cross-reference pins where relevant)
- Seasonal considerations for **April 2026** specifically (ice, mud, weather, daylight hours)
- If a sight is known to change (e.g. glacier recession, volcanic area) note recent changes

### 3. Your Visit — Step by Step
**This is the most important section.** Write a **numbered walk-through** as if you're personally guiding a visitor from the moment they arrive at the parking lot. 4-8 steps. Each step must include:
- **Where to go** (specific spot, landmark, or trail name)
- **What to look for / do there** (concrete — not "admire the view")
- **How long** to spend there
- **Why it matters** (what makes this spot worth the stop)

Format each step as:
```html
<div class="visit-step">
    <div class="visit-step-num">1</div>
    <div class="visit-step-content">
        <strong>Step title — specific spot name</strong>
        What to do / look for, in 2-3 sentences.
        <div class="step-meta">⏱️ 10 min · 📍 ~50m from parking</div>
    </div>
</div>
```

Think: "If I only had 45 minutes here, what are the 5 things I absolutely must do in what order?" Then write that.

### 3b. Photography & Drone
Dedicated section. Cover:
- **Best angles / compositions** — specific vantage points with directions (e.g. "shoot the basalt columns from the south end around 9am for side-light")
- **Best time of day** (golden hour angles, blue hour, etc.)
- **Lens recommendations** (wide for scope, tele for compression)
- **Drone rules FOR THIS SPECIFIC LOCATION ONLY** — 2-3 lines max. Is it allowed here? Any local no-fly zone? Seasonal bird closures? That's it.
- Do NOT include general Iceland drone law, registration rules, DJI wind limits, etc. — those live on the Planning page, not per-sight.
- Cite source for location-specific rules (safetravel.is, park regulations, on-site signage).

### 3c. Photos
Find 2-4 high-quality images from **Wikimedia Commons** (search `https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url&titles=...` or the REST summary endpoint). Use `upload.wikimedia.org` direct URLs with `/thumb/` 600px or 800px sizes.

Format the gallery as:
```html
<div class="gallery">
    <div><img src="IMG_URL" alt="description"><div class="gallery-caption">Caption / source</div></div>
    ...
</div>
```

Also pick ONE image as the `SIGHT:HERO-IMAGE` (the main banner image at the top of the page).

### 3d. Map bounding box
For the OpenStreetMap embed, compute a bounding box around the sight coordinates. Replace in the template:
- `SIGHT_LAT_MIN` = lat - 0.015
- `SIGHT_LAT_MAX` = lat + 0.015
- `SIGHT_LON_MIN` = lon - 0.03
- `SIGHT_LON_MAX` = lon + 0.03
- `SIGHT_LAT` and `SIGHT_LON` = the actual coordinates (in both the iframe src and the Google Maps button href)

### 4. Getting there
- Nearest parking (name + approx cost in THB)
- Walk from parking to main viewpoint (distance/time)
- Road type (paved / gravel / F-road / 4x4 only)
- Any fees

### 5. Good itinerary / timing tips
- Best time of day for photos (sunrise/sunset angles)
- When crowds are lightest
- Combine with what nearby sights (name them)
- How long to allocate given the day's other plans

### 6. Reviews & reputation
- Rough Google Maps rating (if findable) + review count
- What visitors praise
- Common complaints / disappointments
- Is it overrated, underrated, or matches expectations?

### 7. Activities & providers (if any)
Paid tours, guided hikes, boat rides, etc. Include:
- Provider name
- Approx price in THB (assume ฿35/USD, ฿0.25/ISK)
- Whether booking is needed / recommended
- Link to their site

If none, write "Self-guided — no booked activities needed."

### 8. Safety notes
Specific hazards. Copy verbatim from safetravel.is if there's a pin for it.

### 9. Links
- Official site (if any)
- Google Maps link (use `https://www.google.com/maps/search/?api=1&query={url-encoded name}`)
- Wikipedia
- Relevant safetravel.is / road.is page
- Trusted blog or Reddit thread if they give useful current info

---

## Output format

Write a **single HTML file** at `sights/<slug>.html` using `sights/_template.html` as the skeleton. Only edit the content inside the marked placeholders:

```html
<!-- SIGHT:NAME -->           → sight display name
<!-- SIGHT:EMOJI -->          → one emoji (match sights.html card)
<!-- SIGHT:DAYS -->           → "Day 3" / "Day 3 · Day 5" etc.
<!-- SIGHT:LAT -->            → latitude
<!-- SIGHT:LON -->            → longitude
<!-- SIGHT:OVERVIEW -->       → Section 1
<!-- SIGHT:STATUS -->         → Section 2
<!-- SIGHT:VISIT-STEPS -->    → Section 3 (numbered walk-through using .visit-step divs)
<!-- SIGHT:PHOTOGRAPHY -->    → Section 3b (photography tips + drone rules)
<!-- SIGHT:GALLERY -->        → Section 3c (2-4 Wikimedia images in .gallery)
<!-- SIGHT:HERO-IMAGE -->     → main banner image URL (pick best of your gallery finds)
<!-- SIGHT:GETTING-THERE -->  → Section 4
<!-- SIGHT:ITINERARY -->      → Section 5
<!-- SIGHT:REVIEWS -->        → Section 6
<!-- SIGHT:ACTIVITIES -->     → Section 7 (or "Self-guided")
<!-- SIGHT:SAFETY -->         → Section 8
<!-- SIGHT:LINKS -->          → Section 9 (bulleted HTML <ul><li>)
<!-- SIGHT:RESEARCHED -->     → today's date YYYY-MM-DD
```

Do NOT modify any HTML structure, CSS, nav, or scripts outside these placeholders. The template handles all styling.

## Style rules

- **No fluff.** Every sentence must give the reader something actionable or specific.
- **No travel-brochure language.** ("A breathtaking gem!" → cut it.)
- **THB for prices**, not USD or ISK. Convert if needed.
- **No alcohol recommendations.** (Group doesn't drink.)
- **No hot-river swimming recommendations.** (Group doesn't swim in hot springs.)
- **Cite sources** in-line when making a factual claim ("Per safetravel.is:", "Per r/VisitingIceland [date]:", "Per Reykjavik Grapevine:").
- **No fixed word budget.** Write as much as the sight deserves. A major sight like Jokulsarlon or Thingvellir may warrant 1500+ words of rich detail; a minor stop like Dverghamrar may only need 300-400. Let the available info determine length, not an arbitrary cap. Rule: every sentence must earn its place — if you're padding, stop.
- **The "Your Visit" walk-through is always the core.** It's the main value of the page. Err on the side of MORE steps and more specificity there, fewer elsewhere. If you have less real info, write less — don't pad.
- **Honest assessment.** If a sight is overrated, say so. The user wants signal, not marketing.

---

## When done

Report back to the parent agent:
1. The path you wrote (`sights/<slug>.html`)
2. One sentence on what you found that's notable/surprising (or "nothing surprising")
3. Any gaps where info wasn't findable (so the parent can flag them)

Do NOT commit to git. The parent agent handles git.
