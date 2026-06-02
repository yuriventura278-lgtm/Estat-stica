#!/usr/bin/env python3
"""Gera secretaria_geral.html — Secretaria Geral + 5 áreas hospitalares."""
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

CSS = '''
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
:root{
  --header-h:56px;--staff-h:38px;--sidebar-w:230px;
  --bg:#f4f6fa;--surface:#ffffff;--surface2:#f1f5f9;
  --border:#e2e8f0;--text:#0f172a;--muted:#64748b;
  --accent:#1a56db;--accent2:#00d4aa;--red:#ef4444;--amber:#f59e0b;
  --green:#10b981;--purple:#7c3aed;
  --fh:'Inter',sans-serif;--fm:'IBM Plex Mono',monospace;
  --shadow:0 1px 3px rgba(0,0,0,.08),0 4px 16px rgba(0,0,0,.06);
}
html.dark{
  --bg:#0c0f14;--surface:#141820;--surface2:#0f1520;
  --border:rgba(30,40,64,.9);--text:#e2e8f0;--muted:#64748b;
}
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
.splash-pct{font-size:.65rem;color:#00d4aa;font-weight:600;letter-spacing:.05em;font-family:var(--fm);}
.hp-staff-bar{position:fixed;top:0;left:0;right:0;z-index:190;height:var(--staff-h);
  background:rgba(26,86,219,.06);border-bottom:1px solid rgba(26,86,219,.15);
  display:flex;align-items:center;gap:12px;padding:0 20px;}
html.dark .hp-staff-bar{background:rgba(26,86,219,.1);border-bottom-color:rgba(26,86,219,.2);}
.hp-staff-lbl{font-size:.46rem;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:1.4px;white-space:nowrap;}
.hp-staff-sep{color:var(--border);font-size:.8rem;}
.hp-staff-inp{background:transparent;border:none;border-bottom:1px solid rgba(26,86,219,.25);
  color:var(--text);font-family:var(--fh);font-size:.68rem;padding:2px 6px;outline:none;min-width:150px;max-width:220px;}
.hp-staff-inp:focus{border-bottom-color:rgba(26,86,219,.7);}
header{position:fixed;top:var(--staff-h);left:0;right:0;z-index:180;height:var(--header-h);
  background:var(--surface);border-bottom:1px solid var(--border);
  display:flex;align-items:center;padding:0 20px;gap:16px;box-shadow:0 1px 4px rgba(0,0,0,.06);}
.header-logo{width:32px;height:32px;border-radius:50%;overflow:hidden;flex-shrink:0;}
.header-logo img{width:100%;height:100%;object-fit:cover;}
.header-title{flex:1;}
.header-title h1{font-size:.78rem;font-weight:700;}
.header-title span{font-size:.56rem;color:var(--muted);}
.header-right{display:flex;align-items:center;gap:10px;margin-left:auto;}
#theme-toggle{padding:5px 11px;border-radius:4px;cursor:pointer;background:transparent;
  border:1px solid var(--border);color:var(--text);font-size:.57rem;font-weight:600;
  letter-spacing:.4px;text-transform:uppercase;display:inline-flex;align-items:center;gap:5px;}
#theme-toggle:hover{border-color:var(--accent);}
.layout{display:flex;margin-top:calc(var(--staff-h) + var(--header-h));min-height:calc(100vh - var(--staff-h) - var(--header-h));}
.sidebar{width:var(--sidebar-w);flex-shrink:0;background:var(--surface);border-right:1px solid var(--border);
  padding:16px 0;position:sticky;top:calc(var(--staff-h) + var(--header-h));
  height:calc(100vh - var(--staff-h) - var(--header-h));overflow-y:auto;}
.nav-section-lbl{font-size:.47rem;font-weight:700;letter-spacing:.15em;text-transform:uppercase;
  color:var(--muted);padding:14px 20px 6px;}
.nav-item{display:flex;align-items:center;gap:10px;padding:9px 20px;cursor:pointer;
  font-size:.72rem;color:var(--muted);font-weight:500;transition:all .13s;border-left:3px solid transparent;}
.nav-item:hover{color:var(--text);background:var(--surface2);}
.nav-item.active{color:var(--accent);background:rgba(26,86,219,.06);border-left-color:var(--accent);font-weight:600;}
.nav-item svg{width:15px;height:15px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;flex-shrink:0;}
.main{flex:1;padding:24px;min-width:0;}
.section{display:none;max-width:960px;}
.section.active{display:block;}
.page-header{margin-bottom:20px;}
.page-title{font-size:1.05rem;font-weight:700;}
.page-sub{font-size:.68rem;color:var(--muted);margin-top:2px;}
.card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:20px;margin-bottom:16px;box-shadow:var(--shadow);}
.card-title{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.09em;color:var(--muted);margin-bottom:14px;display:flex;align-items:center;gap:8px;}
.card-title .ct-badge{font-size:.6rem;font-weight:500;letter-spacing:normal;color:var(--muted);text-transform:none;margin-left:auto;}
.num-preview{background:rgba(26,86,219,.07);border:1px solid rgba(26,86,219,.2);border-radius:10px;padding:14px 18px;display:flex;align-items:center;gap:16px;margin-bottom:16px;}
html.dark .num-preview{background:rgba(26,86,219,.11);border-color:rgba(26,86,219,.28);}
.num-preview-label{font-size:.58rem;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:.1em;}
.num-preview-val{font-family:var(--fm);font-size:1.6rem;font-weight:700;color:var(--accent);}
.num-preview-sub{font-size:.6rem;color:var(--muted);margin-top:2px;}
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
@media(max-width:640px){.form-grid{grid-template-columns:1fr;}}
.span2{grid-column:span 2;}
.field-group{display:flex;flex-direction:column;gap:5px;}
label{font-size:.57rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;}
input[type="text"],input[type="date"],input[type="number"],select,textarea{
  background:var(--surface2);border:1px solid var(--border);color:var(--text);
  font-family:var(--fh);font-size:.78rem;padding:8px 12px;border-radius:7px;outline:none;width:100%;transition:border-color .13s;}
input:focus,select:focus,textarea:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(26,86,219,.1);}
textarea{resize:vertical;min-height:68px;}
html.dark input,html.dark select,html.dark textarea{background:rgba(255,255,255,.04);border-color:rgba(255,255,255,.1);}
input[readonly]{color:var(--muted);cursor:not-allowed;}
.btn{padding:9px 18px;border-radius:7px;cursor:pointer;font-family:var(--fh);font-size:.72rem;font-weight:600;border:none;transition:all .15s;display:inline-flex;align-items:center;gap:6px;}
.btn-primary{background:var(--accent);color:#fff;}
.btn-primary:hover{background:#1648c8;}
.btn-outline{background:transparent;color:var(--text);border:1px solid var(--border);}
.btn-outline:hover{border-color:var(--accent);color:var(--accent);}
.btn-sm{padding:6px 14px;font-size:.65rem;}
input[type="file"]{background:var(--surface2);border:1px dashed var(--border);color:var(--text);font-size:.72rem;padding:7px 12px;border-radius:7px;width:100%;cursor:pointer;}
input[type="file"]:hover{border-color:var(--accent);}
.doc-list{display:flex;flex-direction:column;gap:10px;}
.doc-card{background:var(--surface);border:1px solid var(--border);border-radius:10px;overflow:hidden;}
.doc-card.doc-despachado{border-left:4px solid var(--green);}
.doc-card.doc-pendente{border-left:4px solid var(--amber);}
.doc-card.doc-recebido{border-left:4px solid var(--accent);}
.doc-card-header{display:flex;align-items:center;gap:8px;padding:9px 14px;
  background:var(--surface2);border-bottom:1px solid var(--border);flex-wrap:wrap;}
.doc-num{font-family:var(--fm);font-size:.75rem;font-weight:700;color:var(--accent);
  background:rgba(26,86,219,.1);padding:3px 8px;border-radius:4px;white-space:nowrap;}
html.dark .doc-num{background:rgba(26,86,219,.18);}
.doc-tipo-badge{font-size:.58rem;font-weight:600;padding:3px 8px;border-radius:12px;
  background:rgba(0,212,170,.1);color:#00957a;text-transform:uppercase;letter-spacing:.05em;white-space:nowrap;}
html.dark .doc-tipo-badge{background:rgba(0,212,170,.15);color:#00d4aa;}
.doc-data{font-size:.6rem;color:var(--muted);font-family:var(--fm);margin-left:auto;}
.despachado-badge{font-size:.58rem;font-weight:600;padding:3px 8px;border-radius:12px;background:rgba(16,185,129,.1);color:#059669;}
html.dark .despachado-badge{background:rgba(16,185,129,.15);color:#34d399;}
.pendente-badge{font-size:.58rem;font-weight:600;padding:3px 8px;border-radius:12px;background:rgba(245,158,11,.1);color:#d97706;}
html.dark .pendente-badge{background:rgba(245,158,11,.14);color:#fbbf24;}
.recebido-badge{font-size:.58rem;font-weight:600;padding:3px 8px;border-radius:12px;background:rgba(26,86,219,.1);color:var(--accent);}
html.dark .recebido-badge{background:rgba(26,86,219,.18);}
.doc-card-body{padding:12px 14px;}
.doc-inst{font-size:.82rem;font-weight:700;margin-bottom:4px;}
.doc-oficio{font-size:.67rem;color:var(--muted);font-family:var(--fm);margin-bottom:3px;}
.doc-assunto{font-size:.74rem;line-height:1.45;}
.doc-anexo{font-size:.62rem;color:var(--muted);margin-top:5px;}
.doc-despacho-info{padding:10px 14px;background:rgba(16,185,129,.04);border-top:1px solid var(--border);}
html.dark .doc-despacho-info{background:rgba(16,185,129,.06);}
.desp-form{padding:14px;border-top:1px solid var(--border);background:var(--surface2);}
html.dark .desp-form{background:rgba(255,255,255,.02);}
.desp-form-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:10px;}
@media(max-width:620px){.desp-form-row{grid-template-columns:1fr;}}
.btn-despachar{background:var(--accent);color:#fff;padding:8px 18px;border-radius:7px;border:none;
  font-family:var(--fh);font-size:.72rem;font-weight:600;cursor:pointer;display:inline-flex;align-items:center;gap:6px;}
.btn-despachar:hover{background:#1648c8;}
.desp-detail-table{width:100%;border-collapse:collapse;font-size:.68rem;}
.desp-detail-table td{padding:4px 8px;}
.desp-detail-table td:first-child{color:var(--muted);font-weight:600;white-space:nowrap;width:135px;text-transform:uppercase;font-size:.57rem;letter-spacing:.05em;}
.search-row{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px;align-items:flex-end;}
.search-box{flex:2;min-width:200px;position:relative;}
.search-box input{padding-left:34px;}
.search-icon{position:absolute;left:11px;top:50%;transform:translateY(-50%);color:var(--muted);pointer-events:none;}
.search-icon svg{width:14px;height:14px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;}
.pesq-stats{font-size:.65rem;color:var(--muted);margin-top:6px;}
.kpi-row{display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:10px;margin-bottom:16px;}
.kpi-box{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:12px 14px;text-align:center;}
.kpi-label{font-size:.51rem;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin-bottom:4px;font-weight:600;}
.kpi-val{font-family:var(--fm);font-size:1.55rem;font-weight:700;}
.kpi-accent{border-color:rgba(26,86,219,.3);}
.kpi-accent .kpi-val{color:var(--accent);}
.kpi-green{border-color:rgba(16,185,129,.3);}
.kpi-green .kpi-val{color:var(--green);}
.kpi-amber{border-color:rgba(245,158,11,.3);}
.kpi-amber .kpi-val{color:var(--amber);}
.def-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:20px;margin-bottom:16px;}
html.dark .def-card{background:#141820;border-color:#1e2840;}
.def-section-title{font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--muted);margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid var(--border);}
.def-preview-box{background:rgba(26,86,219,.06);border:1px dashed rgba(26,86,219,.3);border-radius:8px;padding:12px 16px;margin-top:12px;display:flex;align-items:center;gap:12px;}
.def-preview-lbl{font-size:.57rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;font-weight:600;}
.def-preview-num{font-family:var(--fm);font-size:1.3rem;font-weight:700;color:var(--accent);}
.def-info{font-size:.68rem;color:var(--muted);line-height:1.65;margin-top:12px;padding:10px 14px;background:var(--surface2);border-radius:7px;}
.no-data-msg{text-align:center;padding:30px 20px;color:var(--muted);font-size:.78rem;background:var(--surface2);border-radius:10px;}
.filter-bar{display:flex;gap:12px;align-items:flex-end;flex-wrap:wrap;padding-bottom:14px;border-bottom:1px solid var(--border);margin-bottom:14px;}
hr{border:none;border-top:1px solid var(--border);margin:18px 0;}
#toast{position:fixed;bottom:24px;right:24px;padding:11px 18px;border-radius:8px;font-size:.75rem;font-weight:600;z-index:9998;pointer-events:none;opacity:0;transform:translateY(20px);transition:all .3s;max-width:340px;}
.toast-ok{background:#059669;color:#fff;}
.toast-err{background:#dc2626;color:#fff;}
/* ── AREA TABS ── */
.area-sub-tabs{display:flex;border-bottom:2px solid var(--border);margin-bottom:18px;overflow-x:auto;gap:0;}
.area-sub-btn{padding:9px 15px;border:none;background:transparent;cursor:pointer;font-family:var(--fh);font-size:.67rem;font-weight:600;color:var(--muted);border-bottom:2px solid transparent;margin-bottom:-2px;white-space:nowrap;transition:all .15s;}
.area-sub-btn:hover{color:var(--text);}
.area-sub-btn.active{color:var(--accent);border-bottom-color:var(--accent);}
.area-sub-panel{display:none;}
.area-sub-panel.active{display:block;}
/* ── 3-DATE TIMELINE ── */
.date-timeline{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px;}
.date-chip{display:flex;flex-direction:column;gap:2px;background:var(--surface2);border:1px solid var(--border);border-radius:7px;padding:6px 10px;}
.date-chip-label{font-size:.46rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);}
.date-chip-val{font-size:.72rem;font-weight:700;font-family:var(--fm);}
.date-chip.dc-despacho{border-color:rgba(245,158,11,.4);}
.date-chip.dc-despacho .date-chip-val{color:var(--amber);}
.date-chip.dc-entrada{border-color:rgba(16,185,129,.4);}
.date-chip.dc-entrada .date-chip-val{color:var(--green);}
/* ── RH BADGES ── */
.rh-tipo-badge{font-size:.57rem;font-weight:600;padding:3px 8px;border-radius:12px;letter-spacing:.04em;white-space:nowrap;}
.rh-tipo-jf{background:rgba(239,68,68,.1);color:#dc2626;}
.rh-tipo-mf{background:rgba(139,92,246,.1);color:#7c3aed;}
.rh-tipo-tt{background:rgba(14,165,233,.1);color:#0284c7;}
.rh-tipo-outro{background:rgba(100,116,139,.1);color:var(--muted);}
.rh-num{font-family:var(--fm);font-size:.75rem;font-weight:700;color:#7c3aed;background:rgba(139,92,246,.1);padding:3px 8px;border-radius:4px;}
html.dark .rh-tipo-jf{background:rgba(239,68,68,.15);}
html.dark .rh-tipo-mf{background:rgba(139,92,246,.15);color:#a78bfa;}
html.dark .rh-tipo-tt{background:rgba(14,165,233,.15);color:#38bdf8;}
html.dark .rh-num{background:rgba(139,92,246,.18);color:#a78bfa;}
html.dark header{background:#141820;border-bottom-color:#1e2840;}
html.dark .sidebar{background:#141820;border-right-color:#1e2840;}
html.dark .card{background:#141820;border-color:#1e2840;}
html.dark .doc-card{background:#141820;border-color:#1e2840;}
html.dark .doc-card-header{background:rgba(255,255,255,.03);border-bottom-color:#1e2840;}
html.dark .kpi-box{background:#141820;border-color:#1e2840;}
'''

