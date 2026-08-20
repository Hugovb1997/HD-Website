#!/usr/bin/env python3
"""Compile the Claude Design canvas file into a standalone production page.

Reads `Humain Demand Website.dc.html` (a .dc.html design-canvas component) and
emits ../index-v2.html with no dependency on the canvas runtime:

  <helmet>            -> real <head>
  <sc-for> / <sc-if>  -> expanded static markup
  style-hover="..."   -> generated .hv<n>:hover CSS rules
  <image-slot>        -> <img> wired to the repo's own asset folders
  booking CTAs        -> Cal.com booking modal

Re-run after any canvas edit:  python3 design-import/build.py
"""

import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "Humain Demand Website.dc.html")
# writes the live page; pass a path to build somewhere else for review first
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "index.html")

# Public Cal.com booking link. Public by design — it ships in the page and is
# visible to every visitor. NEVER put a cal_live_* API key here; that key is for
# the Cal Atoms React SDK and needs a backend to mint short-lived tokens.
#
# Two URLs, deliberately:
#   BOOKING_URL  the plain page, used as the anchor href so the CTA still works
#                with JavaScript disabled.
#   BOOKING_EMBED  the same page with embed=true, used as the modal iframe src.
#                Without embed=true Cal.com renders a BLANK iframe cross-origin,
#                and embed=true is also what makes theme=dark take effect.
CAL_LINK = "hugo-van-baal-agjtxz/30min"
CAL_NAMESPACE = "30min"
BOOKING_URL = "https://cal.com/" + CAL_LINK + "?overlayCalendar=true"

SPOTS_LEFT = 2

# --- data lifted from the canvas component's renderVals() ------------------

COMPARE_ROWS = [
    {"label": "Payment model", "us": "Pay per qualified meeting",
     "agency": "Monthly retainer, hope it works", "diy": "Your time + tool costs"},
    {"label": "Targeting", "us": "Demand Activation Zones",
     "agency": "Job titles and company size", "diy": "Whatever you can figure out"},
    {"label": "Data", "us": "Custom AI agents for signals no one else has",
     "agency": "Same lists everyone uses", "diy": "Apollo/ZoomInfo and pray"},
    {"label": "Research", "us": "Reddit, sales calls, customer interviews",
     "agency": "Skim your website", "diy": "Skip it"},
    {"label": "Personalization", "us": "1:1 unique copy per prospect",
     "agency": "Templates with {first_name}", "diy": "Templates with {first_name}"},
    {"label": "Risk", "us": "Ours", "agency": "Yours", "diy": "Yours"},
    {"label": "Workload", "us": "Us (done for you)",
     "agency": "Them (maybe)", "diy": "You"},
]

FAQS = [
    ("How are you different from other agencies?",
     "Most agencies blast templates and charge retainers whether it works or not. We find "
     "people in pain, write 1:1 messages using data we scrape ourselves, and only get paid "
     "when qualified meetings show up."),
    ("What counts as a qualified meeting?",
     "We decide together before we start. Industry, size, title, revenue, tech stack — "
     "whatever matters to you. If they don't fit, you don't pay."),
    ("How do you find data others can't?",
     "We build custom AI agents that scrape signals no database has. If it exists online, "
     "we can get it."),
    ("How fast will I see results?",
     "Most clients see meetings within weeks. One closed $240K in 30 days. Depends on your market."),
    ("What if it doesn't work?", "You don't pay."),
    ("Long-term contract?",
     "No. Minimum commitment to give it time, but no lock-ins."),
    ("Why performance-based?",
     "It keeps us honest. If we don't deliver, we don't eat."),
]

# --- image-slot id -> real asset ------------------------------------------
# fit: "cover"   crops to fill its box (avatars, logo marks)
#      "contain" fits the whole image inside a fixed box (orbit logos)
#      "natural" fills the width and lets height follow the aspect ratio.
#        Screenshots MUST use this: "contain" inside the canvas's fixed-height
#        cards shrinks a 2000x1414 screenshot to ~364px wide and the email text
#        becomes unreadable. Cards using "natural" have their fixed height
#        stripped below so the image drives the card height.

