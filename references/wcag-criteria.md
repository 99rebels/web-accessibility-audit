# WCAG Criteria Reference

Detailed descriptions of each WCAG 2.1 criterion checked by the audit script.

## 1.1.1 Non-text Content (Level A)

All non-text content that is presented to the user has a text alternative that serves the equivalent purpose.

**What we check:**
- `<img>` elements missing `alt` attribute entirely
- `<img>` elements with empty `alt=""` on images that appear informative
- `<svg>` elements without `aria-label`, `role`, or `<title>`

**What we can't check:**
- Whether existing alt text is accurate or descriptive (LLM assists)
- Decorative vs informative distinction in all cases

**Fix pattern:**
```html
<!-- Missing alt -->
<img src="photo.jpg">
<!-- Fix -->
<img src="photo.jpg" alt="Description of the image">

<!-- Decorative image -->
<img src="divider.png" role="presentation" alt="">
```

## 1.3.1 Info and Relationships (Level A)

Information, relationships, and meaning conveyed through presentation can be programmatically determined or are available in text.

**What we check:**
- Heading hierarchy (no skipped levels, single H1, H1 exists)
- Table header cells (`<th>`)
- Form label associations (`<label for="...">`)
- List markup (`<ul>`, `<ol>`, `<li>`)

**Fix pattern:**
```html
<!-- Skipped heading -->
<h1>Title</h1>
<h3>Subtitle</h3>  <!-- Should be H2 -->
<!-- Fix -->
<h1>Title</h1>
<h2>Subtitle</h2>

<!-- Table without headers -->
<table><tr><td>Name</td><td>Age</td></tr></table>
<!-- Fix -->
<table><tr><th>Name</th><th>Age</th></tr>...</table>
```

## 1.4.1 Use of Color (Level A)

Color is not used as the only visual means of conveying information, indicating an action, prompting a response, or distinguishing a visual element.

**What we check:**
- Color-only indicators in form error messages
- Color-only status indicators

**Limitation:** Full detection requires understanding context — the LLM assists.

## 1.4.3 Contrast (Minimum) (Level AA)

The visual presentation of text and images of text has a contrast ratio of at least 4.5:1 (normal text) or 3:1 (large text).

**What we check:**
- Elements with inline `style` attributes containing both `color` and `background-color`
- Calculated using the WCAG relative luminance algorithm

**Thresholds:**
- Normal text (< 18pt / < 14pt bold): 4.5:1 minimum
- Large text (>= 18pt / >= 14pt bold): 3:1 minimum

**Fix pattern:**
```css
/* Fails: 2.1:1 contrast */
color: #999999; background: #ffffff;
/* Fix: increase to at least 4.5:1 */
color: #595959; background: #ffffff;
```

## 2.4.1 Bypass Blocks (Level A)

A mechanism is available to bypass blocks of content that are repeated on multiple web pages.

**What we check:**
- Presence of a skip navigation link (link with "skip" in class or id)

**Fix pattern:**
```html
<a href="#main" class="sr-only focus:not-sr-only">Skip to main content</a>
<main id="main">...</main>
```

## 2.4.2 Page Titled (Level A)

Web pages have titles that describe topic or purpose.

**What we check:**
- Missing `<title>` element
- Empty `<title>` element

**Fix pattern:**
```html
<title>Page Description — Site Name</title>
```

## 2.4.4 Link Purpose (Level A)

The purpose of each link can be determined from link text alone, or from the link text together with its programmatically determined link context.

**What we check:**
- Empty links without `aria-label` or `aria-labelledby`
- Ambiguous link text: "click here", "read more", "more", "here", "link", "learn more", "go", "continue", "details"

**Fix pattern:**
```html
<!-- Ambiguous -->
<a href="/about">Click here</a>
<!-- Fix -->
<a href="/about">Read about our company</a>

<!-- Empty link (icon) -->
<a href="/search"><svg>...</svg></a>
<!-- Fix -->
<a href="/search" aria-label="Search"><svg>...</svg></a>
```

## 2.4.6 Headings and Labels (Level AA)

Headings and labels describe topic or purpose.

**What we check:**
- Content pages (>5000 chars HTML) with zero heading elements

## 3.1.1 Language of Page (Level A)

The default human language of each web page can be programmatically determined.

**What we check:**
- Missing `lang` attribute on `<html>` element

**Fix pattern:**
```html
<html lang="en">
```

## 3.3.2 Labels (Level A)

All user interface components have a label.

**What we check:**
- Form inputs (text, email, password, tel, url, search, number, select, textarea) without `<label>` or `aria-label`
- Missing `autocomplete` attributes on common input types (name, email, phone, etc.)

**Fix pattern:**
```html
<!-- Missing label -->
<input type="email" id="email" name="email">
<!-- Fix -->
<label for="email">Email address</label>
<input type="email" id="email" name="email" autocomplete="email">
```

## 4.1.2 Name, Role, Value (Level A)

All UI components have a name, role, value, and can be programmatically determined.

**What we check:**
- Duplicate `id` attributes
- Elements with `role` but missing `aria-label` or `aria-labelledby`
