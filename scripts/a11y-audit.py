#!/usr/bin/env python3
"""
a11y-audit.py — Automated WCAG 2.1 AA accessibility audit for websites.

Pure Python stdlib. No dependencies.

Usage:
    python3 a11y-audit.py <url> [--max-pages N] [--timeout SECONDS] [--max-bytes BYTES] [--no-ssl-verify]

Output: JSON to stdout
"""

import sys
import json
import re
import math
import argparse
import urllib.request
import urllib.error
import urllib.parse
import ssl
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from datetime import datetime, timezone
from collections import defaultdict

# ─── Constants ───────────────────────────────────────────────────────────────

USER_AGENT = "Mozilla/5.0 (compatible; A11Y-Audit/1.0)"

# WCAG 2.1 AA contrast thresholds
CONTRAST_AA_NORMAL = 4.5   # 4.5:1 for normal text (< 18pt / < 14pt bold)
CONTRAST_AA_LARGE = 3.0     # 3:1 for large text (>= 18pt / >= 14pt bold)
CONTRAST_AA_UI = 3.0        # 3:1 for UI components and graphical objects
LARGE_TEXT_PX = 18
LARGE_TEXT_BOLD_PX = 14

# Font size detection patterns (pt and px)
FONT_SIZE_PX_RE = re.compile(r'font-size\s*:\s*(\d+(?:\.\d+)?)\s*px', re.I)
FONT_SIZE_PT_RE = re.compile(r'font-size\s*:\s*(\d+(?:\.\d+)?)\s*pt', re.I)
FONT_WEIGHT_RE = re.compile(r'font-weight\s*:\s*(\d+|bold|bolder)', re.I)

# Color patterns
HEX_COLOR_RE = re.compile(r'#(?:[0-9a-f]{3}){1,2}\b', re.I)
RGB_COLOR_RE = re.compile(r'rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', re.I)
RGBA_COLOR_RE = re.compile(r'rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', re.I)
COLOR_NAME_RE = re.compile(
    r'(?:color|background-color|background)\s*:\s*([a-z]+)',
    re.I
)

# Common CSS color names to hex
CSS_COLORS = {
    'black': '#000000', 'white': '#ffffff', 'red': '#ff0000', 'green': '#008000',
    'blue': '#0000ff', 'yellow': '#ffff00', 'orange': '#ffa500', 'purple': '#800080',
    'gray': '#808080', 'grey': '#808080', 'silver': '#c0c0c0', 'maroon': '#800000',
    'olive': '#808000', 'navy': '#000080', 'teal': '#008080', 'aqua': '#00ffff',
    'fuchsia': '#ff00ff', 'lime': '#00ff00', 'pink': '#ffc0cb', 'brown': '#a52a2a',
    'coral': '#ff7f50', 'salmon': '#fa8072', 'gold': '#ffd700', 'indigo': '#4b0082',
    'violet': '#ee82ee', 'tan': '#d2b48c', 'cyan': '#00ffff', 'magenta': '#ff00ff',
    'khaki': '#f0e68c', 'crimson': '#dc143c', 'transparent': None,
}

AMBIGUOUS_LINK_PATTERNS = [
    r'^click\s+here$', r'^read\s+more$', r'^more$', r'^here$', r'^link$',
    r'^learn\s+more$', r'^go$', r'^click$', r'^details$', r'^info$',
    r'^continue$', r'^submit$', r'^download$', r'^view\s+more$',
    r'^see\s+more$', r'^more\s+info$', r'^more\s+details$', r'^back$',
]

FORM_INPUT_TYPES = {'text', 'email', 'password', 'tel', 'url', 'search', 'number',
                    'date', 'time', 'datetime-local', 'month', 'week', 'color', 'file'}

AUTOCOMPLETE_MAP = {
    'name': 'name', 'first_name': 'given-name', 'last_name': 'family-name',
    'first-name': 'given-name', 'last-name': 'family-name',
    'email': 'email', 'phone': 'tel', 'telephone': 'tel',
    'city': 'address-level2', 'state': 'address-level1',
    'zip': 'postal-code', 'zipcode': 'postal-code', 'postal': 'postal-code',
    'country': 'country', 'company': 'organization', 'organization': 'organization',
    'address': 'street-address', 'address1': 'street-address',
    'username': 'username', 'password': 'current-password',
    'new-password': 'new-password', 'confirm-password': 'new-password',
    'url': 'url', 'website': 'url',
}