SIDEBAR_AREAS = '''
    <div class="nav-section-lbl">Areas Hospitalares</div>
    <div class="nav-item" data-area="clinica" onclick="showArea('clinica')">
      <svg viewBox="0 0 24 24"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
      Direccao Clinica
    </div>
    <div class="nav-item" data-area="cientifica" onclick="showArea('cientifica')">
      <svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
      Dir. Cientifica e Pedagogica
    </div>
    <div class="nav-item" data-area="enfermagem" onclick="showArea('enfermagem')">
      <svg viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
      Dir. de Enfermagem
    </div>
    <div class="nav-item" data-area="administrativa" onclick="showArea('administrativa')">
      <svg viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
      Dir. Administrativa
    </div>
    <div class="nav-item" data-section="sec-rh" onclick="showSection('sec-rh')">
      <svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
      Recursos Humanos
    </div>
'''

SEC_AREA = '''
    <!-- SEC-AREA: generic shared section for Clinica / Cientifica / Enfermagem / Administrativa -->
    <section id="sec-area" class="section">
      <div class="page-header">
        <div class="page-title" id="area-page-title">Area Hospitalar</div>
        <div class="page-sub" id="area-page-sub">Documentos recebidos e registos internos</div>
      </div>

      <div class="area-sub-tabs">
        <button class="area-sub-btn active" data-atab="recebidos" onclick="switchAreaTab('recebidos')">
          Documentos Recebidos da DG
        </button>
        <button class="area-sub-btn" data-atab="internos" onclick="switchAreaTab('internos')">
          Documentos Internos
        </button>
      </div>

      <!-- Panel: Recebidos -->
      <div id="area-panel-recebidos" class="area-sub-panel active">
        <div class="card">
          <div class="filter-bar">
            <div class="field-group" style="flex:1;min-width:160px;">
              <label>Filtrar por Data de Registo</label>
              <input type="date" id="area-filter-data" onchange="renderAreaReceived()">
            </div>
            <button class="btn btn-outline btn-sm"
              onclick="document.getElementById('area-filter-data').value='';renderAreaReceived()">
              Todos
            </button>
            <div id="area-kpis" style="display:flex;gap:8px;flex-wrap:wrap;align-items:flex-end;"></div>
          </div>
          <div id="area-docs-list" class="doc-list">
            <div class="no-data-msg">Nenhum documento despachado para esta area.</div>
          </div>
        </div>
      </div>

      <!-- Panel: Internos -->
      <div id="area-panel-internos" class="area-sub-panel">
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
            <div class="field-group">
              <label>Data *</label>
              <input type="date" id="area-int-data">
            </div>
            <div id="area-int-nome-f" class="field-group">
              <label>Nome *</label>
              <input type="text" id="area-int-nome" placeholder="Nome do profissional...">
            </div>
            <div id="area-int-servico-f" class="field-group">
              <label>Servico</label>
              <input type="text" id="area-int-servico" placeholder="Servico ou sector...">
            </div>
            <div id="area-int-descricao-f" class="field-group span2" style="display:none;">
              <label>Descricao *</label>
              <textarea id="area-int-descricao" rows="2" placeholder="Descricao do documento..."></textarea>
            </div>
          </div>
          <div style="margin-top:14px;display:flex;gap:8px;">
            <button class="btn btn-primary btn-sm" onclick="registarInternoArea()">Registar</button>
            <button class="btn btn-outline btn-sm" onclick="clearAreaIntForm()">Limpar</button>
          </div>
        </div>
        <div class="card">
          <div class="filter-bar">
            <div class="field-group" style="flex:1;">
              <label>Filtrar por Data</label>
              <input type="date" id="area-int-filter" onchange="renderAreaInternos()">
            </div>
            <button class="btn btn-outline btn-sm"
              onclick="document.getElementById('area-int-filter').value='';renderAreaInternos()">
              Todos
            </button>
          </div>
          <div id="area-internos-list" class="doc-list">
            <div class="no-data-msg">Nenhum documento interno registado.</div>
          </div>
        </div>
      </div>
    </section>
'''

