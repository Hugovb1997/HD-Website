#!/usr/bin/env python3
"""Generate the standalone legal pages (privacy.html, terms.html).

Called at the end of build.py so one `python3 design-import/build.py` run
produces the whole site. These pages are NOT part of the design canvas —
the canvas has no legal screens — so they are authored here against the
same fonts, palette and footer as the compiled landing page.

    >>> CHECK BEFORE PUBLISHING <<<
ENTITY / COUNTRY / GOVERNING_LAW below are the registered-business details
that appear in both documents. They are an assumption, not verified fact:
Hugo has not confirmed the registered entity name or country, so they were
set from the Europe/Amsterdam booking calendar. Confirm them (and add a KvK
/ company number and registered address if one exists) before treating these
pages as binding. Everything else in the copy is business-accurate.
"""

import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

# --- business details rendered into both documents -------------------------
ENTITY = "Humain Demand"
COUNTRY = "the Netherlands"
GOVERNING_LAW = "the laws of the Netherlands"
COURTS = "the competent courts of the Netherlands"
EMAIL = "hugo@humaindemand.com"
LAST_UPDATED = "September 2026"

FONTS = ("https://fonts.googleapis.com/css2?family=Anton&family=Space+Grotesk:"
         "wght@400;500;600;700&family=Instrument+Serif:ital@1&"
         "family=JetBrains+Mono:wght@400;600&display=swap")

CSS = """
html,body{margin:0;padding:0;background:#100d13;font-family:'Space Grotesk',sans-serif;color:#ece7ee}
body{overflow-x:clip}
*{box-sizing:border-box}
a{color:#00ffc4;text-decoration:none}
a:hover{color:#7dffe2}
::selection{background:#00b389;color:#000}

nav{position:sticky;top:0;z-index:70;background:rgba(16,13,19,.82);backdrop-filter:blur(14px);
  border-bottom:1px solid rgba(255,255,255,.07)}
.nav-row{max-width:900px;margin:0 auto;padding:14px 24px;display:flex;align-items:center;
  justify-content:space-between;gap:16px}
.brand{display:flex;align-items:center;gap:10px;color:#fff}
.brand img{width:28px;height:28px;border-radius:7px;object-fit:cover;display:block}
.brand span{font-weight:700;font-size:16px;letter-spacing:-.01em}
.back{font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.08em;
  text-transform:uppercase;border:1px solid rgba(255,255,255,.15);border-radius:999px;
  padding:8px 16px;color:#ece7ee;white-space:nowrap;transition:border-color .3s,color .3s}
.back:hover{border-color:rgba(0,255,196,.5);color:#00ffc4}

main{max-width:900px;margin:0 auto;padding:72px 24px 96px}
.kicker{font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.14em;
  text-transform:uppercase;color:#00ffc4;margin:0 0 18px}
h1{font-family:'Anton',sans-serif;font-weight:400;font-size:clamp(38px,7vw,68px);line-height:1.02;
  text-transform:uppercase;letter-spacing:-.01em;margin:0 0 14px}
.updated{font-family:'JetBrains Mono',monospace;font-size:12.5px;letter-spacing:.06em;
  color:#7d7484;margin:0 0 44px;padding-bottom:28px;border-bottom:1px solid rgba(255,255,255,.09)}
.lede{font-size:17px;line-height:1.75;color:#c9c2d0;margin:0 0 44px}
h2{font-family:'Anton',sans-serif;font-weight:400;font-size:clamp(20px,3vw,26px);line-height:1.2;
  text-transform:uppercase;letter-spacing:.005em;margin:46px 0 16px;color:#fff}
h2 .num{color:#00ffc4;margin-right:12px}
h3{font-size:15px;font-weight:600;color:#fff;margin:26px 0 10px}
p{font-size:15.5px;line-height:1.78;color:#c9c2d0;margin:0 0 16px}
ul{margin:0 0 16px;padding-left:22px}
li{font-size:15.5px;line-height:1.78;color:#c9c2d0;margin-bottom:9px}
li strong,p strong{color:#fff;font-weight:600}
.callout{background:#17121b;border:1px solid rgba(255,255,255,.1);border-left:2px solid #00b389;
  border-radius:14px;padding:22px 24px;margin:0 0 16px}
.callout p:last-child{margin-bottom:0}
.contact{background:#17121b;border:1px solid rgba(255,255,255,.1);border-radius:18px;
  padding:26px 28px;margin-top:14px}
.contact p{margin-bottom:6px}
.contact .name{color:#fff;font-weight:600}

footer{border-top:1px solid rgba(255,255,255,.07);padding:40px 24px}
.foot-row{max-width:900px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;
  gap:18px;flex-wrap:wrap}
.foot-row .copy{font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.06em;color:#7d7484}
.foot-links{display:flex;gap:20px;font-size:13px;flex-wrap:wrap}
.foot-links a{color:#a49daa}
.foot-links a:hover{color:#00ffc4}

@media (max-width:640px){
  main{padding:48px 20px 72px}
  .nav-row{padding:12px 20px}
  .brand span{font-size:14px}
  .back{padding:7px 12px;font-size:11px}
  footer{padding:32px 20px}
  .foot-row{justify-content:flex-start;gap:14px}
}
"""

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Humain Demand</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, follow">
<link rel="icon" href="/logos/hd-mark.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="{fonts}" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<nav>
  <div class="nav-row">
    <a class="brand" href="/">
      <img src="/logos/hd-mark.png" alt="Humain Demand">
      <span>Humain Demand</span>
    </a>
    <a class="back" href="/">&larr; Back to home</a>
  </div>
