# Data Fields Reference

Field reference for the JSON output from `a11y-audit.py`.

## Top-Level

```
url           → Audited URL
base_url     → Scheme + netloc (e.g. https://example.com)
timestamp    → ISO 8601 UTC timestamp
score         → 0-100 accessibility score
grade         → A+ through F
findings      → Array of WCAGCheck objects
errors        → Array of error strings (if crawl failed)
```

## Finding Object

```
criterion    → WCAG success criterion (e.g. "1.1.1", "2.4.4")
level        → Conformance level ("A" or "AA")
title        → Short description of the finding
severity     → "critical", "high", "medium", or "low"
element      → HTML snippet of the affected element
detail       → Explanation of the issue and its impact
fix_hint     → Suggested fix (code or instruction)
page_url     → URL of the page where the finding was detected
```

## Homepage Object

```
url              → Page URL
status           → HTTP status code
title            → <title> content
lang             → lang attribute from <html>
has_skip_nav     → Whether a skip navigation link was found
heading_count    → Number of heading elements (h1-h6)
image_count      → Number of <img> elements
input_count      → Number of form inputs
link_count       → Number of <a> elements
table_count      → Number of <table> elements
duplicate_id_count → Number of duplicate id attributes
aria_element_count → Number of elements with ARIA attributes
style_block_count  → Number of <style> blocks in <head>
page_type        → "homepage", "product", "category", "content", or "other"
```

## Additional Page Object

Same as homepage but may also include:

```
priority    → Sitemap priority (float or null)
lastmod     → Last modified date from sitemap (string or null)
```

## Aggregate Object

```
pages_crawled     → Total HTML pages analyzed
total_findings    → Total number of findings across all pages
by_severity       → {"critical": N, "high": N, "medium": N, "low": N}
by_criterion      → {"1.1.1": N, "2.4.4": N, ...} — findings per WCAG criterion
criteria_checked  → Array of criterion strings that had at least one finding
```

## Scoring

Score is calculated by summing weighted severity values, capped at 5 findings per criterion to avoid one issue type dominating:

```
critical = 8 points
high     = 4 points
medium   = 2 points
low      = 1 point

score = max(0, 100 - capped_total)
```

Grade scale:

```
95-100  A+   Excellent accessibility
90-94   A    Strong
80-89   B    Good
70-79   C    Moderate
60-69   D    Weak
0-59    F    Fails minimum standards
```
