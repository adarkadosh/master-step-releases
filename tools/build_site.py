"""Builds the MAS-707 tester guide site into <repo>/docs. Usage: python3 -I build_site.py <repo> <adf.json>"""
import html
import json
import os
import sys

REPO, ADF = sys.argv[1], sys.argv[2]
DOCS = os.path.join(REPO, 'docs')
EMAIL = 'adarbkadosh@gmail.com'

CSS = """
:root{--bg:#f4f7fa;--card:#ffffff;--text:#1f2937;--muted:#4b5563;--line:#e5e7eb;--brand:#047857;--brand-ink:#047857;--brand-soft:#f0fdf4;--brand-soft-ink:#166534;--head-ink:#ffffff;--badge:#d1fae5;--code:#f1f5f9}
@media (prefers-color-scheme:dark){:root{--bg:#0b1220;--card:#111827;--text:#e5e7eb;--muted:#b6bfcc;--line:#263142;--brand:#047857;--brand-ink:#34d399;--brand-soft:#0f2a20;--brand-soft-ink:#bbf7d0;--head-ink:#ffffff;--badge:#d1fae5;--code:#1f2937}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);font:17px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--brand-ink)}
header{background:var(--brand);color:var(--head-ink);padding:28px 16px 32px;text-align:center}
.top{max-width:760px;margin:0 auto 14px;display:flex;justify-content:flex-end}
.lang{color:var(--head-ink);font-weight:700;font-size:16px;text-decoration:none;border:1.5px solid rgba(255,255,255,.7);border-radius:999px;padding:6px 14px;min-height:44px;display:inline-flex;align-items:center}
.brand{font-size:32px;font-weight:800;letter-spacing:-.5px;color:var(--head-ink);text-decoration:none;display:inline-block}
.badge{margin-top:6px;font-size:13px;font-weight:700;color:var(--badge);letter-spacing:2px;text-transform:uppercase}
main{max-width:760px;margin:0 auto;padding:24px 16px 8px}
h1{font-size:28px;line-height:1.25;margin:0 0 10px}
h2{font-size:24px;margin:36px 0 14px;padding-top:8px}
h3{font-size:18px;margin:22px 0 8px}
p{margin:0 0 14px}
.lead{color:var(--muted);font-size:18px}
.note{background:var(--brand-soft);color:var(--brand-soft-ink);border-radius:12px;padding:14px 16px;margin:18px 0}
.note p:last-child{margin:0}
.jump{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0 6px}
.jump a{flex:1 1 140px;text-align:center;background:var(--card);border:1.5px solid var(--line);border-radius:12px;padding:12px;font-weight:700;text-decoration:none;min-height:44px}
ol.steps{list-style:none;padding:0;margin:0;counter-reset:s}
ol.steps>li{counter-increment:s;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 16px 16px 60px;margin:0 0 12px;position:relative}
[dir=rtl] ol.steps>li{padding:16px 60px 16px 16px}
ol.steps>li::before{content:counter(s);position:absolute;top:14px;left:16px;width:32px;height:32px;border-radius:50%;background:var(--brand);color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center;font-size:16px}
[dir=rtl] ol.steps>li::before{left:auto;right:16px}
ol.steps p:last-child{margin-bottom:0}
figure{margin:12px 0 0}
figure img{display:block;max-width:100%;height:auto;border-radius:10px;border:1px solid var(--line)}
/* SmartScreen shots come from a 1x screen: fill the column like the 2x shots beside them */
figure img[src*="win-smartscreen"]{width:100%}
code,.file{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:15px;background:var(--code);border-radius:6px;padding:1px 6px;word-break:break-all}
ul{padding-inline-start:22px;margin:0 0 14px}
footer{max-width:760px;margin:0 auto;padding:24px 16px 40px;color:var(--muted);font-size:16px;display:flex;gap:18px;flex-wrap:wrap;border-top:1px solid var(--line)}
[dir=rtl] .badge{letter-spacing:0;font-size:14px}
footer a{min-height:44px;display:inline-flex;align-items:center}
.notice p{margin:0 0 16px}
bdi.ui{white-space:nowrap}
"""


