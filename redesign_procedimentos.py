#!/usr/bin/env python3
"""
Redesign visual + split: sistema clínico minimalista.
Gera 13 ficheiros HTML na pasta procedimentos/.
"""

import re
import os

SRC = '/root/.claude/uploads/3a8471dc-f72f-4823-898f-e3c8c807de9c/ef7cf93c-procedimentov62.html'
OUT = '/home/user/Estat-stica/procedimentos'

# ─────────────────────────────────────────────────────────────────────────────
# SVG SPRITE — 24 ícones de linha
# ─────────────────────────────────────────────────────────────────────────────
SVG_SPRITE = '''<svg id="svg-sprite" xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">
  <!-- Serviços -->
  <symbol id="i-bone" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="5.5" cy="5.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>
    <line x1="7.5" y1="7.5" x2="16.5" y2="16.5"/>
    <circle cx="18.5" cy="5.5" r="2.5"/><circle cx="5.5" cy="18.5" r="2.5"/>
    <line x1="16.5" y1="7.5" x2="7.5" y2="16.5"/>
  </symbol>
  <symbol id="i-bed" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M3 7v11M3 18h18M21 18v-5a2 2 0 0 0-2-2H7v7"/><path d="M3 12h18M8 12V9a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v3"/>
  </symbol>
  <symbol id="i-heart" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7z"/>
    <path d="M3.22 12H9.5l1.5-3 2 6 1.5-3h4.28"/>
  </symbol>
  <symbol id="i-scalpel" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M5 3h4l10 10-4 4L5 7z"/><path d="M5 3l2 2M13 17l2-2"/>
    <circle cx="17.5" cy="6.5" r="2.5"/>
  </symbol>
  <symbol id="i-tooth" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M12 2C9 2 6 4 6 7c0 2 .8 3.5 1 5.5S6 18 7 21h2c.5-2 1-4.5 3-4.5S15 19 15.5 21H18c1-3 .8-6 1-8.5S18 9 18 7c0-3-3-5-6-5z"/>
  </symbol>
  <symbol id="i-lamp" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="4"/>
    <line x1="12" y1="2" x2="12" y2="5"/><line x1="12" y1="19" x2="12" y2="22"/>
    <line x1="4.22" y1="4.22" x2="6.34" y2="6.34"/><line x1="17.66" y1="17.66" x2="19.78" y2="19.78"/>
    <line x1="2" y1="12" x2="5" y2="12"/><line x1="19" y1="12" x2="22" y2="12"/>
    <line x1="4.22" y1="19.78" x2="6.34" y2="17.66"/><line x1="17.66" y1="6.34" x2="19.78" y2="4.22"/>
  </symbol>
  <symbol id="i-clipboard" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <rect x="9" y="2" width="6" height="4" rx="1"/>
    <path d="M9 4H5a1 1 0 0 0-1 1v15a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1h-4"/>
    <line x1="9" y1="12" x2="15" y2="12"/><line x1="9" y1="16" x2="13" y2="16"/>
  </symbol>
  <symbol id="i-droplet" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>
  </symbol>
  <symbol id="i-calendar" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <rect x="3" y="4" width="18" height="18" rx="2"/>
    <line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/>
    <line x1="3" y1="10" x2="21" y2="10"/>
    <circle cx="8" cy="14" r=".5" fill="currentColor"/><circle cx="12" cy="14" r=".5" fill="currentColor"/>
    <circle cx="16" cy="14" r=".5" fill="currentColor"/><circle cx="8" cy="18" r=".5" fill="currentColor"/>
    <circle cx="12" cy="18" r=".5" fill="currentColor"/>
  </symbol>
  <symbol id="i-brain" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96-.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24A2.5 2.5 0 0 1 9.5 2z"/>
    <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96-.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24A2.5 2.5 0 0 0 14.5 2z"/>
  </symbol>
  <symbol id="i-ear" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M6 8.5a6 6 0 1 1 11.5 2.3c-.6 1.4-1.5 2.2-2.5 3.7-.7 1-1 2.5-1 3.5M9 15c.5 1 1.5 2 3 2a3 3 0 0 0 3-3"/>
  </symbol>
  <symbol id="i-cross-sq" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <rect x="3" y="3" width="18" height="18" rx="3"/>
    <line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/>
  </symbol>
  <symbol id="i-pill" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="m10.5 20.5-7-7a5 5 0 0 1 7-7l7 7a5 5 0 0 1-7 7z"/>
    <line x1="8.5" y1="8.5" x2="15.5" y2="15.5"/>
  </symbol>
  <!-- UI -->
  <symbol id="i-save" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
    <polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/>
  </symbol>
  <symbol id="i-pdf" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
    <polyline points="14 2 14 8 20 8"/>
    <line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>
    <polyline points="10 9 9 9 8 9"/>
  </symbol>
  <symbol id="i-download" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
    <polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>
  </symbol>
  <symbol id="i-upload" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
    <polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>
  </symbol>
  <symbol id="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="4"/>
    <line x1="12" y1="2" x2="12" y2="4"/><line x1="12" y1="20" x2="12" y2="22"/>
    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
    <line x1="2" y1="12" x2="4" y2="12"/><line x1="20" y1="12" x2="22" y2="12"/>
    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
  </symbol>
  <symbol id="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
  </symbol>
  <symbol id="i-sigma" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <polyline points="18 4 6 4 12 12 6 20 18 20"/>
  </symbol>
  <symbol id="i-chart" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/>
    <line x1="6" y1="20" x2="6" y2="14"/><line x1="2" y1="20" x2="22" y2="20"/>
  </symbol>
  <symbol id="i-notes" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
    <polyline points="14 2 14 8 20 8"/>
    <line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>
    <line x1="10" y1="9" x2="8" y2="9"/>
  </symbol>
  <symbol id="i-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <polyline points="20 6 9 17 4 12"/>
  </symbol>
  <symbol id="i-info" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="10"/>
    <line x1="12" y1="8" x2="12" y2="8"/><line x1="12" y1="12" x2="12" y2="16"/>
  </symbol>
  <symbol id="i-shuffle" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/>
    <polyline points="21 16 21 21 16 21"/><line x1="15" y1="15" x2="21" y2="21"/>
    <line x1="4" y1="4" x2="9" y2="9"/>
  </symbol>
</svg>'''

