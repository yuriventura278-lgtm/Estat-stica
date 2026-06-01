#!/usr/bin/env python3
"""
Aplica as actualizações visuais aos 5 serviços adicionais:
  • Splash com anel circular de 5 segundos + foto real do hospital
  • Botão de tema claro/escuro com preferência em localStorage
  • Barra de staff (nome do profissional + chefe de turno)
  • Prevenção de FOUC (flash of unstyled content)
"""

import re
import os

UPLOADS = '/root/.claude/uploads/039233f2-2ff9-45a6-bc34-cf6cd2d282ab'
OUT     = '/home/user/Estat-stica/procedimentos'

# (source_file, output_file, service_label, theme_default)
# theme_default: 'light' = page is light by default (add dark mode)
#                'dark'  = page is dark by default (add light mode)
FILES = [
    ('43558ce6-blocooperatorio2.html', 'proc_bloco_operatorio2.html', 'Serviço de Bloco Operatório', 'dark'),
    ('7b3a412c-laboratorio4.html',     'proc_laboratorio.html',       'Serviço de Laboratório',      'light'),
    ('90a3f128-consultaexterna.html',  'proc_consulta_externa2.html', 'Consulta Externa',            'dark_nav'),
    ('ee69e8a1-imagiologia5.html',     'proc_imagiologia.html',       'Serviço de Imagiologia',      'light'),
    ('f2665fdb-fisioterapia111.html',  'proc_fisioterapia.html',      'Serviço de Fisioterapia',     'light'),
]

_CIRC = 263.9  # 2π × 42  (viewBox 100×100, r=42)


# ─── helpers ─────────────────────────────────────────────────────────────────

def extract_hosp_img(content):
    m = re.search(r'src="(data:image/jpeg;base64,[^"]{200,})"', content)
    return m.group(1) if m else 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs='


def make_splash_html(hosp_img, service_label):
    return (
        '<div id="splash">\n'
        '  <div class="splash-inner">\n'
        '    <div class="splash-img-ring">\n'
        '      <div class="splash-img-circle">\n'
        f'        <img src="{hosp_img}" alt="Hospital do Prenda">\n'
        '      </div>\n'
        '      <svg class="splash-progress-svg" viewBox="0 0 100 100">\n'
        '        <circle class="spl-ring-bg" cx="50" cy="50" r="42"/>\n'
        f'        <circle class="spl-ring-fg" id="spl-ring" cx="50" cy="50" r="42"'
        f' stroke-dasharray="{_CIRC}" stroke-dashoffset="{_CIRC}"/>\n'
        '      </svg>\n'
        '    </div>\n'
        '    <p class="splash-hosp-lbl">Hospital do Prenda · Luanda</p>\n'
        f'    <h1 class="splash-svc-lbl">{service_label}</h1>\n'
        '    <div class="splash-pct" id="spl-pct">0%</div>\n'
        '  </div>\n'
        '</div>'
    )


SPLASH_CSS = '''
/* ── SPLASH RING ── */
#splash{position:fixed;inset:0;z-index:9999;background:var(--bg,#0c0f14);
  display:flex;align-items:center;justify-content:center;}
.splash-inner{display:flex;flex-direction:column;align-items:center;text-align:center;gap:14px;}
.splash-img-ring{position:relative;width:100px;height:100px;flex-shrink:0;}
.splash-img-circle{position:absolute;inset:8px;border-radius:50%;overflow:hidden;background:#1a2a3a;}
.splash-img-circle img{width:100%;height:100%;object-fit:cover;}
.splash-progress-svg{position:absolute;inset:0;width:100px;height:100px;transform:rotate(-90deg);}
.spl-ring-bg{fill:none;stroke:rgba(255,255,255,.12);stroke-width:4;}
.spl-ring-fg{fill:none;stroke:#00d4aa;stroke-width:4;stroke-linecap:round;}
.splash-hosp-lbl{font-size:.55rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;
  color:rgba(200,230,220,.65);font-family:var(--font-head,var(--fh,Inter,sans-serif));}
.splash-svc-lbl{font-size:.95rem;font-weight:700;color:#fff;max-width:300px;line-height:1.35;
  font-family:var(--font-head,var(--fh,Inter,sans-serif));}
.splash-pct{font-size:.65rem;color:#00d4aa;font-weight:600;letter-spacing:.05em;
  font-family:var(--font-body,var(--fb,monospace));}
'''