def page(lang, title, desc, body, switch_href, switch_label, footer, home_href):
    d = 'rtl' if lang == 'he' else 'ltr'
    badge = 'בטא סגורה' if lang == 'he' else 'Closed beta'
    return f"""<!doctype html>
<html lang="{lang}" dir="{d}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta name="robots" content="noindex">
<meta name="description" content="{html.escape(desc)}">
<title>{html.escape(title)}</title>
<style>{CSS}</style>
</head>
<body>
<header>
  <div class="top"><a class="lang" href="{switch_href}" hreflang="{'en' if lang == 'he' else 'he'}" lang="{'en' if lang == 'he' else 'he'}">{switch_label}</a></div>
  <a class="brand" href="{home_href}" dir="ltr">MasterStep</a>
  <div class="badge">{badge}</div>
</header>
<main>
{body}
</main>
<footer>{footer}</footer>
</body>
</html>
"""


def b(s):
    """A UI label exactly as the OS shows it, isolated so it reads right inside RTL text."""
    return f'<b><bdi class="ui">{s}</bdi></b>'


def w(s):
    """A Latin name inside Hebrew text: one unbreakable LTR unit."""
    return f'<bdi class="ui">{s}</bdi>'


def fig(name, alt):
    return f'<figure><img src="../img/{name}" alt="{html.escape(alt)}" loading="lazy"></figure>'


HE_BODY = f"""<h1>התקנת MasterStep</h1>
<p class="lead">מדריך קצר להתקנה ולפתיחה הראשונה.</p>
<div class="note">
<p>גרסת הבטא עדיין לא חתומה, ולכן בפתיחה הראשונה {w('Windows')} או {w('macOS')} יציגו אזהרה. זה צפוי, ועושים את זה רק פעם אחת.</p>
<p>את קישור ההורדה ואת מפתח הרישיון קיבלתם במייל ההזמנה.</p>
</div>
<nav class="jump"><a href="#windows" dir="ltr">Windows</a><a href="#mac" dir="ltr">Mac</a></nav>

<h2 id="windows" dir="rtl">Windows</h2>
<p>משתמשים ב־{w('Chrome')} או ב־{w('Firefox')}? האזהרה על ההורדה נראית שם אחרת. בחרו לשמור את הקובץ, פתחו אותו והמשיכו משלב 4.</p>
<ol class="steps">
<li><p>אם {w('Edge')} כותב שהקובץ לא מוכר ({b("isn't commonly downloaded")}), עמדו עם העכבר על הקובץ, לחצו על שלוש הנקודות ובחרו {b('Keep')}.</p>
{fig('win-edge-keep.webp', 'רשימת ההורדות של Edge, עם שלוש הנקודות והאפשרות Keep מסומנות')}</li>
<li><p>בחלון שנפתח לחצו על החץ שליד {b('Delete')} ובחרו {b('Keep anyway')}.</p>
{fig('win-edge-keep-anyway.webp', 'החלון של Edge, עם החץ שליד Delete והאפשרות Keep anyway מסומנים')}</li>
<li><p>פתחו את הקובץ. ב־{w('Edge')} לוחצים על {b('Open file')}.</p>
{fig('win-download-open.webp', 'רשימת ההורדות של Edge, עם הקישור Open file מסומן')}</li>
<li><p>אם מופיע חלון כחול {b('Windows protected your PC')}, לחצו על {b('More info')}.</p>
{fig('win-smartscreen-more-info.webp', 'החלון הכחול Windows protected your PC, עם הקישור More info מסומן')}</li>
<li><p>מופיע הכפתור {b('Run anyway')}. לחצו עליו.</p>
{fig('win-smartscreen-run-anyway.webp', 'החלון Windows protected your PC אחרי הלחיצה על More info, עם הכפתור Run anyway מסומן')}</li>
<li><p>ההתקנה רצה לבד, בלי שאלות, ולוקחת פחות מדקה. בסופה MasterStep נפתח.</p>
{fig('win-installing.webp', 'חלון ההתקנה של MasterStep בזמן ההתקנה')}</li>
</ol>
<p>אין כפתור {b('Run anyway')}? השיבו למייל ההזמנה ונעזור.</p>

<h2 id="mac" dir="rtl">Mac</h2>
<ol class="steps">
<li><p>פתחו את קובץ ה־{w('DMG')} וגררו את MasterStep לתיקייה {b('Applications')}.</p></li>
<li><p>פתחו את MasterStep מהתיקייה {b('Applications')}. {w('macOS')} יציג הודעה שהוא לא יכול לאמת את האפליקציה. לחצו על {b('Done')}. לא לוחצים על {b('Move to Trash')}.</p>
{fig('mac-not-opened.webp', 'ההודעה MasterStep Not Opened, עם הכפתור Done מסומן')}</li>
<li><p>בתפריט {w('Apple')} בחרו {b('System Settings…')}, ואז {b('Privacy &amp; Security')}. גללו למטה, ובקטע {b('Security')} לחצו על {b('Open Anyway')}.</p>
{fig('mac-apple-menu.webp', 'תפריט Apple, עם System Settings מסומן')}
{fig('mac-open-anyway-settings.webp', 'הקטע Security בהגדרות, עם הכפתור Open Anyway מסומן')}</li>
<li><p>בחלון שנפתח לחצו שוב על {b('Open Anyway')} והקלידו את הסיסמה של המחשב. מעכשיו MasterStep נפתח כרגיל.</p>
{fig('mac-open-anyway-confirm.webp', 'החלון Open MasterStep, עם הכפתור Open Anyway מסומן')}</li>
</ol>
<p>הכפתור {b('Open Anyway')} מופיע רק במשך כשעה מהרגע שניסיתם לפתוח את האפליקציה. לא רואים אותו? פתחו את MasterStep שוב וחזרו להגדרות.</p>
<h3>{w('macOS 14')} או ישן יותר</h3>
<p>בתיקייה {b('Applications')}, לחצו על MasterStep עם הכפתור הימני (או {w('Control')} ולחיצה), בחרו {b('Open')}, ואז לחצו שוב על {b('Open')}.</p>

<h2 id="first-launch">בפתיחה הראשונה</h2>
<ul>
<li>MasterStep מבקש את מפתח הרישיון. העתיקו אותו מהמייל, הדביקו ולחצו על <b>הפעלה</b>. צריך חיבור לאינטרנט.</li>
<li>רוצים לספר לנו משהו? באפליקציה: <b>הגדרות ← אודות ← שליחת משוב</b>.</li>
</ul>
"""