</nav>
<main>
  <p class="kicker">[ Legal ]</p>
  <h1>{heading}</h1>
  <p class="updated">Last updated: {updated}</p>
  {body}
</main>
<footer>
  <div class="foot-row">
    <span class="copy">&copy; 2026 Humain Demand &middot; Outbound engineering</span>
    <div class="foot-links">
      <a href="/">Home</a>
      <a href="/privacy">Privacy Policy</a>
      <a href="/terms">Terms &amp; Conditions</a>
      <a href="mailto:{email}">Contact</a>
    </div>
  </div>
</footer>
</body>
</html>
"""


def sections(items):
    """[(heading, body_html)] -> numbered <h2> blocks."""
    out = []
    for i, (heading, body) in enumerate(items, start=1):
        out.append('<h2><span class="num">%02d</span>%s</h2>\n%s'
                   % (i, html.escape(heading), body.strip()))
    return "\n\n".join(out)


CONTACT_BLOCK = """<div class="contact">
<p class="name">{entity}</p>
<p>{country_cap}</p>
<p>Email: <a href="mailto:{email}">{email}</a></p>
</div>""".format(entity=ENTITY,
                 country_cap=COUNTRY[0].upper() + COUNTRY[1:],
                 email=EMAIL)

# --------------------------------------------------------------------------
# Privacy Policy
# --------------------------------------------------------------------------

SHORT = "Humain Demand"
NAMED = ENTITY if ENTITY == SHORT else '%s ("%s"' % (ENTITY, SHORT)
# renders as:  Humain Demand ("we", ...)   or   Humain Demand B.V. ("Humain Demand", "we", ...)
SELF = '%s ("we", "us" or "our")' % ENTITY if ENTITY == SHORT else '%s ("%s", "we", "us" or "our")' % (ENTITY, SHORT)

PRIVACY_LEDE = """<p class="lede">{self_ref} is committed to
protecting your privacy. This policy explains what information we collect, how we use it, who we
share it with, and the rights you have over it — both when you visit this website and when we
contact you as part of an outbound campaign.</p>""".format(self_ref=SELF)

PRIVACY = [
    ("Information we collect", """
<h3>Information you give us</h3>
<ul>
  <li>Your name, email address, company and role when you book a call or contact us</li>
  <li>Anything else you choose to share in correspondence, on a call, or during onboarding</li>
</ul>
<h3>Information collected automatically</h3>
<ul>
  <li>Pages visited, time on site and referral source</li>
  <li>Device and browser information</li>
  <li>IP address and the approximate location derived from it</li>
</ul>
<h3>Client relationship records</h3>
<ul>
  <li>Communication history, campaign performance data and service preferences held in our CRM</li>
</ul>
"""),

    ("Prospect data in outbound campaigns", """
<p>Running outbound is our service, so it is worth being explicit about it. When we run campaigns
for a client, we process <strong>business contact details</strong> — typically a work email address,
job title, employer and publicly available information about that company — in order to send
relevant, individually researched messages.</p>
<div class="callout">
<p>We rely on <strong>legitimate interest</strong> as our lawful basis for business-to-business
outreach, and we assess that interest against the recipient's rights before campaigns go out. We do
not target consumers, we do not buy or sell personal data, and we never send bulk untargeted mail.</p>
</div>
<ul>
  <li>Prospect data is sourced from public sources and licensed business-data providers</li>
  <li>Every message carries a clear way to opt out, and opt-outs are honoured across all campaigns</li>
  <li>Once you opt out we retain the minimum needed — normally just your email address on a
      suppression list — so that we do not contact you again</li>
</ul>
<p>If you received an email from us and want to know where your details came from, or want them
removed, email <a href="mailto:{email}">{email}</a> and we will action it.</p>
""".format(email=EMAIL)),

    ("How we use information", """