SEC_RH = '''
    <!-- SEC-RH: Recursos Humanos -->
    <section id="sec-rh" class="section">
      <div class="page-header">
        <div class="page-title">Recursos Humanos</div>
        <div class="page-sub">Documentos recebidos, justificacoes de falta, memorandos de ferias e registos internos</div>
      </div>

      <div class="area-sub-tabs">
        <button class="area-sub-btn active" data-rhtab="recebidos" onclick="switchRHTab('recebidos')">
          Docs Recebidos da DG
        </button>
        <button class="area-sub-btn" data-rhtab="justfalta" onclick="switchRHTab('justfalta')">
          Justificacoes de Falta
        </button>
        <button class="area-sub-btn" data-rhtab="memorandos" onclick="switchRHTab('memorandos')">
          Memorandos de Ferias
        </button>
        <button class="area-sub-btn" data-rhtab="internos" onclick="switchRHTab('internos')">
          Outros Documentos
        </button>
      </div>

      <!-- RH Recebidos -->
      <div id="rh-panel-recebidos" class="area-sub-panel active">
        <div class="card">
          <div class="filter-bar">
            <div class="field-group" style="flex:1;min-width:160px;">
              <label>Filtrar por Data</label>
              <input type="date" id="rh-filter-data" onchange="renderRHReceived()">
            </div>
            <button class="btn btn-outline btn-sm"
              onclick="document.getElementById('rh-filter-data').value='';renderRHReceived()">
              Todos
            </button>
            <div id="rh-kpis" style="display:flex;gap:8px;flex-wrap:wrap;align-items:flex-end;"></div>
          </div>
          <div id="rh-docs-list" class="doc-list">
            <div class="no-data-msg">Nenhum documento despachado para Recursos Humanos.</div>
          </div>
        </div>
      </div>

      <!-- RH Justificacoes de Falta -->
      <div id="rh-panel-justfalta" class="area-sub-panel">
        <div class="card">
          <div class="card-title">Registar Justificacao de Falta</div>
          <div class="form-grid">
            <div class="field-group">
              <label>Nome *</label>
              <input type="text" id="rh-jf-nome" placeholder="Nome do funcionario...">
            </div>
            <div class="field-group">
              <label>Area / Servico *</label>
              <input type="text" id="rh-jf-area" placeholder="Area ou servico...">
            </div>
            <div class="field-group">
              <label>Data da Falta *</label>
              <input type="date" id="rh-jf-data">
            </div>
            <div class="field-group">
              <label>Observacoes</label>
              <input type="text" id="rh-jf-obs" placeholder="Motivo ou observacoes...">
            </div>
          </div>
          <div style="margin-top:14px;display:flex;gap:8px;">
            <button class="btn btn-primary btn-sm" onclick="registarJustFalta()">Registar</button>
            <button class="btn btn-outline btn-sm" onclick="clearJustFalta()">Limpar</button>
          </div>
        </div>
        <div class="card">
          <div class="filter-bar">
            <div class="field-group" style="flex:1;">
              <label>Filtrar por Data</label>
              <input type="date" id="rh-jf-filter" onchange="renderJustFaltas()">
            </div>
            <button class="btn btn-outline btn-sm"
              onclick="document.getElementById('rh-jf-filter').value='';renderJustFaltas()">Todos</button>
          </div>
          <div id="rh-jf-list" class="doc-list">
            <div class="no-data-msg">Nenhuma justificacao registada.</div>
          </div>
        </div>
      </div>

      <!-- RH Memorandos de Ferias -->
      <div id="rh-panel-memorandos" class="area-sub-panel">
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
            <div class="field-group">
              <label>Nome *</label>
              <input type="text" id="rh-memo-nome" placeholder="Nome do funcionario...">
            </div>
            <div class="field-group">
              <label>Area / Servico *</label>
              <input type="text" id="rh-memo-area" placeholder="Area ou servico...">
            </div>
            <div class="field-group">
              <label>Periodo / Tempo *</label>
              <input type="text" id="rh-memo-tempo" placeholder="Ex: 15 dias, 01/07 a 15/07...">
            </div>
            <div class="field-group">
              <label>Data do Memorando *</label>
              <input type="date" id="rh-memo-data">
            </div>
            <div class="field-group span2">
              <label>Observacoes</label>
              <textarea id="rh-memo-obs" rows="2" placeholder="Observacoes adicionais..."></textarea>
            </div>
          </div>
          <div style="margin-top:14px;display:flex;gap:8px;">
            <button class="btn btn-primary btn-sm" onclick="registarMemorando()">Registar</button>
            <button class="btn btn-outline btn-sm" onclick="clearMemorando()">Limpar</button>
          </div>
        </div>
        <div class="card">
          <div class="filter-bar">
            <div class="field-group" style="flex:1;">
              <label>Filtrar por Data</label>
              <input type="date" id="rh-memo-filter" onchange="renderMemorandos()">
            </div>
            <button class="btn btn-outline btn-sm"
              onclick="document.getElementById('rh-memo-filter').value='';renderMemorandos()">Todos</button>
          </div>
          <div id="rh-memo-list" class="doc-list">
            <div class="no-data-msg">Nenhum memorando de ferias registado.</div>
          </div>
        </div>
      </div>

      <!-- RH Internos -->
      <div id="rh-panel-internos" class="area-sub-panel">
        <div class="card">
          <div class="card-title">Registar Documento Interno</div>
          <div class="form-grid">
            <div class="field-group">
              <label>Tipo *</label>
              <select id="rh-int-tipo" onchange="toggleRHTipo()">
                <option value="trocaturno">Troca de Turno</option>
                <option value="outro">Outro Documento</option>
              </select>
            </div>
            <div class="field-group">
              <label>Data *</label>
              <input type="date" id="rh-int-data">
            </div>
            <div id="rh-int-nome-f" class="field-group">
              <label>Nome *</label>
              <input type="text" id="rh-int-nome" placeholder="Nome do profissional...">
            </div>
            <div id="rh-int-servico-f" class="field-group">
              <label>Servico</label>
              <input type="text" id="rh-int-servico" placeholder="Servico ou sector...">
            </div>
            <div id="rh-int-descricao-f" class="field-group span2" style="display:none;">
              <label>Descricao *</label>
              <textarea id="rh-int-descricao" rows="2" placeholder="Descricao..."></textarea>
            </div>
          </div>
          <div style="margin-top:14px;display:flex;gap:8px;">
            <button class="btn btn-primary btn-sm" onclick="registarRHInterno()">Registar</button>
            <button class="btn btn-outline btn-sm" onclick="clearRHIntForm()">Limpar</button>
          </div>
        </div>
        <div class="card">
          <div class="filter-bar">
            <div class="field-group" style="flex:1;">
              <label>Filtrar por Data</label>
              <input type="date" id="rh-int-filter" onchange="renderRHInternos()">
            </div>
            <button class="btn btn-outline btn-sm"
              onclick="document.getElementById('rh-int-filter').value='';renderRHInternos()">Todos</button>
          </div>
          <div id="rh-int-list" class="doc-list">
            <div class="no-data-msg">Nenhum documento interno registado.</div>
          </div>
        </div>
      </div>
    </section>
'''

