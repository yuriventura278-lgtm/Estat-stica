#!/usr/bin/env python3
"""Build cirurgia_geral.html — standalone Cirurgia Geral BU form."""

with open('/tmp/logo_splash.txt') as f:
    LOGO = f.read().strip()

# ── STYLES ────────────────────────────────────────────────────────────────────
CSS = """
:root{
  --bg:#fafaf9;--s1:#fff;--s2:#f5f5f4;--bd:#e7e5e4;
  --txt:#1c1917;--mut:#78716c;--acc:oklch(43% 0.1 230);
  --acc2:oklch(55% 0.12 230);--grn:#059669;--red:#dc2626;
  --war:#d97706;--sw:220px;--hh:58px;--r:10px;--r2:6px;
  --sh:0 2px 8px rgba(0,0,0,.07)
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;font-family:'Inter',system-ui,sans-serif;background:var(--bg);color:var(--txt);font-size:14px}

header{position:fixed;top:0;left:0;right:0;height:var(--hh);
  background:oklch(20% 0.08 230);display:flex;align-items:center;
  padding:0 18px;gap:12px;z-index:1000;box-shadow:0 2px 10px rgba(0,0,0,.2)}
.h-logo{height:36px;width:36px;object-fit:contain;border-radius:4px}
.h-ti{color:#fff;font-weight:700;font-size:.95rem;line-height:1.2}
.h-su{color:rgba(255,255,255,.5);font-size:.7rem}
.h-sp{flex:1}
.h-date{color:rgba(255,255,255,.6);font-size:.78rem;font-family:'IBM Plex Mono',monospace}
.h-btn{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);
  color:#fff;padding:7px 13px;border-radius:7px;cursor:pointer;font-size:.8rem;
  font-weight:500;transition:.15s;white-space:nowrap;display:inline-flex;align-items:center;gap:5px}
.h-btn:hover{background:rgba(255,255,255,.22)}
.h-btn.grn{background:rgba(5,150,105,.35);border-color:rgba(5,150,105,.5)}
.h-btn.grn:hover{background:rgba(5,150,105,.5)}
.h-btn.wa{background:rgba(37,211,102,.25);border-color:rgba(37,211,102,.4)}
.h-btn.wa:hover{background:rgba(37,211,102,.4)}

.sidebar{position:fixed;top:var(--hh);left:0;bottom:0;width:var(--sw);
  background:var(--s1);border-right:1px solid var(--bd);
  display:flex;flex-direction:column;z-index:100;overflow-y:auto}
.nav-item{display:flex;align-items:center;gap:10px;padding:11px 16px;cursor:pointer;
  font-size:.83rem;color:var(--mut);transition:.15s;border-left:3px solid transparent;user-select:none}
.nav-item:hover{background:var(--s2);color:var(--txt)}
.nav-item.active{background:#e0eeff;color:var(--acc);border-left-color:var(--acc2);font-weight:600}
.nav-ico{font-size:1rem;min-width:20px;text-align:center;flex-shrink:0}
.nav-sep{height:1px;background:var(--bd);margin:5px 14px}
.nav-badge{margin-left:auto;background:var(--acc);color:#fff;border-radius:10px;
  padding:1px 7px;font-size:.68rem;font-weight:700}
.sb-footer{padding:12px 14px;font-size:.74rem;color:var(--mut);
  border-top:1px solid var(--bd);margin-top:auto;line-height:1.6}
.sb-footer strong{color:var(--txt)}

.main{margin-left:var(--sw);margin-top:var(--hh);padding:22px;min-height:calc(100vh - var(--hh))}
.sec{display:none}.sec.active{display:block}
.pg-ti{font-size:1.35rem;font-weight:700;margin-bottom:3px}
.pg-su{color:var(--mut);font-size:.82rem;margin-bottom:20px}

.card{background:var(--s1);border-radius:var(--r);border:1px solid var(--bd);padding:18px;
  box-shadow:var(--sh);margin-bottom:16px}
.card-ti{font-size:.78rem;font-weight:700;color:var(--txt);text-transform:uppercase;
  letter-spacing:.05em;margin-bottom:14px;display:flex;align-items:center;gap:7px;
  padding-bottom:10px;border-bottom:1px solid var(--bd)}

.kpi-row{display:grid;grid-template-columns:repeat(auto-fill,minmax(125px,1fr));gap:12px;margin-bottom:18px}
.kpi{background:var(--s1);border-radius:var(--r);border:1px solid var(--bd);padding:14px 16px;
  text-align:center;box-shadow:var(--sh)}
.kpi-val{font-size:2rem;font-weight:800;line-height:1;color:var(--acc)}
.kpi-val.grn{color:var(--grn)}.kpi-val.red{color:var(--red)}.kpi-val.war{color:var(--war)}
.kpi-lbl{font-size:.68rem;color:var(--mut);text-transform:uppercase;letter-spacing:.05em;margin-top:4px}

.fg{display:flex;flex-direction:column;gap:4px}
.fg label{font-size:.74rem;font-weight:700;color:var(--mut);text-transform:uppercase;letter-spacing:.04em}
.fg input,.fg select,.fg textarea{padding:8px 10px;border:1.5px solid var(--bd);border-radius:var(--r2);
  background:var(--s1);color:var(--txt);font-family:inherit;font-size:.875rem;
  transition:border-color .15s;outline:none}
.fg input:focus,.fg select:focus,.fg textarea:focus{border-color:var(--acc2)}
.fg textarea{resize:vertical;min-height:70px}

.fgrid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:14px}
.fgrid.g3{grid-template-columns:1fr 1fr 1fr}
.full{grid-column:1/-1}

.radio-g{display:flex;gap:6px;flex-wrap:wrap;padding:4px 0}
.radio-btn{display:inline-flex;align-items:center;gap:5px;padding:6px 12px;
  border:1.5px solid var(--bd);border-radius:20px;cursor:pointer;font-size:.8rem;
  font-weight:500;transition:.15s;user-select:none}
.radio-btn:hover{border-color:var(--acc2)}
.radio-btn.sel{border-color:var(--acc);background:#e0eeff;color:var(--acc);font-weight:600}
.radio-btn input{display:none}

.med-list{display:flex;flex-direction:column;gap:6px;margin-top:6px}
.med-row{display:flex;gap:6px;align-items:center}
.med-row input{flex:1;padding:7px 10px;border:1.5px solid var(--bd);border-radius:var(--r2);
  background:var(--s1);font-family:inherit;font-size:.875rem;outline:none;transition:border-color .15s}
.med-row input:focus{border-color:var(--acc2)}
.med-row .rm-btn{padding:5px 9px;border:1.5px solid var(--bd);background:var(--s2);
  border-radius:6px;cursor:pointer;color:var(--red);font-size:.85rem;line-height:1;transition:.15s}
.med-row .rm-btn:hover{background:#fee2e2;border-color:var(--red)}
.add-btn{padding:6px 14px;border:1.5px dashed var(--bd);border-radius:var(--r2);
  background:transparent;color:var(--mut);font-size:.8rem;font-weight:600;
  cursor:pointer;transition:.15s;text-align:left;width:100%;font-family:inherit}
.add-btn:hover{border-color:var(--acc2);color:var(--acc);background:var(--s2)}

.tbl-wrap{overflow-x:auto}
table.tbl{width:100%;border-collapse:collapse}
table.tbl th{background:var(--s2);font-size:.72rem;font-weight:700;text-transform:uppercase;
  letter-spacing:.04em;color:var(--mut);padding:9px 10px;text-align:left;
  border-bottom:2px solid var(--bd);white-space:nowrap}
table.tbl td{padding:9px 10px;border-bottom:1px solid var(--bd);font-size:.82rem;
  color:var(--txt);vertical-align:middle}
table.tbl tr:last-child td{border-bottom:none}
table.tbl tr:hover td{background:var(--s2)}
.badge{display:inline-flex;align-items:center;padding:2px 8px;border-radius:10px;
  font-size:.7rem;font-weight:600;white-space:nowrap}
.badge.urg{background:#fee2e2;color:var(--red)}
.badge.ele{background:#dcfce7;color:var(--grn)}
.badge.semi{background:#fef3c7;color:var(--war)}
.badge.comp{background:#fef3c7;color:var(--war)}
.badge.obt{background:#fee2e2;color:var(--red)}
.badge.ok{background:#dcfce7;color:var(--grn)}
.badge.m{background:#dbeafe;color:#1e40af}
.badge.f{background:#fce7f3;color:#9d174d}

.btn{padding:9px 20px;border-radius:8px;border:none;cursor:pointer;font-family:inherit;
  font-size:.82rem;font-weight:600;transition:.15s;display:inline-flex;align-items:center;gap:6px}
.btn-pri{background:var(--acc);color:#fff}.btn-pri:hover{opacity:.88}
.btn-sec{background:var(--s2);border:1.5px solid var(--bd);color:var(--txt)}.btn-sec:hover{background:var(--bd)}
.btn-grn{background:var(--grn);color:#fff}.btn-grn:hover{opacity:.88}
.btn-red{background:var(--red);color:#fff}.btn-red:hover{opacity:.88}
.btn-sm{padding:6px 14px;font-size:.78rem}
.btn-xs{padding:4px 9px;font-size:.73rem}

.equipa-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px}

.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);
  background:#1c1917;color:#fff;padding:10px 20px;border-radius:8px;font-size:.83rem;
  z-index:9999;opacity:0;transition:opacity .3s;pointer-events:none;white-space:nowrap}
.toast.show{opacity:1}

.empty{text-align:center;padding:48px 20px;color:var(--mut)}
.empty-ico{font-size:2.5rem;margin-bottom:10px}
.empty h3{font-size:.9rem;color:var(--txt);margin-bottom:4px}

@media(max-width:768px){
  :root{--sw:0px}
  .sidebar{width:220px;transform:translateX(-220px);transition:.3s}
  .sidebar.open{transform:translateX(0)}
  .main{margin-left:0}
  .equipa-grid,.fgrid,.fgrid.g3{grid-template-columns:1fr}
}
"""