<ul>
  <li>Responding to enquiries and providing support</li>
  <li>Delivering our outbound, lead generation and data enrichment services</li>
  <li>Improving the website, our services and the experience of using them</li>
  <li>Sending service updates and, where you have consented or where permitted for existing
      business contacts, relevant marketing</li>
  <li>Analysing traffic and usage patterns</li>
  <li>Meeting legal obligations and protecting our rights</li>
</ul>
"""),

    ("Who we share it with", """
<p><strong>We do not sell your personal information.</strong> We share it only with:</p>
<ul>
  <li><strong>Service providers</strong> who help us operate — email infrastructure, CRM,
      scheduling, data enrichment and analytics tools — each bound by confidentiality obligations
      and permitted to use the data only to provide their service to us</li>
  <li><strong>Clients</strong>, where you have replied to a campaign we run on their behalf and the
      conversation is being handed over to them</li>
  <li><strong>Authorities</strong>, where we are required to by law or to protect our legal rights</li>
</ul>
"""),

    ("International transfers", """
<p>Some of the providers we use operate outside {country}. Where personal data is transferred
outside the European Economic Area, we rely on appropriate safeguards such as the European
Commission's Standard Contractual Clauses or an adequacy decision covering the destination country.</p>
""".format(country=COUNTRY)),

    ("How long we keep it", """
<p>We keep personal information only as long as needed for the purpose it was collected, plus any
period required for legal, accounting or reporting obligations. In practice that means client
records are kept for the duration of the relationship and a reasonable period afterwards, enquiry
records for as long as the enquiry is live and a reasonable period afterwards, and suppression-list
entries indefinitely, precisely so that we can keep honouring an opt-out.</p>
"""),

    ("Security", """
<p>We apply appropriate technical and organisational measures to protect personal information
against unauthorised access, alteration, disclosure or destruction. No method of transmission or
storage is completely secure, however, and we cannot guarantee absolute security.</p>
"""),

    ("Your rights", """
<p>Subject to certain legal exceptions, you have the right to:</p>
<ul>
  <li><strong>Access</strong> — request a copy of the personal information we hold about you</li>
  <li><strong>Rectification</strong> — have inaccurate or incomplete information corrected</li>
  <li><strong>Erasure</strong> — ask us to delete your personal information</li>
  <li><strong>Restriction and objection</strong> — object to processing based on legitimate
      interest, including our outbound outreach, at any time</li>
  <li><strong>Portability</strong> — receive your data in a structured, machine-readable format</li>
  <li><strong>Opt out</strong> — unsubscribe from marketing at any time</li>
</ul>
<p>To exercise any of these, email <a href="mailto:{email}">{email}</a>. You also have the right to
lodge a complaint with your local data protection authority.</p>
""".format(email=EMAIL)),

    ("Cookies and analytics", """
<p>This site uses a small number of cookies and similar technologies to keep the site working and to
understand how it is used in aggregate. You can control or block cookies through your browser
settings; the site remains usable if you do.</p>
<p>Booking a call loads a scheduling widget from Cal.com, and the testimonial videos are embedded
from YouTube. Both are third parties that may set their own cookies and receive your IP address when
that content loads, under their own privacy policies.</p>
"""),

    ("Changes to this policy", """
<p>We may update this policy from time to time. Changes are published on this page with a revised
"Last updated" date.</p>
"""),

    ("Contact us", """
<p>Questions about this policy or how we handle data:</p>
""" + CONTACT_BLOCK),
]

# --------------------------------------------------------------------------
# Terms & Conditions
# --------------------------------------------------------------------------

TERMS_LEDE = """<p class="lede">These Terms and Conditions ("Terms") govern your access to and use
of this website and the services provided by {self_ref}.</p>""".format(self_ref=SELF)

TERMS = [
    ("Agreement to these terms", """
<p>By using this website or our services you agree to these Terms and to our
<a href="/privacy">Privacy Policy</a>. If you do not agree, please do not use the site or the
services. We may amend these Terms at any time; changes take effect when posted on this page.</p>
"""),

    ("Our services", """
<p>We provide performance-based outbound, lead generation, data enrichment and related business
development services for B2B companies.</p>
<p>The scope, deliverables, timeline and fees for any engagement are set out in the individual
agreement or statement of work between you and us. Where those documents conflict with these Terms,
the individual agreement takes precedence.</p>
"""),

    ("Performance-based engagements", """
