#!/usr/bin/env python3
"""gerar_ortopedia.py — Serviço de Medicina/Ortopedia"""
import os, re, math

HOSP_IMG = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVQI12NgAAIABQAABjE+ibYAAAAASUVORK5CYII='
for _src in ['procedimentos/secretaria_geral.html','proc_laboratorio.html']:
    try:
        _t = open(_src, encoding='utf-8').read()
        _m = re.search(r'data:image/jpeg;base64,([A-Za-z0-9+/=]+)', _t)
        if _m: HOSP_IMG = 'data:image/jpeg;base64,' + _m.group(1); break
    except: pass

CIRC = str(round(2*math.pi*42, 1))

CSS = """\
:root{--bg:#f0f4f8;--surface:#fff;--surface2:#f8fafc;--border:#e2e8f0;--text:#0f172a;--fg:#0f172a;--muted:#64748b;--accent:#1a56db;--green:#059669;--red:#dc2626;--amber:#d97706;--purple:#7c3aed;--cyan:#0891b2;--fh:'Inter',system-ui,sans-serif;--fm:'JetBrains Mono','Fira Code',monospace;}
html.dark{--bg:#0c0f14;--surface:#111827;--surface2:#141b26;--border:#1e2840;--text:#e2e8f0;--fg:#e2e8f0;--muted:#64748b;}
*{margin:0;padding:0;box-sizing:border-box;}
html,body{height:100%;font-family:var(--fh);background:var(--bg);color:var(--text);font-size:14px;}
.layout{display:flex;min-height:calc(100vh - 80px);}
.sidebar{width:210px;flex-shrink:0;background:var(--surface);border-right:1px solid var(--border);overflow-y:auto;position:sticky;top:80px;height:calc(100vh - 80px);}
html.dark .sidebar{background:#0e1117;border-right-color:#1e2840;}
.main{flex:1;padding:20px;overflow-y:auto;max-width:calc(100vw - 210px);}
header{height:52px;background:var(--surface);border-bottom:1px solid var(--border);display:flex;align-items:center;gap:14px;padding:0 20px;position:sticky;top:0;z-index:100;}
html.dark header{background:#0e1117;border-bottom-color:#1e2840;}
.header-logo{width:32px;height:32px;border-radius:50%;overflow:hidden;flex-shrink:0;}
.header-logo img{width:100%;height:100%;object-fit:cover;}
.header-title h1{font-size:.82rem;font-weight:700;}
.header-title span{font-size:.6rem;color:var(--muted);}
.hp-staff-bar{height:28px;background:linear-gradient(90deg,#1a56db,#1e40af);display:flex;align-items:center;gap:10px;padding:0 16px;font-size:.62rem;color:rgba(255,255,255,.9);position:sticky;top:52px;z-index:99;}
.hp-staff-lbl{opacity:.7;font-weight:500;}.hp-staff-name{font-weight:700;}.hp-staff-sep{opacity:.4;}
.hbtn{background:rgba(255,255,255,.15);border:none;color:#fff;padding:2px 9px;border-radius:5px;font-size:.6rem;cursor:pointer;font-family:var(--fh);}
.hbtn:hover{background:rgba(255,255,255,.25);}
.nav-section-lbl{font-size:.46rem;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:var(--muted);padding:12px 18px 4px;}
.nav-item{display:flex;align-items:center;gap:9px;padding:8px 18px;cursor:pointer;font-size:.71rem;color:var(--muted);font-weight:500;transition:all .12s;border-left:3px solid transparent;}
.nav-item:hover{color:var(--text);background:var(--surface2);}
.nav-item.active{color:var(--accent);background:rgba(26,86,219,.06);border-left-color:var(--accent);font-weight:600;}
.nav-item svg{width:14px;height:14px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;flex-shrink:0;}
.section{display:none;}.section.active{display:block;}
.page-header{margin-bottom:18px;}
.page-title{font-size:1.1rem;font-weight:700;}
.page-sub{font-size:.68rem;color:var(--muted);margin-top:2px;}
.card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:16px;margin-bottom:14px;}
html.dark .card{background:#111827;border-color:#1e2840;}
.card-title{font-size:.78rem;font-weight:700;margin-bottom:12px;}
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
.form-grid-3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;}
@media(max-width:700px){.form-grid,.form-grid-3{grid-template-columns:1fr;}}
.span2{grid-column:span 2;}.span3{grid-column:span 3;}
.field-group{display:flex;flex-direction:column;gap:4px;}
.field-group label{font-size:.62rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;}
input[type=text],input[type=date],input[type=number],input[type=password],input[type=time],select,textarea{background:var(--surface2);border:1px solid var(--border);color:var(--text);font-family:var(--fh);font-size:.77rem;padding:7px 11px;border-radius:7px;outline:none;width:100%;transition:border-color .13s;}
input:focus,select:focus,textarea:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(26,86,219,.1);}
textarea{resize:vertical;min-height:60px;}
html.dark input,html.dark select,html.dark textarea{background:rgba(255,255,255,.04);border-color:rgba(255,255,255,.1);}
.req{color:var(--red);}
.btn{display:inline-flex;align-items:center;gap:6px;padding:7px 14px;border-radius:8px;font-size:.72rem;font-weight:600;cursor:pointer;border:1px solid transparent;transition:all .13s;font-family:var(--fh);}
.btn-primary{background:var(--accent);color:#fff;border-color:var(--accent);}.btn-primary:hover{opacity:.88;}
.btn-outline{background:transparent;border-color:var(--border);color:var(--text);}.btn-outline:hover{border-color:var(--accent);color:var(--accent);}
.btn-sm{padding:4px 10px;font-size:.66rem;}.btn-xs{padding:2px 7px;font-size:.6rem;}
.btn-green{background:#059669;color:#fff;border-color:#059669;}.btn-green:hover{opacity:.88;}
.btn-red{background:#dc2626;color:#fff;border-color:#dc2626;}.btn-red:hover{opacity:.88;}
.badge{font-size:.57rem;font-weight:600;padding:2px 7px;border-radius:10px;white-space:nowrap;}
.b-int{background:rgba(26,86,219,.12);color:#1a56db;}
.b-alta{background:rgba(5,150,105,.12);color:#059669;}
.b-obit{background:rgba(220,38,38,.15);color:#dc2626;}
.b-ti{background:rgba(124,58,237,.12);color:#7c3aed;}
.b-te{background:rgba(8,145,178,.12);color:#0891b2;}
.b-leve{background:rgba(5,150,105,.1);color:#059669;}
.b-mod{background:rgba(245,158,11,.1);color:#d97706;}
.b-grave{background:rgba(220,38,38,.1);color:#dc2626;}
.b-crit{background:rgba(220,38,38,.22);color:#dc2626;font-weight:800;}
html.dark .b-int{background:rgba(26,86,219,.22);}
html.dark .b-alta{background:rgba(5,150,105,.22);}
html.dark .b-obit{background:rgba(220,38,38,.25);}
html.dark .b-ti{background:rgba(124,58,237,.22);}
html.dark .b-te{background:rgba(8,145,178,.22);}
.doc-list{display:flex;flex-direction:column;gap:8px;margin-top:10px;}
.doc-card{background:var(--surface);border:1px solid var(--border);border-radius:10px;overflow:hidden;}
html.dark .doc-card{background:#141820;border-color:#1e2840;}
.doc-card-header{display:flex;align-items:center;gap:7px;padding:8px 12px;background:var(--surface2);border-bottom:1px solid var(--border);flex-wrap:wrap;}
html.dark .doc-card-header{background:rgba(255,255,255,.03);border-bottom-color:#1e2840;}
.doc-card-body{padding:10px 12px;display:flex;flex-direction:column;gap:4px;}
.doc-num{font-family:var(--fm);font-size:.73rem;font-weight:700;color:var(--accent);background:rgba(26,86,219,.1);padding:2px 7px;border-radius:4px;white-space:nowrap;}
.doc-name{font-size:.8rem;font-weight:700;}
.doc-sub{font-size:.68rem;color:var(--muted);}
.doc-data{font-size:.62rem;color:var(--muted);margin-left:auto;}
.kpi-row{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px;}
.kpi-box{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:12px 16px;min-width:120px;flex:1;}
html.dark .kpi-box{background:#111827;border-color:#1e2840;}
.kpi-label{font-size:.56rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.07em;margin-bottom:4px;}
.kpi-val{font-family:var(--fm);font-size:1.4rem;font-weight:700;}
.kpi-sub{font-size:.58rem;color:var(--muted);margin-top:2px;}
.kpi-accent .kpi-val{color:var(--accent);}
.kpi-green .kpi-val{color:var(--green);}
.kpi-red .kpi-val{color:var(--red);}
.kpi-amber .kpi-val{color:var(--amber);}
.kpi-purple .kpi-val{color:var(--purple);}
.kpi-cyan .kpi-val{color:var(--cyan);}
.chart-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:14px;margin-bottom:14px;}
html.dark .chart-card{background:#111827;border-color:#1e2840;}
.chart-title{font-size:.68rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.07em;margin-bottom:10px;}
.chart-wrap{height:200px;position:relative;}
.ind-table{width:100%;border-collapse:collapse;font-size:.74rem;}
.ind-table th{background:var(--surface2);font-size:.6rem;font-weight:700;color:var(--muted);padding:8px 12px;text-align:left;text-transform:uppercase;letter-spacing:.06em;border-bottom:2px solid var(--border);}
.ind-table td{padding:8px 12px;border-bottom:1px solid var(--border);}
.ind-table tr:last-child td{border-bottom:none;}
.ind-val{font-family:var(--fm);font-weight:700;color:var(--accent);font-size:.85rem;}
.ind-formula{font-size:.58rem;color:var(--muted);display:block;margin-top:1px;}
.filter-bar{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:12px;}
.period-bar{display:flex;gap:4px;flex-wrap:wrap;margin-bottom:10px;}
.pb{padding:4px 10px;border-radius:6px;font-size:.65rem;font-weight:600;cursor:pointer;border:1px solid var(--border);background:transparent;color:var(--muted);font-family:var(--fh);}
.pb.active,.pb:hover{background:var(--accent);color:#fff;border-color:var(--accent);}
.search-box{position:relative;flex:1;min-width:200px;}
.search-box input{padding-left:32px;}
.search-icon{position:absolute;left:9px;top:50%;transform:translateY(-50%);width:14px;height:14px;stroke:var(--muted);fill:none;stroke-width:2;stroke-linecap:round;}
.modal-overlay{position:fixed;inset:0;z-index:10000;background:rgba(0,0,0,.78);backdrop-filter:blur(4px);display:flex;align-items:center;justify-content:center;}
.modal{background:var(--surface);border-radius:14px;padding:22px;width:90%;max-width:580px;max-height:90vh;overflow-y:auto;box-shadow:0 25px 60px rgba(0,0,0,.4);}
html.dark .modal{background:#111827;}
.modal-title{font-size:.9rem;font-weight:700;margin-bottom:6px;}
.modal-sub{font-size:.65rem;color:var(--muted);margin-bottom:14px;}
.modal-actions{display:flex;gap:8px;margin-top:16px;justify-content:flex-end;}
#toast{position:fixed;bottom:22px;right:22px;padding:10px 16px;border-radius:8px;font-size:.74rem;font-weight:600;z-index:9998;pointer-events:none;opacity:0;transform:translateY(20px);transition:all .3s;max-width:320px;}
.toast-ok{background:#059669;color:#fff;}.toast-err{background:#dc2626;color:#fff;}.toast-info{background:var(--accent);color:#fff;}
#splash{position:fixed;inset:0;z-index:9999;background:#0c0f14;display:flex;align-items:center;justify-content:center;}
.splash-inner{display:flex;flex-direction:column;align-items:center;gap:16px;}
.splash-img-ring{position:relative;width:100px;height:100px;}
.splash-img-circle{position:absolute;inset:12px;border-radius:50%;overflow:hidden;background:#1e2840;}
.splash-img-circle img{width:100%;height:100%;object-fit:cover;}
.splash-progress-svg{position:absolute;inset:0;width:100%;height:100%;}
.spl-ring-bg{fill:none;stroke:#1e2840;stroke-width:4;}
.spl-ring-fg{fill:none;stroke:#1a56db;stroke-width:4;stroke-linecap:round;transform:rotate(-90deg);transform-origin:50% 50%;}
.splash-pct{font-family:var(--fm);font-size:.65rem;color:#64748b;}
.splash-hosp-lbl{font-size:.65rem;color:#64748b;letter-spacing:.08em;}
.splash-svc-lbl{font-size:1.1rem;font-weight:700;color:#e2e8f0;}
.def-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:16px;margin-bottom:12px;}
html.dark .def-card{background:#111827;border-color:#1e2840;}
.def-section-title{font-size:.72rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-bottom:12px;}
.no-data{text-align:center;padding:24px;color:var(--muted);font-size:.72rem;}
.data-table{width:100%;border-collapse:collapse;font-size:.73rem;}
.data-table th{background:var(--surface2);font-size:.6rem;font-weight:700;color:var(--muted);padding:7px 10px;text-align:left;text-transform:uppercase;letter-spacing:.05em;border-bottom:2px solid var(--border);}
.data-table td{padding:7px 10px;border-bottom:1px solid var(--border);vertical-align:middle;}
.data-table tr:last-child td{border-bottom:none;}
.data-table tr:hover td{background:var(--surface2);}
.ast-tabs{display:flex;gap:4px;flex-wrap:wrap;margin-bottom:12px;padding:5px;background:var(--surface2);border-radius:10px;border:1px solid var(--border);}
.ast-btn{padding:5px 12px;border:none;background:transparent;color:var(--muted);font-size:.68rem;font-weight:600;cursor:pointer;border-radius:7px;font-family:var(--fh);transition:all .12s;}
.ast-btn.active{background:var(--accent);color:#fff;}
.mov-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:14px;}
@media(max-width:700px){.mov-grid{grid-template-columns:1fr 1fr;}}
.mov-box{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:14px;text-align:center;}
html.dark .mov-box{background:#111827;border-color:#1e2840;}
.mov-val{font-family:var(--fm);font-size:1.8rem;font-weight:700;}
.mov-lbl{font-size:.6rem;color:var(--muted);margin-top:3px;}
.prof-item{display:flex;align-items:center;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--border);font-size:.74rem;}
.prof-item:last-child{border-bottom:none;}
@media print{.sidebar,.hp-staff-bar,header,#toast,.no-print{display:none!important;}.layout{display:block;}.main{max-width:100%;padding:0;}.section{display:block!important;}}
"""