SLOTS = {
    "nav-logo":   ("logos/Humain Demand_A2 (2).jpg", "Humain Demand", "cover", False),
    "nav-hugo":   ("Profile Pic Hugo/Hugo (Me) profile Pic.jpeg", "Hugo van Baal", "cover", False),

    "arc-av-1": ("Profile Pic Hugo/1579801802849.jpeg", "Client", "cover", False),
    "arc-av-2": ("Testimonials/Ajinder Banns.jpeg", "Ajinder Banns", "cover", False),
    "arc-av-3": ("Profile Pic Hugo/Allan Miller PF.jpeg", "Allan Miller", "cover", False),
    "arc-av-4": ("Testimonials/Theo Gors.jpeg", "Theo Görs", "cover", False),
    "arc-av-5": ("Profile Pic Hugo/Tom Zanoli.jpeg", "Tom Zanoli", "cover", False),

    "reply-7": ("Screenshots/Attached_image7.png", "Cold email reply from a prospect", "natural", True),
    "reply-1": ("Screenshots/Attached_image.png",  "Cold email reply from a prospect", "natural", True),
    "reply-2": ("Screenshots/Attached_image2.png", "Cold email reply from a prospect", "natural", True),
    "reply-3": ("Screenshots/Attached_image3.png", "Cold email reply from a prospect", "natural", True),
    "reply-4": ("Screenshots/Attached_image4.png", "Cold email reply from a prospect", "natural", True),
    "reply-8": ("Screenshots/Attached_image8.png", "Cold email reply from a prospect", "natural", True),
    "reply-6": ("Screenshots/Attached_image6.png", "Cold email reply from a prospect", "natural", True),
    "reply-5": ("Screenshots/Attached_image5.png", "Cold email reply from a prospect", "natural", True),

    "avatar-jesse":   ("Testimonials/Jesse Bak.jpeg", "Jesse Bak", "cover", True),
    "avatar-ajinder": ("Testimonials/Ajinder Banns.jpeg", "Ajinder Banns", "cover", True),
    "avatar-theo":    ("Testimonials/Theo Gors.jpeg", "Theo Görs", "cover", True),

    "cs-np":        ("Proof Elements website/Untitled design (8).png", "National Positions results", "natural", True),
    "cs-avalaunch": ("Proof Elements website/10.png", "Avalaunch Media results", "natural", True),
    "cs-intella":   ("Proof Elements website/8.png", "IntellaWaste results", "natural", True),

    "orbit-1": ("logos/apify-symbol-safe.png", "Apify", "contain", True),
    "orbit-2": ("logos/Icon (1).png", "Outbound tool", "contain", True),
    "orbit-3": ("logos/Icon (2).png", "Outbound tool", "contain", True),
    "orbit-4": ("logos/idHsCfI-UV_1766488223774.jpeg", "Outbound tool", "contain", True),
    "orbit-5": ("logos/idk4YGndV9_1766488176343.jpeg", "Outbound tool", "contain", True),
    "orbit-6": ("logos/idSl0sAgFq_logos.jpeg", "Outbound tool", "contain", True),
    "orbit-7": ("logos/Symbol (1).png", "Outbound tool", "contain", True),
    "orbit-8": ("logos/Symbol.png", "Outbound tool", "contain", True),
    "orbit-center": ("logos/Clay Arch Marque (1).png", "Clay", "contain", True),

    "float-avatar-theo": ("Testimonials/Theo Gors.jpeg", "Theo Görs", "cover", True),
}

# Slots deliberately left empty — no real asset exists yet, and the canvas
# placeholder text says so. Rendered as a styled drop-zone rather than filled
# with stock imagery.
UNFILLED = {"vsl-thumb"}

hover_rules = []


def fail(msg):
    sys.exit("build.py: " + msg)


def add_class(markup, style_marker, classname, expect=None, regex=False):
    """Add `classname` to every tag whose style attribute matches style_marker."""
    count = 0

    def repl(m):
        nonlocal count
        count += 1
        tag = m.group(0)
        if 'class="' in tag:
            return tag.replace('class="', 'class="%s ' % classname, 1)
        return re.sub(r"^<([\w-]+)", r'<\1 class="%s"' % classname, tag, count=1)

    marker = style_marker if regex else re.escape(style_marker)
    pattern = re.compile(r'<\w[\w-]*\b[^>]*?style="[^"]*' + marker + r'[^"]*"[^>]*>')
    markup = pattern.sub(repl, markup)
    if expect is not None and count != expect:
        fail("expected %d matches for %r, found %d" % (expect, style_marker, count))
    return markup