# ─────────────────────────────────────────────────────────────────────────────
# HELPER — inline SVG use tag
# ─────────────────────────────────────────────────────────────────────────────
def icon(name):
    return f'<svg class="svc-icon" aria-hidden="true"><use href="#{name}"/></svg>'

# ─────────────────────────────────────────────────────────────────────────────
# NOVO CSS — clínico minimalista
# ─────────────────────────────────────────────────────────────────────────────
NEW_CSS = '''<style>
/* ════ CLINICAL MINIMAL v1 ════ */
:root{
  --bg:#fafaf9;--surface:#ffffff;
  --border:oklch(92% 0.003 50);
  --text:#0a0a0a;--muted:#6b6b6b;
  --accent:oklch(45% 0.08 230);
  --accent-tint:oklch(97% 0.01 230);
  --accent-ring:oklch(89% 0.03 230);
  /* compat */
  --accent2:var(--muted);--surface2:#f5f5f4;
  --danger:#c0392b;--warn:#b45309;
  --green:#047857;--purple:#5b21b6;--orange:#c2410c;
  --font-head:'Inter',sans-serif;
  --font-body:'IBM Plex Mono',monospace;
  --nav-w:220px;--hdr-h:56px;
}

/* SVG ICON HELPERS */
.svc-icon{display:inline-block;width:13px;height:13px;stroke:currentColor;fill:none;
  stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round;vertical-align:-2px;flex-shrink:0;}
.ni-icon{display:flex;align-items:center;justify-content:center;width:18px;height:18px;color:var(--muted);}
.ni-icon .svc-icon{width:15px;height:15px;}
.nav-item.active .ni-icon,.nav-item:hover .ni-icon{color:var(--accent);}
.spec-hdr-icon{display:flex;align-items:center;justify-content:center;
  width:36px;height:36px;border-radius:8px;background:var(--accent-tint);border:1px solid var(--accent-ring);flex-shrink:0;}
.spec-hdr-icon .svc-icon{width:22px;height:22px;color:var(--accent);}
.btn-h .svc-icon{width:13px;height:13px;vertical-align:-1px;}
.card-label .svc-icon{width:12px;height:12px;}
.tl .svc-icon,.tot-lbl .svc-icon,.sum-label .svc-icon{width:11px;height:11px;vertical-align:-1px;}
.med-notice .svc-icon{width:14px;height:14px;flex-shrink:0;margin-top:1px;color:var(--accent);}
.sync-info .svc-icon{width:12px;height:12px;color:var(--green);}

/* SPLASH */
#splash{position:fixed;inset:0;z-index:9999;background:#fff;
  display:flex;align-items:center;justify-content:center;
  animation:splashOut .35s ease forwards 1.5s;}
@keyframes splashOut{from{opacity:1}to{opacity:0;visibility:hidden;pointer-events:none}}
.splash-inner{display:flex;flex-direction:column;align-items:center;text-align:center;}
.splash-mark{width:44px;height:44px;border-radius:9px;background:var(--accent);color:#fff;
  font-family:var(--font-head);font-size:1rem;font-weight:800;letter-spacing:-.5px;
  display:flex;align-items:center;justify-content:center;margin-bottom:18px;}
.splash-hosp-lbl{font-family:var(--font-head);font-size:.55rem;font-weight:600;
  letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-bottom:6px;}
.splash-svc-lbl{font-family:var(--font-head);font-size:.95rem;font-weight:700;color:var(--text);
  margin-bottom:18px;max-width:300px;line-height:1.35;}
.splash-rule{width:28px;height:1.5px;background:var(--accent);
  animation:splashRule .5s ease forwards .3s;transform:scaleX(0);transform-origin:left;}
@keyframes splashRule{to{transform:scaleX(1)}}
/* esconde elementos do splash original */
.splash-logo-wrap,.splash-hospital,.splash-name,.splash-country,.splash-divider,
.splash-dept,.splash-title,.splash-sub,.splash-service,.splash-bar-wrap,.splash-timer{display:none!important;}

*{margin:0;padding:0;box-sizing:border-box;}
body{background:var(--bg);color:var(--text);font-family:var(--font-body);min-height:100vh;overflow-x:hidden;}

/* HEADER */
header{position:fixed;top:0;left:0;right:0;z-index:200;height:var(--hdr-h);padding:0 20px;
  background:var(--surface);border-bottom:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;gap:8px;}
.logo-area{display:flex;align-items:center;gap:10px;flex-shrink:0;}
.logo-text h1{font-family:var(--font-head);font-size:.88rem;font-weight:700;color:var(--accent);}
.logo-text p{font-size:.46rem;color:var(--muted);text-transform:uppercase;letter-spacing:2px;margin-top:1px;}
.hdr-right{display:flex;align-items:center;gap:6px;flex-wrap:wrap;}
.hdr-date{display:flex;align-items:center;gap:6px;}
.hdr-date label{font-size:.5rem;text-transform:uppercase;letter-spacing:2px;color:var(--muted);}
.hdr-date input[type=date]{background:var(--surface);border:1px solid var(--border);color:var(--text);
  font-family:var(--font-body);font-size:.68rem;padding:4px 8px;border-radius:4px;outline:none;cursor:pointer;}
.hdr-date input[type=date]:focus{border-color:var(--accent);}
.date-disp{font-size:.66rem;color:var(--accent);font-family:var(--font-head);font-weight:600;white-space:nowrap;}
.btn-h{padding:5px 11px;border-radius:4px;cursor:pointer;font-family:var(--font-head);font-size:.57rem;
  font-weight:600;letter-spacing:.4px;text-transform:uppercase;transition:all .13s;white-space:nowrap;border:none;
  display:inline-flex;align-items:center;gap:5px;}
.btn-save{background:var(--accent);color:#fff;}
.btn-save:hover{opacity:.83;}
.btn-out{background:transparent;border:1px solid var(--border)!important;color:var(--muted);}
.btn-out:hover{border-color:var(--accent)!important;color:var(--accent);}
.sync-info{font-size:.53rem;color:var(--green);
  background:oklch(97% 0.01 155);border:1px solid oklch(91% 0.02 155);
  padding:3px 8px;border-radius:4px;white-space:nowrap;display:inline-flex;align-items:center;gap:4px;}

/* LAYOUT */
.app-shell{display:flex;padding-top:var(--hdr-h);min-height:100vh;}

/* SIDEBAR */
.sidebar{position:fixed;top:var(--hdr-h);left:0;bottom:0;width:var(--nav-w);
  background:var(--surface);border-right:1px solid var(--border);
  overflow-y:auto;z-index:100;display:flex;flex-direction:column;}
.sidebar::-webkit-scrollbar{width:3px;}
.sidebar::-webkit-scrollbar-thumb{background:var(--border);}
.sb-hdr{padding:10px 14px 8px;border-bottom:1px solid var(--border);position:sticky;top:0;background:var(--surface);}
.sb-hdr span{font-family:var(--font-head);font-size:.48rem;font-weight:600;text-transform:uppercase;letter-spacing:2.5px;color:var(--muted);}
.nav-list{padding:6px 8px;display:flex;flex-direction:column;gap:1px;}
.nav-item{display:flex;align-items:center;gap:8px;padding:6px 10px;border-radius:5px;
  cursor:pointer;transition:background .12s;user-select:none;border:1px solid transparent;}
.nav-item:hover{background:var(--accent-tint);}
.nav-item.active{background:var(--accent-tint);border-color:var(--accent-ring);}
.nav-item .ni-label{font-family:var(--font-head);font-size:.56rem;font-weight:500;text-transform:uppercase;
  letter-spacing:.7px;color:var(--muted);transition:color .12s;}
.nav-item.active .ni-label,.nav-item:hover .ni-label{color:var(--accent);}
.nav-item .ni-badge{margin-left:auto;min-width:18px;height:16px;background:var(--accent-tint);
  border:1px solid var(--accent-ring);border-radius:8px;padding:0 4px;
  font-size:.49rem;font-weight:700;color:var(--accent);display:none;align-items:center;justify-content:center;}
.ni-badge.on{display:flex;}
.sb-divider{margin:4px 10px;border:none;border-top:1px solid var(--border);}
.sb-sec{padding:6px 14px 2px;font-size:.46rem;text-transform:uppercase;letter-spacing:2px;
  color:var(--muted);font-family:var(--font-head);font-weight:600;}
.nav-item.rpt.active{background:var(--accent-tint);border-color:var(--accent-ring);}
.nav-item.rpt.active .ni-label{color:var(--accent);}

/* MAIN */
.main-content{margin-left:var(--nav-w);flex:1;padding:28px 32px 80px;}

/* SECTIONS */
.section{display:none;animation:fadeIn .16s ease;}
.section.active{display:block;}
@keyframes fadeIn{from{opacity:0;transform:translateY(3px)}to{opacity:1;transform:translateY(0)}}

/* SPEC HEADER */
.spec-hdr{display:flex;align-items:center;gap:12px;margin-bottom:24px;padding-bottom:14px;border-bottom:1px solid var(--border);}
.spec-hdr h2{font-family:var(--font-head);font-size:1.1rem;font-weight:700;color:var(--text);}
.spec-hdr p{font-size:.5rem;color:var(--muted);text-transform:uppercase;letter-spacing:2px;margin-top:2px;}
.spec-totals{margin-left:auto;display:flex;gap:8px;}
.tot-box{border-radius:5px;padding:8px 12px;text-align:center;flex-shrink:0;}
.tot-box.day{background:var(--accent-tint);border:1px solid var(--accent-ring);}
.tot-box.night{background:#f7f7f7;border:1px solid #e8e8e8;}
.tot-box.grand{background:oklch(96% 0.02 230);border:1px solid oklch(89% 0.04 230);}
.tot-lbl{font-size:.45rem;text-transform:uppercase;letter-spacing:1.5px;font-family:var(--font-head);
  font-weight:600;display:flex;align-items:center;justify-content:center;gap:3px;margin-bottom:3px;color:var(--muted);}
.tot-val{font-size:1.35rem;font-weight:300;color:var(--text);line-height:1;font-family:var(--font-body);}

/* CARD */
.card{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:18px;margin-bottom:14px;}
.card-label{font-family:var(--font-head);font-size:.5rem;font-weight:600;text-transform:uppercase;
  letter-spacing:2px;color:var(--muted);margin-bottom:12px;display:flex;align-items:center;gap:5px;}

/* PROC TABLE */
.proc-table{width:100%;border-collapse:collapse;}
.proc-table-head{display:grid;grid-template-columns:1fr 82px 82px 64px;gap:0;
  padding:5px 8px;border-bottom:1px solid var(--border);margin-bottom:4px;}
.proc-table-head span{font-family:var(--font-head);font-size:.46rem;font-weight:600;text-transform:uppercase;
  letter-spacing:1.5px;text-align:center;color:var(--muted);
  display:flex;align-items:center;justify-content:center;gap:3px;}
.proc-table-head .ph-name{text-align:left;justify-content:flex-start;}
.proc-table-head .ph-dia{color:var(--accent);}
.proc-row{display:grid;grid-template-columns:1fr 82px 82px 64px;gap:0;align-items:center;
  border-bottom:1px solid var(--border);transition:background .1s;}
.proc-row:hover{background:oklch(98.5% 0.003 230);}
.proc-row:last-child{border-bottom:none;}
.proc-name{padding:5px 8px;font-size:.87rem;font-family:var(--font-head);font-weight:400;
  color:var(--text);line-height:1.35;}
.proc-cell{padding:3px 5px;display:flex;flex-direction:column;align-items:center;gap:1px;}
.proc-cell input[type=number]{width:70px;background:var(--surface);border:1px solid var(--border);
  border-radius:4px;color:var(--text);font-family:var(--font-body);font-size:.9rem;font-weight:400;
  padding:4px 2px;outline:none;text-align:center;-moz-appearance:textfield;transition:border-color .12s;}
.proc-cell input[type=number]::-webkit-outer-spin-button,
.proc-cell input[type=number]::-webkit-inner-spin-button{-webkit-appearance:none;}
.proc-cell input[type=number]:focus{border-color:var(--accent);}
.proc-cell input.night-inp:focus{border-color:#999;}
.proc-cell input[readonly]{opacity:.35;cursor:not-allowed;background:var(--bg);}
.proc-total-val{font-size:.92rem;font-weight:600;color:var(--text);text-align:center;
  min-width:40px;font-family:var(--font-body);}

/* TOTAL BAR */
.total-bar{display:grid;grid-template-columns:repeat(auto-fit,minmax(100px,1fr));gap:8px;
  margin-top:12px;padding-top:12px;border-top:1px solid var(--border);}
.t-box{background:var(--accent-tint);border:1px solid var(--accent-ring);border-radius:5px;padding:9px;text-align:center;}
.t-box.night{background:#f7f7f7;border-color:#e8e8e8;}
.t-box.grand{background:oklch(96% 0.02 230);border-color:oklch(89% 0.04 230);}
.tl{font-size:.44rem;text-transform:uppercase;letter-spacing:1.5px;color:var(--muted);
  font-family:var(--font-head);font-weight:600;
  display:flex;align-items:center;justify-content:center;gap:3px;margin-bottom:3px;}
.tv{font-size:1.5rem;font-weight:300;color:var(--text);line-height:1;font-family:var(--font-body);}

/* NOTES */
.notes-area textarea{width:100%;background:var(--surface);border:1px solid var(--border);
  color:var(--text);font-family:var(--font-body);font-size:.72rem;padding:9px;
  border-radius:4px;outline:none;resize:vertical;min-height:64px;line-height:1.6;}
.notes-area textarea:focus{border-color:var(--accent);}

/* NOTICE */
.med-notice{margin-bottom:13px;padding:9px 14px;
  background:var(--accent-tint);border:1px solid var(--accent-ring);
  border-radius:5px;font-size:.62rem;color:var(--muted);font-family:var(--font-head);
  letter-spacing:.3px;display:flex;align-items:flex-start;gap:7px;}

/* REPORTS */
.rpt-hdr{display:flex;align-items:center;gap:12px;margin-bottom:18px;}
.rpt-badge{display:inline-flex;align-items:center;gap:5px;padding:2px 9px;border-radius:3px;
  font-size:.5rem;font-weight:600;text-transform:uppercase;letter-spacing:2px;font-family:var(--font-head);}
.rb-day{background:var(--accent-tint);color:var(--accent);border:1px solid var(--accent-ring);}
.rb-week{background:#f0fdf4;color:var(--green);border:1px solid #bbf7d0;}
.rb-month{background:#f5f3ff;color:var(--purple);border:1px solid #ddd6fe;}
.rb-q{background:#fffbeb;color:var(--warn);border:1px solid #fde68a;}
.rb-sem{background:#fff7ed;color:var(--orange);border:1px solid #fed7aa;}
.rb-year{background:#fef2f2;color:var(--danger);border:1px solid #fecaca;}
.rb-cmp{background:oklch(96% 0.02 230);color:var(--accent);border:1px solid oklch(89% 0.04 230);}
.rpt-title{font-family:var(--font-head);font-size:1rem;font-weight:700;color:var(--text);}
.period-row{display:flex;align-items:center;gap:9px;margin-bottom:16px;flex-wrap:wrap;}
.period-row label{font-size:.5rem;text-transform:uppercase;letter-spacing:1.5px;color:var(--muted);}
.period-row input[type=date],.period-row input[type=month],.period-row select{
  background:var(--surface);border:1px solid var(--border);color:var(--text);
  font-family:var(--font-body);font-size:.68rem;padding:5px 8px;border-radius:4px;outline:none;}
.period-row input:focus,.period-row select:focus{border-color:var(--accent);}
.btn-load{padding:6px 14px;background:var(--accent);color:#fff;border:none;border-radius:4px;
  font-family:var(--font-head);font-size:.58rem;font-weight:600;letter-spacing:.4px;
  text-transform:uppercase;cursor:pointer;transition:opacity .13s;display:inline-flex;align-items:center;gap:5px;}
.btn-load:hover{opacity:.83;}

/* REPORT TABLE */
.rpt-wrap{overflow-x:auto;}
.rpt-table{width:100%;border-collapse:collapse;font-size:.7rem;}
.rpt-table thead tr{background:var(--bg);}
.rpt-table th{padding:8px 10px;text-align:left;font-family:var(--font-head);font-size:.48rem;
  font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:var(--muted);
  border-bottom:1px solid var(--border);}
.rpt-table td{padding:7px 10px;border-bottom:1px solid var(--border);font-family:var(--font-body);}
.rpt-table tbody tr:hover{background:oklch(98.5% 0.003 230);}
.rpt-table .num{text-align:right;font-variant-numeric:tabular-nums;font-weight:500;}
.rpt-table .num.d{color:var(--accent);}
.rpt-table .num.n{color:var(--muted);}
.rpt-total-row td{font-weight:600;background:var(--bg);color:var(--text);border-top:1px solid var(--border);}

/* SUMMARY CARDS */
.sum-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin-bottom:16px;}
.sum-card{border-radius:5px;padding:13px;text-align:center;}
.sum-card.c1{background:var(--accent-tint);border:1px solid var(--accent-ring);}
.sum-card.c2{background:#f7f7f7;border:1px solid #e8e8e8;}
.sum-card.c3{background:oklch(96% 0.02 230);border:1px solid oklch(89% 0.04 230);}
.sum-label{font-size:.44rem;text-transform:uppercase;letter-spacing:1.5px;font-family:var(--font-head);
  font-weight:600;color:var(--muted);display:flex;align-items:center;justify-content:center;gap:3px;margin-bottom:4px;}
.sum-val{font-size:1.7rem;font-weight:300;color:var(--text);line-height:1;font-family:var(--font-body);}
.sum-sub{font-size:.5rem;color:var(--muted);margin-top:3px;font-family:var(--font-head);}

/* COMPARAÇÃO */
.cmp-boxes{display:grid;grid-template-columns:1fr 1fr 1fr;gap:9px;margin-bottom:14px;}
.cmp-box{border-radius:5px;padding:11px;text-align:center;}
.cmp-box.a{background:var(--accent-tint);border:1px solid var(--accent-ring);}
.cmp-box.b{background:#f7f7f7;border:1px solid #e8e8e8;}
.cmp-box.diff{background:var(--bg);border:1px solid var(--border);}
.cmp-lbl{font-size:.44rem;text-transform:uppercase;letter-spacing:1.5px;font-family:var(--font-head);
  font-weight:600;display:block;margin-bottom:3px;color:var(--muted);}
.cmp-val{font-size:1.6rem;font-weight:300;line-height:1;color:var(--text);font-family:var(--font-body);}
.diff-pos{color:var(--green)!important;font-weight:600;}
.diff-neg{color:var(--danger)!important;font-weight:600;}
.diff-neu{color:var(--muted)!important;}
.cmp-period-row{display:flex;flex-direction:column;gap:6px;
  background:var(--accent-tint);border:1px solid var(--accent-ring);border-radius:5px;padding:9px 13px;}
.cmp-period-row.b-side{background:#f7f7f7;border-color:#e8e8e8;}
.cmp-period-lbl{font-size:.44rem;text-transform:uppercase;letter-spacing:2px;
  color:var(--muted);font-family:var(--font-head);font-weight:600;}

/* NO DATA */
.no-data{text-align:center;padding:40px 20px;color:var(--muted);font-family:var(--font-head);}
.no-data span{font-size:1.5rem;display:block;margin-bottom:8px;opacity:.4;}

/* TOAST */
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(16px);
  background:var(--text);color:#fff;padding:8px 18px;border-radius:5px;
  font-family:var(--font-head);font-size:.66rem;font-weight:500;
  opacity:0;transition:all .22s;z-index:9999;pointer-events:none;}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0);}

/* MODAL */
.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.3);backdrop-filter:blur(3px);
  z-index:1000;display:none;align-items:center;justify-content:center;}
.modal-overlay.open{display:flex;}
.modal-box{background:var(--surface);border:1px solid var(--border);border-radius:8px;
  padding:24px;width:480px;max-width:94vw;max-height:88vh;overflow-y:auto;
  box-shadow:0 4px 24px rgba(0,0,0,.07);}
.modal-box h3{font-family:var(--font-head);font-size:.95rem;font-weight:700;margin-bottom:8px;color:var(--text);}
.modal-box p{font-size:.68rem;color:var(--muted);margin-bottom:18px;line-height:1.6;font-family:var(--font-head);}
.modal-btns{display:flex;gap:9px;justify-content:flex-end;}
.mbtn{padding:7px 16px;border-radius:4px;font-family:var(--font-head);font-size:.6rem;
  font-weight:600;letter-spacing:.4px;text-transform:uppercase;cursor:pointer;border:none;}
.mbtn.cancel{background:var(--bg);color:var(--muted);border:1px solid var(--border);}
.mbtn.cancel:hover{color:var(--text);}
.mbtn.confirm{background:var(--danger);color:#fff;}
.mbtn.confirm:hover{opacity:.85;}

/* SAVE BAR */
.save-bar{position:fixed;bottom:0;left:var(--nav-w);right:0;height:44px;z-index:50;
  background:var(--surface);border-top:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;padding:0 24px;}
.save-status{font-size:.57rem;color:var(--muted);font-family:var(--font-head);}
.save-status span{color:var(--accent);font-weight:600;}

/* AUTO-SAVE */
.as-dot{display:inline-block;width:6px;height:6px;border-radius:50%;
  background:var(--green);margin-right:5px;opacity:0;transition:opacity .3s;}
.as-dot.saving{opacity:1;animation:pulse .6s infinite;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}

@media(max-width:768px){
  .sidebar{left:calc(-1 * var(--nav-w));transition:left .25s;}
  .sidebar.open{left:0;}
  .main-content{margin-left:0;}
  .save-bar{left:0;}
  .spec-totals{display:none;}
}
</style>'''

