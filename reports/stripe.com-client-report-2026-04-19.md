# WCAG 2.1 AA Accessibility Audit Report

**Client:** stripe.com
**Date:** 2026-04-19
**Pages Audited:** 4
**Standard:** WCAG 2.1 Level AA
**Scope:** Automated audit with JS rendering and LLM-assisted analysis

---

## Executive Summary

Stripe.com scored **82/100 — Grade B** on automated WCAG 2.1 AA testing. While the site demonstrates strong structural foundations (proper heading hierarchy, language attributes, and ARIA usage), two critical categories of issues were identified: widespread insufficient color contrast and a significant number of empty links without accessible names.

The most urgent finding is that key navigation elements, hero text, and pricing information fail contrast requirements — some at ratios as low as 1.00:1 (identical foreground and background colors). This affects the main navigation ("Products"), the primary hero heading ("Financial infrastructure to grow your revenue"), and pricing figures on the pricing page. These are customer-facing elements that directly impact usability for users with visual impairments.

The empty link issue (561 instances across 4 pages) is likely caused by icon-only links or decorative elements wrapped in `<a>` tags without `aria-label` attributes. While some may be decorative, the volume suggests a systemic pattern that should be reviewed.

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
| 🔴 Critical | 16 |
| 🟠 High | 576 |
| 🟡 Medium | 82 |
| 🟢 Low | 0 |

---

## Detailed Findings

🔴 **Critical**

**[WCAG 1.4.3] INSUFFICIENT COLOR CONTRAST (AA NORMAL TEXT)**
**Severity:** Critical
**Pages affected:** 4/4
**Detail:** Multiple text elements fail the minimum 4.5:1 contrast ratio. The most severe instances include the main navigation "Products" item at 1.00:1 (effectively invisible text), the hero heading "Financial infrastructure to grow your revenue" at 2.39:1, and pricing figures ("10%", "€50.28") at 1.79:1 and 2.51:1 respectively. On the Guides page, multiple card links fail with ratios as low as 1.76:1.
**Fix:**

```HTML
1    <!-- Before: Navigation item with 1.00:1 contrast -->
2    <li class="hds-navigation-menu__item">
3      <a>Products</a>
4    </li>
5
6    <!-- After: Add visible foreground color -->
7    <li class="hds-navigation-menu__item">
8      <a style="color: #1a1a2e;">Products</a>
9    </li>
```

```HTML
1    <!-- Before: Hero heading with 2.39:1 contrast -->
2    <h1 class="hero-section__title">
3      Financial infrastructure to grow your revenue
4    </h1>
5
6    <!-- After: Darken text or lighten background -->
7    <h1 class="hero-section__title" style="color: #1a1a2e;">
8      Financial infrastructure to grow your revenue
9    </h1>
```

**[WCAG 1.4.3] INSUFFICIENT COLOR CONTRAST (AA LARGE TEXT)**
**Severity:** Critical
**Pages affected:** 2/4
**Detail:** Large text elements (headings) fail the 3.0:1 threshold. The homepage hero heading "Financial infrastructure to grow your revenue" is at 2.39:1. The stats section heading "The backbone of global commerce" is at 1.65:1. A card heading "500M+" on the developers section is at 1.19:1.
**Fix:** Ensure all heading elements meet at minimum 3.0:1 contrast against their backgrounds. Review CSS custom properties or theme variables that may be setting these colors globally.

**[WCAG 1.1.1] IMAGE MISSING ALT TEXT**
**Severity:** Critical
**Pages affected:** 1/4
**Detail:** One image on the newsroom page has no `alt` attribute at all (not even empty). The image source points to `images.stripeassets.com`.
**Fix:**

```HTML
1    <!-- Before -->
2    <img src="https://images.stripeassets.com/...">
3
4    <!-- After -->
5    <img src="https://images.stripeassets.com/..." alt="Description of image content">
```

🟠 **High**

**[WCAG 2.4.4] EMPTY LINK WITH NO ACCESSIBLE NAME**
**Severity:** High
**Pages affected:** 4/4
**Detail:** 561 links across the 4 audited pages have no text content and no `aria-label`. These are likely icon-only links (social media icons, navigation icons, action buttons) where the visual icon provides context sighted users can see, but screen reader users have no indication of the link's purpose.
**Fix:**

```HTML
1    <!-- Before -->
2    <a href="/some-link"><svg>...</svg></a>
3
4    <!-- After -->
5    <a href="/some-link" aria-label="Twitter"><svg>...</svg></a>
```