SPLASH_RING_JS = r'''
// ── SPLASH RING ──
(function(){
  var DURATION=5000,ring=document.getElementById('spl-ring'),
      pct=document.getElementById('spl-pct'),CIRC=263.9,start=null;
  if(!ring)return;
  function step(ts){
    if(!start)start=ts;
    var p=Math.min((ts-start)/DURATION,1);
    var e=p<.5?2*p*p:-1+(4-2*p)*p;
    ring.style.strokeDashoffset=CIRC*(1-e);
    if(pct)pct.textContent=Math.round(e*100)+'%';
    if(p<1){requestAnimationFrame(step);return;}
    var s=document.getElementById('splash');
    if(s){s.style.transition='opacity .45s';s.style.opacity='0';
      setTimeout(function(){s.style.display='none';},450);}
  }
  requestAnimationFrame(step);
})();
'''

STAFF_JS = r'''
// ── STAFF INFO ──
function loadStaffInfo(){
  var raw=localStorage.getItem('_staff');var d=raw?JSON.parse(raw):{};
  var pi=document.getElementById('inp-profissional');
  var ci=document.getElementById('inp-chefe');
  if(pi)pi.value=d.profissional||'';if(ci)ci.value=d.chefe||'';
}
function saveStaffInfo(){
  var pi=document.getElementById('inp-profissional');
  var ci=document.getElementById('inp-chefe');
  localStorage.setItem('_staff',JSON.stringify({
    profissional:pi?pi.value.trim():'',chefe:ci?ci.value.trim():''}));
}
setTimeout(loadStaffInfo,80);
'''


def staff_bar_html():
    return (
        '<div class="hp-staff-bar" id="hp-staff-bar">'
        '<span class="hp-staff-lbl">Profissional</span>'
        '<input type="text" id="inp-profissional" class="hp-staff-inp" '
        'placeholder="Nome do profissional" autocomplete="name" oninput="saveStaffInfo()">'
        '<span class="hp-staff-sep">·</span>'
        '<span class="hp-staff-lbl">Chefe de Turno</span>'
        '<input type="text" id="inp-chefe" class="hp-staff-inp" '
        'placeholder="Nome do chefe de turno" autocomplete="name" oninput="saveStaffInfo()">'
        '</div>'
    )


def staff_bar_css(staff_h=38, header_h_var='var(--header-h)', bg='rgba(0,100,80,.15)',
                  border='rgba(0,212,170,.2)', label_color='rgba(110,231,183,.7)',
                  inp_color='#e8f4f0', inp_border='rgba(0,212,170,.3)'):
    return f'''
/* ── STAFF BAR ── */
.hp-staff-bar{{position:fixed;top:{header_h_var};left:0;right:0;z-index:190;
  height:{staff_h}px;background:{bg};border-bottom:1px solid {border};
  display:flex;align-items:center;gap:12px;padding:0 20px;}}
.hp-staff-lbl{{font-size:.48rem;color:{label_color};font-weight:600;
  text-transform:uppercase;letter-spacing:1.5px;white-space:nowrap;
  font-family:var(--font-head,var(--fh,'Inter',sans-serif));}}
.hp-staff-sep{{color:{inp_border};font-size:.8rem;margin:0 2px;}}
.hp-staff-inp{{background:transparent;border:none;border-bottom:1px solid {inp_border};
  color:{inp_color};font-family:var(--font-head,var(--fh,'Inter',sans-serif));
  font-size:.68rem;padding:2px 6px;outline:none;min-width:150px;max-width:210px;
  transition:border-color .13s;}}
.hp-staff-inp::placeholder{{opacity:.5;}}
.hp-staff-inp:focus{{border-bottom-color:rgba(0,212,170,.8);}}
'''


# ─── per-theme extras ─────────────────────────────────────────────────────────

