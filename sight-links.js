// Auto-link sight names in page text to their detail pages.
// Include on any page: <script src="sight-links.js" defer></script>
//
// Scans all text nodes once, wraps the FIRST occurrence of each known
// sight name in an anchor to sights/<slug>.html. Skips text inside
// <a>, <h1>, <h2>, <h3>, <script>, <style>, <code>, <pre>.
(function () {
    // slug → aliases (first alias is the canonical display match)
    const SIGHTS = {
        'hallgrimskirkja':   ['Hallgrímskirkja', 'Hallgrimskirkja'],
        'harpa':             ['Harpa Concert Hall', 'Harpa'],
        'sun-voyager':       ['Sun Voyager', 'Sólfar'],
        'rainbow-street':    ['Rainbow Street', 'Skólavörðustígur'],
        'laugavegur':        ['Laugavegur'],
        'thingvellir':       ['Þingvellir', 'Thingvellir'],
        'bruarfoss':         ['Brúarfoss', 'Bruarfoss'],
        'geysir':            ['Geysir', 'Strokkur'],
        'gullfoss':          ['Gullfoss'],
        'kerid':             ['Kerið', 'Kerid'],
        'fridheimar':        ['Friðheimar', 'Fridheimar'],
        'seljalandsfoss':    ['Seljalandsfoss'],
        'gljufrabui':        ['Gljúfrabúi', 'Gljufrabui'],
        'skogafoss':         ['Skógafoss', 'Skogafoss'],
        'kvernufoss':        ['Kvernufoss'],
        'skogar-museum':     ['Skógar Museum', 'Skogar Museum', 'Skógar Folk Museum'],
        'lava-centre':       ['Lava Centre', 'Lava Center'],
        'reynisfjara':       ['Reynisfjara'],
        'dyrholaey':         ['Dyrhólaey', 'Dyrholaey'],
        'vik-church':        ['Víkurkirkja', 'Vik Church', 'Reyniskirkja'],
        'lava-show':         ['Icelandic Lava Show', 'Lava Show'],
        'eldhraun':          ['Eldhraun'],
        'fjadrargljufur':    ['Fjaðrárgljúfur', 'Fjadrargljufur'],
        'hofskirkja':        ['Hofskirkja'],
        'dverghamrar':       ['Dverghamrar'],
        'skaftafell':        ['Skaftafell', 'Svartifoss'],
        'jokulsarlon':       ['Jökulsárlón', 'Jokulsarlon'],
        'diamond-beach':     ['Diamond Beach'],
        'fjallsarlon':       ['Fjallsárlón', 'Fjallsarlon'],
        'vestrahorn':        ['Vestrahorn', 'Stokksnes'],
        'hraunfossar':       ['Hraunfossar'],
        'barnafoss':         ['Barnafoss'],
        'deildartunguhver':  ['Deildartunguhver'],
        'glymur':            ['Glymur'],
        'ytri-tunga':        ['Ytri-Tunga', 'Ytri Tunga'],
        'budakirkja':        ['Búðakirkja', 'Budakirkja', 'Búðir'],
        'arnarstapi':        ['Arnarstapi'],
        'djupalonssandur':   ['Djúpalónssandur', 'Djupalonssandur'],
        'londrangar':        ['Lóndrangar', 'Londrangar'],
        'saxholl':           ['Saxhóll', 'Saxholl'],
        'raudfeldsgja':      ['Rauðfeldsgjá', 'Raudfeldsgja'],
        'kirkjufell':        ['Kirkjufellfoss', 'Kirkjufell'],
        'stykkisholmur':     ['Stykkishólmur', 'Stykkisholmur'],
        'berserkjahraun':    ['Berserkjahraun'],
        'selvallafoss':      ['Selvallafoss'],
        'kleifarvatn':       ['Kleifarvatn'],
        'seltun':            ['Seltún', 'Seltun', 'Krýsuvík'],
        'brimketill':        ['Brimketill'],
        'gunnuhver':         ['Gunnuhver'],
        'blue-lagoon':       ['Blue Lagoon']
    };

    // Detect if we're in a subfolder (sights/) — adjust href prefix
    const prefix = window.location.pathname.includes('/sights/') ? '' : 'sights/';

    // Build flat match list, longest names first (so "Kirkjufellfoss" wins over "Kirkjufell")
    const matches = [];
    for (const slug in SIGHTS) {
        for (const name of SIGHTS[slug]) {
            matches.push({ slug, name });
        }
    }
    matches.sort((a, b) => b.name.length - a.name.length);

    // Track which slugs have already been linked (first occurrence only per page)
    const linked = new Set();

    const SKIP_TAGS = new Set(['A', 'H1', 'H2', 'H3', 'SCRIPT', 'STYLE', 'CODE', 'PRE', 'NAV', 'BUTTON', 'TEXTAREA', 'INPUT', 'SELECT']);

    function walk(node) {
        if (!node) return;
        if (node.nodeType === Node.TEXT_NODE) {
            processText(node);
            return;
        }
        if (node.nodeType !== Node.ELEMENT_NODE) return;
        if (SKIP_TAGS.has(node.tagName)) return;
        // Walk a static copy of childNodes since we may replace text nodes
        const kids = Array.from(node.childNodes);
        for (const k of kids) walk(k);
    }

    function escapeRegex(s) {
        return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    function processText(textNode) {
        const text = textNode.nodeValue;
        if (!text || text.length < 4) return;

        for (const { slug, name } of matches) {
            if (linked.has(slug)) continue;
            // Word-boundary match, case-insensitive. Use unicode-aware lookaround.
            const re = new RegExp('(?<![\\p{L}\\p{M}])' + escapeRegex(name) + '(?![\\p{L}\\p{M}])', 'iu');
            const m = re.exec(textNode.nodeValue);
            if (!m) continue;

            // Split the text node into: before, matched link, after
            const before = textNode.nodeValue.slice(0, m.index);
            const matched = m[0];
            const after = textNode.nodeValue.slice(m.index + matched.length);

            const frag = document.createDocumentFragment();
            if (before) frag.appendChild(document.createTextNode(before));
            const a = document.createElement('a');
            a.href = prefix + slug + '.html';
            a.textContent = matched;
            a.title = 'View sight details';
            a.style.cssText = 'color:inherit;text-decoration:none;border-bottom:1px dashed #0077B6;';
            frag.appendChild(a);
            if (after) frag.appendChild(document.createTextNode(after));

            textNode.parentNode.replaceChild(frag, textNode);
            linked.add(slug);
            return; // text node is gone, bail
        }
    }

    function run() { walk(document.body); }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', run);
    } else {
        run();
    }
})();
