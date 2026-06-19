#!/usr/bin/env python3
"""gerar_ortopedia.py — Serviço de Medicina/Ortopedia (v2)"""
import os, re, math

HOSP_IMG = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVQI12NgAAIABQAABjE+ibYAAAAASUVORK5CYII='
for _src in ['procedimentos/secretaria_geral.html','procedimentos/ortopedia_medicina.html']:
    try:
        _t = open(_src, encoding='utf-8').read()
        _m = re.search(r'data:image/jpeg;base64,([A-Za-z0-9+/=]+)', _t)
        if _m: HOSP_IMG = 'data:image/jpeg;base64,' + _m.group(1); break
    except: pass

CIRC = str(round(2*math.pi*42, 1))

CSS = """\
:root{
  --bg:#f0f4f8;--surface:#fff;--surface2:#f8fafc;--border:#e2e8f0;
  --text:#0f172a;--fg:#0f172a;--muted:#64748b;
  --accent:#1a56db;--green:#059669;--red:#dc2626;--amber:#d97706;
  --purple:#7c3aed;--cyan:#0891b2;
  --fh:'Inter',system-ui,sans-serif;--fm:'JetBrains Mono','Fira Code',monospace;
}
html.dark{
  --bg:#0c0f14;--surface:#111827;--surface2:#141b26;
  --border:#1e2840;--text:#e2e8f0;--fg:#e2e8f0;--muted:#64748b;
}
*{margin:0;padding:0;box-sizing:border-box;}
html,body{height:100%;font-family:var(--fh);background:var(--bg);color:var(--text);font-size:14px;}
.layout{display:flex;min-height:calc(100vh - 88px - 36px);}
.sidebar{width:210px;flex-shrink:0;background:var(--surface);border-right:1px solid var(--border);overflow-y:auto;position:sticky;top:88px;height:calc(100vh - 88px - 36px);}
html.dark .sidebar{background:#0e1117;border-right-color:#1e2840;}
.main{flex:1;padding:20px;overflow-y:auto;max-width:calc(100vw - 210px);}
header{height:52px;background:var(--surface);border-bottom:1px solid var(--border);display:flex;align-items:center;gap:14px;padding:0 20px;position:sticky;top:0;z-index:100;}
html.dark header{background:#0e1117;border-bottom-color:#1e2840;}
.header-logo{width:32px;height:32px;border-radius:50%;overflow:hidden;flex-shrink:0;}
.header-logo img{width:100%;height:100%;object-fit:cover;}
.header-title h1{font-size:.82rem;font-weight:700;}
.header-title span{font-size:.6rem;color:var(--muted);}
.hp-staff-bar{height:36px;background:linear-gradient(90deg,#1a56db,#1e40af);display:flex;align-items:center;gap:10px;padding:0 16px;font-size:.62rem;color:rgba(255,255,255,.9);position:sticky;top:52px;z-index:99;}
.hp-staff-lbl{opacity:.7;font-weight:500;}.hp-staff-name{font-weight:700;}.hp-staff-sep{opacity:.4;}
.hbtn{background:rgba(255,255,255,.15);border:none;color:#fff;padding:3px 10px;border-radius:5px;font-size:.62rem;cursor:pointer;font-family:var(--fh);}
.hbtn:hover{background:rgba(255,255,255,.28);}
.nav-section-lbl{font-size:.46rem;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:var(--muted);padding:12px 18px 4px;}
.nav-item{display:flex;align-items:center;gap:9px;padding:9px 18px;cursor:pointer;font-size:.71rem;color:var(--muted);font-weight:500;transition:all .12s;border-left:3px solid transparent;position:relative;}
.nav-item:hover{color:var(--text);background:var(--surface2);}
.nav-item.active{color:var(--accent);background:rgba(26,86,219,.06);border-left-color:var(--accent);font-weight:600;}
.nav-item svg{width:14px;height:14px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;flex-shrink:0;}
.nav-badge{position:absolute;right:12px;top:50%;transform:translateY(-50%);background:var(--red);color:#fff;border-radius:10px;font-size:.52rem;font-weight:700;padding:1px 5px;min-width:16px;text-align:center;}
.section{display:none;}.section.active{display:block;}
.page-header{margin-bottom:18px;display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:8px;}
.page-title{font-size:1.1rem;font-weight:700;}
.page-sub{font-size:.68rem;color:var(--muted);margin-top:2px;}
.card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:16px;margin-bottom:14px;}
html.dark .card{background:#111827;border-color:#1e2840;}
.card-title{font-size:.78rem;font-weight:700;margin-bottom:12px;display:flex;align-items:center;justify-content:space-between;}
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
.form-grid-3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;}
@media(max-width:700px){.form-grid,.form-grid-3{grid-template-columns:1fr;}}
.span2{grid-column:span 2;}.span3{grid-column:span 3;}
.field-group{display:flex;flex-direction:column;gap:4px;}
.field-group label{font-size:.62rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;}
input[type=text],input[type=date],input[type=number],input[type=password],input[type=time],select,textarea{
  background:var(--surface2);border:1px solid var(--border);color:var(--text);
  font-family:var(--fh);font-size:.77rem;padding:7px 11px;border-radius:7px;outline:none;width:100%;transition:border-color .13s;
}
input:focus,select:focus,textarea:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(26,86,219,.1);}
textarea{resize:vertical;min-height:60px;}
html.dark input,html.dark select,html.dark textarea{background:rgba(255,255,255,.04);border-color:rgba(255,255,255,.1);}
.req{color:var(--red);}
.btn{display:inline-flex;align-items:center;gap:6px;padding:7px 14px;border-radius:8px;font-size:.72rem;font-weight:600;cursor:pointer;border:1px solid transparent;transition:all .13s;font-family:var(--fh);}
.btn-primary{background:var(--accent);color:#fff;border-color:var(--accent);}.btn-primary:hover{opacity:.88;}
.btn-success{background:var(--green);color:#fff;border-color:var(--green);}.btn-success:hover{opacity:.88;}
.btn-danger{background:var(--red);color:#fff;border-color:var(--red);}.btn-danger:hover{opacity:.88;}
.btn-outline{background:transparent;border-color:var(--border);color:var(--text);}.btn-outline:hover{border-color:var(--accent);color:var(--accent);}
.btn-sm{padding:4px 10px;font-size:.66rem;}.btn-xs{padding:2px 7px;font-size:.6rem;}
.kpi-row{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:14px;}
.kpi-box{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:12px 16px;flex:1;min-width:110px;}
html.dark .kpi-box{background:#111827;border-color:#1e2840;}
.kpi-label{font-size:.58rem;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:4px;}
.kpi-val{font-size:1.4rem;font-weight:800;line-height:1;}
.kpi-sub{font-size:.6rem;color:var(--muted);margin-top:2px;}
.kpi-accent .kpi-val{color:var(--accent);}.kpi-green .kpi-val{color:var(--green);}
.kpi-red .kpi-val{color:var(--red);}.kpi-amber .kpi-val{color:var(--amber);}
.kpi-purple .kpi-val{color:var(--purple);}
.table-wrap{overflow-x:auto;}
table{width:100%;border-collapse:collapse;font-size:.72rem;}
th{background:var(--surface2);padding:8px 10px;text-align:left;font-size:.6rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);border-bottom:2px solid var(--border);}
td{padding:8px 10px;border-bottom:1px solid var(--border);vertical-align:middle;}
tr:last-child td{border-bottom:none;}
tr:hover td{background:var(--surface2);}
.badge{display:inline-flex;align-items:center;padding:2px 7px;border-radius:10px;font-size:.6rem;font-weight:700;letter-spacing:.04em;}
.b-int{background:rgba(26,86,219,.12);color:#1a56db;}
.b-alta{background:rgba(5,150,105,.12);color:#059669;}
.b-obit{background:rgba(220,38,38,.12);color:#dc2626;}
.b-ti{background:rgba(124,58,237,.12);color:#7c3aed;}
.b-te{background:rgba(8,145,178,.12);color:#0891b2;}
.doc-card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:12px 14px;margin-bottom:8px;display:flex;align-items:flex-start;gap:12px;}
html.dark .doc-card{background:#111827;border-color:#1e2840;}
.doc-info{flex:1;min-width:0;}
.doc-name{font-weight:700;font-size:.82rem;}
.doc-meta{font-size:.65rem;color:var(--muted);margin-top:2px;}
.doc-actions{display:flex;gap:4px;flex-shrink:0;flex-wrap:wrap;}
.filter-bar{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px;align-items:flex-end;}
.period-bar{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px;}
.pb{padding:4px 12px;border-radius:6px;border:1px solid var(--border);background:transparent;font-size:.65rem;font-weight:600;cursor:pointer;color:var(--muted);font-family:var(--fh);}
.pb.active,.pb:hover{background:var(--accent);color:#fff;border-color:var(--accent);}
.chart-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:14px;margin-bottom:14px;}
html.dark .chart-card{background:#111827;border-color:#1e2840;}
.chart-title{font-size:.74rem;font-weight:700;margin-bottom:10px;}
.chart-wrap{position:relative;height:220px;}
.no-data{text-align:center;color:var(--muted);padding:32px;font-size:.78rem;}
.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:500;display:flex;align-items:center;justify-content:center;}
.modal{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:24px;width:90%;max-height:90vh;overflow-y:auto;}
html.dark .modal{background:#111827;border-color:#1e2840;}
.modal-title{font-size:.95rem;font-weight:700;margin-bottom:4px;}
.modal-sub{font-size:.7rem;color:var(--muted);margin-bottom:16px;}
.hist-item{padding:7px 10px;border-left:3px solid var(--accent);margin-bottom:6px;background:var(--surface2);border-radius:0 6px 6px 0;font-size:.68rem;}
.hist-ts{font-size:.6rem;color:var(--muted);}
.hist-prof{font-weight:700;color:var(--accent);}
.notif-item{display:flex;align-items:flex-start;gap:10px;padding:10px;border-bottom:1px solid var(--border);}
.notif-dot{width:8px;height:8px;border-radius:50%;background:var(--accent);flex-shrink:0;margin-top:4px;}
.notif-dot.read{background:var(--border);}
/* bottom bar */
.bottom-bar{position:fixed;bottom:0;left:0;right:0;height:36px;background:linear-gradient(90deg,#0f172a,#1e293b);display:flex;align-items:center;gap:0;padding:0;font-size:.62rem;color:rgba(255,255,255,.85);z-index:200;border-top:1px solid rgba(255,255,255,.08);}
.bb-stat{padding:0 16px;border-right:1px solid rgba(255,255,255,.1);height:100%;display:flex;align-items:center;gap:6px;}
.bb-label{opacity:.6;}.bb-val{font-weight:800;font-size:.78rem;}
.bb-val.blue{color:#60a5fa;}.bb-val.green{color:#34d399;}.bb-val.red{color:#f87171;}.bb-val.amber{color:#fbbf24;}
/* ind table */
.ind-tbl td{font-size:.7rem;padding:6px 10px;}
.ind-tbl td:first-child{font-weight:600;color:var(--muted);font-size:.6rem;text-transform:uppercase;}
.ind-tbl td:last-child{font-weight:700;}
/* ficha detail */
.ficha-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;}
.ficha-row{padding:6px 10px;background:var(--surface2);border-radius:6px;font-size:.72rem;}
.ficha-lbl{font-size:.58rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:2px;}
.ficha-val{font-weight:600;}
"""

MODAL_LOGIN = """
<div id="login-modal" class="modal-overlay">
  <div class="modal" style="max-width:420px;text-align:center;">
    <div style="margin-bottom:14px;">
      <div style="width:56px;height:56px;border-radius:50%;overflow:hidden;margin:0 auto 10px;border:3px solid var(--accent);">
        <img src="__HOSP_IMG__" style="width:100%;height:100%;object-fit:cover;">
      </div>
      <div style="font-size:1rem;font-weight:800;">Hospital do Prenda</div>
      <div style="font-size:.68rem;color:var(--muted);margin-top:2px;">Serviço de Ortopedia / Medicina</div>
    </div>
    <div class="modal-title" style="font-size:.82rem;">Autenticação do Sistema</div>
    <div style="height:1px;background:var(--border);margin:10px 0 16px;"></div>
    <div class="field-group" style="margin-bottom:10px;text-align:left;">
      <label>Profissional</label>
      <select id="login-prof"></select>
    </div>
    <div class="field-group" style="margin-bottom:10px;text-align:left;">
      <label>Senha</label>
      <input type="password" id="login-senha" placeholder="Senha de acesso..."
             onkeydown="if(event.key==='Enter')doLogin()">
    </div>
    <div id="login-err" style="font-size:.7rem;color:var(--red);display:none;padding:8px 12px;background:rgba(239,68,68,.08);border-radius:7px;margin-bottom:10px;border:1px solid rgba(239,68,68,.2);text-align:left;"></div>
    <button class="btn btn-primary" style="width:100%;justify-content:center;padding:10px;" onclick="doLogin()">Entrar no Sistema</button>
    <div style="font-size:.58rem;color:var(--muted);margin-top:12px;">Acesso restrito a profissionais autorizados</div>
  </div>
</div>
"""

