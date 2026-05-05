# SEO Audit Report — calcclear.com

**Date:** May 4, 2026  
**Auditor:** Automated SEO Audit  
**Pages Audited:** Home page + 6 calculator pages  
**Severity Ratings:** CRITICAL > HIGH > MEDIUM > LOW

---

## Executive Summary

| Page | Title | Meta Desc | Canonical | JSON-LD | OG Tags | Robots |
|------|-------|-----------|-----------|---------|---------|--------|
| Home `/` | ✅ | ✅ | ✅ | ❌ Missing | ✅ | ❌ Missing |
| Coast FIRE | ✅ | ✅ | ✅ | ✅ | ⚠️ Misplaced | ❌ Missing |
| Cash Flow | ✅ | ✅ | ✅ | ✅ | ⚠️ Duplicated | ❌ Missing |
| HELOC | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ Missing |
| Land Loan | ✅ | ✅ | ✅ | ✅ | ⚠️ Duplicated | ❌ Missing |
| Margin vs Markup | ✅ | ✅ | ✅ | ✅ | ⚠️ Duplicated | ❌ Missing |
| Probate | ✅ | ✅ | ✅ | ✅ | ⚠️ Duplicated | ❌ Missing |

---

## CRITICAL Issues

### 1. Coast FIRE Calculator — Malformed HTML Structure
**Severity:** CRITICAL  
**File:** `coast-fire-calculator/index.html`

The `<title>`, JSON-LD schema, and Open Graph `<meta>` tags are placed **AFTER** the closing `</html>` tag. These are therefore **not in the document `<head>`** where they belong.

```html
<!-- BROKEN STRUCTURE -->
</head>
<body>...page content...</body>
</html>
<meta property="og:title" content="Coast FIRE Calculator – CalcClear"/>
<script type="application/ld+json">{...}</script>
<!-- ↑ THESE ARE OUTSIDE </html> — NOT VALID HTML -->
```

**Fix:** Move all `<head>` elements (title, meta, script[type=application/ld+json], link[rel=canonical]) to before `</head>`.

---

### 2. Duplicate/Misplaced Meta Tags — Cash Flow, Land Loan, Margin vs Markup, Probate
**Severity:** HIGH  
**Files:** `cash-flow-calculator/index.html`, `land-loan-calculator/index.html`, `margin-vs-markup-calculator/index.html`, `probate-calculator/index.html`

These pages have **duplicate Open Graph and Twitter Card meta tags** — the same tags appear twice in the HTML source.

Additionally, on `cash-flow-calculator/index.html`:
```html
<meta property="og:title" content="Cash Flow Calculator – CalcClear"/>  <!-- in <head> -->
<!-- then LATER in <body>: -->
<meta property="og:title" content="Cash Flow Calculator – CalcClear"/>  <!-- DUPLICATE -->
```

**Fix:** Remove duplicate meta tags. Keep only one set in `<head>`.

---

### 3. Missing Robots Meta Tag — All Pages
**Severity:** HIGH  
**Affected:** ALL 7 pages (home + 6 calculators)

No `<meta name="robots">` tag is present on any page. Without explicit index/follow directives, crawlers use defaults (usually index,follow). While this isn't harmful, **explicit is better than implicit** for SEO control.

**Fix:** Add to all pages:
```html
<meta name="robots" content="index, follow"/>
```

---

## HIGH Issues

### 4. Missing JSON-LD Schema — Home Page
**Severity:** HIGH  
**File:** `index.html`

The home page has **no Schema.org JSON-LD** structured data. As the main entry point, it should have either:
- `WebSite` schema with `searchAction`, OR
- `Organization` schema, OR  
- At minimum, a link to the site via `WebApplication` on calculator pages

**Fix:** Add JSON-LD to home page:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "CalcClear.com",
  "url": "https://calcclear.com/",
  "description": "Free online financial calculators for Coast FIRE, cash flow, HELOC, land loans, margin vs markup, and probate.",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  }
}
</script>
```

---

### 5. Render-Blocking CSS (@import) — All Pages
**Severity:** HIGH  
**Impact:** Page load speed  
**Affected:** ALL pages

```html
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;510;590&display=swap');
    /* ↑ RENDER-BLOCKING — browser can't render until font loads */