MODAL_LOGIN = """
<div id="login-modal" class="modal-overlay">
  <div class="modal" style="max-width:380px;">
    <div class="modal-title">Autenticacao</div>
    <div class="modal-sub">Servico de Medicina / Ortopedia — Hospital do Prenda</div>
    <div class="field-group" style="margin-bottom:10px;">
      <label>Profissional</label>
      <select id="login-prof"></select>
    </div>
    <div class="field-group" style="margin-bottom:10px;">
      <label>Senha</label>
      <input type="password" id="login-senha" placeholder="Senha de acesso..."
             onkeydown="if(event.key==='Enter')doLogin()">
    </div>
    <div id="login-err" style="font-size:.7rem;color:var(--red);display:none;padding:6px 10px;background:rgba(239,68,68,.08);border-radius:6px;margin-bottom:8px;"></div>
    <button class="btn btn-primary" style="width:100%;justify-content:center;" onclick="doLogin()">Entrar</button>
  </div>
</div>
"""

MODAL_SAIDA = """
<div id="modal-saida" class="modal-overlay" style="display:none;">
  <div class="modal" style="max-width:500px;">
    <div class="modal-title">Registar Saida do Doente</div>
    <div class="modal-sub" id="saida-doente-info"></div>
    <div class="form-grid">
      <div class="field-group">
        <label>Tipo de Saida <span class="req">*</span></label>
        <select id="saida-tipo" onchange="toggleSaidaTipo()">
          <option>Alta</option>
          <option>Obito</option>
          <option>Transferencia Interna</option>
          <option>Transferencia Externa</option>
        </select>
      </div>
      <div class="field-group">
        <label>Data de Saida <span class="req">*</span></label>
        <input type="date" id="saida-data">
      </div>
      <div class="field-group">
        <label>Hora de Saida</label>
        <input type="time" id="saida-hora">
      </div>
      <div class="field-group" id="saida-destino-f">
        <label>Destino / Motivo</label>
        <input type="text" id="saida-destino" placeholder="Servico de destino ou motivo da alta...">
      </div>
      <div class="field-group span2">
        <label>Observacoes</label>
        <textarea id="saida-obs" rows="2"></textarea>
      </div>
    </div>
    <div id="saida-err" style="font-size:.7rem;color:var(--red);display:none;margin-top:8px;"></div>
    <div class="modal-actions">
      <button class="btn btn-outline" onclick="document.getElementById('modal-saida').style.display='none'">Cancelar</button>
      <button class="btn btn-primary" onclick="confirmarSaida()">Registar Saida</button>
    </div>
  </div>
</div>
"""

MODAL_FICHA = """
<div id="modal-ficha" class="modal-overlay" style="display:none;">
  <div class="modal" style="max-width:620px;">
    <div id="ficha-content"></div>
    <div class="modal-actions">
      <button class="btn btn-outline" onclick="document.getElementById('modal-ficha').style.display='none'">Fechar</button>
      <button class="btn btn-outline" onclick="exportFichaPDF()">Exportar PDF</button>
      <button class="btn btn-outline no-print" id="ficha-saida-btn" onclick="abrirSaidaDeFicha()">Registar Saida</button>
    </div>
  </div>
</div>
"""

SEC_REGISTO = """
<section id="sec-registo" class="section active">
  <div class="page-header">
    <div class="page-title">Registo de Doente</div>
    <div class="page-sub">Internamento no Servico de Medicina / Ortopedia</div>
  </div>
  <div class="card">
    <div class="card-title">Dados de Internamento</div>
    <div class="form-grid">
      <div class="field-group">
        <label>Nome Completo <span class="req">*</span></label>
        <input type="text" id="r-nome" placeholder="Nome do doente...">
      </div>
      <div class="field-group">
        <label>N Processo / BI <span class="req">*</span></label>
        <input type="text" id="r-bi" placeholder="Numero do processo ou BI...">
      </div>
      <div class="field-group">
        <label>Data de Nascimento <span class="req">*</span></label>
        <input type="date" id="r-dnasc">
      </div>
      <div class="field-group">
        <label>Sexo <span class="req">*</span></label>
        <select id="r-sexo">
          <option value="">Seleccionar...</option>
          <option value="M">Masculino</option>
          <option value="F">Feminino</option>
        </select>
      </div>
      <div class="field-group">
        <label>Data de Admissao <span class="req">*</span></label>
        <input type="date" id="r-dadm">
      </div>
      <div class="field-group">
        <label>Hora de Admissao <span class="req">*</span></label>
        <input type="time" id="r-hadm">
      </div>
      <div class="field-group">
        <label>Tipo de Admissao <span class="req">*</span></label>
        <select id="r-tadm">
          <option value="">Seleccionar...</option>
          <option>Urgencia</option>
          <option>Programada</option>
          <option>Transferencia Interna</option>
          <option>Transferencia Externa</option>
        </select>
      </div>
      <div class="field-group">
        <label>Gravidade <span class="req">*</span></label>
        <select id="r-grav">
          <option value="">Seleccionar...</option>
          <option>Leve</option>
          <option>Moderada</option>
          <option>Grave</option>
          <option>Critica</option>
        </select>
      </div>
      <div class="field-group span2">
        <label>Diagnostico Principal <span class="req">*</span></label>
        <input type="text" id="r-diag" placeholder="Ex: Fractura do femur, Artroplastia do joelho...">
      </div>
      <div class="field-group">
        <label>Codigo CID-10</label>
        <input type="text" id="r-cid" placeholder="Ex: S72.0">
      </div>
      <div class="field-group">
        <label>N Cama <span class="req">*</span></label>
        <input type="text" id="r-cama" placeholder="Ex: 01, 02A...">
      </div>
      <div class="field-group">
        <label>Enfermaria</label>
        <input type="text" id="r-enf" placeholder="Ex: Enfermaria A...">
      </div>
      <div class="field-group">
        <label>Medico Responsavel</label>
        <input type="text" id="r-med" placeholder="Nome do medico...">
      </div>
      <div class="field-group span2">
        <label>Observacoes</label>
        <textarea id="r-obs" rows="2" placeholder="Observacoes adicionais..."></textarea>
      </div>
      <div class="field-group">
        <label>Procedimento Cirurgico</label>
        <select id="r-cirug">
          <option value="nao">Nao</option>
          <option value="sim">Sim</option>
        </select>
      </div>
      <div class="field-group" id="r-cirug-desc-f" style="display:none;">
        <label>Descricao do Procedimento</label>
        <input type="text" id="r-cirug-desc" placeholder="Ex: Osteossintese do femur...">
      </div>
    </div>
    <div style="margin-top:14px;display:flex;gap:8px;align-items:center;">
      <button class="btn btn-primary" onclick="registarDoente()">Registar Internamento</button>
      <button class="btn btn-outline" onclick="limparRegisto()">Limpar</button>
      <span id="r-num-preview" style="font-family:var(--fm);font-size:.75rem;color:var(--accent);margin-left:10px;"></span>
    </div>
  </div>
</section>
"""

SEC_INTERNADOS = """
<section id="sec-internados" class="section">
  <div class="page-header">
    <div class="page-title">Doentes Internados</div>
    <div class="page-sub">Doentes actualmente internados no servico</div>
  </div>
  <div class="card">
    <div class="kpi-row" id="int-kpis"></div>
    <div class="filter-bar">
      <div class="search-box">
        <svg class="search-icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input type="text" id="int-search" placeholder="Pesquisar por nome, diagnostico, cama..." oninput="renderInternados()">
      </div>
      <div class="field-group" style="min-width:130px;">
        <label>Gravidade</label>
        <select id="int-grav-f" onchange="renderInternados()">
          <option value="">Todas</option>
          <option>Leve</option><option>Moderada</option><option>Grave</option><option>Critica</option>
        </select>
      </div>
      <button class="btn btn-outline btn-sm" onclick="exportInternPDF()">PDF</button>
    </div>
    <div id="internados-list" class="doc-list"><div class="no-data">Nenhum doente internado.</div></div>
  </div>
</section>
"""

SEC_SAIDAS = """
<section id="sec-saidas" class="section">
  <div class="page-header">
    <div class="page-title">Controlo de Saidas</div>
    <div class="page-sub">Altas, obitos e transferencias por data</div>
  </div>
  <div class="card">
    <div class="ast-tabs">
      <button class="ast-btn active" data-st="todos" onclick="setSaidaTab('todos')">Todos</button>
      <button class="ast-btn" data-st="alta" onclick="setSaidaTab('alta')">Altas</button>
      <button class="ast-btn" data-st="obito" onclick="setSaidaTab('obito')">Obitos</button>
      <button class="ast-btn" data-st="ti" onclick="setSaidaTab('ti')">Transf. Interna</button>
      <button class="ast-btn" data-st="te" onclick="setSaidaTab('te')">Transf. Externa</button>
    </div>
    <div class="filter-bar">
      <div class="field-group" style="min-width:150px;"><label>Data</label><input type="date" id="saidas-data-f" onchange="renderSaidas()"></div>
      <div class="field-group" style="min-width:150px;"><label>Ate</label><input type="date" id="saidas-data-t" onchange="renderSaidas()"></div>
      <button class="btn btn-outline btn-sm" onclick="document.getElementById('saidas-data-f').value='';document.getElementById('saidas-data-t').value='';renderSaidas()">Limpar</button>
      <button class="btn btn-outline btn-sm" onclick="exportSaidasPDF()">PDF</button>
    </div>
    <div class="kpi-row" id="saidas-kpis"></div>
    <div id="saidas-list" class="doc-list"><div class="no-data">Nenhuma saida registada.</div></div>
  </div>
</section>
"""

SEC_MOVIMENTO = """
<section id="sec-movimento" class="section">
  <div class="page-header">
    <div class="page-title">Movimento Hospitalar</div>
    <div class="page-sub">Boletim de movimento diario do servico</div>
  </div>
  <div class="card no-print">
    <div class="filter-bar">
      <div class="field-group" style="min-width:160px;"><label>Data</label><input type="date" id="mov-data" onchange="renderMovimento()"></div>
      <button class="btn btn-outline btn-sm" onclick="document.getElementById('mov-data').value=todayKey();renderMovimento()">Hoje</button>
      <button class="btn btn-outline btn-sm" onclick="exportMovPDF()">Exportar PDF</button>
    </div>
  </div>
  <div id="mov-content">
    <div class="mov-grid" id="mov-kpis"></div>
    <div class="card">
      <div class="card-title">Detalhe de Saidas</div>
      <div id="mov-saidas-detail"></div>
    </div>
    <div class="card">
      <div class="card-title">Doentes Presentes</div>
      <div id="mov-presentes-list"></div>
    </div>
  </div>
</section>
"""