JS_AREAS = r"""
// ══ AREA INFO MAP ══
var AREA_INFO = {
  'clinica':        { label: 'Direccao Clinica',               storageKey: 'hp_area_clinica',        dispatchName: 'Direccao Clinica' },
  'cientifica':     { label: 'Dir. Cientifica e Pedagogica',   storageKey: 'hp_area_cientifica',     dispatchName: 'Direccao Cientifica e Pedagogica' },
  'enfermagem':     { label: 'Dir. de Enfermagem',             storageKey: 'hp_area_enfermagem',     dispatchName: 'Direccao de Enfermagem' },
  'administrativa': { label: 'Dir. Administrativa',            storageKey: 'hp_area_administrativa', dispatchName: 'Direccao Administrativa' },
  'rh':             { label: 'Recursos Humanos',               storageKey: 'hp_area_rh',             dispatchName: 'Recursos Humanos' }
};
var currentArea = 'clinica';
var currentAreaTab = 'recebidos';
var currentRHTab = 'recebidos';

function getAreaDocs(key) {
  var raw = localStorage.getItem(AREA_INFO[key].storageKey);
  return raw ? JSON.parse(raw) : [];
}
function saveAreaDocs(key, docs) {
  localStorage.setItem(AREA_INFO[key].storageKey, JSON.stringify(docs));
}
function getRHMemoCfg() {
  var raw = localStorage.getItem('hp_rh_memo_cfg');
  return raw ? JSON.parse(raw) : { numAtual: 1, ano: new Date().getFullYear() };
}
function saveRHMemoCfg(c) { localStorage.setItem('hp_rh_memo_cfg', JSON.stringify(c)); }
function nextRHMemoNum() {
  var c = getRHMemoCfg(); var n = c.numAtual; c.numAtual = n + 1; saveRHMemoCfg(c); return n;
}
function fmtRHNum(num, ano) {
  return 'RH/' + (ano || new Date().getFullYear()) + '/' + String(num).padStart(3,'0');
}

// ── Show area section ──
function showArea(key) {
  document.querySelectorAll('.section').forEach(function(s) { s.classList.remove('active'); });
  document.querySelectorAll('.nav-item').forEach(function(n) { n.classList.remove('active'); });
  document.getElementById('sec-area').classList.add('active');
  var ni = document.querySelector('[data-area="'+key+'"]');
  if (ni) ni.classList.add('active');
  currentArea = key;
  var info = AREA_INFO[key];
  var th = document.getElementById('area-page-title');
  if (th) th.textContent = info.label;
  var ts = document.getElementById('area-page-sub');
  if (ts) ts.textContent = 'Documentos recebidos da Direccao Geral e registos internos — ' + info.label;
  var fd = document.getElementById('area-filter-data');
  if (fd) fd.value = '';
  switchAreaTab('recebidos');
}

function switchAreaTab(tab) {
  currentAreaTab = tab;
  var sec = document.getElementById('sec-area');
  sec.querySelectorAll('[data-atab]').forEach(function(b) { b.classList.remove('active'); });
  sec.querySelectorAll('.area-sub-panel').forEach(function(p) { p.classList.remove('active'); });
  var btn = sec.querySelector('[data-atab="'+tab+'"]');
  if (btn) btn.classList.add('active');
  var panel = document.getElementById('area-panel-'+tab);
  if (panel) panel.classList.add('active');
  if (tab === 'recebidos') renderAreaReceived();
  if (tab === 'internos') { renderAreaInternos(); }
}

// ── Dispatched docs for this area ──
function renderAreaReceived() {
  var info = AREA_INFO[currentArea];
  var flt  = (document.getElementById('area-filter-data') || {}).value || '';
  var all  = getDocs();
  var docs = all.filter(function(d) {
    return d.despacho && (d.despacho.area === info.dispatchName || d.despacho.area === info.label);
  });
  if (flt) docs = docs.filter(function(d) { return d.data === flt; });

  var kpis = document.getElementById('area-kpis');
  if (kpis) {
    var recv = docs.filter(function(d) { return d.recepcao; }).length;
    var pend = docs.length - recv;
    kpis.innerHTML =
      '<div class="kpi-box kpi-accent" style="min-width:80px;padding:8px 12px;">'
        +'<div class="kpi-label">Total</div><div class="kpi-val">'+docs.length+'</div></div>'
      +'<div class="kpi-box kpi-amber" style="min-width:80px;padding:8px 12px;">'
        +'<div class="kpi-label">Por Receber</div><div class="kpi-val">'+pend+'</div></div>'
      +'<div class="kpi-box kpi-green" style="min-width:80px;padding:8px 12px;">'
        +'<div class="kpi-label">Recebidos</div><div class="kpi-val">'+recv+'</div></div>';
  }
  var c = document.getElementById('area-docs-list');
  if (!docs.length) {
    c.innerHTML = '<div class="no-data-msg">Nenhum documento despachado para esta area' + (flt ? ' nesta data' : '') + '.</div>';
    return;
  }
  var sorted = docs.filter(function(d) { return !d.recepcao; })
    .concat(docs.filter(function(d) { return d.recepcao; }));
  c.innerHTML = sorted.map(function(d) { return areaReceivedCard(d, currentArea); }).join('');
}

function areaReceivedCard(d, areaKey) {
  var numStr = fmtNum(d.numProcesso, d.ano);
  var recv   = !!d.recepcao;
  var recvBadge = recv
    ? '<span class="recebido-badge">Entrada Dada</span>'
    : '<span class="pendente-badge">Aguarda Entrada</span>';

  var timeline = '<div class="date-timeline">'
    + '<div class="date-chip">'
      + '<span class="date-chip-label">Registo SG</span>'
      + '<span class="date-chip-val">' + fmtDate(d.data) + '</span></div>'
    + (d.despacho ? '<div class="date-chip dc-despacho">'
      + '<span class="date-chip-label">Despacho DG</span>'
      + '<span class="date-chip-val">' + fmtDate(d.despacho.data) + '</span></div>' : '')
    + (recv ? '<div class="date-chip dc-entrada">'
      + '<span class="date-chip-label">Entrada na Area</span>'
      + '<span class="date-chip-val">' + fmtDate(d.recepcao.data) + '</span></div>' : '')
    + '</div>';

  var actions = '';
  if (!recv) {
    actions = '<div class="desp-form">'
      + '<div class="desp-form-row" style="max-width:320px;">'
        + '<div class="field-group">'
          + '<label>Data de Entrada na Area</label>'
          + '<input type="date" id="rec-data-' + d.id + '" value="' + todayKey() + '">'
        + '</div>'
      + '</div>'
      + '<button class="btn-despachar" style="background:var(--green);" '
        + 'onclick="darEntrada(\'' + d.id + '\',\'' + areaKey + '\')">Dar Entrada</button>'
    + '</div>';
  } else {
    actions = '<div class="desp-form" style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;">'
      + '<span style="font-size:.7rem;color:var(--green);">Entrada registada em '
        + fmtDate(d.recepcao.data) + (d.recepcao.hora ? ' as ' + d.recepcao.hora : '') + '</span>'
      + '<button class="btn btn-outline btn-sm" '
        + 'onclick="desfazerEntrada(\'' + d.id + '\',\'' + areaKey + '\')">Desfazer</button>'
    + '</div>';
  }

  return '<div class="doc-card ' + (recv ? 'doc-recebido' : 'doc-pendente') + '">'
    + '<div class="doc-card-header">'
      + '<span class="doc-num">' + numStr + '</span>'
      + '<span class="doc-tipo-badge">' + d.tipoDoc + '</span>'
      + recvBadge
      + '<span class="doc-data">' + fmtDate(d.data) + '</span>'
    + '</div>'
    + '<div class="doc-card-body">'
      + '<div class="doc-inst"><strong>' + d.instituicao + '</strong></div>'
      + (d.oficio ? '<div class="doc-oficio">Oficio: ' + d.oficio + '</div>' : '')
      + '<div class="doc-assunto">' + d.assunto + '</div>'
      + (d.nomeAnexo ? '<div class="doc-anexo">' + d.nomeAnexo + '</div>' : '')
      + timeline
    + '</div>'
    + actions
  + '</div>';
}

function darEntrada(docId, areaKey) {
  var dataEl = document.getElementById('rec-data-' + docId);
  var data   = dataEl ? dataEl.value : todayKey();
  if (!data) { toast('Selecione a data de entrada', 'err'); return; }
  var docs = getDocs();
  var i = docs.findIndex(function(d) { return d.id === docId; });
  if (i === -1) return;
  docs[i].recepcao = { data: data, hora: fmtTime(), area: AREA_INFO[areaKey].dispatchName };
  saveDocs(docs);
  toast('Entrada registada com sucesso!');
  if (areaKey === 'rh') renderRHReceived(); else renderAreaReceived();
}

function desfazerEntrada(docId, areaKey) {
  if (!confirm('Desfazer o registo de entrada deste documento?')) return;
  var docs = getDocs();
  var i = docs.findIndex(function(d) { return d.id === docId; });
  if (i === -1) return;
  docs[i].recepcao = null;
  saveDocs(docs);
  toast('Entrada desfeita');
  if (areaKey === 'rh') renderRHReceived(); else renderAreaReceived();
}

// ── Area internos ──
function toggleAreaTipo() {
  var tipo = (document.getElementById('area-int-tipo') || {}).value || 'trocaturno';
  var nf = document.getElementById('area-int-nome-f');
  var sf = document.getElementById('area-int-servico-f');
  var df = document.getElementById('area-int-descricao-f');
  if (nf) nf.style.display = tipo === 'trocaturno' ? '' : 'none';
  if (sf) sf.style.display = tipo === 'trocaturno' ? '' : 'none';
  if (df) df.style.display = tipo === 'outro'       ? '' : 'none';
}

function registarInternoArea() {
  var tipo    = (document.getElementById('area-int-tipo')      || {}).value || '';
  var data    = (document.getElementById('area-int-data')      || {}).value || '';
  var nome    = ((document.getElementById('area-int-nome')     || {}).value || '').trim();
  var servico = ((document.getElementById('area-int-servico')  || {}).value || '').trim();
  var desc    = ((document.getElementById('area-int-descricao')|| {}).value || '').trim();
  if (!data) { toast('Selecione a data', 'err'); return; }
  if (tipo === 'trocaturno' && !nome) { toast('Preencha o nome', 'err'); return; }
  if (tipo === 'outro' && !desc)      { toast('Preencha a descricao', 'err'); return; }
  var doc = { id: uid(), tipo: tipo, data: data, hora: fmtTime(), nome: nome, servico: servico, descricao: desc };
  var docs = getAreaDocs(currentArea);
  docs.unshift(doc);
  saveAreaDocs(currentArea, docs);
  clearAreaIntForm();
  toast('Documento interno registado');
  renderAreaInternos();
}

function clearAreaIntForm() {
  ['area-int-nome','area-int-servico','area-int-descricao'].forEach(function(id) {
    var el = document.getElementById(id); if (el) el.value = '';
  });
  var t = document.getElementById('area-int-tipo'); if (t) t.selectedIndex = 0;
  toggleAreaTipo();
}

function renderAreaInternos() {
  var flt  = (document.getElementById('area-int-filter') || {}).value || '';
  var docs = getAreaDocs(currentArea);
  if (flt) docs = docs.filter(function(d) { return d.data === flt; });
  var c = document.getElementById('area-internos-list');
  if (!docs.length) { c.innerHTML = '<div class="no-data-msg">Nenhum documento interno registado.</div>'; return; }
  c.innerHTML = docs.map(function(d) { return internoCard(d); }).join('');
}

function internoCard(d) {
  var badge, info;
  if (d.tipo === 'trocaturno') {
    badge = '<span class="rh-tipo-badge rh-tipo-tt">Troca de Turno</span>';
    info  = '<strong>' + d.nome + '</strong>' + (d.servico ? ' &middot; ' + d.servico : '');
  } else {
    badge = '<span class="rh-tipo-badge rh-tipo-outro">Outro</span>';
    info  = d.descricao;
  }
  return '<div class="doc-card">'
    + '<div class="doc-card-header">' + badge
      + '<span class="doc-data">' + fmtDate(d.data) + ' ' + (d.hora || '') + '</span>'
    + '</div>'
    + '<div class="doc-card-body"><div class="doc-assunto">' + info + '</div></div>'
  + '</div>';
}

// ══ RH ══
function switchRHTab(tab) {
  currentRHTab = tab;
  var sec = document.getElementById('sec-rh');
  sec.querySelectorAll('[data-rhtab]').forEach(function(b) { b.classList.remove('active'); });
  sec.querySelectorAll('.area-sub-panel').forEach(function(p) { p.classList.remove('active'); });
  var btn = sec.querySelector('[data-rhtab="'+tab+'"]');
  if (btn) btn.classList.add('active');
  var panel = document.getElementById('rh-panel-'+tab);
  if (panel) panel.classList.add('active');
  if (tab === 'recebidos')  renderRHReceived();
  if (tab === 'justfalta')  renderJustFaltas();
  if (tab === 'memorandos') { initRHMemoNum(); renderMemorandos(); }
  if (tab === 'internos')   renderRHInternos();
}

function renderRH() { switchRHTab(currentRHTab || 'recebidos'); initRHMemoNum(); }

function renderRHReceived() {
  var info = AREA_INFO['rh'];
  var flt  = (document.getElementById('rh-filter-data') || {}).value || '';
  var all  = getDocs();
  var docs = all.filter(function(d) { return d.despacho && d.despacho.area === info.dispatchName; });
  if (flt) docs = docs.filter(function(d) { return d.data === flt; });
  var kpis = document.getElementById('rh-kpis');
  if (kpis) {
    var recv = docs.filter(function(d) { return d.recepcao; }).length;
    var pend = docs.length - recv;
    kpis.innerHTML =
      '<div class="kpi-box kpi-accent" style="min-width:80px;padding:8px 12px;">'
        +'<div class="kpi-label">Total</div><div class="kpi-val">'+docs.length+'</div></div>'
      +'<div class="kpi-box kpi-amber" style="min-width:80px;padding:8px 12px;">'
        +'<div class="kpi-label">Por Receber</div><div class="kpi-val">'+pend+'</div></div>'
      +'<div class="kpi-box kpi-green" style="min-width:80px;padding:8px 12px;">'
        +'<div class="kpi-label">Recebidos</div><div class="kpi-val">'+recv+'</div></div>';
  }
  var c = document.getElementById('rh-docs-list');
  if (!docs.length) { c.innerHTML = '<div class="no-data-msg">Nenhum documento despachado para Recursos Humanos.</div>'; return; }
  var sorted = docs.filter(function(d) { return !d.recepcao; }).concat(docs.filter(function(d) { return d.recepcao; }));
  c.innerHTML = sorted.map(function(d) { return areaReceivedCard(d, 'rh'); }).join('');
}

// Justificacoes de Falta
function registarJustFalta() {
  var nome = ((document.getElementById('rh-jf-nome') || {}).value || '').trim();
  var area = ((document.getElementById('rh-jf-area') || {}).value || '').trim();
  var data = (document.getElementById('rh-jf-data')  || {}).value || '';
  var obs  = ((document.getElementById('rh-jf-obs')  || {}).value || '').trim();
  if (!nome) { toast('Preencha o nome', 'err'); return; }
  if (!area) { toast('Preencha a area/servico', 'err'); return; }
  if (!data) { toast('Selecione a data', 'err'); return; }
  var doc = { id: uid(), tipo: 'justfalta', nome: nome, area: area, data: data, hora: fmtTime(), obs: obs };
  var docs = getAreaDocs('rh'); docs.unshift(doc); saveAreaDocs('rh', docs);
  clearJustFalta(); toast('Justificacao registada'); renderJustFaltas();
}
function clearJustFalta() {
  ['rh-jf-nome','rh-jf-area','rh-jf-obs'].forEach(function(id) { var el=document.getElementById(id); if(el) el.value=''; });
}
function renderJustFaltas() {
  var flt  = (document.getElementById('rh-jf-filter') || {}).value || '';
  var docs = getAreaDocs('rh').filter(function(d) { return d.tipo === 'justfalta'; });
  if (flt) docs = docs.filter(function(d) { return d.data === flt; });
  var c = document.getElementById('rh-jf-list');
  if (!docs.length) { c.innerHTML = '<div class="no-data-msg">Nenhuma justificacao registada.</div>'; return; }
  c.innerHTML = docs.map(function(d) {
    return '<div class="doc-card">'
      + '<div class="doc-card-header">'
        + '<span class="rh-tipo-badge rh-tipo-jf">Justificacao de Falta</span>'
        + '<span class="doc-data">' + fmtDate(d.data) + ' ' + (d.hora||'') + '</span>'
      + '</div>'
      + '<div class="doc-card-body">'
        + '<div class="doc-inst"><strong>' + d.nome + '</strong></div>'
        + '<div class="doc-oficio">Area: ' + d.area + '</div>'
        + (d.obs ? '<div class="doc-assunto">' + d.obs + '</div>' : '')
      + '</div>'
    + '</div>';
  }).join('');
}

// Memorandos de Ferias
function initRHMemoNum() {
  var c = getRHMemoCfg();
  var ano = new Date().getFullYear();
  var el = document.getElementById('rh-memo-num-val');
  if (el) el.textContent = fmtRHNum(c.numAtual, ano);
  var sub = document.getElementById('rh-memo-num-sub');
  if (sub) sub.textContent = 'Ano ' + ano;
}
function registarMemorando() {
  var nome  = ((document.getElementById('rh-memo-nome')  || {}).value || '').trim();
  var area  = ((document.getElementById('rh-memo-area')  || {}).value || '').trim();
  var tempo = ((document.getElementById('rh-memo-tempo') || {}).value || '').trim();
  var data  = (document.getElementById('rh-memo-data')   || {}).value || '';
  var obs   = ((document.getElementById('rh-memo-obs')   || {}).value || '').trim();
  if (!nome)  { toast('Preencha o nome', 'err'); return; }
  if (!area)  { toast('Preencha a area', 'err'); return; }
  if (!tempo) { toast('Preencha o periodo/tempo', 'err'); return; }
  if (!data)  { toast('Selecione a data', 'err'); return; }
  var num = nextRHMemoNum();
  var ano = new Date().getFullYear();
  var numStr = fmtRHNum(num, ano);
  var doc = { id: uid(), tipo: 'memorando', numMemo: num, anoMemo: ano, numStr: numStr,
    nome: nome, area: area, tempo: tempo, data: data, hora: fmtTime(), obs: obs };
  var docs = getAreaDocs('rh'); docs.unshift(doc); saveAreaDocs('rh', docs);
  clearMemorando(); initRHMemoNum(); toast('Memorando ' + numStr + ' registado'); renderMemorandos();
}
function clearMemorando() {
  ['rh-memo-nome','rh-memo-area','rh-memo-tempo','rh-memo-obs'].forEach(function(id) {
    var el=document.getElementById(id); if(el) el.value='';
  });
}
function renderMemorandos() {
  var flt  = (document.getElementById('rh-memo-filter') || {}).value || '';
  var docs = getAreaDocs('rh').filter(function(d) { return d.tipo === 'memorando'; });
  if (flt) docs = docs.filter(function(d) { return d.data === flt; });
  var c = document.getElementById('rh-memo-list');
  if (!docs.length) { c.innerHTML = '<div class="no-data-msg">Nenhum memorando de ferias registado.</div>'; return; }
  c.innerHTML = docs.map(function(d) {
    return '<div class="doc-card" style="border-left:4px solid #7c3aed;">'
      + '<div class="doc-card-header">'
        + '<span class="rh-num">' + d.numStr + '</span>'
        + '<span class="rh-tipo-badge rh-tipo-mf">Memorando de Ferias</span>'
        + '<span class="doc-data">' + fmtDate(d.data) + '</span>'
      + '</div>'
      + '<div class="doc-card-body">'
        + '<div class="doc-inst"><strong>' + d.nome + '</strong></div>'
        + '<div class="doc-oficio">Area: ' + d.area + '</div>'
        + '<div class="doc-assunto">Periodo: ' + d.tempo + '</div>'
        + (d.obs ? '<div class="doc-assunto" style="color:var(--muted);margin-top:4px;">' + d.obs + '</div>' : '')
      + '</div>'
    + '</div>';
  }).join('');
}

// RH Internos
function toggleRHTipo() {
  var tipo = (document.getElementById('rh-int-tipo') || {}).value || 'trocaturno';
  var nf = document.getElementById('rh-int-nome-f');
  var sf = document.getElementById('rh-int-servico-f');
  var df = document.getElementById('rh-int-descricao-f');
  if (nf) nf.style.display = tipo === 'trocaturno' ? '' : 'none';
  if (sf) sf.style.display = tipo === 'trocaturno' ? '' : 'none';
  if (df) df.style.display = tipo === 'outro'       ? '' : 'none';
}
function registarRHInterno() {
  var tipo    = (document.getElementById('rh-int-tipo')       || {}).value || '';
  var data    = (document.getElementById('rh-int-data')       || {}).value || '';
  var nome    = ((document.getElementById('rh-int-nome')      || {}).value || '').trim();
  var servico = ((document.getElementById('rh-int-servico')   || {}).value || '').trim();
  var desc    = ((document.getElementById('rh-int-descricao') || {}).value || '').trim();
  if (!data) { toast('Selecione a data', 'err'); return; }
  if (tipo === 'trocaturno' && !nome) { toast('Preencha o nome', 'err'); return; }
  if (tipo === 'outro' && !desc)      { toast('Preencha a descricao', 'err'); return; }
  var doc = { id: uid(), tipo: tipo, data: data, hora: fmtTime(), nome: nome, servico: servico, descricao: desc };
  var docs = getAreaDocs('rh'); docs.unshift(doc); saveAreaDocs('rh', docs);
  clearRHIntForm(); toast('Documento registado'); renderRHInternos();
}
function clearRHIntForm() {
  ['rh-int-nome','rh-int-servico','rh-int-descricao'].forEach(function(id) { var el=document.getElementById(id); if(el) el.value=''; });
  var t = document.getElementById('rh-int-tipo'); if(t) t.selectedIndex=0; toggleRHTipo();
}
function renderRHInternos() {
  var flt  = (document.getElementById('rh-int-filter') || {}).value || '';
  var docs = getAreaDocs('rh').filter(function(d) { return d.tipo === 'trocaturno' || d.tipo === 'outro'; });
  if (flt) docs = docs.filter(function(d) { return d.data === flt; });
  var c = document.getElementById('rh-int-list');
  if (!docs.length) { c.innerHTML = '<div class="no-data-msg">Nenhum documento interno registado.</div>'; return; }
  c.innerHTML = docs.map(function(d) { return internoCard(d); }).join('');
}
"""