# Page type patterns (reuse from AEO toolkit)
PAGE_TYPE_PATTERNS = {
    "product": [
        r"/(?:product|item|sku)/[^/]+$",
        r"/(?:skills?|tools?|plugins?|extensions?|apps?)/[^/]+$",
        r"/(?:courses?|lessons?|tutorials?)/[^/]+$",
    ],
    "category": [
        r"/(?:categor|tag|topic)s?(/[^/]+)?/?$",
        r"/(?:skills?|tools?|products?|services?|courses?|blog)s?/?$",
        r"/(?:docs?|learn|guides?|help)s?/?$",
    ],
    "content": [
        r"/(?:blog|article|post|news|story|press)s?/[^/]+$",
        r"/(?:docs?|guide|tutorial|how-to|about|faq)s?/[^/]+$",
        r"/\d{4}/\d{2}/",
    ],
}

SKIP_EXTENSIONS = re.compile(
    r"\.(jpg|jpeg|png|gif|svg|ico|webp|pdf|zip|gz|css|js|woff|woff2|ttf|eot|mp[34]|avi|mov)(\?|$)",
    re.I,
)


# ─── Contrast Calculation ────────────────────────────────────────────────────

def hex_to_rgb(hex_color):
    """Convert hex color to (R, G, B) tuple (0-255)."""
    h = hex_color.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    try:
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    except ValueError:
        return None


def srgb_to_linear(c):
    """Convert sRGB component (0-1) to linear."""
    if c <= 0.03928:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb):
    """Calculate WCAG relative luminance from (R, G, B) tuple (0-255)."""
    if rgb is None:
        return None
    r, g, b = [c / 255.0 for c in rgb]
    return 0.2126 * srgb_to_linear(r) + 0.7152 * srgb_to_linear(g) + 0.0722 * srgb_to_linear(b)


def contrast_ratio(color1_rgb, color2_rgb):
    """Calculate WCAG contrast ratio between two RGB tuples."""
    l1 = relative_luminance(color1_rgb)
    l2 = relative_luminance(color2_rgb)
    if l1 is None or l2 is None:
        return None
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


def parse_color(color_str):
    """Parse a CSS color string to RGB tuple. Returns None if unparseable."""
    if not color_str:
        return None
    color_str = color_str.strip().lower()
    # Hex
    m = HEX_COLOR_RE.match(color_str)
    if m:
        return hex_to_rgb(m.group())
    # RGB/RGBA
    m = RGB_COLOR_RE.match(color_str)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = RGBA_COLOR_RE.match(color_str)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    # Named color
    if color_str in CSS_COLORS:
        hex_val = CSS_COLORS[color_str]
        if hex_val:
            return hex_to_rgb(hex_val)
    return None


def extract_colors_from_css(css_text):
    """Extract color/background-color pairs from CSS text."""
    colors = []
    for m in re.finditer(r'(?:color|background-color|background)\s*:\s*([^;}{]+)', css_text, re.I):
        val = m.group(1).strip()
        rgb = parse_color(val)
        if rgb:
            colors.append({'property': m.group(0).split(':')[0].strip(), 'value': val, 'rgb': rgb})
    return colors


def get_text_color(element_attrs, inline_styles):
    """Get text color from element attributes and inline styles."""
    style = element_attrs.get('style', '') + ' ' + inline_styles
    m = re.search(r'color\s*:\s*([^;]+)', style, re.I)
    if m:
        return parse_color(m.group(1))
    return None


def get_bg_color(element_attrs, inline_styles):
    """Get background color from element attributes and inline styles."""
    style = element_attrs.get('style', '') + ' ' + inline_styles
    # Check background-color first
    m = re.search(r'background-color\s*:\s*([^;]+)', style, re.I)
    if m:
        return parse_color(m.group(1))
    # Then shorthand background (only if it's a color, not image/gradient)
    m = re.search(r'background\s*:\s*([^;]+)', style, re.I)
    if m:
        val = m.group(1).strip()
        if not re.search(r'url|gradient|image', val, re.I):
            return parse_color(val)
    return None