def add_class_by_href(markup, href, classname, expect=None):
    """Add `classname` to the anchor pointing at `href`.

    Keyed on the href rather than a literal tag prefix: by this point the
    hover pass has already injected class="hv<n>" ahead of the href, so
    prefix matching would silently miss.
    """
    pattern = re.compile(r'<a\b[^>]*href="%s"[^>]*>' % re.escape(href))

    def repl(m):
        tag = m.group(0)
        if 'class="' in tag:
            return tag.replace('class="', 'class="%s ' % classname, 1)
        return re.sub(r"^<a", '<a class="%s"' % classname, tag, count=1)

    markup, count = pattern.subn(repl, markup)
    if expect is not None and count != expect:
        fail("expected %d anchors for href=%r, found %d" % (expect, href, count))
    return markup


def subst(tpl, mapping):
    for key, val in mapping.items():
        tpl = tpl.replace("{{ %s }}" % key, val)
    return tpl


def esc(text):
    return html.escape(text, quote=False)


# ---------------------------------------------------------------------------
# 1. split the canvas file
# ---------------------------------------------------------------------------

with open(SRC, encoding="utf-8") as fh:
    raw = fh.read()

helmet = re.search(r"<helmet>(.*?)</helmet>", raw, re.S)
if not helmet:
    fail("no <helmet> block found")
head_inner = helmet.group(1)
head_inner = re.sub(r'<script src="\./image-slot\.js"></script>\s*', "", head_inner)
head_inner = re.sub(r"<title>.*?</title>\s*", "", head_inner, flags=re.S)

body = raw[raw.index("</helmet>") + len("</helmet>"): raw.rindex("</x-dc>")]

# ---------------------------------------------------------------------------
# 2. expand <sc-for> comparison rows
# ---------------------------------------------------------------------------

m = re.search(r'<sc-for list="\{\{ compareRows \}\}"[^>]*>(.*?)</sc-for>', body, re.S)
if not m:
    fail("comparison <sc-for> not found")
row_tpl = m.group(1)
rows_out = "".join(
    subst(row_tpl, {
        "row.label": esc(r["label"]),
        "row.us": esc(r["us"]),
        "row.agency": esc(r["agency"]),
        "row.diy": esc(r["diy"]),
    })
    for r in COMPARE_ROWS
)
body = body[: m.start()] + rows_out + body[m.end():]

# ---------------------------------------------------------------------------
# 3. expand <sc-for> FAQ into a real accordion
# ---------------------------------------------------------------------------

m = re.search(r'<sc-for list="\{\{ faqs \}\}"[^>]*>(.*?)</sc-for>', body, re.S)
if not m:
    fail("FAQ <sc-for> not found")
faq_tpl = m.group(1)

inner_if = re.search(r'<sc-if value="\{\{ faq\.open \}\}"[^>]*>(.*?)</sc-if>', faq_tpl, re.S)
if not inner_if:
    fail("FAQ answer <sc-if> not found")
answer_tpl = inner_if.group(1).strip()

faq_out = []
for i, (question, answer) in enumerate(FAQS):
    is_open = i == 0
    item = faq_tpl[: inner_if.start()], faq_tpl[inner_if.end():]

    head_part = item[0]
    head_part = head_part.replace(
        'onClick="{{ faq.toggle }}"',
        'type="button" class="faq-q" data-faq="%d" id="faq-btn-%d" '
        'aria-expanded="%s" aria-controls="faq-panel-%d"' % (i, i, "true" if is_open else "false", i),
    )
    head_part = subst(head_part, {
        "faq.idx": "Q%02d" % (i + 1),
        "faq.q": esc(question),
        "faq.icon": "&minus;" if is_open else "+",
    })

    panel = subst(answer_tpl, {"faq.a": esc(answer)})
    panel = ('<div class="faq-panel" id="faq-panel-%d" role="region" aria-labelledby="faq-btn-%d"%s>%s</div>'
             % (i, i, "" if is_open else " hidden", panel))

    faq_out.append(head_part + panel + item[1])

