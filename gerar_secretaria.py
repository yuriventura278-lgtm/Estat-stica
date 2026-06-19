#!/usr/bin/env python3
"""Secretaria Geral v3 — gera secretaria_geral.html"""
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

CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
:root{
  --header-h:56px;--staff-h:38px;--sidebar-w:234px;
  --bg:#f4f6fa;--surface:#fff;--surface2:#f1f5f9;
  --border:#e2e8f0;--text:#0f172a;--muted:#64748b;
  --accent:#1a56db;--green:#10b981;--amber:#f59e0b;--red:#ef4444;--purple:#7c3aed;
  --fh:'Inter',sans-serif;--fm:'IBM Plex Mono',monospace;
  --shadow:0 1px 3px rgba(0,0,0,.08),0 4px 16px rgba(0,0,0,.06);
}
html.dark{--bg:#0c0f14;--surface:#141820;--surface2:#0f1520;--border:rgba(30,40,64,.9);--text:#e2e8f0;--muted:#64748b;}
body{font-family:var(--fh);background:var(--bg);color:var(--text);font-size:14px;line-height:1.5;transition:background .2s,color .2s;}
#splash{position:fixed;inset:0;z-index:9999;background:#0c0f14;display:flex;align-items:center;justify-content:center;}
.splash-inner{display:flex;flex-direction:column;align-items:center;gap:14px;text-align:center;}
.splash-img-ring{position:relative;width:100px;height:100px;}
.splash-img-circle{position:absolute;inset:8px;border-radius:50%;overflow:hidden;background:#1a2a3a;}
.splash-img-circle img{width:100%;height:100%;object-fit:cover;}
.splash-progress-svg{position:absolute;inset:0;width:100px;height:100px;transform:rotate(-90deg);}
.spl-ring-bg{fill:none;stroke:rgba(255,255,255,.12);stroke-width:4;}
.spl-ring-fg{fill:none;stroke:#00d4aa;stroke-width:4;stroke-linecap:round;}
.splash-hosp-lbl{font-size:.55rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:rgba(200,230,220,.65);}
.splash-svc-lbl{font-size:.9rem;font-weight:700;color:#fff;max-width:280px;line-height:1.35;}
.splash-pct{font-size:.65rem;color:#00d4aa;font-weight:600;font-family:var(--fm);}
.hp-staff-bar{position:fixed;top:0;left:0;right:0;z-index:190;height:var(--staff-h);background:rgba(26,86,219,.06);border-bottom:1px solid rgba(26,86,219,.15);display:flex;align-items:center;gap:12px;padding:0 20px;}
html.dark .hp-staff-bar{background:rgba(26,86,219,.1);}
.hp-staff-lbl{font-size:.46rem;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:1.4px;white-space:nowrap;}
.hp-staff-name{font-size:.72rem;font-weight:700;color:var(--accent);padding:2px 8px;background:rgba(26,86,219,.08);border-radius:4px;}
.hp-staff-sep{color:var(--border);font-size:.8rem;margin:0 4px;}
header{position:fixed;top:var(--staff-h);left:0;right:0;z-index:180;height:var(--header-h);background:var(--surface);border-bottom:1px solid var(--border);display:flex;align-items:center;padding:0 20px;gap:16px;box-shadow:0 1px 4px rgba(0,0,0,.06);}
html.dark header{background:#141820;border-bottom-color:#1e2840;}
.header-logo{width:32px;height:32px;border-radius:50%;overflow:hidden;flex-shrink:0;}
.header-logo img{width:100%;height:100%;object-fit:cover;}
.header-title{flex:1;}
.header-title h1{font-size:.78rem;font-weight:700;}
.header-title span{font-size:.56rem;color:var(--muted);}
.header-right{display:flex;align-items:center;gap:8px;margin-left:auto;}
.hbtn{padding:5px 11px;border-radius:4px;cursor:pointer;background:transparent;border:1px solid var(--border);color:var(--text);font-size:.57rem;font-weight:600;letter-spacing:.4px;text-transform:uppercase;display:inline-flex;align-items:center;gap:5px;white-space:nowrap;}
.hbtn:hover{border-color:var(--accent);color:var(--accent);}
.layout{display:flex;margin-top:calc(var(--staff-h) + var(--header-h));min-height:calc(100vh - var(--staff-h) - var(--header-h));}
.sidebar{width:var(--sidebar-w);flex-shrink:0;background:var(--surface);border-right:1px solid var(--border);padding:12px 0;position:sticky;top:calc(var(--staff-h)+var(--header-h));height:calc(100vh - var(--staff-h) - var(--header-h));overflow-y:auto;}
html.dark .sidebar{background:#141820;border-right-color:#1e2840;}
.nav-section-lbl{font-size:.46rem;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:var(--muted);padding:12px 18px 4px;}
.nav-item{display:flex;align-items:center;gap:9px;padding:8px 18px;cursor:pointer;font-size:.71rem;color:var(--muted);font-weight:500;transition:all .12s;border-left:3px solid transparent;}
.nav-item:hover{color:var(--text);background:var(--surface2);}
.nav-item.active{color:var(--accent);background:rgba(26,86,219,.06);border-left-color:var(--accent);font-weight:600;}
.nav-item svg{width:14px;height:14px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;flex-shrink:0;}
.main{flex:1;padding:22px;min-width:0;}
.section{display:none;max-width:960px;}
.section.active{display:block;}
.page-header{margin-bottom:18px;}
.page-title{font-size:1.02rem;font-weight:700;}
.page-sub{font-size:.67rem;color:var(--muted);margin-top:2px;}
.card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:18px;margin-bottom:14px;box-shadow:var(--shadow);}
html.dark .card{background:#141820;border-color:#1e2840;}
.card-title{font-size:.67rem;font-weight:700;text-transform:uppercase;letter-spacing:.09em;color:var(--muted);margin-bottom:12px;display:flex;align-items:center;gap:8px;}
.ct-right{margin-left:auto;font-size:.6rem;font-weight:500;color:var(--muted);text-transform:none;letter-spacing:normal;}
.num-preview{background:rgba(26,86,219,.07);border:1px solid rgba(26,86,219,.2);border-radius:10px;padding:12px 16px;display:flex;align-items:center;gap:16px;margin-bottom:14px;}
html.dark .num-preview{background:rgba(26,86,219,.11);border-color:rgba(26,86,219,.28);}
.num-preview-label{font-size:.57rem;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:.1em;}
.num-preview-val{font-family:var(--fm);font-size:1.5rem;font-weight:700;color:var(--accent);}
.num-preview-sub{font-size:.6rem;color:var(--muted);margin-top:1px;}
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
@media(max-width:620px){.form-grid{grid-template-columns:1fr;}}
.span2{grid-column:span 2;}
.field-group{display:flex;flex-direction:column;gap:4px;}
label{font-size:.57rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;}
input[type=text],input[type=date],input[type=number],input[type=password],select,textarea{background:var(--surface2);border:1px solid var(--border);color:var(--text);font-family:var(--fh);font-size:.77rem;padding:7px 11px;border-radius:7px;outline:none;width:100%;transition:border-color .13s;}
input:focus,select:focus,textarea:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(26,86,219,.1);}
textarea{resize:vertical;min-height:60px;}
html.dark input,html.dark select,html.dark textarea{background:rgba(255,255,255,.04);border-color:rgba(255,255,255,.1);}
input[readonly]{color:var(--muted);cursor:default;}
.btn{padding:8px 16px;border-radius:7px;cursor:pointer;font-family:var(--fh);font-size:.71rem;font-weight:600;border:none;transition:all .14s;display:inline-flex;align-items:center;gap:6px;}
.btn-primary{background:var(--accent);color:#fff;}
.btn-primary:hover{background:#1648c8;}
.btn-outline{background:transparent;color:var(--text);border:1px solid var(--border);}
.btn-outline:hover{border-color:var(--accent);color:var(--accent);}
.btn-danger{background:transparent;color:var(--red);border:1px solid rgba(239,68,68,.3);}
.btn-danger:hover{background:rgba(239,68,68,.08);}
.btn-sm{padding:5px 12px;font-size:.64rem;}
.btn-xs{padding:3px 8px;font-size:.6rem;}
input[type=file]{background:var(--surface2);border:1px dashed var(--border);color:var(--text);font-size:.71rem;padding:6px 11px;border-radius:7px;width:100%;cursor:pointer;}
input[type=file]:hover{border-color:var(--accent);}
.doc-list{display:flex;flex-direction:column;gap:8px;}
.doc-card{background:var(--surface);border:1px solid var(--border);border-radius:10px;overflow:hidden;}
html.dark .doc-card{background:#141820;border-color:#1e2840;}
.doc-card.doc-despachado{border-left:4px solid var(--green);}
.doc-card.doc-pendente{border-left:4px solid var(--amber);}
.doc-card.doc-recebido{border-left:4px solid var(--accent);}
.doc-card-header{display:flex;align-items:center;gap:7px;padding:8px 12px;background:var(--surface2);border-bottom:1px solid var(--border);flex-wrap:wrap;}
html.dark .doc-card-header{background:rgba(255,255,255,.03);border-bottom-color:#1e2840;}
.doc-num{font-family:var(--fm);font-size:.73rem;font-weight:700;color:var(--accent);background:rgba(26,86,219,.1);padding:2px 7px;border-radius:4px;white-space:nowrap;}
html.dark .doc-num{background:rgba(26,86,219,.18);}
.badge{font-size:.57rem;font-weight:600;padding:2px 7px;border-radius:10px;white-space:nowrap;}
.badge-tipo{background:rgba(0,212,170,.1);color:#00957a;text-transform:uppercase;letter-spacing:.04em;}
html.dark .badge-tipo{color:#00d4aa;}
.badge-desp{background:rgba(16,185,129,.1);color:#059669;}
html.dark .badge-desp{color:#34d399;}
.badge-pend{background:rgba(245,158,11,.1);color:#d97706;}
html.dark .badge-pend{color:#fbbf24;}
.badge-recv{background:rgba(26,86,219,.1);color:var(--accent);}
.badge-rh-jf{background:rgba(239,68,68,.1);color:#dc2626;}
.badge-rh-mf{background:rgba(139,92,246,.1);color:#7c3aed;}
.badge-rh-tt{background:rgba(14,165,233,.1);color:#0284c7;}
.badge-outro{background:rgba(100,116,139,.1);color:var(--muted);}
.rh-num{font-family:var(--fm);font-size:.73rem;font-weight:700;color:#7c3aed;background:rgba(139,92,246,.1);padding:2px 7px;border-radius:4px;}
html.dark .rh-num{background:rgba(139,92,246,.18);color:#a78bfa;}
.doc-data{font-size:.6rem;color:var(--muted);font-family:var(--fm);margin-left:auto;}
.doc-card-body{padding:10px 12px;}
.doc-inst{font-size:.8rem;font-weight:700;margin-bottom:3px;}
.doc-oficio{font-size:.66rem;color:var(--muted);font-family:var(--fm);margin-bottom:2px;}
.doc-assunto{font-size:.73rem;line-height:1.45;}
.doc-prof{font-size:.6rem;color:var(--muted);margin-top:4px;font-style:italic;}
.doc-footer{padding:8px 12px;border-top:1px solid var(--border);background:var(--surface2);display:flex;gap:6px;flex-wrap:wrap;align-items:center;}
html.dark .doc-footer{background:rgba(255,255,255,.02);}
.desp-info{padding:10px 12px;background:rgba(16,185,129,.04);border-top:1px solid var(--border);}
html.dark .desp-info{background:rgba(16,185,129,.06);}
.desp-form{padding:12px;border-top:1px solid var(--border);background:var(--surface2);}
html.dark .desp-form{background:rgba(255,255,255,.02);}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px;}
@media(max-width:580px){.grid2{grid-template-columns:1fr;}}
.btn-desp{background:var(--accent);color:#fff;padding:7px 16px;border-radius:7px;border:none;font-family:var(--fh);font-size:.71rem;font-weight:600;cursor:pointer;display:inline-flex;align-items:center;gap:5px;}
.btn-desp:hover{background:#1648c8;}
.dt-table{width:100%;border-collapse:collapse;font-size:.67rem;}
.dt-table td{padding:3px 7px;}
.dt-table td:first-child{color:var(--muted);font-weight:600;white-space:nowrap;width:130px;text-transform:uppercase;font-size:.56rem;letter-spacing:.05em;}
.filter-bar{display:flex;gap:10px;align-items:flex-end;flex-wrap:wrap;padding-bottom:12px;border-bottom:1px solid var(--border);margin-bottom:12px;}
.kpi-row{display:grid;grid-template-columns:repeat(auto-fill,minmax(100px,1fr));gap:8px;margin-bottom:14px;}
.kpi-box{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:10px 12px;text-align:center;}
html.dark .kpi-box{background:#141820;border-color:#1e2840;}
.kpi-label{font-size:.5rem;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin-bottom:3px;font-weight:600;}
.kpi-val{font-family:var(--fm);font-size:1.45rem;font-weight:700;}
.kpi-accent{border-color:rgba(26,86,219,.3);}
.kpi-accent .kpi-val{color:var(--accent);}
.kpi-green{border-color:rgba(16,185,129,.3);}
.kpi-green .kpi-val{color:var(--green);}
.kpi-amber{border-color:rgba(245,158,11,.3);}
.kpi-amber .kpi-val{color:var(--amber);}
.search-box{position:relative;flex:2;min-width:200px;}
.search-box input{padding-left:32px;}
.search-icon{position:absolute;left:10px;top:50%;transform:translateY(-50%);color:var(--muted);pointer-events:none;}
.search-icon svg{width:13px;height:13px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;}
.date-nav{display:flex;align-items:center;gap:6px;}
.date-nav-btn{padding:5px 10px;border-radius:6px;border:1px solid var(--border);background:transparent;cursor:pointer;color:var(--text);font-size:.8rem;}
.date-nav-btn:hover{border-color:var(--accent);color:var(--accent);}
.no-data{text-align:center;padding:24px;color:var(--muted);font-size:.77rem;background:var(--surface2);border-radius:10px;}
.area-sub-tabs{display:flex;border-bottom:2px solid var(--border);margin-bottom:16px;overflow-x:auto;}
.ast-btn{padding:8px 14px;border:none;background:transparent;cursor:pointer;font-family:var(--fh);font-size:.66rem;font-weight:600;color:var(--muted);border-bottom:2px solid transparent;margin-bottom:-2px;white-space:nowrap;transition:all .14s;}
.ast-btn:hover{color:var(--text);}
.ast-btn.active{color:var(--accent);border-bottom-color:var(--accent);}
.ast-panel{display:none;}
.ast-panel.active{display:block;}
.date-timeline{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px;}
.date-chip{display:flex;flex-direction:column;gap:1px;background:var(--surface2);border:1px solid var(--border);border-radius:6px;padding:5px 9px;}
.date-chip-lbl{font-size:.45rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);}
.date-chip-val{font-size:.7rem;font-weight:700;font-family:var(--fm);}
.date-chip.dc-desp{border-color:rgba(245,158,11,.4);}
.date-chip.dc-desp .date-chip-val{color:var(--amber);}
.date-chip.dc-recv{border-color:rgba(16,185,129,.4);}
.date-chip.dc-recv .date-chip-val{color:var(--green);}
.def-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:18px;margin-bottom:14px;}
html.dark .def-card{background:#141820;border-color:#1e2840;}
.def-section-title{font-size:.63rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--muted);margin-bottom:10px;padding-bottom:7px;border-bottom:1px solid var(--border);}
.prof-row{display:flex;align-items:center;gap:8px;padding:7px 0;border-bottom:1px solid var(--border);}
.prof-row:last-child{border-bottom:none;}
.prof-name{flex:1;font-size:.75rem;font-weight:600;}
.prof-badge{font-size:.57rem;background:rgba(26,86,219,.1);color:var(--accent);padding:2px 6px;border-radius:8px;font-weight:600;}
.notif-panel{background:rgba(245,158,11,.05);border:1px solid rgba(245,158,11,.2);border-radius:8px;padding:10px 14px;margin-bottom:14px;max-height:150px;overflow-y:auto;}
.notif-item{font-size:.68rem;color:var(--text);padding:3px 0;border-bottom:1px solid var(--border);}
.notif-item:last-child{border-bottom:none;}
.notif-ts{font-size:.58rem;color:var(--muted);font-family:var(--fm);}
.stats-period-bar{display:flex;gap:4px;flex-wrap:wrap;margin-bottom:14px;}
.spb{padding:5px 13px;border-radius:16px;border:1px solid var(--border);background:transparent;cursor:pointer;font-size:.66rem;font-weight:600;color:var(--muted);font-family:var(--fh);transition:all .14s;}
.spb:hover{border-color:var(--accent);color:var(--accent);}
.spb.active{background:var(--accent);color:#fff;border-color:var(--accent);}
.chart-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:16px;margin-bottom:14px;position:relative;}
html.dark .chart-card{background:#141820;border-color:#1e2840;}
.chart-title{font-size:.67rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:12px;}
.chart-wrap{position:relative;height:240px;}
.sum-table{width:100%;border-collapse:collapse;font-size:.71rem;}
.sum-table th{background:var(--surface2);padding:7px 10px;text-align:left;font-size:.59rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);font-weight:700;}
.sum-table td{padding:7px 10px;border-bottom:1px solid var(--border);}
.sum-table tr:last-child td{border-bottom:none;}
.modal-overlay{position:fixed;inset:0;z-index:10000;background:rgba(0,0,0,.78);backdrop-filter:blur(4px);display:flex;align-items:center;justify-content:center;}
.modal-box{background:var(--surface);border-radius:16px;padding:28px;width:380px;max-width:95vw;box-shadow:0 25px 60px rgba(0,0,0,.4);}
html.dark .modal-box{background:#141820;}
.modal-title{font-size:.92rem;font-weight:700;margin-bottom:3px;}
.modal-sub{font-size:.67rem;color:var(--muted);margin-bottom:18px;}
.modal-actions{display:flex;gap:8px;margin-top:16px;justify-content:flex-end;}
.edit-modal-box{background:var(--surface);border-radius:16px;padding:24px;width:540px;max-width:96vw;max-height:90vh;overflow-y:auto;box-shadow:0 25px 60px rgba(0,0,0,.4);}
html.dark .edit-modal-box{background:#141820;}
#toast{position:fixed;bottom:22px;right:22px;padding:10px 16px;border-radius:8px;font-size:.74rem;font-weight:600;z-index:9998;pointer-events:none;opacity:0;transform:translateY(20px);transition:all .3s;max-width:320px;}
.toast-ok{background:#059669;color:#fff;}
.toast-err{background:#dc2626;color:#fff;}
.toast-info{background:var(--accent);color:#fff;}
@media print{
  #splash,header,.hp-staff-bar,.sidebar,.modal-overlay,#toast{display:none!important;}
  .layout{margin:0;}
  .main{padding:0;}
  .section{display:none!important;}
  #sec-stats{display:block!important;}
  .no-print{display:none!important;}
}
"""


# ── HTML Sections ──
MODAL_LOGIN = """
<div id="login-modal" class="modal-overlay">
  <div class="modal-box">
    <div style="text-align:center;margin-bottom:18px;">
      <div style="width:56px;height:56px;border-radius:50%;overflow:hidden;margin:0 auto 10px;">
        <img src="__HOSP_IMG__" style="width:100%;height:100%;object-fit:cover;">
      </div>
      <div class="modal-title">Secretaria Geral</div>
      <div class="modal-sub">Hospital do Prenda &mdash; Autenticacao necessaria</div>
    </div>
    <div style="display:flex;flex-direction:column;gap:11px;">
      <div class="field-group">
        <label>Profissional</label>
        <select id="login-prof"></select>
      </div>
      <div class="field-group">
        <label>Senha</label>
        <input type="password" id="login-senha" placeholder="Digite a sua senha..."
          onkeydown="if(event.key==='Enter')doLogin()">
      </div>
      <div id="login-err" style="font-size:.7rem;color:var(--red);display:none;padding:6px 10px;background:rgba(239,68,68,.08);border-radius:6px;"></div>
      <button class="btn btn-primary" style="width:100%;justify-content:center;" onclick="doLogin()">Entrar</button>
    </div>
  </div>
</div>
"""

MODAL_EDIT = """
<div id="edit-modal" class="modal-overlay" style="display:none;">
  <div class="edit-modal-box">
    <div class="modal-title" id="edit-modal-title">Editar Documento</div>
    <div class="modal-sub" id="edit-modal-num"></div>
    <div class="form-grid" style="margin-top:14px;">
      <div class="field-group span2">
        <label>Instituicao / Nome Singular *</label>
        <input type="text" id="e-inst">
      </div>
      <div class="field-group">
        <label>N do Oficio</label>
        <input type="text" id="e-oficio">
      </div>
      <div class="field-group">
        <label>Tipo de Documento *</label>
        <select id="e-tipo" onchange="toggleEditTipo()">
          <option>Carta</option>
          <option>Oficio</option>
          <option>Ordem de Servico</option>
          <option>Nota de Cobranca</option>
          <option>Factura</option>
          <option>Convite</option>
          <option>Outro</option>
        </select>
      </div>
      <div id="e-tipo-extra-f" class="field-group" style="display:none;">
        <label id="e-tipo-extra-lbl">N / Descricao</label>
        <input type="text" id="e-tipo-extra">
      </div>
      <div class="field-group">
        <label>Assunto *</label>
        <select id="e-assunto" onchange="toggleEditAssunto()">
          <option>Solicitacao para Estagio Voluntario</option>
          <option>Solicitacao para Recolha de Dados</option>
          <option>Solicitacao para Subsidio de Ferias Antecipado</option>
          <option>Solicitacao para Declaracao de Trabalho</option>
          <option>Solicitacao para Amamentacao</option>
          <option>Solicitacao para Troca de Banco</option>
          <option>Solicitacao para Reforma</option>
          <option>Nota de Cobranca</option>
          <option>Factura</option>
          <option>Outro</option>
        </select>
      </div>
      <div id="e-assunto-extra-f" class="field-group" style="display:none;">
        <label id="e-assunto-extra-lbl">N / Descricao</label>
        <input type="text" id="e-assunto-extra">
      </div>
      <div class="field-group">
        <label>Data *</label>
        <input type="date" id="e-data">
      </div>
      <div class="field-group">
        <label>Documento Anexo</label>
        <input type="file" id="e-anexo">
      </div>
    </div>
    <div class="modal-actions">
      <button class="btn btn-outline btn-sm" onclick="closeEditModal()">Cancelar</button>
      <button class="btn btn-primary btn-sm" onclick="saveEdit()">Guardar Alteracoes</button>
    </div>
  </div>
</div>
"""

MODAL_VOLTOU = """
<div id="modal-voltou" class="modal-overlay" style="display:none;">
  <div class="modal" style="max-width:440px;">
    <div class="modal-title">Justificativo Devolvido</div>
    <p style="font-size:.72rem;color:var(--muted);margin-bottom:14px;">Indique o motivo / tipo de documento entregue pelo funcionario.</p>
    <div class="field-group" style="margin-bottom:14px;">
      <label>Motivo / Tipo de Justificativo *</label>
      <input type="text" id="voltou-motivo" placeholder="Ex: Atestado medico, Certidao de obito..."
             onkeydown="if(event.key==='Enter')confirmarVoltou()">
    </div>
    <div id="voltou-err" style="font-size:.7rem;color:var(--red);display:none;margin-bottom:10px;"></div>
    <div class="modal-actions">
      <button class="btn btn-outline" onclick="document.getElementById('modal-voltou').style.display='none'">Cancelar</button>
      <button class="btn btn-primary" onclick="confirmarVoltou()">Confirmar Devolucao</button>
    </div>
  </div>
</div>
"""

MODAL_IC_RESOLVE = """
<div id="modal-ic-resolve" class="modal-overlay" style="display:none;">
  <div class="modal" style="max-width:440px;">
    <div class="modal-title">Marcar como Resolvida</div>
    <p style="font-size:.72rem;color:var(--muted);margin-bottom:14px;">Descreva como a intercorrencia foi resolvida (opcional).</p>
    <div class="field-group" style="margin-bottom:14px;">
      <label>Descricao da Resolucao</label>
      <input type="text" id="ic-resolve-obs" placeholder="Como foi resolvida..."
             onkeydown="if(event.key==='Enter')confirmarResolverIC()">
    </div>
    <div class="modal-actions">
      <button class="btn btn-outline" onclick="document.getElementById('modal-ic-resolve').style.display='none'">Cancelar</button>
      <button class="btn btn-primary" style="background:#059669;" onclick="confirmarResolverIC()">Confirmar</button>
    </div>
  </div>
</div>
"""

SEC_DG = """
<section id="sec-dg" class="section active">
  <div class="page-header">
    <div class="page-title">Direccao Geral &mdash; Registo de Correspondencia</div>
    <div class="page-sub">Registe documentos recebidos e atribua numero de processo</div>
  </div>

  <div id="dg-notif" class="notif-panel" style="display:none;"></div>

  <div class="num-preview">
    <div>
      <div class="num-preview-label">Proximo N de Processo</div>
      <div class="num-preview-val" id="preview-num">---</div>
      <div class="num-preview-sub" id="preview-sub"></div>
    </div>
  </div>

  <div class="card">
    <div class="card-title">Novo Registo <span class="ct-right">* obrigatorio</span></div>
    <div class="form-grid">
      <div class="field-group span2">
        <label>Instituicao / Nome Singular *</label>
        <input type="text" id="input-inst" placeholder="Nome da instituicao ou pessoa singular...">
      </div>
      <div class="field-group">
        <label>N do Oficio</label>
        <input type="text" id="input-oficio" placeholder="Ex: Oficio 123/2025/SG">
      </div>
      <div class="field-group">
        <label>Tipo de Documento *</label>
        <select id="input-tipo" onchange="toggleTipo()">
          <option>Carta</option>
          <option>Oficio</option>
          <option>Ordem de Servico</option>
          <option>Nota de Cobranca</option>
          <option>Factura</option>
          <option>Convite</option>
          <option>Outro</option>
        </select>
      </div>
      <div id="tipo-extra-f" class="field-group" style="display:none;">
        <label id="tipo-extra-lbl">N / Descricao</label>
        <input type="text" id="input-tipo-extra" placeholder="...">
      </div>
      <div class="field-group">
        <label>Assunto *</label>
        <select id="input-assunto" onchange="toggleAssunto()">
          <option>Solicitacao para Estagio Voluntario</option>
          <option>Solicitacao para Recolha de Dados</option>
          <option>Solicitacao para Subsidio de Ferias Antecipado</option>
          <option>Solicitacao para Declaracao de Trabalho</option>
          <option>Solicitacao para Amamentacao</option>
          <option>Solicitacao para Troca de Banco</option>
          <option>Solicitacao para Reforma</option>
          <option>Nota de Cobranca</option>
          <option>Factura</option>
          <option>Outro</option>
        </select>
      </div>
      <div id="assunto-extra-f" class="field-group" style="display:none;">
        <label id="assunto-extra-lbl">N / Descricao</label>
        <input type="text" id="input-assunto-extra" placeholder="...">
      </div>
      <div class="field-group">
        <label>Data de Entrada *</label>
        <input type="date" id="input-data">
      </div>
      <div class="field-group">
        <label>Documento Anexo</label>
        <input type="file" id="input-anexo" accept=".pdf,.doc,.docx,.jpg,.png,.jpeg,.txt,.xlsx">
      </div>
    </div>
    <div style="margin-top:14px;display:flex;gap:8px;">
      <button class="btn btn-primary" onclick="handleRegistar()">Registar Documento</button>
      <button class="btn btn-outline" onclick="clearForm()">Limpar</button>
    </div>
  </div>

  <div class="card">
    <div class="card-title">
      Documentos do Dia
      <span class="ct-right" id="today-count-lbl"></span>
      <div class="date-nav" style="margin-left:auto;">
        <button class="date-nav-btn" onclick="shiftDay(-1)" title="Dia anterior">&lsaquo;</button>
        <input type="date" id="input-data-nav" style="width:140px;" onchange="renderToday()">
        <button class="date-nav-btn" onclick="shiftDay(1)" title="Proximo dia">&rsaquo;</button>
        <button class="btn btn-outline btn-xs" onclick="goToday()">Hoje</button>
      </div>
    </div>
    <div id="today-list" class="doc-list">
      <div class="no-data">Nenhum documento registado para esta data.</div>
    </div>
  </div>
</section>
"""

SEC_DESPACHO = """
<section id="sec-despacho" class="section">
  <div class="page-header">
    <div class="page-title">Despacho de Documentos</div>
    <div class="page-sub">Despache documentos para as areas do hospital</div>
  </div>
  <div class="card">
    <div class="filter-bar">
      <div class="field-group" style="min-width:160px;">
        <label>Data de Entrada</label>
        <input type="date" id="desp-filter-data" onchange="renderDespacho()">
      </div>
      <button class="btn btn-outline btn-sm" onclick="showAllPending()">Todos Pendentes</button>
      <button class="btn btn-outline btn-sm" onclick="goTodayDesp()">Hoje</button>
      <div id="desp-kpis" style="display:flex;gap:6px;flex-wrap:wrap;align-items:flex-end;margin-left:auto;"></div>
    </div>
    <div id="desp-list" class="doc-list">
      <div class="no-data">Selecione uma data ou clique em Todos Pendentes.</div>
    </div>
  </div>
</section>
"""

SEC_AREA = """
<section id="sec-area" class="section">
  <div class="page-header">
    <div class="page-title" id="area-page-title">Area Hospitalar</div>
    <div class="page-sub" id="area-page-sub">Documentos recebidos e registos internos</div>
  </div>
  <div class="area-sub-tabs">
    <button class="ast-btn active" data-atab="recebidos" onclick="switchAreaTab('recebidos')">Docs Recebidos DG</button>
    <button class="ast-btn" data-atab="internos" onclick="switchAreaTab('internos')">Documentos Internos</button>
    <button class="ast-btn" data-atab="stats" onclick="switchAreaTab('stats')">Estatisticas</button>
  </div>
  <div id="area-panel-recebidos" class="ast-panel active">
    <div class="card">
      <div class="filter-bar">
        <div class="field-group" style="min-width:160px;">
          <label>Filtrar por Data</label>
          <input type="date" id="area-filter-data" onchange="renderAreaReceived()">
        </div>
        <button class="btn btn-outline btn-sm" onclick="document.getElementById('area-filter-data').value='';renderAreaReceived()">Todos</button>
        <div id="area-kpis" style="display:flex;gap:6px;flex-wrap:wrap;align-items:flex-end;margin-left:auto;"></div>
      </div>
      <div id="area-docs-list" class="doc-list"><div class="no-data">Nenhum documento despachado para esta area.</div></div>
    </div>
  </div>
  <div id="area-panel-internos" class="ast-panel">
    <div class="card">
      <div class="card-title">Registar Documento Interno</div>
      <div class="form-grid">
        <div class="field-group">
          <label>Tipo *</label>
          <select id="area-int-tipo" onchange="toggleAreaTipo()">
            <option value="trocaturno">Troca de Turno</option>
            <option value="outro">Outro Documento</option>
          </select>
        </div>
        <div class="field-group"><label>Data *</label><input type="date" id="area-int-data"></div>
        <div id="area-int-nome-f" class="field-group"><label>Nome *</label><input type="text" id="area-int-nome" placeholder="Nome do profissional..."></div>
        <div id="area-int-servico-f" class="field-group"><label>Servico</label><input type="text" id="area-int-servico" placeholder="Servico..."></div>
        <div id="area-int-desc-f" class="field-group span2" style="display:none;"><label>Descricao *</label><textarea id="area-int-desc" rows="2"></textarea></div>
      </div>
      <div style="margin-top:12px;display:flex;gap:7px;">
        <button class="btn btn-primary btn-sm" onclick="registarInternoArea()">Registar</button>
        <button class="btn btn-outline btn-sm" onclick="clearAreaIntForm()">Limpar</button>
      </div>
    </div>
    <div class="card">
      <div class="filter-bar">
        <div class="field-group" style="min-width:160px;"><label>Filtrar por Data</label><input type="date" id="area-int-filter" onchange="renderAreaInternos()"></div>
        <button class="btn btn-outline btn-sm" onclick="document.getElementById('area-int-filter').value='';renderAreaInternos()">Todos</button>
      </div>
      <div id="area-internos-list" class="doc-list"><div class="no-data">Nenhum documento interno registado.</div></div>
    </div>
  </div>
  <div id="area-panel-stats" class="ast-panel">
    <div class="stats-period-bar" id="area-stats-periods">
      <button class="spb active" data-p="hoje" onclick="setAreaStatsPeriod('hoje')">Hoje</button>
      <button class="spb" data-p="semana" onclick="setAreaStatsPeriod('semana')">Semana</button>
      <button class="spb" data-p="mes" onclick="setAreaStatsPeriod('mes')">Mes</button>
      <button class="spb" data-p="trimestre" onclick="setAreaStatsPeriod('trimestre')">Trimestre</button>
      <button class="spb" data-p="semestre" onclick="setAreaStatsPeriod('semestre')">Semestre</button>
      <button class="spb" data-p="ano" onclick="setAreaStatsPeriod('ano')">Ano</button>
    </div>
    <div class="kpi-row" id="area-stats-kpis"></div>
    <div class="chart-card"><div class="chart-title">Documentos Recebidos por Periodo</div><div class="chart-wrap"><canvas id="area-chart-trend"></canvas></div></div>
  </div>
</section>
"""

SEC_RH = """
<section id="sec-rh" class="section">
  <div class="page-header">
    <div class="page-title">Recursos Humanos</div>
    <div class="page-sub">Documentos recebidos, justificacoes de falta, memorandos de ferias e registos internos</div>
  </div>
  <div class="area-sub-tabs">
    <button class="ast-btn active" data-rhtab="recebidos" onclick="switchRHTab('recebidos')">Docs Recebidos DG</button>
    <button class="ast-btn" data-rhtab="justfalta" onclick="switchRHTab('justfalta')">Justificacoes Falta</button>
    <button class="ast-btn" data-rhtab="memorandos" onclick="switchRHTab('memorandos')">Memorandos Ferias</button>
    <button class="ast-btn" data-rhtab="internos" onclick="switchRHTab('internos')">Outros Docs</button>
    <button class="ast-btn" data-rhtab="stats" onclick="switchRHTab('stats')">Estatisticas</button>
  </div>
  <div id="rh-panel-recebidos" class="ast-panel active">
    <div class="card">
      <div class="filter-bar">
        <div class="field-group" style="min-width:160px;"><label>Filtrar por Data</label><input type="date" id="rh-filter-data" onchange="renderRHReceived()"></div>
        <button class="btn btn-outline btn-sm" onclick="document.getElementById('rh-filter-data').value='';renderRHReceived()">Todos</button>
        <div id="rh-kpis" style="display:flex;gap:6px;flex-wrap:wrap;align-items:flex-end;margin-left:auto;"></div>
      </div>
      <div id="rh-docs-list" class="doc-list"><div class="no-data">Nenhum documento despachado para Recursos Humanos.</div></div>
    </div>
  </div>
  <div id="rh-panel-justfalta" class="ast-panel">
    <div class="card">
      <div class="card-title">Registar Justificacao de Falta</div>
      <div class="form-grid">
        <div class="field-group"><label>Nome *</label><input type="text" id="rh-jf-nome" placeholder="Nome do funcionario..."></div>
        <div class="field-group"><label>Area / Servico *</label><input type="text" id="rh-jf-area" placeholder="Area ou servico..."></div>
        <div class="field-group"><label>Data da Falta *</label><input type="date" id="rh-jf-data"></div>
        <div class="field-group"><label>Observacoes</label><input type="text" id="rh-jf-obs" placeholder="Motivo..."></div>
      </div>
      <div style="margin-top:12px;display:flex;gap:7px;">
        <button class="btn btn-primary btn-sm" onclick="registarJustFalta()">Registar</button>
        <button class="btn btn-outline btn-sm" onclick="clearJustFalta()">Limpar</button>
      </div>
    </div>
    <div class="card">
      <div class="filter-bar" style="flex-wrap:wrap;gap:8px;">
        <div class="field-group" style="min-width:160px;"><label>Filtrar por data</label><input type="date" id="rh-jf-filter" onchange="renderJustFaltas()"></div>
        <div style="display:flex;gap:6px;align-items:flex-end;">
          <button class="btn btn-sm" id="rh-jf-btn-todos" onclick="setJFFilter('todos')" style="background:var(--accent);color:#fff;">Todos</button>
          <button class="btn btn-outline btn-sm" id="rh-jf-btn-pendentes" onclick="setJFFilter('pendentes')">Pendentes</button>
          <button class="btn btn-outline btn-sm" id="rh-jf-btn-voltaram" onclick="setJFFilter('voltaram')">Voltaram</button>
          <button class="btn btn-outline btn-sm" onclick="document.getElementById('rh-jf-filter').value='';renderJustFaltas()">Limpar data</button>
        </div>
      </div>
      <div id="rh-jf-list" class="doc-list"><div class="no-data">Nenhuma justificacao registada.</div></div>
    </div>
  </div>
  <div id="rh-panel-memorandos" class="ast-panel">
    <div class="num-preview" style="background:rgba(139,92,246,.07);border-color:rgba(139,92,246,.25);">
      <div>
        <div class="num-preview-label" style="color:#7c3aed;">Proximo N de Memorando</div>
        <div class="num-preview-val" id="rh-memo-num-val" style="color:#7c3aed;">---</div>
        <div class="num-preview-sub" id="rh-memo-num-sub"></div>
      </div>
    </div>
    <div class="card">
      <div class="card-title">Registar Memorando de Ferias</div>
      <div class="form-grid">
        <div class="field-group"><label>Nome *</label><input type="text" id="rh-memo-nome" placeholder="Nome..."></div>
        <div class="field-group"><label>Area *</label><input type="text" id="rh-memo-area" placeholder="Area..."></div>
        <div class="field-group"><label>Periodo *</label><input type="text" id="rh-memo-tempo" placeholder="Ex: 01/07 a 15/07..."></div>
        <div class="field-group"><label>Data *</label><input type="date" id="rh-memo-data"></div>
        <div class="field-group span2"><label>Observacoes</label><textarea id="rh-memo-obs" rows="2"></textarea></div>
      </div>
      <div style="margin-top:12px;display:flex;gap:7px;">
        <button class="btn btn-primary btn-sm" onclick="registarMemorando()">Registar</button>
        <button class="btn btn-outline btn-sm" onclick="clearMemorando()">Limpar</button>
      </div>
    </div>
    <div class="card">
      <div class="filter-bar"><div class="field-group" style="min-width:160px;"><label>Filtrar</label><input type="date" id="rh-memo-filter" onchange="renderMemorandos()"></div><button class="btn btn-outline btn-sm" onclick="document.getElementById('rh-memo-filter').value='';renderMemorandos()">Todos</button></div>
      <div id="rh-memo-list" class="doc-list"><div class="no-data">Nenhum memorando registado.</div></div>
    </div>
  </div>
  <div id="rh-panel-internos" class="ast-panel">
    <div class="card">
      <div class="card-title">Registar Documento Interno</div>
      <div class="form-grid">
        <div class="field-group"><label>Tipo *</label><select id="rh-int-tipo" onchange="toggleRHTipo()"><option value="trocaturno">Troca de Turno</option><option value="outro">Outro</option></select></div>
        <div class="field-group"><label>Data *</label><input type="date" id="rh-int-data"></div>
        <div id="rh-int-nome-f" class="field-group"><label>Nome *</label><input type="text" id="rh-int-nome" placeholder="Nome..."></div>
        <div id="rh-int-servico-f" class="field-group"><label>Servico</label><input type="text" id="rh-int-servico" placeholder="Servico..."></div>
        <div id="rh-int-desc-f" class="field-group span2" style="display:none;"><label>Descricao *</label><textarea id="rh-int-desc" rows="2"></textarea></div>
      </div>
      <div style="margin-top:12px;display:flex;gap:7px;"><button class="btn btn-primary btn-sm" onclick="registarRHInterno()">Registar</button><button class="btn btn-outline btn-sm" onclick="clearRHIntForm()">Limpar</button></div>
    </div>
    <div class="card">
      <div class="filter-bar"><div class="field-group" style="min-width:160px;"><label>Filtrar</label><input type="date" id="rh-int-filter" onchange="renderRHInternos()"></div><button class="btn btn-outline btn-sm" onclick="document.getElementById('rh-int-filter').value='';renderRHInternos()">Todos</button></div>
      <div id="rh-int-list" class="doc-list"><div class="no-data">Nenhum documento registado.</div></div>
    </div>
  </div>
  <div id="rh-panel-stats" class="ast-panel">
    <div class="stats-period-bar" id="rh-stats-periods">
      <button class="spb active" data-p="hoje" onclick="setRHStatsPeriod('hoje')">Hoje</button>
      <button class="spb" data-p="semana" onclick="setRHStatsPeriod('semana')">Semana</button>
      <button class="spb" data-p="mes" onclick="setRHStatsPeriod('mes')">Mes</button>
      <button class="spb" data-p="trimestre" onclick="setRHStatsPeriod('trimestre')">Trimestre</button>
      <button class="spb" data-p="semestre" onclick="setRHStatsPeriod('semestre')">Semestre</button>
      <button class="spb" data-p="ano" onclick="setRHStatsPeriod('ano')">Ano</button>
    </div>
    <div class="kpi-row" id="rh-stats-kpis"></div>
    <div class="chart-card"><div class="chart-title">Documentos RH por Periodo</div><div class="chart-wrap"><canvas id="rh-chart-trend"></canvas></div></div>
  </div>
</section>
"""

SEC_INTERCORRENCIAS = """
<section id="sec-intercorrencias" class="section">
  <div class="page-header">
    <div class="page-title">Intercorrencias do Servico</div>
    <div class="page-sub">Registo diario de ocorrencias e intercorrencias da secretaria</div>
  </div>
  <div class="card">
    <div class="card-title">Intercorrencia do Dia</div>
    <div class="form-grid">
      <div class="field-group">
        <label>Data *</label>
        <input type="date" id="ic-data">
      </div>
      <div class="field-group">
        <label>Hora</label>
        <input type="time" id="ic-hora">
      </div>
      <div class="field-group span2">
        <label>Descricao da Intercorrencia *</label>
        <textarea id="ic-descricao" rows="4" placeholder="Descreva a intercorrencia do dia..."></textarea>
      </div>
    </div>
    <div style="margin-top:12px;display:flex;gap:7px;">
      <button class="btn btn-primary btn-sm" onclick="registarIntercorrencia()">Registar</button>
      <button class="btn btn-outline btn-sm" onclick="clearIC()">Limpar</button>
    </div>
  </div>
  <div class="card">
    <div class="filter-bar" style="flex-wrap:wrap;gap:8px;">
      <div class="field-group" style="min-width:160px;">
        <label>Filtrar por data</label>
        <input type="date" id="ic-filter-data" onchange="renderIntercorrencias()">
      </div>
      <div style="display:flex;gap:6px;align-items:flex-end;flex-wrap:wrap;">
        <button class="btn btn-sm" id="ic-btn-todos" onclick="setICFilter('todos')" style="background:var(--accent);color:#fff;">Todos</button>
        <button class="btn btn-outline btn-sm" id="ic-btn-pendentes" onclick="setICFilter('pendentes')">Pendentes</button>
        <button class="btn btn-outline btn-sm" id="ic-btn-resolvidos" onclick="setICFilter('resolvidos')">Resolvidos</button>
        <button class="btn btn-outline btn-sm" onclick="exportICPDF()">Exportar PDF</button>
        <button class="btn btn-outline btn-sm" onclick="document.getElementById('ic-filter-data').value='';renderIntercorrencias()">Limpar Data</button>
      </div>
    </div>
    <div id="ic-list" class="doc-list"><div class="no-data">Nenhuma intercorrencia registada.</div></div>
  </div>
</section>
"""

SEC_STATS = """
<section id="sec-stats" class="section">
  <div class="page-header">
    <div class="page-title">Estatisticas Gerais</div>
    <div class="page-sub">Analise de documentos por periodo — Direccao Geral</div>
  </div>
  <div class="card no-print">
    <div class="stats-period-bar">
      <button class="spb active" data-sp="hoje" onclick="setStatsPeriod('hoje')">Hoje</button>
      <button class="spb" data-sp="semana" onclick="setStatsPeriod('semana')">Semana</button>
      <button class="spb" data-sp="mes" onclick="setStatsPeriod('mes')">Mes</button>
      <button class="spb" data-sp="trimestre" onclick="setStatsPeriod('trimestre')">Trimestre</button>
      <button class="spb" data-sp="semestre" onclick="setStatsPeriod('semestre')">Semestre</button>
      <button class="spb" data-sp="ano" onclick="setStatsPeriod('ano')">Ano</button>
    </div>
    <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:10px;">
      <div class="field-group" style="min-width:140px;"><label>Data Inicio</label><input type="date" id="stats-from" onchange="renderStats()"></div>
      <div class="field-group" style="min-width:140px;"><label>Data Fim</label><input type="date" id="stats-to" onchange="renderStats()"></div>
    </div>
    <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:10px;align-items:center;">
      <span style="font-size:.65rem;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.06em;">Exportar PDF:</span>
      <button class="btn btn-outline btn-xs" onclick="exportPDF('hoje')">Diario</button>
      <button class="btn btn-outline btn-xs" onclick="exportPDF('semana')">Semanal</button>
      <button class="btn btn-outline btn-xs" onclick="exportPDF('mes')">Mensal</button>
      <button class="btn btn-outline btn-xs" onclick="exportPDF('trimestre')">Trimestral</button>
      <button class="btn btn-outline btn-xs" onclick="exportPDF('semestre')">Semestral</button>
      <button class="btn btn-outline btn-xs" onclick="exportPDF('ano')">Anual</button>
      <button class="btn btn-outline btn-xs" onclick="exportPDF('custom')">Periodo Actual</button>
    </div>
  </div>
  <div class="kpi-row" id="stats-kpis"></div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
    <div class="chart-card"><div class="chart-title">Por Tipo de Documento</div><div class="chart-wrap"><canvas id="stats-chart-tipo"></canvas></div></div>
    <div class="chart-card"><div class="chart-title">Por Assunto</div><div class="chart-wrap"><canvas id="stats-chart-assunto"></canvas></div></div>
  </div>
  <div class="chart-card"><div class="chart-title">Evolucao Diaria</div><div class="chart-wrap" style="height:200px;"><canvas id="stats-chart-trend"></canvas></div></div>
  <div class="card">
    <div class="card-title">Resumo por Tipo</div>
    <div id="stats-summary-table"></div>
  </div>
</section>
"""

SEC_PESQUISA = """
<section id="sec-pesquisa" class="section">
  <div class="page-header">
    <div class="page-title">Pesquisar Documentos</div>
    <div class="page-sub">Pesquise por instituicao, assunto, numero de processo ou area de despacho</div>
  </div>
  <div class="card">
    <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:flex-end;margin-bottom:12px;">
      <div class="search-box">
        <div class="search-icon"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></div>
        <input type="text" id="pesq-input" placeholder="Pesquisar por nome, assunto, n processo..." oninput="renderPesquisa()">
      </div>
      <div class="field-group" style="min-width:150px;"><label>Data</label><input type="date" id="pesq-data" onchange="renderPesquisa()"></div>
      <div class="field-group" style="min-width:160px;">
        <label>Area de Despacho</label>
        <select id="pesq-area" onchange="renderPesquisa()">
          <option value="">Todas as areas</option>
          <option>Recursos Humanos</option>
          <option>Direccao Cientifica e Pedagogica</option>
          <option>Direccao Administrativa</option>
          <option>Direccao Clinica</option>
          <option>Direccao de Enfermagem</option>
          <option>Outra Area</option>
        </select>
      </div>
      <button class="btn btn-outline btn-sm" onclick="clearPesquisa()">Limpar</button>
    </div>
    <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px;">
      <button class="btn btn-outline btn-xs" onclick="setPesqFilter('todos')">Todos</button>
      <button class="btn btn-outline btn-xs" id="pesq-btn-pend" onclick="setPesqFilter('pendentes')" style="border-color:var(--amber);color:#d97706;">Sem Despacho</button>
      <button class="btn btn-outline btn-xs" id="pesq-btn-desp" onclick="setPesqFilter('despachados')" style="border-color:var(--green);color:#059669;">Despachados</button>
      <button class="btn btn-outline btn-xs" id="pesq-btn-recv" onclick="setPesqFilter('recebidos')" style="border-color:var(--accent);color:var(--accent);">Recebidos pela Area</button>
    </div>
    <div id="pesq-stats" style="font-size:.65rem;color:var(--muted);"></div>
  </div>
  <div id="pesq-results" class="doc-list"><div class="no-data">Digite algo para pesquisar.</div></div>
</section>
"""

SEC_DEFINICOES = """
<section id="sec-definicoes" class="section">
  <div class="page-header">
    <div class="page-title">Definicoes do Sistema</div>
    <div class="page-sub">Configuracoes — acesso restrito ao chefe</div>
  </div>
  <div id="def-lock" class="card" style="max-width:400px;">
    <div class="card-title">Autenticacao Necessaria</div>
    <p style="font-size:.72rem;color:var(--muted);margin-bottom:14px;">
      As definicoes sao protegidas. Digite a senha de acesso para continuar.
    </p>
    <div class="field-group" style="margin-bottom:12px;">
      <label>Senha de Acesso</label>
      <input type="password" id="def-senha-input" placeholder="Digite a senha..." onkeydown="if(event.key==='Enter')unlockDef()">
    </div>
    <div id="def-lock-err" style="font-size:.7rem;color:var(--red);display:none;margin-bottom:10px;"></div>
    <button class="btn btn-primary btn-sm" onclick="unlockDef()">Aceder</button>
  </div>
  <div id="def-content" style="display:none;">
    <div class="def-card">
      <div class="def-section-title">Estatisticas Gerais</div>
      <div class="kpi-row" id="def-kpis"></div>
    </div>
    <div class="def-card">
      <div class="def-section-title">Numeracao de Processos</div>
      <div class="form-grid">
        <div class="field-group"><label>Ano Actual</label><input type="text" id="def-ano" readonly></div>
        <div class="field-group"><label>Proximo Numero</label><input type="number" id="def-num-atual" min="1" placeholder="Ex: 589" oninput="updateDefPreview()"></div>
      </div>
      <div style="margin-top:10px;padding:10px 14px;background:rgba(26,86,219,.06);border:1px dashed rgba(26,86,219,.3);border-radius:8px;display:flex;align-items:center;gap:10px;">
        <div>
          <div style="font-size:.57rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;font-weight:600;">O proximo processo sera</div>
          <div id="def-preview" style="font-family:var(--fm);font-size:1.3rem;font-weight:700;color:var(--accent);">---</div>
        </div>
      </div>
      <div style="margin-top:12px;"><button class="btn btn-primary btn-sm" onclick="saveDefinicoes()">Guardar</button></div>
    </div>
    <div class="def-card">
      <div class="def-section-title">Senha de Acesso as Definicoes</div>
      <div class="form-grid">
        <div class="field-group"><label>Nova Senha</label><input type="password" id="def-new-senha" placeholder="Nova senha..."></div>
        <div class="field-group"><label>Confirmar</label><input type="password" id="def-confirm-senha" placeholder="Confirmar senha..."></div>
      </div>
      <div style="margin-top:10px;"><button class="btn btn-outline btn-sm" onclick="saveSenha()">Actualizar Senha</button></div>
    </div>
    <div class="def-card">
      <div class="def-section-title">Gestao de Profissionais</div>
      <div id="prof-list" style="margin-bottom:14px;"></div>
      <div class="form-grid" style="max-width:520px;">
        <div class="field-group"><label>Nome do Profissional</label><input type="text" id="new-prof-nome" placeholder="Nome completo..."></div>
        <div class="field-group"><label>Senha</label><input type="password" id="new-prof-senha" placeholder="Senha de acesso..."></div>
      </div>
      <div style="margin-top:10px;"><button class="btn btn-primary btn-sm" onclick="addProfissional()">Adicionar Profissional</button></div>
    </div>
    <div class="def-card">
      <div class="def-section-title">Exportar e Backup</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;">
        <button class="btn btn-outline btn-sm" onclick="exportarDados()">Exportar JSON</button>
        <button class="btn btn-primary btn-sm" onclick="downloadBackup(false)">Backup Completo Agora</button>
      </div>
      <div id="backup-status" style="margin-bottom:12px;"></div>
      <div style="background:rgba(26,86,219,.06);border:1px dashed rgba(26,86,219,.3);border-radius:8px;padding:12px 14px;font-size:.7rem;color:var(--muted);">
        <strong style="color:var(--fg);">Backup automatico diario</strong><br>
        Todos os dias as 14:00 o sistema faz o download automatico do backup.<br>
        Guarde o ficheiro numa pasta segura ou envie para a nuvem (Google Drive, etc).<br><br>
        <button class="btn btn-outline btn-sm" onclick="requestNotifPerm()">Activar Notificacoes do Browser</button>
      </div>
    </div>
  </div>
</section>
"""


JS = r"""
// ═══ CONSTANTS ═══
var DOCS_KEY='hp_secretaria_docs', CFG_KEY='hp_secretaria_cfg', NOTIF_KEY='hp_notifs';
var AREAS=['Recursos Humanos','Direccao Cientifica e Pedagogica','Direccao Administrativa',
           'Direccao Clinica','Direccao de Enfermagem','Outra Area'];
var AREA_INFO={
  clinica:{label:'Direccao Clinica',sk:'hp_area_clinica',dn:'Direccao Clinica'},
  cientifica:{label:'Dir. Cientifica e Pedagogica',sk:'hp_area_cientifica',dn:'Direccao Cientifica e Pedagogica'},
  enfermagem:{label:'Dir. de Enfermagem',sk:'hp_area_enfermagem',dn:'Direccao de Enfermagem'},
  administrativa:{label:'Dir. Administrativa',sk:'hp_area_administrativa',dn:'Direccao Administrativa'},
  rh:{label:'Recursos Humanos',sk:'hp_area_rh',dn:'Recursos Humanos'}
};
var currentArea='clinica', currentAreaTab='recebidos', currentRHTab='recebidos';
var currentProfissional='', editDocId=null, statsCharts={}, areaStatsChart=null, rhStatsChart=null;
var pesqFilter='todos', statsPeriod='mes', areaStatsPeriod='mes', rhStatsPeriod='mes';

// ═══ DATA HELPERS ═══
function getConfig(){var def={numAtual:1,ano:new Date().getFullYear(),profissionais:[{id:'admin',nome:'Secretaria',senha:'1234'}],senhaChefe:'1234'};var r=localStorage.getItem(CFG_KEY);if(!r)return def;try{var c=JSON.parse(r);if(!c.profissionais||!c.profissionais.length)c.profissionais=def.profissionais;if(!c.senhaChefe)c.senhaChefe=def.senhaChefe;if(!c.numAtual)c.numAtual=def.numAtual;if(!c.ano)c.ano=def.ano;return c;}catch(e){return def;}}
function saveConfig(c){localStorage.setItem(CFG_KEY,JSON.stringify(c));}
// Migrate old config: fix old Administrador account name
(function(){var raw=localStorage.getItem('hp_secretaria_cfg');if(raw){try{var c=JSON.parse(raw);var changed=false;if(!c.profissionais||!c.profissionais.length){c.profissionais=[{id:'admin',nome:'Secretaria',senha:'1234'}];changed=true;}else if(c.profissionais.length===1&&c.profissionais[0].nome==='Administrador'){c.profissionais=[{id:'admin',nome:'Secretaria',senha:'1234'}];changed=true;}if(!c.senhaChefe){c.senhaChefe='1234';changed=true;}if(changed)localStorage.setItem('hp_secretaria_cfg',JSON.stringify(c));}catch(e){localStorage.removeItem('hp_secretaria_cfg');}}})();
function getDocs(){var r=localStorage.getItem(DOCS_KEY);return r?JSON.parse(r):[];}
function saveDocs(d){localStorage.setItem(DOCS_KEY,JSON.stringify(d));}
function getAreaDocs(k){var r=localStorage.getItem(AREA_INFO[k].sk);return r?JSON.parse(r):[];}
function saveAreaDocs(k,d){localStorage.setItem(AREA_INFO[k].sk,JSON.stringify(d));}
function getRHMemoCfg(){var r=localStorage.getItem('hp_rh_memo_cfg');return r?JSON.parse(r):{numAtual:1,ano:new Date().getFullYear()};}
function saveRHMemoCfg(c){localStorage.setItem('hp_rh_memo_cfg',JSON.stringify(c));}
function nextNum(){var c=getConfig();var n=c.numAtual;c.numAtual=n+1;saveConfig(c);return n;}
function nextRHNum(){var c=getRHMemoCfg();var n=c.numAtual;c.numAtual=n+1;saveRHMemoCfg(c);return n;}
function fmtNum(n,y){return (y||new Date().getFullYear())+'/'+String(n).padStart(3,'0');}
function fmtRH(n,y){return 'RH/'+(y||new Date().getFullYear())+'/'+String(n).padStart(3,'0');}
function todayKey(){return new Date().toISOString().slice(0,10);}
function fmtDate(d){if(!d)return '---';var p=d.split('-');return p[2]+'/'+p[1]+'/'+p[0];}
function fmtTime(){var n=new Date();return String(n.getHours()).padStart(2,'0')+':'+String(n.getMinutes()).padStart(2,'0');}
function uid(){return Date.now().toString(36)+Math.random().toString(36).slice(2,6);}
function addNotif(msg){var ns=JSON.parse(localStorage.getItem(NOTIF_KEY)||'[]');ns.unshift({ts:new Date().toISOString(),msg:msg});if(ns.length>50)ns=ns.slice(0,50);localStorage.setItem(NOTIF_KEY,JSON.stringify(ns));}
function getDateRange(period){
  var now=new Date(),end=todayKey(),start;
  if(period==='hoje')return{start:end,end:end};
  if(period==='semana'){var d=new Date(now);d.setDate(d.getDate()-6);return{start:d.toISOString().slice(0,10),end:end};}
  if(period==='mes')return{start:new Date(now.getFullYear(),now.getMonth(),1).toISOString().slice(0,10),end:end};
  if(period==='trimestre'){var q=Math.floor(now.getMonth()/3);return{start:new Date(now.getFullYear(),q*3,1).toISOString().slice(0,10),end:end};}
  if(period==='semestre'){var s=now.getMonth()<6?0:6;return{start:new Date(now.getFullYear(),s,1).toISOString().slice(0,10),end:end};}
  if(period==='ano')return{start:new Date(now.getFullYear(),0,1).toISOString().slice(0,10),end:end};
  return{start:end,end:end};
}

// ═══ TOAST ═══
function toast(msg,type){type=type||'ok';var t=document.getElementById('toast');t.textContent=msg;t.className='toast-'+(type==='err'?'err':type==='info'?'info':'ok');t.style.opacity='1';t.style.transform='translateY(0)';setTimeout(function(){t.style.opacity='0';t.style.transform='translateY(20px)';},3200);}

// ═══ AUTH ═══
function initLoginModal(){
  var cfg=getConfig();
  var sel=document.getElementById('login-prof');
  if(!sel)return;
  sel.innerHTML=cfg.profissionais.map(function(p){return '<option value="'+p.id+'">'+p.nome+'</option>';}).join('');
}
function doLogin(){
  var cfg=getConfig();
  var selEl=document.getElementById('login-prof');
  var senhaEl=document.getElementById('login-senha');
  var errEl=document.getElementById('login-err');
  if(!selEl||!senhaEl)return;
  var pid=selEl.value;
  var senha=senhaEl.value;
  var prof=cfg.profissionais.find(function(p){return p.id===pid;});
  if(!prof||prof.senha!==senha){
    errEl.style.display='block';errEl.textContent='Senha incorrecta. Tente novamente.';
    senhaEl.value='';senhaEl.focus();return;
  }
  currentProfissional=prof.nome;
  sessionStorage.setItem('hp_prof',prof.nome);
  document.getElementById('login-modal').style.display='none';
  document.getElementById('staff-prof-name').textContent=prof.nome;
  toast('Bem-vindo(a), '+prof.nome+'!','info');
  initRegisto();
}
function checkSession(){
  var p=sessionStorage.getItem('hp_prof');
  if(p){currentProfissional=p;document.getElementById('login-modal').style.display='none';var n=document.getElementById('staff-prof-name');if(n)n.textContent=p;}
  else{initLoginModal();}
}
function doLogout(){sessionStorage.removeItem('hp_prof');currentProfissional='';location.reload();}

// ═══ NAVIGATION ═══
function showSection(id){
  document.querySelectorAll('.section').forEach(function(s){s.classList.remove('active');});
  document.querySelectorAll('.nav-item').forEach(function(n){n.classList.remove('active');});
  var sec=document.getElementById(id);if(sec)sec.classList.add('active');
  var nav=document.querySelector('[data-section="'+id+'"]');if(nav)nav.classList.add('active');
  if(id==='sec-despacho')renderDespacho();
  if(id==='sec-pesquisa')renderPesquisa();
  if(id==='sec-stats')renderStats();
  if(id==='sec-definicoes')renderDefinicoes();
  if(id==='sec-rh')renderRH();
  if(id==='sec-intercorrencias')renderIntercorrencias();
}
function showArea(key){
  document.querySelectorAll('.section').forEach(function(s){s.classList.remove('active');});
  document.querySelectorAll('.nav-item').forEach(function(n){n.classList.remove('active');});
  document.getElementById('sec-area').classList.add('active');
  var ni=document.querySelector('[data-area="'+key+'"]');if(ni)ni.classList.add('active');
  currentArea=key;
  var info=AREA_INFO[key];
  var th=document.getElementById('area-page-title');if(th)th.textContent=info.label;
  var ts=document.getElementById('area-page-sub');if(ts)ts.textContent='Documentos recebidos da Direccao Geral e registos internos';
  var fd=document.getElementById('area-filter-data');if(fd)fd.value=todayKey();
  switchAreaTab('recebidos');
}

// ═══ FORM CONDITIONALS ═══
function toggleTipo(){
  var v=(document.getElementById('input-tipo')||{}).value||'';
  var f=document.getElementById('tipo-extra-f');
  var l=document.getElementById('tipo-extra-lbl');
  if(!f)return;
  if(v==='Nota de Cobranca'||v==='Factura'){f.style.display='';if(l)l.textContent='N do Documento';}
  else if(v==='Outro'){f.style.display='';if(l)l.textContent='Descricao';}
  else f.style.display='none';
}
function toggleAssunto(){
  var v=(document.getElementById('input-assunto')||{}).value||'';
  var f=document.getElementById('assunto-extra-f');
  var l=document.getElementById('assunto-extra-lbl');
  if(!f)return;
  if(v==='Nota de Cobranca'||v==='Factura'){f.style.display='';if(l)l.textContent='N do Documento';}
  else if(v==='Outro'){f.style.display='';if(l)l.textContent='Descricao';}
  else f.style.display='none';
}
function toggleEditTipo(){
  var v=(document.getElementById('e-tipo')||{}).value||'';
  var f=document.getElementById('e-tipo-extra-f');var l=document.getElementById('e-tipo-extra-lbl');
  if(!f)return;
  if(v==='Nota de Cobranca'||v==='Factura'){f.style.display='';if(l)l.textContent='N do Documento';}
  else if(v==='Outro'){f.style.display='';if(l)l.textContent='Descricao';}
  else f.style.display='none';
}
function toggleEditAssunto(){
  var v=(document.getElementById('e-assunto')||{}).value||'';
  var f=document.getElementById('e-assunto-extra-f');var l=document.getElementById('e-assunto-extra-lbl');
  if(!f)return;
  if(v==='Nota de Cobranca'||v==='Factura'){f.style.display='';if(l)l.textContent='N do Documento';}
  else if(v==='Outro'){f.style.display='';if(l)l.textContent='Descricao';}
  else f.style.display='none';
}
function fmtAssunto(doc){
  var a=doc.assunto||'';
  if((a==='Nota de Cobranca'||a==='Factura')&&doc.assuntoExtra)return a+' N '+doc.assuntoExtra;
  if(a==='Outro'&&doc.assuntoExtra)return doc.assuntoExtra;
  return a;
}
function fmtTipoExtra(doc){
  var t=doc.tipoDoc||'';
  if((t==='Nota de Cobranca'||t==='Factura')&&doc.tipoDocExtra)return ' N '+doc.tipoDocExtra;
  if(t==='Outro'&&doc.tipoDocExtra)return ' ('+doc.tipoDocExtra+')';
  return '';
}

// ═══ REGISTO ═══
function initRegisto(){
  var cfg=getConfig();var ano=new Date().getFullYear();
  var pn=document.getElementById('preview-num');if(pn)pn.textContent=fmtNum(cfg.numAtual,ano);
  var ps=document.getElementById('preview-sub');if(ps)ps.textContent='Ano '+ano;
  var id=document.getElementById('input-data');if(id)id.value=todayKey();
  var idn=document.getElementById('input-data-nav');if(idn)idn.value=todayKey();
  renderToday();renderNotifs();
}
function handleRegistar(){
  if(!currentProfissional){toast('Faca login primeiro','err');return;}
  var inst=((document.getElementById('input-inst')||{}).value||'').trim();
  var oficio=((document.getElementById('input-oficio')||{}).value||'').trim();
  var tipo=(document.getElementById('input-tipo')||{}).value||'';
  var tipoExtra=((document.getElementById('input-tipo-extra')||{}).value||'').trim();
  var assunto=(document.getElementById('input-assunto')||{}).value||'';
  var assuntoExtra=((document.getElementById('input-assunto-extra')||{}).value||'').trim();
  var data=(document.getElementById('input-data')||{}).value||'';
  var fi=(document.getElementById('input-anexo')||{}).files;
  var nomeAnexo=fi&&fi.length?fi[0].name:'';
  if(!inst){toast('Preencha Instituicao / Nome Singular','err');return;}
  if(!data){toast('Selecione a data','err');return;}
  if((tipo==='Nota de Cobranca'||tipo==='Factura')&&!tipoExtra){toast('Preencha o N do documento','err');return;}
  if((assunto==='Nota de Cobranca'||assunto==='Factura')&&!assuntoExtra){toast('Preencha o N do assunto','err');return;}
  var num=nextNum();var ano=new Date().getFullYear();
  var doc={id:uid(),numProcesso:num,ano:ano,data:data,hora:fmtTime(),profissional:currentProfissional,
    instituicao:inst,oficio:oficio,tipoDoc:tipo,tipoDocExtra:tipoExtra,
    assunto:assunto,assuntoExtra:assuntoExtra,nomeAnexo:nomeAnexo,
    despacho:null,recepcao:null,historico:[]};
  var docs=getDocs();docs.unshift(doc);saveDocs(docs);
  clearForm();
  var pn=document.getElementById('preview-num');if(pn)pn.textContent=fmtNum(getConfig().numAtual,ano);
  toast('Registado — Processo '+fmtNum(num,ano));
  addNotif('Novo registo: Processo '+fmtNum(num,ano)+' por '+currentProfissional);
  renderToday();renderNotifs();
}
function clearForm(){
  ['input-inst','input-oficio','input-tipo-extra','input-assunto-extra'].forEach(function(id){var el=document.getElementById(id);if(el)el.value='';});
  var t=document.getElementById('input-tipo');if(t)t.selectedIndex=0;
  var a=document.getElementById('input-assunto');if(a)a.selectedIndex=0;
  var f=document.getElementById('input-anexo');if(f)f.value='';
  toggleTipo();toggleAssunto();
}
function shiftDay(d){
  var el=document.getElementById('input-data-nav');if(!el)return;
  var dt=new Date(el.value+'T12:00:00');dt.setDate(dt.getDate()+d);
  el.value=dt.toISOString().slice(0,10);renderToday();
}
function goToday(){var el=document.getElementById('input-data-nav');if(el){el.value=todayKey();renderToday();}}
function renderToday(){
  var nav=document.getElementById('input-data-nav');
  var d=nav?nav.value:todayKey();
  var docs=getDocs().filter(function(x){return x.data===d;});
  var lbl=document.getElementById('today-count-lbl');if(lbl)lbl.textContent=docs.length?docs.length+' doc(s)':'';
  var c=document.getElementById('today-list');if(!c)return;
  if(!docs.length){c.innerHTML='<div class="no-data">Nenhum documento para esta data.</div>';return;}
  c.innerHTML=docs.map(function(d){return docCardSimple(d,true);}).join('');
}
function renderNotifs(){
  var ns=JSON.parse(localStorage.getItem(NOTIF_KEY)||'[]');
  var panel=document.getElementById('dg-notif');if(!panel)return;
  if(!ns.length){panel.style.display='none';return;}
  panel.style.display='block';
  panel.innerHTML=ns.slice(0,8).map(function(n){
    var ts=n.ts?new Date(n.ts).toLocaleString('pt-AO',{day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'}):'';
    return '<div class="notif-item"><span class="notif-ts">'+ts+'</span> — '+n.msg+'</div>';
  }).join('');
}

// ═══ DOC CARDS ═══
function docCardSimple(d,editable){
  var numStr=fmtNum(d.numProcesso,d.ano);
  var assuntoStr=fmtAssunto(d);var tipoStr=d.tipoDoc+fmtTipoExtra(d);
  var despInfo='';
  if(d.despacho){
    despInfo='<div class="desp-info"><table class="dt-table">'
      +'<tr><td>Despachado a</td><td>'+fmtDate(d.despacho.data)+'</td></tr>'
      +'<tr><td>Area</td><td>'+d.despacho.area+(d.despacho.outraArea?' — '+d.despacho.outraArea:'')+'</td></tr>'
      +(d.despacho.pessoa?'<tr><td>Responsavel</td><td>'+d.despacho.pessoa+'</td></tr>':'')
      +(d.despacho.nomeAnexo?'<tr><td>Doc. Despacho</td><td>'+d.despacho.nomeAnexo+'</td></tr>':'')
      +'</table></div>';
  }
  var footer='';
  if(editable){
    footer='<div class="doc-footer">'
      +(d.profissional?'<span style="font-size:.62rem;color:var(--muted);">'+d.profissional+'</span>':'')
      +'<button class="btn btn-outline btn-xs" style="margin-left:auto;" onclick="openEdit(\''+d.id+'\')">Editar</button>'
      +'<button class="btn btn-danger btn-xs" onclick="eliminarDoc(\''+d.id+'\')">Eliminar</button>'
    +'</div>';
  }
  return '<div class="doc-card '+(d.despacho?'doc-despachado':'doc-pendente')+'">'
    +'<div class="doc-card-header">'
      +'<span class="doc-num">'+numStr+'</span>'
      +'<span class="badge badge-tipo">'+tipoStr+'</span>'
      +'<span class="doc-data">'+fmtDate(d.data)+' '+(d.hora||'')+'</span>'
      +(d.despacho?'<span class="badge badge-desp">Despachado</span>':'<span class="badge badge-pend">Pendente</span>')
    +'</div>'
    +'<div class="doc-card-body">'
      +'<div class="doc-inst"><strong>'+d.instituicao+'</strong></div>'
      +(d.oficio?'<div class="doc-oficio">Oficio: '+d.oficio+'</div>':'')
      +'<div class="doc-assunto">'+assuntoStr+'</div>'
      +(d.nomeAnexo?'<div style="font-size:.62rem;color:var(--muted);margin-top:4px;">'+d.nomeAnexo+'</div>':'')
    +'</div>'
    +despInfo+footer
  +'</div>';
}

// ═══ EDIT / DELETE ═══
function openEdit(id){
  var docs=getDocs();var doc=docs.find(function(d){return d.id===id;});
  if(!doc)return;editDocId=id;
  var setVal=function(eid,v){var el=document.getElementById(eid);if(el)el.value=v||'';};
  setVal('e-inst',doc.instituicao);setVal('e-oficio',doc.oficio);
  setVal('e-tipo-extra',doc.tipoDocExtra);setVal('e-assunto-extra',doc.assuntoExtra);
  setVal('e-data',doc.data);
  var et=document.getElementById('e-tipo');
  if(et){for(var i=0;i<et.options.length;i++)if(et.options[i].value===doc.tipoDoc)et.selectedIndex=i;}
  var ea=document.getElementById('e-assunto');
  if(ea){for(var i=0;i<ea.options.length;i++)if(ea.options[i].value===doc.assunto)ea.selectedIndex=i;}
  toggleEditTipo();toggleEditAssunto();
  var mn=document.getElementById('edit-modal-num');if(mn)mn.textContent='Processo '+fmtNum(doc.numProcesso,doc.ano);
  document.getElementById('edit-modal').style.display='flex';
}
function closeEditModal(){document.getElementById('edit-modal').style.display='none';editDocId=null;}
function saveEdit(){
  if(!editDocId)return;
  var docs=getDocs();var i=docs.findIndex(function(d){return d.id===editDocId;});if(i===-1)return;
  var inst=((document.getElementById('e-inst')||{}).value||'').trim();
  if(!inst){toast('Preencha a instituicao','err');return;}
  var old=docs[i];
  docs[i]=Object.assign({},old,{
    instituicao:inst,oficio:((document.getElementById('e-oficio')||{}).value||'').trim(),
    tipoDoc:(document.getElementById('e-tipo')||{}).value||old.tipoDoc,
    tipoDocExtra:((document.getElementById('e-tipo-extra')||{}).value||'').trim(),
    assunto:(document.getElementById('e-assunto')||{}).value||old.assunto,
    assuntoExtra:((document.getElementById('e-assunto-extra')||{}).value||'').trim(),
    data:(document.getElementById('e-data')||{}).value||old.data,
  });
  var hist=docs[i].historico||[];
  hist.unshift({ts:new Date().toISOString(),profissional:currentProfissional,acao:'Editado'});
  docs[i].historico=hist;
  saveDocs(docs);
  addNotif('Processo '+fmtNum(old.numProcesso,old.ano)+' editado por '+currentProfissional);
  toast('Documento actualizado');closeEditModal();renderToday();renderNotifs();
}
function eliminarDoc(id){
  if(!confirm('Eliminar este documento? Esta accao nao pode ser desfeita.'))return;
  var docs=getDocs();var doc=docs.find(function(d){return d.id===id;});
  var numStr=doc?fmtNum(doc.numProcesso,doc.ano):'';
  saveDocs(docs.filter(function(d){return d.id!==id;}));
  addNotif('Processo '+numStr+' eliminado por '+currentProfissional);
  toast('Documento eliminado');renderToday();renderNotifs();
}

// ═══ DESPACHO ═══
function renderDespacho(){
  var flt=(document.getElementById('desp-filter-data')||{}).value||'';
  var all=getDocs();
  var docs=flt?all.filter(function(d){return d.data===flt;}):all.filter(function(d){return !d.despacho;});
  var kpis=document.getElementById('desp-kpis');
  if(kpis){var pend=docs.filter(function(d){return!d.despacho;}).length;var desp=docs.filter(function(d){return d.despacho;}).length;
    kpis.innerHTML='<div class="kpi-box kpi-accent" style="min-width:75px;padding:7px 10px;"><div class="kpi-label">Total</div><div class="kpi-val">'+docs.length+'</div></div>'
      +'<div class="kpi-box kpi-amber" style="min-width:75px;padding:7px 10px;"><div class="kpi-label">Pendentes</div><div class="kpi-val">'+pend+'</div></div>'
      +'<div class="kpi-box kpi-green" style="min-width:75px;padding:7px 10px;"><div class="kpi-label">Despachados</div><div class="kpi-val">'+desp+'</div></div>';}
  var c=document.getElementById('desp-list');if(!c)return;
  if(!docs.length){c.innerHTML='<div class="no-data">Nenhum documento encontrado.</div>';return;}
  var sorted=docs.filter(function(d){return!d.despacho;}).concat(docs.filter(function(d){return d.despacho;}));
  c.innerHTML=sorted.map(function(d){return despachableCard(d);}).join('');
}
function showAllPending(){var el=document.getElementById('desp-filter-data');if(el)el.value='';renderDespacho();}
function goTodayDesp(){var el=document.getElementById('desp-filter-data');if(el){el.value=todayKey();renderDespacho();}}
function despachableCard(d){
  var numStr=fmtNum(d.numProcesso,d.ano);var eid=d.id;
  var areaOpts=AREAS.map(function(a){return '<option value="'+a+'">'+a+'</option>';}).join('');
  var assuntoStr=fmtAssunto(d);var tipoStr=d.tipoDoc+fmtTipoExtra(d);
  if(d.despacho){
    return '<div class="doc-card doc-despachado">'
      +'<div class="doc-card-header"><span class="doc-num">'+numStr+'</span><span class="badge badge-tipo">'+tipoStr+'</span>'
        +'<span class="badge badge-desp">Despachado</span><span class="doc-data">'+fmtDate(d.data)+'</span></div>'
      +'<div class="doc-card-body"><div class="doc-inst"><strong>'+d.instituicao+'</strong></div>'
        +'<div class="doc-assunto">'+assuntoStr+'</div></div>'
      +'<div class="desp-info"><table class="dt-table">'
        +'<tr><td>Data de entrada</td><td>'+fmtDate(d.data)+'</td></tr>'
        +'<tr><td>Data de despacho</td><td>'+fmtDate(d.despacho.data)+'</td></tr>'
        +'<tr><td>Area</td><td>'+d.despacho.area+(d.despacho.outraArea?' — '+d.despacho.outraArea:'')+'</td></tr>'
        +(d.despacho.pessoa?'<tr><td>Responsavel</td><td>'+d.despacho.pessoa+'</td></tr>':'')
        +(d.despacho.nomeAnexo?'<tr><td>Doc. Digitalizado</td><td>'+d.despacho.nomeAnexo+'</td></tr>':'')
      +'</table>'
      +'<button class="btn btn-outline btn-xs" style="margin-top:8px;" onclick="undoDespacho(\''+eid+'\')">Anular Despacho</button>'
      +'</div></div>';
  }
  return '<div class="doc-card doc-pendente">'
    +'<div class="doc-card-header"><span class="doc-num">'+numStr+'</span><span class="badge badge-tipo">'+tipoStr+'</span>'
      +'<span class="badge badge-pend">Pendente</span>'
      +'<span class="doc-data">Entrada: '+fmtDate(d.data)+' '+(d.hora||'')+'</span></div>'
    +'<div class="doc-card-body"><div class="doc-inst"><strong>'+d.instituicao+'</strong></div>'
      +(d.oficio?'<div class="doc-oficio">Oficio: '+d.oficio+'</div>':'')
      +'<div class="doc-assunto">'+assuntoStr+'</div></div>'
    +'<div class="desp-form">'
      +'<div class="grid2">'
        +'<div class="field-group"><label>Data do Despacho</label><input type="date" id="dd-'+eid+'" value="'+todayKey()+'"></div>'
        +'<div class="field-group"><label>Area de Destino</label><select id="da-'+eid+'" onchange="toggleOutra(\''+eid+'\')">'+areaOpts+'</select></div>'
      +'</div>'
      +'<div class="grid2" id="outra-wrap-'+eid+'" style="display:none;">'
        +'<div class="field-group"><label>Especificar Area</label><input type="text" id="da-outra-'+eid+'" placeholder="Nome da area..."></div>'
        +'<div class="field-group"><label>Pessoa</label><input type="text" id="dp2-'+eid+'" placeholder="Nome..."></div>'
      +'</div>'
      +'<div class="grid2" id="pessoa-wrap-'+eid+'">'
        +'<div class="field-group"><label>Pessoa (opcional)</label><input type="text" id="dp-'+eid+'" placeholder="Nome..."></div>'
        +'<div class="field-group"><label>Doc. Digitalizado (opcional)</label><input type="file" id="df-'+eid+'"></div>'
      +'</div>'
      +'<button class="btn-desp" onclick="despacharDoc(\''+eid+'\')">Despachar</button>'
    +'</div></div>';
}
function toggleOutra(id){
  var area=(document.getElementById('da-'+id)||{}).value||'';
  var wrap=document.getElementById('outra-wrap-'+id);var pwrap=document.getElementById('pessoa-wrap-'+id);
  if(wrap)wrap.style.display=area==='Outra Area'?'grid':'none';
  if(pwrap)pwrap.style.display=area==='Outra Area'?'none':'grid';
}
function despacharDoc(id){
  var data=(document.getElementById('dd-'+id)||{}).value||'';
  var area=(document.getElementById('da-'+id)||{}).value||'';
  var outra=((document.getElementById('da-outra-'+id)||{}).value||'').trim();
  var p1=((document.getElementById('dp-'+id)||{}).value||'').trim();
  var p2=((document.getElementById('dp2-'+id)||{}).value||'').trim();
  var fi=(document.getElementById('df-'+id)||{}).files;
  var nomeAnexo=fi&&fi.length?fi[0].name:'';
  if(!data){toast('Selecione a data','err');return;}
  if(area==='Outra Area'&&!outra){toast('Especifique a area','err');return;}
  var docs=getDocs();var i=docs.findIndex(function(d){return d.id===id;});if(i===-1)return;
  docs[i].despacho={data:data,area:area,outraArea:outra,pessoa:p1||p2,nomeAnexo:nomeAnexo};
  var hist=docs[i].historico||[];hist.unshift({ts:new Date().toISOString(),profissional:currentProfissional,acao:'Despachado para '+area});
  docs[i].historico=hist;saveDocs(docs);
  addNotif('Processo '+fmtNum(docs[i].numProcesso,docs[i].ano)+' despachado para '+area+' por '+currentProfissional);
  toast('Despachado com sucesso!');renderDespacho();
}
function undoDespacho(id){
  if(!confirm('Anular o despacho?'))return;
  var docs=getDocs();var i=docs.findIndex(function(d){return d.id===id;});if(i===-1)return;
  docs[i].despacho=null;saveDocs(docs);toast('Despacho anulado');renderDespacho();
}

// ═══ AREA SECTIONS ═══
function switchAreaTab(tab){
  currentAreaTab=tab;
  var sec=document.getElementById('sec-area');
  sec.querySelectorAll('[data-atab]').forEach(function(b){b.classList.remove('active');});
  sec.querySelectorAll('.ast-panel').forEach(function(p){p.classList.remove('active');});
  var btn=sec.querySelector('[data-atab="'+tab+'"]');if(btn)btn.classList.add('active');
  var panel=document.getElementById('area-panel-'+tab);if(panel)panel.classList.add('active');
  if(tab==='recebidos')renderAreaReceived();
  if(tab==='internos'){renderAreaInternos();var d=document.getElementById('area-int-data');if(d&&!d.value)d.value=todayKey();}
  if(tab==='stats')renderAreaStats();
}
function renderAreaReceived(){
  var info=AREA_INFO[currentArea];
  var flt=(document.getElementById('area-filter-data')||{}).value||'';
  var all=getDocs();
  var docs=all.filter(function(d){return d.despacho&&(d.despacho.area===info.dn||d.despacho.area===info.label);});
  if(flt)docs=docs.filter(function(d){return d.data===flt;});
  var kpis=document.getElementById('area-kpis');
  if(kpis){var recv=docs.filter(function(d){return d.recepcao;}).length;var pend=docs.length-recv;
    kpis.innerHTML='<div class="kpi-box kpi-accent" style="min-width:75px;padding:7px 10px;"><div class="kpi-label">Total</div><div class="kpi-val">'+docs.length+'</div></div>'
      +'<div class="kpi-box kpi-amber" style="min-width:75px;padding:7px 10px;"><div class="kpi-label">Por Receber</div><div class="kpi-val">'+pend+'</div></div>'
      +'<div class="kpi-box kpi-green" style="min-width:75px;padding:7px 10px;"><div class="kpi-label">Recebidos</div><div class="kpi-val">'+recv+'</div></div>';}
  var c=document.getElementById('area-docs-list');if(!c)return;
  if(!docs.length){c.innerHTML='<div class="no-data">Nenhum documento despachado para esta area'+(flt?' nesta data':'')+'.</div>';return;}
  var sorted=docs.filter(function(d){return!d.recepcao;}).concat(docs.filter(function(d){return d.recepcao;}));
  c.innerHTML=sorted.map(function(d){return areaReceivedCard(d,currentArea);}).join('');
}
function areaReceivedCard(d,ak){
  var numStr=fmtNum(d.numProcesso,d.ano);var recv=!!d.recepcao;var assuntoStr=fmtAssunto(d);
  var timeline='<div class="date-timeline">'
    +'<div class="date-chip"><span class="date-chip-lbl">Registo SG</span><span class="date-chip-val">'+fmtDate(d.data)+'</span></div>'
    +(d.despacho?'<div class="date-chip dc-desp"><span class="date-chip-lbl">Despacho DG</span><span class="date-chip-val">'+fmtDate(d.despacho.data)+'</span></div>':'')
    +(recv?'<div class="date-chip dc-recv"><span class="date-chip-lbl">Entrada Area</span><span class="date-chip-val">'+fmtDate(d.recepcao.data)+'</span></div>':'')
  +'</div>';
  var actions=recv
    ?'<div class="desp-form" style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">'
       +'<span style="font-size:.7rem;color:var(--green);">Entrada em '+fmtDate(d.recepcao.data)+(d.recepcao.hora?' as '+d.recepcao.hora:'')+'</span>'
       +'<button class="btn btn-outline btn-xs" onclick="desfazerEntrada(\''+d.id+'\',\''+ak+'\')">Desfazer</button>'
     +'</div>'
    :'<div class="desp-form"><div class="grid2" style="max-width:280px;margin-bottom:8px;">'
       +'<div class="field-group"><label>Data de Entrada</label><input type="date" id="rec-data-'+d.id+'" value="'+todayKey()+'"></div>'
     +'</div>'
     +'<button class="btn-desp" style="background:var(--green);" onclick="darEntrada(\''+d.id+'\',\''+ak+'\')">Dar Entrada</button>'
    +'</div>';
  return '<div class="doc-card '+(recv?'doc-recebido':'doc-pendente')+'">'
    +'<div class="doc-card-header"><span class="doc-num">'+numStr+'</span><span class="badge badge-tipo">'+d.tipoDoc+'</span>'
      +(recv?'<span class="badge badge-recv">Entrada Dada</span>':'<span class="badge badge-pend">Aguarda Entrada</span>')
      +'<span class="doc-data">'+fmtDate(d.data)+'</span></div>'
    +'<div class="doc-card-body"><div class="doc-inst"><strong>'+d.instituicao+'</strong></div>'
      +'<div class="doc-assunto">'+assuntoStr+'</div>'+timeline+'</div>'
    +actions+'</div>';
}
function darEntrada(docId,ak){
  var data=(document.getElementById('rec-data-'+docId)||{}).value||todayKey();
  var docs=getDocs();var i=docs.findIndex(function(d){return d.id===docId;});if(i===-1)return;
  docs[i].recepcao={data:data,hora:fmtTime(),area:AREA_INFO[ak].dn};saveDocs(docs);
  toast('Entrada registada!');if(ak==='rh')renderRHReceived();else renderAreaReceived();
}
function desfazerEntrada(docId,ak){
  if(!confirm('Desfazer entrada?'))return;
  var docs=getDocs();var i=docs.findIndex(function(d){return d.id===docId;});if(i===-1)return;
  docs[i].recepcao=null;saveDocs(docs);toast('Entrada desfeita');
  if(ak==='rh')renderRHReceived();else renderAreaReceived();
}

// ═══ AREA INTERNOS ═══
function toggleAreaTipo(){
  var v=(document.getElementById('area-int-tipo')||{}).value||'trocaturno';
  var nf=document.getElementById('area-int-nome-f');var sf=document.getElementById('area-int-servico-f');var df=document.getElementById('area-int-desc-f');
  if(nf)nf.style.display=v==='trocaturno'?'':'none';
  if(sf)sf.style.display=v==='trocaturno'?'':'none';
  if(df)df.style.display=v==='outro'?'':'none';
}
function registarInternoArea(){
  var tipo=(document.getElementById('area-int-tipo')||{}).value||'';
  var data=(document.getElementById('area-int-data')||{}).value||'';
  var nome=((document.getElementById('area-int-nome')||{}).value||'').trim();
  var servico=((document.getElementById('area-int-servico')||{}).value||'').trim();
  var desc=((document.getElementById('area-int-desc')||{}).value||'').trim();
  if(!data){toast('Selecione a data','err');return;}
  if(tipo==='trocaturno'&&!nome){toast('Preencha o nome','err');return;}
  if(tipo==='outro'&&!desc){toast('Preencha a descricao','err');return;}
  var doc={id:uid(),tipo:tipo,data:data,hora:fmtTime(),profissional:currentProfissional,nome:nome,servico:servico,descricao:desc};
  var docs=getAreaDocs(currentArea);docs.unshift(doc);saveAreaDocs(currentArea,docs);
  clearAreaIntForm();toast('Documento interno registado');renderAreaInternos();
}
function clearAreaIntForm(){['area-int-nome','area-int-servico','area-int-desc'].forEach(function(id){var el=document.getElementById(id);if(el)el.value='';});var t=document.getElementById('area-int-tipo');if(t)t.selectedIndex=0;toggleAreaTipo();}
function renderAreaInternos(){
  var flt=(document.getElementById('area-int-filter')||{}).value||'';
  var docs=getAreaDocs(currentArea);if(flt)docs=docs.filter(function(d){return d.data===flt;});
  var c=document.getElementById('area-internos-list');if(!c)return;
  if(!docs.length){c.innerHTML='<div class="no-data">Nenhum documento interno registado.</div>';return;}
  c.innerHTML=docs.map(function(d){return internoCard(d);}).join('');
}
function internoCard(d){
  var badge,info;
  if(d.tipo==='trocaturno'){badge='<span class="badge badge-rh-tt">Troca de Turno</span>';info='<strong>'+d.nome+'</strong>'+(d.servico?' &middot; '+d.servico:'');}
  else{badge='<span class="badge badge-outro">Outro</span>';info=d.descricao||d.nome||'';}
  return '<div class="doc-card"><div class="doc-card-header">'+badge+'<span class="doc-data">'+fmtDate(d.data)+' '+(d.hora||'')+'</span>'+(d.profissional?'<span style="font-size:.6rem;color:var(--muted);">'+d.profissional+'</span>':'')+'</div>'
    +'<div class="doc-card-body"><div class="doc-assunto">'+info+'</div></div></div>';
}

// ═══ AREA STATS ═══
function setAreaStatsPeriod(p){
  areaStatsPeriod=p;
  var bar=document.getElementById('area-stats-periods');
  if(bar)bar.querySelectorAll('[data-p]').forEach(function(b){b.classList.toggle('active',b.getAttribute('data-p')===p);});
  renderAreaStats();
}
function renderAreaStats(){
  var info=AREA_INFO[currentArea];var range=getDateRange(areaStatsPeriod);
  var all=getDocs();
  var docs=all.filter(function(d){return d.despacho&&(d.despacho.area===info.dn||d.despacho.area===info.label)&&d.data>=range.start&&d.data<=range.end;});
  var recv=docs.filter(function(d){return d.recepcao;}).length;
  var kEl=document.getElementById('area-stats-kpis');
  if(kEl){kEl.innerHTML='<div class="kpi-box kpi-accent"><div class="kpi-label">Recebidos DG</div><div class="kpi-val">'+docs.length+'</div></div>'
    +'<div class="kpi-box kpi-green"><div class="kpi-label">Entrada Dada</div><div class="kpi-val">'+recv+'</div></div>'
    +'<div class="kpi-box kpi-amber"><div class="kpi-label">Pendentes</div><div class="kpi-val">'+(docs.length-recv)+'</div></div>';}
  drawTrendChart('area-chart-trend',docs,areaStatsPeriod,true);
}

// ═══ RH ═══
function switchRHTab(tab){
  currentRHTab=tab;
  var sec=document.getElementById('sec-rh');
  sec.querySelectorAll('[data-rhtab]').forEach(function(b){b.classList.remove('active');});
  sec.querySelectorAll('.ast-panel').forEach(function(p){p.classList.remove('active');});
  var btn=sec.querySelector('[data-rhtab="'+tab+'"]');if(btn)btn.classList.add('active');
  var panel=document.getElementById('rh-panel-'+tab);if(panel)panel.classList.add('active');
  if(tab==='recebidos')renderRHReceived();
  if(tab==='justfalta')renderJustFaltas();
  if(tab==='memorandos'){initRHMemoNum();renderMemorandos();}
  if(tab==='internos'){renderRHInternos();var d=document.getElementById('rh-int-data');if(d&&!d.value)d.value=todayKey();}
  if(tab==='stats')renderRHStats();
}
function renderRH(){switchRHTab(currentRHTab||'recebidos');initRHMemoNum();}
function renderRHReceived(){
  var flt=(document.getElementById('rh-filter-data')||{}).value||'';
  var all=getDocs();var docs=all.filter(function(d){return d.despacho&&d.despacho.area==='Recursos Humanos';});
  if(flt)docs=docs.filter(function(d){return d.data===flt;});
  var kpis=document.getElementById('rh-kpis');
  if(kpis){var recv=docs.filter(function(d){return d.recepcao;}).length;var pend=docs.length-recv;
    kpis.innerHTML='<div class="kpi-box kpi-accent" style="min-width:75px;padding:7px 10px;"><div class="kpi-label">Total</div><div class="kpi-val">'+docs.length+'</div></div>'
      +'<div class="kpi-box kpi-amber" style="min-width:75px;padding:7px 10px;"><div class="kpi-label">Por Receber</div><div class="kpi-val">'+pend+'</div></div>'
      +'<div class="kpi-box kpi-green" style="min-width:75px;padding:7px 10px;"><div class="kpi-label">Recebidos</div><div class="kpi-val">'+recv+'</div></div>';}
  var c=document.getElementById('rh-docs-list');if(!c)return;
  if(!docs.length){c.innerHTML='<div class="no-data">Nenhum documento despachado para RH.</div>';return;}
  var sorted=docs.filter(function(d){return!d.recepcao;}).concat(docs.filter(function(d){return d.recepcao;}));
  c.innerHTML=sorted.map(function(d){return areaReceivedCard(d,'rh');}).join('');
}
function registarJustFalta(){
  var nome=((document.getElementById('rh-jf-nome')||{}).value||'').trim();
  var area=((document.getElementById('rh-jf-area')||{}).value||'').trim();
  var data=(document.getElementById('rh-jf-data')||{}).value||'';
  var obs=((document.getElementById('rh-jf-obs')||{}).value||'').trim();
  if(!nome||!area||!data){toast('Preencha todos os campos obrigatorios','err');return;}
  var doc={id:uid(),tipo:'justfalta',nome:nome,area:area,data:data,hora:fmtTime(),profissional:currentProfissional,obs:obs};
  var docs=getAreaDocs('rh');docs.unshift(doc);saveAreaDocs('rh',docs);
  clearJustFalta();toast('Justificacao registada');renderJustFaltas();
}
function clearJustFalta(){['rh-jf-nome','rh-jf-area','rh-jf-obs'].forEach(function(id){var el=document.getElementById(id);if(el)el.value='';});}
var jfFilterMode='todos', voltouTargetId=null;
function setJFFilter(m){
  jfFilterMode=m;
  ['todos','pendentes','voltaram'].forEach(function(k){
    var b=document.getElementById('rh-jf-btn-'+k);
    if(b){b.className=k===m?'btn btn-sm':'btn btn-outline btn-sm';if(k===m)b.style.background='var(--accent)',b.style.color='#fff';else b.style.background='',b.style.color='';}
  });
  renderJustFaltas();
}
function marcarVoltou(id){
  if(!currentProfissional){toast('Faca login primeiro','err');return;}
  voltouTargetId=id;
  var el=document.getElementById('voltou-motivo');if(el)el.value='';
  var err=document.getElementById('voltou-err');if(err)err.style.display='none';
  var m=document.getElementById('modal-voltou');if(m){m.style.display='flex';setTimeout(function(){if(el)el.focus();},80);}
}
function confirmarVoltou(){
  var motivo=((document.getElementById('voltou-motivo')||{}).value||'').trim();
  var err=document.getElementById('voltou-err');
  if(!motivo){if(err){err.style.display='block';err.textContent='Preencha o motivo do justificativo.';}return;}
  if(!currentProfissional){toast('Faca login primeiro','err');return;}
  var docs=getAreaDocs('rh');
  var idx=docs.findIndex(function(d){return d.id===voltouTargetId;});
  if(idx===-1)return;
  docs[idx].voltou={data:todayKey(),hora:fmtTime(),profissional:currentProfissional,motivo:motivo};
  saveAreaDocs('rh',docs);
  document.getElementById('modal-voltou').style.display='none';
  addNotif('Justificativo de '+docs[idx].nome+' devolvido ('+motivo+') — '+currentProfissional);
  toast('Justificativo marcado como devolvido');
  renderJustFaltas();
}
function desfazerVoltou(id){
  var docs=getAreaDocs('rh');
  var idx=docs.findIndex(function(d){return d.id===id;});
  if(idx===-1)return;
  delete docs[idx].voltou;
  saveAreaDocs('rh',docs);
  toast('Marcacao desfeita');
  renderJustFaltas();
}
function renderJustFaltas(){
  var flt=(document.getElementById('rh-jf-filter')||{}).value||'';
  var docs=getAreaDocs('rh').filter(function(d){return d.tipo==='justfalta';});
  if(flt)docs=docs.filter(function(d){return d.data===flt;});
  if(jfFilterMode==='pendentes')docs=docs.filter(function(d){return !d.voltou;});
  else if(jfFilterMode==='voltaram')docs=docs.filter(function(d){return !!d.voltou;});
  var c=document.getElementById('rh-jf-list');if(!c)return;
  if(!docs.length){c.innerHTML='<div class="no-data">Nenhuma justificacao encontrada.</div>';return;}
  c.innerHTML=docs.map(function(d){
    var voltouBadge=d.voltou
      ?'<span class="badge" style="background:#059669;color:#fff;">Devolvido '+fmtDate(d.voltou.data)+'</span>'
      :'<span class="badge" style="background:#f59e0b;color:#fff;">Pendente</span>';
    var acaoBtns=d.voltou
      ?'<span style="font-size:.68rem;color:#059669;font-weight:600;">Justificativo entregue — processo encerrado</span>'
       +'&nbsp;&nbsp;<button class="btn btn-outline btn-xs" onclick="desfazerVoltou(\''+d.id+'\')" style="font-size:.6rem;">Desfazer</button>'
      :'<button class="btn btn-sm" style="background:#059669;color:#fff;" onclick="marcarVoltou(\''+d.id+'\')">Justificativo Voltou</button>';
    return '<div class="doc-card" style="border-left:4px solid '+(d.voltou?'#059669':'#f59e0b')+';'+(d.voltou?'opacity:.82;':'')+';">'
      +'<div class="doc-card-header">'+voltouBadge+'<span class="doc-data">Falta: '+fmtDate(d.data)+'</span></div>'
      +'<div class="doc-card-body">'
      +'<div class="doc-inst"><strong>'+d.nome+'</strong></div>'
      +'<div class="doc-oficio">Area: '+d.area+'</div>'
      +(d.obs?'<div class="doc-assunto">'+d.obs+'</div>':'')
      +(d.voltou?'<div class="doc-assunto" style="color:#059669;font-weight:600;">Motivo: '+d.voltou.motivo+'</div>':'')
      +(d.voltou?'<div class="doc-assunto" style="color:var(--muted);font-size:.65rem;">Devolvido em '+fmtDate(d.voltou.data)+' '+d.voltou.hora+' por '+d.voltou.profissional+'</div>':'')
      +'<div class="doc-prof">'+(d.profissional||'')+'</div>'
      +'<div style="margin-top:8px;">'+acaoBtns+'</div>'
      +'</div></div>';
  }).join('');
}
function initRHMemoNum(){var c=getRHMemoCfg();var ano=new Date().getFullYear();var el=document.getElementById('rh-memo-num-val');if(el)el.textContent=fmtRH(c.numAtual,ano);var sub=document.getElementById('rh-memo-num-sub');if(sub)sub.textContent='Ano '+ano;}
function registarMemorando(){
  var nome=((document.getElementById('rh-memo-nome')||{}).value||'').trim();
  var area=((document.getElementById('rh-memo-area')||{}).value||'').trim();
  var tempo=((document.getElementById('rh-memo-tempo')||{}).value||'').trim();
  var data=(document.getElementById('rh-memo-data')||{}).value||'';
  var obs=((document.getElementById('rh-memo-obs')||{}).value||'').trim();
  if(!nome||!area||!tempo||!data){toast('Preencha todos os campos obrigatorios','err');return;}
  var num=nextRHNum();var ano=new Date().getFullYear();var numStr=fmtRH(num,ano);
  var doc={id:uid(),tipo:'memorando',numStr:numStr,nome:nome,area:area,tempo:tempo,data:data,hora:fmtTime(),profissional:currentProfissional,obs:obs};
  var docs=getAreaDocs('rh');docs.unshift(doc);saveAreaDocs('rh',docs);
  clearMemorando();initRHMemoNum();toast('Memorando '+numStr+' registado');renderMemorandos();
}
function clearMemorando(){['rh-memo-nome','rh-memo-area','rh-memo-tempo','rh-memo-obs'].forEach(function(id){var el=document.getElementById(id);if(el)el.value='';});}
function renderMemorandos(){
  var flt=(document.getElementById('rh-memo-filter')||{}).value||'';
  var docs=getAreaDocs('rh').filter(function(d){return d.tipo==='memorando';});
  if(flt)docs=docs.filter(function(d){return d.data===flt;});
  var c=document.getElementById('rh-memo-list');if(!c)return;
  if(!docs.length){c.innerHTML='<div class="no-data">Nenhum memorando registado.</div>';return;}
  c.innerHTML=docs.map(function(d){return '<div class="doc-card" style="border-left:4px solid #7c3aed;">'
    +'<div class="doc-card-header"><span class="rh-num">'+d.numStr+'</span><span class="badge badge-rh-mf">Memorando Ferias</span><span class="doc-data">'+fmtDate(d.data)+'</span></div>'
    +'<div class="doc-card-body"><div class="doc-inst"><strong>'+d.nome+'</strong></div><div class="doc-oficio">Area: '+d.area+'</div>'
    +'<div class="doc-assunto">Periodo: '+d.tempo+'</div>'+(d.obs?'<div class="doc-assunto" style="color:var(--muted);">'+d.obs+'</div>':'')
    +'<div class="doc-prof">'+(d.profissional||'')+'</div></div></div>';}).join('');
}
function toggleRHTipo(){var v=(document.getElementById('rh-int-tipo')||{}).value||'trocaturno';var nf=document.getElementById('rh-int-nome-f');var sf=document.getElementById('rh-int-servico-f');var df=document.getElementById('rh-int-desc-f');if(nf)nf.style.display=v==='trocaturno'?'':'none';if(sf)sf.style.display=v==='trocaturno'?'':'none';if(df)df.style.display=v==='outro'?'':'none';}
function registarRHInterno(){var tipo=(document.getElementById('rh-int-tipo')||{}).value||'';var data=(document.getElementById('rh-int-data')||{}).value||'';var nome=((document.getElementById('rh-int-nome')||{}).value||'').trim();var servico=((document.getElementById('rh-int-servico')||{}).value||'').trim();var desc=((document.getElementById('rh-int-desc')||{}).value||'').trim();if(!data){toast('Selecione a data','err');return;}if(tipo==='trocaturno'&&!nome){toast('Preencha o nome','err');return;}if(tipo==='outro'&&!desc){toast('Preencha a descricao','err');return;}var doc={id:uid(),tipo:tipo,data:data,hora:fmtTime(),profissional:currentProfissional,nome:nome,servico:servico,descricao:desc};var docs=getAreaDocs('rh');docs.unshift(doc);saveAreaDocs('rh',docs);clearRHIntForm();toast('Documento registado');renderRHInternos();}
function clearRHIntForm(){['rh-int-nome','rh-int-servico','rh-int-desc'].forEach(function(id){var el=document.getElementById(id);if(el)el.value='';});var t=document.getElementById('rh-int-tipo');if(t)t.selectedIndex=0;toggleRHTipo();}
function renderRHInternos(){var flt=(document.getElementById('rh-int-filter')||{}).value||'';var docs=getAreaDocs('rh').filter(function(d){return d.tipo==='trocaturno'||d.tipo==='outro';});if(flt)docs=docs.filter(function(d){return d.data===flt;});var c=document.getElementById('rh-int-list');if(!c)return;if(!docs.length){c.innerHTML='<div class="no-data">Nenhum documento registado.</div>';return;}c.innerHTML=docs.map(function(d){return internoCard(d);}).join('');}
function setRHStatsPeriod(p){rhStatsPeriod=p;var bar=document.getElementById('rh-stats-periods');if(bar)bar.querySelectorAll('[data-p]').forEach(function(b){b.classList.toggle('active',b.getAttribute('data-p')===p);});renderRHStats();}
function renderRHStats(){var range=getDateRange(rhStatsPeriod);var all=getDocs();var docs=all.filter(function(d){return d.despacho&&d.despacho.area==='Recursos Humanos'&&d.data>=range.start&&d.data<=range.end;});var recv=docs.filter(function(d){return d.recepcao;}).length;var kEl=document.getElementById('rh-stats-kpis');if(kEl){kEl.innerHTML='<div class="kpi-box kpi-accent"><div class="kpi-label">Recebidos DG</div><div class="kpi-val">'+docs.length+'</div></div><div class="kpi-box kpi-green"><div class="kpi-label">Entrada Dada</div><div class="kpi-val">'+recv+'</div></div><div class="kpi-box kpi-amber"><div class="kpi-label">Pendentes</div><div class="kpi-val">'+(docs.length-recv)+'</div></div>';}drawTrendChart('rh-chart-trend',docs,rhStatsPeriod,true);}

// ═══ STATISTICS ═══
function setStatsPeriod(p){
  statsPeriod=p;
  document.querySelectorAll('[data-sp]').forEach(function(b){b.classList.toggle('active',b.getAttribute('data-sp')===p);});
  var range=getDateRange(p);
  var f=document.getElementById('stats-from');if(f)f.value=range.start;
  var t=document.getElementById('stats-to');if(t)t.value=range.end;
  renderStats();
}
function renderStats(){
  var f=(document.getElementById('stats-from')||{}).value||'';
  var t=(document.getElementById('stats-to')||{}).value||todayKey();
  var docs=getDocs();
  if(f)docs=docs.filter(function(d){return d.data>=f&&d.data<=t;});
  var total=docs.length;var pend=docs.filter(function(d){return!d.despacho;}).length;var desp=docs.filter(function(d){return d.despacho;}).length;var recv=docs.filter(function(d){return d.recepcao;}).length;
  var kEl=document.getElementById('stats-kpis');
  if(kEl)kEl.innerHTML='<div class="kpi-box kpi-accent"><div class="kpi-label">Total</div><div class="kpi-val">'+total+'</div></div>'
    +'<div class="kpi-box kpi-amber"><div class="kpi-label">Pendentes</div><div class="kpi-val">'+pend+'</div></div>'
    +'<div class="kpi-box kpi-green"><div class="kpi-label">Despachados</div><div class="kpi-val">'+desp+'</div></div>'
    +'<div class="kpi-box"><div class="kpi-label">Recebidos</div><div class="kpi-val">'+recv+'</div></div>';
  drawTypeChart('stats-chart-tipo',docs,'tipoDoc');
  drawTypeChart('stats-chart-assunto',docs,'assunto');
  drawTrendChart('stats-chart-trend',docs,statsPeriod,false);
  renderSummaryTable(docs);
}
function renderSummaryTable(docs){
  var counts={};docs.forEach(function(d){counts[d.tipoDoc]=(counts[d.tipoDoc]||0)+1;});
  var rows=Object.keys(counts).sort().map(function(k){return '<tr><td>'+k+'</td><td style="text-align:right;font-family:var(--fm);font-weight:700;">'+counts[k]+'</td></tr>';}).join('');
  var el=document.getElementById('stats-summary-table');
  if(el)el.innerHTML='<table class="sum-table"><thead><tr><th>Tipo de Documento</th><th style="text-align:right;">Quantidade</th></tr></thead><tbody>'+rows+'</tbody></table>';
}

// ═══ CHARTS ═══
function isDark(){return document.documentElement.classList.contains('dark');}
function chartColors(){return isDark()?['rgba(100,149,255,.8)','rgba(0,212,170,.8)','rgba(251,191,36,.8)','rgba(239,68,68,.8)','rgba(167,139,250,.8)','rgba(56,189,248,.8)']:['rgba(26,86,219,.8)','rgba(16,185,129,.8)','rgba(245,158,11,.8)','rgba(239,68,68,.8)','rgba(124,58,237,.8)','rgba(14,165,233,.8)'];}
function chartTextColor(){return isDark()?'rgba(255,255,255,.5)':'rgba(0,0,0,.4)';}
function drawTypeChart(canvasId,docs,field){
  var canvas=document.getElementById(canvasId);if(!canvas||typeof Chart==='undefined')return;
  var counts={};docs.forEach(function(d){var v=d[field]||'Desconhecido';counts[v]=(counts[v]||0)+1;});
  var labels=Object.keys(counts).sort(function(a,b){return counts[b]-counts[a];});
  var data=labels.map(function(l){return counts[l];});
  var colors=chartColors();
  if(statsCharts[canvasId])statsCharts[canvasId].destroy();
  statsCharts[canvasId]=new Chart(canvas,{type:'bar',data:{labels:labels,datasets:[{data:data,backgroundColor:colors.slice(0,labels.length),borderRadius:4}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(ctx){return ctx.parsed.y+' doc(s)';}}}} ,scales:{x:{ticks:{color:chartTextColor(),font:{size:10}},grid:{display:false}},y:{ticks:{color:chartTextColor(),font:{size:10},stepSize:1},grid:{color:isDark()?'rgba(255,255,255,.05)':'rgba(0,0,0,.05)'}}}}});
}
function drawTrendChart(canvasId,docs,period,small){
  var canvas=document.getElementById(canvasId);if(!canvas||typeof Chart==='undefined')return;
  var byDate={};docs.forEach(function(d){byDate[d.data]=(byDate[d.data]||0)+1;});
  var dates=Object.keys(byDate).sort();
  var labels=dates.map(function(d){var p=d.split('-');return p[2]+'/'+p[1];});
  var data=dates.map(function(d){return byDate[d];});
  var colors=chartColors();
  if(statsCharts[canvasId])statsCharts[canvasId].destroy();
  statsCharts[canvasId]=new Chart(canvas,{type:'bar',data:{labels:labels,datasets:[{data:data,backgroundColor:colors[0],borderRadius:3,label:'Documentos'}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{ticks:{color:chartTextColor(),font:{size:small?9:10}},grid:{display:false}},y:{ticks:{color:chartTextColor(),font:{size:10},stepSize:1},grid:{color:isDark()?'rgba(255,255,255,.05)':'rgba(0,0,0,.05)'}}}}});
}

// ═══ PESQUISA ═══
function setPesqFilter(f){pesqFilter=f;renderPesquisa();}
function clearPesquisa(){var pi=document.getElementById('pesq-input');if(pi)pi.value='';var pd=document.getElementById('pesq-data');if(pd)pd.value='';var pa=document.getElementById('pesq-area');if(pa)pa.value='';pesqFilter='todos';renderPesquisa();}
function renderPesquisa(){
  var q=((document.getElementById('pesq-input')||{}).value||'').toLowerCase().trim();
  var fdata=(document.getElementById('pesq-data')||{}).value||'';
  var farea=(document.getElementById('pesq-area')||{}).value||'';
  var all=getDocs();var docs=all;
  if(fdata)docs=docs.filter(function(d){return d.data===fdata;});
  if(farea)docs=docs.filter(function(d){return d.despacho&&(d.despacho.area===farea||d.despacho.outraArea===farea);});
  if(q)docs=docs.filter(function(d){return(d.instituicao||'').toLowerCase().includes(q)||(fmtAssunto(d)||'').toLowerCase().includes(q)||(d.oficio||'').toLowerCase().includes(q)||(d.tipoDoc||'').toLowerCase().includes(q)||fmtNum(d.numProcesso,d.ano).includes(q);});
  if(pesqFilter==='pendentes')docs=docs.filter(function(d){return!d.despacho;});
  if(pesqFilter==='despachados')docs=docs.filter(function(d){return d.despacho;});
  if(pesqFilter==='recebidos')docs=docs.filter(function(d){return d.recepcao;});
  var sorted=docs.filter(function(d){return d.despacho;}).concat(docs.filter(function(d){return!d.despacho;}));
  var se=document.getElementById('pesq-stats');if(se)se.textContent=docs.length+' resultado(s) de '+all.length+' documentos';
  var c=document.getElementById('pesq-results');if(!c)return;
  if(!sorted.length){c.innerHTML='<div class="no-data">Nenhum resultado encontrado.</div>';return;}
  c.innerHTML=sorted.map(function(d){return docCardFull(d);}).join('');
}
function docCardFull(d){
  var numStr=fmtNum(d.numProcesso,d.ano);var assuntoStr=fmtAssunto(d);var tipoStr=d.tipoDoc+fmtTipoExtra(d);
  var despInfo='';
  if(d.despacho){despInfo='<div class="desp-info"><table class="dt-table">'
    +'<tr><td>Data de entrada</td><td>'+fmtDate(d.data)+' '+(d.hora||'')+'</td></tr>'
    +'<tr><td>Despacho DG</td><td>'+fmtDate(d.despacho.data)+'</td></tr>'
    +'<tr><td>Area</td><td>'+d.despacho.area+(d.despacho.outraArea?' — '+d.despacho.outraArea:'')+'</td></tr>'
    +(d.despacho.pessoa?'<tr><td>Responsavel</td><td>'+d.despacho.pessoa+'</td></tr>':'')
    +(d.recepcao?'<tr><td>Entrada na Area</td><td>'+fmtDate(d.recepcao.data)+'</td></tr>':'')
    +'</table></div>';}
  return '<div class="doc-card '+(d.despacho?'doc-despachado':'doc-pendente')+'">'
    +'<div class="doc-card-header"><span class="doc-num">'+numStr+'</span><span class="badge badge-tipo">'+tipoStr+'</span>'
      +'<span class="doc-data">'+fmtDate(d.data)+' '+(d.hora||'')+'</span>'
      +(d.despacho?'<span class="badge badge-desp">Despachado</span>':'<span class="badge badge-pend">Pendente</span>')
      +(d.recepcao?'<span class="badge badge-recv">Recebido</span>':'')
    +'</div>'
    +'<div class="doc-card-body"><div class="doc-inst"><strong>'+d.instituicao+'</strong></div>'
      +(d.oficio?'<div class="doc-oficio">Oficio: '+d.oficio+'</div>':'')
      +'<div class="doc-assunto">'+assuntoStr+'</div>'
      +'<div class="doc-prof">'+(d.profissional||'')+'</div>'
    +'</div>'+despInfo+'</div>';
}

// ═══ DEFINICOES ═══
function unlockDef(){
  var cfg=getConfig();var senha=(document.getElementById('def-senha-input')||{}).value||'';
  if(senha!==cfg.senhaChefe){var e=document.getElementById('def-lock-err');if(e){e.style.display='block';e.textContent='Senha incorrecta.';}return;}
  document.getElementById('def-lock').style.display='none';
  document.getElementById('def-content').style.display='block';
  renderDefinicoes();
}
function renderDefinicoes(){
  var cfg=getConfig();var ano=new Date().getFullYear();
  var anoEl=document.getElementById('def-ano');if(anoEl)anoEl.value=ano;
  var numEl=document.getElementById('def-num-atual');if(numEl)numEl.value=cfg.numAtual;
  updateDefPreview();
  var docs=getDocs();var pend=docs.filter(function(d){return!d.despacho;}).length;var desp=docs.filter(function(d){return d.despacho;}).length;
  var kEl=document.getElementById('def-kpis');
  if(kEl)kEl.innerHTML='<div class="kpi-box kpi-accent"><div class="kpi-label">Total</div><div class="kpi-val">'+docs.length+'</div></div>'
    +'<div class="kpi-box kpi-amber"><div class="kpi-label">Pendentes</div><div class="kpi-val">'+pend+'</div></div>'
    +'<div class="kpi-box kpi-green"><div class="kpi-label">Despachados</div><div class="kpi-val">'+desp+'</div></div>';
  renderProfList();
}
function updateDefPreview(){var el=document.getElementById('def-num-atual');var n=el?parseInt(el.value):NaN;var p=document.getElementById('def-preview');if(p)p.textContent=(!isNaN(n)&&n>0)?fmtNum(n,new Date().getFullYear()):'---';}
function saveDefinicoes(){var el=document.getElementById('def-num-atual');var n=el?parseInt(el.value):NaN;if(isNaN(n)||n<1){toast('Numero invalido','err');return;}var cfg=getConfig();cfg.numAtual=n;saveConfig(cfg);updateDefPreview();var pn=document.getElementById('preview-num');if(pn)pn.textContent=fmtNum(n,new Date().getFullYear());toast('Definicoes guardadas');}
function saveSenha(){
  var ns=(document.getElementById('def-new-senha')||{}).value||'';
  var cs=(document.getElementById('def-confirm-senha')||{}).value||'';
  if(!ns){toast('Preencha a nova senha','err');return;}
  if(ns!==cs){toast('As senhas nao coincidem','err');return;}
  var cfg=getConfig();cfg.senhaChefe=ns;saveConfig(cfg);
  document.getElementById('def-new-senha').value='';document.getElementById('def-confirm-senha').value='';
  toast('Senha actualizada');
}
function renderProfList(){
  var cfg=getConfig();var el=document.getElementById('prof-list');if(!el)return;
  if(!cfg.profissionais.length){el.innerHTML='<div class="no-data">Nenhum profissional configurado.</div>';return;}
  el.innerHTML=cfg.profissionais.map(function(p){
    return '<div class="prof-row"><span class="prof-name">'+p.nome+'</span>'
      +(p.id==='admin'?'<span class="prof-badge">Admin</span>':'')
      +'<button class="btn btn-danger btn-xs" onclick="removeProfissional(\''+p.id+'\')">Remover</button>'
    +'</div>';
  }).join('');
}
function addProfissional(){
  var nome=((document.getElementById('new-prof-nome')||{}).value||'').trim();
  var senha=((document.getElementById('new-prof-senha')||{}).value||'').trim();
  if(!nome||!senha){toast('Preencha nome e senha','err');return;}
  var cfg=getConfig();
  cfg.profissionais.push({id:'p'+Date.now(),nome:nome,senha:senha});
  saveConfig(cfg);
  document.getElementById('new-prof-nome').value='';document.getElementById('new-prof-senha').value='';
  toast('Profissional adicionado');renderProfList();initLoginModal();
}
function removeProfissional(id){
  if(id==='admin'){toast('Nao e possivel remover o administrador','err');return;}
  if(!confirm('Remover este profissional?'))return;
  var cfg=getConfig();cfg.profissionais=cfg.profissionais.filter(function(p){return p.id!==id;});saveConfig(cfg);renderProfList();toast('Profissional removido');
}
function exportarDados(){
  var data={config:getConfig(),documentos:getDocs(),exportadoEm:new Date().toISOString()};
  Object.keys(AREA_INFO).forEach(function(k){data['area_'+k]=getAreaDocs(k);});
  var blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  var url=URL.createObjectURL(blob);var a=document.createElement('a');a.href=url;a.download='secretaria_geral_'+todayKey()+'.json';document.body.appendChild(a);a.click();document.body.removeChild(a);URL.revokeObjectURL(url);toast('Dados exportados');
}

// ═══ PDF EXPORT ═══
function exportPDF(period){
  if(typeof jspdf==='undefined'){toast('Biblioteca PDF a carregar, aguarde e tente novamente','err');return;}
  var docs=getDocs();
  var f,t,periodoLabel;
  if(period==='custom'){
    f=(document.getElementById('stats-from')||{}).value||'';
    t=(document.getElementById('stats-to')||{}).value||todayKey();
    periodoLabel='Periodo Seleccionado';
  } else {
    var range=getDateRange(period);f=range.start;t=range.end;
    periodoLabel={'hoje':'Diario','semana':'Semanal','mes':'Mensal','trimestre':'Trimestral','semestre':'Semestral','ano':'Anual'}[period]||period;
  }
  if(f)docs=docs.filter(function(d){return d.data>=f&&d.data<=t;});
  var total=docs.length;
  var desp=docs.filter(function(d){return d.despacho;}).length;
  var pend=total-desp;
  var recv=docs.filter(function(d){return d.recepcao;}).length;
  var doc=new jspdf.jsPDF({orientation:'landscape'});
  doc.setFontSize(14);doc.setFont('helvetica','bold');
  doc.text('Hospital do Prenda — Secretaria Geral',14,14);
  doc.setFontSize(9);doc.setFont('helvetica','normal');doc.setTextColor(80);
  doc.text('Relatorio '+periodoLabel+'  |  '+fmtDate(f)+' ate '+fmtDate(t),14,21);
  doc.text('Total: '+total+'   Despachados: '+desp+'   Pendentes: '+pend+'   Recebidos: '+recv,14,27);
  doc.setTextColor(0);
  var rows=docs.map(function(d){
    return [
      fmtNum(d.numProcesso,d.ano),
      fmtDate(d.data),
      (d.instituicao||'').substring(0,30),
      (d.tipoDoc||'')+(d.tipoDocExtra?' ('+d.tipoDocExtra+')':''),
      (d.assunto||'').substring(0,28),
      d.despacho?(d.despacho.area||'').substring(0,22):'Pendente',
      (d.profissional||'')
    ];
  });
  doc.autoTable({
    startY:32,
    head:[['Processo','Data','Instituicao','Tipo Doc.','Assunto','Despacho','Profissional']],
    body:rows,
    styles:{fontSize:7.5,cellPadding:2},
    headStyles:{fillColor:[26,86,219],textColor:255,fontStyle:'bold'},
    alternateRowStyles:{fillColor:[240,244,255]},
    columnStyles:{0:{cellWidth:22},1:{cellWidth:20},5:{cellWidth:30}}
  });
  var fname='secretaria_'+period+'_'+todayKey()+'.pdf';
  doc.save(fname);
  toast('PDF guardado: '+fname,'info');
}

// ═══ INTERCORRENCIAS ═══
var IC_KEY='hp_intercorrencias', icFilter='todos', icResolveId=null;
function getICs(){var r=localStorage.getItem(IC_KEY);return r?JSON.parse(r):[];}
function saveICs(d){localStorage.setItem(IC_KEY,JSON.stringify(d));}
function registarIntercorrencia(){
  if(!currentProfissional){toast('Faca login primeiro','err');return;}
  var desc=((document.getElementById('ic-descricao')||{}).value||'').trim();
  var data=(document.getElementById('ic-data')||{}).value||'';
  var hora=(document.getElementById('ic-hora')||{}).value||fmtTime();
  if(!desc||!data){toast('Preencha a descricao e a data','err');return;}
  var ic={id:uid(),descricao:desc,data:data,hora:hora,profissional:currentProfissional,status:'pendente',resolucao:null};
  var ics=getICs();ics.unshift(ic);saveICs(ics);
  clearIC();
  addNotif('Intercorrencia do dia '+fmtDate(data)+' registada por '+currentProfissional);
  toast('Intercorrencia registada');
  renderIntercorrencias();
}
function clearIC(){
  var el=document.getElementById('ic-descricao');if(el)el.value='';
  var d=document.getElementById('ic-data');if(d)d.value=todayKey();
  var h=document.getElementById('ic-hora');if(h)h.value=fmtTime();
}
function setICFilter(f){
  icFilter=f;
  ['todos','pendentes','resolvidos'].forEach(function(k){
    var b=document.getElementById('ic-btn-'+k);
    if(b){b.className=k===f?'btn btn-sm':'btn btn-outline btn-sm';if(k===f)b.style.background='var(--accent)',b.style.color='#fff';else b.style.background='',b.style.color='';}
  });
  renderIntercorrencias();
}
function abrirResolverIC(id){
  if(!currentProfissional){toast('Faca login primeiro','err');return;}
  icResolveId=id;
  var el=document.getElementById('ic-resolve-obs');if(el)el.value='';
  var m=document.getElementById('modal-ic-resolve');if(m){m.style.display='flex';setTimeout(function(){if(el)el.focus();},80);}
}
function confirmarResolverIC(){
  var obs=((document.getElementById('ic-resolve-obs')||{}).value||'').trim();
  var ics=getICs();
  var idx=ics.findIndex(function(d){return d.id===icResolveId;});
  if(idx===-1)return;
  ics[idx].status='resolvido';
  ics[idx].resolucao={data:todayKey(),hora:fmtTime(),profissional:currentProfissional,obs:obs};
  saveICs(ics);
  document.getElementById('modal-ic-resolve').style.display='none';
  addNotif('Intercorrencia resolvida: '+ics[idx].tipo+' por '+currentProfissional);
  toast('Intercorrencia marcada como resolvida');
  renderIntercorrencias();
}
function eliminarIC(id){
  var ics=getICs().filter(function(d){return d.id!==id;});
  saveICs(ics);renderIntercorrencias();
}
function renderIntercorrencias(){
  var flt=(document.getElementById('ic-filter-data')||{}).value||'';
  var ics=getICs();
  if(flt)ics=ics.filter(function(d){return d.data===flt;});
  if(icFilter==='pendentes')ics=ics.filter(function(d){return d.status!=='resolvido';});
  else if(icFilter==='resolvidos')ics=ics.filter(function(d){return d.status==='resolvido';});
  var c=document.getElementById('ic-list');if(!c)return;
  if(!ics.length){c.innerHTML='<div class="no-data">Nenhuma intercorrencia encontrada.</div>';return;}
  c.innerHTML=ics.map(function(ic){
    var res=ic.status==='resolvido';
    var cor=res?'#059669':'#1a56db';
    var badge=res
      ?'<span class="badge" style="background:#059669;color:#fff;">Resolvido '+fmtDate(ic.resolucao.data)+'</span>'
      :'<span class="badge" style="background:#1a56db;color:#fff;">Intercorrencia do Dia</span>';
    var acoes=res
      ?'<span style="font-size:.68rem;color:#059669;font-weight:600;">Encerrada</span>'
      :'<button class="btn btn-sm" style="background:#059669;color:#fff;" onclick="abrirResolverIC(\''+ic.id+'\')">Marcar Resolvida</button>';
    return '<div class="doc-card" style="border-left:4px solid '+cor+';'+(res?'opacity:.82;':'')+';">'
      +'<div class="doc-card-header">'+badge+'<span class="doc-data">'+fmtDate(ic.data)+' '+ic.hora+'</span></div>'
      +'<div class="doc-card-body">'
      +'<div class="doc-assunto" style="white-space:pre-line;font-size:.8rem;">'+ic.descricao+'</div>'
      +(res&&ic.resolucao?'<div class="doc-assunto" style="color:#059669;font-weight:600;margin-top:6px;">'+(ic.resolucao.obs?'Resolucao: '+ic.resolucao.obs:'Resolvida sem observacoes')+'</div>'
        +'<div class="doc-assunto" style="color:var(--muted);font-size:.65rem;">Por '+ic.resolucao.profissional+' em '+fmtDate(ic.resolucao.data)+' '+ic.resolucao.hora+'</div>':'')
      +'<div class="doc-prof">'+ic.profissional+'</div>'
      +'<div style="margin-top:8px;display:flex;gap:6px;flex-wrap:wrap;">'+acoes
      +'<button class="btn btn-outline btn-xs" style="color:var(--red);border-color:var(--red);" onclick="eliminarIC(\''+ic.id+'\')">Eliminar</button></div>'
      +'</div></div>';
  }).join('');
}
function exportICPDF(){
  if(typeof jspdf==='undefined'){toast('Biblioteca PDF a carregar, tente novamente','err');return;}
  var flt=(document.getElementById('ic-filter-data')||{}).value||'';
  var ics=getICs();
  if(flt)ics=ics.filter(function(d){return d.data===flt;});
  if(icFilter==='pendentes')ics=ics.filter(function(d){return d.status!=='resolvido';});
  else if(icFilter==='resolvidos')ics=ics.filter(function(d){return d.status==='resolvido';});
  var doc=new jspdf.jsPDF();
  doc.setFontSize(13);doc.setFont('helvetica','bold');
  doc.text('Hospital do Prenda — Intercorrencias do Servico',14,14);
  doc.setFontSize(8.5);doc.setFont('helvetica','normal');doc.setTextColor(80);
  doc.text('Exportado em '+new Date().toLocaleString('pt-PT')+(currentProfissional?' por '+currentProfissional:''),14,21);
  doc.setTextColor(0);
  var rows=ics.map(function(ic){
    return [fmtDate(ic.data)+' '+ic.hora,ic.descricao.substring(0,70),
      ic.status==='resolvido'?'Resolvido':'Pendente',
      ic.resolucao&&ic.resolucao.obs?ic.resolucao.obs:'',ic.profissional];
  });
  doc.autoTable({
    startY:26,
    head:[['Data/Hora','Descricao','Estado','Resolucao','Profissional']],
    body:rows,
    styles:{fontSize:8,cellPadding:2},
    headStyles:{fillColor:[26,86,219],textColor:255,fontStyle:'bold'},
    alternateRowStyles:{fillColor:[240,244,255]},
    columnStyles:{1:{cellWidth:80}}
  });
  var fname='intercorrencias_'+todayKey()+'.pdf';
  doc.save(fname);
  toast('PDF guardado: '+fname,'info');
}

// ═══ BACKUP AUTOMATICO ═══
function allDataBackup(){
  var d={ts:new Date().toISOString(),docs:getDocs(),config:getConfig(),notifs:JSON.parse(localStorage.getItem(NOTIF_KEY)||'[]'),areas:{},intercorrencias:getICs()};
  Object.keys(AREA_INFO).forEach(function(k){d.areas[k]=getAreaDocs(k);});
  return d;
}
function downloadBackup(silent){
  var blob=new Blob([JSON.stringify(allDataBackup(),null,2)],{type:'application/json'});
  var url=URL.createObjectURL(blob);var a=document.createElement('a');a.href=url;
  a.download='backup_secretaria_'+todayKey()+'.json';
  document.body.appendChild(a);a.click();document.body.removeChild(a);URL.revokeObjectURL(url);
  localStorage.setItem('hp_last_backup',todayKey());
  renderBackupStatus();
  if(!silent)toast('Backup realizado — backup_secretaria_'+todayKey()+'.json','info');
}
function triggerAutoBackup(){
  if('Notification' in window&&Notification.permission==='granted'){
    try{var n=new Notification('Hospital do Prenda — Secretaria',{body:'Backup diario automatico das 14:00 em curso...'});setTimeout(function(){n.close();},6000);}catch(e){}
  }
  downloadBackup(true);
  toast('Backup automatico das 14h efectuado','info');
}
function requestNotifPerm(){
  if(!('Notification' in window)){toast('Notificacoes nao suportadas neste browser','err');return;}
  Notification.requestPermission().then(function(p){
    toast(p==='granted'?'Notificacoes activadas! Sera avisado as 14h.':'Permissao recusada',p==='granted'?'ok':'err');
    renderBackupStatus();
  });
}
function renderBackupStatus(){
  var el=document.getElementById('backup-status');if(!el)return;
  var last=localStorage.getItem('hp_last_backup')||null;
  var perm='indisponivel';
  if('Notification' in window){var pm=Notification.permission;perm=pm==='granted'?'Activadas':pm==='denied'?'Bloqueadas':'Nao solicitadas';}
  el.innerHTML='<div style="font-size:.7rem;color:var(--muted);padding:8px 10px;background:rgba(0,0,0,.03);border-radius:6px;">'
    +'Ultimo backup: <strong>'+(last?fmtDate(last):'Nunca realizado')+'</strong>'
    +' &nbsp;|&nbsp; Notificacoes browser: <strong>'+perm+'</strong></div>';
}
function setupBackupScheduler(){
  renderBackupStatus();
  setInterval(function(){
    var now=new Date();
    if(now.getHours()===14&&now.getMinutes()===0){
      if(localStorage.getItem('hp_last_backup')!==todayKey())triggerAutoBackup();
    }
  },58000);
}

// ═══ THEME / SPLASH / INIT ═══
function toggleTheme(){var dark=document.documentElement.classList.toggle('dark');localStorage.setItem('theme',dark?'dark':'light');}
(function(){var D=5000,ring=document.getElementById('spl-ring'),pct=document.getElementById('spl-pct'),C=263.9,start=null;
  if(!ring)return;
  function step(ts){if(!start)start=ts;var p=Math.min((ts-start)/D,1),e=p<.5?2*p*p:-1+(4-2*p)*p;
    ring.style.strokeDashoffset=C*(1-e);if(pct)pct.textContent=Math.round(e*100)+'%';
    if(p<1){requestAnimationFrame(step);return;}
    var s=document.getElementById('splash');if(s){s.style.transition='opacity .45s';s.style.opacity='0';setTimeout(function(){s.style.display='none';},450);}
  }requestAnimationFrame(step);
})();
document.addEventListener('DOMContentLoaded',function(){
  checkSession();
  var dd=document.getElementById('desp-filter-data');if(dd)dd.value=todayKey();
  var rf=document.getElementById('rh-filter-data');if(rf)rf.value=todayKey();
  initRHMemoNum();
  var range=getDateRange('mes');var sf=document.getElementById('stats-from');if(sf)sf.value=range.start;var st=document.getElementById('stats-to');if(st)st.value=range.end;
  var icd=document.getElementById('ic-data');if(icd)icd.value=todayKey();
  var ich=document.getElementById('ic-hora');if(ich)ich.value=fmtTime();
  setupBackupScheduler();
});
"""


def build_html():
    sidebar = (
        '<nav class="sidebar">'
        '<div class="nav-section-lbl">Direccao Geral</div>'
        '<div class="nav-item active" data-section="sec-dg" onclick="showSection(\'sec-dg\')">'
        '<svg viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>'
        '<path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>Direccao Geral</div>'
        '<div class="nav-item" data-section="sec-despacho" onclick="showSection(\'sec-despacho\')">'
        '<svg viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/>'
        '<polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>Despacho</div>'
        '<div class="nav-section-lbl">Areas Hospitalares</div>'
        '<div class="nav-item" data-area="clinica" onclick="showArea(\'clinica\')">'
        '<svg viewBox="0 0 24 24"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>Direccao Clinica</div>'
        '<div class="nav-item" data-area="cientifica" onclick="showArea(\'cientifica\')">'
        '<svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>'
        'Dir. Cientifica e Pedagogica</div>'
        '<div class="nav-item" data-area="enfermagem" onclick="showArea(\'enfermagem\')">'
        '<svg viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>'
        'Dir. de Enfermagem</div>'
        '<div class="nav-item" data-area="administrativa" onclick="showArea(\'administrativa\')">'
        '<svg viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="2"/>'
        '<path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>Dir. Administrativa</div>'
        '<div class="nav-item" data-section="sec-rh" onclick="showSection(\'sec-rh\')">'
        '<svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>'
        '<circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/>'
        '<path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>Recursos Humanos</div>'
        '<div class="nav-section-lbl">Analise</div>'
        '<div class="nav-item" data-section="sec-intercorrencias" onclick="showSection(\'sec-intercorrencias\')">'
        '<svg viewBox="0 0 24 24"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>'
        '<line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>Intercorrencias</div>'
        '<div class="nav-item" data-section="sec-stats" onclick="showSection(\'sec-stats\')">'
        '<svg viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/>'
        '<line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>Estatisticas</div>'
        '<div class="nav-section-lbl">Consulta</div>'
        '<div class="nav-item" data-section="sec-pesquisa" onclick="showSection(\'sec-pesquisa\')">'
        '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/>'
        '<line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>Pesquisar</div>'
        '<div class="nav-section-lbl">Sistema</div>'
        '<div class="nav-item" data-section="sec-definicoes" onclick="showSection(\'sec-definicoes\')">'
        '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/>'
        '<path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06'
        'a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09'
        'A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06'
        'A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09'
        'A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06'
        'A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09'
        'a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06'
        'A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09'
        'a1.65 1.65 0 0 0-1.51 1z"/></svg>Definicoes</div>'
        '</nav>'
    )
    return (
        '<!DOCTYPE html>\n<html lang="pt">\n<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1.0">\n'
        '<title>Secretaria Geral - Hospital do Prenda</title>\n'
        '<script>if(localStorage.getItem("theme")==="dark")document.documentElement.classList.add("dark");</script>\n'
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>\n'
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>\n'
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.8.2/jspdf.plugin.autotable.min.js"></script>\n'
        '<style>' + CSS + '</style>\n'
        '</head>\n<body>\n'
        + MODAL_LOGIN + MODAL_EDIT + MODAL_VOLTOU + MODAL_IC_RESOLVE +
        '<div id="splash"><div class="splash-inner">'
        '<div class="splash-img-ring"><div class="splash-img-circle"><img src="__HOSP_IMG__" alt="HP"></div>'
        '<svg class="splash-progress-svg" viewBox="0 0 100 100">'
        '<circle class="spl-ring-bg" cx="50" cy="50" r="42"/>'
        '<circle class="spl-ring-fg" id="spl-ring" cx="50" cy="50" r="42" stroke-dasharray="__CIRC__" stroke-dashoffset="__CIRC__"/>'
        '</svg></div>'
        '<p class="splash-hosp-lbl">Hospital do Prenda &middot; Luanda</p>'
        '<h1 class="splash-svc-lbl">Secretaria Geral</h1>'
        '<div class="splash-pct" id="spl-pct">0%</div>'
        '</div></div>\n'
        '<div class="hp-staff-bar">'
        '<span class="hp-staff-lbl">Profissional</span>'
        '<span class="hp-staff-name" id="staff-prof-name">---</span>'
        '<span class="hp-staff-sep">&middot;</span>'
        '<button class="hbtn" onclick="doLogout()">Sair</button>'
        '<div style="margin-left:auto;display:flex;gap:8px;">'
        '<button class="hbtn" onclick="toggleTheme()">Tema</button>'
        '</div></div>\n'
        '<header>'
        '<div class="header-logo"><img src="__HOSP_IMG__" alt="HP"></div>'
        '<div class="header-title"><h1>Secretaria Geral &mdash; Registo de Correspondencia</h1>'
        '<span>Hospital do Prenda &middot; Luanda &middot; Angola</span></div>'
        '</header>\n'
        '<div class="layout">' + sidebar + '<main class="main">\n'
        + SEC_DG + SEC_DESPACHO + SEC_AREA + SEC_RH + SEC_INTERCORRENCIAS + SEC_STATS + SEC_PESQUISA + SEC_DEFINICOES +
        '</main></div>\n'
        '<div id="toast"></div>\n'
        '<script>' + JS + '</script>\n'
        '</body></html>\n'
    )

HTML = build_html()
HTML = HTML.replace('__HOSP_IMG__', HOSP_IMG)
HTML = HTML.replace('__CIRC__', CIRC)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(HTML)
print('Gerado: ' + OUT)
print('Tamanho: ' + str(round(os.path.getsize(OUT)/1024, 1)) + ' KB')