<p>Our standard model is payment per qualified meeting rather than a fixed retainer. Because that
turns on what "qualified" means, we define it with you in writing before a campaign starts —
covering industry, company size, job title, revenue and any other criteria that matter to you.</p>
<ul>
  <li>Meetings that do not meet the agreed criteria are not chargeable</li>
  <li>The criteria, rates and any minimum commitment are recorded in your engagement agreement</li>
  <li>We do not guarantee a specific number of meetings, conversion rate, pipeline value or revenue.
      Outbound results depend on your market, offer and sales process as well as our work</li>
</ul>
"""),

    ("Your responsibilities as a client", """
<p>Where we run campaigns on your behalf, you confirm that:</p>
<ul>
  <li>You have the authority to instruct outreach on behalf of your business, including use of
      domains and sending identities you provide or ask us to set up</li>
  <li>Any data, claims, case studies or testimonials you give us to use are accurate and yours
      to use</li>
  <li>You will handle contact details of people who reply in line with applicable data protection
      law, including honouring opt-out requests</li>
</ul>
"""),

    ("Acceptable use of this website", """
<p>You agree to use this website lawfully, and specifically not to:</p>
<ul>
  <li>Use it in any way that breaches applicable law or regulation</li>
  <li>Attempt to gain unauthorised access to any part of the site or its systems</li>
  <li>Interfere with or disrupt the site or the servers behind it</li>
  <li>Use automated systems to extract data from the site without our permission</li>
  <li>Transmit malware, viruses or other harmful code</li>
</ul>
"""),

    ("Intellectual property", """
<p>All content on this website — text, graphics, logos, imagery, code and design — belongs to
{entity} or its licensors and is protected by intellectual property law. You may not reproduce,
distribute, modify or create derivative works from it without our written consent.</p>
<p>Campaign copy, research and messaging frameworks we produce for you under an engagement are
yours to use for your business as set out in that agreement. The underlying methods, tooling and
know-how we use to produce them remain ours.</p>
""".format(entity=ENTITY)),

    ("Confidentiality", """
<p>Each party will keep the other's confidential information confidential and will not disclose it
to third parties without prior written consent, except where required by law. This obligation
survives the end of any engagement.</p>
"""),

    ("Disclaimer of warranties", """
<p>This website and our services are provided "as is" and "as available", without warranties of any
kind, express or implied. We do not warrant that the site will be uninterrupted, error-free or free
of harmful components. While we work hard to deliver results, we make no guarantee of any specific
business outcome.</p>
"""),

    ("Limitation of liability", """
<p>To the fullest extent permitted by law, {entity} is not liable for any indirect, incidental,
special, consequential or punitive damages — including lost profits, lost data or lost business
opportunities — arising from your use of this website or our services, even if we were advised such
damages were possible.</p>
<p>Our total liability for any claim arising out of these Terms or our services will not exceed the
fees you paid us in the twelve (12) months before the claim arose.</p>
<p>Nothing in these Terms excludes or limits liability that cannot lawfully be excluded or limited,
including liability for death or personal injury caused by negligence, or for fraud.</p>
""".format(entity=ENTITY)),

    ("Indemnification", """
<p>You agree to indemnify and hold harmless {entity}, its officers, employees and agents against
claims, liabilities, damages, losses and expenses arising from your breach of these Terms or your
misuse of the website or services.</p>
""".format(entity=ENTITY)),

    ("Governing law and jurisdiction", """
<p>These Terms are governed by {law}. Any dispute arising out of or relating to these Terms or your
use of our website or services is subject to the exclusive jurisdiction of {courts}.</p>
""".format(law=GOVERNING_LAW, courts=COURTS)),

    ("Severability", """
<p>If any provision of these Terms is found unenforceable or invalid, it will be limited or removed
to the minimum extent necessary and the remaining provisions stay in full force.</p>
"""),

    ("Contact us", """
<p>Questions about these Terms:</p>
""" + CONTACT_BLOCK),
]


def write(filename, title, heading, desc, lede, items):
    body = lede + "\n\n" + sections(items)
    page = SHELL.format(title=title, heading=heading, desc=desc, body=body,
                        fonts=FONTS, css=CSS, updated=LAST_UPDATED, email=EMAIL)
    path = os.path.join(ROOT, filename)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(page)
    return filename, len(items)


def build():
    results = [
        write("privacy.html", "Privacy Policy", "Privacy Policy",
              "How Humain Demand collects, uses and protects personal information, "
              "including prospect data used in outbound campaigns.",
              PRIVACY_LEDE, PRIVACY),
        write("terms.html", "Terms &amp; Conditions", "Terms &amp; Conditions",
              "The terms governing use of the Humain Demand website and our "
              "performance-based outbound services.",
              TERMS_LEDE, TERMS),
    ]
    return results


if __name__ == "__main__":
    for name, n in build():
        print("wrote %s (%d sections)" % (name, n))