**[WCAG 1.4.3] INSUFFICIENT COLOR CONTRAST (AA NORMAL TEXT) — BORDERLINE FAILURES**
**Severity:** High
**Pages affected:** 3/4
**Detail:** Several elements are very close to passing but fall just short of 4.5:1: the "Sign in" link (4.45:1), the "English" language picker (4.04:1), and pricing page labels (3.84:1–4.04:1). These are quick wins — minor color adjustments would bring them into compliance.
**Fix:** Adjust foreground colors slightly. Increasing darkness by 5-10% on each should be sufficient.

**[WCAG 4.1.2] DUPLICATE ID: "A"**
**Severity:** High
**Detail:** ID "a" appears 2 times. Duplicate IDs break label associations and ARIA references.
**Fix:** Rename to unique values: `"a-2"` on the second occurrence.

**[WCAG 4.1.2] DUPLICATE ID: "B"**
**Severity:** High
**Detail:** ID "b" appears 2 times. Same root cause as above.
**Fix:** Rename to unique values: `"b-2"` on the second occurrence.

🟡 **Medium**

**[WCAG 1.1.1] IMAGE HAS EMPTY ALT TEXT**
**Severity:** Medium
**Detail:** 39 images have `alt=""` but are not marked as decorative (no `role="presentation"` or `role="none"`). Some of these may be decorative, but without explicit decoration markers, assistive technologies may flag them.
**Fix:** For decorative images, add `role="presentation"`. For informative images, provide descriptive alt text.

**[WCAG 1.3.1] MULTIPLE H1 HEADINGS**
**Severity:** Medium
**Detail:** Multiple pages have more than one H1 heading. Best practice for screen reader compatibility is a single H1 per page.
**Fix:** Use H1 for the primary page heading only. Demote additional H1s to H2.

**[WCAG 1.3.1] SKIPPED HEADING LEVEL**
**Severity:** Medium
**Detail:** 2 instances of heading levels being skipped (e.g., H1 → H3 without an H2).
**Fix:** Ensure heading levels increment by one (H1 → H2 → H3).

**[WCAG 2.4.1] MISSING SKIP NAVIGATION LINK**
**Severity:** Medium
**Detail:** No skip navigation link found on any of the 4 audited pages. Keyboard users must tab through all navigation items to reach the main content.
**Fix:**

```HTML
1    <!-- Before -->
2    <body>
3      <nav>...</nav>
4
5    <!-- After -->
6    <body>
7      <a href="#main" class="sr-only focus:not-sr-only">Skip to main content</a>
8      <nav>...</nav>
```

**[WCAG 2.4.4] AMBIGUOUS LINK TEXT**
**Severity:** Medium
**Detail:** 32 instances of ambiguous link text across 4 pages. Common examples include "Learn more", "Read more", "Read story".
**Fix:** Use descriptive text: "Learn more about [specific topic]" or "Read the BMW case study".

**[WCAG 4.1.2] ELEMENT WITH ROLE BUT NO ACCESSIBLE NAME**
**Severity:** Medium
**Detail:** 1 element has a `role` attribute but no `aria-label` or `aria-labelledby`.
**Fix:** Add `aria-label="Description"` to the element.

---

## Compliance Checklist

| WCAG Criterion | Level | Status |
|----------------|-------|--------|
| 1.1.1 Non-text Content | A | ❌ Fail |
| 1.3.1 Info and Relationships | A | ❌ Fail |
| 1.4.3 Contrast (Minimum) | AA | ❌ Fail |
| 2.4.1 Bypass Blocks | A | ❌ Fail |
| 2.4.2 Page Titled | A | ✅ Pass |
| 2.4.4 Link Purpose | A | ❌ Fail |
| 2.4.6 Headings and Labels | AA | ✅ Pass |
| 3.1.1 Language of Page | A | ✅ Pass |
| 3.3.2 Labels | A | ✅ Pass |
| 4.1.2 Name, Role, Value | A | ❌ Fail |

---

## Remediation Roadmap

**Priority 1 — Fix Immediately (Critical)**

1. Color contrast on navigation, hero, and pricing elements — **Estimated effort: 4-8 hours** (CSS variable/theme review)

**Priority 2 — Fix This Week (High)**

1. Empty links — add aria-label to all icon-only links — **Estimated effort: 8-16 hours** (audit all icon components)
2. Borderline contrast failures (4.0-4.5:1) — **Estimated effort: 1-2 hours**
3. Duplicate IDs "a" and "b" — **Estimated effort: 15 minutes**

**Priority 3 — Fix This Sprint (Medium)**

1. Skip navigation link — **Estimated effort: 30 minutes**
2. Ambiguous link text — **Estimated effort: 2-4 hours**
3. Empty alt text review — **Estimated effort: 2-4 hours**
4. Heading hierarchy cleanup — **Estimated effort: 1-2 hours**

**Priority 4 — Nice to Have (Low)**

1. Role without accessible name — **Estimated effort: 15 minutes**

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