MODAL_SAIDA = """
<div id="modal-saida" class="modal-overlay" style="display:none;" onclick="if(event.target===this)closeModal('modal-saida')">
  <div class="modal" style="max-width:520px;">
    <div class="modal-title">Registar Saída do Doente</div>
    <div class="modal-sub" id="saida-doente-info"></div>
    <div class="form-grid">
      <div class="field-group">
        <label>Tipo de Saída <span class="req">*</span></label>
        <select id="saida-tipo" onchange="toggleSaidaTipo()">
          <option>Alta</option>
          <option>Obito</option>
          <option>Transferencia Interna</option>
          <option>Transferencia Externa</option>
        </select>
      </div>
      <div class="field-group">
        <label>Data de Saída <span class="req">*</span></label>
        <input type="date" id="saida-data">
      </div>
      <div class="field-group">
        <label>Hora de Saída <span class="req">*</span></label>
        <input type="time" id="saida-hora">
      </div>
      <div class="field-group" id="saida-destino-f">
        <label>Destino / Unidade</label>
        <input type="text" id="saida-destino" placeholder="Ex: Cirurgia, Hospital Central...">
      </div>
      <div class="field-group span2">
        <label>Observações / Motivo</label>
        <textarea id="saida-obs" rows="2" placeholder="Observações sobre a saída..."></textarea>
      </div>
    </div>
    <div style="margin-top:14px;display:flex;gap:8px;justify-content:flex-end;">
      <button class="btn btn-outline btn-sm" onclick="closeModal('modal-saida')">Cancelar</button>
      <button class="btn btn-success btn-sm" onclick="confirmarSaida()">Confirmar Saída</button>
    </div>
  </div>
</div>
"""

MODAL_FICHA = """
<div id="modal-ficha" class="modal-overlay" style="display:none;" onclick="if(event.target===this)closeModal('modal-ficha')">
  <div class="modal" style="max-width:700px;">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
      <div>
        <div class="modal-title" id="ficha-num" style="margin-bottom:0;"></div>
        <div class="modal-sub" style="margin-bottom:0;" id="ficha-status"></div>
      </div>
      <div style="display:flex;gap:6px;">
        <button class="btn btn-outline btn-sm" onclick="exportarFichaPDF()">PDF</button>
        <button class="btn btn-primary btn-sm" onclick="abrirEditarDoente()">Editar</button>
        <button class="btn btn-outline btn-sm" onclick="closeModal('modal-ficha')">✕</button>
      </div>
    </div>
    <div id="ficha-body"></div>
    <div style="margin-top:14px;">
      <div style="font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:8px;">Histórico de Alterações</div>
      <div id="ficha-hist" style="max-height:200px;overflow-y:auto;"></div>
    </div>
  </div>
</div>
"""

MODAL_EDIT = """
<div id="modal-edit" class="modal-overlay" style="display:none;" onclick="if(event.target===this)closeModal('modal-edit')">
  <div class="modal" style="max-width:620px;">
    <div class="modal-title">Editar Dados do Doente</div>
    <div class="modal-sub" id="edit-doente-info"></div>
    <div class="form-grid">
      <div class="field-group"><label>Nome Completo <span class="req">*</span></label><input type="text" id="e-nome"></div>
      <div class="field-group"><label>NUP <span class="req">*</span></label><input type="text" id="e-nup" placeholder="Número Único do Paciente"></div>
      <div class="field-group"><label>BI / Passaporte</label><input type="text" id="e-bi"></div>
      <div class="field-group"><label>Sexo <span class="req">*</span></label>
        <select id="e-sexo"><option value="M">Masculino</option><option value="F">Feminino</option></select>
      </div>
      <div class="field-group"><label>Data de Nascimento</label><input type="date" id="e-dnasc" onchange="calcIdadeEdit()"></div>
      <div class="field-group"><label>Idade (se sem data)</label><input type="text" id="e-idade-manual" placeholder="Ex: 45 anos"></div>
      <div class="field-group"><label>Data de Admissão <span class="req">*</span></label><input type="date" id="e-dadm"></div>
      <div class="field-group"><label>Hora de Admissão <span class="req">*</span></label><input type="time" id="e-hadm"></div>
      <div class="field-group"><label>Tipo de Admissão <span class="req">*</span></label>
        <select id="e-tadm">
          <option>Urgencia</option><option>Programada</option>
          <option>Transferencia Interna</option><option>Transferencia Externa</option>
        </select>
      </div>
      <div class="field-group"><label>Cama <span class="req">*</span></label><input type="text" id="e-cama"></div>
      <div class="field-group span2"><label>Diagnóstico Principal <span class="req">*</span></label><input type="text" id="e-diag"></div>
      <div class="field-group"><label>Médico Responsável</label><input type="text" id="e-med"></div>
      <div class="field-group span2"><label>Observações</label><textarea id="e-obs" rows="2"></textarea></div>
    </div>
    <div style="margin-top:14px;display:flex;gap:8px;justify-content:flex-end;">
      <button class="btn btn-outline btn-sm" onclick="closeModal('modal-edit')">Cancelar</button>
      <button class="btn btn-primary btn-sm" onclick="salvarEdicao()">Guardar Alterações</button>
    </div>
  </div>
</div>
"""

MODAL_DEL = """
<div id="modal-del" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:800;display:none;align-items:center;justify-content:center;" onclick="if(event.target===this)closeModal('modal-del')">
  <div style="background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:28px 32px;max-width:360px;width:90%;text-align:center;">
    <div style="font-size:2rem;margin-bottom:10px;">⚠️</div>
    <div style="font-weight:700;font-size:.95rem;margin-bottom:6px;">Eliminar Registo</div>
    <div style="font-size:.75rem;color:var(--muted);margin-bottom:20px;">Esta ação é irreversível. Confirmas a eliminação?</div>
    <div style="display:flex;gap:10px;justify-content:center;">
      <button class="btn btn-outline btn-sm" onclick="closeModal('modal-del')">Cancelar</button>
      <button class="btn btn-danger btn-sm" onclick="confirmDel()">Eliminar</button>
    </div>
  </div>
</div>
"""

SEC_REGISTO = """
<section id="sec-registo" class="section active">
  <div class="page-header">
    <div><div class="page-title">Registo de Doente</div><div class="page-sub">Internamento — Serviço de Ortopedia / Medicina</div></div>
    <span id="r-num-preview" style="font-family:var(--fm);font-size:.78rem;color:var(--accent);font-weight:700;"></span>
  </div>
  <div class="card">
    <div class="card-title">Dados de Internamento</div>
    <div class="form-grid">
      <div class="field-group">
        <label>Nome Completo <span class="req">*</span></label>
        <input type="text" id="r-nome" placeholder="Nome completo do doente...">
      </div>
      <div class="field-group">
        <label>NUP — Número Único do Paciente <span class="req">*</span></label>
        <input type="text" id="r-nup" placeholder="Ex: ANG-2024-00123">
      </div>
      <div class="field-group">
        <label>BI / Passaporte</label>
        <input type="text" id="r-bi" placeholder="Opcional">
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
        <label>Data de Nascimento</label>
        <input type="date" id="r-dnasc" onchange="calcIdadeRegisto()">
      </div>
      <div class="field-group">
        <label>Idade (se sem data de nasc.)</label>
        <input type="text" id="r-idade-manual" placeholder="Ex: 45 anos" id="r-idade-manual">
      </div>
      <div class="field-group">
        <label>Data de Admissão <span class="req">*</span></label>
        <input type="date" id="r-dadm">
      </div>
      <div class="field-group">
        <label>Hora de Admissão <span class="req">*</span></label>
        <input type="time" id="r-hadm">
      </div>
      <div class="field-group">
        <label>Tipo de Admissão <span class="req">*</span></label>
        <select id="r-tadm">
          <option value="">Seleccionar...</option>
          <option>Urgencia</option>
          <option>Programada</option>
          <option>Transferencia Interna</option>
          <option>Transferencia Externa</option>
        </select>
      </div>
      <div class="field-group">
        <label>N.º Cama <span class="req">*</span></label>
        <input type="text" id="r-cama" placeholder="Ex: 01, 02A...">
      </div>
      <div class="field-group span2">
        <label>Diagnóstico Principal <span class="req">*</span></label>
        <input type="text" id="r-diag" placeholder="Ex: Fractura do fémur, Artroplastia do joelho...">
      </div>
      <div class="field-group">
        <label>Médico Responsável</label>
        <input type="text" id="r-med" placeholder="Nome do médico...">
      </div>
      <div class="field-group span2">
        <label>Observações</label>
        <textarea id="r-obs" rows="2" placeholder="Observações adicionais..."></textarea>
      </div>
    </div>
    <div style="margin-top:14px;display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
      <button class="btn btn-primary" onclick="registarDoente()">Registar Internamento</button>
      <button class="btn btn-outline" onclick="limparRegisto()">Limpar Formulário</button>
    </div>
  </div>
</section>"""

SEC_INTERNADOS = """
<section id="sec-internados" class="section">
  <div class="page-header">
    <div><div class="page-title">Doentes Internados</div><div class="page-sub">Lista de doentes em internamento activo</div></div>
    <button class="btn btn-outline btn-sm" onclick="exportIntPDF()">Exportar PDF</button>
  </div>
  <div id="int-kpis" class="kpi-row"></div>
  <div class="card">
    <div class="filter-bar">
      <div class="field-group" style="flex:1;min-width:180px;">
        <label>Pesquisar</label>
        <input type="text" id="int-search" placeholder="Nome, NUP, diagnóstico, cama..." onkeyup="renderInternados()">
      </div>
      <div class="field-group" style="min-width:140px;">
        <label>Tipo Admissão</label>
        <select id="int-tadm-f" onchange="renderInternados()">
          <option value="">Todos</option>
          <option>Urgencia</option><option>Programada</option>
          <option>Transferencia Interna</option><option>Transferencia Externa</option>
        </select>
      </div>
    </div>
    <div id="internados-list"></div>
  </div>
</section>"""

SEC_SAIDAS = """
<section id="sec-saidas" class="section">
  <div class="page-header">
    <div><div class="page-title">Saídas</div><div class="page-sub">Doentes com alta, óbito ou transferência</div></div>
    <button class="btn btn-outline btn-sm" onclick="exportSaidasPDF()">Exportar PDF</button>
  </div>
  <div id="saidas-kpis" class="kpi-row"></div>
  <div class="card">
    <div class="filter-bar" style="flex-wrap:wrap;gap:8px;">
      <div class="field-group" style="min-width:140px;"><label>De</label><input type="date" id="saidas-from" onchange="renderSaidas()"></div>
      <div class="field-group" style="min-width:140px;"><label>Até</label><input type="date" id="saidas-to" onchange="renderSaidas()"></div>
      <div class="field-group" style="min-width:130px;">
        <label>Tipo</label>
        <select id="saidas-tipo-f" onchange="renderSaidas()">
          <option value="">Todos</option>
          <option>Alta</option><option>Obito</option>
          <option>Transferencia Interna</option><option>Transferencia Externa</option>
        </select>
      </div>
      <div class="field-group" style="flex:1;min-width:160px;">
        <label>Pesquisar</label>
        <input type="text" id="saidas-search" placeholder="Nome, NUP..." onkeyup="renderSaidas()">
      </div>
    </div>
    <div id="saidas-list"></div>
  </div>
</section>"""

SEC_MOVIMENTO = """
<section id="sec-movimento" class="section">
  <div class="page-header">
    <div><div class="page-title">Movimento Hospitalar</div><div class="page-sub">Registo diário de entradas e saídas</div></div>
    <button class="btn btn-outline btn-sm" onclick="exportMovPDF()">Exportar PDF</button>
  </div>
  <div class="card">
    <div class="card-title">Período</div>
    <div class="period-bar">
      <button class="pb active" onclick="setMovPeriod('hoje',this)">Hoje</button>
      <button class="pb" onclick="setMovPeriod('semana',this)">Semana</button>
      <button class="pb" onclick="setMovPeriod('mes',this)">Mês</button>
      <button class="pb" onclick="setMovPeriod('custom',this)">Personalizado</button>
    </div>
    <div id="mov-custom" style="display:none;display:flex;gap:8px;flex-wrap:wrap;margin-top:6px;">
      <div class="field-group" style="min-width:140px;"><label>De</label><input type="date" id="mov-from" onchange="renderMovimento()"></div>
      <div class="field-group" style="min-width:140px;"><label>Até</label><input type="date" id="mov-to" onchange="renderMovimento()"></div>
    </div>
  </div>
  <div id="mov-kpis" class="kpi-row"></div>
  <div class="card">
    <div class="card-title">Entradas no Período</div>
    <div id="mov-entradas-list"></div>
  </div>
  <div class="card">
    <div class="card-title">Saídas no Período</div>
    <div id="mov-saidas-list"></div>
  </div>
</section>"""