body = body[: m.start()] + "".join(faq_out) + body[m.end():]

# ---------------------------------------------------------------------------
# 4. resolve remaining <sc-if> blocks (marquee on, floating card on)
# ---------------------------------------------------------------------------

body = re.sub(r'<sc-if value="\{\{ showMarquee \}\}"[^>]*>(.*?)</sc-if>', r"\1", body, flags=re.S)

m = re.search(r'<sc-if value="\{\{ floatingVisible \}\}"[^>]*>(.*?)</sc-if>', body, re.S)
if not m:
    fail("floating testimonial <sc-if> not found")
floating = m.group(1)
floating = floating.replace(
    'onClick="{{ dismissFloating }}"',
    'type="button" id="floating-dismiss" aria-label="Dismiss testimonial"',
)
floating = floating.replace("<div style=\"position:fixed", "<div id=\"floating-card\" style=\"position:fixed", 1)
body = body[: m.start()] + floating + body[m.end():]

if "<sc-" in body:
    fail("unresolved <sc-*> directive remains")

# ---------------------------------------------------------------------------
# 5. scalar interpolation
# ---------------------------------------------------------------------------

body = body.replace("{{ spotsLeft }}", str(SPOTS_LEFT))
leftover = re.findall(r"\{\{[^}]*\}\}", body)
if leftover:
    fail("unresolved interpolation(s): %s" % sorted(set(leftover)))

# ---------------------------------------------------------------------------
# 5b. hero VSL frame — removed until the VSL exists
#
# Hugo asked (2026-08-20) to take the video frame out of the hero until he has
# the actual VSL. The markup stays in the canvas file; this just skips it at
# build time. TO BRING IT BACK: set SHOW_VSL = True, and map "vsl-thumb" in
# SLOTS to the real thumbnail (or leave it in UNFILLED for the branded cover).
# ---------------------------------------------------------------------------

SHOW_VSL = False

VSL_MARKER = ('<div style="max-width:960px;width:100%;'
              'animation:rise .9s cubic-bezier(.22,.7,.25,1) .4s both">')

if not SHOW_VSL:
    i = body.find(VSL_MARKER)
    if i == -1:
        fail("VSL frame marker not found in canvas")
    depth = 0
    end = -1
    for m in re.finditer(r"<div\b|</div>", body[i:]):
        depth += 1 if m.group(0).startswith("<div") else -1
        if depth == 0:
            end = i + m.end()
            break
    if end == -1:
        fail("VSL frame divs not balanced")
    body = body[:i] + body[end:]
    if "vsl-thumb" in body:
        fail("VSL removal left the vsl-thumb slot behind")

# ---------------------------------------------------------------------------
# 6. style-hover="..." -> real :hover CSS
# ---------------------------------------------------------------------------


def hover_repl(m):
    rules = m.group("rules").strip().rstrip(";")
    cls = "hv%d" % (len(hover_rules) + 1)
    hover_rules.append((cls, rules))
    tag = m.group(0)
    tag = re.sub(r'\s*style-hover="[^"]*"', "", tag)
    if 'class="' in tag:
        return tag.replace('class="', 'class="%s ' % cls, 1)
    return re.sub(r"^<([\w-]+)", r'<\1 class="%s"' % cls, tag, count=1)


body = re.sub(r'<[\w-]+\b[^>]*?style-hover="(?P<rules>[^"]*)"[^>]*>', hover_repl, body)
if "style-hover" in body:
    fail("style-hover attribute survived the rewrite")

# ---------------------------------------------------------------------------
# 7. <image-slot> -> <img>
# ---------------------------------------------------------------------------

RADIUS = {"circle": "50%", "pill": "999px", "rect": "0"}


