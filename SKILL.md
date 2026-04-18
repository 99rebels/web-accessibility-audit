---
name: a11y-audit
description: >-
  WCAG 2.1 AA accessibility audit that produces a client-ready report. Crawls
  websites, checks 20+ accessibility criteria, maps findings to specific WCAG
  success criteria, and generates a professional report with legal context,
  severity ratings, fix code snippets, and a remediation roadmap. No external
  dependencies — pure Python.
allowed-tools:
  - Bash(python3 *)
  - Read
  - Write(*.md)
  - Write(*.txt)
  - Write(*.html)
---

# ♿ Accessibility Audit

**WCAG 2.1 AA accessibility audit that produces a report your freelancer can send directly to a client.**

## When to Use

- "Audit my site for accessibility"
- "WCAG audit", "accessibility check", "a11y audit"
- "Is my website ADA compliant?"
- "Check my site for accessibility issues"
- "Generate an accessibility report for my client"

## Quick Start

```bash
# Default mode (fast, no extra dependencies)
python3 scripts/a11y-audit.py "https://example.com"

# JS rendering mode (recommended for thorough audits)
python3 scripts/a11y-audit.py "https://example.com" --render
```

### Installing Playwright (for JS rendering)

The `--render` flag enables full JavaScript rendering via Playwright. This is **strongly recommended** for modern websites — most sites today rely on JS to render content, and without it the audit may miss significant issues or produce false positives.

**Install in two steps:**

```bash
pip install playwright
playwright install chromium
```

This downloads the Chromium browser (~130MB, one-time). If Chrome is already installed on the system, Playwright will use it automatically without the download.

**If Playwright is not installed and `--render` is used:** The script will fall back to plain HTTP mode and print a warning. The audit still runs, but results may be incomplete for JS-heavy sites.

**What Playwright does:** Opens a real browser, loads the page, waits for all JavaScript to execute, then extracts the fully rendered HTML for analysis. The LLM never sees JavaScript code — only the rendered HTML results.

**Tradeoffs:**
- `--render` adds ~5-15 seconds per page (vs <1 second without)
- For 4 pages (--page-types), expect ~30-60 seconds total
- No impact on LLM token usage — output is the same size
- Catch ~70-80% of WCAG issues vs ~40% without JS rendering

```
# Page-type sampling (one of each: homepage, product, content, category)
python3 scripts/a11y-audit.py "https://example.com" --page-types --render

# Homepage only (fastest, no JS rendering)
python3 scripts/a11y-audit.py "https://example.com" --max-pages 1

# Homepage with JS rendering
python3 scripts/a11y-audit.py "https://example.com" --max-pages 1 --render

# Deep crawl with JS rendering
python3 scripts/a11y-audit.py "https://example.com" --max-pages 50 --render
```

**Flags:**

```
--max-pages N       Sitemap pages (default: 10, 0 = all)
--page-types        Smart sampling: one URL per page type (4 pages)
--timeout SECONDS   Per-request timeout (default: 15)
--max-bytes BYTES   Max response size (default: 512KB)
--no-ssl-verify     Skip SSL verification
--render            Enable JS rendering via Playwright (recommended)
```

## Two Outputs

The skill produces **two separate documents**:

### 1. Client Report
A polished, professional accessibility audit report designed to be sent directly to the client. The freelancer's name/agency goes on this.

### 2. Freelancer Audit Notes
Internal technical notes for the freelancer: what was checked, what couldn't be checked, and what needs manual verification. **Do not share this with the client.**

## Audit Flow

### Step 1: Crawl

**Always use `--render` for thorough audits.** JS rendering catches significantly more issues and reduces false positives on modern websites.

If the user hasn't installed Playwright:
1. Run the audit with `--render` anyway
2. If it falls back to plain HTTP, **tell the user clearly:**
   - "Playwright is required for JS rendering but isn't installed. The audit ran in basic mode, which may miss issues on JavaScript-heavy sites."
   - Provide the install commands: `pip install playwright && playwright install chromium`
   - Offer to re-run with `--render` after installation
3. **Do not proceed with the report as if nothing happened.** The user should know the limitation and have the choice to install.

Run the script. Review the JSON output.

**Do NOT show raw JSON to the user.** Parse, analyze, and present the two documents.