JS_MAIN = r"""
var DOCS_KEY   = 'hp_secretaria_docs';
var CONFIG_KEY = 'hp_secretaria_cfg';
var AREAS = ['Recursos Humanos','Direccao Cientifica e Pedagogica','Direccao Administrativa',
             'Direccao Clinica','Direccao de Enfermagem','Outra Area'];

function getConfig() {
  var raw = localStorage.getItem(CONFIG_KEY);
  return raw ? JSON.parse(raw) : { numAtual: 1, ano: new Date().getFullYear() };
}
function saveConfig(c) { localStorage.setItem(CONFIG_KEY, JSON.stringify(c)); }
function getDocs() { var raw = localStorage.getItem(DOCS_KEY); return raw ? JSON.parse(raw) : []; }
function saveDocs(d) { localStorage.setItem(DOCS_KEY, JSON.stringify(d)); }
function nextNumProcesso() { var c=getConfig(); var n=c.numAtual; c.numAtual=n+1; saveConfig(c); return n; }
function fmtNum(num, ano) { return (ano||new Date().getFullYear())+'/'+String(num).padStart(3,'0'); }
function todayKey() { return new Date().toISOString().slice(0,10); }
function fmtDate(d) {
  if (!d) return '---';
  var p = d.split('-');
  return p[2]+'/'+p[1]+'/'+p[0];
}
function fmtTime() {
  var n=new Date();
  return String(n.getHours()).padStart(2,'0')+':'+String(n.getMinutes()).padStart(2,'0');
}
function uid() { return Date.now().toString(36)+Math.random().toString(36).slice(2,6); }

function toast(msg, type) {
  type = type || 'ok';
  var t = document.getElementById('toast');
  t.textContent = msg; t.className = 'toast-' + type;
  t.style.opacity = '1'; t.style.transform = 'translateY(0)';
  setTimeout(function() { t.style.opacity='0'; t.style.transform='translateY(20px)'; }, 3200);
}

function showSection(id) {
  document.querySelectorAll('.section').forEach(function(s) { s.classList.remove('active'); });
  document.querySelectorAll('.nav-item').forEach(function(n) { n.classList.remove('active'); });
  document.getElementById(id).classList.add('active');
  var nav = document.querySelector('[data-section="'+id+'"]');
  if (nav) nav.classList.add('active');
  if (id === 'sec-despacho')   renderDespacho();
  if (id === 'sec-pesquisa')   renderPesquisa();
  if (id === 'sec-definicoes') renderDefinicoes();
  if (id === 'sec-rh')         renderRH();
}

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
  if (!inst)    { toast('Preencha Instituicao / Nome Singular', 'err'); return; }
  if (!assunto) { toast('Preencha o Assunto', 'err'); return; }
  if (!data)    { toast('Selecione a data de entrada', 'err'); return; }
  var num = nextNumProcesso();
  var ano = new Date().getFullYear();
  var doc = { id: uid(), numProcesso: num, ano: ano, data: data, hora: fmtTime(),
    instituicao: inst, oficio: oficio, tipoDoc: tipo, assunto: assunto,
    nomeAnexo: nomeAnexo, despacho: null, recepcao: null };
  var docs = getDocs(); docs.unshift(doc); saveDocs(docs);
  clearForm();
  document.getElementById('preview-num').textContent = fmtNum(getConfig().numAtual, ano);
  toast('Registado -- Processo ' + fmtNum(num, ano));
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
  var d    = document.getElementById('input-data').value || todayKey();
  var docs = getDocs().filter(function(x) { return x.data === d; });
  var lbl  = document.getElementById('today-count-lbl');
  if (lbl) lbl.textContent = docs.length ? docs.length + ' documento(s)' : '';
  var c = document.getElementById('today-list');
  if (!docs.length) { c.innerHTML = '<div class="no-data-msg">Nenhum documento registado para esta data.</div>'; return; }
  c.innerHTML = docs.map(function(d) { return docCardSimple(d); }).join('');
}

function docCardSimple(d) {
  var numStr = fmtNum(d.numProcesso, d.ano);
  var desp = '';
  if (d.despacho) {
    desp = '<div class="doc-despacho-info"><table class="desp-detail-table">'
      + '<tr><td>Despachado a</td><td>' + fmtDate(d.despacho.data) + '</td></tr>'
      + '<tr><td>Area</td><td>' + d.despacho.area + (d.despacho.outraArea ? ' -- ' + d.despacho.outraArea : '') + '</td></tr>'
      + (d.despacho.pessoa ? '<tr><td>Responsavel</td><td>' + d.despacho.pessoa + '</td></tr>' : '')
      + '</table></div>';
  }
  return '<div class="doc-card ' + (d.despacho ? 'doc-despachado' : 'doc-pendente') + '">'
    + '<div class="doc-card-header">'
      + '<span class="doc-num">' + numStr + '</span>'
      + '<span class="doc-tipo-badge">' + d.tipoDoc + '</span>'
      + '<span class="doc-data">' + fmtDate(d.data) + ' ' + (d.hora||'') + '</span>'
      + (d.despacho ? '<span class="despachado-badge">Despachado</span>' : '<span class="pendente-badge">Pendente</span>')
    + '</div>'
    + '<div class="doc-card-body">'
      + '<div class="doc-inst"><strong>' + d.instituicao + '</strong></div>'
      + (d.oficio ? '<div class="doc-oficio">Oficio: ' + d.oficio + '</div>' : '')
      + '<div class="doc-assunto">' + d.assunto + '</div>'
      + (d.nomeAnexo ? '<div class="doc-anexo">' + d.nomeAnexo + '</div>' : '')
    + '</div>'
    + desp
  + '</div>';
}

function renderDespacho() {
  var flt  = (document.getElementById('desp-filter-data') || {}).value || todayKey();
  var docs = getDocs().filter(function(d) { return d.data === flt; });
  var kpis = document.getElementById('desp-kpis');
  if (kpis) {
    var pend = docs.filter(function(d) { return !d.despacho; }).length;
    var desp = docs.filter(function(d) { return  d.despacho; }).length;
    kpis.innerHTML =
      '<div class="kpi-box kpi-accent" style="min-width:80px;padding:8px 12px;">'
        + '<div class="kpi-label">Total</div><div class="kpi-val">'+docs.length+'</div></div>'
      + '<div class="kpi-box kpi-amber" style="min-width:80px;padding:8px 12px;">'
        + '<div class="kpi-label">Pendentes</div><div class="kpi-val">'+pend+'</div></div>'
      + '<div class="kpi-box kpi-green" style="min-width:80px;padding:8px 12px;">'
        + '<div class="kpi-label">Despachados</div><div class="kpi-val">'+desp+'</div></div>';
  }
  var c = document.getElementById('desp-list');
  if (!docs.length) { c.innerHTML = '<div class="no-data-msg">Nenhum documento para esta data.</div>'; return; }
  var sorted = docs.filter(function(d) { return !d.despacho; }).concat(docs.filter(function(d) { return d.despacho; }));
  c.innerHTML = sorted.map(function(d) { return despachableCard(d); }).join('');
}

function despachableCard(d) {
  var numStr   = fmtNum(d.numProcesso, d.ano);
  var areaOpts = AREAS.map(function(a) { return '<option value="'+a+'">'+a+'</option>'; }).join('');
  var eid      = d.id;
  if (d.despacho) {
    return '<div class="doc-card doc-despachado">'
      + '<div class="doc-card-header">'
        + '<span class="doc-num">'+numStr+'</span>'
        + '<span class="doc-tipo-badge">'+d.tipoDoc+'</span>'
        + '<span class="despachado-badge">Despachado</span>'
        + '<span class="doc-data">'+fmtDate(d.data)+'</span>'
      + '</div>'
      + '<div class="doc-card-body">'
        + '<div class="doc-inst"><strong>'+d.instituicao+'</strong></div>'
        + (d.oficio ? '<div class="doc-oficio">Oficio: '+d.oficio+'</div>' : '')
        + '<div class="doc-assunto">'+d.assunto+'</div>'
      + '</div>'
      + '<div class="doc-despacho-info"><table class="desp-detail-table">'
          + '<tr><td>Data de entrada</td><td>'+fmtDate(d.data)+'</td></tr>'
          + '<tr><td>Data de despacho</td><td>'+fmtDate(d.despacho.data)+'</td></tr>'
          + '<tr><td>Area / Destino</td><td>'+d.despacho.area+(d.despacho.outraArea?' -- '+d.despacho.outraArea:'')+'</td></tr>'
          + (d.despacho.pessoa ? '<tr><td>Responsavel</td><td>'+d.despacho.pessoa+'</td></tr>' : '')
        + '</table>'
        + '<button class="btn btn-outline btn-sm" style="margin-top:8px;" '
          + 'onclick="undoDespacho(\''+eid+'\')">Anular Despacho</button>'
      + '</div>'
    + '</div>';
  }
  return '<div class="doc-card doc-pendente">'
    + '<div class="doc-card-header">'
      + '<span class="doc-num">'+numStr+'</span>'
      + '<span class="doc-tipo-badge">'+d.tipoDoc+'</span>'
      + '<span class="pendente-badge">Pendente</span>'
      + '<span class="doc-data">Entrada: '+fmtDate(d.data)+' '+(d.hora||'')+'</span>'
    + '</div>'
    + '<div class="doc-card-body">'
      + '<div class="doc-inst"><strong>'+d.instituicao+'</strong></div>'
      + (d.oficio ? '<div class="doc-oficio">Oficio: '+d.oficio+'</div>' : '')
      + '<div class="doc-assunto">'+d.assunto+'</div>'
    + '</div>'
    + '<div class="desp-form">'
      + '<div class="desp-form-row">'
        + '<div class="field-group"><label>Data do Despacho</label>'
          + '<input type="date" id="dd-'+eid+'" value="'+todayKey()+'"></div>'
        + '<div class="field-group"><label>Area de Destino</label>'
          + '<select id="da-'+eid+'" onchange="toggleOutra(\''+eid+'\')">'+areaOpts+'</select></div>'
      + '</div>'
      + '<div class="desp-form-row" id="outra-wrap-'+eid+'" style="display:none;">'
        + '<div class="field-group"><label>Especificar Area</label>'
          + '<input type="text" id="da-outra-'+eid+'" placeholder="Nome da area..."></div>'
        + '<div class="field-group"><label>Pessoa (opcional)</label>'
          + '<input type="text" id="dp2-'+eid+'" placeholder="Nome da pessoa..."></div>'
      + '</div>'
      + '<div class="desp-form-row" id="pessoa-wrap-'+eid+'">'
        + '<div class="field-group"><label>Pessoa (opcional)</label>'
          + '<input type="text" id="dp-'+eid+'" placeholder="Nome da pessoa responsavel..."></div>'
      + '</div>'
      + '<button class="btn-despachar" onclick="despacharDoc(\''+eid+'\')">Despachar</button>'
    + '</div>'
  + '</div>';
}

function toggleOutra(id) {
  var area  = (document.getElementById('da-'+id) || {}).value || '';
  var wrap  = document.getElementById('outra-wrap-'+id);
  var pwrap = document.getElementById('pessoa-wrap-'+id);
  if (wrap)  wrap.style.display  = area === 'Outra Area' ? 'grid' : 'none';
  if (pwrap) pwrap.style.display = area === 'Outra Area' ? 'none' : 'grid';
}

function despacharDoc(id) {
  var data  = (document.getElementById('dd-'+id)       || {}).value || '';
  var area  = (document.getElementById('da-'+id)       || {}).value || '';
  var outra = ((document.getElementById('da-outra-'+id)|| {}).value || '').trim();
  var p1    = ((document.getElementById('dp-'+id)      || {}).value || '').trim();
  var p2    = ((document.getElementById('dp2-'+id)     || {}).value || '').trim();
  var pessoa= p1 || p2;
  if (!data) { toast('Selecione a data do despacho', 'err'); return; }
  if (area === 'Outra Area' && !outra) { toast('Especifique o nome da area', 'err'); return; }
  var docs = getDocs();
  var i = docs.findIndex(function(d) { return d.id === id; });
  if (i === -1) return;
  docs[i].despacho = { data: data, area: area, outraArea: outra, pessoa: pessoa };
  saveDocs(docs); toast('Documento despachado com sucesso!'); renderDespacho();
}

function undoDespacho(id) {
  if (!confirm('Anular o despacho deste documento?')) return;
  var docs = getDocs();
  var i = docs.findIndex(function(d) { return d.id === id; });
  if (i === -1) return;
  docs[i].despacho = null; saveDocs(docs); toast('Despacho anulado'); renderDespacho();
}

function renderPesquisa() {
  var q     = ((document.getElementById('pesq-input') || {}).value || '').toLowerCase().trim();
  var fdata = (document.getElementById('pesq-data')   || {}).value || '';
  var all   = getDocs();
  var docs  = all;
  if (fdata) docs = docs.filter(function(d) { return d.data === fdata; });
  if (q) docs = docs.filter(function(d) {
    return d.instituicao.toLowerCase().includes(q)
      || d.assunto.toLowerCase().includes(q)
      || (d.oficio||'').toLowerCase().includes(q)
      || (d.tipoDoc||'').toLowerCase().includes(q)
      || String(d.numProcesso).includes(q)
      || fmtNum(d.numProcesso, d.ano).includes(q);
  });
  var statsEl = document.getElementById('pesq-stats');
  if (statsEl) statsEl.textContent = docs.length === all.length
    ? all.length + ' documentos no total'
    : docs.length + ' resultado(s) de ' + all.length + ' documentos';
  var c = document.getElementById('pesq-results');
  if (!docs.length) { c.innerHTML = '<div class="no-data-msg">Nenhum resultado encontrado.</div>'; return; }
  c.innerHTML = docs.map(function(d) { return docCardFull(d); }).join('');
}

function clearPesquisa() {
  var pi = document.getElementById('pesq-input'); if (pi) pi.value = '';
  var pd = document.getElementById('pesq-data');  if (pd) pd.value = '';
  renderPesquisa();
}

function docCardFull(d) {
  var numStr = fmtNum(d.numProcesso, d.ano);
  var desp = '';
  if (d.despacho) {
    desp = '<div class="doc-despacho-info"><table class="desp-detail-table">'
      + '<tr><td>Data de entrada</td><td>'+fmtDate(d.data)+' '+(d.hora||'')+'</td></tr>'
      + '<tr><td>Data de despacho</td><td>'+fmtDate(d.despacho.data)+'</td></tr>'
      + '<tr><td>Area / Destino</td><td>'+d.despacho.area+(d.despacho.outraArea?' -- '+d.despacho.outraArea:'')+'</td></tr>'
      + (d.despacho.pessoa ? '<tr><td>Responsavel</td><td>'+d.despacho.pessoa+'</td></tr>' : '')
      + (d.recepcao ? '<tr><td>Entrada na Area</td><td>'+fmtDate(d.recepcao.data)+'</td></tr>' : '')
      + '</table></div>';
  }
  return '<div class="doc-card '+(d.despacho?'doc-despachado':'doc-pendente')+'">'
    + '<div class="doc-card-header">'
      + '<span class="doc-num">'+numStr+'</span>'
      + '<span class="doc-tipo-badge">'+d.tipoDoc+'</span>'
      + '<span class="doc-data">'+fmtDate(d.data)+' '+(d.hora||'')+'</span>'
      + (d.despacho?'<span class="despachado-badge">Despachado</span>':'<span class="pendente-badge">Pendente</span>')
      + (d.recepcao?'<span class="recebido-badge">Recebido</span>':'')
    + '</div>'
    + '<div class="doc-card-body">'
      + '<div class="doc-inst"><strong>'+d.instituicao+'</strong></div>'
      + (d.oficio?'<div class="doc-oficio">Oficio: '+d.oficio+'</div>':'')
      + '<div class="doc-assunto">'+d.assunto+'</div>'
      + (d.nomeAnexo?'<div class="doc-anexo">'+d.nomeAnexo+'</div>':'')
    + '</div>'
    + desp
  + '</div>';
}

function renderDefinicoes() {
  var cfg = getConfig();
  var ano = new Date().getFullYear();
  var anoEl = document.getElementById('def-ano'); if (anoEl) anoEl.value = ano;
  var numEl = document.getElementById('def-num-atual'); if (numEl) numEl.value = cfg.numAtual;
  updateDefPreview();
  var docs  = getDocs();
  var pend  = docs.filter(function(d) { return !d.despacho; }).length;
  var desp  = docs.filter(function(d) { return  d.despacho; }).length;
  var today = docs.filter(function(d) { return d.data === todayKey(); }).length;
  var kpis  = document.getElementById('def-kpis');
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
  var prev = document.getElementById('def-preview');
  if (prev) prev.textContent = (!isNaN(n) && n > 0) ? fmtNum(n, new Date().getFullYear()) : '---';
}

function saveDefinicoes() {
  var el = document.getElementById('def-num-atual');
  var n  = el ? parseInt(el.value) : NaN;
  if (isNaN(n) || n < 1) { toast('Numero invalido', 'err'); return; }
  var cfg = getConfig(); cfg.numAtual = n; saveConfig(cfg);
  updateDefPreview();
  var prev = document.getElementById('preview-num');
  if (prev) prev.textContent = fmtNum(n, new Date().getFullYear());
  toast('Definicoes guardadas');
}

function exportarDados() {
  var docs = getDocs(); var cfg = getConfig();
  var data = { config: cfg, documentos: docs, exportadoEm: new Date().toISOString() };
  var blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  var url  = URL.createObjectURL(blob);
  var a    = document.createElement('a');
  a.href = url; a.download = 'secretaria_geral_' + todayKey() + '.json'; a.click();
  URL.revokeObjectURL(url); toast('Dados exportados com sucesso');
}

function loadStaffInfo() {
  var raw = localStorage.getItem('_staff'); var d = raw ? JSON.parse(raw) : {};
  var pi = document.getElementById('inp-profissional'); if (pi) pi.value = d.profissional || '';
  var ci = document.getElementById('inp-chefe');        if (ci) ci.value = d.chefe || '';
}
function saveStaffInfo() {
  var pi = document.getElementById('inp-profissional');
  var ci = document.getElementById('inp-chefe');
  localStorage.setItem('_staff', JSON.stringify({
    profissional: pi ? pi.value.trim() : '', chefe: ci ? ci.value.trim() : ''
  }));
}
setTimeout(loadStaffInfo, 80);

function toggleTheme() {
  var dark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', dark ? 'dark' : 'light');
}

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
    var e = p < 0.5 ? 2*p*p : -1+(4-2*p)*p;
    ring.style.strokeDashoffset = CIRC * (1 - e);
    if (pct) pct.textContent = Math.round(e * 100) + '%';
    if (p < 1) { requestAnimationFrame(step); return; }
    var s = document.getElementById('splash');
    if (s) { s.style.transition='opacity .45s'; s.style.opacity='0'; setTimeout(function(){s.style.display='none';},450); }
  }
  requestAnimationFrame(step);
})();

document.addEventListener('DOMContentLoaded', function() {
  initRegisto();
  var dd = document.getElementById('desp-filter-data'); if (dd) dd.value = todayKey();
  document.getElementById('input-data').addEventListener('change', renderToday);
  initRHMemoNum();
});
"""