def slot_repl(m):
    attrs = m.group(1)

    def attr(name):
        a = re.search(r'\b%s="([^"]*)"' % name, attrs)
        return a.group(1) if a else None

    sid = attr("id")
    shape = attr("shape") or "rounded"
    extra = attr("style") or ""
    placeholder = attr("placeholder") or ""

    radius = RADIUS.get(shape, "%spx" % (attr("radius") or "12"))
    fit_mode = SLOTS[sid][2] if sid in SLOTS else "contain"
    if fit_mode == "natural":
        base = "display:block;width:100%;height:auto;border-radius:" + radius
    else:
        base = "display:block;width:100%;height:100%;border-radius:" + radius

    if sid == "vsl-thumb" and sid in UNFILLED:
        # Only used when SHOW_VSL is on but no thumbnail is mapped yet: a
        # branded cover (logo on the page's gradient palette) so the frame
        # looks finished — the canvas layers the play button on top of it.
        return ('<div style="' + base + ';' + extra + ';position:relative;background:'
                'radial-gradient(60% 80% at 50% 20%, rgba(0,179,137,.28) 0%, rgba(11,9,13,0) 70%),'
                'radial-gradient(50% 60% at 85% 80%, rgba(70,30,110,.4) 0%, rgba(11,9,13,0) 70%),'
                'radial-gradient(40% 50% at 15% 75%, rgba(90,20,60,.35) 0%, rgba(11,9,13,0) 70%),#0b090d;'
                'display:flex;align-items:center;justify-content:center">'
                '<img src="logos/Humain Demand_A2 (2).jpg" alt="Humain Demand" '
                'style="width:110px;height:110px;border-radius:26px;object-fit:cover;'
                'box-shadow:0 0 70px rgba(0,255,196,.3);opacity:.92"></div>')

    if sid in UNFILLED:
        return ('<div class="slot-empty" style="%s;%s">'
                '<span>%s</span></div>' % (base, extra, esc(placeholder)))

    if sid not in SLOTS:
        fail("no asset mapped for image-slot id=%r" % sid)

    src, alt, fit, lazy = SLOTS[sid]
    path = os.path.join(HERE, "..", src)
    if not os.path.exists(path):
        fail("asset missing on disk: %s" % src)

    # object-fit is meaningless once height is auto — the image is already at
    # its natural ratio — so omit it rather than emit a no-op declaration
    fit_decl = "" if fit == "natural" else "object-fit:%s;" % fit
    return ('<img src="%s" alt="%s" %sstyle="%s;%s%s">'
            % (html.escape(src), html.escape(alt),
               'loading="lazy" decoding="async" ' if lazy else "",
               base, fit_decl, extra))


body = re.sub(r"<image-slot\b([^>]*)></image-slot>", slot_repl, body)
if "<image-slot" in body:
    fail("image-slot element survived the rewrite")

# ---------------------------------------------------------------------------
# 8. wire booking CTAs to the Calendly modal
# ---------------------------------------------------------------------------

booked = 0


def cta_repl(m):
    global booked
    tag = m.group(0)
    text = re.sub(r"<[^>]+>", "", m.group(2))
    if "Apply For A Performance Campaign" not in text and "Book Your Demo" not in text:
        return tag
    booked += 1
    # href stays a real link so the CTA still works without JS; Cal's embed.js
    # binds data-cal-link and preventDefaults the click to open its modal
    cal_attrs = ('href="%s" data-book="1" data-cal-namespace="%s" data-cal-link="%s" '
                 "data-cal-config='{\"layout\":\"month_view\",\"theme\":\"dark\"}'"
                 % (html.escape(BOOKING_URL), CAL_NAMESPACE, CAL_LINK))
    opening = re.sub(r'href="#(?:apply|faq)"', cal_attrs, m.group(1), count=1)
    if "Apply For A Performance Campaign" in text:
        # the long-label buttons are the ones that need mobile shrinking;
        # the hover pass already put a class on these tags, so append to it
        if 'class="' in opening:
            opening = opening.replace('class="', 'class="cta-primary ', 1)
        else:
            opening = re.sub(r"^<a", '<a class="cta-primary"', opening, count=1)
    return opening + m.group(2) + "</a>"


body = re.sub(r'(<a\b[^>]*href="#(?:apply|faq)"[^>]*>)(.*?)</a>', cta_repl, body, flags=re.S)
if booked != 7:
    fail("expected 7 booking CTAs, wired %d" % booked)

# ---------------------------------------------------------------------------
# 8b. let the reply screenshots set their own card height
#
# The canvas pins these cards to 250px/320px and stretches the slot to fill,
# which is right for a decorative placeholder but wrong for a 1.41:1 screenshot
# of an email — it ends up scaled down to a fifth of the card width and the text
# is unreadable. Dropping the fixed height lets each screenshot render full
# width at its natural ratio, the way the previous site did it.
# ---------------------------------------------------------------------------