def is_large_text(style_str):
    """Determine if text is 'large' per WCAG (>= 18pt or >= 14pt bold)."""
    is_bold = False
    font_size_px = None

    m = FONT_WEIGHT_RE.search(style_str)
    if m:
        w = m.group(1)
        is_bold = w.lower() in ('bold', 'bolder') or (w.isdigit() and int(w) >= 700)

    m = FONT_SIZE_PX_RE.search(style_str)
    if m:
        font_size_px = float(m.group(1))
    else:
        m = FONT_SIZE_PT_RE.search(style_str)
        if m:
            font_size_px = float(m.group(1)) * 1.333  # pt to px approximation

    if font_size_px is None:
        return False, False  # (is_large, detected)
    return (font_size_px >= LARGE_TEXT_PX or (font_size_px >= LARGE_TEXT_BOLD_PX and is_bold)), True


# ─── WCAG Checks ─────────────────────────────────────────────────────────────

class WCAGCheck:
    """Represents a single WCAG finding."""

    def __init__(self, criterion, level, title, severity, element, detail, fix_hint=""):
        self.criterion = criterion
        self.level = level
        self.title = title
        self.severity = severity  # critical, high, medium, low
        self.element = element    # tag + attributes snippet
        self.detail = detail
        self.fix_hint = fix_hint
        self.page_url = ""

    def to_dict(self):
        return {
            "criterion": self.criterion,
            "level": self.level,
            "title": self.title,
            "severity": self.severity,
            "element": self.element,
            "detail": self.detail,
            "fix_hint": self.fix_hint,
            "page_url": self.page_url,
        }


# ─── HTML Parser ─────────────────────────────────────────────────────────────

class A11YParser(HTMLParser):
    """Parse HTML and collect accessibility-relevant data."""

    def __init__(self, url=""):
        super().__init__()
        self.url = url

        # Page-level
        self.title = ""
        self.lang = ""
        self.has_skip_nav = False
        self.headings = []  # [(level, text, attrs), ...]
        self.links = []     # [(href, text, attrs), ...]
        self.images = []    # [(src, alt, attrs), ...]
        self.forms = []     # list of form data
        self.inputs = []    # [(tag, type, name, id, label_id, attrs), ...]
        self.tables = []    # list of table data
        self.aria_elements = []  # elements with ARIA attributes
        self.duplicate_ids = []  # [(id, count), ...]
        self.style_blocks = []   # CSS from <style> tags
        self.inline_styles = {}  # element id -> inline style string

        # Internal tracking
        self._id_counts = defaultdict(int)
        self._current_form = None
        self._current_label_for = None
        self._in_head = False
        self._in_style = False
        self._style_content = ""
        self._in_title = False
        self._title_text = ""

    def handle_starttag(self, tag, attrs):
        t = tag.lower()
        ad = {k.lower(): (v or "") for k, v in attrs}

        if t == "html":
            self.lang = ad.get("lang", "")
        elif t == "head":
            self._in_head = True
        elif t == "title" and self._in_head:
            self._in_title = True
        elif t == "style" and self._in_head:
            self._in_style = True
            self._style_content = ""
        elif t == "body":
            self._in_head = False
        elif t == "a":
            href = ad.get("href", "")
            self.links.append((href, "", ad))
        elif t == "img":
            alt = ad.get("alt", None)
            src = ad.get("src", "")
            self.images.append((src, alt, ad))
        elif t == "svg":
            aria_label = ad.get("aria-label", "")
            role = ad.get("role", "")
            title = ad.get("title", "")
            if not aria_label and not role and not title:
                self.aria_elements.append(("svg", "missing-accessible-name", ad))
        elif t == "input":
            input_type = ad.get("type", "text").lower()
            name = ad.get("name", "")
            eid = ad.get("id", "")
            autocomplete = ad.get("autocomplete", "")
            label_id = self._current_label_for
            self._current_label_for = None
            self.inputs.append((t, input_type, name, eid, label_id, autocomplete, ad))
        elif t == "select":
            eid = ad.get("id", "")
            name = ad.get("name", "")
            autocomplete = ad.get("autocomplete", "")
            label_id = self._current_label_for
            self._current_label_for = None
            self.inputs.append((t, "select", name, eid, label_id, autocomplete, ad))
        elif t == "textarea":
            eid = ad.get("id", "")
            name = ad.get("name", "")
            autocomplete = ad.get("autocomplete", "")
            label_id = self._current_label_for
            self._current_label_for = None
            self.inputs.append((t, "textarea", name, eid, label_id, autocomplete, ad))
        elif t == "label":
            self._current_label_for = ad.get("for", "")
        elif t == "form":
            self._current_form = {"action": ad.get("action", ""), "method": ad.get("method", ""), "inputs": []}
        elif t == "table":
            self.tables.append({"headers": [], "rows": [], "attrs": ad})
        elif t == "th":
            if self.tables:
                self.tables[-1]["headers"].append(ad)
        elif t in ("nav",):
            if "skip" in (ad.get("class", "") + " " + ad.get("id", "")).lower():
                self.has_skip_nav = True
        elif t == "a":
            if "skip" in (ad.get("class", "") + " " + ad.get("id", "")).lower():
                self.has_skip_nav = True

        # Track IDs for duplicate detection
        eid = ad.get("id", "")
        if eid:
            self._id_counts[eid] += 1

        # Track ARIA
        aria_attrs = [k for k in ad if k.startswith("aria-")]
        if aria_attrs:
            role = ad.get("role", "")
            self.aria_elements.append((t, role, ad))

        # Track inline styles
        if "style" in ad:
            self.inline_styles[eid] = ad["style"]

    def handle_endtag(self, tag):
        t = tag.lower()
        if t == "head":
            self._in_head = False
        elif t == "title":
            self._in_title = False
        elif t == "style":
            self._in_style = False
            self.style_blocks.append(self._style_content)

    def handle_data(self, data):
        if self._in_title:
            self._title_text += data
        if self.links and not self.links[-1][1]:
            self.links[-1] = (self.links[-1][0], data, self.links[-1][2])

    def handle_comment(self, data):
        pass

    def finalize(self):
        self.title = self._title_text.strip()
        # Deduplicate IDs
        for eid, count in self._id_counts.items():
            if count > 1:
                self.duplicate_ids.append((eid, count))


