# WCAG 2.1 AA Accessibility Audit Report

**Client:** walmart.com
**Date:** April 18, 2026
**Pages Audited:** 1
**Standard:** WCAG 2.1 Level AA
**Scope:** Automated audit with LLM-assisted analysis

---

## Executive Summary

Walmart's homepage has a compliance score of **65/100 (Grade D)**, indicating significant accessibility barriers. The most critical finding is a missing alt attribute on a tracking pixel image, which represents a broader pattern of accessibility oversights on a site of this scale.

The site has strong ARIA implementation (84 ARIA elements detected) and proper language declaration, but fails in several foundational areas: no skip navigation, zero heading elements on a content-heavy homepage, duplicate IDs that break assistive technology references, and multiple ambiguous link texts.

Given that Walmart is a major e-commerce platform and the #1 target for ADA digital accessibility lawsuits (e-commerce accounts for 78% of all cases), these findings represent real legal exposure.

**Compliance Score: 65/100 — Grade D**

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
| 🟠 High | 5 |
| 🟡 Medium | 3 |
| 🟢 Low | 1 |

---

## Detailed Findings

🔴 **Critical**

**[WCAG 1.1.1] IMAGE MISSING ALT TEXT**
**Severity:** Critical
**Pages affected:** 1/1
**Detail:** Tracking pixel image has no alt attribute. While tracking pixels are typically decorative, the missing `alt` means screen readers may announce the URL, confusing users. More importantly, this pattern suggests alt text enforcement may be inconsistent across the site.
**Fix:**

```HTML
1
2    <img src="...pixel_4414782a">

3
4    <img src="...pixel_4414782a" alt="" role="presentation">
```

🟠 **High**

**[WCAG 2.4.4] EMPTY LINK WITH NO ACCESSIBLE NAME**
**Severity:** High
**Detail:** An empty link (`<a href="">`) was found with no text content and no `aria-label`. Screen reader users cannot determine the purpose of this link. This is likely a JavaScript-triggered element that should include `aria-label`.
**Fix:**

```HTML
1
2    <a href="">

4    <a href="" aria-label="Menu" role="button">
```

**[WCAG 4.1.2] DUPLICATE ID: "GIC-WRAPPER"**
**Severity:** High
**Detail:** ID "gic-wrapper" appears 2 times. Duplicate IDs break label associations and ARIA references. Screen readers may only find the first element, ignoring the second.
**Fix:** Rename the second instance to `gic-wrapper-2`.

**[WCAG 4.1.2] DUPLICATE ID: "PRISMCOLLECTIONCAROUSEL-VERTICALSMALL-UNDEFINED-LYDPCYUT"**
**Severity:** High
**Detail:** Duplicate carousel component IDs (container and heading both affected). This appears to be a dynamically generated ID collision — the carousel component renders multiple times without unique IDs per instance.
**Fix:** Ensure dynamic components generate unique IDs per instance (e.g., using a counter or UUID suffix).

**[WCAG 2.4.6] NO HEADINGS FOUND ON CONTENT PAGE**
**Severity:** High
**Detail:** The homepage has substantial content (70 links, 20 images) but zero heading elements in the initial HTML. This is a significant navigation barrier — screen reader users rely on headings to understand page structure and jump between sections. *Note: Walmart is JavaScript-heavy; headings may render client-side.*
**Fix:**

```HTML
1
2    <h1>Walmart — Save Money. Live Better</h1>

4    <h2>Featured Departments</h2>
5    <h2>Trending Now</h2>
```

🟡 **Medium**

**[WCAG 2.4.1] MISSING SKIP NAVIGATION LINK**
**Severity:** Medium
**Detail:** No skip navigation link found. Keyboard users must tab through all navigation items before reaching the main content. On a page with this many links, this is a significant usability barrier.
**Fix:**

```HTML
1    <a href="#main" class="sr-only focus:not-sr-only">Skip to main content</a>
```

**[WCAG 2.4.4] AMBIGUOUS LINK TEXT: "LEARN MORE" (×2)**
**Severity:** Medium
**Detail:** Two links use the text "Learn more" without additional context. When screen reader users navigate by link list, they see identical "Learn more" entries with no way to distinguish them. Both point to the Virtual Care section.
**Fix:**

```HTML
1
2    <a href="...">Learn more</a>

4    <a href="...virtual-care...">Learn more about Virtual Care</a>
```

🟢 **Low**

**[WCAG 3.3.2] FORM INPUT USING ARIA-LABEL INSTEAD OF VISIBLE LABEL**
**Severity:** Low
**Detail:** The search input uses `aria-label` but has no visible `<label>`. While technically compliant, visible labels benefit all users.
**Fix:** Add a visible label: `<label for="search">Search</label>`

---

## Compliance Checklist

| WCAG Criterion | Level | Status |
|----------------|-------|--------|
| 1.1.1 Non-text Content | A | ❌ Fail |
| 2.4.1 Bypass Blocks | A | ❌ Fail |
| 2.4.2 Page Titled | A | ✅ Pass |
| 2.4.4 Link Purpose | A | ❌ Fail |
| 2.4.6 Headings and Labels | AA | ❌ Fail |
| 3.1.1 Language of Page | A | ✅ Pass |
| 3.3.2 Labels | A | ⚠️ Partial |
| 4.1.2 Name, Role, Value | A | ❌ Fail |

---

## Remediation Roadmap

**Priority 1 — Fix Immediately (Critical)**

1. Add `alt=""` and `role="presentation"` to tracking pixel images — **Estimated effort: 30 minutes**

**Priority 2 — Fix This Week (High)**

1. Add `aria-label` to empty link elements — **Estimated effort: 1 hour**
2. Fix duplicate IDs in carousel components — **Estimated effort: 2 hours**
3. Add heading structure to homepage — **Estimated effort: 2 hours**

**Priority 3 — Fix This Sprint (Medium)**

1. Add skip navigation link — **Estimated effort: 30 minutes**
2. Replace "Learn more" with descriptive link text — **Estimated effort: 1 hour**

**Priority 4 — Nice to Have (Low)**

1. Add visible label to search input — **Estimated effort: 30 minutes**

---

## Limitations

This audit covers approximately 30-50% of WCAG 2.1 AA criteria through automated testing. The following require manual testing:

● Keyboard navigation and focus management
● Screen reader compatibility
● Video/audio captions and descriptions
● Dynamic content and interaction patterns
● Cognitive accessibility (reading level, plain language)

**Important:** Walmart.com is heavily JavaScript-dependent. This audit captures only the initial HTML response. A comprehensive manual audit should be conducted to assess the fully rendered page.