# ─────────────────────────────────────────────────────────────────────────────
# NOVO SPLASH HTML
# ─────────────────────────────────────────────────────────────────────────────
NEW_SPLASH = '''<div id="splash">
  <div class="splash-inner">
    <div class="splash-mark">HP</div>
    <p class="splash-hosp-lbl">Hospital do Prenda · Luanda</p>
    <h1 class="splash-svc-lbl">Serviço de Procedimentos de Enfermagem</h1>
    <div class="splash-rule"></div>
  </div>
  <div id="splash-timer" style="display:none"></div>
</div>'''

# ─────────────────────────────────────────────────────────────────────────────
# TRANSFORMAÇÃO PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
def transform(content):
    # 1. Font link
    content = content.replace(
        'family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500',
        'family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@300;400;500'
    )

    # 2. CSS block
    content = re.sub(r'<style>.*?</style>', NEW_CSS, content, flags=re.DOTALL)

    # 3. Splash
    content = re.sub(r'<div id="splash">.*?(?=\n<header>)', NEW_SPLASH, content, flags=re.DOTALL)

    # 4. SVG sprite — logo pequeno no header (preserva mas esconde a img)
    content = content.replace('<body>\n', '<body>\n' + SVG_SPRITE + '\n', 1)

    # 5. Botões estáticos — emojis → SVG
    btn_map = [
        ('>💾 Guardado<',    f'>{icon("i-check")} Guardado<'),
        ('>💾 Guardar</',    f'>{icon("i-save")} Guardar</'),
        ('>📄 PDF</',        f'>{icon("i-pdf")} PDF</'),
        ('>⬇️ Backup</',    f'>{icon("i-download")} Backup</'),
        ('>⬆️ Restaurar<',  f'>{icon("i-upload")} Restaurar<'),
        ('>💾 Guardar Dia<', f'>{icon("i-save")} Guardar<'),
        ('>📄 Exportar PDF<',f'>{icon("i-pdf")} Exportar PDF<'),
    ]
    for old, new in btn_map:
        content = content.replace(old, new)

    # 6. Nav relatórios — emojis nos ni-icon
    rpt_icons = [
        ('<span class="ni-icon">📅</span><span class="ni-label">Resumo Diário</span>',
         f'<span class="ni-icon">{icon("i-sun")}</span><span class="ni-label">Resumo Diário</span>'),
        ('<span class="ni-icon">📊</span><span class="ni-label">Semanal</span>',
         f'<span class="ni-icon">{icon("i-chart")}</span><span class="ni-label">Semanal</span>'),
        ('<span class="ni-icon">📆</span><span class="ni-label">Mensal</span>',
         f'<span class="ni-icon">{icon("i-calendar")}</span><span class="ni-label">Mensal</span>'),
        ('<span class="ni-icon">📈</span><span class="ni-label">Trimestral</span>',
         f'<span class="ni-icon">{icon("i-chart")}</span><span class="ni-label">Trimestral</span>'),
        ('<span class="ni-icon">📉</span><span class="ni-label">Semestral</span>',
         f'<span class="ni-icon">{icon("i-chart")}</span><span class="ni-label">Semestral</span>'),
        ('<span class="ni-icon">🗓️</span><span class="ni-label">Anual</span>',
         f'<span class="ni-icon">{icon("i-calendar")}</span><span class="ni-label">Anual</span>'),
        ('<span class="ni-icon">🔀</span><span class="ni-label">Comparação</span>',
         f'<span class="ni-icon">{icon("i-shuffle")}</span><span class="ni-label">Comparação</span>'),
    ]
    for old, new in rpt_icons:
        content = content.replace(old, new)

    # 7. Report badges
    badge_map = [
        ('>📅 Resumo Diário<',  f'>{icon("i-sun")} Resumo Diário<'),
        ('🗓️ Anual',            f'{icon("i-calendar")} Anual'),
    ]
    for old, new in badge_map:
        content = content.replace(old, new)

    # 8. Modal warning emoji
    content = content.replace('<h3>⚠️ Restaurar Backup</h3>', '<h3>Restaurar Backup</h3>')

    # 9. No-data emoji spans (mantém span, limpa emoji)
    content = re.sub(r'<span>(📅|🔀|📊|📆|📈|📉|🗓️)</span>', '', content)

    # 10. JS template strings — emoji → SVG
    js_map = [
        ('☀️ Turno Dia',     f'{icon("i-sun")} Turno Dia'),
        ('🌙 Turno Noite',   f'{icon("i-moon")} Turno Noite'),
        ('☀️ Dia',           f'{icon("i-sun")} Dia'),
        ('🌙 Noite',         f'{icon("i-moon")} Noite'),
        ('☀️ Total Dia',     f'{icon("i-sun")} Total Dia'),
        ('🌙 Total Noite',   f'{icon("i-moon")} Total Noite'),
        ('📝 Notas — Turno Dia',   f'{icon("i-notes")} Notas — Dia'),
        ('📝 Notas — Turno Noite', f'{icon("i-notes")} Notas — Noite'),
        ('⚡ Calculado',     f'{icon("i-info")} Calculado'),
        # sum cards accent2 compat
        ('style="color:var(--accent2)"', ''),
    ]
    for old, new in js_map:
        content = content.replace(old, new)

    # 11. Toast + sync emoji
    content = content.replace("showToast('📄 PDF", "showToast('PDF")
    content = content.replace(
        "setSyncInfo('💾 Guardado",
        f"setSyncInfo('{icon('i-check')} Guardado"
    )

    # 12. select option — textContent não renderiza SVG
    content = content.replace(
        "o.textContent = sp.icon + ' ' + sp.label;",
        "o.textContent = sp.label;"
    )

    # 13. Inline styles dos botões de relatório — strip cor específica,
    #     deixar só o btn-load (já estilizado no CSS)
    content = re.sub(
        r' style="background:transparent;border:1px solid var\(--\w+\);color:var\(--\w+\);"',
        '',
        content
    )

    return content


# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DOS FICHEIROS
# ─────────────────────────────────────────────────────────────────────────────
INDIVIDUAL = [
    ('ortopedia',      'Ortopedia',            'i-bone'),
    ('cuid_intermedio','Cuidados Intermédios',  'i-bed'),
    ('uci',            'UCI',                  'i-heart'),
    ('cirurgia',       'Cirurgia',             'i-scalpel'),
    ('maxilo',         'Maxilo Facial',        'i-tooth'),
    ('consulta_ext',   'Consulta Externa',     'i-clipboard'),
    ('nefrologia',     'Nefrologia',           'i-droplet'),
    ('hosp_dia',       'Hospital de Dia',      'i-calendar'),
    ('neurocirurgia',  'Neurocirurgia',        'i-brain'),
    ('otorrino',       'Otorrinolaringologia', 'i-ear'),
    ('banco_urg',      'Banco de Urgência',    'i-cross-sq'),
]

GROUPS = [
    (
        'bloco_op', 'Bloco Operatório',
        [('bloco_op','Bloco Operatório','i-lamp'),
         ('bloco_urgente','Bloco Op. Urgente','i-cross-sq'),
         ('bloco_electiva','Bloco Op. Electiva','i-calendar')]
    ),
    (
        'medicina', 'Medicina',
        [('med_homem','Medicina Homem','i-notes'),
         ('med_mulher','Medicina Mulher','i-notes'),
         ('medicina','Medicina (Auto)','i-pill')]
    ),
]