# ─── Check Runner ────────────────────────────────────────────────────────────

def run_checks(html_text, url="", css_text=""):
    """Run all automated checks on parsed HTML. Returns list of WCAGCheck."""
    parser = A11YParser(url)
    try:
        parser.feed(html_text)
    except Exception:
        pass
    parser.finalize()

    checks = []

    # ── 3.1.1 Language of Page (A) ──
    if not parser.lang:
        checks.append(WCAGCheck(
            "3.1.1", "A", "Missing language attribute",
            "high", "<html>", "No lang attribute on <html> element. Screen readers cannot determine the page language.",
            'Add lang attribute: <html lang="en">'
        ))

    # ── 2.4.2 Page Titled (A) ──
    if not parser.title:
        checks.append(WCAGCheck(
            "2.4.2", "A", "Missing page title",
            "high", "<title>", "No <title> element found or title is empty.",
            'Add a descriptive title: <title>Page Description — Site Name</title>'
        ))

    # ── 1.1.1 Non-text Content (A) ──
    for src, alt, attrs in parser.images:
        if alt is None:
            # Check if it's decorative (hidden, role=presentation, empty alt via aria)
            role = attrs.get("role", "")
            aria_hidden = attrs.get("aria-hidden", "")
            if role == "presentation" or role == "none" or aria_hidden == "true":
                continue  # Decorative, no alt needed
            checks.append(WCAGCheck(
                "1.1.1", "A", "Image missing alt text",
                "critical", f'<img src="{src[:60]}">', 
                "Image has no alt attribute. Screen readers cannot describe this image to users.",
                f'Add alt text: <img src="{src[:40]}..." alt="Description of image">'
            ))
        elif alt.strip() == "":
            # Empty alt — could be decorative or missing
            role = attrs.get("role", "")
            if role not in ("presentation", "none"):
                checks.append(WCAGCheck(
                    "1.1.1", "A", "Image has empty alt text",
                    "medium", f'<img src="{src[:60]}" alt="">',
                    "Image has alt=\"\". This marks the image as decorative. If the image conveys information, add descriptive alt text.",
                    'If decorative: role="presentation" | If informative: alt="Description"'
                ))

    # ── 1.3.1 Info and Relationships (A) ──

    # Heading hierarchy
    if parser.headings:
        prev_level = 0
        h1_count = 0
        for level, text, attrs in parser.headings:
            h1_count += (1 if level == 1 else 0)
            if level > prev_level + 1 and prev_level > 0:
                checks.append(WCAGCheck(
                    "1.3.1", "A", "Skipped heading level",
                    "medium", f'<h{level}>{text[:40]}</h{level}>',
                    f"Heading level skipped from H{prev_level} to H{level}. Screen reader users expect sequential heading hierarchy.",
                    f"Change H{level} to H{prev_level + 1} or add missing H{prev_level + 1}"
                ))
            prev_level = level
        if h1_count == 0:
            checks.append(WCAGCheck(
                "1.3.1", "A", "Missing H1 heading",
                "high", "<h1>", "No H1 heading found. The H1 describes the main purpose of the page and is the first heading screen reader users encounter.",
                "Add a single H1 heading that describes the page's main topic."
            ))
        elif h1_count > 1:
            checks.append(WCAGCheck(
                "1.3.1", "A", "Multiple H1 headings",
                "medium", "<h1>", f"Found {h1_count} H1 headings. Best practice is a single H1 per page.",
                "Keep one H1 as the main page heading. Use H2-H6 for subsections."
            ))

    # Table headers
    for table in parser.tables:
        if not table["headers"]:
            checks.append(WCAGCheck(
                "1.3.1", "A", "Data table missing header cells",
                "high", "<table>", "Table has no <th> elements. Screen reader users cannot understand the relationship between headers and data cells.",
                "Add <th> elements for row and/or column headers: <th>Header</th>"
            ))

    # ── 3.3.2 Labels (A) / 1.3.1 Info and Relationships ──
    for tag, itype, name, eid, label_id, autocomplete, attrs in parser.inputs:
        if itype in ("hidden", "submit", "reset", "button", "image"):
            continue
        has_label = bool(label_id)
        has_aria = bool(attrs.get("aria-label") or attrs.get("aria-labelledby"))
        has_placeholder = bool(attrs.get("placeholder", "").strip())
        has_title = bool(attrs.get("title", "").strip())

        if not has_label and not has_aria:
            checks.append(WCAGCheck(
                "3.3.2", "A", "Form input missing label",
                "high", f'<{tag} type="{itype}" name="{name}">',
                f"Form input '{name or itype}' has no associated <label> or aria-label. Screen reader users cannot identify the purpose of this field.",
                f'Add a label: <label for="{eid}">Label text</label> or aria-label="Purpose"'
            ))
        elif not has_label and has_aria:
            checks.append(WCAGCheck(
                "3.3.2", "A", "Form input using aria-label instead of visible label",
                "low", f'<{tag} type="{itype}" name="{name}">',
                f"Input '{name or itype}' uses aria-label but has no visible <label>. Visible labels benefit all users, not just screen reader users.",
                f'Add a visible label: <label for="{eid}">Label text</label>'
            ))

    # Autocomplete
    for tag, itype, name, eid, label_id, autocomplete, attrs in parser.inputs:
        if itype in ("hidden", "submit", "reset", "button", "image"):
            continue
        if not autocomplete and name:
            # Check if name matches known autocomplete values
            normalized = name.lower().replace('_', '-').replace(' ', '-')
            if normalized in AUTOCOMPLETE_MAP:
                checks.append(WCAGCheck(
                    "3.3.2", "A", "Missing autocomplete attribute",
                    "low", f'<{tag} name="{name}">',
                    f"Input '{name}' could benefit from autocomplete=\"{AUTOCOMPLETE_MAP[normalized]}\" for browser autofill support.",
                    f'Add autocomplete="{AUTOCOMPLETE_MAP[normalized]}" to the input element.'
                ))

    # ── 2.1.1 Keyboard / 2.4.1 Bypass Blocks (A) ──
    if not parser.has_skip_nav:
        checks.append(WCAGCheck(
            "2.4.1", "A", "Missing skip navigation link",
            "medium", "<a>", "No skip navigation link found. Keyboard users must tab through all navigation items to reach the main content.",
            'Add: <a href="#main" class="sr-only focus:not-sr-only">Skip to main content</a>'
        ))

    # ── 2.4.4 Link Purpose (A) ──
    for href, text, attrs in parser.links:
        if not text or not text.strip():
            if attrs.get("aria-label") or attrs.get("aria-labelledby"):
                continue
            checks.append(WCAGCheck(
                "2.4.4", "A", "Empty link with no accessible name",
                "high", f'<a href="{href[:60]}">',
                "Link has no text content and no aria-label. Screen reader users cannot determine where this link goes.",
                f'Add text or aria-label: <a href="{href[:40]}..." aria-label="Description">'
            ))
        else:
            stripped = text.strip().lower()
            for pattern in AMBIGUOUS_LINK_PATTERNS:
                if re.match(pattern, stripped, re.I):
                    checks.append(WCAGCheck(
                        "2.4.4", "A", "Ambiguous link text",
                        "medium", f'<a href="{href[:60]}">{text[:30]}</a>',
                        f'Link text "{text.strip()}" does not describe the link destination. Screen reader users navigating by link cannot determine the purpose.',
                        f'Use descriptive text: <a href="...">Read about [specific topic]</a>'
                    ))
                    break

    # ── 4.1.2 Name, Role, Value (A) ──

    # Duplicate IDs
    for eid, count in parser.duplicate_ids:
        checks.append(WCAGCheck(
            "4.1.2", "A", f'Duplicate ID: "{eid}"',
            "high", f'id="{eid}"', f'ID "{eid}" appears {count} times. Duplicate IDs break label associations and ARIA references.',
            f'Make each ID unique: change "{eid}" to "{eid}-2" on subsequent elements.'
        ))

    # ARIA on interactive elements
    interactive_tags = {'a', 'button', 'input', 'select', 'textarea', 'summary', 'details'}
    for tag, role, attrs in parser.aria_elements:
        if tag in interactive_tags:
            continue
        if tag == 'svg':
            continue  # Already handled above
        aria_label = attrs.get("aria-label", "")
        aria_labelledby = attrs.get("aria-labelledby", "")
        role_val = attrs.get("role", "")
        if not role_val and not aria_label and not aria_labelledby:
            # Only flag custom/div elements with ARIA but missing role/label
            pass
        if role_val and not aria_label and not aria_labelledby:
            checks.append(WCAGCheck(
                "4.1.2", "A", f"Element with role but no accessible name",
                "medium", f'<{tag} role="{role_val}">',
                f'Element has role="{role_val}" but no aria-label or aria-labelledby. Assistive technologies cannot identify this element.',
                f'Add aria-label="Description" to the element.'
            ))

    # ── 1.4.3 Contrast (Minimum) (AA) ──
    # Check elements with inline styles for contrast
    for eid, style_str in parser.inline_styles.items():
        fg = get_text_color({'style': style_str}, "")
        bg = get_bg_color({'style': style_str}, "")
        if fg and bg:
            ratio = contrast_ratio(fg, bg)
            if ratio is not None:
                is_large, detected = is_large_text(style_str)
                threshold = CONTRAST_AA_LARGE if is_large else CONTRAST_AA_NORMAL
                if ratio < threshold:
                    level = "AA Large Text" if is_large else "AA Normal Text"
                    checks.append(WCAGCheck(
                        "1.4.3", "AA", f"Insufficient color contrast ({level})",
                        "critical" if ratio < 3.0 else "high",
                        f'element#{eid} style="{style_str[:50]}"',
                        f"Contrast ratio is {ratio:.2f}:1, minimum required is {threshold}:1 for {level.lower()}.",
                        f"Increase text color contrast. Current: {ratio:.2f}:1, need: {threshold}:1+"
                    ))

    # ── 2.4.6 Headings and Labels (AA) ──
    # Check for pages with substantial content but no headings
    text_len = len(html_text)
    if text_len > 5000 and not parser.headings:
        checks.append(WCAGCheck(
            "2.4.6", "AA", "No headings found on content page",
            "high", "<h1>", "Page has substantial content but no heading elements. Headings help screen reader users navigate and understand page structure.",
            "Add headings to organize content: <h1>Main topic</h1>, <h2>Section</h2>, etc."
        ))

    # Set page URL on all checks
    for check in checks:
        check.page_url = url

    return checks, parser