def drop_style(markup, fragment, replacement, expect):
    count = markup.count(fragment)
    if count != expect:
        fail("expected %d occurrences of %r, found %d" % (expect, fragment, count))
    return markup.replace(fragment, replacement)


body = drop_style(body, ";height:250px;transition", ";transition", expect=6)
# The two featured (span-2) frames keep the canvas's 320px card height; their
# 2000x1414 screenshots would render ~520px tall at full width, so show a
# vertically-centered 320px window of the image instead (same crop the old
# site used: fixed-height window, overflow hidden, image centered).
body = drop_style(
    body,
    '<div style="height:calc(100% - 22px)">',
    '<div style="height:calc(100% - 22px);overflow:hidden;display:flex;'
    'align-items:center;border-radius:10px">',
    expect=2,
)
body = drop_style(body, '<div style="height:calc(100% - 20px)">', "<div>", expect=6)

# ---------------------------------------------------------------------------
# 9. tag layout containers so the responsive stylesheet can reach them
# ---------------------------------------------------------------------------

# the phase/result cards stick at 88px..148px; the nav sticks at 0 and must not match
body = add_class(body, r"position:sticky;top:\d{2,}px", "phase-sticky", expect=6, regex=True)
body = add_class(body, "min-height:420px", "phase-card", expect=5)
body = add_class(body, "gap:48px;align-items:center", "cs-card", expect=3)
body = add_class(body, "grid-template-columns:1fr auto 1fr auto 1fr", "stats-grid", expect=1)
body = add_class(body, "width:1px;height:34px", "stat-divider", expect=2)
body = add_class(body, "grid-template-columns:1fr 1fr;gap:32px", "reply-grid", expect=1)
body = add_class(body, "grid-template-columns:150px repeat(3,1fr)", "compare-grid", expect=1)
body = add_class(body, "width:480px;height:480px", "orbit", expect=1)
body = add_class(body, "gap:26px;font-size:14px", "nav-actions", expect=1)
body = add_class(body, "letter-spacing:.14em;text-transform:uppercase;color:#7d7484;border:1px solid", "nav-badge", expect=1)
# leading ';' required — bare "order:1" also matches inside "border:1px"
body = add_class(body, ";order:1;", "cs-media-first", expect=1)
body = add_class(body, ";order:2;", "cs-text-second", expect=1)

# nav text links (the three in-page anchors), so they can collapse on mobile
for anchor in ("#methodology", "#case-studies", "#faq"):
    body = add_class_by_href(body, anchor, "nav-link", expect=1)

# comparison table gets a horizontal scroll container on narrow screens
body = body.replace('<div class="compare-grid"', '<div class="table-scroll"><div class="compare-grid"', 1)
body = body.replace("</sc-for-close-marker>", "")
idx = body.index('<div class="table-scroll">')
end = body.index("</div>\n  </div>\n</section>", idx)
body = body[:end] + "</div>\n" + body[end:]

# ---------------------------------------------------------------------------
# 10. assemble the page
# ---------------------------------------------------------------------------

# Every declaration needs !important: the canvas puts ALL base styling in
# inline style="" attributes, and inline styles beat any selector — so a plain
# .hvN:hover rule silently loses and no hover effect ever shows. Author
# !important is the one thing in the cascade that outranks inline styles.
def importantify(rules):
    parts = [p.strip() for p in rules.split(";") if p.strip()]
    return ";".join(p if p.endswith("!important") else p + " !important" for p in parts)


hover_css = "\n".join(".%s:hover{%s}" % (cls, importantify(rules)) for cls, rules in hover_rules)

