# Audit Notes — stripe.com — 2026-04-19

## What Was Checked

**Automated Checks (script detected)**

● 1.1.1 Non-text Content — image alt text presence and quality
● 1.3.1 Info and Relationships — heading hierarchy, table headers
● 1.4.3 Contrast (Minimum) — computed styles via Playwright `getComputedStyle()`, background walk-up for transparent elements
● 2.4.1 Bypass Blocks — skip navigation link
● 2.4.2 Page Titled — `<title>` element
● 2.4.4 Link Purpose — ambiguous/empty link text
● 2.4.6 Headings and Labels — heading presence on content pages
● 3.1.1 Language of Page — `<html lang>` attribute
● 3.3.2 Labels — form input labels (no forms found on audited pages)
● 4.1.2 Name, Role, Value — duplicate IDs, ARIA roles without accessible names

**LLM-Assisted Analysis**

● Alt text quality assessment (empty alt without decoration marker)
● Link text descriptiveness in context
● Heading structure quality
● Contrast finding interpretation and fix suggestions

---

## What Could NOT Be Checked (Manual Testing Required)

**JavaScript Rendering**

● Site is JS-heavy (React/Next.js framework detected). Playwright was used for full rendering — all 4 pages were rendered before analysis.
● The 561 empty links may include links that are populated by JavaScript after the initial render — verify these aren't false positives by checking if the links become populated on interaction.

**Keyboard Navigation**
● Focus order cannot be verified without actual keyboard interaction
● Focus traps in modals/dropdowns not detectable
● The navigation menu likely has dropdown behavior that needs keyboard testing
● Mega-menu patterns need focus trap verification

**Screen Reader Compatibility**
● How the navigation menu announces to screen readers
● ARIA live region behavior
● Reading order in complex card layouts (pricing grid, guides cards, case study cards)
● The "Products" dropdown menu accessibility

**Dynamic Content**
● Content revealed on hover/click (navigation dropdowns, pricing toggles)
● Modal and dialog behavior
● The pricing page likely has interactive toggles (monthly/annual pricing)
● Language picker behavior
● Cookie consent dialogs

**Media**

● No video/audio elements detected on audited pages
● Autoplay behavior not testable via automated audit

**Cognitive Accessibility**

● Reading level not assessed
● Consistency of terminology not fully verified

---

## Recommendations for Manual Testing

1. Tab through every page — note focus order issues and traps in navigation, pricing, and card components
2. Test with a screen reader (VoiceOver/NVDA/JAWS) — especially the navigation dropdown, pricing page, and guides cards
3. Check all empty links — verify which are truly icon-only and which might be JS-populated
4. Test navigation dropdown with keyboard only — verify it's operable and announced correctly
5. Test pricing page interactive elements (toggle, tooltips) with keyboard
6. Verify the BMW case study card contrast — the 1.00:1 and 1.06:1 ratios suggest a dark-on-dark or light-on-light overlay
7. Test on mobile viewport — check touch target sizes and orientation behavior

## Severity Adjustments

None made. All severities match script assignment.

## False Positive Notes

● **Empty links (×561):** Very high count likely includes decorative/icon links. Many are probably wrapped SVG icons. The freelancer should verify which are interactive and which are decorative before quoting fix estimates.
● **Empty alt text (×39):** Some may be intentionally decorative. Recommend reviewing each and adding `role="presentation"` where appropriate rather than adding alt text to all.
● **Ambiguous link text (×32):** Some "Read more" links may have sufficient context from surrounding text. Screen readers announce surrounding content, so not all will be true accessibility barriers.

## Consolidated Findings

Raw findings: 674 → Unique: 43 after deduplication.
Major consolidation: 561 empty link findings consolidated into 1 finding with count ×561.
39 empty alt findings consolidated into 1 finding with count ×39.

## Page Discovery Notes

Sitemap returned a CAPTCHA page (bot detection). Homepage link extraction was used as fallback — discovered 102 pages across 4 types. Audited 4 representative pages:
- Homepage (stripe.com)
- Pricing page (stripe.com/ie/pricing)
- News article (stripe.com/ie/newsroom/news/stripe-openai-instant-checkout)
- Guides index (stripe.com/ie/guides)