EN_BODY = f"""<h1>Installing MasterStep</h1>
<p class="lead">A short guide to installing and opening the app the first time.</p>
<div class="note">
<p>The beta isn't signed yet, so Windows or macOS shows a warning the first time you open it. That's expected, and you only do this once.</p>
<p>Your download link and license key are in your invite email.</p>
</div>
<nav class="jump"><a href="#windows">Windows</a><a href="#mac">Mac</a></nav>

<h2 id="windows">Windows</h2>
<p>Using Chrome or Firefox? Its download warning looks different. Choose to keep the file, open it, and continue from step 4.</p>
<ol class="steps">
<li><p>If Edge says the file {b("isn't commonly downloaded")}, point at the file, click the three dots and choose {b('Keep')}.</p>
{fig('win-edge-keep.webp', 'The Edge downloads list, with the three dots and Keep marked')}</li>
<li><p>In the window that opens, click the arrow next to {b('Delete')} and choose {b('Keep anyway')}.</p>
{fig('win-edge-keep-anyway.webp', 'The Edge window, with the arrow next to Delete and Keep anyway marked')}</li>
<li><p>Open the file. In Edge, click {b('Open file')}.</p>
{fig('win-download-open.webp', 'The Edge downloads list, with Open file marked')}</li>
<li><p>If a blue {b('Windows protected your PC')} window appears, click {b('More info')}.</p>
{fig('win-smartscreen-more-info.webp', 'The blue Windows protected your PC window, with More info marked')}</li>
<li><p>A {b('Run anyway')} button appears. Click it.</p>
{fig('win-smartscreen-run-anyway.webp', 'The Windows protected your PC window after More info, with Run anyway marked')}</li>
<li><p>The installer runs on its own, with no questions, and takes under a minute. When it's done, MasterStep opens.</p>
{fig('win-installing.webp', 'The MasterStep installer while it installs')}</li>
</ol>
<p>No {b('Run anyway')} button? Reply to your invite email and we'll help.</p>

<h2 id="mac">Mac</h2>
<ol class="steps">
<li><p>Open the DMG file and drag MasterStep into the {b('Applications')} folder.</p></li>
<li><p>Open MasterStep from {b('Applications')}. macOS says it can't verify the app. Click {b('Done')}. Don't click {b('Move to Trash')}.</p>
{fig('mac-not-opened.webp', 'The MasterStep Not Opened message, with Done marked')}</li>
<li><p>From the {w('Apple')} menu, choose {b('System Settings…')}, then {b('Privacy &amp; Security')}. Scroll down, and under {b('Security')} click {b('Open Anyway')}.</p>
{fig('mac-apple-menu.webp', 'The Apple menu, with System Settings marked')}
{fig('mac-open-anyway-settings.webp', 'The Security section in Settings, with Open Anyway marked')}</li>
<li><p>In the window that opens, click {b('Open Anyway')} again and type your Mac password. From now on MasterStep opens like any other app.</p>
{fig('mac-open-anyway-confirm.webp', 'The Open MasterStep window, with Open Anyway marked')}</li>
</ol>
<p>The {b('Open Anyway')} button only stays there for about an hour after you try to open the app. Don't see it? Open MasterStep again, then go back to Settings.</p>
<h3>macOS 14 or older</h3>
<p>In {b('Applications')}, right-click MasterStep (or Control-click it), choose {b('Open')}, then click {b('Open')} again.</p>

<h2 id="first-launch">The first time you open it</h2>
<ul>
<li>MasterStep asks for your license key. Copy it from the email, paste it, and click <b>Activate</b>. You need an internet connection.</li>
<li>Want to tell us something? In the app: <b>Settings → About → Send feedback</b>.</li>
</ul>
"""


