# Web Accessibility Audit — example.com

**Score: 82/100 — Grade B** · 4 pages · WCAG 2.1 AA · Playwright JS rendering

**Findings: 16 Critical · 42 High · 28 Medium**

---

## 🔴 Critical

**[WCAG 1.4.3] Color Contrast — AA Normal Text** · Pages: 4/4
Multiple elements fail the 4.5:1 contrast ratio:
- Navigation "Products" link: **1.00:1** (invisible)
- Hero heading: **2.39:1**
- Pricing figure "$49/mo": **1.79:1**

**[WCAG 1.1.1] Image Missing Alt Text** · Pages: 1/4
1 image has no alt attribute at all.

---

## 🟠 High

**[WCAG 2.4.4] Icon Links Missing Accessible Name** · ×464
SVG icon links have no `aria-label`. Screen reader users can't determine link purpose.

**[WCAG 3.3.2] Form Input Missing Label** · ×3
Search inputs have no `<label>` or `aria-label`.

---

## 🟡 Medium

- **[WCAG 2.4.1]** Missing skip navigation link
- **[WCAG 1.3.1]** Skipped heading level · ×2
- **[WCAG 2.4.4]** Ambiguous link text · ×12
- **[WCAG 1.1.1]** Empty alt without `role="presentation"` · ×8

---

## 📋 Compliance Checklist

✅ 2.4.2 Page Titled · ✅ 2.4.6 Headings Present · ✅ 3.1.1 Language of Page
❌ 1.1.1 Non-text Content · ❌ 1.3.1 Info and Relationships · ❌ 1.4.3 Contrast · ❌ 2.4.1 Bypass Blocks · ❌ 2.4.4 Link Purpose

---

## 🛠 Remediation Roadmap

1. Color contrast on nav/hero/pricing — **~4-8 hrs**
2. Add aria-label to icon links — **~8-12 hrs**
3. Add labels to search inputs — **~30 min**
4. Skip navigation link — **~30 min**
5. Heading hierarchy + ambiguous links — **~3-5 hrs**

---

## 📊 Page Discovery
Source: Homepage links (sitemap returned CAPTCHA) · Found: 102 pages · Audited: 4

## 🔧 Freelancer Notes
- 464 icon links likely includes decorative SVGs — verify before quoting
- Pricing page has interactive toggles — needs manual keyboard testing
- No forms on blog/contact pages — form checks couldn't run

## 📄 Output Files
- `example.com-client-report.md` — full client-ready report
- `example.com-freelancer-notes.md` — internal audit notes