EXTRA_CSS = """
/* NO global box-sizing reset here on purpose. The canvas was authored against
   the browser default (content-box) — it sets box-sizing:border-box inline on
   the few elements that want it — so forcing border-box globally silently
   resizes every fixed-size element that also has padding, and the page stops
   matching the design. Keep this file additive; never restyle the canvas. */

/* Safety net for the oversized decorative type. Must be `clip`, NOT `hidden`:
   overflow-x:hidden computes overflow-y to auto, which makes body a scroll
   container and silently kills position:sticky on the phase cards. */
body{overflow-x:clip}
img{max-width:100%}
.skip-link{position:absolute;left:-9999px;top:0;z-index:200;background:#00ffc4;color:#000;
  padding:12px 20px;border-radius:0 0 10px 0;font-weight:700}
.skip-link:focus{left:0;color:#000}
:focus-visible{outline:2px solid #00ffc4;outline-offset:3px}

.slot-empty{display:flex;align-items:center;justify-content:center;text-align:center;padding:24px;
  background:repeating-linear-gradient(45deg,rgba(255,255,255,.03) 0 12px,transparent 12px 24px),#0b090d;
  border:1px dashed rgba(0,255,196,.35);color:#7d7484;font-family:'JetBrains Mono',monospace;
  font-size:12px;letter-spacing:.08em;text-transform:uppercase}

.faq-q{width:100%}
.faq-panel[hidden]{display:none}

/* Cal.com renders its own modal; just keep it above the sticky nav */
cal-modal-box{z-index:200}

@media (max-width:1080px){
  .cs-card,.phase-card{padding:36px !important;gap:32px !important}
}
#nav-burger{display:none;background:none;border:1px solid rgba(255,255,255,.15);border-radius:10px;
  color:#ece7ee;width:38px;height:38px;font-size:17px;cursor:pointer;
  align-items:center;justify-content:center;flex-shrink:0}
#nav-burger:hover{border-color:rgba(0,255,196,.4);color:#00ffc4}
#mobile-nav{position:absolute;top:100%;left:0;right:0;background:rgba(16,13,19,.97);
  backdrop-filter:blur(14px);border-bottom:1px solid rgba(255,255,255,.1);
  padding:10px 24px 16px;display:flex;flex-direction:column;gap:4px}
#mobile-nav[hidden]{display:none}
#mobile-nav .nav-link{display:block !important;padding:10px 0;font-size:15px;font-weight:500}

@media (max-width:900px){
  #nav-burger{display:inline-flex}
  .phase-sticky{position:relative !important;top:auto !important;margin-bottom:24px !important}
  .phase-card,.cs-card{grid-template-columns:minmax(0,1fr) !important;min-height:0 !important}
  .cs-media-first{order:2 !important}
  .cs-text-second{order:1 !important}
  .reply-grid{grid-template-columns:minmax(0,1fr) !important}
  .reply-grid>*{grid-column:auto !important;transform:none !important}
  .stats-grid{grid-template-columns:minmax(0,1fr) !important;gap:18px !important}
  .stat-divider{display:none !important}
  .table-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch;border-radius:20px}
  .compare-grid{min-width:720px}
  .nav-link,.nav-badge{display:none !important}
}
@media (max-width:640px){
  section,header{padding-left:18px !important;padding-right:18px !important}
  .phase-card,.cs-card{padding:26px !important}
  .orbit{transform:scale(.68);margin:-76px 0}
  .nav-actions{gap:12px !important}
  /* the long CTA label needs room to breathe at 390px */
  .cta-primary{font-size:15px !important;padding:14px 20px !important;text-align:center}
  h1{font-size:clamp(34px,9vw,46px) !important}
}
"""