# For LIGHT default pages (fisio, imag, lab): add dark mode + light staff bar
DARK_MODE_LIGHT_PAGES = '''
/* ── DARK MODE ── */
html.dark{
  --bg:#0c0f14!important;--surface:#141820!important;--surface2:#0f1520!important;
  --border:#1e2840!important;--text:#e2e8f0!important;--muted:#64748b!important;
}
html.dark body{background:#0c0f14!important;color:#e2e8f0!important;}
html.dark header{background:#141820!important;border-bottom-color:#1e2840!important;}
html.dark .sidebar{background:#141820!important;border-right-color:#1e2840!important;}
html.dark .card,html.dark .table-container{background:#141820!important;border-color:#1e2840!important;}
html.dark input,html.dark select,html.dark textarea{
  background:#0f1520!important;color:#e2e8f0!important;border-color:#1e2840!important;}
html.dark .hp-staff-bar{background:rgba(30,40,64,.85)!important;border-bottom-color:#1e2840!important;}
html.dark .hp-staff-inp{color:#e2e8f0!important;border-bottom-color:#1e2840!important;}
html.dark .hp-staff-lbl{color:#64748b!important;}
html.dark #theme-toggle{color:#60a5fa!important;}
'''

DARK_TOGGLE_JS_LIGHT = r'''
// ── THEME TOGGLE (light default) ──
function toggleTheme(){
  var dark=document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme',dark?'dark':'light');
  var btn=document.getElementById('theme-toggle');
  if(btn)btn.title=dark?'Mudar para tema claro':'Mudar para tema escuro';
}
'''

FOUC_LIGHT = '<script>if(localStorage.getItem("theme")==="dark")document.documentElement.classList.add("dark");</script>'


# For DARK default page (bloco_op): add light mode
LIGHT_MODE_DARK_PAGES = '''
/* ── LIGHT MODE ── */
html.light{
  --bg:#f8fafc!important;--surface:#ffffff!important;--surface2:#f1f5f9!important;
  --border:#e2e8f0!important;--text:#0f172a!important;--muted:#64748b!important;
}
html.light body{background:#f8fafc!important;color:#0f172a!important;}
html.light header,.html.light header{
  background:#ffffff!important;border-bottom:1px solid #e2e8f0!important;}
html.light .sidebar{background:#ffffff!important;border-right-color:#e2e8f0!important;}
html.light .card{background:#ffffff!important;border-color:#e2e8f0!important;}
html.light input,html.light select,html.light textarea{
  background:#ffffff!important;color:#0f172a!important;border-color:#e2e8f0!important;}
html.light .hp-staff-bar{background:oklch(97% .01 155)!important;border-bottom-color:#e2e8f0!important;}
html.light .hp-staff-inp{color:#0f172a!important;border-bottom-color:#e2e8f0!important;}
html.light .hp-staff-lbl{color:#6b7280!important;}
html.light #theme-toggle{color:#0f172a!important;}
'''

LIGHT_TOGGLE_JS_DARK = r'''
// ── THEME TOGGLE (dark default) ──
function toggleTheme(){
  var light=document.documentElement.classList.toggle('light');
  localStorage.setItem('theme',light?'light':'dark');
  var btn=document.getElementById('theme-toggle');
  if(btn)btn.title=light?'Mudar para tema escuro':'Mudar para tema claro';
}
'''

FOUC_DARK = '<script>if(localStorage.getItem("theme")==="light")document.documentElement.classList.add("light");</script>'


# For consulta externa (dark nav, light content)
DARK_MODE_DARK_NAV = '''
/* ── DARK MODE ── */
html.dark .main{background:#0c0f14!important;color:#e2e8f0!important;}
html.dark .layout{background:#0c0f14!important;}
html.dark .card,html.dark [class*="card"],html.dark .table-container{
  background:#141820!important;border-color:#1e2840!important;}
html.dark input,html.dark select,html.dark textarea{
  background:#0f1520!important;color:#e2e8f0!important;border-color:#1e2840!important;}
html.dark .hp-staff-bar{background:rgba(0,50,80,.9)!important;border-bottom-color:rgba(6,182,212,.25)!important;}
html.dark .hp-staff-inp{color:#e2e8f0!important;}
html.dark .hp-staff-lbl{color:#94a3b8!important;}
html.dark #theme-toggle{color:#06b6d4!important;}
'''

