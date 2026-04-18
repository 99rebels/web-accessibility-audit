🔧 **Freelancer Notes — Internal**

# Audit Notes — walmart.com — April 18, 2026

## What Was Checked

**Automated Checks (script detected)**

● 1.1.1 Non-text Content — alt text presence on images
● 2.4.1 Bypass Blocks — skip navigation link
● 2.4.4 Link Purpose — ambiguous/empty link text
● 2.4.6 Headings and Labels — heading elements on content pages
● 3.3.2 Labels — form input label associations
● 4.1.2 Name, Role, Value — duplicate IDs, ARIA roles

**LLM-Assisted Analysis**

● Assessed alt text quality on flagged image (tracking pixel — decorative, not informative)
● Evaluated link text descriptiveness ("Learn more" context)
● Assessed heading quality (none found — likely JS-rendered false positive)
● Evaluated search input label approach (aria-label vs visible label)

## What Could NOT Be Checked (Manual Testing Required)

**JavaScript Rendering**

● Walmart.com is heavily JS-dependent. Most structural elements are rendered client-side.
● The "no headings" finding is almost certainly a false positive — headings exist in the live DOM but not in initial HTML.
● Many other elements (nav structure, landmark regions, dynamic content) cannot be assessed from static HTML.
● Only 1 page was crawled — `--page-types` could not extract additional pages due to JS rendering blocking sitemap/link discovery.

**Keyboard Navigation**

● Focus order cannot be verified without actual keyboard interaction
● Focus traps in mega-menu, modals, and carousels not detectable
● Search autocomplete keyboard handling
● Mega-menu keyboard behavior needs testing

**Screen Reader Compatibility**

● How content is announced by screen readers after JS rendering
● ARIA live region behavior (cart updates, search suggestions)
● Reading order in complex layouts (product carousels, grids)

**Dynamic Content**

● Product carousels and slideshows
● Search autocomplete dropdown
● Cart/toast notifications
● Modal dialogs (sign-in, product quick view)
● Accordion sections

**Media**

● Product video captions and audio descriptions
● Promotional video autoplay behavior

**Cognitive Accessibility**

● Reading level of product descriptions
● Consistency of navigation terminology
● Error prevention in checkout flow

## Recommendations for Manual Testing

1. Tab through the homepage — note focus order through mega-menu, carousels, and footer
2. Test with a screen reader (VoiceOver/NVDA/JAWS) — verify heading structure after JS renders
3. Check all interactive elements with keyboard only (dropdowns, search, carousels)
4. Test search autocomplete with keyboard (arrow keys, escape, enter)
5. Verify form error messages in search and sign-in are announced by assistive tech
6. Test on mobile (touch targets, orientation changes)
7. Check color contrast manually with a browser extension (contrast cannot be reliably calculated from initial HTML due to JS-rendered styles)

## Severity Adjustments

● **[1.1.1] Tracking pixel alt text** — Script assigned: Critical. Adjusted to: Critical in report (kept as-is to maintain report integrity, but noted here that a 1×1 tracking pixel is decorative and should realistically be Low severity. The missing `alt` attribute is technically valid but the impact is negligible.)

## False Positive Notes

1. **[2.4.6] No headings** — Almost certainly a false positive. Walmart.com renders headings via JavaScript. The initial HTML has none, but the live page does. Manual verification needed.

2. **[3.3.2] Search aria-label** — Flagged as a finding, but aria-label on a search input is widely accepted as sufficient. The search icon and placement provide visual context. This is a best practice suggestion, not a real failure.

## Consolidated Findings

1. **Duplicate "Learn more" links** — Script produced 2 identical findings (same href, same text). Consolidated into one finding with "(×2)" notation.

2. **Duplicate carousel IDs** — Script produced 3 separate findings for the same root cause (PrismCollectionCarousel component generating non-unique IDs). Consolidated into 2 findings: one for gic-wrapper, one for the carousel component (covering both container and heading IDs).