SEC_INDICADORES = """
<section id="sec-indicadores" class="section">
  <div class="page-header">
    <div><div class="page-title">Indicadores Hospitalares</div><div class="page-sub">Taxas e métricas do Serviço de Ortopedia/Medicina</div></div>
  </div>
  <div class="card">
    <div class="period-bar">
      <button class="pb active" data-p="mes" onclick="setIndPeriod('mes')">Mês</button>
      <button class="pb" data-p="semana" onclick="setIndPeriod('semana')">Semana</button>
      <button class="pb" data-p="trimestre" onclick="setIndPeriod('trimestre')">Trimestre</button>
      <button class="pb" data-p="semestre" onclick="setIndPeriod('semestre')">Semestre</button>
      <button class="pb" data-p="ano" onclick="setIndPeriod('ano')">Ano</button>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:flex-end;">
      <div class="field-group" style="min-width:140px;"><label>Início</label><input type="date" id="ind-from" onchange="renderIndicadores()"></div>
      <div class="field-group" style="min-width:140px;"><label>Fim</label><input type="date" id="ind-to" onchange="renderIndicadores()"></div>
      <div class="field-group" style="min-width:80px;"><label>N.º Camas</label><input type="number" id="ind-ncamas" min="1" placeholder="30" onchange="renderIndicadores()"></div>
    </div>
    <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:10px;">
      <span style="font-size:.65rem;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.06em;align-self:center;">PDF:</span>
      <button class="btn btn-outline btn-xs" onclick="exportIndPDF('semana')">Semanal</button>
      <button class="btn btn-outline btn-xs" onclick="exportIndPDF('mes')">Mensal</button>
      <button class="btn btn-outline btn-xs" onclick="exportIndPDF('trimestre')">Trimestral</button>
      <button class="btn btn-outline btn-xs" onclick="exportIndPDF('semestre')">Semestral</button>
      <button class="btn btn-outline btn-xs" onclick="exportIndPDF('ano')">Anual</button>
      <button class="btn btn-outline btn-xs" onclick="exportIndPDF('custom')">Período Actual</button>
    </div>
  </div>
  <div class="kpi-row" id="ind-kpis"></div>
  <div class="card">
    <div class="card-title">Tabela de Indicadores</div>
    <div id="ind-table-wrap"></div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
    <div class="chart-card"><div class="chart-title">Entradas vs Saídas</div><div class="chart-wrap"><canvas id="ind-chart-mov"></canvas></div></div>
    <div class="chart-card"><div class="chart-title">Tipo de Saída</div><div class="chart-wrap"><canvas id="ind-chart-tipo"></canvas></div></div>
  </div>
  <div class="chart-card"><div class="chart-title">Evolução da Taxa de Ocupação</div><div class="chart-wrap" style="height:180px;"><canvas id="ind-chart-ocup"></canvas></div></div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
    <div class="chart-card"><div class="chart-title">Tipo de Admissão</div><div class="chart-wrap"><canvas id="ind-chart-tadm"></canvas></div></div>
    <div class="chart-card"><div class="chart-title">Tendência Semanal (Entradas)</div><div class="chart-wrap"><canvas id="ind-chart-trend"></canvas></div></div>
  </div>
</section>"""

SEC_DIAGNOSTICOS = """
<section id="sec-diagnosticos" class="section">
  <div class="page-header">
    <div><div class="page-title">Diagnósticos</div><div class="page-sub">Análise por patologia e diagnóstico</div></div>
  </div>
  <div class="card">
    <div class="filter-bar">
      <div class="field-group" style="min-width:130px;">
        <label>Estado</label>
        <select id="diag-estado-f" onchange="renderDiagnosticos()">
          <option value="">Todos</option>
          <option value="internado">Internados</option>
          <option value="saido">Com Saída</option>
        </select>
      </div>
    </div>
    <div id="diag-list"></div>
  </div>
  <div class="chart-card">
    <div class="chart-title">Top Diagnósticos</div>
    <div class="chart-wrap"><canvas id="diag-chart"></canvas></div>
  </div>
</section>"""

SEC_PESQUISA = """
<section id="sec-pesquisa" class="section">
  <div class="page-header">
    <div><div class="page-title">Pesquisa</div><div class="page-sub">Pesquisa avançada de doentes</div></div>
  </div>
  <div class="card">
    <div class="form-grid">
      <div class="field-group span2">
        <label>Pesquisar (Nome, NUP, BI, Diagnóstico)</label>
        <input type="text" id="pq-q" placeholder="Digite para pesquisar..." onkeyup="renderPesquisa()">
      </div>
      <div class="field-group"><label>Estado</label>
        <select id="pq-status" onchange="renderPesquisa()">
          <option value="">Todos</option>
          <option value="internado">Internado</option>
          <option value="alta">Alta</option>
          <option value="obito">Óbito</option>
          <option value="transferencia_interna">Transf. Interna</option>
          <option value="transferencia_externa">Transf. Externa</option>
        </select>
      </div>
      <div class="field-group"><label>Sexo</label>
        <select id="pq-sexo" onchange="renderPesquisa()">
          <option value="">Todos</option>
          <option value="M">Masculino</option>
          <option value="F">Feminino</option>
        </select>
      </div>
      <div class="field-group"><label>Admissão De</label><input type="date" id="pq-from" onchange="renderPesquisa()"></div>
      <div class="field-group"><label>Admissão Até</label><input type="date" id="pq-to" onchange="renderPesquisa()"></div>
    </div>
  </div>
  <div id="pq-results"></div>
</section>"""

SEC_DEFINICOES = """
<section id="sec-definicoes" class="section">
  <div class="page-header">
    <div><div class="page-title">Definições</div><div class="page-sub">Configuração completa do sistema</div></div>
  </div>
  <div class="card">
    <div class="card-title">Informações do Serviço</div>
    <div class="form-grid">
      <div class="field-group"><label>Nome do Serviço</label><input type="text" id="def-servico" placeholder="Ex: Ortopedia/Medicina"></div>
      <div class="field-group"><label>N.º de Camas</label><input type="number" id="def-ncamas" min="1" placeholder="30"></div>
      <div class="field-group"><label>Número Processo Actual</label><input type="number" id="def-numAtual" min="1"></div>
      <div class="field-group"><label>Ano</label><input type="number" id="def-ano" min="2020"></div>
      <div class="field-group"><label>Senha do Chefe</label><input type="password" id="def-senhachefe" placeholder="Nova senha do chefe..."></div>
      <div class="field-group" style="align-self:flex-end;">
        <button class="btn btn-primary" onclick="salvarConfigServico()">Guardar Configuração</button>
      </div>
    </div>
  </div>
  <div class="card">
    <div class="card-title">Profissionais
      <button class="btn btn-outline btn-xs" onclick="addProfissional()">+ Adicionar</button>
    </div>
    <div id="def-profs"></div>
  </div>
  <div class="card">
    <div class="card-title">Dados e Backup</div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;">
      <button class="btn btn-outline btn-sm" onclick="downloadBackup()">Descarregar Backup JSON</button>
      <button class="btn btn-outline btn-sm" onclick="importarBackup()">Importar Backup</button>
      <button class="btn btn-outline btn-sm" onclick="exportIndPDF('mes')">PDF Mensal</button>
      <button class="btn btn-outline btn-sm" onclick="exportIndPDF('ano')">PDF Anual</button>
    </div>
    <input type="file" id="import-file" accept=".json" style="display:none" onchange="processarBackup(event)">
    <div id="def-backup-info" style="margin-top:10px;font-size:.7rem;color:var(--muted);"></div>
  </div>
  <div class="card">
    <div class="card-title">Notificações de Saída</div>
    <div id="def-notifs" style="max-height:300px;overflow-y:auto;"></div>
    <button class="btn btn-outline btn-sm" style="margin-top:8px;" onclick="limparNotifs()">Limpar Todas</button>
  </div>
</section>"""