specialties_pattern = re.compile(r'const SPECIALTIES = \[.*?\];', re.DOTALL)

def make_specialties_js(entries):
    lines = ['const SPECIALTIES = [']
    for sid, label, ico in entries:
        svg = icon(ico).replace('"', '\\"')  # escape for JS string
        # Use the icon in the JS object
        lines.append(f"  {{ id:'{sid}', label:'{label}', icon:'{icon(ico)}' }},")
    lines.append('];')
    return '\n'.join(lines)


def generate(content, label, filename, entries):
    new_array = make_specialties_js(entries)
    out = specialties_pattern.sub(new_array, content)
    # Title
    out = out.replace(
        '<title>Serviço de Procedimentos de Enfermagem</title>',
        f'<title>Procedimentos do Serviço de {label}</title>'
    )
    # Splash service label (in h1.splash-svc-lbl)
    out = out.replace(
        'Serviço de Procedimentos de Enfermagem',
        f'Procedimentos do Serviço de {label}'
    )
    path = os.path.join(OUT, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(out)
    print(f'  ✓  {filename}')


# ─────────────────────────────────────────────────────────────────────────────
# EXECUÇÃO
# ─────────────────────────────────────────────────────────────────────────────
print('A ler ficheiro fonte…')
with open(SRC, 'r', encoding='utf-8') as f:
    original = f.read()

print('A aplicar redesign visual…')
transformed = transform(original)

os.makedirs(OUT, exist_ok=True)

print('A gerar ficheiros individuais…')
for sid, label, ico in INDIVIDUAL:
    generate(transformed, label, f'proc_{sid}.html', [(sid, label, ico)])

print('A gerar ficheiros combinados…')
for fid, label, entries in GROUPS:
    generate(transformed, label, f'proc_{fid}.html', entries)

total = len(INDIVIDUAL) + len(GROUPS)
print(f'\n✓ {total} ficheiros gerados em {OUT}/')