FOUC_DARK_NAV = '<script>if(localStorage.getItem("theme")==="dark")document.documentElement.classList.add("dark");</script>'

DARK_TOGGLE_JS_DARK_NAV = r'''
// ── THEME TOGGLE (dark nav) ──
function toggleTheme(){
  var dark=document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme',dark?'dark':'light');
}
'''


# ─── SVG icons for buttons ────────────────────────────────────────────────────

SVG_MOON = '<svg style="display:inline-block;width:13px;height:13px;stroke:currentColor;fill:none;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round;vertical-align:-2px"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
SVG_SUN  = '<svg style="display:inline-block;width:13px;height:13px;stroke:currentColor;fill:none;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round;vertical-align:-2px"><circle cx="12" cy="12" r="4"/><line x1="12" y1="2" x2="12" y2="4"/><line x1="12" y1="20" x2="12" y2="22"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="2" y1="12" x2="4" y2="12"/><line x1="20" y1="12" x2="22" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'


# ─── main transformer ─────────────────────────────────────────────────────────

def transform(content, service_label, theme_default):
    hosp_img = extract_hosp_img(content)
    new_splash = make_splash_html(hosp_img, service_label)

    # ── 1. Replace / inject splash ──────────────────────────────────────────
    if 'id="splash"' in content:
        # Replace existing splash (everything from <div id="splash"> up to just before <header> or <div class="layout">)
        content = re.sub(
            r'<div id="splash">.*?(?=\n<header>|\n\n<header>|\n<div class="layout">|\n<div id="app)',
            new_splash,
            content,
            flags=re.DOTALL
        )
    else:
        # consulta externa — inject splash at start of body
        content = content.replace('<body>\n', f'<body>\n{new_splash}\n', 1)
        if '<body>\n' + new_splash not in content:
            content = content.replace('<body>', f'<body>\n{new_splash}', 1)

    # ── 2. Inject splash CSS (replace existing splash CSS block or append) ──
    # Remove the auto-hide animation from #splash (critical — would fight our 5s ring)
    content = re.sub(r'\s*animation\s*:\s*splashFadeOut[^;]+;', '', content)
    # Remove all old @keyframes for splash animations
    content = re.sub(r'@keyframes\s+splashFadeOut\s*\{[^}]+\}', '', content)
    content = re.sub(r'@keyframes\s+splashRing\s*\{[^}]+\}', '', content)
    content = re.sub(r'@keyframes\s+splashProgress\s*\{[^}]+\}', '', content)
    # Hide old splash sub-elements (they'll be replaced by our new HTML)
    OLD_SPLASH_CLASSES = (
        r'\.(splash-logo-wrap|splash-logo-ring|splash-logo-img|splash-logo|splash-hospital|'
        r'splash-name|splash-country|splash-divider|splash-dept|splash-title|splash-sub|'
        r'splash-service|splash-bar-wrap|splash-bar|splash-timer|splash-mark|splash-rule|'
        r'splash-inner|splash-hosp-lbl|splash-svc-lbl|splash-pct)'
        r'\s*\{[^}]+\}'
    )
    content = re.sub(OLD_SPLASH_CLASSES, '', content)
    # Add new splash CSS just before </style>
    content = content.replace('</style>', SPLASH_CSS + '</style>', 1)

    # ── 3. Theme CSS + staff bar CSS ────────────────────────────────────────
    if theme_default == 'light':
        extra_css = DARK_MODE_LIGHT_PAGES
        staff_css = staff_bar_css(
            header_h_var='var(--header-h)',
            bg='oklch(97% .01 200)',
            border='oklch(89% .02 200)',
            label_color='var(--muted,#64748b)',
            inp_color='var(--text,#0f172a)',
            inp_border='oklch(85% .02 200)'
        )
    elif theme_default == 'dark':
        extra_css = LIGHT_MODE_DARK_PAGES
        staff_css = staff_bar_css()  # dark defaults
    else:  # dark_nav (consulta externa)
        extra_css = DARK_MODE_DARK_NAV
        staff_css = staff_bar_css(
            header_h_var='62px',
            bg='rgba(10,22,40,.95)',
            border='rgba(255,255,255,.08)',
            label_color='rgba(148,163,184,.8)',
            inp_color='#e2e8f0',
            inp_border='rgba(255,255,255,.2)'
        )

    content = content.replace('</style>', extra_css + staff_css + '</style>', 1)

    # ── 4. FOUC prevention in <head> ────────────────────────────────────────
    if theme_default == 'light' or theme_default == 'dark_nav':
        fouc = FOUC_LIGHT
    else:
        fouc = FOUC_DARK
    content = content.replace('</head>', fouc + '\n</head>', 1)

    # ── 5. Theme toggle button in header ────────────────────────────────────
    if theme_default == 'dark':
        icon = SVG_SUN
        title = 'Mudar para tema claro'
    else:
        icon = SVG_MOON
        title = 'Mudar para tema escuro'

    theme_btn = (
        f'<button id="theme-toggle" onclick="toggleTheme()" title="{title}" '
        f'style="padding:5px 11px;border-radius:4px;cursor:pointer;background:transparent;'
        f'border:1px solid rgba(255,255,255,.2);color:inherit;font-size:.57rem;font-weight:600;'
        f'letter-spacing:.4px;text-transform:uppercase;display:inline-flex;align-items:center;'
        f'gap:5px;white-space:nowrap;">'
        f'{icon} Tema</button>'
    )

    # Try header-right first, then topbar-right
    for btn_area in ['<div class="header-right">', '<div class="topbar-right">']:
        if btn_area in content:
            content = content.replace(btn_area, btn_area + '\n    ' + theme_btn, 1)
            break

    # ── 6. Staff bar injection ───────────────────────────────────────────────
    sb = staff_bar_html()
    if theme_default == 'dark_nav':
        # After closing </div> of topbar div
        content = content.replace('</div>\n\n<div class="sidebar-overlay"',
                                  f'</div>\n{sb}\n<div class="sidebar-overlay"', 1)
        # Shift sidebar top and layout min-height
        content = content.replace('top: 62px;', 'top: 100px;')
        content = content.replace('min-height: calc(100vh - 62px)', 'min-height: calc(100vh - 100px)')
    else:
        # After </header>
        content = content.replace('\n<header>', '\n' + sb + '\n<header>', 1)
        # Adjust sidebar and main-content top offsets
        content = content.replace(
            'top:var(--header-h);', 'top:calc(var(--header-h) + 38px);')
        content = content.replace(
            'top: var(--header-h);', 'top: calc(var(--header-h) + 38px);')
        content = content.replace(
            'padding-top:var(--header-h)', 'padding-top:calc(var(--header-h) + 38px)')
        content = content.replace(
            'padding-top: var(--header-h)', 'padding-top: calc(var(--header-h) + 38px)')

    # ── 7. Inject JS before </body> ──────────────────────────────────────────
    if theme_default == 'light':
        toggle_js = DARK_TOGGLE_JS_LIGHT
    elif theme_default == 'dark':
        toggle_js = LIGHT_TOGGLE_JS_DARK
    else:
        toggle_js = DARK_TOGGLE_JS_DARK_NAV

    inject_js = (
        '<script>\n'
        + SPLASH_RING_JS
        + STAFF_JS
        + toggle_js
        + '</script>\n'
        '</body>'
    )
    content = content.replace('</body>', inject_js, 1)

    return content


# ─── execution ────────────────────────────────────────────────────────────────

os.makedirs(OUT, exist_ok=True)

for src_name, out_name, label, theme in FILES:
    src_path = os.path.join(UPLOADS, src_name)
    out_path = os.path.join(OUT, out_name)
    print(f'A processar {src_name}…')
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = transform(content, label, theme)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  ✓  {out_name}')

print(f'\n✓ {len(FILES)} ficheiros gerados em {OUT}/')