# ─── Scoring ─────────────────────────────────────────────────────────────────

def calculate_score(checks):
    """Calculate a 0-100 accessibility score.
    
    Weighted by severity. Critical/High findings hurt the most.
    Cap per criterion to avoid one issue type dominating.
    """
    severity_weights = {"critical": 8, "high": 4, "medium": 2, "low": 1}
    
    # Cap findings per criterion
    criterion_counts = defaultdict(int)
    for c in checks:
        criterion_counts[c.criterion] += 1
    
    MAX_PER_CRITERION = 5
    capped_total = 0
    for c in checks:
        count = criterion_counts.get(c.criterion, 0)
        if count <= MAX_PER_CRITERION:
            capped_total += severity_weights.get(c.severity, 1)
    
    score = max(0, 100 - capped_total)
    return round(score)


def get_grade(score):
    if score >= 95: return "A+"
    if score >= 90: return "A"
    if score >= 80: return "B"
    if score >= 70: return "C"
    if score >= 60: return "D"
    return "F"


# ─── HTTP Fetch ──────────────────────────────────────────────────────────────

def fetch(url, timeout=15, max_bytes=524288, verify_ssl=True):
    try:
        ctx = None
        if not verify_ssl:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(url, headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,text/plain,*/*",
        })
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            body = resp.read(max_bytes)
            return resp.status, body.decode("utf-8", errors="replace"), None
    except urllib.error.HTTPError as e:
        try:
            body = e.read(max_bytes).decode("utf-8", errors="replace")
        except Exception:
            body = ""
        return e.code, body, None
    except Exception as e:
        return 0, "", str(e)


# ─── Page Type ───────────────────────────────────────────────────────────────

def classify_page_type(url):
    from urllib.parse import urlparse
    path = urlparse(url).path.rstrip("/")
    if path in ("", "/"):
        return "homepage"
    for ptype, patterns in PAGE_TYPE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, path, re.I):
                return ptype
    return "other"


def select_page_type_samples(sitemap_pages):
    typed = defaultdict(list)
    for page in sitemap_pages:
        ptype = classify_page_type(page["url"])
        if ptype != "homepage":
            typed[ptype].append(page)
    samples = []
    for ptype, pages in typed.items():
        pages.sort(key=lambda p: (p["priority"] is not None, p["priority"] or 0), reverse=True)
        samples.extend(pages[:1])
    return samples


# ─── Sitemap ─────────────────────────────────────────────────────────────────

def parse_sitemap(text):
    urls = []
    try:
        clean = re.sub(r'\sxmlns[^"]*"[^"]*"', '', text, flags=re.DOTALL)
        root = ET.fromstring(clean)
        for url_el in root.iter("url"):
            loc, pri, mod = "", None, None
            for child in url_el:
                if child.tag == "loc" and child.text: loc = child.text.strip()
                elif child.tag == "priority" and child.text:
                    try: pri = float(child.text)
                    except ValueError: pass
                elif child.tag == "lastmod" and child.text: mod = child.text.strip()
            if loc:
                urls.append({"url": loc, "priority": pri, "lastmod": mod})
    except ET.ParseError:
        for m in re.finditer(r"<loc>\s*(.*?)\s*</loc>", text):
            urls.append({"url": m.group(1).strip(), "priority": None, "lastmod": None})
    urls.sort(key=lambda u: (u["priority"] is not None, u["priority"] or 0), reverse=True)
    return urls


# ─── Main ────────────────────────────────────────────────────────────────────

def audit(url, max_pages=10, timeout=15, max_bytes=524288, verify_ssl=True, page_type_mode=False):
    """Run full accessibility audit."""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    result = {
        "url": url,
        "base_url": base,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "homepage": None,
        "additional_pages": [],
        "aggregate": {},
        "score": 0,
        "grade": "",
    }

    all_checks = []

    # 1. Homepage
    st, html, err = fetch(url, timeout, max_bytes, verify_ssl)
    if err and st == 0:
        result["homepage"] = {"url": url, "status": 0, "error": err}
        result["errors"] = [err]
        return result
    if st != 200 or not html:
        result["homepage"] = {"url": url, "status": st, "error": "Not HTML or non-200"}
        return result

    checks, parser = run_checks(html, url)
    result["homepage"] = {
        "url": url,
        "status": st,
        "title": parser.title,
        "lang": parser.lang,
        "has_skip_nav": parser.has_skip_nav,
        "heading_count": len(parser.headings),
        "image_count": len(parser.images),
        "input_count": len(parser.inputs),
        "link_count": len(parser.links),
        "table_count": len(parser.tables),
        "duplicate_id_count": len(parser.duplicate_ids),
        "aria_element_count": len(parser.aria_elements),
        "style_block_count": len(parser.style_blocks),
        "page_type": "homepage",
    }
    all_checks.extend(checks)

    # 2. Sitemap
    sm_url = f"{base}/sitemap.xml"
    st, sm_html, _ = fetch(sm_url, timeout, max_bytes, verify_ssl)
    sitemap_pages = []
    if st == 200 and sm_html:
        sitemap_pages = parse_sitemap(sm_html)

    # Filter
    crawl_urls = [
        p for p in sitemap_pages
        if p["url"] not in (url, url + "/")
        and not SKIP_EXTENSIONS.search(p["url"])
        and p["url"].startswith("http")
    ]

    if page_type_mode and crawl_urls:
        samples = select_page_type_samples(crawl_urls)
        sample_set = {s["url"] for s in samples}
        crawl_urls = [p for p in crawl_urls if p["url"] in sample_set]

    if max_pages > 0:
        crawl_urls = crawl_urls[:max_pages]

    # 3. Additional pages
    for page_info in crawl_urls:
        pu = page_info["url"]
        st, html, err = fetch(pu, timeout, max_bytes, verify_ssl)
        if err and st == 0:
            result["additional_pages"].append({"url": pu, "status": 0, "error": err})
            continue
        if st != 200 or not html:
            result["additional_pages"].append({"url": pu, "status": st, "is_html": False})
            continue
        checks, parser = run_checks(html, pu)
        pr = {
            "url": pu, "status": st,
            "title": parser.title, "lang": parser.lang,
            "has_skip_nav": parser.has_skip_nav,
            "heading_count": len(parser.headings),
            "image_count": len(parser.images),
            "input_count": len(parser.inputs),
            "link_count": len(parser.links),
            "page_type": classify_page_type(pu),
        }
        result["additional_pages"].append(pr)
        all_checks.extend(checks)

    # 4. Aggregate
    severity_counts = defaultdict(int)
    criterion_counts = defaultdict(int)
    for c in all_checks:
        severity_counts[c.severity] += 1
        criterion_counts[c.criterion] += 1

    result["aggregate"] = {
        "pages_crawled": 1 + len([p for p in result["additional_pages"] if p.get("status") == 200]),
        "total_findings": len(all_checks),
        "by_severity": dict(severity_counts),
        "by_criterion": {k: v for k, v in sorted(criterion_counts.items())},
        "criteria_checked": list(set(c.criterion for c in all_checks)),
    }

    # 5. Score
    score = calculate_score(all_checks)
    result["score"] = score
    result["grade"] = get_grade(score)

    # 6. Findings (all checks as dicts)
    result["findings"] = [c.to_dict() for c in all_checks]

    return result


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="A11Y Audit — WCAG 2.1 AA accessibility audit")
    ap.add_argument("url", nargs="?", help="URL to audit")
    ap.add_argument("--max-pages", type=int, default=10, help="Max sitemap pages (default: 10, 0 = all)")
    ap.add_argument("--page-types", action="store_true", help="Sample one per page type")
    ap.add_argument("--timeout", type=int, default=15, help="Request timeout (default: 15)")
    ap.add_argument("--max-bytes", type=int, default=524288, help="Max response size (default: 512KB)")
    ap.add_argument("--no-ssl-verify", action="store_true", help="Skip SSL verification")
    args = ap.parse_args()

    def validate_url(u):
        u = u.strip()
        if not re.match(r"^https?://", u, re.I): return None
        if any(c in u for c in ';|&$`(){}<>\\n'): return None
        return u

    if not args.url:
        print(json.dumps({"error": "Provide a URL"}))
        sys.exit(1)

    url = validate_url(args.url)
    if not url:
        print(json.dumps({"error": "Invalid URL"}))
        sys.exit(1)

    result = audit(
        url,
        max_pages=args.max_pages,
        timeout=args.timeout,
        max_bytes=args.max_bytes,
        verify_ssl=not args.no_ssl_verify,
        page_type_mode=args.page_types,
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