JS = r"""
// ═══ CONSTANTES ═══
var DOCS_KEY='hp_orto_docs', CFG_KEY='hp_orto_cfg', NOTIF_KEY='hp_orto_notifs';
var currentProfissional='', indPeriod='mes', fichaCurId=null, delTargetId=null, saidaTargetId=null;
var ortoCharts={}, movPeriod='hoje';

// ─── MIGRAÇÃO ───
(function(){
  var raw=localStorage.getItem('hp_orto_cfg');
  if(raw){
    try{
      var c=JSON.parse(raw);var ch=false;
      if(!c.profissionais||!c.profissionais.length){c.profissionais=[{id:'admin',nome:'Administrador',senha:'1234'}];ch=true;}
      if(!c.senhaChefe){c.senhaChefe='1234';ch=true;}
      if(!c.numCamas){c.numCamas=30;ch=true;}
      if(!c.servico){c.servico='Ortopedia/Medicina';ch=true;}
      if(ch)localStorage.setItem('hp_orto_cfg',JSON.stringify(c));
    }catch(e){localStorage.removeItem('hp_orto_cfg');}
  }
})();

// ═══ UTILS ═══
function uid(){return Date.now().toString(36)+Math.random().toString(36).slice(2,7);}
function todayKey(){return new Date().toISOString().slice(0,10);}
function fmtDate(d){if(!d)return '---';var p=d.split('-');return p[2]+'/'+p[1]+'/'+p[0];}
function fmtTime(){var n=new Date();return String(n.getHours()).padStart(2,'0')+':'+String(n.getMinutes()).padStart(2,'0');}
function fmtNum(n,y){return 'ORT/'+(y||new Date().getFullYear())+'/'+String(n).padStart(3,'0');}
function daysBetween(d1,d2){var a=new Date(d1),b=new Date(d2);return Math.max(0,Math.round((b-a)/86400000));}
function calcIdadeFromDnasc(dnasc){if(!dnasc)return null;return Math.floor((new Date()-new Date(dnasc))/31557600000);}
function statusBadge(s){
  var map={internado:'b-int',alta:'b-alta',obito:'b-obit',transferencia_interna:'b-ti',transferencia_externa:'b-te'};
  var labels={internado:'Internado',alta:'Alta',obito:'Óbito',transferencia_interna:'Transf. Interna',transferencia_externa:'Transf. Externa'};
  return '<span class="badge '+(map[s]||'')+'">'+(labels[s]||s)+'</span>';
}
function statusKey(tipo){
  if(!tipo)return 'internado';
  if(tipo==='Alta')return 'alta';
  if(tipo==='Obito')return 'obito';
  if(tipo==='Transferencia Interna')return 'transferencia_interna';
  if(tipo==='Transferencia Externa')return 'transferencia_externa';
  return 'internado';
}
function toast(msg,type){
  var t=document.getElementById('toast');if(!t)return;
  t.textContent=msg;
  t.style.background=type==='err'?'#dc2626':type==='info'?'#1a56db':'#059669';
  t.style.color='#fff';t.style.display='block';t.style.opacity='1';t.style.transform='translateY(0)';
  setTimeout(function(){t.style.opacity='0';t.style.transform='translateY(20px)';setTimeout(function(){t.style.display='none';},350);},3500);
}
function closeModal(id){var m=document.getElementById(id);if(m)m.style.display='none';}
function openModal(id){var m=document.getElementById(id);if(m)m.style.display='flex';}

// ═══ DATA ═══
function getConfig(){
  var def={numAtual:1,ano:new Date().getFullYear(),numCamas:30,servico:'Ortopedia/Medicina',
    profissionais:[{id:'admin',nome:'Administrador',senha:'1234'}],senhaChefe:'1234'};
  var r=localStorage.getItem(CFG_KEY);if(!r)return def;
  try{
    var c=JSON.parse(r);
    if(!c.profissionais||!c.profissionais.length)c.profissionais=def.profissionais;
    if(!c.senhaChefe)c.senhaChefe=def.senhaChefe;
    if(!c.numCamas)c.numCamas=def.numCamas;
    if(!c.servico)c.servico=def.servico;
    if(!c.numAtual)c.numAtual=def.numAtual;
    if(!c.ano)c.ano=def.ano;
    return c;
  }catch(e){return def;}
}
function saveConfig(c){localStorage.setItem(CFG_KEY,JSON.stringify(c));}
function getDoentes(){var r=localStorage.getItem(DOCS_KEY);return r?JSON.parse(r):[];}
function saveDoentes(d){localStorage.setItem(DOCS_KEY,JSON.stringify(d));}
function getNotifs(){var r=localStorage.getItem(NOTIF_KEY);return r?JSON.parse(r):[];}
function saveNotifs(n){localStorage.setItem(NOTIF_KEY,JSON.stringify(n));}
function nextNum(){var c=getConfig();var n=c.numAtual;c.numAtual=n+1;saveConfig(c);return n;}

function addNotif(doente, tipo){
  var notifs=getNotifs();
  notifs.unshift({id:uid(),ts:new Date().toISOString(),doente:doente.nome,numStr:doente.numStr,
    tipo:tipo,profissional:currentProfissional,lida:false});
  saveNotifs(notifs);updateNotifBadge();
}
function updateNotifBadge(){
  var notifs=getNotifs();var unread=notifs.filter(function(n){return !n.lida;}).length;
  var b=document.getElementById('notif-badge');
  if(b){b.textContent=unread;b.style.display=unread?'':'none';}
}

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
  if(!prof||prof.senha!==senha){
    errEl.style.display='block';errEl.textContent='Credenciais incorrectas. Verifique o profissional e a senha.';
    document.getElementById('login-senha').value='';document.getElementById('login-senha').focus();return;
  }
  currentProfissional=prof.nome;sessionStorage.setItem('hp_orto_prof',prof.nome);
  closeModal('login-modal');
  document.getElementById('staff-name').textContent=prof.nome;
  toast('Bem-vindo(a), '+prof.nome+'!','info');
  updateNumPreview();updateBottomBar();updateNotifBadge();
  renderInternados();
}
function doLogout(){sessionStorage.removeItem('hp_orto_prof');currentProfissional='';location.reload();}
function checkSession(){
  var p=sessionStorage.getItem('hp_orto_prof');
  if(p){
    currentProfissional=p;document.getElementById('staff-name').textContent=p;
    closeModal('login-modal');updateNumPreview();updateBottomBar();updateNotifBadge();
    renderInternados();
  }else{initLoginModal();}
}

// ═══ NAVEGAÇÃO ═══
function nav(id){
  document.querySelectorAll('.section').forEach(function(s){s.classList.remove('active');});
  document.querySelectorAll('.nav-item').forEach(function(n){n.classList.remove('active');});
  var sec=document.getElementById('sec-'+id);if(sec)sec.classList.add('active');
  var ni=document.querySelector('.nav-item[data-s="'+id+'"]');if(ni)ni.classList.add('active');
  if(id==='internados')renderInternados();
  if(id==='saidas')renderSaidas();
  if(id==='movimento')renderMovimento();
  if(id==='indicadores')renderIndicadores();
  if(id==='diagnosticos')renderDiagnosticos();
  if(id==='pesquisa')renderPesquisa();
  if(id==='definicoes')renderDefinicoes();
}

// ═══ REGISTO ═══
function updateNumPreview(){
  var cfg=getConfig();var el=document.getElementById('r-num-preview');
  if(el)el.textContent='Próximo: '+fmtNum(cfg.numAtual,cfg.ano);
}
function calcIdadeRegisto(){
  var d=(document.getElementById('r-dnasc')||{}).value;
  if(d){var im=document.getElementById('r-idade-manual');if(im){var a=calcIdadeFromDnasc(d);im.value=a+' anos';}}
}
function registarDoente(){
  if(!currentProfissional){toast('Faça login primeiro','err');return;}
  var nome=((document.getElementById('r-nome')||{}).value||'').trim();
  var nup=((document.getElementById('r-nup')||{}).value||'').trim();
  var bi=((document.getElementById('r-bi')||{}).value||'').trim();
  var dnasc=(document.getElementById('r-dnasc')||{}).value||'';
  var idadeManual=((document.getElementById('r-idade-manual')||{}).value||'').trim();
  var sexo=(document.getElementById('r-sexo')||{}).value||'';
  var dadm=(document.getElementById('r-dadm')||{}).value||'';
  var hadm=(document.getElementById('r-hadm')||{}).value||'';
  var tadm=(document.getElementById('r-tadm')||{}).value||'';
  var cama=((document.getElementById('r-cama')||{}).value||'').trim();
  var diag=((document.getElementById('r-diag')||{}).value||'').trim();
  if(!nome||!nup||!sexo||!dadm||!hadm||!tadm||!cama||!diag){
    toast('Preencha todos os campos obrigatórios (*)','err');return;
  }
  if(!dnasc&&!idadeManual){toast('Indique a data de nascimento ou a idade','err');return;}
  var cfg=getConfig();var num=nextNum();var ano=cfg.ano;
  var idadeCalc=dnasc?calcIdadeFromDnasc(dnasc):null;
  var doente={
    id:uid(),numProcesso:num,ano:ano,numStr:fmtNum(num,ano),
    nup:nup,nome:nome,bi:bi,
    dataNascimento:dnasc,idadeManual:idadeManual,
    idade:idadeCalc!==null?idadeCalc:idadeManual,
    sexo:sexo,dataAdmissao:dadm,horaAdmissao:hadm,tipoAdmissao:tadm,
    diagnostico:diag,cama:cama,
    medico:((document.getElementById('r-med')||{}).value||'').trim(),
    obs:((document.getElementById('r-obs')||{}).value||'').trim(),
    status:'internado',saida:null,
    profissional:currentProfissional,registadoEm:new Date().toISOString(),
    historico:[{ts:new Date().toISOString(),profissional:currentProfissional,acao:'Internamento registado',campos:'Registo inicial'}]
  };
  var docs=getDoentes();docs.unshift(doente);saveDoentes(docs);
  limparRegisto();updateNumPreview();updateBottomBar();
  toast('Internamento registado — '+doente.numStr);
}
function limparRegisto(){
  ['r-nome','r-nup','r-bi','r-idade-manual','r-cama','r-med','r-obs'].forEach(function(id){var el=document.getElementById(id);if(el)el.value='';});
  var dnasc=document.getElementById('r-dnasc');if(dnasc)dnasc.value='';
  var dadm=document.getElementById('r-dadm');if(dadm)dadm.value=todayKey();
  var hadm=document.getElementById('r-hadm');if(hadm)hadm.value=fmtTime();
  var sexo=document.getElementById('r-sexo');if(sexo)sexo.value='';
  var tadm=document.getElementById('r-tadm');if(tadm)tadm.value='';
}

// ═══ FICHA DO DOENTE ═══
function openFicha(id){
  fichaCurId=id;
  var d=getDoentes().find(function(x){return x.id===id;});if(!d)return;
  document.getElementById('ficha-num').textContent=d.numStr+' — '+d.nome;
  document.getElementById('ficha-status').textContent='Estado: '+(d.status==='internado'?'Internado':d.saida?d.saida.tipo:'---');
  var dias=d.saida?d.saida.diasInternamento:daysBetween(d.dataAdmissao,todayKey());
  var idadeStr=d.dataNascimento?calcIdadeFromDnasc(d.dataNascimento)+' anos':(d.idadeManual||'---');
  document.getElementById('ficha-body').innerHTML=
    '<div class="ficha-grid">'
    +'<div class="ficha-row"><div class="ficha-lbl">NUP</div><div class="ficha-val">'+d.nup+'</div></div>'
    +'<div class="ficha-row"><div class="ficha-lbl">N.º Processo</div><div class="ficha-val">'+d.numStr+'</div></div>'
    +'<div class="ficha-row"><div class="ficha-lbl">BI / Passaporte</div><div class="ficha-val">'+(d.bi||'---')+'</div></div>'
    +'<div class="ficha-row"><div class="ficha-lbl">Sexo</div><div class="ficha-val">'+(d.sexo==='M'?'Masculino':'Feminino')+'</div></div>'
    +'<div class="ficha-row"><div class="ficha-lbl">Data de Nascimento</div><div class="ficha-val">'+(d.dataNascimento?fmtDate(d.dataNascimento):(d.idadeManual||'---'))+'</div></div>'
    +'<div class="ficha-row"><div class="ficha-lbl">Idade</div><div class="ficha-val">'+idadeStr+'</div></div>'
    +'<div class="ficha-row"><div class="ficha-lbl">Data de Admissão</div><div class="ficha-val">'+fmtDate(d.dataAdmissao)+' '+d.horaAdmissao+'</div></div>'
    +'<div class="ficha-row"><div class="ficha-lbl">Tipo de Admissão</div><div class="ficha-val">'+d.tipoAdmissao+'</div></div>'
    +'<div class="ficha-row"><div class="ficha-lbl">Cama</div><div class="ficha-val">'+d.cama+'</div></div>'
    +'<div class="ficha-row"><div class="ficha-lbl">Dias Internamento</div><div class="ficha-val">'+dias+' dia(s)</div></div>'
    +'<div class="ficha-row" style="grid-column:span 2"><div class="ficha-lbl">Diagnóstico</div><div class="ficha-val">'+d.diagnostico+'</div></div>'
    +'<div class="ficha-row"><div class="ficha-lbl">Médico</div><div class="ficha-val">'+(d.medico||'---')+'</div></div>'
    +'<div class="ficha-row"><div class="ficha-lbl">Estado</div><div class="ficha-val">'+statusBadge(d.status)+'</div></div>'
    +(d.saida?'<div class="ficha-row"><div class="ficha-lbl">Data de Saída</div><div class="ficha-val">'+fmtDate(d.saida.data)+' '+d.saida.hora+'</div></div>'
      +'<div class="ficha-row"><div class="ficha-lbl">Destino</div><div class="ficha-val">'+(d.saida.destino||'---')+'</div></div>'
      +'<div class="ficha-row" style="grid-column:span 2"><div class="ficha-lbl">Obs. Saída</div><div class="ficha-val">'+(d.saida.obs||'---')+'</div></div>':'')
    +(d.obs?'<div class="ficha-row" style="grid-column:span 2"><div class="ficha-lbl">Observações</div><div class="ficha-val">'+d.obs+'</div></div>':'')
    +'</div>';
  var hist=d.historico||[];
  document.getElementById('ficha-hist').innerHTML=hist.length?hist.map(function(h){
    return '<div class="hist-item"><div><span class="hist-prof">'+h.profissional+'</span> — '+h.acao
      +(h.campos?'<br><span style="color:var(--muted);font-size:.6rem;">'+h.campos+'</span>':'')
      +'</div><div class="hist-ts">'+new Date(h.ts).toLocaleString('pt-AO')+'</div></div>';
  }).join(''):'<div class="no-data" style="padding:12px;">Sem histórico.</div>';
  openModal('modal-ficha');
}
function abrirEditarDoente(){
  var d=getDoentes().find(function(x){return x.id===fichaCurId;});if(!d)return;
  document.getElementById('edit-doente-info').textContent=d.numStr+' — '+d.nome;
  document.getElementById('e-nome').value=d.nome||'';
  document.getElementById('e-nup').value=d.nup||'';
  document.getElementById('e-bi').value=d.bi||'';
  document.getElementById('e-sexo').value=d.sexo||'M';
  document.getElementById('e-dnasc').value=d.dataNascimento||'';
  document.getElementById('e-idade-manual').value=d.idadeManual||'';
  document.getElementById('e-dadm').value=d.dataAdmissao||'';
  document.getElementById('e-hadm').value=d.horaAdmissao||'';
  document.getElementById('e-tadm').value=d.tipoAdmissao||'';
  document.getElementById('e-cama').value=d.cama||'';
  document.getElementById('e-diag').value=d.diagnostico||'';
  document.getElementById('e-med').value=d.medico||'';
  document.getElementById('e-obs').value=d.obs||'';
  openModal('modal-edit');
}
function calcIdadeEdit(){
  var d=(document.getElementById('e-dnasc')||{}).value;
  if(d){var im=document.getElementById('e-idade-manual');if(im)im.value=calcIdadeFromDnasc(d)+' anos';}
}
function salvarEdicao(){
  if(!currentProfissional){toast('Faça login primeiro','err');return;}
  var nome=(document.getElementById('e-nome').value||'').trim();
  var nup=(document.getElementById('e-nup').value||'').trim();
  var sexo=document.getElementById('e-sexo').value;
  var dadm=document.getElementById('e-dadm').value;
  var hadm=document.getElementById('e-hadm').value;
  var tadm=document.getElementById('e-tadm').value;
  var cama=(document.getElementById('e-cama').value||'').trim();
  var diag=(document.getElementById('e-diag').value||'').trim();
  if(!nome||!nup||!sexo||!dadm||!hadm||!tadm||!cama||!diag){
    toast('Preencha todos os campos obrigatórios','err');return;
  }
  var docs=getDoentes();var idx=docs.findIndex(function(x){return x.id===fichaCurId;});if(idx<0)return;
  var old=docs[idx];
  var campos=[];
  if(old.nome!==nome)campos.push('Nome: '+old.nome+' → '+nome);
  if(old.nup!==nup)campos.push('NUP: '+old.nup+' → '+nup);
  if(old.cama!==cama)campos.push('Cama: '+old.cama+' → '+cama);
  if(old.diagnostico!==diag)campos.push('Diagnóstico: '+old.diagnostico+' → '+diag);
  if(old.tipoAdmissao!==tadm)campos.push('Tipo Adm.: '+old.tipoAdmissao+' → '+tadm);
  var dnasc=document.getElementById('e-dnasc').value;
  var idadeManual=(document.getElementById('e-idade-manual').value||'').trim();
  docs[idx]=Object.assign({},old,{
    nome:nome,nup:nup,bi:(document.getElementById('e-bi').value||'').trim(),
    sexo:sexo,dataNascimento:dnasc,idadeManual:idadeManual,
    idade:dnasc?calcIdadeFromDnasc(dnasc):idadeManual,
    dataAdmissao:dadm,horaAdmissao:hadm,tipoAdmissao:tadm,
    cama:cama,diagnostico:diag,
    medico:(document.getElementById('e-med').value||'').trim(),
    obs:(document.getElementById('e-obs').value||'').trim(),
    historico:(old.historico||[]).concat([{
      ts:new Date().toISOString(),profissional:currentProfissional,
      acao:'Dados editados',campos:campos.length?campos.join('; '):'Sem alterações relevantes'
    }])
  });
  saveDoentes(docs);closeModal('modal-edit');openFicha(fichaCurId);toast('Dados guardados');
}

// ═══ INTERNADOS ═══
function renderInternados(){
  var q=((document.getElementById('int-search')||{}).value||'').toLowerCase();
  var tadmF=(document.getElementById('int-tadm-f')||{}).value||'';
  var all=getDoentes().filter(function(d){return d.status==='internado';});
  var kEl=document.getElementById('int-kpis');
  if(kEl){
    var hj=all.filter(function(d){return d.dataAdmissao===todayKey();}).length;
    kEl.innerHTML=
      '<div class="kpi-box kpi-accent"><div class="kpi-label">Total Internados</div><div class="kpi-val">'+all.length+'</div></div>'
      +'<div class="kpi-box kpi-green"><div class="kpi-label">Entrados Hoje</div><div class="kpi-val">'+hj+'</div></div>'
      +'<div class="kpi-box kpi-amber"><div class="kpi-label">Urgências</div><div class="kpi-val">'+all.filter(function(d){return d.tipoAdmissao==='Urgencia';}).length+'</div></div>'
      +'<div class="kpi-box kpi-purple"><div class="kpi-label">Camas Ocupadas</div><div class="kpi-val">'+all.length+' / '+getConfig().numCamas+'</div></div>';
  }
  var docs=all.slice();
  if(tadmF)docs=docs.filter(function(d){return d.tipoAdmissao===tadmF;});
  if(q)docs=docs.filter(function(d){
    return (d.nome||'').toLowerCase().includes(q)||(d.nup||'').toLowerCase().includes(q)||
           (d.diagnostico||'').toLowerCase().includes(q)||(d.cama||'').toLowerCase().includes(q)||
           (d.numStr||'').toLowerCase().includes(q);
  });
  var c=document.getElementById('internados-list');if(!c)return;
  if(!docs.length){c.innerHTML='<div class="no-data">Nenhum doente encontrado.</div>';return;}
  c.innerHTML=docs.map(function(d){
    var dias=daysBetween(d.dataAdmissao,todayKey());
    return '<div class="doc-card" style="border-left:4px solid var(--accent);">'
      +'<div class="doc-info">'
      +'<div class="doc-name">'+d.nome+' <span style="font-size:.65rem;font-weight:400;color:var(--muted);">'+d.numStr+'</span></div>'
      +'<div class="doc-meta">NUP: '+d.nup+' | Cama: '+d.cama+' | Adm: '+fmtDate(d.dataAdmissao)+' | '+dias+' dia(s) | '+d.diagnostico+'</div>'
      +'<div class="doc-meta" style="margin-top:3px;">'+d.tipoAdmissao+(d.medico?' | Dr. '+d.medico:'')+'</div>'
      +'</div>'
      +'<div class="doc-actions">'
      +'<button class="btn btn-outline btn-xs" onclick="openFicha(\''+d.id+'\')">Ficha</button>'
      +'<button class="btn btn-success btn-xs" onclick="abrirSaida(\''+d.id+'\')">Saída</button>'
      +'<button class="btn btn-danger btn-xs" onclick="promptDel(\''+d.id+'\')">Del</button>'
      +'</div></div>';
  }).join('');
}

// ═══ SAÍDA ═══
function abrirSaida(id){
  saidaTargetId=id;
  var d=getDoentes().find(function(x){return x.id===id;});if(!d)return;
  document.getElementById('saida-doente-info').textContent=d.numStr+' — '+d.nome+' | '+d.diagnostico;
  document.getElementById('saida-data').value=todayKey();
  document.getElementById('saida-hora').value=fmtTime();
  document.getElementById('saida-tipo').value='Alta';
  document.getElementById('saida-obs').value='';
  document.getElementById('saida-destino').value='';
  toggleSaidaTipo();
  openModal('modal-saida');
}
function toggleSaidaTipo(){
  var tipo=(document.getElementById('saida-tipo')||{}).value||'';
  var df=document.getElementById('saida-destino-f');
  if(df)df.style.display=(tipo.indexOf('Transf')!==-1)?'':'none';
}
function confirmarSaida(){
  if(!saidaTargetId)return;
  var tipo=(document.getElementById('saida-tipo')||{}).value;
  var data=(document.getElementById('saida-data')||{}).value;
  var hora=(document.getElementById('saida-hora')||{}).value;
  if(!tipo||!data||!hora){toast('Preencha tipo, data e hora de saída','err');return;}
  var docs=getDoentes();var idx=docs.findIndex(function(x){return x.id===saidaTargetId;});if(idx<0)return;
  var d=docs[idx];
  var dias=daysBetween(d.dataAdmissao,data);
  docs[idx].status=statusKey(tipo);
  docs[idx].saida={tipo:tipo,data:data,hora:hora,
    destino:(document.getElementById('saida-destino').value||'').trim(),
    obs:(document.getElementById('saida-obs').value||'').trim(),
    diasInternamento:dias,profissional:currentProfissional};
  docs[idx].historico=(docs[idx].historico||[]).concat([{
    ts:new Date().toISOString(),profissional:currentProfissional,
    acao:'Saída registada: '+tipo,campos:'Dias de internamento: '+dias}]);
  saveDoentes(docs);
  addNotif(docs[idx],tipo);
  closeModal('modal-saida');renderInternados();updateBottomBar();
  toast('Saída registada: '+tipo+' — '+d.nome);
}

// ═══ LISTA DE SAÍDAS ═══
function renderSaidas(){
  var f=(document.getElementById('saidas-from')||{}).value||'';
  var t=(document.getElementById('saidas-to')||{}).value||'';
  var tipoF=(document.getElementById('saidas-tipo-f')||{}).value||'';
  var q=((document.getElementById('saidas-search')||{}).value||'').toLowerCase();
  var all=getDoentes().filter(function(d){return d.saida;});
  var kEl=document.getElementById('saidas-kpis');
  if(kEl){
    var total=all.length;
    var altas=all.filter(function(d){return d.status==='alta';}).length;
    var obitos=all.filter(function(d){return d.status==='obito';}).length;
    var transf=all.filter(function(d){return d.status.indexOf('transf')!==-1;}).length;
    kEl.innerHTML=
      '<div class="kpi-box kpi-accent"><div class="kpi-label">Total Saídas</div><div class="kpi-val">'+total+'</div></div>'
      +'<div class="kpi-box kpi-green"><div class="kpi-label">Altas</div><div class="kpi-val">'+altas+'</div></div>'
      +'<div class="kpi-box kpi-red"><div class="kpi-label">Óbitos</div><div class="kpi-val">'+obitos+'</div></div>'
      +'<div class="kpi-box kpi-purple"><div class="kpi-label">Transferências</div><div class="kpi-val">'+transf+'</div></div>';
  }
  var docs=all.slice();
  if(f)docs=docs.filter(function(d){return d.saida.data>=f;});
  if(t)docs=docs.filter(function(d){return d.saida.data<=t;});
  if(tipoF)docs=docs.filter(function(d){return d.saida.tipo===tipoF;});
  if(q)docs=docs.filter(function(d){
    return (d.nome||'').toLowerCase().includes(q)||(d.nup||'').toLowerCase().includes(q)||
           (d.numStr||'').toLowerCase().includes(q);
  });
  docs.sort(function(a,b){return b.saida.data.localeCompare(a.saida.data);});
  var c=document.getElementById('saidas-list');if(!c)return;
  if(!docs.length){c.innerHTML='<div class="no-data">Nenhuma saída encontrada.</div>';return;}
  c.innerHTML=docs.map(function(d){
    return '<div class="doc-card" style="border-left:4px solid '+(d.status==='obito'?'var(--red)':d.status==='alta'?'var(--green)':'var(--purple)')+';">'
      +'<div class="doc-info">'
      +'<div class="doc-name">'+d.nome+' <span style="font-size:.65rem;font-weight:400;color:var(--muted);">'+d.numStr+'</span></div>'
      +'<div class="doc-meta">NUP: '+d.nup+' | Saída: '+fmtDate(d.saida.data)+' '+d.saida.hora+' | '+d.saida.diasInternamento+' dias</div>'
      +'<div class="doc-meta">'+statusBadge(d.status)+(d.saida.destino?' → '+d.saida.destino:'')+(d.saida.obs?' | '+d.saida.obs:'')+'</div>'
      +'</div>'
      +'<div class="doc-actions"><button class="btn btn-outline btn-xs" onclick="openFicha(\''+d.id+'\')">Ficha</button></div>'
      +'</div>';
  }).join('');
}

// ═══ MOVIMENTO ═══
var movRange={start:todayKey(),end:todayKey()};
function setMovPeriod(p,btn){
  movPeriod=p;
  document.querySelectorAll('.period-bar .pb').forEach(function(b){b.classList.remove('active');});
  if(btn)btn.classList.add('active');
  var custom=document.getElementById('mov-custom');
  if(p==='custom'){if(custom)custom.style.display='flex';return;}
  if(custom)custom.style.display='none';
  var r=getDateRange(p);movRange={start:r.start,end:r.end};
  renderMovimento();
}
function getDateRange(p){
  var today=todayKey();var d=new Date();
  if(p==='hoje')return{start:today,end:today};
  if(p==='semana'){var s=new Date(d);s.setDate(d.getDate()-6);return{start:s.toISOString().slice(0,10),end:today};}
  if(p==='mes')return{start:today.slice(0,7)+'-01',end:today};
  if(p==='trimestre'){var s2=new Date(d);s2.setMonth(d.getMonth()-3);return{start:s2.toISOString().slice(0,10),end:today};}
  if(p==='semestre'){var s3=new Date(d);s3.setMonth(d.getMonth()-6);return{start:s3.toISOString().slice(0,10),end:today};}
  if(p==='ano')return{start:today.slice(0,4)+'-01-01',end:today};
  return{start:today,end:today};
}
function renderMovimento(){
  var f,t;
  if(movPeriod==='custom'){
    f=(document.getElementById('mov-from')||{}).value||todayKey();
    t=(document.getElementById('mov-to')||{}).value||todayKey();
  }else{var r=getDateRange(movPeriod);f=r.start;t=r.end;}
  var docs=getDoentes();
  var entradas=docs.filter(function(d){return d.dataAdmissao>=f&&d.dataAdmissao<=t;});
  var saidas=docs.filter(function(d){return d.saida&&d.saida.data>=f&&d.saida.data<=t;});
  var obitos=saidas.filter(function(d){return d.status==='obito';});
  var kEl=document.getElementById('mov-kpis');
  if(kEl){
    kEl.innerHTML=
      '<div class="kpi-box kpi-accent"><div class="kpi-label">Entradas</div><div class="kpi-val">'+entradas.length+'</div></div>'
      +'<div class="kpi-box kpi-green"><div class="kpi-label">Saídas Totais</div><div class="kpi-val">'+saidas.length+'</div></div>'
      +'<div class="kpi-box kpi-red"><div class="kpi-label">Óbitos</div><div class="kpi-val">'+obitos.length+'</div></div>'
      +'<div class="kpi-box"><div class="kpi-label">Internados Activos</div><div class="kpi-val">'+docs.filter(function(d){return d.status==='internado';}).length+'</div></div>';
  }
  function listDocs(arr,container){
    var c=document.getElementById(container);if(!c)return;
    if(!arr.length){c.innerHTML='<div class="no-data">Nenhum registo.</div>';return;}
    c.innerHTML='<div class="table-wrap"><table><thead><tr><th>Processo</th><th>NUP</th><th>Nome</th><th>Data</th><th>Diagnóstico</th><th>Estado</th></tr></thead><tbody>'
      +arr.map(function(d){
        return '<tr onclick="openFicha(\''+d.id+'\')" style="cursor:pointer;">'
          +'<td>'+d.numStr+'</td><td>'+d.nup+'</td><td>'+d.nome+'</td>'
          +'<td>'+(container==='mov-entradas-list'?fmtDate(d.dataAdmissao):fmtDate(d.saida.data))+'</td>'
          +'<td>'+d.diagnostico+'</td><td>'+statusBadge(d.status)+'</td></tr>';
      }).join('')+'</tbody></table></div>';
  }
  listDocs(entradas,'mov-entradas-list');listDocs(saidas,'mov-saidas-list');
}

// ═══ INDICADORES ═══
function setIndPeriod(p){
  indPeriod=p;
  document.querySelectorAll('[data-p]').forEach(function(b){b.classList.remove('active');});
  var b=document.querySelector('[data-p="'+p+'"]');if(b)b.classList.add('active');
  var r=getDateRange(p);
  var f=document.getElementById('ind-from');if(f)f.value=r.start;
  var t=document.getElementById('ind-to');if(t)t.value=r.end;
  renderIndicadores();
}
function calcIndicadores(f,t,numCamas){
  var all=getDoentes();var numDias=daysBetween(f,t)+1;var diasCamas=numCamas*numDias;
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
  return{numDias,numCamas,diasCamas,diasDoentes,
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
    entradas,saidas,obitos:obitos,altas,transf};
}
function renderIndicadores(){
  var f=(document.getElementById('ind-from')||{}).value||todayKey().slice(0,7)+'-01';
  var t=(document.getElementById('ind-to')||{}).value||todayKey();
  var nc=parseInt((document.getElementById('ind-ncamas')||{}).value||getConfig().numCamas||30);
  var ind=calcIndicadores(f,t,nc);
  var kEl=document.getElementById('ind-kpis');
  if(kEl){
    kEl.innerHTML=
      '<div class="kpi-box kpi-accent"><div class="kpi-label">Taxa de Ocupação</div><div class="kpi-val">'+ind.taxaOcupacao.toFixed(1)+'%</div><div class="kpi-sub">'+ind.diasDoentes+' dias-doente / '+ind.diasCamas+' dias-cama</div></div>'
      +'<div class="kpi-box kpi-green"><div class="kpi-label">Média Permanência</div><div class="kpi-val">'+ind.mediaPermanencia.toFixed(1)+'<span style="font-size:.7rem;font-weight:500">d</span></div></div>'
      +'<div class="kpi-box kpi-red"><div class="kpi-label">Taxa de Mortalidade</div><div class="kpi-val">'+ind.taxaMortalidade.toFixed(1)+'%</div><div class="kpi-sub">'+ind.obitos.length+' óbito(s)</div></div>'
      +'<div class="kpi-box kpi-amber"><div class="kpi-label">Índice Rotatividade</div><div class="kpi-val">'+ind.indiceRotatividade.toFixed(2)+'</div></div>'
      +'<div class="kpi-box kpi-purple"><div class="kpi-label">Intervalo Substituição</div><div class="kpi-val">'+ind.intervaloSubstituicao.toFixed(1)+'<span style="font-size:.7rem;font-weight:500">d</span></div></div>'
      +'<div class="kpi-box kpi-green"><div class="kpi-label">Internados Activos</div><div class="kpi-val">'+ind.doentesAtivos+'</div></div>';
  }
  var tw=document.getElementById('ind-table-wrap');
  if(tw){
    tw.innerHTML='<table class="ind-tbl"><tbody>'
      +'<tr><td>Período</td><td>'+fmtDate(f)+' a '+fmtDate(t)+' ('+ind.numDias+' dias)</td></tr>'
      +'<tr><td>N.º Camas</td><td>'+nc+'</td></tr>'
      +'<tr><td>Dias-Cama</td><td>'+ind.diasCamas+'</td></tr>'
      +'<tr><td>Dias-Doente</td><td>'+ind.diasDoentes+'</td></tr>'
      +'<tr><td>Total Entradas</td><td>'+ind.totalEntradas+'</td></tr>'
      +'<tr><td>Total Saídas</td><td>'+ind.totalSaidas+'</td></tr>'
      +'<tr><td>Altas</td><td>'+ind.altas.length+' ('+ind.taxaAlta.toFixed(1)+'%)</td></tr>'
      +'<tr><td>Óbitos</td><td>'+ind.obitos.length+' ('+ind.taxaMortalidade.toFixed(1)+'%)</td></tr>'
      +'<tr><td>Transferências</td><td>'+ind.transferencias+' ('+ind.taxaTransferencia.toFixed(1)+'%)</td></tr>'
      +'<tr><td>Taxa de Ocupação</td><td>'+ind.taxaOcupacao.toFixed(2)+'%</td></tr>'
      +'<tr><td>Média de Permanência</td><td>'+ind.mediaPermanencia.toFixed(2)+' dias</td></tr>'
      +'<tr><td>Índice de Rotatividade</td><td>'+ind.indiceRotatividade.toFixed(3)+'</td></tr>'
      +'<tr><td>Intervalo de Substituição</td><td>'+ind.intervaloSubstituicao.toFixed(2)+' dias</td></tr>'
      +'</tbody></table>';
  }
  renderIndCharts(ind,f,t);
}
function destroyChart(id){if(ortoCharts[id]){ortoCharts[id].destroy();delete ortoCharts[id];}}
function mkChart(id,type,labels,datasets,opts){
  destroyChart(id);var c=document.getElementById(id);if(!c)return;
  var isDark=document.documentElement.classList.contains('dark');
  var gc=isDark?'rgba(255,255,255,.08)':'rgba(0,0,0,.06)';
  var tc=isDark?'#94a3b8':'#475569';
  ortoCharts[id]=new Chart(c,{type:type,data:{labels:labels,datasets:datasets},options:Object.assign({
    responsive:true,maintainAspectRatio:false,
    plugins:{legend:{labels:{color:tc,font:{size:10}}},tooltip:{callbacks:{}}},
    scales:type==='doughnut'||type==='pie'?{}:{
      x:{ticks:{color:tc,font:{size:9}},grid:{color:gc}},
      y:{ticks:{color:tc,font:{size:9}},grid:{color:gc}}
    }
  },opts||{})});
}
function renderIndCharts(ind,f,t){
  mkChart('ind-chart-mov','bar',['Entradas','Saídas','Óbitos'],
    [{label:'Contagem',data:[ind.totalEntradas,ind.totalSaidas,ind.obitos.length],
      backgroundColor:['rgba(26,86,219,.7)','rgba(5,150,105,.7)','rgba(220,38,38,.7)']}]);
  mkChart('ind-chart-tipo','doughnut',['Alta','Óbito','Transf. Interna','Transf. Externa'],
    [{data:[ind.altas.length,ind.obitos.length,
        ind.saidas.filter(function(d){return d.status==='transferencia_interna';}).length,
        ind.saidas.filter(function(d){return d.status==='transferencia_externa';}).length],
      backgroundColor:['#059669','#dc2626','#7c3aed','#0891b2'],borderWidth:2}]);
  mkChart('ind-chart-tadm','doughnut',['Urgência','Programada','Transf. Int.','Transf. Ext.'],
    [{data:[
        ind.entradas.filter(function(d){return d.tipoAdmissao==='Urgencia';}).length,
        ind.entradas.filter(function(d){return d.tipoAdmissao==='Programada';}).length,
        ind.entradas.filter(function(d){return d.tipoAdmissao==='Transferencia Interna';}).length,
        ind.entradas.filter(function(d){return d.tipoAdmissao==='Transferencia Externa';}).length],
      backgroundColor:['#d97706','#1a56db','#7c3aed','#0891b2'],borderWidth:2}]);
  // Tendência semanal
  var weeks=[];var wdata=[];var d=new Date(f);
  while(d<=new Date(t)){
    var ws=d.toISOString().slice(0,10);var we=new Date(d);we.setDate(we.getDate()+6);
    var wend=we>new Date(t)?t:we.toISOString().slice(0,10);
    weeks.push('Sem '+fmtDate(ws).slice(0,5));
    wdata.push(getDoentes().filter(function(x){return x.dataAdmissao>=ws&&x.dataAdmissao<=wend;}).length);
    d.setDate(d.getDate()+7);
    if(weeks.length>=12)break;
  }
  mkChart('ind-chart-trend','line',weeks,
    [{label:'Entradas Semanais',data:wdata,borderColor:'#1a56db',backgroundColor:'rgba(26,86,219,.1)',fill:true,tension:.3,pointRadius:3}]);
  // Ocupação simulada (taxa por semana)
  var oweeks=[];var odata=[];var od=new Date(f);
  while(od<=new Date(t)){
    var os=od.toISOString().slice(0,10);var oe=new Date(od);oe.setDate(oe.getDate()+6);
    var oend=oe>new Date(t)?t:oe.toISOString().slice(0,10);
    oweeks.push(fmtDate(os).slice(0,5));
    var nc=parseInt((document.getElementById('ind-ncamas')||{}).value||getConfig().numCamas||30);
    var oi=calcIndicadores(os,oend,nc);odata.push(parseFloat(oi.taxaOcupacao.toFixed(1)));
    od.setDate(od.getDate()+7);if(oweeks.length>=12)break;
  }
  mkChart('ind-chart-ocup','line',oweeks,
    [{label:'Taxa de Ocupação (%)',data:odata,borderColor:'#059669',backgroundColor:'rgba(5,150,105,.1)',fill:true,tension:.3,pointRadius:3}]);
}

// ═══ DIAGNÓSTICOS ═══
function renderDiagnosticos(){
  var estadoF=(document.getElementById('diag-estado-f')||{}).value||'';
  var docs=getDoentes();
  if(estadoF==='internado')docs=docs.filter(function(d){return d.status==='internado';});
  if(estadoF==='saido')docs=docs.filter(function(d){return d.saida;});
  var map={};
  docs.forEach(function(d){
    var k=d.diagnostico||'Sem diagnóstico';
    if(!map[k])map[k]={diag:k,total:0,internados:0,altas:0,obitos:0,transf:0};
    map[k].total++;
    if(d.status==='internado')map[k].internados++;
    if(d.status==='alta')map[k].altas++;
    if(d.status==='obito')map[k].obitos++;
    if(d.status.indexOf('transf')!==-1)map[k].transf++;
  });
  var list=Object.values(map).sort(function(a,b){return b.total-a.total;});
  var c=document.getElementById('diag-list');if(!c)return;
  if(!list.length){c.innerHTML='<div class="no-data">Sem dados.</div>';return;}
  c.innerHTML='<div class="table-wrap"><table><thead><tr><th>Diagnóstico</th><th>Total</th><th>Internados</th><th>Altas</th><th>Óbitos</th><th>Transf.</th></tr></thead><tbody>'
    +list.map(function(r){
      return '<tr><td>'+r.diag+'</td><td>'+r.total+'</td><td>'+r.internados+'</td><td>'+r.altas+'</td><td>'+r.obitos+'</td><td>'+r.transf+'</td></tr>';
    }).join('')+'</tbody></table></div>';
  var top=list.slice(0,8);
  mkChart('diag-chart','bar',top.map(function(r){return r.diag.slice(0,20);}),
    [{label:'Total',data:top.map(function(r){return r.total;}),backgroundColor:'rgba(26,86,219,.7)'}],
    {indexAxis:'y',scales:{x:{ticks:{color:'#475569',font:{size:8}}},y:{ticks:{color:'#475569',font:{size:8}}}}});
}

// ═══ PESQUISA ═══
function renderPesquisa(){
  var q=((document.getElementById('pq-q')||{}).value||'').toLowerCase();
  var st=(document.getElementById('pq-status')||{}).value||'';
  var sx=(document.getElementById('pq-sexo')||{}).value||'';
  var f=(document.getElementById('pq-from')||{}).value||'';
  var t=(document.getElementById('pq-to')||{}).value||'';
  var docs=getDoentes();
  if(st)docs=docs.filter(function(d){return d.status===st;});
  if(sx)docs=docs.filter(function(d){return d.sexo===sx;});
  if(f)docs=docs.filter(function(d){return d.dataAdmissao>=f;});
  if(t)docs=docs.filter(function(d){return d.dataAdmissao<=t;});
  if(q)docs=docs.filter(function(d){
    return (d.nome||'').toLowerCase().includes(q)||(d.nup||'').toLowerCase().includes(q)||
           (d.bi||'').toLowerCase().includes(q)||(d.diagnostico||'').toLowerCase().includes(q)||
           (d.numStr||'').toLowerCase().includes(q);
  });
  var c=document.getElementById('pq-results');if(!c)return;
  if(!docs.length){c.innerHTML='<div class="card"><div class="no-data">Nenhum resultado.</div></div>';return;}
  c.innerHTML='<div class="card"><div style="font-size:.7rem;color:var(--muted);margin-bottom:8px;">'+docs.length+' resultado(s)</div>'
    +'<div class="table-wrap"><table><thead><tr><th>Processo</th><th>NUP</th><th>Nome</th><th>Sexo</th><th>Admissão</th><th>Diagnóstico</th><th>Estado</th><th></th></tr></thead><tbody>'
    +docs.map(function(d){
      return '<tr><td>'+d.numStr+'</td><td>'+d.nup+'</td><td>'+d.nome+'</td>'
        +'<td>'+(d.sexo==='M'?'M':'F')+'</td><td>'+fmtDate(d.dataAdmissao)+'</td>'
        +'<td>'+d.diagnostico+'</td><td>'+statusBadge(d.status)+'</td>'
        +'<td><button class="btn btn-outline btn-xs" onclick="openFicha(\''+d.id+'\')">Ficha</button></td></tr>';
    }).join('')+'</tbody></table></div></div>';
}

// ═══ ELIMINAÇÃO ═══
function promptDel(id){
  delTargetId=id;
  var m=document.getElementById('modal-del');if(m){m.style.display='flex';}
}
function confirmDel(){
  if(!delTargetId)return;
  var docs=getDoentes().filter(function(d){return d.id!==delTargetId;});
  saveDoentes(docs);delTargetId=null;
  closeModal('modal-del');renderInternados();updateBottomBar();toast('Registo eliminado');
}

// ═══ DEFINIÇÕES ═══
function renderDefinicoes(){
  var cfg=getConfig();
  var s=document.getElementById('def-servico');if(s)s.value=cfg.servico||'';
  var nc=document.getElementById('def-ncamas');if(nc)nc.value=cfg.numCamas||30;
  var na=document.getElementById('def-numAtual');if(na)na.value=cfg.numAtual||1;
  var an=document.getElementById('def-ano');if(an)an.value=cfg.ano||new Date().getFullYear();
  renderDefProfs();renderDefNotifs();
  var bk=localStorage.getItem('hp_orto_lastbackup');
  var bi=document.getElementById('def-backup-info');
  if(bi)bi.textContent=bk?'Último backup: '+fmtDate(bk.slice(0,10))+' '+bk.slice(11,16):'Nenhum backup realizado nesta sessão.';
}
function salvarConfigServico(){
  if(!currentProfissional){toast('Faça login primeiro','err');return;}
  var senhaAct=prompt('Senha do Chefe para confirmar alterações:');
  var cfg=getConfig();if(senhaAct!==cfg.senhaChefe){toast('Senha incorrecta','err');return;}
  cfg.servico=(document.getElementById('def-servico').value||'').trim()||cfg.servico;
  cfg.numCamas=parseInt(document.getElementById('def-ncamas').value||cfg.numCamas)||cfg.numCamas;
  cfg.numAtual=parseInt(document.getElementById('def-numAtual').value||cfg.numAtual)||cfg.numAtual;
  cfg.ano=parseInt(document.getElementById('def-ano').value||cfg.ano)||cfg.ano;
  var sc=(document.getElementById('def-senhachefe').value||'').trim();
  if(sc)cfg.senhaChefe=sc;
  saveConfig(cfg);updateNumPreview();toast('Configuração guardada');
  document.getElementById('def-senhachefe').value='';
}
function renderDefProfs(){
  var cfg=getConfig();var c=document.getElementById('def-profs');if(!c)return;
  c.innerHTML=cfg.profissionais.map(function(p,i){
    return '<div style="display:flex;align-items:center;gap:8px;padding:8px 0;border-bottom:1px solid var(--border);">'
      +'<div style="flex:1;font-size:.78rem;font-weight:600;">'+p.nome+'</div>'
      +'<div style="font-size:.65rem;color:var(--muted);">ID: '+p.id+'</div>'
      +'<button class="btn btn-outline btn-xs" onclick="editarProf('+i+')">Editar</button>'
      +(cfg.profissionais.length>1?'<button class="btn btn-danger btn-xs" onclick="removerProf('+i+')">Del</button>':'')
      +'</div>';
  }).join('');
}
function addProfissional(){
  var senhaAct=prompt('Senha do Chefe:');var cfg=getConfig();
  if(senhaAct!==cfg.senhaChefe){toast('Senha incorrecta','err');return;}
  var nome=prompt('Nome do profissional:');if(!nome||!nome.trim())return;
  var senha=prompt('Senha:');if(!senha)return;
  cfg.profissionais.push({id:nome.trim().toLowerCase().replace(/\s+/g,'_')+'_'+Date.now().toString(36),nome:nome.trim(),senha:senha});
  saveConfig(cfg);renderDefProfs();toast('Profissional adicionado');
}
function editarProf(i){
  var cfg=getConfig();var p=cfg.profissionais[i];
  var senhaAct=prompt('Senha do Chefe para editar:');
  if(senhaAct!==cfg.senhaChefe){toast('Senha incorrecta','err');return;}
  var nome=prompt('Nome:',p.nome);if(!nome)return;
  var senha=prompt('Nova senha (deixe vazio para manter):');
  cfg.profissionais[i].nome=nome.trim();
  if(senha)cfg.profissionais[i].senha=senha;
  saveConfig(cfg);renderDefProfs();toast('Profissional actualizado');
}
function removerProf(i){
  var cfg=getConfig();if(cfg.profissionais.length<=1){toast('Tem de existir pelo menos 1 profissional','err');return;}
  var senhaAct=prompt('Senha do Chefe para remover:');
  if(senhaAct!==cfg.senhaChefe){toast('Senha incorrecta','err');return;}
  if(!confirm('Remover '+cfg.profissionais[i].nome+'?'))return;
  cfg.profissionais.splice(i,1);saveConfig(cfg);renderDefProfs();toast('Profissional removido');
}
function downloadBackup(){
  var data={config:getConfig(),doentes:getDoentes(),notifs:getNotifs(),exportedAt:new Date().toISOString()};
  var blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  var a=document.createElement('a');a.href=URL.createObjectURL(blob);
  a.download='backup_ortopedia_'+todayKey()+'.json';document.body.appendChild(a);a.click();document.body.removeChild(a);
  localStorage.setItem('hp_orto_lastbackup',new Date().toISOString());
  renderDefinicoes();toast('Backup descarregado');
}
function importarBackup(){document.getElementById('import-file').click();}
function processarBackup(ev){
  var file=ev.target.files[0];if(!file)return;
  var r=new FileReader();
  r.onload=function(e){
    try{
      var data=JSON.parse(e.target.result);
      if(!confirm('Isto irá substituir todos os dados actuais. Continuar?'))return;
      if(data.config)saveConfig(data.config);
      if(data.doentes)saveDoentes(data.doentes);
      if(data.notifs)saveNotifs(data.notifs);
      toast('Backup importado com sucesso','info');renderDefinicoes();updateBottomBar();updateNotifBadge();
    }catch(ex){toast('Ficheiro inválido','err');}
  };r.readAsText(file);ev.target.value='';
}
function renderDefNotifs(){
  var notifs=getNotifs();var c=document.getElementById('def-notifs');if(!c)return;
  if(!notifs.length){c.innerHTML='<div class="no-data">Sem notificações.</div>';return;}
  notifs.forEach(function(n){n.lida=true;});saveNotifs(notifs);updateNotifBadge();
  c.innerHTML=notifs.map(function(n){
    return '<div class="notif-item">'
      +'<div class="notif-dot read"></div>'
      +'<div><div style="font-size:.75rem;font-weight:600;">'+n.tipo+': '+n.doente+'</div>'
      +'<div style="font-size:.65rem;color:var(--muted);">'+n.numStr+' | Por: '+n.profissional+' | '+new Date(n.ts).toLocaleString('pt-AO')+'</div></div>'
      +'</div>';
  }).join('');
}
function limparNotifs(){saveNotifs([]);renderDefinicoes();updateNotifBadge();}

// ═══ BARRA INFERIOR ═══
function updateBottomBar(){
  var docs=getDoentes();var hoje=todayKey();
  var internados=docs.filter(function(d){return d.status==='internado';}).length;
  var entradosHj=docs.filter(function(d){return d.dataAdmissao===hoje;}).length;
  var saidosHj=docs.filter(function(d){return d.saida&&d.saida.data===hoje;}).length;
  var obitosHj=docs.filter(function(d){return d.saida&&d.saida.data===hoje&&d.status==='obito';}).length;
  var el=document.getElementById('bb-internados');if(el)el.textContent=internados;
  el=document.getElementById('bb-entrados');if(el)el.textContent=entradosHj;
  el=document.getElementById('bb-saidos');if(el)el.textContent=saidosHj;
  el=document.getElementById('bb-obitos');if(el)el.textContent=obitosHj;
  var dt=document.getElementById('bb-date');if(dt)dt.textContent=fmtDate(hoje);
}

// ═══ PDF ═══
function jsPDFReady(){return typeof jspdf!=='undefined'&&typeof jspdf.jsPDF!=='undefined';}
function exportIndPDF(period){
  if(!jsPDFReady()){toast('A aguardar biblioteca PDF...','err');return;}
  var f,t,nc;
  if(period==='custom'){
    f=(document.getElementById('ind-from')||{}).value||todayKey();
    t=(document.getElementById('ind-to')||{}).value||todayKey();
  }else{var r=getDateRange(period);f=r.start;t=r.end;}
  nc=parseInt((document.getElementById('ind-ncamas')||{}).value||getConfig().numCamas||30);
  var ind=calcIndicadores(f,t,nc);
  var pPeriod={semana:'Semanal',mes:'Mensal',trimestre:'Trimestral',semestre:'Semestral',ano:'Anual',custom:'Personalizado'};
  var doc=new jspdf.jsPDF({orientation:'landscape'});
  doc.setFontSize(14);doc.setFont('helvetica','bold');
  doc.text('Hospital do Prenda — Relatório '+( pPeriod[period]||period),14,14);
  doc.setFontSize(9);doc.setFont('helvetica','normal');doc.setTextColor(80);
  doc.text('Serviço de Ortopedia/Medicina | Período: '+fmtDate(f)+' a '+fmtDate(t),14,21);
  doc.text('Gerado em: '+new Date().toLocaleString('pt-AO')+' por '+currentProfissional,14,27);
  doc.setTextColor(0);
  doc.autoTable({startY:33,
    head:[['Indicador','Valor']],
    body:[
      ['Período',fmtDate(f)+' a '+fmtDate(t)+' ('+ind.numDias+' dias)'],
      ['N.º Camas',String(nc)],
      ['Dias-Cama',String(ind.diasCamas)],
      ['Dias-Doente',String(ind.diasDoentes)],
      ['Total Entradas',String(ind.totalEntradas)],
      ['Total Saídas',String(ind.totalSaidas)],
      ['Altas',ind.altas.length+' ('+ind.taxaAlta.toFixed(1)+'%)'],
      ['Óbitos',ind.obitos.length+' ('+ind.taxaMortalidade.toFixed(1)+'%)'],
      ['Transferências',String(ind.transferencias)],
      ['Taxa de Ocupação',ind.taxaOcupacao.toFixed(2)+'%'],
      ['Média de Permanência',ind.mediaPermanencia.toFixed(2)+' dias'],
      ['Índice de Rotatividade',ind.indiceRotatividade.toFixed(3)],
      ['Intervalo de Substituição',ind.intervaloSubstituicao.toFixed(2)+' dias'],
      ['Doentes Internados Activos',String(ind.doentesAtivos)]
    ],
    styles:{fontSize:9,cellPadding:3},
    headStyles:{fillColor:[26,86,219],textColor:255},
    alternateRowStyles:{fillColor:[240,244,255]}
  });
  var y=doc.lastAutoTable.finalY+10;
  if(ind.totalSaidas>0&&y<160){
    doc.autoTable({startY:y,
      head:[['Processo','NUP','Nome','Tipo Saída','Data','Dias']],
      body:ind.saidas.slice(0,20).map(function(d){
        return [d.numStr,d.nup,d.nome,d.saida.tipo,fmtDate(d.saida.data),String(d.saida.diasInternamento)];
      }),
      styles:{fontSize:8,cellPadding:2},
      headStyles:{fillColor:[30,64,175],textColor:255}
    });
  }
  doc.save('relatorio_ortopedia_'+period+'_'+todayKey()+'.pdf');toast('PDF exportado');
}
function exportIntPDF(){
  if(!jsPDFReady()){toast('A aguardar biblioteca PDF...','err');return;}
  var docs=getDoentes().filter(function(d){return d.status==='internado';});
  var doc=new jspdf.jsPDF({orientation:'landscape'});
  doc.setFontSize(13);doc.setFont('helvetica','bold');
  doc.text('Hospital do Prenda — Doentes Internados',14,14);
  doc.setFontSize(9);doc.setFont('helvetica','normal');doc.setTextColor(80);
  doc.text('Serviço de Ortopedia/Medicina | '+fmtDate(todayKey())+' | Total: '+docs.length,14,21);doc.setTextColor(0);
  doc.autoTable({startY:27,
    head:[['Processo','NUP','Nome','Sexo','Cama','Admissão','Dias','Diagnóstico','Médico']],
    body:docs.map(function(d){
      return [d.numStr,d.nup,d.nome,d.sexo==='M'?'M':'F',d.cama,fmtDate(d.dataAdmissao),
        String(daysBetween(d.dataAdmissao,todayKey())),d.diagnostico,d.medico||'---'];
    }),
    styles:{fontSize:8,cellPadding:2},
    headStyles:{fillColor:[26,86,219],textColor:255},
    alternateRowStyles:{fillColor:[240,244,255]}
  });
  doc.save('internados_'+todayKey()+'.pdf');toast('PDF exportado');
}
function exportSaidasPDF(){
  if(!jsPDFReady()){toast('A aguardar biblioteca PDF...','err');return;}
  var f=(document.getElementById('saidas-from')||{}).value||'';
  var t=(document.getElementById('saidas-to')||{}).value||todayKey();
  var docs=getDoentes().filter(function(d){return d.saida&&(!f||d.saida.data>=f)&&d.saida.data<=t;});
  var doc=new jspdf.jsPDF({orientation:'landscape'});
  doc.setFontSize(13);doc.setFont('helvetica','bold');
  doc.text('Hospital do Prenda — Relatório de Saídas',14,14);
  doc.setFontSize(9);doc.setFont('helvetica','normal');doc.setTextColor(80);
  doc.text('Serviço de Ortopedia/Medicina | Período: '+(f?fmtDate(f):'-')+' a '+fmtDate(t),14,21);doc.setTextColor(0);
  doc.autoTable({startY:27,
    head:[['Processo','NUP','Nome','Tipo Saída','Data Saída','Dias','Destino']],
    body:docs.map(function(d){
      return [d.numStr,d.nup,d.nome,d.saida.tipo,fmtDate(d.saida.data),String(d.saida.diasInternamento),d.saida.destino||'---'];
    }),
    styles:{fontSize:8,cellPadding:2},
    headStyles:{fillColor:[26,86,219],textColor:255},
    alternateRowStyles:{fillColor:[240,244,255]}
  });
  doc.save('saidas_'+todayKey()+'.pdf');toast('PDF exportado');
}
function exportMovPDF(){exportSaidasPDF();}
function exportarFichaPDF(){
  if(!jsPDFReady()||!fichaCurId){toast('Sem dados para exportar','err');return;}
  var d=getDoentes().find(function(x){return x.id===fichaCurId;});if(!d)return;
  var dias=d.saida?d.saida.diasInternamento:daysBetween(d.dataAdmissao,todayKey());
  var idadeStr=d.dataNascimento?calcIdadeFromDnasc(d.dataNascimento)+' anos':(d.idadeManual||'---');
  var doc=new jspdf.jsPDF();
  doc.setFontSize(13);doc.setFont('helvetica','bold');
  doc.text('Ficha do Doente — '+d.numStr,14,14);
  doc.setFontSize(9);doc.setFont('helvetica','normal');doc.setTextColor(80);
  doc.text('Serviço de Ortopedia/Medicina — Hospital do Prenda',14,21);doc.setTextColor(0);
  doc.autoTable({startY:27,
    head:[['Campo','Valor']],
    body:[
      ['NUP',d.nup],['N.º Processo',d.numStr],['Nome Completo',d.nome],
      ['Sexo',d.sexo==='M'?'Masculino':'Feminino'],['Idade',idadeStr],
      ['Data de Nascimento',d.dataNascimento?fmtDate(d.dataNascimento):(d.idadeManual||'---')],
      ['BI / Passaporte',d.bi||'---'],['Diagnóstico',d.diagnostico],
      ['Tipo de Admissão',d.tipoAdmissao],['Data de Admissão',fmtDate(d.dataAdmissao)+' '+d.horaAdmissao],
      ['Cama',d.cama],['Médico',d.medico||'---'],['Observações',d.obs||'---'],
      ['Dias de Internamento',String(dias)],
      ['Estado',d.status==='internado'?'Internado':d.saida?d.saida.tipo:'---'],
      ['Data de Saída',d.saida?fmtDate(d.saida.data)+' '+d.saida.hora:'---'],
      ['Destino/Obs. Saída',d.saida&&d.saida.destino?d.saida.destino:(d.saida&&d.saida.obs?d.saida.obs:'---')]
    ],
    styles:{fontSize:9,cellPadding:3},
    headStyles:{fillColor:[26,86,219],textColor:255},
    alternateRowStyles:{fillColor:[240,244,255]}
  });
  if(d.historico&&d.historico.length){
    doc.autoTable({startY:doc.lastAutoTable.finalY+8,
      head:[['Data/Hora','Profissional','Acção','Campos Alterados']],
      body:d.historico.map(function(h){
        return [new Date(h.ts).toLocaleString('pt-AO'),h.profissional,h.acao,h.campos||'---'];
      }),
      styles:{fontSize:8,cellPadding:2},
      headStyles:{fillColor:[30,64,175],textColor:255}
    });
  }
  doc.save('ficha_'+d.numStr.replace(/\//g,'_')+'_'+todayKey()+'.pdf');toast('Ficha exportada');
}

// ═══ AUTO-BACKUP ═══
(function(){
  var done=false;
  setInterval(function(){
    var h=new Date().getHours(),m=new Date().getMinutes();
    if(h===14&&m<1&&!done){done=true;downloadBackup();}
    if(h!==14)done=false;
  },55000);
})();

// ═══ TEMA / SPLASH / INIT ═══
function toggleTheme(){var dark=document.documentElement.classList.toggle('dark');localStorage.setItem('hp_orto_theme',dark?'dark':'light');}
(function(){
  var D=3500,ring=document.getElementById('spl-ring'),pct=document.getElementById('spl-pct'),C=263.9,start=null;
  if(!ring)return;
  function step(ts){
    if(!start)start=ts;var p=Math.min((ts-start)/D,1),e=p<.5?2*p*p:-1+(4-2*p)*p;
    ring.style.strokeDashoffset=C*(1-e);if(pct)pct.textContent=Math.round(e*100)+'%';
    if(p<1){requestAnimationFrame(step);return;}
    var s=document.getElementById('splash');
    if(s){s.style.transition='opacity .4s';s.style.opacity='0';setTimeout(function(){s.style.display='none';},400);}
  }
  requestAnimationFrame(step);
})();
document.addEventListener('DOMContentLoaded',function(){
  checkSession();
  var dadm=document.getElementById('r-dadm');if(dadm)dadm.value=todayKey();
  var hadm=document.getElementById('r-hadm');if(hadm)hadm.value=fmtTime();
  var r=getDateRange('mes');
  var fi=document.getElementById('ind-from');if(fi)fi.value=r.start;
  var ti=document.getElementById('ind-to');if(ti)ti.value=r.end;
  var sf=document.getElementById('saidas-from');if(sf)sf.value=todayKey().slice(0,7)+'-01';
  var st=document.getElementById('saidas-to');if(st)st.value=todayKey();
  updateBottomBar();
  setInterval(updateBottomBar,60000);
});
"""