def build_html():
    return (
'<!DOCTYPE html>\n'
'<html lang="pt">\n'
'<head>\n'
'<meta charset="UTF-8">\n'
'<meta name="viewport" content="width=device-width,initial-scale=1.0">\n'
'<title>Secretaria Geral - Hospital do Prenda</title>\n'
'<script>if(localStorage.getItem("theme")==="dark")document.documentElement.classList.add("dark");</script>\n'
'<style>' + CSS + '</style>\n'
'</head>\n'
'<body>\n'
'\n'
'<div id="splash">\n'
'  <div class="splash-inner">\n'
'    <div class="splash-img-ring">\n'
'      <div class="splash-img-circle"><img src="__HOSP_IMG__" alt="HP"></div>\n'
'      <svg class="splash-progress-svg" viewBox="0 0 100 100">\n'
'        <circle class="spl-ring-bg" cx="50" cy="50" r="42"/>\n'
'        <circle class="spl-ring-fg" id="spl-ring" cx="50" cy="50" r="42"\n'
'          stroke-dasharray="__CIRC__" stroke-dashoffset="__CIRC__"/>\n'
'      </svg>\n'
'    </div>\n'
'    <p class="splash-hosp-lbl">Hospital do Prenda &middot; Luanda</p>\n'
'    <h1 class="splash-svc-lbl">Secretaria Geral</h1>\n'
'    <div class="splash-pct" id="spl-pct">0%</div>\n'
'  </div>\n'
'</div>\n'
'\n'
'<div class="hp-staff-bar">\n'
'  <span class="hp-staff-lbl">Profissional</span>\n'
'  <input type="text" id="inp-profissional" class="hp-staff-inp" placeholder="Nome do profissional" oninput="saveStaffInfo()">\n'
'  <span class="hp-staff-sep">&middot;</span>\n'
'  <span class="hp-staff-lbl">Chefe de Turno</span>\n'
'  <input type="text" id="inp-chefe" class="hp-staff-inp" placeholder="Nome do chefe de turno" oninput="saveStaffInfo()">\n'
'</div>\n'
'\n'
'<header>\n'
'  <div class="header-logo"><img src="__HOSP_IMG__" alt="HP"></div>\n'
'  <div class="header-title">\n'
'    <h1>Secretaria Geral &mdash; Registo de Correspondencia</h1>\n'
'    <span>Hospital do Prenda &middot; Luanda &middot; Angola</span>\n'
'  </div>\n'
'  <div class="header-right">\n'
'    <button id="theme-toggle" onclick="toggleTheme()">Tema</button>\n'
'  </div>\n'
'</header>\n'
'\n'
'<div class="layout">\n'
'<nav class="sidebar">\n'
'  <div class="nav-section-lbl">Correspondencia</div>\n'
'  <div class="nav-item active" data-section="sec-registo" onclick="showSection(\'sec-registo\')">\n'
'    <svg viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>'
'<path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>\n'
'    Registo Diario\n'
'  </div>\n'
'  <div class="nav-item" data-section="sec-despacho" onclick="showSection(\'sec-despacho\')">\n'
'    <svg viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/>'
'<polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>\n'
'    Despacho\n'
'  </div>\n'
+ SIDEBAR_AREAS +
'  <div class="nav-section-lbl">Consulta</div>\n'
'  <div class="nav-item" data-section="sec-pesquisa" onclick="showSection(\'sec-pesquisa\')">\n'
'    <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/>'
'<line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>\n'
'    Pesquisar\n'
'  </div>\n'
'  <div class="nav-section-lbl">Sistema</div>\n'
'  <div class="nav-item" data-section="sec-definicoes" onclick="showSection(\'sec-definicoes\')">\n'
'    <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/>'
'<path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06'
'a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09'
'A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06'
'A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09'
'A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06'
'A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09'
'a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06'
'A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09'
'a1.65 1.65 0 0 0-1.51 1z"/></svg>\n'
'    Definicoes\n'
'  </div>\n'
'</nav>\n'
'\n'
'<main class="main">\n'
'\n'
'<!-- SEC-REGISTO -->\n'
'<section id="sec-registo" class="section active">\n'
'  <div class="page-header">\n'
'    <div class="page-title">Registo de Correspondencia Recebida</div>\n'
'    <div class="page-sub">Registe documentos recebidos pela Direccao Geral e atribua numero de processo</div>\n'
'  </div>\n'
'  <div class="num-preview">\n'
'    <div>\n'
'      <div class="num-preview-label">Proximo N de Processo</div>\n'
'      <div class="num-preview-val" id="preview-num">---</div>\n'
'      <div class="num-preview-sub" id="preview-sub"></div>\n'
'    </div>\n'
'  </div>\n'
'  <div class="card">\n'
'    <div class="card-title">Novo Registo <span class="ct-badge">* campos obrigatorios</span></div>\n'
'    <div class="form-grid">\n'
'      <div class="field-group span2">\n'
'        <label>Instituicao / Nome Singular *</label>\n'
'        <input type="text" id="input-inst" placeholder="Nome da instituicao ou pessoa singular...">\n'
'      </div>\n'
'      <div class="field-group">\n'
'        <label>N do Oficio (se aplicavel)</label>\n'
'        <input type="text" id="input-oficio" placeholder="Ex: Oficio 123/2025/SG">\n'
'      </div>\n'
'      <div class="field-group">\n'
'        <label>Tipo de Documento *</label>\n'
'        <select id="input-tipo">\n'
'          <option>Carta</option><option>Oficio</option><option>Despacho</option>\n'
'          <option>Nota de Cobranca</option><option>Fatura</option><option>Convite</option>\n'
'          <option>Solicitacao para Estagio Voluntario</option>\n'
'          <option>Solicitacao para Recolha de Dados</option><option>Outro</option>\n'
'        </select>\n'
'      </div>\n'
'      <div class="field-group span2">\n'
'        <label>Assunto *</label>\n'
'        <textarea id="input-assunto" rows="2" placeholder="Breve descricao do assunto..."></textarea>\n'
'      </div>\n'
'      <div class="field-group">\n'
'        <label>Data de Entrada *</label>\n'
'        <input type="date" id="input-data">\n'
'      </div>\n'
'      <div class="field-group">\n'
'        <label>Documento Anexo</label>\n'
'        <input type="file" id="input-anexo" accept=".pdf,.doc,.docx,.jpg,.png,.jpeg,.txt,.xlsx">\n'
'      </div>\n'
'    </div>\n'
'    <div style="margin-top:16px;display:flex;gap:10px;">\n'
'      <button class="btn btn-primary" onclick="handleRegistar()">Registar Documento</button>\n'
'      <button class="btn btn-outline" onclick="clearForm()">Limpar</button>\n'
'    </div>\n'
'  </div>\n'
'  <div class="card">\n'
'    <div class="card-title">Documentos do Dia <span class="ct-badge" id="today-count-lbl"></span></div>\n'
'    <div id="today-list" class="doc-list"><div class="no-data-msg">Nenhum documento registado para hoje.</div></div>\n'
'  </div>\n'
'</section>\n'
'\n'
'<!-- SEC-DESPACHO -->\n'
'<section id="sec-despacho" class="section">\n'
'  <div class="page-header">\n'
'    <div class="page-title">Despacho de Documentos</div>\n'
'    <div class="page-sub">Registe para onde cada documento foi despachado apos a Direccao Geral</div>\n'
'  </div>\n'
'  <div class="card">\n'
'    <div class="filter-bar">\n'
'      <div class="field-group" style="flex:1;min-width:180px;">\n'
'        <label>Filtrar por Data de Entrada</label>\n'
'        <input type="date" id="desp-filter-data" onchange="renderDespacho()">\n'
'      </div>\n'
'      <div id="desp-kpis" style="display:flex;gap:8px;flex-wrap:wrap;align-items:flex-end;"></div>\n'
'    </div>\n'
'    <div id="desp-list" class="doc-list"><div class="no-data-msg">Selecione uma data para ver os documentos.</div></div>\n'
'  </div>\n'
'</section>\n'
'\n'
+ SEC_AREA
+ SEC_RH +
'\n'
'<!-- SEC-PESQUISA -->\n'
'<section id="sec-pesquisa" class="section">\n'
'  <div class="page-header">\n'
'    <div class="page-title">Pesquisar Documentos</div>\n'
'    <div class="page-sub">Pesquise por nome, assunto, oficio, tipo ou numero de processo</div>\n'
'  </div>\n'
'  <div class="card">\n'
'    <div class="search-row">\n'
'      <div class="search-box">\n'
'        <div class="search-icon"><svg viewBox="0 0 24 24">'
'<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></div>\n'
'        <input type="text" id="pesq-input" placeholder="Pesquisar..." oninput="renderPesquisa()">\n'
'      </div>\n'
'      <div class="field-group" style="min-width:170px;">\n'
'        <label>Filtrar por Data</label>\n'
'        <input type="date" id="pesq-data" onchange="renderPesquisa()">\n'
'      </div>\n'
'      <button class="btn btn-outline btn-sm" onclick="clearPesquisa()">Limpar</button>\n'
'    </div>\n'
'    <div class="pesq-stats" id="pesq-stats"></div>\n'
'  </div>\n'
'  <div id="pesq-results" class="doc-list"><div class="no-data-msg">Digite algo para pesquisar ou selecione uma data.</div></div>\n'
'</section>\n'
'\n'
'<!-- SEC-DEFINICOES -->\n'
'<section id="sec-definicoes" class="section">\n'
'  <div class="page-header">\n'
'    <div class="page-title">Definicoes do Sistema</div>\n'
'    <div class="page-sub">Configure a numeracao de processos</div>\n'
'  </div>\n'
'  <div class="def-card"><div class="def-section-title">Estatisticas Gerais</div><div class="kpi-row" id="def-kpis"></div></div>\n'
'  <div class="def-card">\n'
'    <div class="def-section-title">Numeracao de Processos</div>\n'
'    <div class="form-grid">\n'
'      <div class="field-group"><label>Ano Actual</label><input type="text" id="def-ano" readonly></div>\n'
'      <div class="field-group"><label>Proximo Numero a Atribuir</label>'
'<input type="number" id="def-num-atual" min="1" step="1" placeholder="Ex: 589" oninput="updateDefPreview()"></div>\n'
'    </div>\n'
'    <div class="def-preview-box">\n'
'      <div><div class="def-preview-lbl">O proximo processo sera</div>'
'<div class="def-preview-num" id="def-preview">---</div></div>\n'
'    </div>\n'
'    <div class="def-info">No inicio de cada ano, actualize este numero para o valor inicial definido.<br>'
'Exemplo: Em 2025 iniciou em <strong>589</strong>.</div>\n'
'    <div style="margin-top:14px;">'
'<button class="btn btn-primary" onclick="saveDefinicoes()">Guardar Definicoes</button></div>\n'
'  </div>\n'
'  <div class="def-card">\n'
'    <div class="def-section-title">Exportar Dados</div>\n'
'    <div class="def-info" style="margin-bottom:12px;">Exporte todos os registos para ficheiro JSON.</div>\n'
'    <button class="btn btn-outline btn-sm" onclick="exportarDados()">Exportar JSON</button>\n'
'  </div>\n'
'</section>\n'
'\n'
'</main>\n'
'</div>\n'
'\n'
'<div id="toast"></div>\n'
'\n'
'<script>\n'
+ JS_MAIN
+ JS_AREAS +
'</script>\n'
'</body>\n'
'</html>\n'
    )

HTML = build_html()
HTML = HTML.replace('__HOSP_IMG__', HOSP_IMG)
HTML = HTML.replace('__CIRC__', CIRC)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(HTML)

print('Gerado: ' + OUT)
print('Tamanho: ' + str(round(os.path.getsize(OUT)/1024, 1)) + ' KB')
