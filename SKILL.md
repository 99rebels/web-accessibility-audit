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
python3 scripts/a11y-audit.py "https://example.com"
```

```
# Page-type sampling (one of each: homepage, product, content, category)
python3 scripts/a11y-audit.py "https://example.com" --page-types

# Homepage only (fastest)
python3 scripts/a11y-audit.py "https://example.com" --max-pages 1

# Deep crawl
python3 scripts/a11y-audit.py "https://example.com" --max-pages 50
```

**Flags:**

```
--max-pages N       Sitemap pages (default: 10, 0 = all)
--page-types        Smart sampling: one URL per page type (4 pages)
--timeout SECONDS   Per-request timeout (default: 15)
--max-bytes BYTES   Max response size (default: 512KB)
--no-ssl-verify     Skip SSL verification
```

## Two Outputs

The skill produces **two separate documents**:

### 1. Client Report
A polished, professional accessibility audit report designed to be sent directly to the client. The freelancer's name/agency goes on this.

### 2. Freelancer Audit Notes
Internal technical notes for the freelancer: what was checked, what couldn't be checked, and what needs manual verification. **Do not share this with the client.**

## Audit Flow

### Step 1: Crawl

Run the script. Review the JSON output.

**Do NOT show raw JSON to the user.** Parse, analyze, and present the two documents.

The script outputs:
- `score` — 0-100 accessibility score
- `grade` — A+ through F
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

### Step 3: Generate Client Report

Use this structure:

```
# WCAG 2.1 AA Accessibility Audit Report

**Client:** [domain]
**Date:** [date]
**Auditor:** [freelancer name/agency]
**Pages Audited:** [number]
**Standard:** WCAG 2.1 Level AA
**Scope:** Automated audit with LLM-assisted analysis

---

## Executive Summary

[2-3 paragraphs: overall compliance status, critical issues, recommended actions]

**Compliance Score:** [X]/100
**Grade:** [A+ through F]

---

## Legal Context

### United States (ADA Title III)
- 8,667 federal ADA Title III lawsuits filed in 2025
- 3,117 website-specific lawsuits (+27% from 2024)
- WCAG 2.1 AA is the accepted compliance standard
- [Business type] websites are the #1 litigation target
- Accessibility overlay widgets do NOT protect from lawsuits
  (22.64% of 2025 lawsuits targeted sites WITH overlays)

### European Union (European Accessibility Act)
- EAA enforceable since June 28, 2025
- Enforcement intensifying across EU member states in 2026
- WCAG 2.1 AA compliance required
- Fines up to €3 million depending on member state
- Microenterprise exemption: <10 employees, <€2M turnover

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

### 🔴 Critical

#### [WCAG X.X.X] Finding Title
**Severity:** Critical
**Pages affected:** X/X
**Detail:** [Specific finding with context]
**Impact:** [Why this matters]
**Fix:**
```html
<!-- Before -->
[broken code]
<!-- After -->
[fixed code]
```

[... more findings by severity ...]

---

## Compliance Checklist

| WCAG Criterion | Level | Status | Pages |
|---------------|-------|--------|-------|
| 1.1.1 Non-text Content | A | ❌ Fail | 3/5 |
| 1.3.1 Info and Relationships | A | ⚠️ Partial | 2/5 |
| 1.4.3 Contrast (Minimum) | AA | ❌ Fail | 4/5 |
| 2.4.2 Page Titled | A | ✅ Pass | 5/5 |
| ... | ... | ... | ... |

---

## Remediation Roadmap

### Priority 1 — Fix Immediately (Critical)
1. [Issue] — Estimated effort: [X hours]

### Priority 2 — Fix This Week (High)
1. [Issue] — Estimated effort: [X hours]

### Priority 3 — Fix This Sprint (Medium)
1. [Issue] — Estimated effort: [X hours]

### Priority 4 — Nice to Have (Low)
1. [Issue] — Estimated effort: [X hours]

---

## Limitations

This audit covers approximately 30-50% of WCAG 2.1 AA criteria through automated testing. The following require manual testing by an accessibility professional:

- Keyboard navigation and focus management
- Screen reader compatibility
- Video/audio captions and descriptions
- Dynamic content and interaction patterns
- Cognitive accessibility (reading level, plain language)

A full WCAG 2.1 AA conformance evaluation requires manual testing. This report identifies issues detectable through automated analysis and provides a prioritized remediation roadmap.
```

**Report rules:**
- Be specific — reference actual elements and pages
- Include fix code snippets for all Critical and High findings
- Estimate remediation effort where possible
- Include legal context relevant to the client's jurisdiction
- If the site scored A or above, acknowledge what's working well
- **Never mention the skill, the script, or the methodology in the client report.** The client sees a professional audit from the freelancer.

### Step 4: Generate Freelancer Audit Notes

This is the internal document. Be thorough and technical.

```
# Audit Notes — [domain] — [date]

## What Was Checked

### Automated Checks (script detected)
[List all WCAG criteria the script evaluated]

### LLM-Assisted Analysis
[List what the LLM assessed: alt text quality, link context, heading quality]

## What Could NOT Be Checked (Manual Testing Required)

### Keyboard Navigation
- Focus order cannot be verified without actual keyboard interaction
- Focus traps in modals/dropdowns not detectable
- Custom keyboard shortcuts not testable

### Screen Reader Compatibility
- How content is announced by screen readers
- ARIA live region behavior
- Reading order in complex layouts

### Dynamic Content
- Content revealed on hover/click/focus
- Modal and dialog behavior
- Form validation error announcements
- Loading states and progress indicators

### Media
- Video caption accuracy and synchronization
- Audio description quality
- Autoplay behavior

### Cognitive Accessibility
- Reading level / plain language assessment
- Consistency of navigation and terminology
- Error prevention and recovery

## Recommendations for Manual Testing

1. Tab through every page — note focus order issues and traps
2. Test with a screen reader (VoiceOver/NVDA/JAWS)
3. Check all interactive elements with keyboard only
4. Test on mobile (touch targets, orientation)
5. Verify form error messages are announced by assistive tech
6. Test any dynamic content (modals, accordions, carousels)

## False Positive Notes
[Note any findings that might be false positives and why]
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