# ── HTML BODY ────────────────────────────────────────────────────────────────
BODY = """
<!-- HEADER -->
<header>
  <img class="h-logo" src="__LOGO__" alt="HP">
  <div>
    <div class="h-ti">Cirurgia Geral — Banco de Urgência</div>
    <div class="h-su">Hospital do Prenda · Luanda</div>
  </div>
  <div class="h-sp"></div>
  <span class="h-date" id="hdr-date"></span>
  <button class="h-btn wa" onclick="shareWhatsApp()">
    <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347"/></svg>
    WhatsApp
  </button>
  <button class="h-btn grn" onclick="exportPDF()" style="margin-left:6px">
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14,2 14,8 20,8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
    PDF Reunião
  </button>
  <button class="h-btn" onclick="showSec('registo')" style="margin-left:6px">
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
    Registo
  </button>
</header>

<!-- SIDEBAR -->
<nav class="sidebar" id="sidebar">
  <div class="nav-item active" id="nb-dash" onclick="showSec('dash')">
    <span class="nav-ico">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
    </span>
    Painel
  </div>
  <div class="nav-item" id="nb-equipa" onclick="showSec('equipa')">
    <span class="nav-ico">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
    </span>
    Equipa Médica
  </div>
  <div class="nav-item" id="nb-registo" onclick="showSec('registo')">
    <span class="nav-ico">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
    </span>
    Novo Registo
  </div>
  <div class="nav-item" id="nb-lista" onclick="showSec('lista')">
    <span class="nav-ico">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
    </span>
    Doentes Registados
    <span class="nav-badge" id="nb-cnt">0</span>
  </div>
  <div class="nav-sep"></div>
  <div class="nav-item" id="nb-relat" onclick="showSec('relat')">
    <span class="nav-ico">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22,12 18,12 15,21 9,3 6,12 2,12"/></svg>
    </span>
    Estatísticas
  </div>
  <div class="sb-footer">
    <strong id="sb-total">0</strong> intervenções<br>
    <strong id="sb-today"></strong>
  </div>
</nav>

<!-- MAIN -->
<main class="main">

<!-- ═══ PAINEL ═══ -->
<div class="sec active" id="sec-dash">
  <div class="pg-ti">Painel do Dia</div>
  <div class="pg-su" id="dash-date">—</div>
  <div class="kpi-row">
    <div class="kpi"><div class="kpi-val" id="kpi-total">0</div><div class="kpi-lbl">Total</div></div>
    <div class="kpi"><div class="kpi-val war" id="kpi-urg">0</div><div class="kpi-lbl">Urgentes</div></div>
    <div class="kpi"><div class="kpi-val grn" id="kpi-ele">0</div><div class="kpi-lbl">Eletivas</div></div>
    <div class="kpi"><div class="kpi-val war" id="kpi-comp">0</div><div class="kpi-lbl">Complicações</div></div>
    <div class="kpi"><div class="kpi-val red" id="kpi-obt">0</div><div class="kpi-lbl">Óbitos</div></div>
    <div class="kpi"><div class="kpi-val" id="kpi-men">0</div><div class="kpi-lbl">&lt;15 Anos</div></div>
  </div>
  <div class="card">
    <div class="card-ti">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
      Equipa de Serviço
    </div>
    <div id="dash-equipa" style="font-size:.85rem;color:var(--mut)">
      Nenhuma equipa configurada. <a href="#" onclick="showSec('equipa');return false" style="color:var(--acc)">Configurar agora</a>
    </div>
  </div>
  <div class="card">
    <div class="card-ti">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v11m0 0H5m4 0h4"/></svg>
      Últimas Intervenções
    </div>
    <div id="dash-recent"></div>
  </div>
</div>

<!-- ═══ EQUIPA ═══ -->
<div class="sec" id="sec-equipa">
  <div class="pg-ti">Equipa Médica</div>
  <div class="pg-su">Configure a equipa de serviço para hoje</div>
  <div class="card">
    <div class="fgrid" style="margin-bottom:18px">
      <div class="fg">
        <label>Data de Serviço</label>
        <input type="date" id="eq-data" onchange="saveEquipa()">
      </div>
      <div class="fg">
        <label>Turno</label>
        <select id="eq-turno" onchange="saveEquipa()">
          <option value="manha">Manhã (07h–13h)</option>
          <option value="tarde">Tarde (13h–19h)</option>
          <option value="noite">Noite (19h–07h)</option>
          <option value="24h">24 Horas</option>
        </select>
      </div>
    </div>
    <div class="equipa-grid">
      <div>
        <div style="font-size:.74rem;font-weight:700;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);margin-bottom:8px">
          Médico Especialista
        </div>
        <div class="fg" style="margin-bottom:8px">
          <input type="text" id="eq-especialista" placeholder="Nome do especialista" oninput="saveEquipa()">
        </div>
        <div class="fg">
          <label>Categoria</label>
          <select id="eq-esp-cat" onchange="saveEquipa()">
            <option value="Cirurgião Sénior">Cirurgião Sénior</option>
            <option value="Cirurgião">Cirurgião</option>
            <option value="Assistente Hospitalar">Assistente Hospitalar</option>
            <option value="Assistente Principal">Assistente Principal</option>
          </select>
        </div>
      </div>
      <div>
        <div style="font-size:.74rem;font-weight:700;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);margin-bottom:8px">
          Médicos Internos
        </div>
        <div class="med-list" id="list-internos"></div>
        <button class="add-btn" onclick="addMedico('internos')" style="margin-top:6px">
          + Adicionar Médico Interno
        </button>
      </div>
      <div>
        <div style="font-size:.74rem;font-weight:700;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);margin-bottom:8px">
          Médicos Estagiários
        </div>
        <div class="med-list" id="list-estagiarios"></div>
        <button class="add-btn" onclick="addMedico('estagiarios')" style="margin-top:6px">
          + Adicionar Estagiário
        </button>
      </div>
    </div>
    <div style="margin-top:18px;display:flex;gap:10px;flex-wrap:wrap">
      <button class="btn btn-pri" onclick="saveEquipa();toast('Equipa guardada')">Guardar Equipa</button>
      <button class="btn btn-sec" onclick="showSec('registo')">Ir para Registo →</button>
    </div>
  </div>
</div>

<!-- ═══ REGISTO ═══ -->
<div class="sec" id="sec-registo">
  <div class="pg-ti">Novo Registo Cirúrgico</div>
  <div class="pg-su">Preencha os dados da intervenção cirúrgica</div>
  <div class="card">
    <div class="card-ti">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
      Identificação do Doente
    </div>
    <div class="fgrid">
      <div class="fg">
        <label>Nome (opcional)</label>
        <input type="text" id="r-nome" placeholder="Nome completo">
      </div>
      <div class="fg">
        <label>Nº Processo</label>
        <input type="text" id="r-proc" placeholder="Número de processo / BI">
      </div>
      <div class="fg">
        <label>Sexo</label>
        <div class="radio-g" id="rg-sexo">
          <label class="radio-btn"><input type="radio" name="rsexo" value="M" onchange="markRadio('rg-sexo',this)"> Masculino</label>
          <label class="radio-btn"><input type="radio" name="rsexo" value="F" onchange="markRadio('rg-sexo',this)"> Feminino</label>
        </div>
      </div>
      <div class="fg">
        <label>Idade (anos)</label>
        <input type="number" id="r-idade" min="0" max="120" placeholder="Idade">
      </div>
      <div class="fg">
        <label>Data de Entrada</label>
        <input type="date" id="r-data">
      </div>
      <div class="fg">
        <label>Hora de Entrada</label>
        <input type="time" id="r-hora">
      </div>
    </div>

    <div class="card-ti" style="margin-top:6px">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
      Tipologia da Intervenção
    </div>
    <div class="fgrid">
      <div class="fg">
        <label>Tipo</label>
        <div class="radio-g" id="rg-tipo">
          <label class="radio-btn"><input type="radio" name="rtipo" value="urgente" onchange="markRadio('rg-tipo',this)"> Urgente</label>
          <label class="radio-btn"><input type="radio" name="rtipo" value="eletiva" onchange="markRadio('rg-tipo',this)"> Eletiva</label>
          <label class="radio-btn"><input type="radio" name="rtipo" value="semiurgente" onchange="markRadio('rg-tipo',this)"> Semiurgente</label>
        </div>
      </div>
      <div class="fg">
        <label>ASA (Risco Anestésico)</label>
        <select id="r-asa">
          <option value="">— Selecionar —</option>
          <option value="ASA I">ASA I — Saudável</option>
          <option value="ASA II">ASA II — Doença sistémica leve</option>
          <option value="ASA III">ASA III — Doença sistémica grave</option>
          <option value="ASA IV">ASA IV — Risco de vida constante</option>
          <option value="ASA V">ASA V — Moribundo</option>
        </select>
      </div>
    </div>

    <div class="card-ti" style="margin-top:6px">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
      Diagnóstico e Procedimento
    </div>
    <div class="fgrid">
      <div class="fg">
        <label>Diagnóstico / Patologia</label>
        <select id="r-diag" onchange="handleDiagChange()">
          <option value="">— Selecionar —</option>
          <option>Apendicite aguda</option>
          <option>Hérnia inguinal</option>
          <option>Hérnia umbilical</option>
          <option>Hérnia epigástrica</option>
          <option>Oclusão intestinal</option>
          <option>Peritonite</option>
          <option>Abcesso abdominal</option>
          <option>Trauma abdominal</option>
          <option>Colelitíase / Colecistite</option>
          <option>Úlcera péptica perfurada</option>
          <option>Volvo intestinal</option>
          <option>Fístula</option>
          <option>Neoplasia colo-retal</option>
          <option>Neoplasia gástrica</option>
          <option>Neoplasia hepática</option>
          <option>Neoplasia pancreática</option>
          <option>Hemorróidas</option>
          <option>Fissura anal</option>
          <option>Abcesso perianal</option>
          <option>Torção testicular</option>
          <option>Trauma vascular</option>
          <option>Lipoma / Quisto</option>
          <option value="Outro">Outro (especificar)</option>
        </select>
      </div>
      <div class="fg" id="fg-diag-outro" style="display:none">
        <label>Especificar Diagnóstico</label>
        <input type="text" id="r-diag-outro" placeholder="Descrever diagnóstico">
      </div>
      <div class="fg">
        <label>Procedimento Cirúrgico</label>
        <select id="r-proc-cir">
          <option value="">— Selecionar —</option>
          <option>Apendicectomia</option>
          <option>Herniorrafia inguinal</option>
          <option>Herniorrafia umbilical</option>
          <option>Herniorrafia epigástrica</option>
          <option>Laparotomia exploradora</option>
          <option>Laparotomia + ressecção intestinal</option>
          <option>Colecistectomia aberta</option>
          <option>Colecistectomia laparoscópica</option>
          <option>Drenagem de abcesso</option>
          <option>Rafia de perfuração</option>
          <option>Desvolvulação intestinal</option>
          <option>Colostomia</option>
          <option>Hemorroidectomia</option>
          <option>Fistulotomia</option>
          <option>Orquidopexia</option>
          <option>Orquiectomia</option>
          <option>Excisão de massa / tumor</option>
          <option>Desbridamento cirúrgico</option>
          <option>Amputação</option>
          <option>Outro</option>
        </select>
      </div>
      <div class="fg">
        <label>Via de Acesso</label>
        <select id="r-via">
          <option value="aberta">Cirurgia Aberta</option>
          <option value="laparoscopica">Laparoscópica</option>
          <option value="endoscopica">Endoscópica</option>
          <option value="percutanea">Percutânea</option>
        </select>
      </div>
      <div class="fg">
        <label>Tipo de Anestesia</label>
        <select id="r-anest">
          <option value="geral">Geral</option>
          <option value="raquidiana">Raquidiana / Espinal</option>
          <option value="epidural">Epidural</option>
          <option value="local">Local</option>
          <option value="sedacao">Sedação</option>
          <option value="nenhuma">Sem Anestesia</option>
        </select>
      </div>
    </div>

    <div class="card-ti" style="margin-top:6px">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
      Equipa Cirúrgica
    </div>
    <div class="fgrid g3" style="margin-bottom:14px">
      <div class="fg">
        <label>Cirurgião Principal</label>
        <input type="text" id="r-cirurgiao" placeholder="Nome do cirurgião">
      </div>
      <div class="fg">
        <label>1.º Ajudante</label>
        <input type="text" id="r-ajud1" placeholder="Nome">
      </div>
      <div class="fg">
        <label>2.º Ajudante</label>
        <input type="text" id="r-ajud2" placeholder="Nome (opcional)">
      </div>
      <div class="fg">
        <label>Anestesista</label>
        <input type="text" id="r-anestesista" placeholder="Nome do anestesista">
      </div>
      <div class="fg">
        <label>Enfermeiro Instrumentista</label>
        <input type="text" id="r-enf" placeholder="Nome do enfermeiro">
      </div>
    </div>

    <div class="card-ti" style="margin-top:6px">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20,6 9,17 4,12"/></svg>
      Resultado Pós-Operatório
    </div>
    <div class="fgrid">
      <div class="fg">
        <label>Resultado da Intervenção</label>
        <div class="radio-g" id="rg-resultado">
          <label class="radio-btn"><input type="radio" name="rresultado" value="ok" onchange="markRadio('rg-resultado',this)"> Sem intercorrências</label>
          <label class="radio-btn"><input type="radio" name="rresultado" value="complicacao" onchange="markRadio('rg-resultado',this);showComp(true)"> Complicação</label>
          <label class="radio-btn"><input type="radio" name="rresultado" value="obito" onchange="markRadio('rg-resultado',this);showComp(false)"> Óbito</label>
        </div>
      </div>
      <div class="fg" id="fg-comp" style="display:none">
        <label>Descrever Complicação</label>
        <input type="text" id="r-comp-desc" placeholder="Ex: Hemorragia intraoperatória">
      </div>
      <div class="fg">
        <label>Destino Pós-Operatório</label>
        <select id="r-destino">
          <option value="enfermaria">Enfermaria</option>
          <option value="uci">UCI / Cuidados Intensivos</option>
          <option value="recobro">Recobro / UCPA</option>
          <option value="alta">Alta imediata</option>
          <option value="transferencia">Transferência</option>
          <option value="obito">Óbito</option>
        </select>
      </div>
      <div class="fg full">
        <label>Observações / Notas Clínicas</label>
        <textarea id="r-obs" placeholder="Notas clínicas, intercorrências, observações adicionais…"></textarea>
      </div>
    </div>

    <div style="display:flex;gap:10px;justify-content:flex-end;flex-wrap:wrap;margin-top:8px">
      <button class="btn btn-sec" onclick="clearForm()">Limpar</button>
      <button class="btn btn-pri" onclick="guardarRegisto()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17,21 17,13 7,13 7,21"/><polyline points="7,3 7,8 15,8"/></svg>
        Guardar Registo
      </button>
    </div>
  </div>
</div>

<!-- ═══ LISTA ═══ -->
<div class="sec" id="sec-lista">
  <div class="pg-ti">Doentes Registados</div>
  <div class="pg-su" id="lista-date">Hoje</div>
  <div style="display:flex;gap:10px;margin-bottom:16px;align-items:center;flex-wrap:wrap">
    <input type="date" id="lista-filtro" style="padding:8px 10px;border:1.5px solid var(--bd);border-radius:var(--r2);font-family:inherit;font-size:.875rem" onchange="renderLista()">
    <button class="btn btn-sec btn-sm" onclick="document.getElementById('lista-filtro').value='';renderLista()">Todos</button>
    <div style="flex:1"></div>
    <button class="btn btn-pri btn-sm" onclick="showSec('registo')">+ Novo Registo</button>
  </div>
  <div class="card">
    <div id="lista-body"></div>
  </div>
</div>

<!-- ═══ ESTATÍSTICAS ═══ -->
<div class="sec" id="sec-relat">
  <div class="pg-ti">Estatísticas</div>
  <div class="pg-su">Análise por período</div>
  <div style="display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap;align-items:center">
    <button class="btn btn-pri btn-sm" id="p-dia" onclick="setPeriod('dia',this)">Hoje</button>
    <button class="btn btn-sec btn-sm" id="p-sem" onclick="setPeriod('semana',this)">Semana</button>
    <button class="btn btn-sec btn-sm" id="p-mes" onclick="setPeriod('mes',this)">Mês</button>
    <input type="date" id="stat-from" style="padding:6px 10px;border:1.5px solid var(--bd);border-radius:var(--r2);font-size:.8rem;font-family:inherit" onchange="setPeriod('custom',null)">
    <span style="color:var(--mut);font-size:.8rem">→</span>
    <input type="date" id="stat-to" style="padding:6px 10px;border:1.5px solid var(--bd);border-radius:var(--r2);font-size:.8rem;font-family:inherit" onchange="setPeriod('custom',null)">
  </div>
  <div class="kpi-row" id="stat-kpis"></div>
  <div class="card">
    <div class="card-ti">Demografias (Sexo × Faixa Etária)</div>
    <div class="tbl-wrap"><table class="tbl" id="stat-demo-tbl"></table></div>
  </div>
  <div class="card">
    <div class="card-ti">Por Diagnóstico</div>
    <div class="tbl-wrap"><table class="tbl" id="stat-diag-tbl"></table></div>
  </div>
  <div class="card">
    <div class="card-ti">Por Procedimento</div>
    <div class="tbl-wrap"><table class="tbl" id="stat-proc-tbl"></table></div>
  </div>
</div>

</main>
<div class="toast" id="toast"></div>
"""

