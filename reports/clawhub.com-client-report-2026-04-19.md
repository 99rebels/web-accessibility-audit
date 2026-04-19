# WCAG 2.1 AA Accessibility Audit Report

**Client:** clawhub.com
**Date:** 2026-04-19
**Pages Audited:** 3
**Standard:** WCAG 2.1 Level AA
**Scope:** Automated audit with JS rendering and LLM-assisted analysis

---

## Executive Summary

ClawHub.com scored **82/100 — Grade B** on automated WCAG 2.1 AA testing. The site has a solid foundation with proper language attributes, page titles, and heading structure. The main areas of concern are color contrast issues on navigation elements and search functionality, along with missing labels on form inputs.

The most critical finding is a contrast failure on the "Search" heading at 1.00:1 (identical foreground and background colors). Several navigation and filter elements are borderline — between 4.0:1 and 4.5:1 — and could be fixed with minor color adjustments.

**Compliance Score: 82/100 — Grade B**

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
| 🔴 Critical | 1 |
| 🟠 High | 9 |
| 🟡 Medium | 9 |
| 🟢 Low | 4 |

---

## Detailed Findings

🔴 **Critical**

**[WCAG 1.4.3] INSUFFICIENT COLOR CONTRAST (AA LARGE TEXT)**
**Severity:** Critical
**Pages affected:** 1/3
**Detail:** The "Search" heading has a contrast ratio of 1.00:1 (identical foreground and background colors). The text is effectively invisible against its background.
**Fix:**

```HTML
1    <!-- Before: Search heading at 1.00:1 contrast -->
2    <h2>Search</h2>
3
4    <!-- After: Apply visible color -->
5    <h2 style="color: #1a1a2e;">Search</h2>
```

🟠 **High**

**[WCAG 1.4.3] INSUFFICIENT COLOR CONTRAST (AA NORMAL TEXT) — BORDERLINE FAILURES**
**Severity:** High
**Pages affected:** 2/3
**Detail:** Several navigation and filter elements fall just short of the 4.5:1 threshold:
- "Skill" text: 3.00:1
- "Install" button: 4.12:1
- "Skills" nav item: 4.10:1
- "Most downloaded" filter: 4.49:1
- "Plugins" nav item: 4.10:1
- "All types" filter: 4.49:1

These are quick wins — minor color adjustments would bring them into compliance.
**Fix:** Darken foreground colors by 5-10% on each element.

**[WCAG 3.3.2] FORM INPUT MISSING LABEL**
**Severity:** High
**Pages affected:** 2/3
**Detail:** 3 search/filter inputs across the skills and plugins pages have no associated `<label>` or `aria-label`. Screen reader users cannot identify the purpose of these fields.
**Fix:**

```HTML
1    <!-- Before -->
2    <input type="text" name="text">
3
4    <!-- After -->
5    <label for="search-input">Search skills</label>
6    <input type="text" name="text" id="search-input">
```

🟡 **Medium**

**[WCAG 1.1.1] IMAGE HAS EMPTY ALT TEXT**
**Severity:** Medium
**Detail:** 3 images have `alt=""` but are not marked as decorative (no `role="presentation"` or `role="none"`).
**Fix:** For decorative images, add `role="presentation"`. For informative images, provide descriptive alt text.

**[WCAG 1.3.1] SKIPPED HEADING LEVEL**
**Severity:** Medium
**Detail:** 3 instances of heading levels being skipped. Screen reader users expect sequential heading hierarchy.
**Fix:** Ensure heading levels increment by one (H1 → H2 → H3).

**[WCAG 2.4.1] MISSING SKIP NAVIGATION LINK**
**Severity:** Medium
**Detail:** No skip navigation link found on any of the 3 audited pages.
**Fix:**

```HTML
1    <a href="#main" class="sr-only focus:not-sr-only">Skip to main content</a>
```

🟢 **Low**

**[WCAG 3.3.2] FORM INPUT USING ARIA-LABEL INSTEAD OF VISIBLE LABEL**
**Severity:** Low
**Detail:** 4 form inputs use `aria-label` but have no visible `<label>`. Visible labels benefit all users, not just screen reader users.
**Fix:** Add a visible `<label>` alongside the `aria-label`.

---

## Compliance Checklist

| WCAG Criterion | Level | Status |
|----------------|-------|--------|
| 1.1.1 Non-text Content | A | ❌ Fail |
| 1.3.1 Info and Relationships | A | ❌ Fail |
| 1.4.3 Contrast (Minimum) | AA | ❌ Fail |
| 2.4.1 Bypass Blocks | A | ❌ Fail |
| 2.4.2 Page Titled | A | ✅ Pass |
| 2.4.4 Link Purpose | A | ✅ Pass |
| 2.4.6 Headings and Labels | AA | ✅ Pass |
| 3.1.1 Language of Page | A | ✅ Pass |
| 3.3.2 Labels | A | ❌ Fail |
| 4.1.2 Name, Role, Value | A | ✅ Pass |

---

## Remediation Roadmap

**Priority 1 — Fix Immediately (Critical)**

1. "Search" heading contrast — **Estimated effort: 15 minutes**

**Priority 2 — Fix This Week (High)**

1. Borderline contrast failures (4.0-4.5:1) on nav and filter elements — **Estimated effort: 1-2 hours**
2. Missing labels on search/filter inputs — **Estimated effort: 30 minutes**

**Priority 3 — Fix This Sprint (Medium)**

1. Skip navigation link — **Estimated effort: 30 minutes**
2. Heading hierarchy cleanup — **Estimated effort: 30 minutes**
3. Empty alt text review — **Estimated effort: 1 hour**

**Priority 4 — Nice to Have (Low)**

1. Add visible labels alongside aria-labels on inputs — **Estimated effort: 30 minutes**

---

## Limitations

This audit covers approximately 30-50% of WCAG 2.1 AA criteria through automated testing. The following require manual testing:

● Keyboard navigation and focus management
● Screen reader compatibility
● Video/audio captions and descriptions
● Dynamic content and interaction patterns
● Cognitive accessibility (reading level, plain language)

The audit used Playwright for full JavaScript rendering. However, dynamic content revealed on hover/click, modal behavior, and form validation announcements require manual testing.

A full WCAG 2.1 AA conformance evaluation requires manual testing. This report identifies issues detectable through automated analysis and provides a prioritized remediation roadmap.
