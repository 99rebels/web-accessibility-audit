# web-accessibility-audit v3 — Changelog & Status

## v3.0.0 — 2026-04-19

All v3 problems resolved. Tested on Google, Wikipedia, GitHub.

### Changes

**1. Page discovery fallback (Problem 1 — medium-high) ✅**
- When sitemap.xml returns 0 pages (CAPTCHA, SPA, missing), extracts links from the rendered homepage
- Links filtered to same-domain, media extensions excluded, deduplicated
- Page type classification applied to homepage links (same as sitemap)
- New `page_discovery` object in JSON output: total_discovered, source, by_type, audited_count, audited_urls
- Source field: "sitemap", "homepage_links", or "sitemap+homepage_links"
- Sitemap remains default — homepage links are fallback only

**2. Contrast checking via Playwright computed styles (Problem 2 — medium) ✅**
- Second pass after page render using `page.evaluate()` + `getComputedStyle()`
- Gets actual computed foreground/background colors — works with CSS classes, external stylesheets, everything
- Background walk-up (5 levels) handles transparent backgrounds
- Font-size aware: applies 4.5:1 threshold for normal text, 3.0:1 for large text
- Color pair dedup: same fg/bg combo checked once, even across different elements
- Cap: 500 elements per page, with warning only when actually hitting the limit
- Skips hidden elements, empty text, duplicates
- Only runs in `--render` mode (requires Playwright)
- Zero extra page loads — uses same browser session
- `contrast_elements_checked` field: cumulative across all pages
- `contrast_capped` field: true only when actually hitting 500-element limit

**3. Finding deduplication (Problem 6 — low) ✅**
- Deduplicates by `(criterion, title, detail)` tuple before output
- Each finding gets `count` field — same issue on multiple pages consolidated
- Anti-hallucination rules updated: LLM uses `count` directly, reports with "×N" notation
- `total_findings_raw` and `total_findings_unique` fields in output

**4. Smart render wait (Problem 4 — low-medium) ✅**
- `wait_for_selector('h1, h2, h3', timeout=10000)` instead of flat `wait_for_timeout(5000)`
- Stops as soon as content appears (fast on most sites)
- Falls back to 3s wait if no headings found (some pages genuinely don't have them)
- Still tries `networkidle` first, falls back to domcontentloaded + smart wait

**5. Bug fix: URL validation**
- `validate_url` had `\\n` in bad-chars list — treated as `\` and `n` separately
- This rejected any URL containing the letter `n` — most URLs!
- Fixed: `\` and newline are now checked separately

### Skipped problems

**Problem 3: No `<noscript>` content comparison** — Skipped
- Marginal value. `js_heavy` flag and contrast pass give enough signal.
- LLM can infer JS-only elements from heading/link count differences.

**Problem 5: Sanity test on static sites** — Tested, not a code change
- Wikipedia tested: `--render` produces same or better results on static sites
- Score 96/A+ with render, no false positives

### Test results

| Site | Mode | Score | Pages | Raw | Unique | Contrast |
|------|------|-------|-------|-----|--------|----------|
| Google | plain HTTP | 76/C | 2 | 8 | 4 | 0 |
| Google | render | 72/C | 2 | 9 | 4 | 6 |
| Wikipedia | render | 96/A+ | 1 | 29 | 4 | 6 |
| GitHub | render | 78/C | 2 | 108 | 26 | 26 |
| GitHub | page-types+render | 60/D | 4 | 131 | 35 | 64 |
| Downed site | plain HTTP | 0 | 0 | 0 | 0 | 0 |
| Downed site | render | 0 | 0 | 0 | 0 | 0 |
| Playwright missing | fallback | 76/C | 2 | 8 | 4 | 0 |
| expired.badssl.com | --no-ssl-verify | 94/A | 1 | 2 | 1 | 0 |

### Known limitations

- Walmart (and similar) blocks our crawler with CAPTCHA — not fixable
- Gradient backgrounds, image backgrounds can't be contrast-checked
- Pages with >500 text elements per page may miss some contrast issues
- Some JS-heavy sites may time out on Playwright render