# ── JAVASCRIPT ────────────────────────────────────────────────────────────────
JS = r"""
(function(){
'use strict';

const SK = 'cg_bu_v1';
const LOGO_B64 = '__LOGO__';

let state = {
  equipa: { data:'', turno:'manha', especialista:'', espCat:'Cirurgiao Senior', internos:[], estagiarios:[] },
  registos: []
};
let editId = null;
let statFrom = '', statTo = '';

/* ── INIT ── */
function init(){
  const saved = localStorage.getItem(SK);
  if(saved){ try{ state = JSON.parse(saved); }catch(e){} }
  const today = todayStr();
  if(!state.equipa) state.equipa = { data:today, turno:'manha', especialista:'', espCat:'Cirurgiao Senior', internos:[], estagiarios:[] };
  if(!state.registos) state.registos = [];
  document.getElementById('eq-data').value = state.equipa.data || today;
  document.getElementById('eq-turno').value = state.equipa.turno || 'manha';
  document.getElementById('eq-especialista').value = state.equipa.especialista || '';
  document.getElementById('eq-esp-cat').value = state.equipa.espCat || 'Cirurgiao Senior';
  renderMedicos('internos');
  renderMedicos('estagiarios');
  document.getElementById('r-data').value = today;
  document.getElementById('r-hora').value = nowTime();
  document.getElementById('lista-filtro').value = today;
  document.getElementById('hdr-date').textContent = fmtDateShort(today);
  document.getElementById('sb-today').textContent = fmtDateShort(today);
  document.getElementById('dash-date').textContent = fmtDate(today);
  setPeriod('dia', document.getElementById('p-dia'));
  renderDash();
  renderLista();
  renderStat();
  updateBadge();
}

/* ── SAVE ── */
function save(){ localStorage.setItem(SK, JSON.stringify(state)); }

/* ── HELPERS ── */
function todayStr(){ return new Date().toISOString().slice(0,10); }
function nowTime(){ return new Date().toTimeString().slice(0,5); }
function uid(){ return Date.now().toString(36)+Math.random().toString(36).slice(2,6); }
function fmtDate(s){
  if(!s) return '';
  const d = new Date(s+'T12:00:00');
  return d.toLocaleDateString('pt-PT',{weekday:'long',day:'numeric',month:'long',year:'numeric'});
}
function fmtDateShort(s){
  if(!s) return '';
  const d = new Date(s+'T12:00:00');
  return d.toLocaleDateString('pt-PT',{day:'numeric',month:'short',year:'numeric'});
}
function ageGroup(a){ return parseInt(a)<15?'<15':'≥15'; }
function escH(s){ return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

function toast(msg, ok){
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.style.background = ok===false ? '#dc2626' : '#059669';
  t.classList.add('show');
  setTimeout(function(){ t.classList.remove('show'); }, 2600);
}
window.toast = toast;

/* ── NAV ── */
function showSec(id){
  document.querySelectorAll('.sec').forEach(function(s){ s.classList.remove('active'); });
  document.querySelectorAll('.nav-item').forEach(function(n){ n.classList.remove('active'); });
  document.getElementById('sec-'+id).classList.add('active');
  var nb = document.getElementById('nb-'+id);
  if(nb) nb.classList.add('active');
  if(id==='lista') renderLista();
  if(id==='relat') renderStat();
  if(id==='dash') renderDash();
}
window.showSec = showSec;

/* ── RADIO ── */
function markRadio(grpId, inp){
  document.querySelectorAll('#'+grpId+' .radio-btn').forEach(function(b){ b.classList.remove('sel'); });
  var btn = inp.closest('.radio-btn');
  if(btn) btn.classList.add('sel');
}
window.markRadio = markRadio;

function showComp(show){ document.getElementById('fg-comp').style.display = show ? 'flex' : 'none'; }
window.showComp = showComp;

function handleDiagChange(){
  var v = document.getElementById('r-diag').value;
  document.getElementById('fg-diag-outro').style.display = v==='Outro' ? 'flex' : 'none';
}
window.handleDiagChange = handleDiagChange;

function getRadio(name){
  var el = document.querySelector('input[name="r'+name+'"]:checked');
  return el ? el.value : '';
}

function setRadioVal(name, val){
  document.querySelectorAll('input[name="r'+name+'"]').forEach(function(inp){
    if(inp.value===val){
      inp.checked = true;
      var grp = inp.closest('[id^="rg-"]');
      if(grp) grp.querySelectorAll('.radio-btn').forEach(function(b){ b.classList.remove('sel'); });
      var btn = inp.closest('.radio-btn');
      if(btn) btn.classList.add('sel');
    }
  });
}

/* ── MEDICOS ── */
function renderMedicos(tipo){
  var list = document.getElementById('list-'+tipo);
  var arr = state.equipa[tipo] || [];
  list.innerHTML = arr.map(function(m,i){
    return '<div class="med-row"><input type="text" value="'+escH(m)+'" placeholder="Nome do médico" oninput="updateMedico(\''+tipo+'\','+i+',this.value)"><button class="rm-btn" onclick="removeMedico(\''+tipo+'\','+i+')">✕</button></div>';
  }).join('');
}

function addMedico(tipo){
  if(!state.equipa[tipo]) state.equipa[tipo] = [];
  state.equipa[tipo].push('');
  renderMedicos(tipo);
  save();
}
window.addMedico = addMedico;

function removeMedico(tipo, idx){
  state.equipa[tipo].splice(idx, 1);
  renderMedicos(tipo);
  save();
}
window.removeMedico = removeMedico;

function updateMedico(tipo, idx, val){
  state.equipa[tipo][idx] = val;
  save();
}
window.updateMedico = updateMedico;

/* ── EQUIPA ── */
function saveEquipa(){
  state.equipa.data = document.getElementById('eq-data').value;
  state.equipa.turno = document.getElementById('eq-turno').value;
  state.equipa.especialista = document.getElementById('eq-especialista').value;
  state.equipa.espCat = document.getElementById('eq-esp-cat').value;
  save();
  renderDash();
}
window.saveEquipa = saveEquipa;

/* ── FORM ── */
function clearForm(){
  ['r-nome','r-proc','r-idade','r-diag-outro','r-cirurgiao','r-ajud1','r-ajud2',
   'r-anestesista','r-enf','r-comp-desc','r-obs'].forEach(function(id){
    var el = document.getElementById(id); if(el) el.value = '';
  });
  ['r-diag','r-proc-cir','r-via','r-anest','r-asa','r-destino'].forEach(function(id){
    var el = document.getElementById(id); if(el) el.selectedIndex = 0;
  });
  document.querySelectorAll('.radio-btn').forEach(function(b){ b.classList.remove('sel'); });
  document.querySelectorAll('input[type=radio]').forEach(function(r){ r.checked = false; });
  document.getElementById('fg-diag-outro').style.display = 'none';
  document.getElementById('fg-comp').style.display = 'none';
  document.getElementById('r-data').value = todayStr();
  document.getElementById('r-hora').value = nowTime();
  editId = null;
}
window.clearForm = clearForm;

function guardarRegisto(){
  var diagSel = document.getElementById('r-diag').value;
  var diagFinal = diagSel==='Outro' ? document.getElementById('r-diag-outro').value : diagSel;
  var sexo = getRadio('sexo');
  var tipo = getRadio('tipo');
  var resultado = getRadio('resultado');
  if(!sexo){ toast('Selecione o sexo do doente', false); return; }
  if(!tipo){ toast('Selecione o tipo de intervenção', false); return; }
  if(!resultado){ toast('Selecione o resultado', false); return; }

  var reg = {
    id: uid(),
    data: document.getElementById('r-data').value || todayStr(),
    hora: document.getElementById('r-hora').value,
    nome: document.getElementById('r-nome').value,
    procNum: document.getElementById('r-proc').value,
    sexo: sexo,
    idade: document.getElementById('r-idade').value,
    tipo: tipo,
    asa: document.getElementById('r-asa').value,
    diag: diagFinal,
    procCir: document.getElementById('r-proc-cir').value,
    via: document.getElementById('r-via').value,
    anest: document.getElementById('r-anest').value,
    cirurgiao: document.getElementById('r-cirurgiao').value,
    ajud1: document.getElementById('r-ajud1').value,
    ajud2: document.getElementById('r-ajud2').value,
    anestesista: document.getElementById('r-anestesista').value,
    enf: document.getElementById('r-enf').value,
    resultado: resultado,
    compDesc: document.getElementById('r-comp-desc').value,
    destino: document.getElementById('r-destino').value,
    obs: document.getElementById('r-obs').value
  };

  if(editId){
    var idx = state.registos.findIndex(function(r){ return r.id===editId; });
    if(idx>=0){ reg.id = editId; state.registos[idx] = reg; }
    editId = null;
  } else {
    state.registos.push(reg);
  }

  save(); clearForm(); updateBadge(); renderDash();
  toast('Registo guardado');
  showSec('lista');
}
window.guardarRegisto = guardarRegisto;

/* ── BADGE ── */
function updateBadge(){
  var today = todayStr();
  var cnt = state.registos.filter(function(r){ return r.data===today; }).length;
  document.getElementById('nb-cnt').textContent = cnt;
  document.getElementById('sb-total').textContent = state.registos.length;
}

/* ── DASH ── */
function renderDash(){
  var today = todayStr();
  var recs = state.registos.filter(function(r){ return r.data===today; });
  document.getElementById('kpi-total').textContent = recs.length;
  document.getElementById('kpi-urg').textContent = recs.filter(function(r){ return r.tipo==='urgente'; }).length;
  document.getElementById('kpi-ele').textContent = recs.filter(function(r){ return r.tipo==='eletiva'||r.tipo==='semiurgente'; }).length;
  document.getElementById('kpi-comp').textContent = recs.filter(function(r){ return r.resultado==='complicacao'; }).length;
  document.getElementById('kpi-obt').textContent = recs.filter(function(r){ return r.resultado==='obito'; }).length;
  document.getElementById('kpi-men').textContent = recs.filter(function(r){ return parseInt(r.idade)<15; }).length;

  var eq = state.equipa;
  var eqHtml = '';
  if(eq.especialista && eq.especialista.trim()){
    eqHtml += '<div style="margin-bottom:8px;font-size:.9rem"><strong>'+escH(eq.especialista)+'</strong> <span style="color:var(--mut);font-size:.78rem">— '+escH(eq.espCat)+'</span></div>';
    var internos = (eq.internos||[]).filter(function(m){ return m.trim(); });
    if(internos.length) eqHtml += '<div style="font-size:.8rem;color:var(--mut);margin-bottom:3px"><em>Internos:</em> '+internos.map(escH).join(', ')+'</div>';
    var estag = (eq.estagiarios||[]).filter(function(m){ return m.trim(); });
    if(estag.length) eqHtml += '<div style="font-size:.8rem;color:var(--mut)"><em>Estagiários:</em> '+estag.map(escH).join(', ')+'</div>';
  } else {
    eqHtml = 'Nenhuma equipa configurada. <a href="#" onclick="showSec(\'equipa\');return false" style="color:var(--acc)">Configurar agora</a>';
  }
  document.getElementById('dash-equipa').innerHTML = eqHtml;

  var recent = recs.slice(-5).reverse();
  if(!recent.length){
    document.getElementById('dash-recent').innerHTML = '<div class="empty"><div class="empty-ico">🔪</div><h3>Sem intervenções hoje</h3><p>Use o botão Registo no topo para adicionar</p></div>';
    return;
  }
  var html = '<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Hora</th><th>Diagnóstico</th><th>Procedimento</th><th>Doente</th><th>Tipo</th><th>Resultado</th></tr></thead><tbody>';
  recent.forEach(function(r){
    var tipoBadge = r.tipo==='urgente'?'<span class="badge urg">Urgente</span>':r.tipo==='eletiva'?'<span class="badge ele">Eletiva</span>':'<span class="badge semi">Semiurg.</span>';
    var resBadge = r.resultado==='ok'?'<span class="badge ok">OK</span>':r.resultado==='complicacao'?'<span class="badge comp">Complicação</span>':'<span class="badge obt">Óbito</span>';
    var sexoBadge = r.sexo==='M'?'<span class="badge m">M</span>':'<span class="badge f">F</span>';
    html += '<tr><td>'+escH(r.hora)+'</td><td>'+escH(r.diag||'—')+'</td><td>'+escH(r.procCir||'—')+'</td><td>'+sexoBadge+(r.idade?' '+escH(r.idade)+'a':'')+'</td><td>'+tipoBadge+'</td><td>'+resBadge+'</td></tr>';
  });
  html += '</tbody></table></div>';
  document.getElementById('dash-recent').innerHTML = html;
}

/* ── LISTA ── */
function renderLista(){
  var filtData = document.getElementById('lista-filtro').value;
  var recs = filtData ? state.registos.filter(function(r){ return r.data===filtData; }) : state.registos.slice();
  recs.sort(function(a,b){ return (a.data+a.hora).localeCompare(b.data+b.hora); });
  var label = filtData ? fmtDate(filtData) : 'Todos os registos';
  document.getElementById('lista-date').textContent = label + ' — ' + recs.length + ' registo(s)';
  if(!recs.length){
    document.getElementById('lista-body').innerHTML = '<div class="empty"><div class="empty-ico">📋</div><h3>Sem registos</h3><p>Adicione intervenções cirúrgicas</p></div>';
    return;
  }
  var html = '<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Data</th><th>Hora</th><th>Diagnóstico</th><th>Procedimento</th><th>Doente</th><th>Tipo</th><th>Resultado</th><th>Destino</th><th></th></tr></thead><tbody>';
  recs.forEach(function(r){
    var tipoBadge = r.tipo==='urgente'?'<span class="badge urg">Urg</span>':r.tipo==='eletiva'?'<span class="badge ele">Ele</span>':'<span class="badge semi">Semi</span>';
    var resBadge = r.resultado==='ok'?'<span class="badge ok">OK</span>':r.resultado==='complicacao'?'<span class="badge comp">Comp</span>':'<span class="badge obt">Óbito</span>';
    var sexoBadge = r.sexo==='M'?'<span class="badge m">M</span>':'<span class="badge f">F</span>';
    html += '<tr><td>'+escH(r.data)+'</td><td>'+escH(r.hora)+'</td><td>'+escH(r.diag||'—')+'</td><td>'+escH(r.procCir||'—')+'</td><td>'+sexoBadge+(r.idade?' '+escH(r.idade)+'a':'')+'</td><td>'+tipoBadge+'</td><td>'+resBadge+'</td><td>'+escH(r.destino||'—')+'</td><td><button class="btn btn-sec btn-xs" onclick="editRegisto(\''+r.id+'\')">Editar</button></td></tr>';
  });
  html += '</tbody></table></div>';
  document.getElementById('lista-body').innerHTML = html;
}
window.renderLista = renderLista;

/* ── EDIT ── */
function editRegisto(id){
  var r = state.registos.find(function(x){ return x.id===id; });
  if(!r) return;
  editId = id;
  document.getElementById('r-nome').value = r.nome||'';
  document.getElementById('r-proc').value = r.procNum||'';
  document.getElementById('r-idade').value = r.idade||'';
  document.getElementById('r-data').value = r.data||todayStr();
  document.getElementById('r-hora').value = r.hora||'';
  document.getElementById('r-diag').value = r.diag||'';
  document.getElementById('r-proc-cir').value = r.procCir||'';
  document.getElementById('r-via').value = r.via||'aberta';
  document.getElementById('r-anest').value = r.anest||'geral';
  document.getElementById('r-asa').value = r.asa||'';
  document.getElementById('r-cirurgiao').value = r.cirurgiao||'';
  document.getElementById('r-ajud1').value = r.ajud1||'';
  document.getElementById('r-ajud2').value = r.ajud2||'';
  document.getElementById('r-anestesista').value = r.anestesista||'';
  document.getElementById('r-enf').value = r.enf||'';
  document.getElementById('r-comp-desc').value = r.compDesc||'';
  document.getElementById('r-destino').value = r.destino||'enfermaria';
  document.getElementById('r-obs').value = r.obs||'';
  setRadioVal('sexo', r.sexo||'');
  setRadioVal('tipo', r.tipo||'');
  setRadioVal('resultado', r.resultado||'');
  if(r.resultado==='complicacao') document.getElementById('fg-comp').style.display='flex';
  showSec('registo');
}
window.editRegisto = editRegisto;

/* ── STAT PERIOD ── */
function setPeriod(p, btn){
  document.querySelectorAll('#sec-relat .btn').forEach(function(b){
    b.classList.remove('btn-pri'); b.classList.add('btn-sec');
  });
  if(btn){ btn.classList.remove('btn-sec'); btn.classList.add('btn-pri'); }
  var today = todayStr();
  var d = new Date(today+'T12:00:00');
  if(p==='dia'){
    statFrom = statTo = today;
  } else if(p==='semana'){
    var dow = d.getDay();
    var mon = new Date(d); mon.setDate(d.getDate()-(dow===0?6:dow-1));
    var sun = new Date(mon); sun.setDate(mon.getDate()+6);
    statFrom = mon.toISOString().slice(0,10);
    statTo = sun.toISOString().slice(0,10);
  } else if(p==='mes'){
    statFrom = today.slice(0,7)+'-01';
    var last = new Date(d.getFullYear(), d.getMonth()+1, 0);
    statTo = last.toISOString().slice(0,10);
  } else {
    statFrom = document.getElementById('stat-from').value || today;
    statTo = document.getElementById('stat-to').value || today;
  }
  if(p!=='custom'){
    document.getElementById('stat-from').value = statFrom;
    document.getElementById('stat-to').value = statTo;
  }
  renderStat();
}
window.setPeriod = setPeriod;

/* ── STAT RENDER ── */
function renderStat(){
  var recs = state.registos.filter(function(r){ return r.data>=statFrom && r.data<=statTo; });
  var total = recs.length;
  var urg = recs.filter(function(r){ return r.tipo==='urgente'; }).length;
  var ele = recs.filter(function(r){ return r.tipo==='eletiva'||r.tipo==='semiurgente'; }).length;
  var comp = recs.filter(function(r){ return r.resultado==='complicacao'; }).length;
  var obt = recs.filter(function(r){ return r.resultado==='obito'; }).length;
  var men = recs.filter(function(r){ return parseInt(r.idade)<15; }).length;

  document.getElementById('stat-kpis').innerHTML =
    kpiC(total,'Total','')+kpiC(urg,'Urgentes','war')+kpiC(ele,'Eletivas','grn')+
    kpiC(comp,'Complicações','war')+kpiC(obt,'Óbitos','red')+kpiC(men,'< 15 anos','');

  var cats = {'M≥15':0,'F≥15':0,'M<15':0,'F<15':0};
  recs.forEach(function(r){ var k=r.sexo+ageGroup(r.idade); cats[k]=(cats[k]||0)+1; });
  var dHtml='<thead><tr><th>Grupo</th><th>N</th><th>%</th></tr></thead><tbody>';
  Object.keys(cats).forEach(function(k){ var v=cats[k]; dHtml+='<tr><td>'+k+'</td><td>'+v+'</td><td>'+(total?Math.round(v/total*100):0)+'%</td></tr>'; });
  dHtml+='<tr style="font-weight:700;background:var(--s2)"><td>Total</td><td>'+total+'</td><td>100%</td></tr></tbody>';
  document.getElementById('stat-demo-tbl').innerHTML=dHtml;

  var diagMap={};
  recs.forEach(function(r){ if(r.diag) diagMap[r.diag]=(diagMap[r.diag]||0)+1; });
  var diagArr=Object.entries(diagMap).sort(function(a,b){ return b[1]-a[1]; });
  var dgH='<thead><tr><th>Diagnóstico</th><th>N</th></tr></thead><tbody>';
  diagArr.forEach(function(e){ dgH+='<tr><td>'+escH(e[0])+'</td><td>'+e[1]+'</td></tr>'; });
  if(!diagArr.length) dgH+='<tr><td colspan="2" style="text-align:center;color:var(--mut)">Sem dados</td></tr>';
  document.getElementById('stat-diag-tbl').innerHTML=dgH+'</tbody>';

  var procMap={};
  recs.forEach(function(r){ if(r.procCir) procMap[r.procCir]=(procMap[r.procCir]||0)+1; });
  var procArr=Object.entries(procMap).sort(function(a,b){ return b[1]-a[1]; });
  var prH='<thead><tr><th>Procedimento</th><th>N</th></tr></thead><tbody>';
  procArr.forEach(function(e){ prH+='<tr><td>'+escH(e[0])+'</td><td>'+e[1]+'</td></tr>'; });
  if(!procArr.length) prH+='<tr><td colspan="2" style="text-align:center;color:var(--mut)">Sem dados</td></tr>';
  document.getElementById('stat-proc-tbl').innerHTML=prH+'</tbody>';
}

function kpiC(v,l,cls){ return '<div class="kpi"><div class="kpi-val '+cls+'">'+v+'</div><div class="kpi-lbl">'+l+'</div></div>'; }

/* ── WHATSAPP ── */
function shareWhatsApp(){
  var today = todayStr();
  var recs = state.registos.filter(function(r){ return r.data===today; });
  var eq = state.equipa;
  var internos = (eq.internos||[]).filter(function(m){ return m.trim(); }).join(', ') || '—';
  var estag = (eq.estagiarios||[]).filter(function(m){ return m.trim(); }).join(', ') || '—';
  var urg = recs.filter(function(r){ return r.tipo==='urgente'; }).length;
  var ele = recs.filter(function(r){ return r.tipo==='eletiva'||r.tipo==='semiurgente'; }).length;
  var comp = recs.filter(function(r){ return r.resultado==='complicacao'; }).length;
  var obt = recs.filter(function(r){ return r.resultado==='obito'; }).length;
  var cats = {'M≥15':0,'F≥15':0,'M<15':0,'F<15':0};
  recs.forEach(function(r){ var k=r.sexo+ageGroup(r.idade); cats[k]=(cats[k]||0)+1; });

  var ln = '\n';
  var txt = '🏥 *HOSPITAL DO PRENDA*'+ln;
  txt += '*Cirurgia Geral — Banco de Urgência*'+ln;
  txt += '*'+fmtDate(today).toUpperCase()+'*'+ln;
  txt += '───────────────'+ln+ln;
  txt += '*EQUIPA DE SERVIÇO*'+ln;
  txt += '• Especialista: '+((eq.especialista&&eq.especialista.trim())||'—')+ln;
  txt += '• Internos: '+internos+ln;
  txt += '• Estagiários: '+estag+ln+ln;
  txt += '*RESUMO DO DIA*'+ln;
  txt += '• Total: '+recs.length+' intervenções'+ln;
  txt += '• Urgentes: '+urg+' | Eletivas/Semi: '+ele+ln;
  txt += '• Complicações: '+comp+' | Óbitos: '+obt+ln+ln;
  txt += '*DEMOGRAFIAS*'+ln;
  txt += '• H≥15: '+cats['M≥15']+' | M≥15: '+cats['F≥15']+ln;
  txt += '• H<15: '+cats['M<15']+' | M<15: '+cats['F<15']+ln+ln;
  if(recs.length){
    txt += '*INTERVENÇÕES*'+ln;
    recs.forEach(function(r,i){
      txt += (i+1)+'. '+r.hora+' — '+(r.diag||'—')+(r.procCir?' ('+r.procCir+')':'')+ln;
      txt += '   '+r.sexo+(r.idade?' '+r.idade+'a':'')+' | '+(r.tipo||'—')+' | '+(r.resultado||'—')+ln;
    });
    txt += ln;
  }
  txt += '───────────────'+ln;
  txt += '_Gerado por Sistema BU · HP_';

  window.open('https://wa.me/?text='+encodeURIComponent(txt), '_blank');
}
window.shareWhatsApp = shareWhatsApp;

/* ── PDF ── */
function exportPDF(){
  var jsPDFLib = (window.jspdf && window.jspdf.jsPDF) || window.jsPDF;
  if(!jsPDFLib){ toast('jsPDF não disponível', false); return; }
  var doc = new jsPDFLib({orientation:'portrait',unit:'mm',format:'a4'});
  var W = doc.internal.pageSize.getWidth();
  var today = todayStr();
  var recs = state.registos.filter(function(r){ return r.data===today; });
  var eq = state.equipa;

  // Dark blue header
  doc.setFillColor(15,43,74);
  doc.rect(0,0,W,28,'F');
  try{ doc.addImage(LOGO_B64,'JPEG',W-20,3,15,15,'','FAST'); }catch(e){}
  doc.setTextColor(255,255,255);
  doc.setFontSize(11); doc.setFont(undefined,'bold');
  doc.text('Hospital do Prenda',12,10);
  doc.setFontSize(7.5); doc.setFont(undefined,'normal');
  doc.text('GEPE — Departamento de Estatística Médica',12,16);
  doc.setFontSize(10); doc.setFont(undefined,'bold');
  doc.text('Cirurgia Geral — Relatório Reunião Matinal',12,23);

  var y = 34;
  doc.setTextColor(0,0,0);

  // Date line
  doc.setFontSize(8.5); doc.setFont(undefined,'normal');
  doc.text('Data: '+fmtDate(today)+'  |  Turno: '+getLabelTurno(eq.turno), 12, y); y+=7;

  // Equipa box
  doc.setFillColor(240,244,255);
  doc.roundedRect(12, y, W-24, 24, 2, 2, 'F');
  doc.setFont(undefined,'bold'); doc.setFontSize(8);
  doc.text('EQUIPA DE SERVIÇO', 15, y+6);
  doc.setFont(undefined,'normal'); doc.setFontSize(8);
  var espStr = (eq.especialista&&eq.especialista.trim()) ? eq.especialista+' ('+eq.espCat+')' : '—';
  doc.text('Especialista: '+espStr, 15, y+12);
  var internos = (eq.internos||[]).filter(function(m){ return m.trim(); });
  doc.text('Internos: '+(internos.length ? internos.join(', ') : '—'), 15, y+18);
  var estag = (eq.estagiarios||[]).filter(function(m){ return m.trim(); });
  doc.text('Estagiários: '+(estag.length ? estag.join(', ') : '—'), W/2, y+18);
  y += 28;

  // KPI summary
  var urg = recs.filter(function(r){ return r.tipo==='urgente'; }).length;
  var ele = recs.filter(function(r){ return r.tipo==='eletiva'||r.tipo==='semiurgente'; }).length;
  var comp = recs.filter(function(r){ return r.resultado==='complicacao'; }).length;
  var obt = recs.filter(function(r){ return r.resultado==='obito'; }).length;
  var men = recs.filter(function(r){ return parseInt(r.idade)<15; }).length;
  var mai = recs.length - men;

  doc.autoTable({
    startY: y,
    head:[['Total','Urgentes','Eletivas','Complicações','Óbitos','≥15 Anos','<15 Anos']],
    body:[[recs.length,urg,ele,comp,obt,mai,men].map(String)],
    theme:'grid',
    headStyles:{fillColor:[15,43,74],textColor:255,fontSize:7.5,fontStyle:'bold',halign:'center'},
    bodyStyles:{fontSize:9.5,fontStyle:'bold',halign:'center'},
    margin:{left:12,right:12}
  });
  y = doc.lastAutoTable.finalY + 5;

  // Demo table
  var cats = {};
  cats['M≥15']=0; cats['F≥15']=0; cats['M<15']=0; cats['F<15']=0;
  recs.forEach(function(r){ var k=r.sexo+ageGroup(r.idade); cats[k]=(cats[k]||0)+1; });
  doc.autoTable({
    startY: y,
    head:[['Grupo Etário','H ≥ 15','F ≥ 15','H < 15','F < 15','Total']],
    body:[['Intervenções',cats['M≥15'],cats['F≥15'],cats['M<15'],cats['F<15'],recs.length]],
    theme:'grid',
    headStyles:{fillColor:[15,43,74],textColor:255,fontSize:7.5},
    bodyStyles:{fontSize:8.5},
    margin:{left:12,right:12}
  });
  y = doc.lastAutoTable.finalY + 5;

  // Interventions table
  if(recs.length){
    doc.setFont(undefined,'bold'); doc.setFontSize(8.5);
    doc.text('INTERVENÇÕES CIRÚRGICAS', 12, y); y+=4;
    var rows = recs.map(function(r){
      return [
        r.hora||'—',
        r.sexo+(r.idade?' '+r.idade+'a':''),
        r.diag||'—',
        r.procCir||'—',
        r.tipo==='urgente'?'Urg':r.tipo==='eletiva'?'Ele':'Semi',
        r.anest||'—',
        r.resultado==='ok'?'OK':r.resultado==='complicacao'?'Comp.':'Óbito',
        r.destino||'—'
      ];
    });
    doc.autoTable({
      startY: y,
      head:[['Hora','Doente','Diagnóstico','Procedimento','Tipo','Anest.','Result.','Destino']],
      body: rows,
      theme:'striped',
      headStyles:{fillColor:[15,43,74],textColor:255,fontSize:7,fontStyle:'bold'},
      bodyStyles:{fontSize:7},
      columnStyles:{2:{cellWidth:35},3:{cellWidth:35}},
      margin:{left:12,right:12}
    });
    y = doc.lastAutoTable.finalY + 5;
  }

  // Diagnostics summary
  var diagMap={};
  recs.forEach(function(r){ if(r.diag) diagMap[r.diag]=(diagMap[r.diag]||0)+1; });
  var diagArr=Object.entries(diagMap).sort(function(a,b){ return b[1]-a[1]; });
  if(diagArr.length){
    doc.setFont(undefined,'bold'); doc.setFontSize(8.5);
    doc.text('DIAGNÓSTICOS', 12, y); y+=4;
    doc.autoTable({
      startY: y,
      head:[['Diagnóstico','Nº Casos']],
      body: diagArr,
      theme:'grid',
      headStyles:{fillColor:[15,43,74],textColor:255,fontSize:7.5},
      bodyStyles:{fontSize:8},
      margin:{left:12,right:12}
    });
  }

  // Footer
  var pgH = doc.internal.pageSize.getHeight();
  doc.setFillColor(15,43,74);
  doc.rect(0,pgH-11,W,11,'F');
  doc.setTextColor(255,255,255);
  doc.setFontSize(7);
  doc.text('Hospital do Prenda · Cirurgia Geral BU · '+new Date().toLocaleString('pt-PT'), 12, pgH-4);
  doc.text('Pág. 1', W-12, pgH-4, {align:'right'});

  doc.save('CirurgiaGeral_BU_'+today+'.pdf');
  toast('PDF gerado com sucesso');
}
window.exportPDF = exportPDF;

function getLabelTurno(t){
  var map = {manha:'Manhã (07h–13h)',tarde:'Tarde (13h–19h)',noite:'Noite (19h–07h)','24h':'24 Horas'};
  return map[t] || (t||'—');
}

init();
})();
"""

# ── ASSEMBLE ────────────────────────────────────────────────────────────────
HTML = """<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cirurgia Geral — BU · Hospital do Prenda</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.8.2/jspdf.plugin.autotable.min.js"></script>
<style>""" + CSS + """</style>
</head>
<body>
""" + BODY.replace('__LOGO__', LOGO) + """
<script>
""" + JS.replace('__LOGO__', LOGO) + """
</script>
</body>
</html>"""

out = '/home/user/Estat-stica/cirurgia_geral.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(HTML)

print('Written %d chars to %s' % (len(HTML), out))