The script outputs:
- `score` — 0-100 accessibility score
- `grade` — A+ through F
- `render_mode` — "playwright" or "plain_http"
- `render_warning` — present if `--render` was requested but Playwright wasn't available
- `js_heavy` — true if the page appears to be JavaScript-heavy (in aggregate)
- `findings` — array of individual findings with WCAG criterion, severity, element, detail, fix hint
- `aggregate.by_severity` — counts per severity level
- `aggregate.by_criterion` — counts per WCAG criterion
- `aggregate.criteria_checked` — which criteria had findings
- Per-page data (title, lang, headings, images, inputs, etc.)

See [references/data-fields.md](references/data-fields.md) for full output schema.

### Step 2: Analyze

Review findings and categorize:

```
Critical → Legal liability, blocks users with disabilities
High     → Significant barrier, fails WCAG Level A/AA
Medium   → Usability issue, best practice violation
Low      → Enhancement, nice to have
```

**Apply the LLM's judgment to:**
- Assess whether existing alt text is *meaningful* (not just present)
- Determine if link text is descriptive *in context*
- Evaluate heading quality (not just hierarchy)
- Assess form error handling patterns

### Anti-Hallucination Rules

**This section is non-negotiable.** The client report is a professional deliverable that freelancers send to paying clients. Fabricated data, inflated findings, or invented details can damage the freelancer's reputation and create legal liability.

**Every finding MUST originate from the script's JSON output.** The script produces the ground truth. The LLM's job is to interpret, contextualize, and present — not invent.

Specific rules:
- **Score and grade:** Use the exact numbers from `score` and `grade` fields. Do not round, adjust, or explain away the score.
- **Findings:** Only report findings present in the `findings` array. Never add findings the script didn't detect. Never split one finding into multiple to inflate the count.
- **Severity:** The script assigns severity. You may adjust it ONLY if you have a clear, documented reason (e.g., tracking pixel flagged as Critical is actually Low). If you adjust severity, note the original and your reasoning in the freelancer notes.
- **Elements and code:** Use the exact element strings from the JSON. Do not fabricate HTML that wasn't in the output. Fix code snippets must address the actual reported element, not a generic example.
- **Page counts and URLs:** Use the exact `page_url` values and page counts from the crawl data. Do not estimate or assume.
- **Legal statistics:** Use ONLY the numbers provided in the Legal Context reference section below. Do not look up, estimate, or update these numbers.
- **WCAG criteria:** Only list criteria that the script actually checked (see WCAG Criteria Checked section). Do not add criteria the script doesn't cover.
- **Effort estimates:** These are the LLM's professional judgment and are acceptable to generate, but keep them realistic and proportional.
- **Consolidate duplicates:** If the script produces multiple identical findings (same criterion, same element), report them as one finding with a count (e.g., "×2"), not as separate entries.
- **False positives:** If you suspect a finding is a false positive, still include it in the client report but note the caveat in the detail. Explain your reasoning in the freelancer notes.
- **When unsure:** Include the finding as reported by the script. Flag uncertainty in the freelancer notes. Never silently drop a finding.

### Step 3: Generate Client Report

Prefix the report with: `♿ **Client Report**`

Use this exact structure and formatting:

```
♿ **Client Report**

# WCAG 2.1 AA Accessibility Audit Report

**Client:** [domain]
**Date:** [date]
**Pages Audited:** [number]
**Standard:** WCAG 2.1 Level AA
**Scope:** Automated audit with LLM-assisted analysis

---

## Executive Summary

[2-3 paragraphs of narrative prose. Start with the score and grade. Describe the most critical issues and their implications. If the site is in a high-litigation category (e-commerce, healthcare, finance), note the legal exposure. End with the score line.]

**Compliance Score: [X]/100 — Grade [X]**

---

## Legal Context

**United States (ADA Title III)**

● 8,667 federal ADA Title III lawsuits filed in 2025
● 3,117 website-specific lawsuits (+27% from 2024)
● WCAG 2.1 AA is the accepted compliance standard
● **E-commerce websites are the #1 litigation target** (78% of digital suits)
● Accessibility overlay widgets do NOT protect from lawsuits

**European Union (European Accessibility Act)**

● EAA enforceable since June 28, 2025
● Enforcement intensifying across EU member states in 2026
● WCAG 2.1 AA compliance required
● Fines up to €3 million

---

## Findings Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | X |
| 🟠 High | X |
| 🟡 Medium | X |
| 🟢 Low | X |

---

## Detailed Findings

🔴 **Critical**

**[WCAG X.X.X] FINDING TITLE IN UPPERCASE**
**Severity:** Critical
**Pages affected:** X/X
**Detail:** [Specific finding with context. Explain what was found and why it matters. For JS-heavy sites, note if the finding may be a false positive due to client-side rendering.]
**Fix:**

```HTML
1    <!-- Before -->
2    [actual broken element from JSON output]
3
4    <!-- After -->
5    [fixed version of that same element]
```

🟠 **High**

**[WCAG X.X.X] FINDING TITLE IN UPPERCASE**
**Severity:** High
**Detail:** [Specific finding with context]
**Fix:**

```HTML
1    <!-- Before -->
2    [actual broken element from JSON output]
3
4    <!-- After -->
5    [fixed version]
```

[Consolidate duplicate findings from the same root cause into one entry]

🟡 **Medium**

**[WCAG X.X.X] FINDING TITLE IN UPPERCASE**
**Severity:** Medium
**Detail:** [Specific finding with context]
**Fix:**

```HTML
1    <!-- Before -->
2    [actual broken element]
3
4    <!-- After -->
5    [fixed version]
```

🟢 **Low**

**[WCAG X.X.X] FINDING TITLE IN UPPERCASE**
**Severity:** Low
**Detail:** [Specific finding with context]
**Fix:** [Inline fix description if simple]

---

## Compliance Checklist

| WCAG Criterion | Level | Status |
|----------------|-------|--------|
| 1.1.1 Non-text Content | A | ❌ Fail |
| 2.4.1 Bypass Blocks | A | ❌ Fail |
| 2.4.2 Page Titled | A | ✅ Pass |
| ... | ... | ... |

[Only include criteria the script actually checked. Use ✅ Pass, ❌ Fail, or ⚠️ Partial]

---

## Remediation Roadmap

**Priority 1 — Fix Immediately (Critical)**

1. [Issue] — **Estimated effort: X hours**

**Priority 2 — Fix This Week (High)**

1. [Issue] — **Estimated effort: X hours**
2. [Issue] — **Estimated effort: X hours**

**Priority 3 — Fix This Sprint (Medium)**

1. [Issue] — **Estimated effort: X hours**

**Priority 4 — Nice to Have (Low)**

1. [Issue] — **Estimated effort: X hours**

---

## Limitations

This audit covers approximately 30-50% of WCAG 2.1 AA criteria through automated testing. The following require manual testing:

● Keyboard navigation and focus management
● Screen reader compatibility
● Video/audio captions and descriptions
● Dynamic content and interaction patterns
● Cognitive accessibility (reading level, plain language)

**Important:** [If the site is JavaScript-heavy, add a note that the audit captures only the initial HTML response and a manual audit is recommended for the fully rendered page.]

A full WCAG 2.1 AA conformance evaluation requires manual testing. This report identifies issues detectable through automated analysis and provides a prioritized remediation roadmap.
```

**Styling rules (Slack-compatible):**
- Use `●` bullets (not `•` or `-`)
- Finding titles in **UPPERCASE**
- Code blocks use `HTML` language tag with line numbers
- Fix code blocks always show `<!-- Before -->` and `<!-- After -->` labels
- No `Impact:` field — fold impact into `Detail:`
- No `Pages` column in compliance checklist (keeps it clean)
- Bold effort estimates in roadmap
- Roadmap priority headers are **bold**, not `###`
- Use `---` dividers between major sections
- For Slack output: tables are fine (Slack supports them)

**Report rules:**
- Be specific — reference actual elements and pages from the JSON output
- Include fix code snippets for all Critical and High findings
- Estimate remediation effort where possible
- Include legal context relevant to the client's jurisdiction
- If the site scored A or above, acknowledge what's working well
- **Never mention the skill, the script, or the methodology in the client report.** The client sees a professional audit from the freelancer.
- **Never fabricate findings, inflate counts, or adjust scores.** See Anti-Hallucination Rules above.

### Step 4: Generate Freelancer Audit Notes

Prefix with: `🔧 **Freelancer Notes — Internal**`

This is the internal document. Be thorough and technical. **Do not share with the client.**