SEC_INDICADORES = """
<section id="sec-indicadores" class="section">
  <div class="page-header">
    <div class="page-title">Indicadores Hospitalares</div>
    <div class="page-sub">Taxas e indicadores do Servico de Medicina / Ortopedia</div>
  </div>
  <div class="card no-print">
    <div class="period-bar">
      <button class="pb active" data-p="mes" onclick="setIndPeriod('mes')">Mes</button>
      <button class="pb" data-p="semana" onclick="setIndPeriod('semana')">Semana</button>
      <button class="pb" data-p="trimestre" onclick="setIndPeriod('trimestre')">Trimestre</button>
      <button class="pb" data-p="semestre" onclick="setIndPeriod('semestre')">Semestre</button>
      <button class="pb" data-p="ano" onclick="setIndPeriod('ano')">Ano</button>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:flex-end;">
      <div class="field-group" style="min-width:140px;"><label>Inicio</label><input type="date" id="ind-from" onchange="renderIndicadores()"></div>
      <div class="field-group" style="min-width:140px;"><label>Fim</label><input type="date" id="ind-to" onchange="renderIndicadores()"></div>
      <div class="field-group" style="min-width:80px;"><label>N Camas</label><input type="number" id="ind-ncamas" min="1" placeholder="30" onchange="renderIndicadores()"></div>
    </div>
    <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:10px;">
      <span style="font-size:.65rem;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.06em;align-self:center;">PDF:</span>
      <button class="btn btn-outline btn-xs" onclick="exportIndPDF('semana')">Semanal</button>
      <button class="btn btn-outline btn-xs" onclick="exportIndPDF('mes')">Mensal</button>
      <button class="btn btn-outline btn-xs" onclick="exportIndPDF('trimestre')">Trimestral</button>
      <button class="btn btn-outline btn-xs" onclick="exportIndPDF('semestre')">Semestral</button>
      <button class="btn btn-outline btn-xs" onclick="exportIndPDF('ano')">Anual</button>
      <button class="btn btn-outline btn-xs" onclick="exportIndPDF('custom')">Periodo Actual</button>
    </div>
  </div>
  <div class="kpi-row" id="ind-kpis"></div>
  <div class="card">
    <div class="card-title">Tabela de Indicadores</div>
    <div id="ind-table-wrap"></div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
    <div class="chart-card"><div class="chart-title">Entradas vs Saidas</div><div class="chart-wrap"><canvas id="ind-chart-mov"></canvas></div></div>
    <div class="chart-card"><div class="chart-title">Tipo de Saida</div><div class="chart-wrap"><canvas id="ind-chart-tipo"></canvas></div></div>
  </div>
  <div class="chart-card"><div class="chart-title">Evolucao da Taxa de Ocupacao</div><div class="chart-wrap" style="height:180px;"><canvas id="ind-chart-ocup"></canvas></div></div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
    <div class="chart-card"><div class="chart-title">Distribuicao por Gravidade</div><div class="chart-wrap"><canvas id="ind-chart-grav"></canvas></div></div>
    <div class="chart-card"><div class="chart-title">Tipo de Admissao</div><div class="chart-wrap"><canvas id="ind-chart-tadm"></canvas></div></div>
  </div>
</section>
"""

SEC_DIAGNOSTICOS = """
<section id="sec-diagnosticos" class="section">
  <div class="page-header">
    <div class="page-title">Diagnosticos</div>
    <div class="page-sub">Analise por diagnostico e patologia</div>
  </div>
  <div class="card">
    <div class="filter-bar">
      <div class="field-group" style="min-width:140px;"><label>Estado</label>
        <select id="diag-estado-f" onchange="renderDiagnosticos()">
          <option value="">Todos</option>
          <option value="internado">Internados</option>
          <option value="saido">Com Saida</option>
        </select>
      </div>
      <div class="search-box">
        <svg class="search-icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input type="text" id="diag-search" placeholder="Filtrar por diagnostico..." oninput="renderDiagnosticos()">
      </div>
    </div>
    <div id="diag-kpis" class="kpi-row"></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px;">
      <div class="chart-card"><div class="chart-title">Top 10 Diagnosticos</div><div class="chart-wrap"><canvas id="diag-chart-top"></canvas></div></div>
      <div class="chart-card"><div class="chart-title">Gravidade por Diagnostico</div><div class="chart-wrap"><canvas id="diag-chart-grav"></canvas></div></div>
    </div>
    <div id="diag-table"></div>
  </div>
</section>
"""

SEC_PESQUISA = """
<section id="sec-pesquisa" class="section">
  <div class="page-header">
    <div class="page-title">Pesquisa de Doentes</div>
    <div class="page-sub">Pesquise por nome, diagnostico, numero de processo ou cama</div>
  </div>
  <div class="card">
    <div class="filter-bar" style="margin-bottom:14px;">
      <div class="search-box">
        <svg class="search-icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input type="text" id="pesq-input" placeholder="Nome, diagnostico, N processo, cama..." oninput="renderPesquisa()">
      </div>
      <div class="field-group" style="min-width:130px;"><label>Estado</label>
        <select id="pesq-estado" onchange="renderPesquisa()">
          <option value="">Todos</option>
          <option value="internado">Internados</option>
          <option value="alta">Alta</option>
          <option value="obito">Obito</option>
          <option value="transferencia">Transferencia</option>
        </select>
      </div>
      <div class="field-group" style="min-width:130px;"><label>Gravidade</label>
        <select id="pesq-grav" onchange="renderPesquisa()">
          <option value="">Todas</option>
          <option>Leve</option><option>Moderada</option><option>Grave</option><option>Critica</option>
        </select>
      </div>
    </div>
    <div id="pesq-stats" style="font-size:.65rem;color:var(--muted);margin-bottom:8px;"></div>
    <div id="pesq-results" class="doc-list"><div class="no-data">Digite algo para pesquisar.</div></div>
  </div>
</section>
"""

SEC_DEFINICOES = """
<section id="sec-definicoes" class="section">
  <div class="page-header">
    <div class="page-title">Definicoes</div>
    <div class="page-sub">Configuracoes do sistema — acesso restrito</div>
  </div>
  <div id="def-lock" class="card" style="max-width:400px;">
    <div class="card-title">Autenticacao Necessaria</div>
    <p style="font-size:.72rem;color:var(--muted);margin-bottom:14px;">As definicoes requerem a senha de chefe.</p>
    <div class="field-group" style="margin-bottom:12px;">
      <label>Senha de Acesso</label>
      <input type="password" id="def-senha-input" placeholder="Senha..." onkeydown="if(event.key==='Enter')unlockDef()">
    </div>
    <div id="def-lock-err" style="font-size:.7rem;color:var(--red);display:none;margin-bottom:10px;"></div>
    <button class="btn btn-primary btn-sm" onclick="unlockDef()">Aceder</button>
  </div>
  <div id="def-content" style="display:none;">
    <div class="def-card">
      <div class="def-section-title">Servico</div>
      <div class="form-grid">
        <div class="field-group"><label>Nome do Servico</label><input type="text" id="def-servico" placeholder="Medicina/Ortopedia"></div>
        <div class="field-group"><label>N de Camas do Servico</label><input type="number" id="def-ncamas" min="1" placeholder="30"></div>
      </div>
      <div style="margin-top:10px;"><button class="btn btn-primary btn-sm" onclick="saveDefinicoes()">Guardar</button></div>
    </div>
    <div class="def-card">
      <div class="def-section-title">Numeracao de Processos</div>
      <div class="form-grid">
        <div class="field-group"><label>Proximo Numero</label><input type="number" id="def-num" min="1" oninput="updateDefPreview()"></div>
        <div class="field-group"><label>Ano</label><input type="text" id="def-ano" readonly></div>
      </div>
      <div id="def-preview" style="margin-top:8px;font-family:var(--fm);font-size:1.1rem;font-weight:700;color:var(--accent);">---</div>
      <div style="margin-top:10px;"><button class="btn btn-primary btn-sm" onclick="saveNumeracao()">Guardar Numeracao</button></div>
    </div>
    <div class="def-card">
      <div class="def-section-title">Senha de Acesso as Definicoes</div>
      <div class="form-grid">
        <div class="field-group"><label>Nova Senha</label><input type="password" id="def-new-senha"></div>
        <div class="field-group"><label>Confirmar</label><input type="password" id="def-conf-senha"></div>
      </div>
      <div style="margin-top:10px;"><button class="btn btn-outline btn-sm" onclick="saveSenhaChefe()">Actualizar Senha</button></div>
    </div>
    <div class="def-card">
      <div class="def-section-title">Profissionais</div>
      <div id="prof-list" style="margin-bottom:14px;"></div>
      <div class="form-grid" style="max-width:520px;">
        <div class="field-group"><label>Nome</label><input type="text" id="new-prof-nome"></div>
        <div class="field-group"><label>Senha</label><input type="password" id="new-prof-senha"></div>
      </div>
      <div style="margin-top:10px;"><button class="btn btn-primary btn-sm" onclick="addProfissional()">Adicionar</button></div>
    </div>
    <div class="def-card">
      <div class="def-section-title">Dados</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;">
        <button class="btn btn-outline btn-sm" onclick="exportarJSON()">Exportar JSON</button>
        <button class="btn btn-primary btn-sm" onclick="downloadBackup()">Backup Completo</button>
      </div>
      <div id="def-backup-status" style="margin-top:10px;"></div>
    </div>
  </div>
</section>
"""