def notice_lines(adf_path):
    data = json.load(open(adf_path, encoding='utf-8'))
    out = {}
    for para in data:
        text = ''.join(n['text'] for n in para['content'] if n['type'] == 'text')
        label, *lines = text.split('\n')
        out['he' if label.startswith('HE') else 'en'] = lines
    return out


def notice_html(lines):
    parts = []
    for line in lines:
        esc = html.escape(line, quote=False)
        esc = esc.replace(EMAIL, f'<a href="mailto:{EMAIL}" dir="ltr">{EMAIL}</a>')
        parts.append(f'<p>{esc}</p>')
    return '<div class="notice" id="notice">\n' + '\n'.join(parts) + '\n</div>'


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


notice = notice_lines(ADF)
assert len(notice['he']) == 4 and len(notice['en']) == 4, notice

write(os.path.join(DOCS, 'he/index.html'), page(
    'he', 'התקנת MasterStep', 'איך להתקין ולפתוח את MasterStep בפעם הראשונה ב־Windows וב־Mac.',
    HE_BODY, '../en/', 'English', '<a href="privacy/">פרטיות</a>', './'))
write(os.path.join(DOCS, 'en/index.html'), page(
    'en', 'Installing MasterStep', 'How to install and first open MasterStep on Windows and Mac.',
    EN_BODY, '../he/', 'עברית', '<a href="privacy/">Privacy</a>', './'))
write(os.path.join(DOCS, 'he/privacy/index.html'), page(
    'he', 'פרטיות', 'פרטיות', '<h1>פרטיות</h1>\n' + notice_html(notice['he']),
    '../../en/privacy/', 'English', '<a href="../">התקנת MasterStep</a>', '../'))
write(os.path.join(DOCS, 'en/privacy/index.html'), page(
    'en', 'Privacy', 'Privacy', '<h1>Privacy</h1>\n' + notice_html(notice['en']),
    '../../he/privacy/', 'עברית', '<a href="../">Installing MasterStep</a>', '../'))

ROOT = """<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta name="robots" content="noindex">
<title>MasterStep</title>
<script>
try{var l=(navigator.languages&&navigator.languages[0])||navigator.language||'';location.replace(/^(he|iw)\\b/i.test(l)?'he/':'en/')}catch(e){}
</script>
<style>""" + CSS + """
.pick{display:flex;gap:12px;flex-wrap:wrap;max-width:420px;margin:40px auto;padding:0 16px}
.pick a{flex:1 1 160px;text-align:center;background:var(--card);border:1.5px solid var(--line);border-radius:12px;padding:16px;font-weight:700;font-size:18px;text-decoration:none}
</style>
</head>
<body>
<header><span class="brand" dir="ltr">MasterStep</span></header>
<div class="pick"><a href="he/" lang="he">עברית</a><a href="en/" lang="en" dir="ltr">English</a></div>
</body>
</html>
"""
write(os.path.join(DOCS, 'index.html'), ROOT)
write(os.path.join(DOCS, '.nojekyll'), '')
print('built', DOCS)
