#!/usr/bin/env python3
"""Apply comma formatting + AdSense slots to all calculator pages."""
import re, os, json

CALCCLEAR_DIR = '/Users/fred/calcclear-site'
COAST_DIR     = '/Users/fred/calculator-niche-research/coastfirewhen.com'

# JS helper injected at top of first script block
FMT_NUMS_JS = "\n  function fmtNums(v){return parseFloat((v||'0').replace(/,/g,''))||0;}\n"

# oninput attribute for dollar inputs (comma-format as user types)
ONINPUT = (
    "oninput=\"var v=this.value.replace(/[^0-9]/g,'');"
    "if(v||v==='0')this.value=Number(v).toLocaleString('en-US');\" "
    "onblur=\"if(this.value)this.value=Number(this.value.replace(/[^0-9]/g,'')).toLocaleString('en-US')\""
)

ADSENSE_SLOT_CSS = (
    ".ad-slot{background:rgba(255,255,255,0.02);"
    "border:1px dashed rgba(255,255,255,0.1);border-radius:8px;"
    "padding:20px;text-align:center;margin:24px 0;}"
    ".ad-slot p{font-size:12px;color:#62666d;text-transform:uppercase;"
    "letter-spacing:.05em;margin:0 0 10px;}"
)
ADSENSE_SLOT_HTML = (
    '<div class="ad-slot">'
    '<p>Advertisement</p>'
    '<ins class="adsbygoogle" style="display:block" '
    'data-ad-client="ca-pub-XXXXXXXXXX" data-ad-slot="XXXXXXXXXX" '
    'data-ad-format="auto" data-full-width-responsive="true"></ins>'
    '</div>'
)

def add_comma_formatting(html_path, dollar_field_ids):
    with open(html_path) as f:
        html = f.read()

    # 1. Inject fmtNums before first function in first <script> block
    m = re.search(r'(<script[^>]*>)(.*?)(</script>)', html, re.DOTALL)
    if m:
        otag, body, ctag = m.group(1), m.group(2), m.group(3)
        fn = re.search(r'\bfunction\s+\w+\s*\(', body)
        if fn:
            pos = fn.start()
            body = body[:pos] + FMT_NUMS_JS + body[pos:]
        html = html[:m.start()] + otag + body + ctag + html[m.end():]

    # 2. Swap dollar inputs: number -> text + add oninput/onblur
    for fid in dollar_field_ids:
        old = '<input type="number" id="{}"'.format(fid)
        new = '<input type="text" inputmode="numeric" pattern="[0-9,]*" id="{}" {}'.format(fid, ONINPUT)
        html = html.replace(old, new, 1)

    # 3. Replace value-reading patterns with fmtNums wrapper
    for fid in dollar_field_ids:
        for pat in [
            '+el("{}").value'.format(fid),
            "+el('{}').value".format(fid),
            'parseFloat(el("{}").value)'.format(fid),
            "parseFloat(el('{}').value)".format(fid),
        ]:
            replacement = 'fmtNums(el("{}").value)'.format(fid)
            html = html.replace(pat, replacement)

    with open(html_path, 'w') as f:
        f.write(html)
    ok = os.path.basename(html_path)
    print("  comma [{} fields]: {}".format(len(dollar_field_ids), ok))

def add_adsense_slot(html_path):
    with open(html_path) as f:
        html = f.read()
    if '<div class="ad-slot">' in html:
        print("  adskip (exists): {}".format(os.path.basename(html_path)))
        return
    # Inject CSS
    m = re.search(r'(<style[^>]*>)(.*?)(</style>)', html, re.DOTALL)
    if m and '.ad-slot{' not in m.group(2):
        css = m.group(2) + ADSENSE_SLOT_CSS
        html = html[:m.start()] + m.group(1) + css + m.group(3) + html[m.end():]
    # Insert slot after calc-card div
    before = '<div class="ad-slot">'
    if before not in html:
        html = re.sub(
            r'(<div class="calc-card">.*?</div>\s*)(<div)',
            r'\1\n' + ADSENSE_SLOT_HTML + r'\n\2',
            html, count=1, flags=re.DOTALL
        )
    with open(html_path, 'w') as f:
        f.write(html)
    ok = '<div class="ad-slot">' in html
    status = "OK" if ok else "FAIL"
    print("  adslot [{}]: {}".format(status, os.path.basename(html_path)))

def remove_no_ads(path):
    with open(path) as f:
        html = f.read()
    changed = html.replace(
        'Straightforward financial tools \u2014 no sign-up, no ads, no fluff.',
        'Straightforward financial tools \u2014 no sign-up, no fluff.'
    )
    with open(path, 'w') as f:
        f.write(changed)
    print("  no-ads: index.html")

# ═══ CALCCLEAR ════════════════════════════════════════════════════════════════
calcclear_dollar = {
    'coast-fire-calculator/index.html':      ['annual-expenses', 'current-savings'],
    'cash-flow-calculator/index.html': [
        'p-salary','p-side','p-passive','p-other-inc',
        'p-housing','p-utilities','p-groceries','p-transport',
        'p-insurance','p-debt','p-subs','p-other-exp',
        'b-revenue','b-other-inc','b-cogs','b-payroll',
        'b-rent','b-marketing','b-software','b-utilities','b-taxes','b-other-exp',
        'r-rent','r-other-inc','r-mortgage','r-tax','r-insurance',
        'r-hoa','r-maintenance','r-vacancy','r-pm','r-other-exp',
    ],
    'heloc-calculator/index.html':            ['h-limit', 'h-balance'],
    'land-loan-calculator/index.html':        ['ll-price', 'll-down'],
    'margin-vs-markup-calculator/index.html': ['m-cost'],
    'probate-calculator/index.html':          ['p-estate'],
}

print("=== CALCCLEAR comma formatting ===")
for rel, fields in calcclear_dollar.items():
    add_comma_formatting('{}/{}'.format(CALCCLEAR_DIR, rel), fields)

print("\n=== CALCCLEAR landing page ===")
remove_no_ads('{}/index.html'.format(CALCCLEAR_DIR))

# ═══ COASTFIREWHEN ═══════════════════════════════════════════════════════════
coastfirewhen_dollar = {
    'fire-progress-tracker.html':       ['expenses', 'investments', 'realEstate', 'cash', 'otherAssets', 'mortgage', 'otherDebt'],
    'safe-withdrawal-rate-guide.html':  ['portfolio', 'withdrawal'],
    'compound-interest-explained.html': ['principal', 'monthly'],
    'coast-fire-calculator-explained.html': ['expenses', 'savings'],
}

print("\n=== COASTFIREWHEN comma formatting ===")
for rel, fields in coastfirewhen_dollar.items():
    add_comma_formatting('{}/{}'.format(COAST_DIR, rel), fields)

print("\n=== COASTFIREWHEN AdSense slots ===")
for rel in list(coastfirewhen_dollar.keys()) + [
    'about.html', 'what-is-coast-fire.html', 'terms.html',
    'privacy-policy.html', 'probate-guide.html', 'margin-vs-markup-guide.html'
]:
    p = '{}/{}'.format(COAST_DIR, rel)
    if os.path.exists(p):
        add_adsense_slot(p)

print("\nAll done.")