```
🔧 **Freelancer Notes — Internal**

# Audit Notes — [domain] — [date]

## What Was Checked

**Automated Checks (script detected)**

● [WCAG criterion] — [what was checked]
● [WCAG criterion] — [what was checked]
● ...

**LLM-Assisted Analysis**

● Alt text quality assessment (meaningful vs present-only)
● Link text descriptiveness in context
● Heading structure quality
● Form error handling patterns

---

## What Could NOT Be Checked (Manual Testing Required)

**JavaScript Rendering**

● [If js_heavy flag is true: note that most structural elements may be client-side]
● [Note any elements that were likely false positives due to JS rendering]
● [Check if headings, nav structure, and landmarks are absent in HTML but likely present after JS execution]

---

**Keyboard Navigation**
● Focus order cannot be verified without actual keyboard interaction
● Focus traps in modals/dropdowns not detectable
● Custom keyboard shortcuts not testable

**Screen Reader Compatibility**
● How content is announced by screen readers
● ARIA live region behavior
● Reading order in complex layouts

**Dynamic Content**
● Content revealed on hover/click/focus
● Modal and dialog behavior
● Form validation error announcements
● Loading states and progress indicators

**Media**
● Video caption accuracy and synchronization
● Audio description quality
● Autoplay behavior

**Cognitive Accessibility**
● Reading level / plain language assessment
● Consistency of navigation and terminology
● Error prevention and recovery

## Recommendations for Manual Testing

1. Tab through every page — note focus order issues and traps
2. Test with a screen reader (VoiceOver/NVDA/JAWS)
3. Check all interactive elements with keyboard only
4. Test on mobile (touch targets, orientation)
5. Verify form error messages are announced by assistive tech
6. Test any dynamic content (modals, accordions, carousels)

## Severity Adjustments

[List any severities you changed from the script's assignment, with reasoning]

## False Positive Notes

[List any findings that may be false positives and why]

## Consolidated Findings

[List any findings that were consolidated from duplicates in the script output]
```

## WCAG Criteria Checked

The script checks the following WCAG 2.1 Level A and AA criteria:

### Perceivable
| Criterion | Level | What's Checked |
|-----------|-------|---------------|
| 1.1.1 Non-text Content | A | Missing alt text on images, empty alt on informative images, SVG accessibility |
| 1.3.1 Info and Relationships | A | Heading hierarchy (h1-h6), table headers, form label associations, list markup |
| 1.4.1 Use of Color | A | Color used as sole indicator |
| 1.4.3 Contrast (Minimum) | AA | Text contrast ratio (calculated from inline styles) |
| 1.4.11 Non-text Contrast | AA | UI component contrast |

### Operable
| Criterion | Level | What's Checked |
|-----------|-------|---------------|
| 2.1.1 Keyboard | A | Elements with click handlers but no keyboard patterns |
| 2.4.1 Bypass Blocks | A | Missing skip navigation link |
| 2.4.2 Page Titled | A | Missing or empty `<title>` |
| 2.4.4 Link Purpose | A | Ambiguous link text ("click here", "read more"), empty links |
| 2.4.6 Headings and Labels | AA | Missing headings on content pages |
| 2.5.5 Target Size | AA | Small interactive elements |

### Understandable
| Criterion | Level | What's Checked |
|-----------|-------|---------------|
| 3.1.1 Language of Page | A | Missing `lang` attribute on `<html>` |
| 3.2.3 Consistent Navigation | AA | Nav consistency across pages |
| 3.3.2 Labels | A | Missing labels for form inputs, autocomplete attributes |

### Robust
| Criterion | Level | What's Checked |
|-----------|-------|---------------|
| 4.1.2 Name, Role, Value | A | Duplicate IDs, missing ARIA roles, missing accessible names |

Full criterion details: [references/wcag-criteria.md](references/wcag-criteria.md)

## Legal Context (Reference)

Keep this accurate and current when writing reports:

**United States (ADA Title III):**
- 8,667 federal lawsuits in 2025, 3,117 website-specific (+27% YoY)
- WCAG 2.1 AA is the accepted compliance standard
- DOJ government website deadline: April 24, 2026 (50k+ population)
- Top states: New York, Florida, California
- E-commerce is #1 target (78% of lawsuits)
- Overlay widgets do NOT protect from lawsuits

**European Union (EAA):**
- Enforceable since June 28, 2025
- Enforcement intensifying: France (lawsuits), Sweden (inspections), Netherlands (audits)
- WCAG 2.1 AA via EN 301 549 standard
- Fines up to €3 million
- Microenterprise exemption: <10 employees, <€2M turnover
- Grace period for existing products: June 28, 2030

## Security

- URLs must start with `http://` or `https://`
- Shell metacharacters rejected
- Never interpolate user input into shell commands
- Responses capped at 512KB per page
- Respects robots.txt