</style>
```

The `@import` inside a `<style>` tag is synchronous and blocks rendering. Combined with no `preconnect` hints for Google Fonts, this adds latency.

**Fix:** Replace with non-blocking approach:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;510;590&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;510;590&display=swap"></noscript>
```

---

### 6. External Links to Same-Owner Domain (coastfirewhen.com) — All Calculator Pages
**Severity:** MEDIUM  
**Affected:** All calculator pages

Footer links point to `https://coastfirewhen.com/privacy-policy.html` and `https://coastfirewhen.com/terms.html`. Since this is the same owner/brand, these should likely be **internal links** (relative paths or same-domain). Currently they create a cross-domain link for link equity leakage.

Also, links to `https://coastfirewhen.com/*` in content cards (e.g., "Coast FIRE Guide →", "Compound Interest →") — these are outbound links to an affiliated site.

**Fix:** 
1. Change footer privacy/terms links to relative paths or same-domain URLs.
2. For content cards linking to coastfirewhen.com, consider adding `rel="nofollow"` if not a strategic link, or ensure they're intentional outbound links to a related site you control.

---

## MEDIUM Issues

### 7. Missing `preconnect` / `dns-prefetch` Hints
**Severity:** MEDIUM  
**Impact:** Page load speed  
**Affected:** ALL pages

No `preconnect` hints for external resources:
- `https://fonts.googleapis.com` (Google Fonts)
- `https://pagead2.googlesyndication.com` (AdSense)
- `https://googlesyndication.com` (AdSense)

**Fix:** Add to `<head>`:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://pagead2.googlesyndication.com">
<link rel="dns-prefetch" href="https://www.googlesyndication.com">
```

---

### 8. Ad Slot Placeholder `data-ad-slot="XXXXXXXXXX"` — All Calculator Pages
**Severity:** MEDIUM  
**Affected:** All 6 calculator pages

```html
<ins class="adsbygoogle" data-ad-client="ca-pub-1342579174060580" data-ad-format="auto" data-ad-slot="XXXXXXXXXX" ...>
```

The `data-ad-slot="XXXXXXXXXX"` is a placeholder. Real ad slots should have actual slot IDs. This won't cause SEO issues but means **no actual ads are being served** on these slots.

**Fix:** Replace `XXXXXXXXXX` with actual AdSense ad slot IDs from your AdSense dashboard.

---

### 9. Missing `og:image` Open Graph Tag — All Pages
**Severity:** MEDIUM  
**Affected:** ALL pages

No `og:image` tag is present. Social sharing will show no preview image.

**Fix:** Add to `<head>` of all pages:
```html
<meta property="og:image" content="https://calcclear.com/og-image.png"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
```

---

### 10. Sitemap Priority Inconsistencies
**Severity:** LOW  
**File:** `sitemap.xml`

```xml
<url>
  <loc>https://calcclear.com/coast-fire-calculator/</loc>
  <priority>1.0</priority>  <!-- Same as home page? -->
  <changefreq>weekly</changefreq>
</url>
<url>
  <loc>https://calcclear.com/cash-flow-calculator/</loc>
  <priority>0.9</priority>  <!-- Slightly lower -->
  <changefreq>weekly</changefreq>
</url>
```

Coast FIRE gets `1.0` (same as home) but Cash Flow gets `0.9`. If Coast FIRE is the flagship calculator, this may be intentional. However, the sitemap doesn't include all calculator pages with consistent priority logic.

**Fix:** Review priority assignments — if Coast FIRE isn't definitively more important than others, consider `0.9` for all calculator pages.

---

## LOW Issues

### 11. No Structured Navigation Links Between Calculators
**Severity:** LOW  
**Note:** Actually, prev/next navigation is present and working ✅

The footer navigation strip (`calc-nav-strip`) correctly links between calculators:
- Coast FIRE → Cash Flow (next)
- Cash Flow → Coast FIRE (prev), HELOC (next)
- HELOC → Cash Flow (prev), Land Loan (next)
- Land Loan → HELOC (prev), Margin vs Markup (next)
- Margin vs Markup → Land Loan (prev), Probate (next)
- Probate → Margin vs Markup (prev), (none next)

This is **working correctly** — no action needed.

---

### 12. No Images — No Alt Text Issues
**Severity:** INFO  
**Status:** ✅ PASS

None of the pages use `<img>` tags, so there are no missing `alt` attributes. This is fine for calculator pages — no images to audit.

---

### 13. URL Structure
**Severity:** INFO  
**Status:** ✅ PASS

URLs are clean and readable:
- `/coast-fire-calculator/`
- `/cash-flow-calculator/`
- `/heloc-calculator/`
- `/land-loan-calculator/`
- `/margin-vs-markup-calculator/`
- `/probate-calculator/`

No dynamic parameters, no trailing index.html, no ugly URL structures. ✅

---

### 14. robots.txt
**Severity:** INFO  
**Status:** ✅ PASS

```text
User-agent: *
Allow: /