JS = r"""
// ═══ CONSTANTS ═══
var DOCS_KEY='hp_orto_docs', CFG_KEY='hp_orto_cfg', NOTIF_KEY='hp_orto_notifs';
var currentProfissional='', indPeriod='mes', saidaTabFilter='todos', saidaTargetId=null, fichaCurId=null;
var ortoCharts={};

// ═══ UTILS ═══
function uid(){return Date.now().toString(36)+Math.random().toString(36).slice(2,7);}
function todayKey(){return new Date().toISOString().slice(0,10);}
function fmtDate(d){if(!d)return '---';var p=d.split('-');return p[2]+'/'+p[1]+'/'+p[0];}
function fmtTime(){var n=new Date();return String(n.getHours()).padStart(2,'0')+':'+String(n.getMinutes()).padStart(2,'0');}
function fmtNum(n,y){return 'ORT/'+(y||new Date().getFullYear())+'/'+String(n).padStart(3,'0');}
function daysBetween(d1,d2){var a=new Date(d1),b=new Date(d2);return Math.max(0,Math.round((b-a)/86400000));}
function calcIdade(dnasc){if(!dnasc)return '?';return Math.floor((new Date()-new Date(dnasc))/31557600000);}
function gravBadge(g){var m={'Leve':'b-leve','Moderada':'b-mod','Grave':'b-grave','Critica':'b-crit'};return '<span class="badge '+(m[g]||'')+'">'+g+'</span>';}
function statusBadge(s){
  if(s==='internado')return '<span class="badge b-int">Internado</span>';
  if(s==='alta')return '<span class="badge b-alta">Alta</span>';
  if(s==='obito')return '<span class="badge b-obit">Obito</span>';
  if(s==='transferencia_interna')return '<span class="badge b-ti">Transf. Interna</span>';
  if(s==='transferencia_externa')return '<span class="badge b-te">Transf. Externa</span>';
  return '<span class="badge">'+s+'</span>';
}
function statusKey(tipo){
  if(!tipo)return 'internado';
  if(tipo==='Alta')return 'alta';
  if(tipo==='Obito')return 'obito';
  if(tipo==='Transferencia Interna')return 'transferencia_interna';
  if(tipo==='Transferencia Externa')return 'transferencia_externa';
  return 'internado';
}
function toast(msg,type){type=type||'ok';var t=document.getElementById('toast');t.textContent=msg;t.className='toast-'+(type==='err'?'err':type==='info'?'info':'ok');t.style.opacity='1';t.style.transform='translateY(0)';setTimeout(function(){t.style.opacity='0';t.style.transform='translateY(20px)';},3500);}

// ═══ DATA ═══
function getConfig(){
  var def={numAtual:1,ano:new Date().getFullYear(),numCamas:30,servico:'Medicina/Ortopedia',profissionais:[{id:'admin',nome:'Secretaria',senha:'1234'}],senhaChefe:'1234'};
  var r=localStorage.getItem(CFG_KEY);if(!r)return def;
  try{var c=JSON.parse(r);if(!c.profissionais||!c.profissionais.length)c.profissionais=def.profissionais;if(!c.senhaChefe)c.senhaChefe=def.senhaChefe;if(!c.numCamas)c.numCamas=def.numCamas;return c;}catch(e){return def;}
}
function saveConfig(c){localStorage.setItem(CFG_KEY,JSON.stringify(c));}
function getDoentes(){var r=localStorage.getItem(DOCS_KEY);return r?JSON.parse(r):[];}
function saveDoentes(d){localStorage.setItem(DOCS_KEY,JSON.stringify(d));}
function nextNum(){var c=getConfig();var n=c.numAtual;c.numAtual=n+1;saveConfig(c);return n;}

// ═══ AUTH ═══
function initLoginModal(){
  var cfg=getConfig();var sel=document.getElementById('login-prof');if(!sel)return;
  sel.innerHTML=cfg.profissionais.map(function(p){return '<option value="'+p.id+'">'+p.nome+'</option>';}).join('');
}
function doLogin(){
  var cfg=getConfig();
  var pid=(document.getElementById('login-prof')||{}).value;
  var senha=(document.getElementById('login-senha')||{}).value||'';
  var errEl=document.getElementById('login-err');
  var prof=cfg.profissionais.find(function(p){return p.id===pid;});
  if(!prof||prof.senha!==senha){errEl.style.display='block';errEl.textContent='Senha incorrecta. Tente novamente.';document.getElementById('login-senha').value='';document.getElementById('login-senha').focus();return;}
  currentProfissional=prof.nome;sessionStorage.setItem('hp_orto_prof',prof.nome);
  document.getElementById('login-modal').style.display='none';
  document.getElementById('staff-prof-name').textContent=prof.nome;
  toast('Bem-vindo(a), '+prof.nome+'!','info');
  updateNumPreview();
}
function doLogout(){sessionStorage.removeItem('hp_orto_prof');currentProfissional='';location.reload();}
function checkSession(){
  var p=sessionStorage.getItem('hp_orto_prof');
  if(p){currentProfissional=p;document.getElementById('staff-prof-name').textContent=p;document.getElementById('login-modal').style.display='none';updateNumPreview();}
  else{initLoginModal();}
}

// ═══ NAVIGATION ═══
function showSection(id){
  document.querySelectorAll('.section').forEach(function(s){s.classList.remove('active');});
  document.querySelectorAll('.nav-item').forEach(function(n){n.classList.remove('active');});
  var sec=document.getElementById(id);if(sec)sec.classList.add('active');
  var nav=document.querySelector('[data-section="'+id+'"]');if(nav)nav.classList.add('active');
  if(id==='sec-internados'){renderInternados();}
  if(id==='sec-saidas'){renderSaidas();}
  if(id==='sec-movimento'){renderMovimento();}
  if(id==='sec-indicadores'){renderIndicadores();}
  if(id==='sec-diagnosticos'){renderDiagnosticos();}
  if(id==='sec-pesquisa'){renderPesquisa();}
  if(id==='sec-definicoes'){renderDefinicoes();}
}

// ═══ REGISTO ═══
function updateNumPreview(){
  var cfg=getConfig();var el=document.getElementById('r-num-preview');
  if(el)el.textContent='Proximo: '+fmtNum(cfg.numAtual,cfg.ano);
}
function registarDoente(){
  if(!currentProfissional){toast('Faca login primeiro','err');return;}
  var nome=((document.getElementById('r-nome')||{}).value||'').trim();
  var bi=((document.getElementById('r-bi')||{}).value||'').trim();
  var dnasc=(document.getElementById('r-dnasc')||{}).value||'';
  var sexo=(document.getElementById('r-sexo')||{}).value||'';
  var dadm=(document.getElementById('r-dadm')||{}).value||'';
  var hadm=(document.getElementById('r-hadm')||{}).value||'';
  var tadm=(document.getElementById('r-tadm')||{}).value||'';
  var grav=(document.getElementById('r-grav')||{}).value||'';
  var diag=((document.getElementById('r-diag')||{}).value||'').trim();
  var cama=((document.getElementById('r-cama')||{}).value||'').trim();
  if(!nome||!bi||!dnasc||!sexo||!dadm||!hadm||!tadm||!grav||!diag||!cama){
    toast('Preencha todos os campos obrigatorios (*)','err');return;
  }
  var cfg=getConfig();var num=nextNum();var ano=cfg.ano;
  var doente={
    id:uid(),numProcesso:num,ano:ano,numStr:fmtNum(num,ano),
    nome:nome,bi:bi,dataNascimento:dnasc,idade:calcIdade(dnasc),sexo:sexo,
    dataAdmissao:dadm,horaAdmissao:hadm,tipoAdmissao:tadm,gravidade:grav,
    diagnostico:diag,cid:((document.getElementById('r-cid')||{}).value||'').trim(),
    cama:cama,enfermaria:((document.getElementById('r-enf')||{}).value||'').trim(),
    medico:((document.getElementById('r-med')||{}).value||'').trim(),
    cirurgia:(document.getElementById('r-cirug')||{}).value==='sim',
    cirurgiaDesc:((document.getElementById('r-cirug-desc')||{}).value||'').trim(),
    obs:((document.getElementById('r-obs')||{}).value||'').trim(),
    status:'internado',saida:null,
    profissional:currentProfissional,registadoEm:new Date().toISOString(),
    historico:[{ts:new Date().toISOString(),profissional:currentProfissional,acao:'Internamento registado'}]
  };
  var docs=getDoentes();docs.unshift(doente);saveDoentes(docs);
  limparRegisto();updateNumPreview();
  toast('Internamento registado — '+doente.numStr);
}
function limparRegisto(){
  ['r-nome','r-bi','r-cid','r-cama','r-enf','r-med','r-obs','r-cirug-desc'].forEach(function(id){var el=document.getElementById(id);if(el)el.value='';});
  ['r-dnasc','r-dadm'].forEach(function(id){var el=document.getElementById(id);if(el)el.value='';});
  ['r-sexo','r-tadm','r-grav'].forEach(function(id){var el=document.getElementById(id);if(el)el.value='';});
  var hadm=document.getElementById('r-hadm');if(hadm)hadm.value=fmtTime();
  var dadm=document.getElementById('r-dadm');if(dadm)dadm.value=todayKey();
  document.getElementById('r-cirug-desc-f').style.display='none';
}
function toggleCirug(){
  var v=(document.getElementById('r-cirug')||{}).value;
  var f=document.getElementById('r-cirug-desc-f');if(f)f.style.display=v==='sim'?'':'none';
}

// ═══ INTERNADOS ═══
function renderInternados(){
  var q=((document.getElementById('int-search')||{}).value||'').toLowerCase();
  var gf=(document.getElementById('int-grav-f')||{}).value||'';
  var docs=getDoentes().filter(function(d){return d.status==='internado';});
  if(gf)docs=docs.filter(function(d){return d.gravidade===gf;});
  if(q)docs=docs.filter(function(d){
    return (d.nome||'').toLowerCase().includes(q)||(d.diagnostico||'').toLowerCase().includes(q)||
           (d.cama||'').toLowerCase().includes(q)||(d.numStr||'').toLowerCase().includes(q);
  });
  var kEl=document.getElementById('int-kpis');
  if(kEl){
    var all=getDoentes().filter(function(d){return d.status==='internado';});
    var crit=all.filter(function(d){return d.gravidade==='Critica';}).length;
    var grave=all.filter(function(d){return d.gravidade==='Grave';}).length;
    kEl.innerHTML='<div class="kpi-box kpi-accent"><div class="kpi-label">Total Internados</div><div class="kpi-val">'+all.length+'</div></div>'
      +'<div class="kpi-box kpi-red"><div class="kpi-label">Criticos</div><div class="kpi-val">'+crit+'</div></div>'
      +'<div class="kpi-box kpi-amber"><div class="kpi-label">Graves</div><div class="kpi-val">'+grave+'</div></div>';
  }
  var c=document.getElementById('internados-list');if(!c)return;
  if(!docs.length){c.innerHTML='<div class="no-data">Nenhum doente encontrado.</div>';return;}
  c.innerHTML=docs.map(function(d){
    var dias=daysBetween(d.dataAdmissao,todayKey());
    return '<div class="doc-card" style="border-left:4px solid '+(d.gravidade==='Critica'?'#dc2626':d.gravidade==='Grave'?'#d97706':'#1a56db')+';">'
      +'<div class="doc-card-header">'
      +'<span class="doc-num">'+d.numStr+'</span>'
      +gravBadge(d.gravidade)
      +'<span class="badge b-int">Internado</span>'
      +'<span class="doc-data">Adm: '+fmtDate(d.dataAdmissao)+'</span>'
      +'</div>'
      +'<div class="doc-card-body">'
      +'<div class="doc-name">'+d.nome+' &nbsp;<span style="font-size:.68rem;font-weight:400;color:var(--muted);">'+d.sexo+' · '+d.idade+' anos</span></div>'
      +'<div class="doc-sub">'+d.diagnostico+(d.cid?' ('+d.cid+')':'')+'</div>'
      +'<div class="doc-sub">Cama: <strong>'+d.cama+'</strong>'+(d.enfermaria?' · Enf: '+d.enfermaria:'')+(d.medico?' · Dr: '+d.medico:'')+'</div>'
      +'<div class="doc-sub">Internado ha <strong>'+dias+'</strong> dia(s) · Tipo: '+d.tipoAdmissao+'</div>'
      +'<div style="margin-top:8px;display:flex;gap:6px;">'
      +'<button class="btn btn-outline btn-xs" onclick="openFicha(\''+d.id+'\')">Ficha</button>'
      +'<button class="btn btn-green btn-xs" onclick="abrirSaida(\''+d.id+'\')">Registar Saida</button>'
      +'</div>'
      +'</div></div>';
  }).join('');
}

// ═══ SAIDA ═══
function abrirSaida(id){
  saidaTargetId=id;var docs=getDoentes();var d=docs.find(function(x){return x.id===id;});
  if(!d||d.status!=='internado'){toast('Doente ja teve saida registada','err');return;}
  var info=document.getElementById('saida-doente-info');
  if(info)info.textContent=d.nome+' — '+d.numStr+' — '+d.diagnostico;
  var sd=document.getElementById('saida-data');if(sd)sd.value=todayKey();
  var sh=document.getElementById('saida-hora');if(sh)sh.value=fmtTime();
  var err=document.getElementById('saida-err');if(err)err.style.display='none';
  document.getElementById('saida-destino-f').style.display='';
  document.getElementById('modal-saida').style.display='flex';
}
function toggleSaidaTipo(){
  var t=(document.getElementById('saida-tipo')||{}).value||'';
  var df=document.getElementById('saida-destino-f');
  if(df){
    var lbl=df.querySelector('label');
    if(t==='Alta')lbl.textContent='Motivo / Condicao de Alta';
    else if(t.indexOf('Transf')!==-1)lbl.textContent='Servico de Destino';
    else if(t==='Obito')lbl.textContent='Causa do Obito';
    else lbl.textContent='Destino / Motivo';
  }
}
function confirmarSaida(){
  if(!currentProfissional){toast('Faca login primeiro','err');return;}
  var tipo=(document.getElementById('saida-tipo')||{}).value||'';
  var data=(document.getElementById('saida-data')||{}).value||'';
  var hora=(document.getElementById('saida-hora')||{}).value||'';
  var destino=((document.getElementById('saida-destino')||{}).value||'').trim();
  var obs=((document.getElementById('saida-obs')||{}).value||'').trim();
  var err=document.getElementById('saida-err');
  if(!data){if(err){err.style.display='block';err.textContent='Preencha a data de saida.';}return;}
  var docs=getDoentes();var idx=docs.findIndex(function(d){return d.id===saidaTargetId;});
  if(idx===-1)return;
  var d=docs[idx];
  var diasIntern=daysBetween(d.dataAdmissao,data);
  docs[idx].saida={tipo:tipo,data:data,hora:hora,destino:destino,obs:obs,diasInternamento:diasIntern};
  docs[idx].status=statusKey(tipo);
  docs[idx].historico=(docs[idx].historico||[]).concat([{ts:new Date().toISOString(),profissional:currentProfissional,acao:'Saida registada: '+tipo+' em '+fmtDate(data)}]);
  saveDoentes(docs);
  document.getElementById('modal-saida').style.display='none';
  document.getElementById('saida-obs').value='';
  toast('Saida registada: '+tipo+' — '+d.nome);
}
function setSaidaTab(t){
  saidaTabFilter=t;
  document.querySelectorAll('[data-st]').forEach(function(b){b.classList.toggle('active',b.getAttribute('data-st')===t);});
  renderSaidas();
}
function renderSaidas(){
  var f=(document.getElementById('saidas-data-f')||{}).value||'';
  var t=(document.getElementById('saidas-data-t')||{}).value||'';
  var docs=getDoentes().filter(function(d){return d.saida;});
  if(f)docs=docs.filter(function(d){return d.saida.data>=f;});
  if(t)docs=docs.filter(function(d){return d.saida.data<=t;});
  if(saidaTabFilter==='alta')docs=docs.filter(function(d){return d.saida.tipo==='Alta';});
  else if(saidaTabFilter==='obito')docs=docs.filter(function(d){return d.saida.tipo==='Obito';});
  else if(saidaTabFilter==='ti')docs=docs.filter(function(d){return d.saida.tipo==='Transferencia Interna';});
  else if(saidaTabFilter==='te')docs=docs.filter(function(d){return d.saida.tipo==='Transferencia Externa';});
  var kEl=document.getElementById('saidas-kpis');
  if(kEl){
    var all=getDoentes().filter(function(d){return d.saida;});
    var tot=docs.length;
    var alt=docs.filter(function(d){return d.saida.tipo==='Alta';}).length;
    var obi=docs.filter(function(d){return d.saida.tipo==='Obito';}).length;
    var tr=docs.filter(function(d){return d.saida.tipo.indexOf('Transf')!==-1;}).length;
    kEl.innerHTML='<div class="kpi-box kpi-accent"><div class="kpi-label">Total</div><div class="kpi-val">'+tot+'</div></div>'
      +'<div class="kpi-box kpi-green"><div class="kpi-label">Altas</div><div class="kpi-val">'+alt+'</div></div>'
      +'<div class="kpi-box kpi-red"><div class="kpi-label">Obitos</div><div class="kpi-val">'+obi+'</div></div>'
      +'<div class="kpi-box kpi-purple"><div class="kpi-label">Transferencias</div><div class="kpi-val">'+tr+'</div></div>';
  }
  var c=document.getElementById('saidas-list');if(!c)return;
  if(!docs.length){c.innerHTML='<div class="no-data">Nenhuma saida encontrada.</div>';return;}
  docs.sort(function(a,b){return b.saida.data.localeCompare(a.saida.data);});
  c.innerHTML=docs.map(function(d){
    return '<div class="doc-card">'
      +'<div class="doc-card-header">'
      +'<span class="doc-num">'+d.numStr+'</span>'
      +statusBadge(d.status)
      +gravBadge(d.gravidade)
      +'<span class="doc-data">Saida: '+fmtDate(d.saida.data)+' '+d.saida.hora+'</span>'
      +'</div>'
      +'<div class="doc-card-body">'
      +'<div class="doc-name">'+d.nome+'</div>'
      +'<div class="doc-sub">'+d.diagnostico+'</div>'
      +'<div class="doc-sub">Internamento: '+fmtDate(d.dataAdmissao)+' → '+fmtDate(d.saida.data)+' ('+d.saida.diasInternamento+' dias)</div>'
      +(d.saida.destino?'<div class="doc-sub">Destino/Obs: '+d.saida.destino+'</div>':'')
      +'<div style="margin-top:6px;"><button class="btn btn-outline btn-xs" onclick="openFicha(\''+d.id+'\')">Ficha</button></div>'
      +'</div></div>';
  }).join('');
}

// ═══ MOVIMENTO ═══
function renderMovimento(){
  var data=(document.getElementById('mov-data')||{}).value||todayKey();
  var prev=new Date(data);prev.setDate(prev.getDate()-1);
  var prevKey=prev.toISOString().slice(0,10);
  var all=getDoentes();
  // Existentes início = admitted on or before previous day AND (no saida OR saida on data or later)
  var existIni=all.filter(function(d){return d.dataAdmissao<=prevKey&&(!d.saida||d.saida.data>=data);});
  var entradas=all.filter(function(d){return d.dataAdmissao===data;});
  var saidasDia=all.filter(function(d){return d.saida&&d.saida.data===data;});
  var altas=saidasDia.filter(function(d){return d.saida.tipo==='Alta';});
  var obitos=saidasDia.filter(function(d){return d.saida.tipo==='Obito';});
  var ti=saidasDia.filter(function(d){return d.saida.tipo==='Transferencia Interna';});
  var te=saidasDia.filter(function(d){return d.saida.tipo==='Transferencia Externa';});
  var existFim=existIni.length+entradas.length-saidasDia.length;
  var doenteDia=existIni.length+entradas.length;
  var cfg=getConfig();var numCamas=cfg.numCamas||30;
  var taxaOcup=numCamas>0?(doenteDia/numCamas*100):0;
  var kEl=document.getElementById('mov-kpis');
  if(kEl){
    kEl.innerHTML=''
      +'<div class="mov-box"><div class="mov-val" style="color:var(--accent);">'+existIni.length+'</div><div class="mov-lbl">Existentes Inicio</div></div>'
      +'<div class="mov-box"><div class="mov-val" style="color:var(--green);">'+entradas.length+'</div><div class="mov-lbl">Entradas</div></div>'
      +'<div class="mov-box"><div class="mov-val" style="color:var(--amber);">'+saidasDia.length+'</div><div class="mov-lbl">Saidas Totais</div></div>'
      +'<div class="mov-box"><div class="mov-val" style="color:var(--accent);">'+existFim+'</div><div class="mov-lbl">Existentes Fim</div></div>'
      +'<div class="mov-box"><div class="mov-val" style="color:var(--green);">'+altas.length+'</div><div class="mov-lbl">Altas</div></div>'
      +'<div class="mov-box"><div class="mov-val" style="color:var(--red);">'+obitos.length+'</div><div class="mov-lbl">Obitos</div></div>'
      +'<div class="mov-box"><div class="mov-val" style="color:var(--purple);">'+ti.length+'</div><div class="mov-lbl">Transf. Interna</div></div>'
      +'<div class="mov-box"><div class="mov-val" style="color:var(--cyan);">'+te.length+'</div><div class="mov-lbl">Transf. Externa</div></div>'
      +'<div class="mov-box"><div class="mov-val">'+doenteDia+'</div><div class="mov-lbl">Dias de Doente</div></div>'
      +'<div class="mov-box"><div class="mov-val" style="color:var(--accent);">'+numCamas+'</div><div class="mov-lbl">Camas Activas</div></div>'
      +'<div class="mov-box"><div class="mov-val" style="color:'+(taxaOcup>90?'var(--red)':taxaOcup>75?'var(--amber)':'var(--green)')+';">'+taxaOcup.toFixed(1)+'%</div><div class="mov-lbl">Taxa de Ocupacao</div></div>';
  }
  var sd=document.getElementById('mov-saidas-detail');
  if(sd){
    if(!saidasDia.length){sd.innerHTML='<div class="no-data">Sem saidas neste dia.</div>';}
    else{sd.innerHTML='<table class="data-table"><thead><tr><th>Processo</th><th>Nome</th><th>Tipo Saida</th><th>Diagnostico</th><th>Dias</th></tr></thead><tbody>'
      +saidasDia.map(function(d){return '<tr><td><span class="doc-num">'+d.numStr+'</span></td><td>'+d.nome+'</td><td>'+statusBadge(d.status)+'</td><td>'+d.diagnostico+'</td><td>'+d.saida.diasInternamento+'</td></tr>';}).join('')
      +'</tbody></table>';}
  }
  var pl=document.getElementById('mov-presentes-list');
  var presentes=all.filter(function(d){return d.dataAdmissao<=data&&(!d.saida||d.saida.data>data);});
  if(pl){
    if(!presentes.length){pl.innerHTML='<div class="no-data">Sem doentes presentes.</div>';}
    else{pl.innerHTML='<table class="data-table"><thead><tr><th>Processo</th><th>Nome</th><th>Cama</th><th>Diagnostico</th><th>Gravidade</th><th>Dias</th></tr></thead><tbody>'
      +presentes.map(function(d){var dias=daysBetween(d.dataAdmissao,data);return '<tr><td><span class="doc-num">'+d.numStr+'</span></td><td>'+d.nome+'</td><td>'+d.cama+'</td><td>'+d.diagnostico+'</td><td>'+gravBadge(d.gravidade)+'</td><td>'+dias+'</td></tr>';}).join('')
      +'</tbody></table>';}
  }
}

// ═══ INDICADORES ═══
function getDateRange(period){
  var now=new Date(),y=now.getFullYear(),m=now.getMonth(),d=now.getDate();
  if(period==='semana'){var s=new Date(now);s.setDate(d-6);return{start:s.toISOString().slice(0,10),end:now.toISOString().slice(0,10)};}
  if(period==='mes')return{start:new Date(y,m,1).toISOString().slice(0,10),end:now.toISOString().slice(0,10)};
  if(period==='trimestre'){var qm=Math.floor(m/3)*3;return{start:new Date(y,qm,1).toISOString().slice(0,10),end:now.toISOString().slice(0,10)};}
  if(period==='semestre'){var sm=m<6?0:6;return{start:new Date(y,sm,1).toISOString().slice(0,10),end:now.toISOString().slice(0,10)};}
  if(period==='ano')return{start:new Date(y,0,1).toISOString().slice(0,10),end:now.toISOString().slice(0,10)};
  return{start:now.toISOString().slice(0,10),end:now.toISOString().slice(0,10)};
}
function setIndPeriod(p){
  indPeriod=p;
  document.querySelectorAll('.pb').forEach(function(b){b.classList.toggle('active',b.getAttribute('data-p')===p);});
  var r=getDateRange(p);
  var f=document.getElementById('ind-from');if(f)f.value=r.start;
  var t=document.getElementById('ind-to');if(t)t.value=r.end;
  renderIndicadores();
}
function calcIndicadores(f,t,numCamas){
  var all=getDoentes();
  var numDias=daysBetween(f,t)+1;
  var diasCamas=numCamas*numDias;
  var active=all.filter(function(d){return d.dataAdmissao<=t&&(!d.saida||d.saida.data>=f);});
  var entradas=all.filter(function(d){return d.dataAdmissao>=f&&d.dataAdmissao<=t;});
  var saidas=all.filter(function(d){return d.saida&&d.saida.data>=f&&d.saida.data<=t;});
  var obitos=saidas.filter(function(d){return d.saida.tipo==='Obito';});
  var altas=saidas.filter(function(d){return d.saida.tipo==='Alta';});
  var transf=saidas.filter(function(d){return d.saida.tipo.indexOf('Transf')!==-1;});
  var diasDoentes=0;
  active.forEach(function(d){
    var s=d.dataAdmissao>=f?d.dataAdmissao:f;
    var e=d.saida&&d.saida.data<=t?d.saida.data:t;
    diasDoentes+=daysBetween(s,e);
    if(!d.saida||d.saida.data>t)diasDoentes+=1;
  });
  var ts=saidas.length;
  return{
    numDias:numDias,numCamas:numCamas,diasCamas:diasCamas,diasDoentes:diasDoentes,
    totalEntradas:entradas.length,totalSaidas:ts,
    obitos:obitos.length,altas:altas.length,transferencias:transf.length,
    taxaOcupacao:diasCamas>0?(diasDoentes/diasCamas*100):0,
    mediaPermanencia:ts>0?(diasDoentes/ts):0,
    taxaMortalidade:ts>0?(obitos.length/ts*100):0,
    indiceRotatividade:numCamas>0?(ts/numCamas):0,
    intervaloSubstituicao:ts>0?Math.max(0,(diasCamas-diasDoentes)/ts):0,
    taxaAlta:ts>0?(altas.length/ts*100):0,
    taxaTransferencia:ts>0?(transf.length/ts*100):0,
    doentesAtivos:all.filter(function(d){return d.status==='internado';}).length,
    entradas:entradas,saidas:saidas
  };
}
function renderIndicadores(){
  var f=(document.getElementById('ind-from')||{}).value||getDateRange('mes').start;
  var t=(document.getElementById('ind-to')||{}).value||todayKey();
  var nc=parseInt((document.getElementById('ind-ncamas')||{}).value||'')||getConfig().numCamas||30;
  var I=calcIndicadores(f,t,nc);
  var kEl=document.getElementById('ind-kpis');
  if(kEl){
    kEl.innerHTML=''
      +'<div class="kpi-box kpi-accent"><div class="kpi-label">Doentes Activos</div><div class="kpi-val">'+I.doentesAtivos+'</div><div class="kpi-sub">Internados agora</div></div>'
      +'<div class="kpi-box kpi-green"><div class="kpi-label">Entradas</div><div class="kpi-val">'+I.totalEntradas+'</div><div class="kpi-sub">No periodo</div></div>'
      +'<div class="kpi-box kpi-purple"><div class="kpi-label">Saidas</div><div class="kpi-val">'+I.totalSaidas+'</div><div class="kpi-sub">No periodo</div></div>'
      +'<div class="kpi-box kpi-amber"><div class="kpi-label">Taxa Ocupacao</div><div class="kpi-val">'+I.taxaOcupacao.toFixed(1)+'%</div><div class="kpi-sub">'+I.diasDoentes+' / '+I.diasCamas+' dias</div></div>'
      +'<div class="kpi-box kpi-cyan"><div class="kpi-label">Media Permanencia</div><div class="kpi-val">'+I.mediaPermanencia.toFixed(1)+'d</div><div class="kpi-sub">Dias por doente</div></div>'
      +'<div class="kpi-box kpi-red"><div class="kpi-label">Taxa Mortalidade</div><div class="kpi-val">'+I.taxaMortalidade.toFixed(1)+'%</div><div class="kpi-sub">'+I.obitos+' obito(s)</div></div>';
  }
  var tw=document.getElementById('ind-table-wrap');
  if(tw){
    tw.innerHTML='<table class="ind-table"><thead><tr><th>Indicador</th><th>Valor</th><th>Formula / Nota</th></tr></thead><tbody>'
      +'<tr><td>Dias de Camas (DC)</td><td class="ind-val">'+I.diasCamas+'</td><td><span class="ind-formula">'+I.numCamas+' camas × '+I.numDias+' dias</span></td></tr>'
      +'<tr><td>Dias de Doentes (DD)</td><td class="ind-val">'+I.diasDoentes+'</td><td><span class="ind-formula">Soma dos dias de internamento no periodo</span></td></tr>'
      +'<tr><td>Taxa de Ocupacao</td><td class="ind-val">'+I.taxaOcupacao.toFixed(2)+'%</td><td><span class="ind-formula">DD / DC × 100</span></td></tr>'
      +'<tr><td>Media de Permanencia</td><td class="ind-val">'+I.mediaPermanencia.toFixed(2)+' dias</td><td><span class="ind-formula">DD / Total Saidas</span></td></tr>'
      +'<tr><td>Taxa de Mortalidade Geral</td><td class="ind-val">'+I.taxaMortalidade.toFixed(2)+'%</td><td><span class="ind-formula">Obitos / Total Saidas × 100</span></td></tr>'
      +'<tr><td>Indice de Rotatividade</td><td class="ind-val">'+I.indiceRotatividade.toFixed(2)+'</td><td><span class="ind-formula">Total Saidas / N Camas</span></td></tr>'
      +'<tr><td>Intervalo de Substituicao</td><td class="ind-val">'+I.intervaloSubstituicao.toFixed(2)+' dias</td><td><span class="ind-formula">(DC - DD) / Total Saidas</span></td></tr>'
      +'<tr><td>Taxa de Alta</td><td class="ind-val">'+I.taxaAlta.toFixed(2)+'%</td><td><span class="ind-formula">Altas / Total Saidas × 100 ('+I.altas+' altas)</span></td></tr>'
      +'<tr><td>Taxa de Transferencia</td><td class="ind-val">'+I.taxaTransferencia.toFixed(2)+'%</td><td><span class="ind-formula">Transferencias / Total Saidas × 100 ('+I.transferencias+' transf.)</span></td></tr>'
      +'<tr><td>Total de Entradas</td><td class="ind-val">'+I.totalEntradas+'</td><td><span class="ind-formula">Admissoes no periodo</span></td></tr>'
      +'<tr><td>Total de Saidas</td><td class="ind-val">'+I.totalSaidas+'</td><td><span class="ind-formula">Altas + Obitos + Transferencias</span></td></tr>'
      +'</tbody></table>';
  }
  drawIndCharts(I,f,t,nc);
}
function isDark(){return document.documentElement.classList.contains('dark');}
function cColors(){return isDark()?['rgba(100,149,255,.8)','rgba(0,212,170,.8)','rgba(251,191,36,.8)','rgba(239,68,68,.8)','rgba(167,139,250,.8)','rgba(56,189,248,.8)']:['rgba(26,86,219,.8)','rgba(16,185,129,.8)','rgba(245,158,11,.8)','rgba(239,68,68,.8)','rgba(124,58,237,.8)','rgba(14,165,233,.8)'];}
function cText(){return isDark()?'rgba(255,255,255,.45)':'rgba(0,0,0,.35)';}
function cGrid(){return isDark()?'rgba(255,255,255,.05)':'rgba(0,0,0,.05)';}
function mkChart(id,config){var c=document.getElementById(id);if(!c||typeof Chart==='undefined')return;if(ortoCharts[id])ortoCharts[id].destroy();ortoCharts[id]=new Chart(c,config);}
function drawIndCharts(I,f,t,nc){
  var cols=cColors();var ct=cText();var cg=cGrid();
  // Entradas vs Saidas by week
  var all=getDoentes();var byWeek={};
  all.forEach(function(d){
    if(d.dataAdmissao>=f&&d.dataAdmissao<=t){var w=d.dataAdmissao.slice(0,7);byWeek[w]=byWeek[w]||{e:0,s:0};byWeek[w].e++;}
    if(d.saida&&d.saida.data>=f&&d.saida.data<=t){var w=d.saida.data.slice(0,7);byWeek[w]=byWeek[w]||{e:0,s:0};byWeek[w].s++;}
  });
  var wks=Object.keys(byWeek).sort();
  mkChart('ind-chart-mov',{type:'bar',data:{labels:wks,datasets:[{label:'Entradas',data:wks.map(function(k){return byWeek[k].e;}),backgroundColor:cols[1],borderRadius:3},{label:'Saidas',data:wks.map(function(k){return byWeek[k].s;}),backgroundColor:cols[2],borderRadius:3}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:ct,font:{size:10}}}},scales:{x:{ticks:{color:ct,font:{size:9}},grid:{display:false}},y:{ticks:{color:ct,stepSize:1},grid:{color:cg}}}}});
  // Tipo saida pie
  mkChart('ind-chart-tipo',{type:'doughnut',data:{labels:['Altas','Obitos','Transf.Int','Transf.Ext'],datasets:[{data:[I.altas,I.obitos,I.transferencias,I.totalSaidas-I.altas-I.obitos-I.transferencias].map(function(v){return Math.max(0,v);}),backgroundColor:[cols[1],cols[3],cols[4],cols[5]]}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'right',labels:{color:ct,font:{size:9},boxWidth:12}}}}});
  // Taxa ocupacao trend (monthly)
  var months={};all.forEach(function(d){
    var start=d.dataAdmissao>=f?d.dataAdmissao:f;
    var end=d.saida&&d.saida.data<=t?d.saida.data:t;
    if(start>t||end<f)return;
    var cur=new Date(start);while(cur.toISOString().slice(0,10)<=end&&cur.toISOString().slice(0,10)<=t){
      var mk=cur.toISOString().slice(0,7);months[mk]=(months[mk]||0)+1;cur.setDate(cur.getDate()+1);}
  });
  var mks=Object.keys(months).sort();
  var daysInMonth=mks.map(function(mk){var d=new Date(mk+'-01');var n=new Date(d.getFullYear(),d.getMonth()+1,0).getDate();return nc*n;});
  var tocc=mks.map(function(mk,i){return daysInMonth[i]>0?(months[mk]/daysInMonth[i]*100):0;});
  mkChart('ind-chart-ocup',{type:'line',data:{labels:mks,datasets:[{label:'Taxa Ocupacao %',data:tocc,borderColor:cols[0],backgroundColor:cols[0].replace('.8)','.12)'),fill:true,tension:.3,pointRadius:3}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{ticks:{color:ct,font:{size:9}},grid:{display:false}},y:{min:0,max:100,ticks:{color:ct,callback:function(v){return v+'%'}},grid:{color:cg}}}}});
  // Gravidade distribution
  var all2=getDoentes().filter(function(d){return d.dataAdmissao>=f&&d.dataAdmissao<=t;});
  var gravCount={Leve:0,Moderada:0,Grave:0,Critica:0};all2.forEach(function(d){if(gravCount[d.gravidade]!==undefined)gravCount[d.gravidade]++;});
  mkChart('ind-chart-grav',{type:'doughnut',data:{labels:Object.keys(gravCount),datasets:[{data:Object.values(gravCount),backgroundColor:[cols[1],cols[2],cols[3],cols[3].replace('dc2626','8b0000')]}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'right',labels:{color:ct,font:{size:9},boxWidth:12}}}}});
  // Tipo admissao
  var tadmCount={};all2.forEach(function(d){tadmCount[d.tipoAdmissao]=(tadmCount[d.tipoAdmissao]||0)+1;});
  var tadmKeys=Object.keys(tadmCount);
  mkChart('ind-chart-tadm',{type:'bar',data:{labels:tadmKeys,datasets:[{data:tadmKeys.map(function(k){return tadmCount[k];}),backgroundColor:cols.slice(0,tadmKeys.length),borderRadius:4}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{ticks:{color:ct,font:{size:9}},grid:{display:false}},y:{ticks:{color:ct,stepSize:1},grid:{color:cg}}}}});
}

// ═══ DIAGNOSTICOS ═══
function renderDiagnosticos(){
  var ef=(document.getElementById('diag-estado-f')||{}).value||'';
  var q=((document.getElementById('diag-search')||{}).value||'').toLowerCase();
  var all=getDoentes();
  if(ef==='internado')all=all.filter(function(d){return d.status==='internado';});
  else if(ef==='saido')all=all.filter(function(d){return d.status!=='internado';});
  if(q)all=all.filter(function(d){return (d.diagnostico||'').toLowerCase().includes(q);});
  var diagMap={};
  all.forEach(function(d){
    var k=d.diagnostico||'Nao especificado';
    if(!diagMap[k])diagMap[k]={total:0,internados:0,altas:0,obitos:0,transf:0,gravidade:{}};
    diagMap[k].total++;
    if(d.status==='internado')diagMap[k].internados++;
    else if(d.status==='alta')diagMap[k].altas++;
    else if(d.status==='obito')diagMap[k].obitos++;
    else diagMap[k].transf++;
    diagMap[k].gravidade[d.gravidade]=(diagMap[k].gravidade[d.gravidade]||0)+1;
  });
  var sorted=Object.keys(diagMap).sort(function(a,b){return diagMap[b].total-diagMap[a].total;});
  var kEl=document.getElementById('diag-kpis');
  if(kEl)kEl.innerHTML='<div class="kpi-box kpi-accent"><div class="kpi-label">Diagnosticos Distintos</div><div class="kpi-val">'+sorted.length+'</div></div>'
    +'<div class="kpi-box kpi-green"><div class="kpi-label">Total Doentes</div><div class="kpi-val">'+all.length+'</div></div>';
  var top10=sorted.slice(0,10);
  var cols=cColors();var ct=cText();var cg=cGrid();
  mkChart('diag-chart-top',{type:'bar',data:{labels:top10.map(function(k){return k.length>20?k.slice(0,20)+'...':k;}),datasets:[{data:top10.map(function(k){return diagMap[k].total;}),backgroundColor:cols[0],borderRadius:3}]},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{ticks:{color:ct,stepSize:1},grid:{color:cg}},y:{ticks:{color:ct,font:{size:9}},grid:{display:false}}}}});
  // Gravidade stacked
  var gravKeys=['Leve','Moderada','Grave','Critica'];var gcols=[cols[1],cols[2],cols[3],cols[3]];
  mkChart('diag-chart-grav',{type:'bar',data:{labels:top10.map(function(k){return k.length>15?k.slice(0,15)+'...':k;}),datasets:gravKeys.map(function(g,i){return{label:g,data:top10.map(function(k){return diagMap[k].gravidade[g]||0;}),backgroundColor:gcols[i],borderRadius:2};})},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'bottom',labels:{color:ct,font:{size:9},boxWidth:10}}},scales:{x:{stacked:true,ticks:{color:ct,stepSize:1},grid:{color:cg}},y:{stacked:true,ticks:{color:ct,font:{size:9}},grid:{display:false}}}}});
  var tEl=document.getElementById('diag-table');
  if(tEl){
    tEl.innerHTML='<table class="data-table"><thead><tr><th>Diagnostico</th><th>Total</th><th>Internados</th><th>Altas</th><th>Obitos</th><th>Transf.</th></tr></thead><tbody>'
      +sorted.map(function(k){var v=diagMap[k];return '<tr><td>'+k+'</td><td><strong>'+v.total+'</strong></td><td>'+v.internados+'</td><td>'+v.altas+'</td><td>'+v.obitos+'</td><td>'+v.transf+'</td></tr>';}).join('')
      +'</tbody></table>';
  }
}

// ═══ PESQUISA ═══
function renderPesquisa(){
  var q=((document.getElementById('pesq-input')||{}).value||'').toLowerCase();
  var ef=(document.getElementById('pesq-estado')||{}).value||'';
  var gf=(document.getElementById('pesq-grav')||{}).value||'';
  var all=getDoentes();
  if(ef)all=all.filter(function(d){
    if(ef==='internado')return d.status==='internado';
    if(ef==='alta')return d.status==='alta';
    if(ef==='obito')return d.status==='obito';
    if(ef==='transferencia')return d.status==='transferencia_interna'||d.status==='transferencia_externa';
    return true;
  });
  if(gf)all=all.filter(function(d){return d.gravidade===gf;});
  if(q)all=all.filter(function(d){
    return (d.nome||'').toLowerCase().includes(q)||(d.diagnostico||'').toLowerCase().includes(q)||
           (d.numStr||'').toLowerCase().includes(q)||(d.cama||'').toLowerCase().includes(q)||
           (d.bi||'').toLowerCase().includes(q)||(d.medico||'').toLowerCase().includes(q);
  });
  var ps=document.getElementById('pesq-stats');if(ps)ps.textContent=all.length+' resultado(s)';
  var c=document.getElementById('pesq-results');if(!c)return;
  if(!q&&!ef&&!gf){c.innerHTML='<div class="no-data">Digite algo para pesquisar.</div>';return;}
  if(!all.length){c.innerHTML='<div class="no-data">Nenhum resultado encontrado.</div>';return;}
  c.innerHTML=all.map(function(d){
    return '<div class="doc-card">'
      +'<div class="doc-card-header">'
      +'<span class="doc-num">'+d.numStr+'</span>'
      +statusBadge(d.status)+gravBadge(d.gravidade)
      +'<span class="doc-data">'+fmtDate(d.dataAdmissao)+'</span>'
      +'</div>'
      +'<div class="doc-card-body">'
      +'<div class="doc-name">'+d.nome+' &nbsp;<span style="font-size:.68rem;font-weight:400;color:var(--muted);">'+d.sexo+' · '+d.idade+' anos</span></div>'
      +'<div class="doc-sub">'+d.diagnostico+'</div>'
      +'<div class="doc-sub">Cama: '+d.cama+(d.medico?' · Dr: '+d.medico:'')+'</div>'
      +(d.saida?'<div class="doc-sub">Saida: '+fmtDate(d.saida.data)+' — '+d.saida.tipo+' ('+d.saida.diasInternamento+' dias)</div>':'')
      +'<div style="margin-top:6px;"><button class="btn btn-outline btn-xs" onclick="openFicha(\''+d.id+'\')">Ver Ficha</button></div>'
      +'</div></div>';
  }).join('');
}

// ═══ FICHA ═══
function openFicha(id){
  fichaCurId=id;var docs=getDoentes();var d=docs.find(function(x){return x.id===id;});if(!d)return;
  var sb=document.getElementById('ficha-saida-btn');if(sb)sb.style.display=d.status==='internado'?'':'none';
  var fc=document.getElementById('ficha-content');
  if(fc){
    var dias=d.saida?d.saida.diasInternamento:daysBetween(d.dataAdmissao,todayKey());
    fc.innerHTML='<div class="modal-title">Ficha do Doente — '+d.numStr+'</div>'
      +'<div class="modal-sub">Registado por '+d.profissional+' em '+fmtDate(d.dataAdmissao)+'</div>'
      +'<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px;">'
      +'<div><div style="font-size:.58rem;color:var(--muted);font-weight:600;text-transform:uppercase;">Nome</div><div style="font-weight:700;font-size:.9rem;">'+d.nome+'</div></div>'
      +'<div><div style="font-size:.58rem;color:var(--muted);font-weight:600;text-transform:uppercase;">Processo</div><div style="font-family:var(--fm);font-weight:700;color:var(--accent);">'+d.numStr+'</div></div>'
      +'<div><div style="font-size:.58rem;color:var(--muted);font-weight:600;text-transform:uppercase;">Data Nascimento</div><div>'+fmtDate(d.dataNascimento)+' ('+d.idade+' anos)</div></div>'
      +'<div><div style="font-size:.58rem;color:var(--muted);font-weight:600;text-transform:uppercase;">Sexo</div><div>'+(d.sexo==='M'?'Masculino':'Feminino')+'</div></div>'
      +'<div><div style="font-size:.58rem;color:var(--muted);font-weight:600;text-transform:uppercase;">N BI / Processo</div><div>'+d.bi+'</div></div>'
      +'<div><div style="font-size:.58rem;color:var(--muted);font-weight:600;text-transform:uppercase;">Estado</div><div>'+statusBadge(d.status)+'</div></div>'
      +'<div><div style="font-size:.58rem;color:var(--muted);font-weight:600;text-transform:uppercase;">Diagnostico</div><div style="font-weight:600;">'+d.diagnostico+(d.cid?' — '+d.cid:'')+'</div></div>'
      +'<div><div style="font-size:.58rem;color:var(--muted);font-weight:600;text-transform:uppercase;">Gravidade</div><div>'+gravBadge(d.gravidade)+'</div></div>'
      +'<div><div style="font-size:.58rem;color:var(--muted);font-weight:600;text-transform:uppercase;">Admissao</div><div>'+fmtDate(d.dataAdmissao)+' '+d.horaAdmissao+' ('+d.tipoAdmissao+')</div></div>'
      +'<div><div style="font-size:.58rem;color:var(--muted);font-weight:600;text-transform:uppercase;">Cama / Enfermaria</div><div>'+d.cama+(d.enfermaria?' / '+d.enfermaria:'')+'</div></div>'
      +(d.medico?'<div><div style="font-size:.58rem;color:var(--muted);font-weight:600;text-transform:uppercase;">Medico</div><div>'+d.medico+'</div></div>':'')
      +'<div><div style="font-size:.58rem;color:var(--muted);font-weight:600;text-transform:uppercase;">Dias Internamento</div><div style="font-family:var(--fm);font-weight:700;">'+dias+'</div></div>'
      +(d.cirurgia?'<div class="span2"><div style="font-size:.58rem;color:var(--muted);font-weight:600;text-transform:uppercase;">Cirurgia</div><div>'+d.cirurgiaDesc+'</div></div>':'')
      +(d.obs?'<div class="span2"><div style="font-size:.58rem;color:var(--muted);font-weight:600;text-transform:uppercase;">Observacoes</div><div>'+d.obs+'</div></div>':'')
      +(d.saida?'<div class="span2" style="background:rgba(26,86,219,.05);border-radius:8px;padding:10px;">'
        +'<div style="font-size:.58rem;color:var(--muted);font-weight:600;text-transform:uppercase;margin-bottom:6px;">Saida</div>'
        +'<div><strong>Tipo:</strong> '+d.saida.tipo+'</div>'
        +'<div><strong>Data:</strong> '+fmtDate(d.saida.data)+' '+d.saida.hora+'</div>'
        +'<div><strong>Dias:</strong> '+d.saida.diasInternamento+'</div>'
        +(d.saida.destino?'<div><strong>Destino/Obs:</strong> '+d.saida.destino+'</div>':'')
        +'</div>':'')
      +'</div>'
      +(d.historico&&d.historico.length?'<div style="margin-top:8px;"><div style="font-size:.62rem;font-weight:700;color:var(--muted);text-transform:uppercase;margin-bottom:6px;">Historico</div>'
        +d.historico.map(function(h){return '<div style="font-size:.65rem;border-left:2px solid var(--border);padding-left:8px;margin-bottom:4px;color:var(--muted);">'+new Date(h.ts).toLocaleString('pt-PT')+' — '+h.profissional+': '+h.acao+'</div>';}).join('')+'</div>':'');
  }
  document.getElementById('modal-ficha').style.display='flex';
}
function abrirSaidaDeFicha(){if(fichaCurId){document.getElementById('modal-ficha').style.display='none';abrirSaida(fichaCurId);}}

// ═══ DEFINICOES ═══
function unlockDef(){
  var s=((document.getElementById('def-senha-input')||{}).value||'');
  var err=document.getElementById('def-lock-err');
  if(s!==getConfig().senhaChefe){err.style.display='block';err.textContent='Senha incorrecta.';return;}
  document.getElementById('def-lock').style.display='none';
  document.getElementById('def-content').style.display='block';
  renderDefinicoes();
}
function renderDefinicoes(){
  var cfg=getConfig();
  var svc=document.getElementById('def-servico');if(svc)svc.value=cfg.servico||'Medicina/Ortopedia';
  var nc=document.getElementById('def-ncamas');if(nc)nc.value=cfg.numCamas||30;
  var dn=document.getElementById('def-num');if(dn)dn.value=cfg.numAtual||1;
  var da=document.getElementById('def-ano');if(da)da.value=cfg.ano||new Date().getFullYear();
  updateDefPreview();
  var pl=document.getElementById('prof-list');
  if(pl){pl.innerHTML=cfg.profissionais.map(function(p){return '<div class="prof-item"><span>'+p.nome+'</span><button class="btn btn-outline btn-xs" style="color:var(--red);" onclick="removeProfissional(\''+p.id+'\')">Remover</button></div>';}).join('')||'<div style="color:var(--muted);font-size:.72rem;">Nenhum profissional.</div>';}
  renderBackupStatus();
}
function updateDefPreview(){
  var n=parseInt((document.getElementById('def-num')||{}).value)||1;
  var el=document.getElementById('def-preview');if(el)el.textContent='ORT/'+new Date().getFullYear()+'/'+String(n).padStart(3,'0');
}
function saveDefinicoes(){
  var cfg=getConfig();
  var svc=((document.getElementById('def-servico')||{}).value||'').trim();
  var nc=parseInt((document.getElementById('def-ncamas')||{}).value)||30;
  if(svc)cfg.servico=svc;cfg.numCamas=nc;saveConfig(cfg);toast('Configuracoes guardadas');
}
function saveNumeracao(){
  var cfg=getConfig();var n=parseInt((document.getElementById('def-num')||{}).value)||1;cfg.numAtual=n;saveConfig(cfg);toast('Numeracao actualizada');updateNumPreview();
}
function saveSenhaChefe(){
  var ns=((document.getElementById('def-new-senha')||{}).value||'');
  var cs=((document.getElementById('def-conf-senha')||{}).value||'');
  if(!ns||ns!==cs){toast('Senhas nao coincidem','err');return;}
  var cfg=getConfig();cfg.senhaChefe=ns;saveConfig(cfg);toast('Senha actualizada');
  document.getElementById('def-new-senha').value='';document.getElementById('def-conf-senha').value='';
}
function addProfissional(){
  var nome=((document.getElementById('new-prof-nome')||{}).value||'').trim();
  var senha=((document.getElementById('new-prof-senha')||{}).value||'');
  if(!nome||!senha){toast('Preencha nome e senha','err');return;}
  var cfg=getConfig();var id='p'+Date.now().toString(36);
  cfg.profissionais.push({id:id,nome:nome,senha:senha});saveConfig(cfg);
  document.getElementById('new-prof-nome').value='';document.getElementById('new-prof-senha').value='';
  renderDefinicoes();toast('Profissional adicionado');
}
function removeProfissional(id){
  var cfg=getConfig();cfg.profissionais=cfg.profissionais.filter(function(p){return p.id!==id;});
  if(!cfg.profissionais.length)cfg.profissionais=[{id:'admin',nome:'Secretaria',senha:'1234'}];
  saveConfig(cfg);renderDefinicoes();toast('Profissional removido');
}
function exportarJSON(){
  var data={config:getConfig(),doentes:getDoentes(),exportadoEm:new Date().toISOString()};
  var blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  var url=URL.createObjectURL(blob);var a=document.createElement('a');a.href=url;a.download='ortopedia_'+todayKey()+'.json';document.body.appendChild(a);a.click();document.body.removeChild(a);URL.revokeObjectURL(url);toast('Dados exportados');
}
function downloadBackup(){
  var data={ts:new Date().toISOString(),doentes:getDoentes(),config:getConfig()};
  var blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  var url=URL.createObjectURL(blob);var a=document.createElement('a');a.href=url;
  a.download='backup_ortopedia_'+todayKey()+'.json';document.body.appendChild(a);a.click();document.body.removeChild(a);URL.revokeObjectURL(url);
  localStorage.setItem('hp_orto_last_backup',todayKey());renderBackupStatus();toast('Backup realizado','info');
}
function renderBackupStatus(){
  var el=document.getElementById('def-backup-status');if(!el)return;
  var last=localStorage.getItem('hp_orto_last_backup');
  el.innerHTML='<div style="font-size:.7rem;color:var(--muted);">Ultimo backup: <strong>'+(last?fmtDate(last):'Nunca')+'</strong></div>';
}

// ═══ PDF EXPORT ═══
function jsPDFReady(){return typeof jspdf!=='undefined';}
function exportIndPDF(period){
  if(!jsPDFReady()){toast('Biblioteca PDF a carregar, tente de novo','err');return;}
  var f,t,label;
  if(period==='custom'){f=(document.getElementById('ind-from')||{}).value||getDateRange('mes').start;t=(document.getElementById('ind-to')||{}).value||todayKey();label='Periodo Seleccionado';}
  else{var r=getDateRange(period);f=r.start;t=r.end;label={'semana':'Semanal','mes':'Mensal','trimestre':'Trimestral','semestre':'Semestral','ano':'Anual'}[period]||period;}
  var nc=parseInt((document.getElementById('ind-ncamas')||{}).value||'')||getConfig().numCamas||30;
  var I=calcIndicadores(f,t,nc);
  var doc=new jspdf.jsPDF();
  doc.setFontSize(14);doc.setFont('helvetica','bold');
  doc.text('Hospital do Prenda — Servico de Medicina/Ortopedia',14,14);
  doc.setFontSize(9);doc.setFont('helvetica','normal');doc.setTextColor(80);
  doc.text('Relatorio de Indicadores Hospitalares — '+label,14,21);
  doc.text('Periodo: '+fmtDate(f)+' a '+fmtDate(t)+'   |   N Camas: '+nc,14,27);
  doc.setTextColor(0);
  doc.autoTable({startY:32,head:[['Indicador','Valor','Notas']],
    body:[
      ['Doentes Activos',I.doentesAtivos,'Internados no momento'],
      ['Total Entradas',I.totalEntradas,'Admissoes no periodo'],
      ['Total Saidas',I.totalSaidas,'Altas+Obitos+Transf.'],
      ['Dias de Camas (DC)',I.diasCamas,nc+' camas x '+I.numDias+' dias'],
      ['Dias de Doentes (DD)',I.diasDoentes,'Soma dias internamento'],
      ['Taxa de Ocupacao',I.taxaOcupacao.toFixed(2)+'%','DD/DC x 100'],
      ['Media de Permanencia',I.mediaPermanencia.toFixed(2)+' dias','DD/Total Saidas'],
      ['Taxa de Mortalidade',I.taxaMortalidade.toFixed(2)+'%',I.obitos+' obito(s)'],
      ['Indice de Rotatividade',I.indiceRotatividade.toFixed(2),'Saidas/N Camas'],
      ['Intervalo de Substituicao',I.intervaloSubstituicao.toFixed(2)+' dias','(DC-DD)/Saidas'],
      ['Taxa de Alta',I.taxaAlta.toFixed(2)+'%',I.altas+' alta(s)'],
      ['Taxa de Transferencia',I.taxaTransferencia.toFixed(2)+'%',I.transferencias+' transf.']
    ],
    styles:{fontSize:9,cellPadding:3},
    headStyles:{fillColor:[26,86,219],textColor:255,fontStyle:'bold'},
    alternateRowStyles:{fillColor:[240,244,255]},
    columnStyles:{1:{fontStyle:'bold',textColor:[26,86,219]}}
  });
  doc.save('indicadores_ortopedia_'+period+'_'+todayKey()+'.pdf');
  toast('PDF guardado','info');
}
function exportInternPDF(){
  if(!jsPDFReady()){toast('Biblioteca PDF a carregar','err');return;}
  var docs=getDoentes().filter(function(d){return d.status==='internado';});
  var doc=new jspdf.jsPDF({orientation:'landscape'});
  doc.setFontSize(12);doc.setFont('helvetica','bold');
  doc.text('Doentes Internados — Servico Medicina/Ortopedia',14,14);
  doc.setFontSize(8);doc.setFont('helvetica','normal');doc.setTextColor(80);
  doc.text('Emitido em '+new Date().toLocaleString('pt-PT'),14,20);doc.setTextColor(0);
  doc.autoTable({startY:25,
    head:[['Processo','Nome','Idade','Cama','Diagnostico','Gravidade','Admissao','Dias','Medico']],
    body:docs.map(function(d){return[d.numStr,d.nome,d.idade+'a',d.cama,d.diagnostico.substring(0,30),d.gravidade,fmtDate(d.dataAdmissao),daysBetween(d.dataAdmissao,todayKey()),d.medico||''];}),
    styles:{fontSize:7.5,cellPadding:2},headStyles:{fillColor:[26,86,219],textColor:255},alternateRowStyles:{fillColor:[240,244,255]}
  });
  doc.save('internados_'+todayKey()+'.pdf');toast('PDF guardado','info');
}
function exportSaidasPDF(){
  if(!jsPDFReady()){toast('Biblioteca PDF a carregar','err');return;}
  var f=(document.getElementById('saidas-data-f')||{}).value||'';
  var t=(document.getElementById('saidas-data-t')||{}).value||'';
  var docs=getDoentes().filter(function(d){return d.saida;});
  if(f)docs=docs.filter(function(d){return d.saida.data>=f;});
  if(t)docs=docs.filter(function(d){return d.saida.data<=t;});
  var doc=new jspdf.jsPDF({orientation:'landscape'});
  doc.setFontSize(12);doc.setFont('helvetica','bold');
  doc.text('Controlo de Saidas — Medicina/Ortopedia',14,14);
  doc.setFontSize(8);doc.setFont('helvetica','normal');doc.setTextColor(80);
  doc.text('Periodo: '+(f?fmtDate(f):'Inicio')+' a '+(t?fmtDate(t):'Hoje')+'   Total: '+docs.length,14,20);doc.setTextColor(0);
  doc.autoTable({startY:25,
    head:[['Processo','Nome','Tipo Saida','Admissao','Saida','Dias','Diagnostico']],
    body:docs.map(function(d){return[d.numStr,d.nome.substring(0,20),d.saida.tipo,fmtDate(d.dataAdmissao),fmtDate(d.saida.data),d.saida.diasInternamento,d.diagnostico.substring(0,30)];}),
    styles:{fontSize:7.5,cellPadding:2},headStyles:{fillColor:[26,86,219],textColor:255},alternateRowStyles:{fillColor:[240,244,255]}
  });
  doc.save('saidas_'+todayKey()+'.pdf');toast('PDF guardado','info');
}
function exportMovPDF(){
  if(!jsPDFReady()){toast('Biblioteca PDF a carregar','err');return;}
  var data=(document.getElementById('mov-data')||{}).value||todayKey();
  var prev=new Date(data);prev.setDate(prev.getDate()-1);var prevKey=prev.toISOString().slice(0,10);
  var all=getDoentes();
  var existIni=all.filter(function(d){return d.dataAdmissao<=prevKey&&(!d.saida||d.saida.data>=data);});
  var entradas=all.filter(function(d){return d.dataAdmissao===data;});
  var saidasDia=all.filter(function(d){return d.saida&&d.saida.data===data;});
  var cfg=getConfig();var nc=cfg.numCamas||30;
  var doenteDia=existIni.length+entradas.length;
  var doc=new jspdf.jsPDF();
  doc.setFontSize(13);doc.setFont('helvetica','bold');
  doc.text('Boletim de Movimento Hospitalar',14,14);
  doc.setFontSize(9);doc.setFont('helvetica','normal');doc.setTextColor(80);
  doc.text('Servico de Medicina/Ortopedia   |   Data: '+fmtDate(data),14,21);doc.setTextColor(0);
  doc.autoTable({startY:27,
    head:[['Descricao','Valor']],
    body:[
      ['Existentes no Inicio do Dia',String(existIni.length)],
      ['Entradas do Dia',String(entradas.length)],
      ['Total Saidas',String(saidasDia.length)],
      ['  — Altas',String(saidasDia.filter(function(d){return d.saida.tipo==='Alta';}).length)],
      ['  — Obitos',String(saidasDia.filter(function(d){return d.saida.tipo==='Obito';}).length)],
      ['  — Transf. Interna',String(saidasDia.filter(function(d){return d.saida.tipo==='Transferencia Interna';}).length)],
      ['  — Transf. Externa',String(saidasDia.filter(function(d){return d.saida.tipo==='Transferencia Externa';}).length)],
      ['Existentes no Fim do Dia',String(existIni.length+entradas.length-saidasDia.length)],
      ['Dias de Doentes',String(doenteDia)],
      ['N de Camas',String(nc)],
      ['Taxa de Ocupacao',nc>0?(doenteDia/nc*100).toFixed(1)+'%':'---']
    ],
    styles:{fontSize:9,cellPadding:4},
    headStyles:{fillColor:[26,86,219],textColor:255},
    alternateRowStyles:{fillColor:[240,244,255]},
    columnStyles:{1:{fontStyle:'bold',textColor:[26,86,219]}}
  });
  doc.save('movimento_'+data+'.pdf');toast('PDF guardado','info');
}
function exportFichaPDF(){
  if(!fichaCurId){return;}
  var docs=getDoentes();var d=docs.find(function(x){return x.id===fichaCurId;});if(!d)return;
  if(!jsPDFReady()){toast('Biblioteca PDF a carregar','err');return;}
  var dias=d.saida?d.saida.diasInternamento:daysBetween(d.dataAdmissao,todayKey());
  var doc=new jspdf.jsPDF();
  doc.setFontSize(13);doc.setFont('helvetica','bold');
  doc.text('Ficha do Doente — '+d.numStr,14,14);
  doc.setFontSize(9);doc.setFont('helvetica','normal');doc.setTextColor(80);
  doc.text('Servico de Medicina/Ortopedia — Hospital do Prenda',14,21);doc.setTextColor(0);
  doc.autoTable({startY:27,
    head:[['Campo','Valor']],
    body:[
      ['Nome Completo',d.nome],['Sexo',d.sexo==='M'?'Masculino':'Feminino'],['Idade',d.idade+' anos'],
      ['Data de Nascimento',fmtDate(d.dataNascimento)],['N Processo / BI',d.bi],
      ['Diagnostico',d.diagnostico+(d.cid?' ('+d.cid+')':'')],['Gravidade',d.gravidade],
      ['Tipo de Admissao',d.tipoAdmissao],['Data de Admissao',fmtDate(d.dataAdmissao)+' '+d.horaAdmissao],
      ['Cama',d.cama+(d.enfermaria?' / Enf: '+d.enfermaria:'')],
      ['Medico Responsavel',d.medico||'---'],['Cirurgia',d.cirurgia?(d.cirurgiaDesc||'Sim'):'Nao'],
      ['Observacoes',d.obs||'---'],['Dias de Internamento',String(dias)],
      ['Estado',d.status==='internado'?'Internado':d.saida?d.saida.tipo:'---'],
      ['Saida — Data',d.saida?fmtDate(d.saida.data)+' '+d.saida.hora:'---'],
      ['Saida — Destino/Obs',d.saida&&d.saida.destino?d.saida.destino:'---']
    ],
    styles:{fontSize:9,cellPadding:3},
    headStyles:{fillColor:[26,86,219],textColor:255},
    alternateRowStyles:{fillColor:[240,244,255]}
  });
  doc.save('ficha_'+d.numStr.replace('/','_')+'_'+todayKey()+'.pdf');toast('Ficha exportada','info');
}

// ═══ THEME / SPLASH / INIT ═══
function toggleTheme(){var dark=document.documentElement.classList.toggle('dark');localStorage.setItem('hp_orto_theme',dark?'dark':'light');}
(function(){var D=4000,ring=document.getElementById('spl-ring'),pct=document.getElementById('spl-pct'),C=263.9,start=null;
  if(!ring)return;
  function step(ts){if(!start)start=ts;var p=Math.min((ts-start)/D,1),e=p<.5?2*p*p:-1+(4-2*p)*p;
    ring.style.strokeDashoffset=C*(1-e);if(pct)pct.textContent=Math.round(e*100)+'%';
    if(p<1){requestAnimationFrame(step);return;}
    var s=document.getElementById('splash');if(s){s.style.transition='opacity .45s';s.style.opacity='0';setTimeout(function(){s.style.display='none';},450);}
  }requestAnimationFrame(step);
})();
document.addEventListener('DOMContentLoaded',function(){
  checkSession();
  var md=document.getElementById('mov-data');if(md)md.value=todayKey();
  var r=getDateRange('mes');
  var f=document.getElementById('ind-from');if(f)f.value=r.start;
  var t=document.getElementById('ind-to');if(t)t.value=r.end;
  var nc=document.getElementById('ind-ncamas');if(nc)nc.value=getConfig().numCamas||30;
  var ra=document.getElementById('r-dadm');if(ra)ra.value=todayKey();
  var rh=document.getElementById('r-hadm');if(rh)rh.value=fmtTime();
  document.getElementById('r-cirug').addEventListener('change',toggleCirug);
});
"""

