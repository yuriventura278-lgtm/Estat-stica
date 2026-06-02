#!/usr/bin/env python3
"""
Gera a página da Secretaria Geral do Hospital do Prenda.
Extrai a foto do hospital de um ficheiro existente e injeta-a na splash.
"""
import re, os

OUT = '/home/user/Estat-stica/procedimentos/secretaria_geral.html'
SRC = '/home/user/Estat-stica/procedimentos/proc_laboratorio.html'

def get_hosp_img():
    with open(SRC, 'r', encoding='utf-8') as f:
        c = f.read()
    m = re.search(r'src="(data:image/jpeg;base64,[^"]{200,})"', c)
    return m.group(1) if m else 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs='

HOSP_IMG = get_hosp_img()
CIRC = '263.9'

# Use __HOSP_IMG__ and __CIRC__ as placeholders — substituted at end
HTML = '''<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Secretaria Geral — Hospital do Prenda</title>
<script>if(localStorage.getItem("theme")==="dark")document.documentElement.classList.add("dark");</script>
<style>
/* ── RESET & TOKENS ── */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
:root{
  --header-h:56px;--staff-h:38px;--sidebar-w:230px;
  --bg:#f4f6fa;--surface:#ffffff;--surface2:#f1f5f9;
  --border:#e2e8f0;--text:#0f172a;--muted:#64748b;
  --accent:#1a56db;--accent2:#00d4aa;--red:#ef4444;--amber:#f59e0b;
  --green:#10b981;
  --fh:'Inter',sans-serif;--fm:'IBM Plex Mono',monospace;
  --shadow:0 1px 3px rgba(0,0,0,.08),0 4px 16px rgba(0,0,0,.06);
}
html.dark{
  --bg:#0c0f14;--surface:#141820;--surface2:#0f1520;
  --border:rgba(30,40,64,.9);--text:#e2e8f0;--muted:#64748b;
}
body{font-family:var(--fh);background:var(--bg);color:var(--text);
  font-size:14px;line-height:1.5;transition:background .2s,color .2s;}

/* ── SPLASH ── */
#splash{position:fixed;inset:0;z-index:9999;background:#0c0f14;
  display:flex;align-items:center;justify-content:center;}
.splash-inner{display:flex;flex-direction:column;align-items:center;gap:14px;text-align:center;}
.splash-img-ring{position:relative;width:100px;height:100px;}
.splash-img-circle{position:absolute;inset:8px;border-radius:50%;overflow:hidden;background:#1a2a3a;}
.splash-img-circle img{width:100%;height:100%;object-fit:cover;}
.splash-progress-svg{position:absolute;inset:0;width:100px;height:100px;transform:rotate(-90deg);}
.spl-ring-bg{fill:none;stroke:rgba(255,255,255,.12);stroke-width:4;}
.spl-ring-fg{fill:none;stroke:#00d4aa;stroke-width:4;stroke-linecap:round;}
.splash-hosp-lbl{font-size:.55rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;
  color:rgba(200,230,220,.65);}
.splash-svc-lbl{font-size:.9rem;font-weight:700;color:#fff;max-width:280px;line-height:1.35;}
.splash-pct{font-size:.65rem;color:#00d4aa;font-weight:600;letter-spacing:.05em;font-family:var(--fm);}

/* ── STAFF BAR ── */
.hp-staff-bar{position:fixed;top:0;left:0;right:0;z-index:190;height:var(--staff-h);
  background:rgba(26,86,219,.06);border-bottom:1px solid rgba(26,86,219,.15);
  display:flex;align-items:center;gap:12px;padding:0 20px;}
html.dark .hp-staff-bar{background:rgba(26,86,219,.1);border-bottom-color:rgba(26,86,219,.2);}
.hp-staff-lbl{font-size:.46rem;color:var(--muted);font-weight:600;text-transform:uppercase;
  letter-spacing:1.4px;white-space:nowrap;}
.hp-staff-sep{color:var(--border);font-size:.8rem;margin:0 2px;}
.hp-staff-inp{background:transparent;border:none;border-bottom:1px solid rgba(26,86,219,.25);
  color:var(--text);font-family:var(--fh);font-size:.68rem;padding:2px 6px;outline:none;
  min-width:150px;max-width:220px;transition:border-color .13s;}
.hp-staff-inp::placeholder{opacity:.4;}
.hp-staff-inp:focus{border-bottom-color:rgba(26,86,219,.7);}

/* ── HEADER ── */
header{position:fixed;top:var(--staff-h);left:0;right:0;z-index:180;height:var(--header-h);
  background:var(--surface);border-bottom:1px solid var(--border);
  display:flex;align-items:center;padding:0 20px;gap:16px;
  box-shadow:0 1px 4px rgba(0,0,0,.06);}
.header-logo{width:32px;height:32px;border-radius:50%;overflow:hidden;flex-shrink:0;}
.header-logo img{width:100%;height:100%;object-fit:cover;}
.header-title{flex:1;}
.header-title h1{font-size:.78rem;font-weight:700;color:var(--text);letter-spacing:.01em;}
.header-title span{font-size:.56rem;color:var(--muted);}
.header-right{display:flex;align-items:center;gap:10px;margin-left:auto;}
#theme-toggle{padding:5px 11px;border-radius:4px;cursor:pointer;background:transparent;
  border:1px solid var(--border);color:var(--text);font-size:.57rem;font-weight:600;
  letter-spacing:.4px;text-transform:uppercase;display:inline-flex;align-items:center;
  gap:5px;white-space:nowrap;transition:border-color .15s;}
#theme-toggle:hover{border-color:var(--accent);}

/* ── LAYOUT ── */
.layout{display:flex;
  margin-top:calc(var(--staff-h) + var(--header-h));
  min-height:calc(100vh - var(--staff-h) - var(--header-h));}
.sidebar{width:var(--sidebar-w);flex-shrink:0;background:var(--surface);
  border-right:1px solid var(--border);padding:16px 0;
  position:sticky;top:calc(var(--staff-h) + var(--header-h));
  height:calc(100vh - var(--staff-h) - var(--header-h));overflow-y:auto;}
.nav-section-lbl{font-size:.47rem;font-weight:700;letter-spacing:.15em;text-transform:uppercase;
  color:var(--muted);padding:14px 20px 6px;}
.nav-item{display:flex;align-items:center;gap:10px;padding:9px 20px;cursor:pointer;
  font-size:.72rem;color:var(--muted);font-weight:500;transition:all .13s;
  border-left:3px solid transparent;}
.nav-item:hover{color:var(--text);background:var(--surface2);}
.nav-item.active{color:var(--accent);background:rgba(26,86,219,.06);
  border-left-color:var(--accent);font-weight:600;}
.nav-item svg{width:15px;height:15px;stroke:currentColor;fill:none;
  stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;flex-shrink:0;}
.main{flex:1;padding:24px;min-width:0;}

/* ── SECTION ── */
.section{display:none;max-width:920px;}
.section.active{display:block;}
.page-header{margin-bottom:20px;}
.page-title{font-size:1.05rem;font-weight:700;color:var(--text);}
.page-sub{font-size:.68rem;color:var(--muted);margin-top:2px;}

/* ── CARDS ── */
.card{background:var(--surface);border:1px solid var(--border);border-radius:12px;
  padding:20px;margin-bottom:16px;box-shadow:var(--shadow);}
.card-title{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.09em;
  color:var(--muted);margin-bottom:14px;display:flex;align-items:center;gap:8px;}
.card-title .ct-badge{font-size:.6rem;font-weight:500;letter-spacing:normal;color:var(--muted);
  text-transform:none;margin-left:auto;}

/* ── PROCESS NUMBER PREVIEW ── */
.num-preview{background:rgba(26,86,219,.07);border:1px solid rgba(26,86,219,.2);
  border-radius:10px;padding:14px 18px;display:flex;align-items:center;gap:16px;
  margin-bottom:16px;}
html.dark .num-preview{background:rgba(26,86,219,.11);border-color:rgba(26,86,219,.28);}
.num-preview-label{font-size:.58rem;font-weight:600;color:var(--accent);
  text-transform:uppercase;letter-spacing:.1em;}
.num-preview-val{font-family:var(--fm);font-size:1.6rem;font-weight:700;color:var(--accent);}
.num-preview-sub{font-size:.6rem;color:var(--muted);margin-top:2px;}

/* ── FORM ── */
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
@media(max-width:640px){.form-grid{grid-template-columns:1fr;}}
.span2{grid-column:span 2;}
.field-group{display:flex;flex-direction:column;gap:5px;}
label{font-size:.57rem;font-weight:600;color:var(--muted);
  text-transform:uppercase;letter-spacing:.08em;}
input[type="text"],input[type="date"],input[type="number"],select,textarea{
  background:var(--surface2);border:1px solid var(--border);
  color:var(--text);font-family:var(--fh);font-size:.78rem;
  padding:8px 12px;border-radius:7px;outline:none;width:100%;
  transition:border-color .13s;}
input:focus,select:focus,textarea:focus{
  border-color:var(--accent);box-shadow:0 0 0 3px rgba(26,86,219,.1);}
textarea{resize:vertical;min-height:68px;}
html.dark input,html.dark select,html.dark textarea{
  background:rgba(255,255,255,.04);border-color:rgba(255,255,255,.1);}
input[readonly]{color:var(--muted);cursor:not-allowed;}

/* ── BUTTONS ── */
.btn{padding:9px 18px;border-radius:7px;cursor:pointer;font-family:var(--fh);
  font-size:.72rem;font-weight:600;border:none;transition:all .15s;
  display:inline-flex;align-items:center;gap:6px;}
.btn-primary{background:var(--accent);color:#fff;}
.btn-primary:hover{background:#1648c8;}
.btn-outline{background:transparent;color:var(--text);border:1px solid var(--border);}
.btn-outline:hover{border-color:var(--accent);color:var(--accent);}
.btn-sm{padding:6px 14px;font-size:.65rem;}
.btn-ghost{background:transparent;color:var(--muted);border:1px dashed var(--border);}
.btn-ghost:hover{border-color:var(--accent);color:var(--accent);}

/* ── FILE INPUT ── */
input[type="file"]{background:var(--surface2);border:1px dashed var(--border);
  color:var(--text);font-size:.72rem;padding:7px 12px;border-radius:7px;
  width:100%;cursor:pointer;}
input[type="file"]:hover{border-color:var(--accent);}

/* ── DOC CARDS ── */
.doc-list{display:flex;flex-direction:column;gap:10px;}
.doc-card{background:var(--surface);border:1px solid var(--border);border-radius:10px;
  overflow:hidden;}
.doc-card.doc-despachado{border-left:4px solid var(--green);}
.doc-card.doc-pendente{border-left:4px solid var(--amber);}
.doc-card-header{display:flex;align-items:center;gap:8px;padding:9px 14px;
  background:var(--surface2);border-bottom:1px solid var(--border);flex-wrap:wrap;gap:8px;}
.doc-num{font-family:var(--fm);font-size:.75rem;font-weight:700;color:var(--accent);
  background:rgba(26,86,219,.1);padding:3px 8px;border-radius:4px;white-space:nowrap;}
html.dark .doc-num{background:rgba(26,86,219,.18);}
.doc-tipo-badge{font-size:.58rem;font-weight:600;padding:3px 8px;border-radius:12px;
  background:rgba(0,212,170,.1);color:#00957a;text-transform:uppercase;
  letter-spacing:.05em;white-space:nowrap;}
html.dark .doc-tipo-badge{background:rgba(0,212,170,.15);color:#00d4aa;}
.doc-data{font-size:.6rem;color:var(--muted);font-family:var(--fm);margin-left:auto;}
.despachado-badge{font-size:.58rem;font-weight:600;padding:3px 8px;border-radius:12px;
  background:rgba(16,185,129,.1);color:#059669;}
html.dark .despachado-badge{background:rgba(16,185,129,.15);color:#34d399;}
.pendente-badge{font-size:.58rem;font-weight:600;padding:3px 8px;border-radius:12px;
  background:rgba(245,158,11,.1);color:#d97706;}
html.dark .pendente-badge{background:rgba(245,158,11,.14);color:#fbbf24;}
.doc-card-body{padding:12px 14px;}
.doc-inst{font-size:.82rem;font-weight:700;color:var(--text);margin-bottom:4px;}
.doc-oficio{font-size:.67rem;color:var(--muted);font-family:var(--fm);margin-bottom:3px;}
.doc-assunto{font-size:.74rem;color:var(--text);line-height:1.45;}
.doc-anexo{font-size:.62rem;color:var(--muted);margin-top:5px;}
.doc-despacho-info{padding:10px 14px;background:rgba(16,185,129,.04);
  border-top:1px solid var(--border);}
html.dark .doc-despacho-info{background:rgba(16,185,129,.06);}

/* ── DESPACHO FORM ── */
.desp-form{padding:14px;border-top:1px solid var(--border);background:var(--surface2);}
html.dark .desp-form{background:rgba(255,255,255,.02);}
.desp-form-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:10px;}
@media(max-width:620px){.desp-form-row{grid-template-columns:1fr;}}
.btn-despachar{background:var(--accent);color:#fff;padding:8px 18px;
  border-radius:7px;border:none;font-family:var(--fh);font-size:.72rem;font-weight:600;
  cursor:pointer;display:inline-flex;align-items:center;gap:6px;transition:background .15s;}
.btn-despachar:hover{background:#1648c8;}

/* ── DESPACHO TABLE ── */
.desp-detail-table{width:100%;border-collapse:collapse;font-size:.68rem;}
.desp-detail-table td{padding:4px 8px;color:var(--text);}
.desp-detail-table td:first-child{color:var(--muted);font-weight:600;
  white-space:nowrap;width:135px;text-transform:uppercase;
  font-size:.57rem;letter-spacing:.05em;}

/* ── SEARCH ── */
.search-row{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px;align-items:flex-end;}
.search-box{flex:2;min-width:200px;position:relative;}
.search-box input{padding-left:34px;}
.search-icon{position:absolute;left:11px;top:50%;transform:translateY(-50%);
  color:var(--muted);pointer-events:none;}
.search-icon svg{width:14px;height:14px;stroke:currentColor;fill:none;
  stroke-width:2;stroke-linecap:round;stroke-linejoin:round;}
.pesq-stats{font-size:.65rem;color:var(--muted);margin-top:6px;}

/* ── KPI ROW ── */
.kpi-row{display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));
  gap:10px;margin-bottom:16px;}
.kpi-box{background:var(--surface);border:1px solid var(--border);border-radius:10px;
  padding:12px 14px;text-align:center;}
.kpi-label{font-size:.51rem;text-transform:uppercase;letter-spacing:.1em;
  color:var(--muted);margin-bottom:4px;font-weight:600;}
.kpi-val{font-family:var(--fm);font-size:1.55rem;font-weight:700;color:var(--text);}
.kpi-accent{border-color:rgba(26,86,219,.3);}
.kpi-accent .kpi-val{color:var(--accent);}
.kpi-green{border-color:rgba(16,185,129,.3);}
.kpi-green .kpi-val{color:var(--green);}
.kpi-amber{border-color:rgba(245,158,11,.3);}
.kpi-amber .kpi-val{color:var(--amber);}

/* ── DEFINIÇÕES ── */
.def-card{background:var(--surface);border:1px solid var(--border);
  border-radius:12px;padding:20px;margin-bottom:16px;}
html.dark .def-card{background:#141820;border-color:#1e2840;}
.def-section-title{font-size:.64rem;font-weight:700;text-transform:uppercase;
  letter-spacing:.12em;color:var(--muted);margin-bottom:12px;padding-bottom:8px;
  border-bottom:1px solid var(--border);}
.def-preview-box{background:rgba(26,86,219,.06);border:1px dashed rgba(26,86,219,.3);
  border-radius:8px;padding:12px 16px;margin-top:12px;
  display:flex;align-items:center;gap:12px;}
html.dark .def-preview-box{background:rgba(26,86,219,.1);}
.def-preview-lbl{font-size:.57rem;color:var(--muted);text-transform:uppercase;
  letter-spacing:.08em;font-weight:600;}
.def-preview-num{font-family:var(--fm);font-size:1.3rem;font-weight:700;color:var(--accent);}
.def-info{font-size:.68rem;color:var(--muted);line-height:1.65;margin-top:12px;
  padding:10px 14px;background:var(--surface2);border-radius:7px;}

/* ── MISC ── */
.no-data-msg{text-align:center;padding:30px 20px;color:var(--muted);
  font-size:.78rem;background:var(--surface2);border-radius:10px;}
.filter-bar{display:flex;gap:12px;align-items:flex-end;flex-wrap:wrap;
  padding-bottom:14px;border-bottom:1px solid var(--border);margin-bottom:14px;}
hr{border:none;border-top:1px solid var(--border);margin:18px 0;}

/* ── TOAST ── */
#toast{position:fixed;bottom:24px;right:24px;padding:11px 18px;border-radius:8px;
  font-size:.75rem;font-weight:600;z-index:9998;pointer-events:none;
  opacity:0;transform:translateY(20px);transition:all .3s;max-width:340px;}
.toast-ok{background:#059669;color:#fff;}
.toast-err{background:#dc2626;color:#fff;}

/* ── DARK MODE OVERRIDES ── */
html.dark header{background:#141820;border-bottom-color:#1e2840;}
html.dark .sidebar{background:#141820;border-right-color:#1e2840;}
html.dark .card{background:#141820;border-color:#1e2840;}
html.dark .doc-card{background:#141820;border-color:#1e2840;}
html.dark .doc-card-header{background:rgba(255,255,255,.03);border-bottom-color:#1e2840;}
html.dark .kpi-box{background:#141820;border-color:#1e2840;}
</style>
</head>
<body>

<!-- ══ SPLASH ══ -->
<div id="splash">
  <div class="splash-inner">
    <div class="splash-img-ring">
      <div class="splash-img-circle">
        <img src="__HOSP_IMG__" alt="Hospital do Prenda">
      </div>
      <svg class="splash-progress-svg" viewBox="0 0 100 100">
        <circle class="spl-ring-bg" cx="50" cy="50" r="42"/>
        <circle class="spl-ring-fg" id="spl-ring" cx="50" cy="50" r="42"
          stroke-dasharray="__CIRC__" stroke-dashoffset="__CIRC__"/>
      </svg>
    </div>
    <p class="splash-hosp-lbl">Hospital do Prenda · Luanda</p>
    <h1 class="splash-svc-lbl">Secretaria Geral</h1>
    <div class="splash-pct" id="spl-pct">0%</div>
  </div>
</div>

<!-- ══ STAFF BAR ══ -->
<div class="hp-staff-bar">
  <span class="hp-staff-lbl">Profissional</span>
  <input type="text" id="inp-profissional" class="hp-staff-inp"
    placeholder="Nome do profissional" autocomplete="name" oninput="saveStaffInfo()">
  <span class="hp-staff-sep">·</span>
  <span class="hp-staff-lbl">Chefe de Turno</span>
  <input type="text" id="inp-chefe" class="hp-staff-inp"
    placeholder="Nome do chefe de turno" autocomplete="name" oninput="saveStaffInfo()">
</div>

<!-- ══ HEADER ══ -->
<header>
  <div class="header-logo"><img src="__HOSP_IMG__" alt="HP"></div>
  <div class="header-title">
    <h1>Secretaria Geral — Registo de Correspondência</h1>
    <span>Hospital do Prenda · Luanda · Angola</span>
  </div>
  <div class="header-right">
    <button id="theme-toggle" onclick="toggleTheme()" title="Mudar para tema escuro"
      style="padding:5px 11px;border-radius:4px;cursor:pointer;background:transparent;
      border:1px solid var(--border);color:inherit;font-size:.57rem;font-weight:600;
      letter-spacing:.4px;text-transform:uppercase;display:inline-flex;align-items:center;
      gap:5px;white-space:nowrap;">
      <svg style="width:13px;height:13px;stroke:currentColor;fill:none;stroke-width:1.5;
        stroke-linecap:round;stroke-linejoin:round;vertical-align:-2px">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
      </svg>
      Tema
    </button>
  </div>
</header>

<!-- ══ LAYOUT ══ -->
<div class="layout">

  <!-- Sidebar -->
  <nav class="sidebar">
    <div class="nav-section-lbl">Correspondência</div>
    <div class="nav-item active" data-section="sec-registo" onclick="showSection('sec-registo')">
      <svg viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
      Registo Diário
    </div>
    <div class="nav-item" data-section="sec-despacho" onclick="showSection('sec-despacho')">
      <svg viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/>
        <polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
      Despacho
    </div>
    <div class="nav-section-lbl">Consulta</div>
    <div class="nav-item" data-section="sec-pesquisa" onclick="showSection('sec-pesquisa')">
      <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/>
        <line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      Pesquisar
    </div>
    <div class="nav-section-lbl">Sistema</div>
    <div class="nav-item" data-section="sec-definicoes" onclick="showSection('sec-definicoes')">
      <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/>
        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06
          a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09
          A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06
          A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09
          A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06
          A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09
          a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06
          A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09
          a1.65 1.65 0 0 0-1.51 1z"/></svg>
      Definições
    </div>
  </nav>

  <!-- Main -->
  <main class="main">

    <!-- ── REGISTO ── -->
    <section id="sec-registo" class="section active">
      <div class="page-header">
        <div class="page-title">📋 Registo de Correspondência Recebida</div>
        <div class="page-sub">Registe documentos recebidos pela Direcção Geral e atribua número de processo</div>
      </div>

      <div class="num-preview">
        <div>
          <div class="num-preview-label">Próximo Nº de Processo</div>
          <div class="num-preview-val" id="preview-num">—</div>
          <div class="num-preview-sub" id="preview-sub"></div>
        </div>
      </div>

      <div class="card">
        <div class="card-title">
          <svg style="width:14px;height:14px;stroke:currentColor;fill:none;stroke-width:2;
            stroke-linecap:round;stroke-linejoin:round" viewBox="0 0 24 24">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
          </svg>
          Novo Registo
          <span class="ct-badge">* campos obrigatórios</span>
        </div>

        <div class="form-grid">
          <div class="field-group span2">
            <label>Instituição / Nome Singular *</label>
            <input type="text" id="input-inst"
              placeholder="Nome da instituição ou pessoa singular...">
          </div>

          <div class="field-group">
            <label>Nº do Ofício (se aplicável)</label>
            <input type="text" id="input-oficio"
              placeholder="Ex: Ofício 123/2025/SG">
          </div>

          <div class="field-group">
            <label>Tipo de Documento *</label>
            <select id="input-tipo">
              <option>Carta</option>
              <option>Ofício</option>
              <option>Despacho</option>
              <option>Nota de Cobrança</option>
              <option>Fatura</option>
              <option>Convite</option>
              <option>Solicitação para Estágio Voluntário</option>
              <option>Solicitação para Recolha de Dados</option>
              <option>Outro</option>
            </select>
          </div>

          <div class="field-group span2">
            <label>Assunto *</label>
            <textarea id="input-assunto" rows="2"
              placeholder="Breve descrição do assunto do documento..."></textarea>
          </div>

          <div class="field-group">
            <label>Data de Entrada *</label>
            <input type="date" id="input-data">
          </div>

          <div class="field-group">
            <label>Documento Anexo (+)</label>
            <input type="file" id="input-anexo"
              accept=".pdf,.doc,.docx,.jpg,.png,.jpeg,.txt,.xlsx">
          </div>
        </div>

        <div style="margin-top:16px;display:flex;gap:10px;">
          <button class="btn btn-primary" onclick="handleRegistar()">
            <svg style="width:13px;height:13px;stroke:currentColor;fill:none;stroke-width:2;
              stroke-linecap:round;stroke-linejoin:round" viewBox="0 0 24 24">
              <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
              <polyline points="17 21 17 13 7 13 7 21"/>
              <polyline points="7 3 7 8 15 8"/>
            </svg>
            Registar Documento
          </button>
          <button class="btn btn-outline" onclick="clearForm()">Limpar</button>
        </div>
      </div>

      <!-- Today's documents -->
      <div class="card">
        <div class="card-title">
          <svg style="width:14px;height:14px;stroke:currentColor;fill:none;stroke-width:2;
            stroke-linecap:round;stroke-linejoin:round" viewBox="0 0 24 24">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
            <line x1="16" y1="2" x2="16" y2="6"/>
            <line x1="8" y1="2" x2="8" y2="6"/>
            <line x1="3" y1="10" x2="21" y2="10"/>
          </svg>
          Documentos do Dia
          <span class="ct-badge" id="today-count-lbl"></span>
        </div>
        <div id="today-list" class="doc-list">
          <div class="no-data-msg">Nenhum documento registado para hoje.</div>
        </div>
      </div>
    </section>

    <!-- ── DESPACHO ── -->
    <section id="sec-despacho" class="section">
      <div class="page-header">
        <div class="page-title">📤 Despacho de Documentos</div>
        <div class="page-sub">Registe para onde cada documento foi despachado após a Direcção Geral</div>
      </div>

      <div class="card">
        <div class="filter-bar">
          <div class="field-group" style="flex:1;min-width:180px;">
            <label>Filtrar por Data de Entrada</label>
            <input type="date" id="desp-filter-data" onchange="renderDespacho()">
          </div>
          <div id="desp-kpis" style="display:flex;gap:8px;flex-wrap:wrap;align-items:flex-end;"></div>
        </div>
        <div id="desp-list" class="doc-list">
          <div class="no-data-msg">Selecione uma data para ver os documentos.</div>
        </div>
      </div>
    </section>

    <!-- ── PESQUISA ── -->
    <section id="sec-pesquisa" class="section">
      <div class="page-header">
        <div class="page-title">🔍 Pesquisar Documentos</div>
        <div class="page-sub">Pesquise por nome, assunto, ofício, tipo ou número de processo</div>
      </div>

      <div class="card">
        <div class="search-row">
          <div class="search-box">
            <div class="search-icon">
              <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/>
                <line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            </div>
            <input type="text" id="pesq-input"
              placeholder="Pesquisar por instituição, assunto, ofício ou nº de processo..."
              oninput="renderPesquisa()">
          </div>
          <div class="field-group" style="min-width:170px;">
            <label>Filtrar por Data</label>
            <input type="date" id="pesq-data" onchange="renderPesquisa()">
          </div>
          <button class="btn btn-outline btn-sm" onclick="clearPesquisa()">Limpar</button>
        </div>
        <div class="pesq-stats" id="pesq-stats"></div>
      </div>

      <div id="pesq-results" class="doc-list">
        <div class="no-data-msg">Digite algo para pesquisar ou selecione uma data.</div>
      </div>
    </section>

    <!-- ── DEFINIÇÕES ── -->
    <section id="sec-definicoes" class="section">
      <div class="page-header">
        <div class="page-title">⚙️ Definições do Sistema</div>
        <div class="page-sub">Configure a numeração de processos</div>
      </div>

      <div class="def-card">
        <div class="def-section-title">📋 Estatísticas Gerais</div>
        <div class="kpi-row" id="def-kpis"></div>
      </div>

      <div class="def-card">
        <div class="def-section-title">🔢 Numeração de Processos</div>
        <div class="form-grid">
          <div class="field-group">
            <label>Ano Actual</label>
            <input type="text" id="def-ano" readonly>
          </div>
          <div class="field-group">
            <label>Próximo Número a Atribuir</label>
            <input type="number" id="def-num-atual" min="1" step="1"
              placeholder="Ex: 589" oninput="updateDefPreview()">
          </div>
        </div>
        <div class="def-preview-box">
          <div>
            <div class="def-preview-lbl">O próximo processo será</div>
            <div class="def-preview-num" id="def-preview">—</div>
          </div>
        </div>
        <div class="def-info">
          ℹ️ No início de cada ano, actualize este número para o valor inicial definido para o novo ano.<br>
          Exemplo: Em 2025 iniciou em <strong>589</strong> — em 2026 poderá reiniciar em <strong>589</strong>
          ou outro valor conforme política interna do Hospital do Prenda.
        </div>
        <div style="margin-top:14px;">
          <button class="btn btn-primary" onclick="saveDefinicoes()">
            💾 Guardar Definições
          </button>
        </div>
      </div>

      <div class="def-card">
        <div class="def-section-title">📥 Exportar Dados</div>
        <div class="def-info" style="margin-bottom:12px;">
          Exporte todos os registos para um ficheiro JSON (backup / arquivo).
        </div>
        <button class="btn btn-outline btn-sm" onclick="exportarDados()">
          📥 Exportar JSON
        </button>
      </div>
    </section>

  </main>
</div>

<div id="toast"></div>

<script>
// ══════════════════════════════════════════════════════════
// STORAGE KEYS & CONSTANTS
// ══════════════════════════════════════════════════════════
var DOCS_KEY   = 'hp_secretaria_docs';
var CONFIG_KEY = 'hp_secretaria_cfg';

var AREAS = [
  'Recursos Humanos',
  'Direcção Científica e Pedagógica',
  'Direcção Administrativa',
  'Direcção Clínica',
  'Direcção de Enfermagem',
  'Outra Área'
];

// ══════════════════════════════════════════════════════════
// DATA HELPERS
// ══════════════════════════════════════════════════════════
function getConfig() {
  var raw = localStorage.getItem(CONFIG_KEY);
  if (raw) return JSON.parse(raw);
  return { numAtual: 1, ano: new Date().getFullYear() };
}
function saveConfig(c) { localStorage.setItem(CONFIG_KEY, JSON.stringify(c)); }

function getDocs() {
  var raw = localStorage.getItem(DOCS_KEY);
  return raw ? JSON.parse(raw) : [];
}
function saveDocs(d) { localStorage.setItem(DOCS_KEY, JSON.stringify(d)); }

function nextNumProcesso() {
  var c = getConfig();
  var n = c.numAtual;
  c.numAtual = n + 1;
  saveConfig(c);
  return n;
}
function fmtNum(num, ano) {
  return (ano || new Date().getFullYear()) + '/' + String(num).padStart(3,'0');
}
function todayKey() {
  return new Date().toISOString().slice(0,10);
}
function fmtDate(d) {
  if (!d) return '—';
  var p = d.split('-');
  return p[2]+'/'+p[1]+'/'+p[0];
}
function fmtTime() {
  var n = new Date();
  return String(n.getHours()).padStart(2,'0')+':'+String(n.getMinutes()).padStart(2,'0');
}
function uid() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2,6);
}

// ══════════════════════════════════════════════════════════
// TOAST
// ══════════════════════════════════════════════════════════
function toast(msg, type) {
  type = type || 'ok';
  var t = document.getElementById('toast');
  t.textContent = msg; t.className = 'toast-' + type;
  t.style.opacity = '1'; t.style.transform = 'translateY(0)';
  setTimeout(function() {
    t.style.opacity = '0'; t.style.transform = 'translateY(20px)';
  }, 3200);
}

// ══════════════════════════════════════════════════════════
// NAVIGATION
// ══════════════════════════════════════════════════════════
function showSection(id) {
  document.querySelectorAll('.section').forEach(function(s) { s.classList.remove('active'); });
  document.querySelectorAll('.nav-item').forEach(function(n) { n.classList.remove('active'); });
  document.getElementById(id).classList.add('active');
  document.querySelector('[data-section="'+id+'"]').classList.add('active');
  if (id === 'sec-despacho')  renderDespacho();
  if (id === 'sec-pesquisa')  renderPesquisa();
  if (id === 'sec-definicoes') renderDefinicoes();
}

// ══════════════════════════════════════════════════════════
// REGISTO
// ══════════════════════════════════════════════════════════
function initRegisto() {
  var cfg = getConfig();
  var ano = new Date().getFullYear();
  document.getElementById('preview-num').textContent = fmtNum(cfg.numAtual, ano);
  var sub = document.getElementById('preview-sub');
  if (sub) sub.textContent = 'Ano ' + ano;
  document.getElementById('input-data').value = todayKey();
  renderToday();
}

function handleRegistar() {
  var inst    = document.getElementById('input-inst').value.trim();
  var oficio  = document.getElementById('input-oficio').value.trim();
  var tipo    = document.getElementById('input-tipo').value;
  var assunto = document.getElementById('input-assunto').value.trim();
  var data    = document.getElementById('input-data').value;
  var fi      = document.getElementById('input-anexo').files;
  var nomeAnexo = (fi && fi.length) ? fi[0].name : '';

  if (!inst)    { toast('⚠ Preencha o campo Instituição / Nome Singular', 'err'); return; }
  if (!assunto) { toast('⚠ Preencha o campo Assunto', 'err'); return; }
  if (!data)    { toast('⚠ Selecione a data de entrada', 'err'); return; }

  var num = nextNumProcesso();
  var ano = new Date().getFullYear();
  var doc = {
    id: uid(), numProcesso: num, ano: ano,
    data: data, hora: fmtTime(),
    instituicao: inst, oficio: oficio,
    tipoDoc: tipo, assunto: assunto,
    nomeAnexo: nomeAnexo, despacho: null
  };

  var docs = getDocs();
  docs.unshift(doc);
  saveDocs(docs);
  clearForm();

  var newCfg = getConfig();
  document.getElementById('preview-num').textContent = fmtNum(newCfg.numAtual, ano);
  toast('✅ Registado — Processo ' + fmtNum(num, ano));
  renderToday();
}

function clearForm() {
  document.getElementById('input-inst').value = '';
  document.getElementById('input-oficio').value = '';
  document.getElementById('input-assunto').value = '';
  document.getElementById('input-anexo').value = '';
  document.getElementById('input-tipo').selectedIndex = 0;
}

function renderToday() {
  var d    = document.getElementById('input-data') ? document.getElementById('input-data').value : todayKey();
  var docs = getDocs().filter(function(x) { return x.data === d; });
  var lbl  = document.getElementById('today-count-lbl');
  if (lbl) lbl.textContent = docs.length ? docs.length + ' documento(s)' : '';
  var c = document.getElementById('today-list');
  if (!docs.length) {
    c.innerHTML = '<div class="no-data-msg">Nenhum documento registado para esta data.</div>';
    return;
  }
  c.innerHTML = docs.map(function(d) { return docCardSimple(d); }).join('');
}

function docCardSimple(d) {
  var numStr = fmtNum(d.numProcesso, d.ano);
  var desp = '';
  if (d.despacho) {
    desp = '<div class="doc-despacho-info">'
      +'<table class="desp-detail-table">'
      +'<tr><td>Despachado a</td><td>'+fmtDate(d.despacho.data)+'</td></tr>'
      +'<tr><td>Área</td><td>'+d.despacho.area+(d.despacho.outraArea?' — '+d.despacho.outraArea:'')+'</td></tr>'
      +(d.despacho.pessoa?'<tr><td>Responsável</td><td>'+d.despacho.pessoa+'</td></tr>':'')
      +'</table></div>';
  }
  return '<div class="doc-card '+(d.despacho?'doc-despachado':'doc-pendente')+'">'
    +'<div class="doc-card-header">'
    +'<span class="doc-num">'+numStr+'</span>'
    +'<span class="doc-tipo-badge">'+d.tipoDoc+'</span>'
    +'<span class="doc-data">'+fmtDate(d.data)+' '+(d.hora||'')+'</span>'
    +(d.despacho?'<span class="despachado-badge">✅ Despachado</span>':'<span class="pendente-badge">⏳ Pendente</span>')
    +'</div>'
    +'<div class="doc-card-body">'
    +'<div class="doc-inst"><strong>'+d.instituicao+'</strong></div>'
    +(d.oficio?'<div class="doc-oficio">Ofício: '+d.oficio+'</div>':'')
    +'<div class="doc-assunto">'+d.assunto+'</div>'
    +(d.nomeAnexo?'<div class="doc-anexo">📎 '+d.nomeAnexo+'</div>':'')
    +'</div>'
    +desp
    +'</div>';
}

// ══════════════════════════════════════════════════════════
// DESPACHO
// ══════════════════════════════════════════════════════════
function renderDespacho() {
  var flt  = document.getElementById('desp-filter-data') ? document.getElementById('desp-filter-data').value : todayKey();
  var docs = getDocs().filter(function(d) { return d.data === flt; });

  var kpis = document.getElementById('desp-kpis');
  if (kpis) {
    var pend = docs.filter(function(d) { return !d.despacho; }).length;
    var desp = docs.filter(function(d) { return  d.despacho; }).length;
    kpis.innerHTML =
      '<div class="kpi-box kpi-accent" style="min-width:80px;padding:8px 12px;">'
        +'<div class="kpi-label">Total</div><div class="kpi-val">'+docs.length+'</div></div>'
      +'<div class="kpi-box kpi-amber" style="min-width:80px;padding:8px 12px;">'
        +'<div class="kpi-label">Pendentes</div><div class="kpi-val">'+pend+'</div></div>'
      +'<div class="kpi-box kpi-green" style="min-width:80px;padding:8px 12px;">'
        +'<div class="kpi-label">Despachados</div><div class="kpi-val">'+desp+'</div></div>';
  }

  var c = document.getElementById('desp-list');
  if (!docs.length) {
    c.innerHTML = '<div class="no-data-msg">Nenhum documento para esta data.</div>';
    return;
  }
  // Pending first, dispatched last
  var sorted = docs.filter(function(d) { return !d.despacho; })
    .concat(docs.filter(function(d) { return d.despacho; }));
  c.innerHTML = sorted.map(function(d) { return despachableCard(d); }).join('');
}

function despachableCard(d) {
  var numStr   = fmtNum(d.numProcesso, d.ano);
  var areaOpts = AREAS.map(function(a) { return '<option value="'+a+'">'+a+'</option>'; }).join('');
  var eid      = d.id;

  if (d.despacho) {
    return '<div class="doc-card doc-despachado">'
      +'<div class="doc-card-header">'
        +'<span class="doc-num">'+numStr+'</span>'
        +'<span class="doc-tipo-badge">'+d.tipoDoc+'</span>'
        +'<span class="despachado-badge">✅ Despachado</span>'
        +'<span class="doc-data">'+fmtDate(d.data)+'</span>'
      +'</div>'
      +'<div class="doc-card-body">'
        +'<div class="doc-inst"><strong>'+d.instituicao+'</strong></div>'
        +(d.oficio?'<div class="doc-oficio">Ofício: '+d.oficio+'</div>':'')
        +'<div class="doc-assunto">'+d.assunto+'</div>'
      +'</div>'
      +'<div class="doc-despacho-info">'
        +'<table class="desp-detail-table">'
          +'<tr><td>Data de entrada</td><td>'+fmtDate(d.data)+'</td></tr>'
          +'<tr><td>Data de despacho</td><td>'+fmtDate(d.despacho.data)+'</td></tr>'
          +'<tr><td>Área / Destino</td><td>'+d.despacho.area+(d.despacho.outraArea?' — '+d.despacho.outraArea:'')+'</td></tr>'
          +(d.despacho.pessoa?'<tr><td>Responsável</td><td>'+d.despacho.pessoa+'</td></tr>':'')
        +'</table>'
        +'<button class="btn btn-outline btn-sm" style="margin-top:8px;" '
          +'onclick="undoDespacho(\''+eid+'\')">↩️ Anular Despacho</button>'
      +'</div>'
    +'</div>';
  }

  return '<div class="doc-card doc-pendente">'
    +'<div class="doc-card-header">'
      +'<span class="doc-num">'+numStr+'</span>'
      +'<span class="doc-tipo-badge">'+d.tipoDoc+'</span>'
      +'<span class="pendente-badge">⏳ Pendente</span>'
      +'<span class="doc-data">Entrada: '+fmtDate(d.data)+' '+(d.hora||'')+'</span>'
    +'</div>'
    +'<div class="doc-card-body">'
      +'<div class="doc-inst"><strong>'+d.instituicao+'</strong></div>'
      +(d.oficio?'<div class="doc-oficio">Ofício: '+d.oficio+'</div>':'')
      +'<div class="doc-assunto">'+d.assunto+'</div>'
    +'</div>'
    +'<div class="desp-form">'
      +'<div class="desp-form-row">'
        +'<div class="field-group">'
          +'<label>Data do Despacho</label>'
          +'<input type="date" id="dd-'+eid+'" value="'+todayKey()+'">'
        +'</div>'
        +'<div class="field-group">'
          +'<label>Área de Destino</label>'
          +'<select id="da-'+eid+'" onchange="toggleOutra(\''+eid+'\')">'+areaOpts+'</select>'
        +'</div>'
      +'</div>'
      +'<div class="desp-form-row" id="outra-wrap-'+eid+'" style="display:none;">'
        +'<div class="field-group">'
          +'<label>Especificar Área</label>'
          +'<input type="text" id="da-outra-'+eid+'" placeholder="Nome da área...">'
        +'</div>'
        +'<div class="field-group">'
          +'<label>Pessoa (opcional)</label>'
          +'<input type="text" id="dp2-'+eid+'" placeholder="Nome da pessoa...">'
        +'</div>'
      +'</div>'
      +'<div class="desp-form-row" id="pessoa-wrap-'+eid+'">'
        +'<div class="field-group">'
          +'<label>Pessoa (opcional)</label>'
          +'<input type="text" id="dp-'+eid+'" placeholder="Nome da pessoa responsável...">'
        +'</div>'
      +'</div>'
      +'<button class="btn-despachar" onclick="despacharDoc(\''+eid+'\')">📤 Despachar</button>'
    +'</div>'
  +'</div>';
}

function toggleOutra(id) {
  var area  = document.getElementById('da-'+id) ? document.getElementById('da-'+id).value : '';
  var wrap  = document.getElementById('outra-wrap-'+id);
  var pwrap = document.getElementById('pessoa-wrap-'+id);
  if (wrap)  wrap.style.display  = area === 'Outra Área' ? 'grid' : 'none';
  if (pwrap) pwrap.style.display = area === 'Outra Área' ? 'none' : 'grid';
}

function despacharDoc(id) {
  var data   = document.getElementById('dd-'+id)       ? document.getElementById('dd-'+id).value : '';
  var area   = document.getElementById('da-'+id)       ? document.getElementById('da-'+id).value : '';
  var outra  = document.getElementById('da-outra-'+id) ? document.getElementById('da-outra-'+id).value.trim() : '';
  var p1     = document.getElementById('dp-'+id)       ? document.getElementById('dp-'+id).value.trim() : '';
  var p2     = document.getElementById('dp2-'+id)      ? document.getElementById('dp2-'+id).value.trim() : '';
  var pessoa = p1 || p2;

  if (!data) { toast('⚠ Selecione a data do despacho', 'err'); return; }
  if (area === 'Outra Área' && !outra) { toast('⚠ Especifique o nome da área', 'err'); return; }

  var docs = getDocs();
  var i = docs.findIndex(function(d) { return d.id === id; });
  if (i === -1) return;
  docs[i].despacho = { data: data, area: area, outraArea: outra, pessoa: pessoa };
  saveDocs(docs);
  toast('✅ Documento despachado com sucesso!');
  renderDespacho();
}

function undoDespacho(id) {
  if (!confirm('Anular o despacho deste documento?')) return;
  var docs = getDocs();
  var i = docs.findIndex(function(d) { return d.id === id; });
  if (i === -1) return;
  docs[i].despacho = null;
  saveDocs(docs);
  toast('↩️ Despacho anulado');
  renderDespacho();
}

// ══════════════════════════════════════════════════════════
// PESQUISA
// ══════════════════════════════════════════════════════════
function renderPesquisa() {
  var qEl   = document.getElementById('pesq-input');
  var dEl   = document.getElementById('pesq-data');
  var q     = qEl ? qEl.value.toLowerCase().trim() : '';
  var fdata = dEl ? dEl.value : '';
  var all   = getDocs();
  var docs  = all;

  if (fdata) docs = docs.filter(function(d) { return d.data === fdata; });
  if (q) docs = docs.filter(function(d) {
    return d.instituicao.toLowerCase().includes(q)
      || d.assunto.toLowerCase().includes(q)
      || (d.oficio || '').toLowerCase().includes(q)
      || (d.tipoDoc || '').toLowerCase().includes(q)
      || String(d.numProcesso).includes(q)
      || fmtNum(d.numProcesso, d.ano).includes(q);
  });

  var statsEl = document.getElementById('pesq-stats');
  if (statsEl) {
    statsEl.textContent = docs.length === all.length
      ? all.length + ' documentos no total'
      : docs.length + ' resultado(s) de ' + all.length + ' documentos';
  }

  var c = document.getElementById('pesq-results');
  if (!docs.length) {
    c.innerHTML = '<div class="no-data-msg">Nenhum resultado encontrado.</div>';
    return;
  }
  c.innerHTML = docs.map(function(d) { return docCardFull(d); }).join('');
}

function clearPesquisa() {
  var pi = document.getElementById('pesq-input');
  var pd = document.getElementById('pesq-data');
  if (pi) pi.value = '';
  if (pd) pd.value = '';
  renderPesquisa();
}

function docCardFull(d) {
  var numStr = fmtNum(d.numProcesso, d.ano);
  var desp = '';
  if (d.despacho) {
    desp = '<div class="doc-despacho-info">'
      +'<table class="desp-detail-table">'
      +'<tr><td>Data de entrada</td><td>'+fmtDate(d.data)+' '+(d.hora||'')+'</td></tr>'
      +'<tr><td>Data de despacho</td><td>'+fmtDate(d.despacho.data)+'</td></tr>'
      +'<tr><td>Área / Destino</td><td>'+d.despacho.area+(d.despacho.outraArea?' — '+d.despacho.outraArea:'')+'</td></tr>'
      +(d.despacho.pessoa?'<tr><td>Responsável</td><td>'+d.despacho.pessoa+'</td></tr>':'')
      +'</table></div>';
  }
  return '<div class="doc-card '+(d.despacho?'doc-despachado':'doc-pendente')+'">'
    +'<div class="doc-card-header">'
    +'<span class="doc-num">'+numStr+'</span>'
    +'<span class="doc-tipo-badge">'+d.tipoDoc+'</span>'
    +'<span class="doc-data">'+fmtDate(d.data)+' '+(d.hora||'')+'</span>'
    +(d.despacho?'<span class="despachado-badge">✅ Despachado</span>':'<span class="pendente-badge">⏳ Pendente</span>')
    +'</div>'
    +'<div class="doc-card-body">'
    +'<div class="doc-inst"><strong>'+d.instituicao+'</strong></div>'
    +(d.oficio?'<div class="doc-oficio">Ofício: '+d.oficio+'</div>':'')
    +'<div class="doc-assunto">'+d.assunto+'</div>'
    +(d.nomeAnexo?'<div class="doc-anexo">📎 '+d.nomeAnexo+'</div>':'')
    +'</div>'
    +desp
    +'</div>';
}

// ══════════════════════════════════════════════════════════
// DEFINIÇÕES
// ══════════════════════════════════════════════════════════
function renderDefinicoes() {
  var cfg = getConfig();
  var ano = new Date().getFullYear();
  var anoEl = document.getElementById('def-ano');
  if (anoEl) anoEl.value = ano;
  var numEl = document.getElementById('def-num-atual');
  if (numEl) numEl.value = cfg.numAtual;
  updateDefPreview();

  var docs   = getDocs();
  var pend   = docs.filter(function(d) { return !d.despacho; }).length;
  var desp   = docs.filter(function(d) { return  d.despacho; }).length;
  var today  = docs.filter(function(d) { return d.data === todayKey(); }).length;

  var kpis = document.getElementById('def-kpis');
  if (kpis) {
    kpis.innerHTML =
      '<div class="kpi-box kpi-accent"><div class="kpi-label">Total Docs</div><div class="kpi-val">'+docs.length+'</div></div>'
      +'<div class="kpi-box kpi-amber"><div class="kpi-label">Pendentes</div><div class="kpi-val">'+pend+'</div></div>'
      +'<div class="kpi-box kpi-green"><div class="kpi-label">Despachados</div><div class="kpi-val">'+desp+'</div></div>'
      +'<div class="kpi-box"><div class="kpi-label">Hoje</div><div class="kpi-val">'+today+'</div></div>';
  }
}

function updateDefPreview() {
  var el = document.getElementById('def-num-atual');
  var n  = el ? parseInt(el.value) : NaN;
  var ano = new Date().getFullYear();
  var prev = document.getElementById('def-preview');
  if (prev) prev.textContent = (!isNaN(n) && n > 0) ? fmtNum(n, ano) : '—';
}

function saveDefinicoes() {
  var el = document.getElementById('def-num-atual');
  var n  = el ? parseInt(el.value) : NaN;
  if (isNaN(n) || n < 1) { toast('⚠ Número inválido', 'err'); return; }
  var cfg = getConfig();
  cfg.numAtual = n;
  saveConfig(cfg);
  updateDefPreview();
  var ano = new Date().getFullYear();
  var prev = document.getElementById('preview-num');
  if (prev) prev.textContent = fmtNum(n, ano);
  toast('✅ Definições guardadas');
}

function exportarDados() {
  var docs = getDocs();
  var cfg  = getConfig();
  var data = { config: cfg, documentos: docs, exportadoEm: new Date().toISOString() };
  var blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  var url  = URL.createObjectURL(blob);
  var a    = document.createElement('a');
  a.href = url;
  a.download = 'secretaria_geral_' + todayKey() + '.json';
  a.click();
  URL.revokeObjectURL(url);
  toast('📥 Dados exportados com sucesso');
}

// ══════════════════════════════════════════════════════════
// STAFF BAR
// ══════════════════════════════════════════════════════════
function loadStaffInfo() {
  var raw = localStorage.getItem('_staff');
  var d   = raw ? JSON.parse(raw) : {};
  var pi  = document.getElementById('inp-profissional');
  var ci  = document.getElementById('inp-chefe');
  if (pi) pi.value = d.profissional || '';
  if (ci) ci.value = d.chefe || '';
}
function saveStaffInfo() {
  var pi = document.getElementById('inp-profissional');
  var ci = document.getElementById('inp-chefe');
  localStorage.setItem('_staff', JSON.stringify({
    profissional: pi ? pi.value.trim() : '',
    chefe:        ci ? ci.value.trim() : ''
  }));
}
setTimeout(loadStaffInfo, 80);

// ══════════════════════════════════════════════════════════
// THEME
// ══════════════════════════════════════════════════════════
function toggleTheme() {
  var dark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', dark ? 'dark' : 'light');
  var btn = document.getElementById('theme-toggle');
  if (btn) btn.title = dark ? 'Mudar para tema claro' : 'Mudar para tema escuro';
}

// ══════════════════════════════════════════════════════════
// SPLASH RING ANIMATION
// ══════════════════════════════════════════════════════════
(function() {
  var DURATION = 5000;
  var ring  = document.getElementById('spl-ring');
  var pct   = document.getElementById('spl-pct');
  var CIRC  = 263.9;
  var start = null;
  if (!ring) return;
  function step(ts) {
    if (!start) start = ts;
    var p = Math.min((ts - start) / DURATION, 1);
    var e = p < 0.5 ? 2 * p * p : -1 + (4 - 2 * p) * p;
    ring.style.strokeDashoffset = CIRC * (1 - e);
    if (pct) pct.textContent = Math.round(e * 100) + '%';
    if (p < 1) { requestAnimationFrame(step); return; }
    var s = document.getElementById('splash');
    if (s) {
      s.style.transition = 'opacity .45s';
      s.style.opacity = '0';
      setTimeout(function() { s.style.display = 'none'; }, 450);
    }
  }
  requestAnimationFrame(step);
})();

// ══════════════════════════════════════════════════════════
// INIT
// ══════════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', function() {
  initRegisto();
  var dd = document.getElementById('desp-filter-data');
  if (dd) dd.value = todayKey();
  document.getElementById('input-data').addEventListener('change', renderToday);
});
</script>
</body>
</html>
'''

# Substitute placeholders
HTML = HTML.replace('__HOSP_IMG__', HOSP_IMG)
HTML = HTML.replace('__CIRC__', CIRC)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(HTML)

print(f'✓ Gerado: {OUT}')
print(f'  Tamanho: {os.path.getsize(OUT)/1024:.1f} KB')