Sitemap: https://calcclear.com/sitemap.xml
```

Clean, allows all crawlers, points to sitemap. ✅

---

### 15. Sitemap Completeness
**Severity:** INFO  
**Status:** ✅ PASS

All 7 pages are in sitemap.xml:
- `/` (home)
- `/coast-fire-calculator/`
- `/cash-flow-calculator/`
- `/heloc-calculator/`
- `/land-loan-calculator/`
- `/margin-vs-markup-calculator/`
- `/probate-calculator/`

✅ All pages accounted for.

---

### 16. Language Attribute
**Severity:** INFO  
**Status:** ✅ PASS

All pages have `<html lang="en">` ✅

---

### 17. Mobile Viewport
**Severity:** INFO  
**Status:** ✅ PASS

All pages have `<meta name="viewport" content="width=device-width, initial-scale=1.0">` ✅

---

## Per-Page Summary

### Home Page (`/`)
| Item | Status | Notes |
|------|--------|-------|
| Title | ✅ | "CalcClear.com — Free Online Financial Calculators" (60 chars) |
| Meta Description | ✅ | Good length, includes all calculator types |
| Canonical | ✅ | `https://calcclear.com/` |
| H1 | ✅ | "Free Online Calculators" |
| JSON-LD | ❌ | Missing — should add WebSite schema |
| OG Tags | ✅ | title/description/type present |
| Twitter Card | ✅ | summary card |
| Robots Meta | ❌ | Missing — add explicit `index,follow` |
| Images | N/A | No images |
| Internal Links | ✅ | All 6 calculators linked |

---

### Coast FIRE Calculator (`/coast-fire-calculator/`)
| Item | Status | Notes |
|------|--------|-------|
| Title | ✅ | "Coast FIRE Calculator – CalcClear" |
| Meta Description | ✅ | Keyword-rich, descriptive |
| Canonical | ✅ | Points to page URL |
| H1 | ✅ | "Coast FIRE Calculator" (exactly one) |
| H2s | ✅ | "How it works" |
| JSON-LD | ⚠️ | **Present but misplaced — outside `<head>`** |
| OG Tags | ⚠️ | **Misplaced — outside `<html>`** |
| Robots Meta | ❌ | Missing |
| Images | N/A | No images |
| Internal Links | ✅ | Working prev/next nav |

**CRITICAL FIX:** Move all `<head>` elements before `</head>`, not after `</html>`.

---

### Cash Flow Calculator (`/cash-flow-calculator/`)
| Item | Status | Notes |
|------|--------|-------|
| Title | ✅ | "Cash Flow Calculator – CalcClear" |
| Meta Description | ✅ | Good, unique to this page |
| Canonical | ✅ | Correct |
| H1 | ✅ | Exactly one |
| JSON-LD | ✅ | Valid WebApplication schema |
| OG Tags | ⚠️ | **Duplicated** — same tags appear twice |
| Robots Meta | ❌ | Missing |
| Internal Links | ✅ | Prev (Coast FIRE) / Next (HELOC) |

---

### HELOC Calculator (`/heloc-calculator/`)
| Item | Status | Notes |
|------|--------|-------|
| Title | ✅ | "HELOC Calculator – CalcClear" |
| Meta Description | ✅ | "Calculate HELOC payments..." |
| Canonical | ✅ | Correct |
| H1 | ✅ | Exactly one |
| JSON-LD | ✅ | Valid WebApplication |
| OG Tags | ✅ | Complete |
| Robots Meta | ❌ | Missing |