def build_html():
    nav = """
<nav class="sidebar" id="sidebar">
  <div class="nav-section-lbl">Gestão</div>
  <div class="nav-item active" data-s="registo" onclick="nav('registo')">
    <svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>Registo
  </div>
  <div class="nav-item" data-s="internados" onclick="nav('internados')">
    <svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>Internados
  </div>
  <div class="nav-item" data-s="saidas" onclick="nav('saidas')">
    <svg viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9"/></svg>Saídas
    <span id="notif-badge" class="nav-badge" style="display:none;">0</span>
  </div>
  <div class="nav-item" data-s="movimento" onclick="nav('movimento')">
    <svg viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>Movimento
  </div>
  <div class="nav-section-lbl">Análise</div>
  <div class="nav-item" data-s="indicadores" onclick="nav('indicadores')">
    <svg viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>Indicadores
  </div>
  <div class="nav-item" data-s="diagnosticos" onclick="nav('diagnosticos')">
    <svg viewBox="0 0 24 24"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>Diagnósticos
  </div>
  <div class="nav-item" data-s="pesquisa" onclick="nav('pesquisa')">
    <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>Pesquisa
  </div>
  <div class="nav-section-lbl">Sistema</div>
  <div class="nav-item" data-s="definicoes" onclick="nav('definicoes')">
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
  <div style="margin-top:14px;font-family:'Inter',sans-serif;font-size:.85rem;font-weight:700;color:#fff;">Hospital do Prenda</div>
  <div style="font-size:.68rem;color:rgba(255,255,255,.5);margin-top:4px;">Serviço de Ortopedia / Medicina</div>
  <div id="spl-pct" style="font-size:.6rem;color:rgba(255,255,255,.35);margin-top:8px;">0%</div>
</div>"""

    bottom_bar = """
<div class="bottom-bar">
  <div class="bb-stat">
    <span class="bb-label">Data:</span>
    <span id="bb-date" class="bb-val" style="color:rgba(255,255,255,.9);font-size:.65rem;"></span>
  </div>
  <div class="bb-stat">
    <span class="bb-label">Internados:</span>
    <span id="bb-internados" class="bb-val blue">0</span>
  </div>
  <div class="bb-stat">
    <span class="bb-label">Entrados hoje:</span>
    <span id="bb-entrados" class="bb-val green">0</span>
  </div>
  <div class="bb-stat">
    <span class="bb-label">Saídos hoje:</span>
    <span id="bb-saidos" class="bb-val amber">0</span>
  </div>
  <div class="bb-stat">
    <span class="bb-label">Óbitos hoje:</span>
    <span id="bb-obitos" class="bb-val red">0</span>
  </div>
  <div style="margin-left:auto;padding-right:16px;font-size:.58rem;color:rgba(255,255,255,.35);">Ortopedia/Medicina v2</div>
</div>"""

    hosp_img = HOSP_IMG.replace("'", "\\'")

    modal_login_html = MODAL_LOGIN.replace('__HOSP_IMG__', HOSP_IMG)

    html = f"""<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ortopedia/Medicina — Hospital do Prenda</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
{splash}

{modal_login_html}
{MODAL_SAIDA}
{MODAL_FICHA}
{MODAL_EDIT}
{MODAL_DEL}

<header>
  <div class="header-logo"><img src="{HOSP_IMG}" alt="Logo"></div>
  <div class="header-title">
    <h1>Hospital do Prenda</h1>
    <span>Serviço de Ortopedia / Medicina</span>
  </div>
  <div style="margin-left:auto;display:flex;align-items:center;gap:8px;">
    <button class="btn btn-outline btn-sm" onclick="toggleTheme()" title="Alternar tema">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
    </button>
  </div>
</header>

<div class="hp-staff-bar">
  <span class="hp-staff-lbl">Utilizador:</span>
  <span class="hp-staff-name" id="staff-name">—</span>
  <span class="hp-staff-sep">|</span>
  <span class="hp-staff-lbl">Serviço:</span>
  <span>Ortopedia/Medicina</span>
  <span style="margin-left:auto;"></span>
  <button class="hbtn" onclick="doLogout()">Sair</button>
</div>

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

{bottom_bar}

<div id="toast" style="display:none;position:fixed;bottom:50px;right:24px;padding:10px 18px;border-radius:10px;font-size:.76rem;font-weight:600;z-index:9000;box-shadow:0 4px 20px rgba(0,0,0,.25);transition:opacity .3s,transform .3s;"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.8.2/jspdf.plugin.autotable.min.js"></script>
<script>
(function(){{
  var th=localStorage.getItem('hp_orto_theme')||'light';
  if(th==='dark')document.documentElement.classList.add('dark');
}})();
</script>
<script>{JS}</script>
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
