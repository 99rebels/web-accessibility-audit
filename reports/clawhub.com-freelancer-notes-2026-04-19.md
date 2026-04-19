# Audit Notes — clawhub.com — 2026-04-19

## What Was Checked

**Automated Checks (script detected)**

● 1.1.1 Non-text Content — image alt text presence and quality
● 1.3.1 Info and Relationships — heading hierarchy
● 1.4.3 Contrast (Minimum) — computed styles via Playwright `getComputedStyle()`
● 2.4.1 Bypass Blocks — skip navigation link
● 2.4.2 Page Titled — `<title>` element
● 2.4.4 Link Purpose — link text analysis
● 2.4.6 Headings and Labels — heading presence
● 3.1.1 Language of Page — `<html lang>` attribute
● 3.3.2 Labels — form input labels
● 4.1.2 Name, Role, Value — duplicate IDs, ARIA roles

**LLM-Assisted Analysis**

● Alt text quality assessment
● Link text descriptiveness
● Heading structure quality
● Contrast finding interpretation and fix suggestions

---

## What Could NOT Be Checked (Manual Testing Required)

**JavaScript Rendering**
● Site is JS-heavy. Playwright was used for full rendering — all 3 pages rendered successfully.
● Search functionality and filter interactions could not be tested (requires input submission).

**Keyboard Navigation**
● Tab order through navigation, search, and filter elements
● Focus management on the search/filter inputs
● Mobile navigation menu behavior

**Screen Reader Compatibility**
● How the search and filter interface announces to screen readers
● Reading order in the skills/plugins listing grid
● Navigation menu behavior

**Dynamic Content**
● Search results behavior (requires input)
● Filter/category interactions
● Any modal or dialog behavior

**Media**
● No video/audio elements detected

---

## Recommendations for Manual Testing

1. Tab through all pages — verify focus order through nav, search, and skill cards
2. Test search with a screen reader — verify the input is announced correctly
3. Test filter interactions with keyboard
4. Verify the "Search" heading contrast — 1.00:1 seems extreme, may be a dynamic styling issue
5. Check if the borderline contrast failures (4.0-4.5:1) are consistent across different screen sizes

## Severity Adjustments

None made. All severities match script assignment.

## False Positive Notes

● **"Search" heading at 1.00:1:** This ratio is extremely low and may indicate the heading uses the same color as its background in a specific section. Verify manually — if the heading is inside a colored container, the computed background may not match the visual background.
● **Borderline contrast (4.0-4.5:1):** These are real failures per WCAG but minor in practice. The "Install" button at 4.12:1 and "Most downloaded" at 4.49:1 are very close to passing.

## Consolidated Findings

Raw findings: 23 → Unique: 13 after deduplication.

## Page Discovery Notes

No sitemap found (or returned non-sitemap content). Homepage link extraction used — discovered 20 pages across 3 types. Audited 2 representative pages:
- Skills listing (clawhub.com/skills)
- Plugins listing (clawhub.com/plugins)