---

### Land Loan Calculator (`/land-loan-calculator/`)
| Item | Status | Notes |
|------|--------|-------|
| Title | ✅ | "Land Loan Calculator – CalcClear" |
| Meta Description | ✅ | Unique |
| Canonical | ✅ | Correct |
| H1 | ✅ | Exactly one |
| JSON-LD | ✅ | Valid |
| OG Tags | ⚠️ | **Duplicated** (appears twice in source) |
| Robots Meta | ❌ | Missing |

---

### Margin vs Markup Calculator (`/margin-vs-markup-calculator/`)
| Item | Status | Notes |
|------|--------|-------|
| Title | ✅ | "Margin vs Markup Calculator – CalcClear" |
| Meta Description | ✅ | Unique |
| Canonical | ✅ | Correct |
| H1 | ✅ | Exactly one |
| JSON-LD | ✅ | Valid |
| OG Tags | ⚠️ | **Duplicated** |
| Robots Meta | ❌ | Missing |

---

### Probate Calculator (`/probate-calculator/`)
| Item | Status | Notes |
|------|--------|-------|
| Title | ✅ | "Probate Calculator – CalcClear" |
| Meta Description | ✅ | Unique |
| Canonical | ✅ | Correct |
| H1 | ✅ | Exactly one |
| JSON-LD | ✅ | Valid |
| OG Tags | ⚠️ | **Duplicated** |
| Robots Meta | ❌ | Missing |

---

## Action Items (Priority Order)

### Immediate (Fix Today)
1. **[CRITICAL]** Fix malformed HTML in `coast-fire-calculator/index.html` — move meta/JSON-LD into `<head>`
2. **[HIGH]** Remove duplicate meta tags from Cash Flow, Land Loan, Margin vs Markup, Probate pages
3. **[HIGH]** Add `robots` meta tag to ALL pages: `<meta name="robots" content="index, follow"/>`

### Soon (This Week)
4. **[HIGH]** Add JSON-LD WebSite schema to home page
5. **[HIGH]** Fix render-blocking font loading (use `preconnect` + non-blocking stylesheet)
6. **[MEDIUM]** Add `og:image` to all pages (create an og-image.png first)
7. **[MEDIUM]** Replace `XXXXXXXXXX` ad slot placeholders with real AdSense slot IDs

### Eventually (Nice to Have)
8. **[MEDIUM]** Add `preconnect`/`dns-prefetch` hints for Google Fonts and AdSense
9. **[LOW]** Consider making coastfirewhen.com links internal or adding nofollow if appropriate
10. **[LOW]** Review sitemap priority values for consistency

---

## Positive Findings ✅

- **Clean URL structure** — readable, descriptive, no dynamic parameters
- **Consistent heading structure** — exactly one H1 per page
- **Proper canonical URLs** — all pages self-canonical
- **Valid JSON-LD** — WebApplication schema on all calculator pages
- **Complete Open Graph tags** — on most pages
- **Working internal navigation** — prev/next links between calculators
- **Good title tags** — unique, keyword-appropriate, proper length
- **Unique meta descriptions** — each page has its own
- **Fast infrastructure** — Cloudflare Pages with proper security headers
- **robots.txt and sitemap.xml** — accessible and well-formed
- **No render-blocking JavaScript** — AdSense uses `async`
- **No duplicate content** — all pages are unique

---

## Scorecard

| Category | Score | Notes |
|----------|-------|-------|
| On-Page SEO | 7/10 | Good titles/descriptions, missing robots meta, malformed HTML on 1 page |
| Technical SEO | 7/10 | Good canonical, URLs, sitemap; render-blocking CSS; missing preconnect |
| Performance | 6/10 | Font @import blocks render; no lazy loading hints needed (no images) |
| Social/Sharing | 6/10 | OG tags mostly present but missing og:image |
| Structured Data | 8/10 | JSON-LD present on calculators, missing on home |
| Security Headers | 10/10 | X-Content-Type-Options set in Cloudflare Pages _headers |

**Overall SEO Health: 7.3/10** — Solid foundation with fixable critical issues.