def build_html():
    nav = """
<nav class="sidebar" id="sidebar">
  <div class="nav-section-lbl">Principal</div>
  <div class="nav-item active" onclick="nav('registo')">
    <svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>Registo de Doente
  </div>
  <div class="nav-item" onclick="nav('internados')">
    <svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>Internados
  </div>
  <div class="nav-item" onclick="nav('saidas')">
    <svg viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9"/></svg>Saídas
  </div>
  <div class="nav-item" onclick="nav('movimento')">
    <svg viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>Movimento
  </div>
  <div class="nav-section-lbl">Análise</div>
  <div class="nav-item" onclick="nav('indicadores')">
    <svg viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>Indicadores
  </div>
  <div class="nav-item" onclick="nav('diagnosticos')">
    <svg viewBox="0 0 24 24"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>Diagnósticos
  </div>
  <div class="nav-item" onclick="nav('pesquisa')">
    <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>Pesquisa
  </div>
  <div class="nav-section-lbl">Sistema</div>
  <div class="nav-item" onclick="nav('definicoes')">
    <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.07 4.93a10 10 0 010 14.14M4.93 4.93a10 10 0 000 14.14"/></svg>Definições
  </div>
</nav>"""

    splash = f"""
<div id="splash" style="position:fixed;inset:0;background:#0c1421;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:9999;">
  <svg width="100" height="100" viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="42" fill="none" stroke="rgba(255,255,255,.1)" stroke-width="8"/>
    <circle id="spl-ring" cx="50" cy="50" r="42" fill="none" stroke="#1a56db" stroke-width="8"
      stroke-linecap="round" stroke-dasharray="{CIRC}" stroke-dashoffset="{CIRC}"
      transform="rotate(-90 50 50)"/>
  </svg>
  <div style="margin-top:16px;font-family:'Inter',sans-serif;font-size:.8rem;color:rgba(255,255,255,.7);">
    Hospital do Prenda — Ortopedia/Medicina
  </div>
  <div id="spl-pct" style="font-size:.65rem;color:rgba(255,255,255,.4);margin-top:6px;">0%</div>
</div>"""

    html = f"""<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ortopedia/Medicina — Hospital do Prenda</title>
<style>{CSS}</style>
</head>
<body>
{splash}

<!-- ── MODAIS ── -->
{MODAL_LOGIN}
{MODAL_SAIDA}
{MODAL_FICHA}

<!-- Modal Confirmar Eliminação -->
<div id="modal-del" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:800;align-items:center;justify-content:center;" onclick="if(event.target===this)closeModal('modal-del')">
  <div style="background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:28px 32px;max-width:360px;width:90%;text-align:center;">
    <div style="font-size:1.8rem;margin-bottom:10px;">⚠️</div>
    <div style="font-weight:700;font-size:.95rem;margin-bottom:6px;">Eliminar Registo</div>
    <div style="font-size:.75rem;color:var(--muted);margin-bottom:20px;">Esta ação é irreversível. Confirmas a eliminação?</div>
    <div style="display:flex;gap:10px;justify-content:center;">
      <button class="btn btn-outline btn-sm" onclick="closeModal('modal-del')">Cancelar</button>
      <button class="btn btn-sm" style="background:var(--red);color:#fff;border-color:var(--red);" onclick="confirmDel()">Eliminar</button>
    </div>
  </div>
</div>

<!-- ── HEADER ── -->
<header>
  <div class="header-logo"><img src="{HOSP_IMG}" alt="Logo"></div>
  <div class="header-title">
    <h1>Hospital do Prenda</h1>
    <span>Sistema de Gestão — Serviço de Ortopedia/Medicina</span>
  </div>
  <div style="margin-left:auto;display:flex;align-items:center;gap:10px;">
    <button class="btn btn-outline btn-sm" onclick="toggleTheme()" title="Tema">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
    </button>
  </div>
</header>

<!-- Staff bar -->
<div class="hp-staff-bar">
  <span class="hp-staff-lbl">Utilizador:</span>
  <span class="hp-staff-name" id="staff-name">—</span>
  <span class="hp-staff-sep">|</span>
  <span class="hp-staff-lbl">Data:</span>
  <span id="staff-date"></span>
  <span class="hp-staff-sep">|</span>
  <span class="hp-staff-lbl">Serviço:</span>
  <span>Ortopedia/Medicina</span>
  <span style="margin-left:auto;"></span>
  <button class="hbtn" onclick="doLogout()">Sair</button>
</div>

<!-- ── LAYOUT ── -->
<div class="layout">
{nav}
<main class="main">
{SEC_REGISTO}
{SEC_INTERNADOS}
{SEC_SAIDAS}
{SEC_MOVIMENTO}
{SEC_INDICADORES}
{SEC_DIAGNOSTICOS}
{SEC_PESQUISA}
{SEC_DEFINICOES}
</main>
</div>

<!-- Toast -->
<div id="toast" style="display:none;position:fixed;bottom:24px;right:24px;padding:10px 18px;border-radius:10px;font-size:.76rem;font-weight:600;z-index:9000;box-shadow:0 4px 20px rgba(0,0,0,.18);transition:opacity .3s;"></div>

<!-- CDN Scripts -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.8.2/jspdf.plugin.autotable.min.js"></script>
<script>
(function(){{
  var th=localStorage.getItem('hp_orto_theme')||'light';
  if(th==='dark')document.documentElement.classList.add('dark');
}})();
</script>
<script>
{JS}
</script>
</body>
</html>"""
    return html


if __name__ == '__main__':
    os.makedirs('procedimentos', exist_ok=True)
    out = 'procedimentos/ortopedia_medicina.html'
    html = build_html()
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    kb = len(html.encode()) // 1024
    print(f'✓ Gerado: {out} ({kb} KB)')