JS = """
(function(){
  // Cal's embed.js opens its modal from its own click listener but never
  // prevents the anchor's default navigation (its docs assume <button>s with
  // no href), so without this the browser follows the link to cal.com and the
  // visitor leaves the page. Cancel navigation only once the embed has really
  // executed — Cal.instance exists only after embed.js runs — so the href
  // stays a working fallback whenever the embed script is blocked or slow.
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-cal-link]');
    if(a && window.Cal && window.Cal.instance) e.preventDefault();
  });

  // FAQ accordion — one open at a time, matching the canvas behaviour
  document.addEventListener('click',function(e){
    var btn=e.target.closest('.faq-q');
    if(!btn) return;
    var isOpen=btn.getAttribute('aria-expanded')==='true';
    document.querySelectorAll('.faq-q').forEach(function(other){
      other.setAttribute('aria-expanded','false');
      other.querySelector('span:last-child').innerHTML='+';
      document.getElementById(other.getAttribute('aria-controls')).hidden=true;
    });
    if(!isOpen){
      btn.setAttribute('aria-expanded','true');
      btn.querySelector('span:last-child').innerHTML='\\u2212';
      document.getElementById(btn.getAttribute('aria-controls')).hidden=false;
    }
  });

  // Mobile nav: below 900px the canvas's text links are hidden (it is a
  // desktop-only design), so rebuild them as a hamburger dropdown cloned from
  // the same anchors. Runtime injection keeps the canvas markup untouched.
  var actions=document.querySelector('.nav-actions');
  var links=document.querySelectorAll('nav .nav-link');
  if(actions&&links.length){
    var burger=document.createElement('button');
    burger.id='nav-burger';burger.type='button';burger.innerHTML='&#9776;';
    burger.setAttribute('aria-label','Open navigation menu');
    burger.setAttribute('aria-expanded','false');
    burger.setAttribute('aria-controls','mobile-nav');
    actions.appendChild(burger);
    var panel=document.createElement('div');
    panel.id='mobile-nav';panel.hidden=true;
    links.forEach(function(a){panel.appendChild(a.cloneNode(true));});
    document.querySelector('nav').appendChild(panel);
    function setMenu(open){
      panel.hidden=!open;
      burger.setAttribute('aria-expanded',String(open));
    }
    burger.addEventListener('click',function(){setMenu(panel.hidden);});
    panel.addEventListener('click',function(e){if(e.target.closest('a'))setMenu(false);});
  }

  var dismiss=document.getElementById('floating-dismiss');
  if(dismiss) dismiss.addEventListener('click',function(){
    var card=document.getElementById('floating-card');
    if(card) card.remove();
  });
})();
"""

# Cal.com's official embed. A plain <iframe> to the booking page does NOT work:
# Cal only reveals the booking UI after embed.js completes a postMessage
# handshake from the parent, so without this script the iframe stays blank.
# embed.js binds every [data-cal-link] element and opens its own themed modal.
MODAL = """
<script>
(function (C, A, L) { let p = function (a, ar) { a.q.push(ar); }; let d = C.document; C.Cal = C.Cal || function () { let cal = C.Cal; let ar = arguments; if (!cal.loaded) { cal.ns = {}; cal.q = cal.q || []; d.head.appendChild(d.createElement("script")).src = A; cal.loaded = true; } if (ar[0] === L) { const api = function () { p(api, arguments); }; const namespace = ar[1]; api.q = api.q || []; if (typeof namespace === "string") { cal.ns[namespace] = cal.ns[namespace] || api; p(cal.ns[namespace], ar); p(cal, ["initNamespace", namespace]); } else p(cal, ar); return; } p(cal, ar); }; })(window, "https://app.cal.com/embed/embed.js", "init");
Cal("init", "%s", {origin:"https://cal.com"});
Cal.ns["%s"]("ui", {"theme":"dark","hideEventTypeDetails":false,"layout":"month_view"});
</script>
""" % (CAL_NAMESPACE, CAL_NAMESPACE)

DESCRIPTION = ("Performance-based outbound for B2B marketing agencies doing $100K+/month. "
               "We book you 12-30 qualified meetings per month - you only pay when we do.")

page = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Humain Demand — Outbound Engineering</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:title" content="Humain Demand — Outbound Engineering">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="logos/Humain Demand_A2 (2).jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="logos/Humain Demand_A2 (2).jpg">
{head}
<style>
{extra}
{hover}
</style>
</head>
<body>
<a class="skip-link" href="#main-content">Skip to content</a>
{body}
{modal}
<script>
{js}
</script>
</body>
</html>
""".format(desc=html.escape(DESCRIPTION, quote=True),
           head=head_inner.strip(),
           extra=EXTRA_CSS.strip(),
           hover=hover_css,
           body=body.strip(),
           modal=MODAL.strip(),
           js=JS.strip())

# anchor target for the skip link
page = page.replace("<!-- HERO -->\n<header", '<!-- HERO -->\n<header id="main-content"', 1)

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write(page)

print("wrote %s" % os.path.normpath(OUT))
print("  %d hover rules, %d images, %d FAQ items, %d compare rows, %d booking CTAs"
      % (len(hover_rules), len(SLOTS), len(FAQS), len(COMPARE_ROWS), booked))
