/**
 * hprenda-grid.js — Excel-like editable data grid component
 * Hospital do Prenda — Consulta Externa
 *
 * Expõe (em window):
 *   window.GridHP.init(containerId, options)
 *   window.GridHP.refresh(containerId)
 *   window.GridHP.setFilter(containerId, searchText)
 *   window.GridHP.setSort(containerId, colKey, direction)
 *   window.GridHP.getStats(containerId)
 *   window.GridHP.flushChanges(containerId)
 *   window.GridHP.destroy(containerId)
 *
 * options: { type: 'consultas'|'proc'|'mat'|'summary', onSave, onDelete }
 */

(function (global) {
  'use strict';

  var LOG = '[hprenda-grid]';

  /* ─────────────────────────────────────────────────────────────
     Registry of active grid instances
  ───────────────────────────────────────────────────────────── */
  var _instances = {};

  /* ─────────────────────────────────────────────────────────────
     CSS injection — only once
  ───────────────────────────────────────────────────────────── */
  function _injectCSS() {
    if (document.getElementById('hp-grid-styles')) return;
    var style = document.createElement('style');
    style.id = 'hp-grid-styles';
    style.textContent = [
      /* Container */
      '.hp-grid-container{position:relative;display:flex;flex-direction:column;font-family:Inter,system-ui,sans-serif;font-size:13px;background:#fff;border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;}',

      /* Dirty banner */
      '.hp-grid-dirty-banner{position:sticky;top:0;z-index:20;display:none;align-items:center;gap:10px;padding:8px 16px;background:#f59e0b;color:#1c1917;font-size:13px;font-weight:500;border-bottom:1px solid #d97706;}',
      '.hp-grid-dirty-banner.visible{display:flex;}',
      '.hp-grid-dirty-banner-btn{padding:4px 12px;border:1px solid #92400e;border-radius:4px;background:#fff;color:#92400e;font-size:12px;font-weight:600;cursor:pointer;transition:background .15s;}',
      '.hp-grid-dirty-banner-btn:hover{background:#fef3c7;}',
      '.hp-grid-dirty-banner-discard{background:transparent;border-color:#78350f;color:#78350f;}',
      '.hp-grid-dirty-banner-discard:hover{background:rgba(0,0,0,.06);}',

      /* Toolbar */
      '.hp-grid-toolbar{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;padding:12px 16px;background:#f8f9fb;border-bottom:1px solid #e2e8f0;}',
      '.hp-grid-toolbar-left{display:flex;align-items:center;gap:8px;flex-wrap:wrap;}',
      '.hp-grid-toolbar-right{display:flex;align-items:center;gap:8px;flex-wrap:wrap;}',
      '.hp-grid-type-sel,.hp-grid-period-filter{padding:5px 10px;border:1px solid #cbd5e1;border-radius:6px;background:#fff;font-size:12px;color:#334155;cursor:pointer;outline:none;transition:border-color .15s;}',
      '.hp-grid-type-sel:focus,.hp-grid-period-filter:focus{border-color:#1a56db;}',
      '.hp-grid-search{padding:5px 10px;border:1px solid #cbd5e1;border-radius:6px;background:#fff;font-size:12px;color:#334155;width:220px;outline:none;transition:border-color .15s;}',
      '.hp-grid-search:focus{border-color:#1a56db;box-shadow:0 0 0 3px rgba(26,86,219,.1);}',
      '.hp-grid-date-from,.hp-grid-date-to{padding:5px 8px;border:1px solid #cbd5e1;border-radius:6px;background:#fff;font-size:12px;color:#334155;outline:none;}',
      '.hp-grid-count{font-size:12px;color:#64748b;white-space:nowrap;}',
      '.hp-grid-btn{padding:5px 12px;border:1px solid #cbd5e1;border-radius:6px;background:#fff;font-size:12px;color:#334155;cursor:pointer;font-weight:500;transition:background .15s,border-color .15s;}',
      '.hp-grid-btn:hover{background:#f1f5f9;border-color:#94a3b8;}',
      '.hp-grid-btn-refresh{color:#1a56db;border-color:#1a56db;}',
      '.hp-grid-btn-refresh:hover{background:#eff6ff;}',
      '.hp-grid-btn-csv{color:#059669;border-color:#059669;}',
      '.hp-grid-btn-csv:hover{background:#ecfdf5;}',
      '.hp-grid-btn-excel{color:#7c3aed;border-color:#7c3aed;}',
      '.hp-grid-btn-excel:hover{background:#f5f3ff;}',

      /* Table wrapper */
      '.hp-grid-table-wrap{overflow:auto;flex:1;-webkit-overflow-scrolling:touch;}',
      '.hp-grid-table{border-collapse:collapse;width:100%;min-width:800px;table-layout:auto;}',

      /* Header */
      '.hp-grid-th{position:sticky;top:0;z-index:10;background:#1a56db;color:#fff;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;padding:10px 12px;text-align:left;white-space:nowrap;cursor:default;user-select:none;border-right:1px solid rgba(255,255,255,.12);}',
      '.hp-grid-th:last-child{border-right:none;}',
      '.hp-grid-th.sortable{cursor:pointer;}',
      '.hp-grid-th.sortable:hover{background:#1e40af;}',
      '.hp-grid-th .sort-arrow{display:inline-block;margin-left:4px;opacity:.5;font-size:9px;}',
      '.hp-grid-th.sort-asc .sort-arrow,.hp-grid-th.sort-desc .sort-arrow{opacity:1;}',

      /* Cells */
      '.hp-grid-td{padding:8px 12px;border-bottom:1px solid #f1f5f9;color:#1e293b;vertical-align:middle;white-space:nowrap;}',
      '.hp-grid-td.hp-grid-editable:hover{background:#f0f7ff;cursor:cell;}',
      '.hp-grid-td.hp-grid-dirty{background:#fff7ed;border-left:3px solid #f59e0b;}',
      '.hp-grid-td.hp-grid-dirty:not(.hp-grid-editable){border-left:none;}',
      '.hp-grid-td.hp-grid-num{text-align:right;}',
      '.hp-grid-td.hp-grid-pct{text-align:right;color:#64748b;}',

      /* Editing input */
      '.hp-grid-input{border:1px solid #1a56db;border-radius:4px;width:70px;text-align:right;padding:3px 6px;font-size:13px;font-family:inherit;outline:none;background:#fff;color:#1e293b;}',
      '.hp-grid-input:focus{box-shadow:0 0 0 3px rgba(26,86,219,.18);}',
      '.hp-grid-input.hp-grid-input-warn{border-color:#f59e0b;box-shadow:0 0 0 2px rgba(245,158,11,.2);}',

      /* Row hover */
      '.hp-grid-table tbody tr:hover .hp-grid-td{background:#f8fafc;}',
      '.hp-grid-table tbody tr:hover .hp-grid-td.hp-grid-dirty{background:#fef3c7;}',
      '.hp-grid-table tbody tr:hover .hp-grid-td.hp-grid-editable{background:#e8f1ff;}',

      /* Total row */
      '.hp-grid-total .hp-grid-td{background:#0f172a !important;color:#f8fafc !important;font-weight:700;border-bottom:none;}',
      '.hp-grid-total .hp-grid-td.hp-grid-pct{color:#94a3b8 !important;}',

      /* Delete button */
      '.hp-grid-del-btn{display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;border:1px solid #fca5a5;border-radius:4px;background:#fff;color:#ef4444;font-size:14px;font-weight:700;cursor:pointer;line-height:1;padding:0;transition:background .15s,color .15s;}',
      '.hp-grid-del-btn:hover{background:#ef4444;color:#fff;border-color:#ef4444;}',

      /* Footer */
      '.hp-grid-footer{display:flex;align-items:center;flex-wrap:wrap;gap:12px;padding:8px 16px;background:#f8f9fb;border-top:1px solid #e2e8f0;font-size:12px;color:#64748b;}',
      '.hp-grid-footer-dirty{color:#d97706;font-weight:600;}',
      '.hp-grid-footer-time{margin-left:auto;}',

      /* Empty state */
      '.hp-grid-empty{padding:40px;text-align:center;color:#94a3b8;font-size:14px;}',

      /* Toast (standalone — used when global toast not available) */
      '.hp-grid-toast-wrap{position:fixed;bottom:20px;right:20px;z-index:99999;display:flex;flex-direction:column;gap:8px;pointer-events:none;}',
      '.hp-grid-toast{padding:10px 16px;border-radius:8px;font-size:13px;font-weight:500;pointer-events:all;box-shadow:0 4px 12px rgba(0,0,0,.15);animation:hp-grid-toast-in .2s ease;}',
      '.hp-grid-toast-ok{background:#059669;color:#fff;}',
      '.hp-grid-toast-err{background:#dc2626;color:#fff;}',
      '.hp-grid-toast-warn{background:#d97706;color:#fff;}',
      '.hp-grid-toast-info{background:#1a56db;color:#fff;}',
      '@keyframes hp-grid-toast-in{from{opacity:0;transform:translateY(10px);}to{opacity:1;transform:translateY(0);}}'
    ].join('');
    document.head.appendChild(style);
    console.log(LOG, 'CSS injectado.');
  }

  /* ─────────────────────────────────────────────────────────────
     Toast helper
  ───────────────────────────────────────────────────────────── */
  function _toast(msg, type) {
    if (typeof global.toast === 'function') {
      global.toast(msg, type || 'info');
      return;
    }
    /* fallback toast */
    var types = { ok: 'hp-grid-toast-ok', err: 'hp-grid-toast-err', warn: 'hp-grid-toast-warn', info: 'hp-grid-toast-info' };
    var wrap = document.getElementById('hp-grid-toast-wrap');
    if (!wrap) {
      wrap = document.createElement('div');
      wrap.id = 'hp-grid-toast-wrap';
      wrap.className = 'hp-grid-toast-wrap';
      document.body.appendChild(wrap);
    }
    var el = document.createElement('div');
    el.className = 'hp-grid-toast ' + (types[type] || types.info);
    el.textContent = msg;
    wrap.appendChild(el);
    setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 3000);
  }

  /* ─────────────────────────────────────────────────────────────
     localStorage helpers
  ───────────────────────────────────────────────────────────── */
  function _safeGet(k) {
    try { return localStorage.getItem(k); } catch (e) { console.warn(LOG, 'localStorage read error', k, e); return null; }
  }
  function _safeSet(k, v) {
    try { localStorage.setItem(k, v); return true; } catch (e) { console.warn(LOG, 'localStorage write error', k, e); return false; }
  }
  function _safeParse(raw, def) {
    if (!raw) return def;
    try { return JSON.parse(raw); } catch (e) { return def; }
  }
  function _storageKey(type, date) { return 'prenda_' + type + '_' + date; }

  /* ─────────────────────────────────────────────────────────────
     Static reference lists (mirror from crud/export)
  ───────────────────────────────────────────────────────────── */
  function _ESPECIALIDADES() {
    return global.ESPECIALIDADES || [
      'Medicina Interna', 'Ortopedia', 'Cirurgia Geral', 'Proctologia',
      'Cardiologia', 'Reumatologia', 'Estomatologia', 'Oftalmologia',
      'Optometria', 'Anestesiologia', 'Maxilo Facial', 'Neurocirurgia',
      'Gastroenterologia', 'Neurologia', 'Otorrinolaringologia'
    ];
  }
  function _PROCEDIMENTOS() {
    return global.PROCEDIMENTOS || [
      'Curativos feitos', 'Pontos retirados', 'Gessos retirados',
      'Gessos aplicados', 'Algálias retiradas', 'Talas colocadas',
      'Talas retiradas', 'Injeções', 'Infiltrações',
      'Exodontia simples', 'Exodontia complicada'
    ];
  }
  function _MATERIAIS() {
    return global.MATERIAIS || [
      { nome: 'Fitas de glicemia', unit: 'unidade' },
      { nome: 'Rolo de gesso', unit: 'unidade' },
      { nome: 'Ligadura', unit: 'unidade' },
      { nome: 'Seringas', unit: 'unidade' },
      { nome: 'Ampolas injectáveis', unit: 'unidade' },
      { nome: 'Compressas', unit: 'unidade' },
      { nome: 'Bisturi', unit: 'unidade' },
      { nome: 'Sacos de colectores', unit: 'unidade' },
      { nome: 'Luvas descartáveis', unit: 'par' },
      { nome: 'Algodão', unit: 'grama' },
      { nome: 'Soro fisiológico', unit: 'frasco' },
      { nome: 'Algália', unit: 'unidade' }
    ];
  }

  /* ─────────────────────────────────────────────────────────────
     Date helpers
  ───────────────────────────────────────────────────────────── */
  function _formatDate(d) {
    if (!d) return '—';
    var p = d.split('-');
    return p.length === 3 ? p[2] + '/' + p[1] + '/' + p[0] : d;
  }
  function _todayKey() { return new Date().toISOString().slice(0, 10); }
  function _timeNow() {
    var n = new Date();
    return ('0' + n.getHours()).slice(-2) + ':' + ('0' + n.getMinutes()).slice(-2) + ':' + ('0' + n.getSeconds()).slice(-2);
  }

  /* ─────────────────────────────────────────────────────────────
     Period filter helper — returns array of date strings
  ───────────────────────────────────────────────────────────── */
  function _getSavedDates() {
    var raw = _safeGet('prenda_saved_dates');
    if (raw) return _safeParse(raw, []);
    /* Fallback: scan localStorage */
    var dates = [];
    try {
      for (var i = 0; i < localStorage.length; i++) {
        var k = localStorage.key(i);
        if (k && k.match(/^prenda_consultas_(\d{4}-\d{2}-\d{2})$/)) {
          dates.push(k.replace('prenda_consultas_', ''));
        }
      }
    } catch (e) { /* ignore */ }
    return dates.sort();
  }

  function _filterDatesByPeriod(dates, period, from, to) {
    if (period === 'all') return dates;
    var today = new Date(_todayKey());
    return dates.filter(function (d) {
      var dt = new Date(d);
      if (isNaN(dt.getTime())) return false;
      if (period === 'month') {
        return dt.getFullYear() === today.getFullYear() && dt.getMonth() === today.getMonth();
      }
      if (period === 'quarter') {
        var q = Math.floor(today.getMonth() / 3);
        var dq = Math.floor(dt.getMonth() / 3);
        return dt.getFullYear() === today.getFullYear() && dq === q;
      }
      if (period === 'year') {
        return dt.getFullYear() === today.getFullYear();
      }
      if (period === 'range') {
        var fromDt = from ? new Date(from) : null;
        var toDt = to ? new Date(to) : null;
        if (fromDt && dt < fromDt) return false;
        if (toDt && dt > toDt) return false;
        return true;
      }
      return true;
    });
  }

  /* ─────────────────────────────────────────────────────────────
     Data loading — with fallback to direct localStorage
  ───────────────────────────────────────────────────────────── */
  function _loadRows(type, dates) {
    if (type === 'summary') return _loadSummaryRows(dates);
    if (type === 'consultas') return _loadConsultasRows(dates);
    if (type === 'proc') return _loadProcRows(dates);
    if (type === 'mat') return _loadMatRows(dates);
    return [];
  }

  function _loadSummaryRows(dates) {
    return dates.map(function (date) {
      var cRaw = _safeGet(_storageKey('consultas', date));
      var pRaw = _safeGet(_storageKey('proc', date));
      var mRaw = _safeGet(_storageKey('mat', date));
      var cData = _safeParse(cRaw, {});
      var pData = _safeParse(pRaw, {});
      var mData = _safeParse(mRaw, {});

      var ag = 0, re = 0, ca = 0, m15 = 0, M15 = 0, proc = 0, stock = 0, usado = 0;
      _ESPECIALIDADES().forEach(function (e) {
        var d = cData[e] || {};
        ag += (d.ag || 0); re += (d.re || 0); ca += (d.ca || 0);
        m15 += (d.m15 || 0); M15 += (d.M15 || 0);
      });
      _PROCEDIMENTOS().forEach(function (p) {
        var d = pData[p] || {};
        proc += (d.manha || 0) + (d.tarde || 0);
      });
      _MATERIAIS().forEach(function (m) {
        var d = mData[m.nome] || {};
        stock += (d.stock || 0); usado += (d.usado || 0);
      });

      return {
        _date: date,
        _id: date,
        _label: _formatDate(date),
        data: ag, re: re, ca: ca, m15: m15, M15: M15,
        pctRe: ag > 0 ? (re / ag * 100).toFixed(1) : '—',
        pctCa: ag > 0 ? (ca / ag * 100).toFixed(1) : '—',
        proc: proc, stock: stock, usado: usado
      };
    });
  }

  function _loadConsultasRows(dates) {
    var rows = [];
    dates.forEach(function (date) {
      var raw = _safeGet(_storageKey('consultas', date));
      var cData = _safeParse(raw, {});
      _ESPECIALIDADES().forEach(function (esp) {
        var d = cData[esp] || { ag: 0, re: 0, ca: 0, m15: 0, M15: 0 };
        rows.push({
          _date: date,
          _id: date + '|' + esp,
          _label: esp,
          _dateLabel: _formatDate(date),
          esp: esp,
          ag: d.ag || 0, re: d.re || 0, ca: d.ca || 0,
          m15: d.m15 || 0, M15: d.M15 || 0,
          pctRe: (d.ag || 0) > 0 ? ((d.re || 0) / (d.ag || 1) * 100).toFixed(1) : '—',
          pctCa: (d.ag || 0) > 0 ? ((d.ca || 0) / (d.ag || 1) * 100).toFixed(1) : '—'
        });
      });
    });
    return rows;
  }

  function _loadProcRows(dates) {
    var rows = [];
    dates.forEach(function (date) {
      var raw = _safeGet(_storageKey('proc', date));
      var pData = _safeParse(raw, {});
      var totalDay = 0;
      _PROCEDIMENTOS().forEach(function (p) {
        var d = pData[p] || { manha: 0, tarde: 0 };
        totalDay += (d.manha || 0) + (d.tarde || 0);
      });
      _PROCEDIMENTOS().forEach(function (p) {
        var d = pData[p] || { manha: 0, tarde: 0 };
        var tot = (d.manha || 0) + (d.tarde || 0);
        rows.push({
          _date: date,
          _id: date + '|' + p,
          _label: p,
          _dateLabel: _formatDate(date),
          proc: p,
          manha: d.manha || 0,
          tarde: d.tarde || 0,
          total: tot,
          pctDia: totalDay > 0 ? (tot / totalDay * 100).toFixed(1) : '—',
          _totalDay: totalDay
        });
      });
    });
    return rows;
  }

  function _loadMatRows(dates) {
    var rows = [];
    var matsMap = {};
    _MATERIAIS().forEach(function (m) { matsMap[m.nome] = m.unit; });
    dates.forEach(function (date) {
      var raw = _safeGet(_storageKey('mat', date));
      var mData = _safeParse(raw, {});
      _MATERIAIS().forEach(function (m) {
        var d = mData[m.nome] || { stock: 0, usado: 0 };
        var saldo = Math.max(0, (d.stock || 0) - (d.usado || 0));
        rows.push({
          _date: date,
          _id: date + '|' + m.nome,
          _label: m.nome,
          _dateLabel: _formatDate(date),
          mat: m.nome,
          unit: m.unit,
          stock: d.stock || 0,
          usado: d.usado || 0,
          saldo: saldo,
          pctConsumo: (d.stock || 0) > 0 ? ((d.usado || 0) / (d.stock || 1) * 100).toFixed(1) : '—'
        });
      });
    });
    return rows;
  }

  /* ─────────────────────────────────────────────────────────────
     Column definitions
  ───────────────────────────────────────────────────────────── */
  var COLS = {
    summary: [
      { key: 'data',  label: 'Data',           sortKey: '_date',   editable: false, cls: '' },
      { key: 'ag',    label: 'Agendadas',       sortKey: 'data',    editable: false, cls: 'hp-grid-num' },
      { key: 're',    label: 'Realizadas',      sortKey: 're',      editable: false, cls: 'hp-grid-num' },
      { key: 'ca',    label: 'Canceladas',      sortKey: 'ca',      editable: false, cls: 'hp-grid-num' },
      { key: 'm15',   label: '<15 Anos',        sortKey: 'm15',     editable: false, cls: 'hp-grid-num' },
      { key: 'M15',   label: '>15 Anos',        sortKey: 'M15',     editable: false, cls: 'hp-grid-num' },
      { key: 'pctRe', label: '% Realiz.',       sortKey: 'pctRe',   editable: false, cls: 'hp-grid-pct', computed: true },
      { key: 'pctCa', label: '% Canc.',         sortKey: 'pctCa',   editable: false, cls: 'hp-grid-pct', computed: true },
      { key: 'proc',  label: 'Procedimentos',   sortKey: 'proc',    editable: false, cls: 'hp-grid-num' },
      { key: 'stock', label: 'Stock Inicial',   sortKey: 'stock',   editable: false, cls: 'hp-grid-num' },
      { key: 'usado', label: 'Consumido',       sortKey: 'usado',   editable: false, cls: 'hp-grid-num' },
      { key: '_actions', label: 'Acções',       sortKey: null,      editable: false, cls: '' }
    ],
    consultas: [
      { key: 'data',  label: 'Data',           sortKey: '_date',   editable: false, cls: '' },
      { key: 'esp',   label: 'Especialidade',  sortKey: 'esp',     editable: false, cls: '' },
      { key: 'ag',    label: 'Agendadas',      sortKey: 'ag',      editable: true,  cls: 'hp-grid-num', field: 'ag' },
      { key: 're',    label: 'Realizadas',     sortKey: 're',      editable: true,  cls: 'hp-grid-num', field: 're' },
      { key: 'ca',    label: 'Canceladas',     sortKey: 'ca',      editable: true,  cls: 'hp-grid-num', field: 'ca' },
      { key: 'm15',   label: '<15 Anos',       sortKey: 'm15',     editable: true,  cls: 'hp-grid-num', field: 'm15' },
      { key: 'M15',   label: '>15 Anos',       sortKey: 'M15',     editable: true,  cls: 'hp-grid-num', field: 'M15' },
      { key: 'pctRe', label: '% Realiz.',      sortKey: 'pctRe',   editable: false, cls: 'hp-grid-pct', computed: true },
      { key: 'pctCa', label: '% Canc.',        sortKey: 'pctCa',   editable: false, cls: 'hp-grid-pct', computed: true },
      { key: '_actions', label: 'Acções',      sortKey: null,      editable: false, cls: '' }
    ],
    proc: [
      { key: 'data',   label: 'Data',         sortKey: '_date',    editable: false, cls: '' },
      { key: 'proc',   label: 'Procedimento', sortKey: 'proc',     editable: false, cls: '' },
      { key: 'manha',  label: 'Manhã',        sortKey: 'manha',    editable: true,  cls: 'hp-grid-num', field: 'manha' },
      { key: 'tarde',  label: 'Tarde',        sortKey: 'tarde',    editable: true,  cls: 'hp-grid-num', field: 'tarde' },
      { key: 'total',  label: 'Total',        sortKey: 'total',    editable: false, cls: 'hp-grid-num', computed: true },
      { key: 'pctDia', label: '% do Dia',     sortKey: 'pctDia',   editable: false, cls: 'hp-grid-pct', computed: true },
      { key: '_actions', label: 'Acções',     sortKey: null,       editable: false, cls: '' }
    ],
    mat: [
      { key: 'data',       label: 'Data',         sortKey: '_date',    editable: false, cls: '' },
      { key: 'mat',        label: 'Material',     sortKey: 'mat',      editable: false, cls: '' },
      { key: 'unit',       label: 'Unidade',      sortKey: 'unit',     editable: false, cls: '' },
      { key: 'stock',      label: 'Stock Inicial',sortKey: 'stock',    editable: true,  cls: 'hp-grid-num', field: 'stock' },
      { key: 'usado',      label: 'Consumido',    sortKey: 'usado',    editable: true,  cls: 'hp-grid-num', field: 'usado' },
      { key: 'saldo',      label: 'Saldo',        sortKey: 'saldo',    editable: false, cls: 'hp-grid-num', computed: true },
      { key: 'pctConsumo', label: '% Consumo',    sortKey: 'pctConsumo', editable: false, cls: 'hp-grid-pct', computed: true },
      { key: '_actions',   label: 'Acções',       sortKey: null,       editable: false, cls: '' }
    ]
  };

  /* ─────────────────────────────────────────────────────────────
     Compute derived fields after editing
  ───────────────────────────────────────────────────────────── */
  function _recompute(row, type) {
    if (type === 'consultas') {
      var ag = row.ag || 0;
      row.pctRe = ag > 0 ? ((row.re || 0) / ag * 100).toFixed(1) : '—';
      row.pctCa = ag > 0 ? ((row.ca || 0) / ag * 100).toFixed(1) : '—';
    } else if (type === 'proc') {
      row.total = (row.manha || 0) + (row.tarde || 0);
      row.pctDia = row._totalDay > 0 ? (row.total / row._totalDay * 100).toFixed(1) : '—';
    } else if (type === 'mat') {
      row.saldo = Math.max(0, (row.stock || 0) - (row.usado || 0));
      row.pctConsumo = (row.stock || 0) > 0 ? ((row.usado || 0) / (row.stock || 1) * 100).toFixed(1) : '—';
    }
  }

  /* ─────────────────────────────────────────────────────────────
     Sorting
  ───────────────────────────────────────────────────────────── */
  function _sortRows(rows, colKey, direction) {
    if (!direction || !colKey) return rows.slice();
    return rows.slice().sort(function (a, b) {
      var va = a[colKey], vb = b[colKey];
      /* Numeric comparison if possible */
      var na = parseFloat(va), nb = parseFloat(vb);
      if (!isNaN(na) && !isNaN(nb)) {
        return direction === 'asc' ? na - nb : nb - na;
      }
      /* String comparison */
      va = String(va || '').toLowerCase();
      vb = String(vb || '').toLowerCase();
      if (va < vb) return direction === 'asc' ? -1 : 1;
      if (va > vb) return direction === 'asc' ? 1 : -1;
      return 0;
    });
  }

  /* ─────────────────────────────────────────────────────────────
     Filtering
  ───────────────────────────────────────────────────────────── */
  function _filterRows(rows, search) {
    if (!search) return rows;
    var q = search.toLowerCase().trim();
    return rows.filter(function (row) {
      return Object.keys(row).some(function (k) {
        if (k.charAt(0) === '_') return false;
        return String(row[k]).toLowerCase().indexOf(q) !== -1;
      });
    });
  }

  /* ─────────────────────────────────────────────────────────────
     Total row computation
  ───────────────────────────────────────────────────────────── */
  function _computeTotals(rows, type) {
    if (!rows.length) return null;
    if (type === 'summary') {
      var t = { ag: 0, re: 0, ca: 0, m15: 0, M15: 0, proc: 0, stock: 0, usado: 0 };
      rows.forEach(function (r) {
        t.ag += (r.data || 0); t.re += (r.re || 0); t.ca += (r.ca || 0);
        t.m15 += (r.m15 || 0); t.M15 += (r.M15 || 0);
        t.proc += (r.proc || 0); t.stock += (r.stock || 0); t.usado += (r.usado || 0);
      });
      t.pctRe = t.ag > 0 ? (t.re / t.ag * 100).toFixed(1) : '—';
      t.pctCa = t.ag > 0 ? (t.ca / t.ag * 100).toFixed(1) : '—';
      return t;
    }
    if (type === 'consultas') {
      var t = { ag: 0, re: 0, ca: 0, m15: 0, M15: 0 };
      rows.forEach(function (r) { t.ag += r.ag; t.re += r.re; t.ca += r.ca; t.m15 += r.m15; t.M15 += r.M15; });
      t.pctRe = t.ag > 0 ? (t.re / t.ag * 100).toFixed(1) : '—';
      t.pctCa = t.ag > 0 ? (t.ca / t.ag * 100).toFixed(1) : '—';
      return t;
    }
    if (type === 'proc') {
      var t = { manha: 0, tarde: 0, total: 0 };
      rows.forEach(function (r) { t.manha += r.manha; t.tarde += r.tarde; t.total += r.total; });
      t.pctDia = '100';
      return t;
    }
    if (type === 'mat') {
      var t = { stock: 0, usado: 0 };
      rows.forEach(function (r) { t.stock += r.stock; t.usado += r.usado; });
      t.saldo = Math.max(0, t.stock - t.usado);
      t.pctConsumo = t.stock > 0 ? (t.usado / t.stock * 100).toFixed(1) : '—';
      return t;
    }
    return null;
  }

  /* ─────────────────────────────────────────────────────────────
     Render cell value
  ───────────────────────────────────────────────────────────── */
  function _cellValue(row, col, type, isTotalRow) {
    if (col.key === 'data') return isTotalRow ? 'TOTAL' : (row._dateLabel || row._label || '—');
    if (col.key === 'esp') return row.esp || '—';
    if (col.key === 'proc') return row.proc || '—';
    if (col.key === 'mat') return row.mat || '—';
    if (col.key === 'unit') return row.unit || '—';
    if (col.key === '_actions') return '';
    var v = row[col.key];
    if (v === undefined || v === null) return '—';
    return v;
  }

  /* ─────────────────────────────────────────────────────────────
     Build table rows using DocumentFragment
  ───────────────────────────────────────────────────────────── */
  function _buildRows(inst, displayRows, totalRow) {
    var frag = document.createDocumentFragment();
    var cols = COLS[inst.type];
    var type = inst.type;

    displayRows.forEach(function (row) {
      var tr = document.createElement('tr');
      tr.dataset.rowId = row._id;

      cols.forEach(function (col) {
        var td = document.createElement('td');
        td.className = 'hp-grid-td' + (col.cls ? ' ' + col.cls : '');
        td.dataset.col = col.key;
        td.dataset.rowId = row._id;

        if (col.key === '_actions') {
          var btn = document.createElement('button');
          btn.className = 'hp-grid-del-btn';
          btn.title = 'Apagar linha';
          btn.textContent = '×';
          btn.dataset.rowId = row._id;
          btn.dataset.label = row._label || row.esp || row.proc || row.mat || '';
          btn.dataset.date = row._date || '';
          td.appendChild(btn);
        } else if (col.editable) {
          td.classList.add('hp-grid-editable');
          if (inst._dirty[row._id] && inst._dirty[row._id][col.field]) {
            td.classList.add('hp-grid-dirty');
          }
          var span = document.createElement('span');
          span.textContent = _cellValue(row, col, type, false);
          td.appendChild(span);
        } else {
          var v = _cellValue(row, col, type, false);
          if (col.key === 'pctRe' || col.key === 'pctCa' || col.key === 'pctDia' || col.key === 'pctConsumo') {
            td.textContent = v !== '—' ? v + '%' : '—';
          } else {
            td.textContent = v;
          }
        }
        tr.appendChild(td);
      });

      frag.appendChild(tr);
    });

    /* Total row */
    if (totalRow) {
      var tr = document.createElement('tr');
      tr.className = 'hp-grid-total';
      cols.forEach(function (col) {
        var td = document.createElement('td');
        td.className = 'hp-grid-td' + (col.cls ? ' ' + col.cls : '');
        if (col.key === '_actions') {
          td.textContent = '';
        } else if (col.key === 'data') {
          td.textContent = 'TOTAL GERAL';
        } else if (col.key === 'esp' || col.key === 'proc' || col.key === 'mat' || col.key === 'unit') {
          td.textContent = '';
        } else if (col.key === 'pctRe' || col.key === 'pctCa' || col.key === 'pctDia' || col.key === 'pctConsumo') {
          var v = totalRow[col.key];
          td.textContent = v !== undefined && v !== '—' ? v + '%' : '—';
          td.classList.add('hp-grid-pct');
        } else {
          var v = totalRow[col.key];
          td.textContent = v !== undefined ? v : '—';
        }
        tr.appendChild(td);
      });
      frag.appendChild(tr);
    }

    return frag;
  }

  /* ─────────────────────────────────────────────────────────────
     Re-render tbody only (fast path used after sort/filter)
  ───────────────────────────────────────────────────────────── */
  function _renderBody(inst) {
    var tbody = inst._el.querySelector('tbody');
    if (!tbody) return;
    while (tbody.firstChild) tbody.removeChild(tbody.firstChild);

    var rows = inst._filtered;
    var totals = _computeTotals(rows, inst.type);
    tbody.appendChild(_buildRows(inst, rows, totals));

    /* Update footer counts */
    _updateFooter(inst);
    _updateDirtyBanner(inst);
  }

  /* ─────────────────────────────────────────────────────────────
     Full render
  ───────────────────────────────────────────────────────────── */
  function _render(inst) {
    var container = inst._el;

    /* Clear container except toolbar (already inserted) */
    var toolbar = container.querySelector('.hp-grid-toolbar');
    var banner  = container.querySelector('.hp-grid-dirty-banner');
    /* Remove everything except toolbar and banner */
    Array.from(container.children).forEach(function (c) {
      if (c !== toolbar && c !== banner) container.removeChild(c);
    });

    /* Table wrapper */
    var wrap = document.createElement('div');
    wrap.className = 'hp-grid-table-wrap';

    var table = document.createElement('table');
    table.className = 'hp-grid-table';

    /* Thead */
    var thead = document.createElement('thead');
    var tr = document.createElement('tr');
    COLS[inst.type].forEach(function (col) {
      var th = document.createElement('th');
      th.className = 'hp-grid-th';
      th.dataset.col = col.key;
      if (col.sortKey) {
        th.classList.add('sortable');
        var arrow = document.createElement('span');
        arrow.className = 'sort-arrow';
        arrow.textContent = '↕';
        if (inst._sortCol === col.sortKey) {
          th.classList.add(inst._sortDir === 'asc' ? 'sort-asc' : 'sort-desc');
          arrow.textContent = inst._sortDir === 'asc' ? '▲' : '▼';
        }
        th.textContent = col.label;
        th.appendChild(arrow);
      } else {
        th.textContent = col.label;
      }
      tr.appendChild(th);
    });
    thead.appendChild(tr);
    table.appendChild(thead);

    /* Tbody */
    var tbody = document.createElement('tbody');
    if (inst._filtered.length === 0) {
      var emptyTr = document.createElement('tr');
      var emptyTd = document.createElement('td');
      emptyTd.colSpan = COLS[inst.type].length;
      emptyTd.className = 'hp-grid-empty';
      emptyTd.textContent = 'Sem dados para exibir.';
      emptyTr.appendChild(emptyTd);
      tbody.appendChild(emptyTr);
    } else {
      var totals = _computeTotals(inst._filtered, inst.type);
      tbody.appendChild(_buildRows(inst, inst._filtered, totals));
    }
    table.appendChild(tbody);
    wrap.appendChild(table);
    container.appendChild(wrap);

    /* Footer */
    var footer = document.createElement('div');
    footer.className = 'hp-grid-footer';
    footer.innerHTML =
      '<span class="hp-grid-footer-rows">Linhas: ' + inst._rows.length + ' total | ' + inst._filtered.length + ' filtradas</span>' +
      '<span class="hp-grid-footer-dirty hp-grid-dirty-indicator" style="display:none"></span>' +
      '<span class="hp-grid-footer-time">| Última actualização: ' + _timeNow() + '</span>';
    container.appendChild(footer);

    _updateDirtyBanner(inst);
    console.log(LOG, 'Grid renderizada: ' + inst.type + ', ' + inst._filtered.length + ' linhas (' + inst._rows.length + ' total)');
  }

  /* ─────────────────────────────────────────────────────────────
     Update footer row counts
  ───────────────────────────────────────────────────────────── */
  function _updateFooter(inst) {
    var footerRows = inst._el.querySelector('.hp-grid-footer-rows');
    var footerTime = inst._el.querySelector('.hp-grid-footer-time');
    if (footerRows) footerRows.textContent = 'Linhas: ' + inst._rows.length + ' total | ' + inst._filtered.length + ' filtradas';
    if (footerTime) footerTime.textContent = '| Última actualização: ' + _timeNow();
    _updateDirtyBanner(inst);
  }

  /* ─────────────────────────────────────────────────────────────
     Dirty banner
  ───────────────────────────────────────────────────────────── */
  function _updateDirtyBanner(inst) {
    var banner = inst._el.querySelector('.hp-grid-dirty-banner');
    var footerDirty = inst._el.querySelector('.hp-grid-dirty-indicator');
    var n = _countDirty(inst);
    if (n > 0) {
      if (banner) {
        banner.classList.add('visible');
        var msg = banner.querySelector('.hp-grid-dirty-msg');
        if (msg) msg.textContent = n + ' alteração(ões) por guardar';
      }
      if (footerDirty) {
        footerDirty.style.display = '';
        footerDirty.textContent = '| ' + n + ' alterações por guardar';
      }
    } else {
      if (banner) banner.classList.remove('visible');
      if (footerDirty) footerDirty.style.display = 'none';
    }
  }

  function _countDirty(inst) {
    return Object.keys(inst._dirty).reduce(function (acc, k) {
      return acc + Object.keys(inst._dirty[k]).length;
    }, 0);
  }

  /* ─────────────────────────────────────────────────────────────
     Build toolbar
  ───────────────────────────────────────────────────────────── */
  function _buildToolbar(inst) {
    var tb = document.createElement('div');
    tb.className = 'hp-grid-toolbar';

    /* Left */
    var left = document.createElement('div');
    left.className = 'hp-grid-toolbar-left';

    var typeSel = document.createElement('select');
    typeSel.className = 'hp-grid-type-sel';
    [
      { v: 'consultas', l: 'Consultas' },
      { v: 'proc',      l: 'Procedimentos' },
      { v: 'mat',       l: 'Materiais' },
      { v: 'summary',   l: 'Resumo' }
    ].forEach(function (o) {
      var opt = document.createElement('option');
      opt.value = o.v;
      opt.textContent = o.l;
      if (o.v === inst.type) opt.selected = true;
      typeSel.appendChild(opt);
    });
    left.appendChild(typeSel);

    var search = document.createElement('input');
    search.type = 'text';
    search.className = 'hp-grid-search';
    search.placeholder = 'Filtrar...';
    search.value = inst._search || '';
    left.appendChild(search);

    var periodSel = document.createElement('select');
    periodSel.className = 'hp-grid-period-filter';
    [
      { v: 'all',     l: 'Todos' },
      { v: 'month',   l: 'Este mês' },
      { v: 'quarter', l: 'Este trimestre' },
      { v: 'year',    l: 'Este ano' },
      { v: 'range',   l: 'Intervalo' }
    ].forEach(function (o) {
      var opt = document.createElement('option');
      opt.value = o.v;
      opt.textContent = o.l;
      if (o.v === inst._period) opt.selected = true;
      periodSel.appendChild(opt);
    });
    left.appendChild(periodSel);

    var dateFrom = document.createElement('input');
    dateFrom.type = 'date';
    dateFrom.className = 'hp-grid-date-from';
    dateFrom.style.display = inst._period === 'range' ? '' : 'none';
    dateFrom.value = inst._dateFrom || '';
    left.appendChild(dateFrom);

    var dateTo = document.createElement('input');
    dateTo.type = 'date';
    dateTo.className = 'hp-grid-date-to';
    dateTo.style.display = inst._period === 'range' ? '' : 'none';
    dateTo.value = inst._dateTo || '';
    left.appendChild(dateTo);

    /* Right */
    var right = document.createElement('div');
    right.className = 'hp-grid-toolbar-right';

    var count = document.createElement('span');
    count.className = 'hp-grid-count';
    count.textContent = '0 registos';
    right.appendChild(count);

    var btnCSV = document.createElement('button');
    btnCSV.className = 'hp-grid-btn hp-grid-btn-csv';
    btnCSV.textContent = 'CSV';
    right.appendChild(btnCSV);

    var btnExcel = document.createElement('button');
    btnExcel.className = 'hp-grid-btn hp-grid-btn-excel';
    btnExcel.textContent = 'Excel';
    right.appendChild(btnExcel);

    var btnRefresh = document.createElement('button');
    btnRefresh.className = 'hp-grid-btn hp-grid-btn-refresh';
    btnRefresh.textContent = '↺ Actualizar';
    right.appendChild(btnRefresh);

    tb.appendChild(left);
    tb.appendChild(right);
    return tb;
  }

  /* ─────────────────────────────────────────────────────────────
     Build dirty banner
  ───────────────────────────────────────────────────────────── */
  function _buildDirtyBanner(inst) {
    var banner = document.createElement('div');
    banner.className = 'hp-grid-dirty-banner';
    banner.innerHTML =
      '<span>⚠ <span class="hp-grid-dirty-msg">0 alteração(ões) por guardar</span></span>' +
      '<button class="hp-grid-dirty-banner-btn hp-grid-dirty-save">Guardar agora</button>' +
      '<button class="hp-grid-dirty-banner-btn hp-grid-dirty-banner-discard">Descartar</button>';
    return banner;
  }

  /* ─────────────────────────────────────────────────────────────
     Inline editing — activate
  ───────────────────────────────────────────────────────────── */
  function _activateEdit(inst, td, row, col) {
    if (td.querySelector('.hp-grid-input')) return; /* already editing */
    var span = td.querySelector('span');
    var origValue = span ? span.textContent : '0';
    span.style.display = 'none';

    var input = document.createElement('input');
    input.type = 'number';
    input.min = '0';
    input.className = 'hp-grid-input';
    input.value = origValue === '—' ? '0' : origValue;
    td.appendChild(input);
    input.focus();
    input.select();

    function _commit() {
      var raw = input.value.trim();
      var val = parseInt(raw, 10);
      if (isNaN(val) || val < 0) {
        /* Restore */
        _cancel();
        _toast('Valor inválido — deve ser um número inteiro não negativo.', 'warn');
        return;
      }

      /* Cross-field validation */
      if (inst.type === 'consultas') {
        if (col.field === 're' && val > row.ag) {
          _toast('Atenção: realizadas (' + val + ') > agendadas (' + row.ag + ').', 'warn');
        }
      }
      if (inst.type === 'mat') {
        var stockVal = col.field === 'stock' ? val : row.stock;
        var usadoVal = col.field === 'usado' ? val : row.usado;
        if (usadoVal > stockVal) {
          _toast('Atenção: consumido (' + usadoVal + ') > stock (' + stockVal + ').', 'warn');
        }
      }

      /* Update row */
      var oldVal = row[col.field];
      row[col.field] = val;
      _recompute(row, inst.type);

      /* Mark dirty */
      if (!inst._dirty[row._id]) inst._dirty[row._id] = {};
      inst._dirty[row._id][col.field] = val;

      /* Update cell */
      td.removeChild(input);
      span.textContent = val;
      span.style.display = '';
      td.classList.add('hp-grid-dirty');

      /* Update computed cells in same row */
      var tr = td.parentElement;
      COLS[inst.type].forEach(function (c) {
        if (!c.computed) return;
        var compTd = tr.querySelector('[data-col="' + c.key + '"]');
        if (!compTd) return;
        var v = row[c.key];
        if (c.key === 'pctRe' || c.key === 'pctCa' || c.key === 'pctDia' || c.key === 'pctConsumo') {
          compTd.textContent = v !== '—' ? v + '%' : '—';
        } else {
          compTd.textContent = v !== undefined ? v : '—';
        }
      });

      /* Update proc _totalDay for all rows on same date */
      if (inst.type === 'proc' && (col.field === 'manha' || col.field === 'tarde')) {
        _updateProcDayTotals(inst, row._date);
      }

      _updateDirtyBanner(inst);
    }

    function _cancel() {
      if (td.querySelector('.hp-grid-input')) td.removeChild(input);
      span.style.display = '';
    }

    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); _commit(); }
      if (e.key === 'Escape') { e.preventDefault(); _cancel(); }
      if (e.key === 'Tab') {
        e.preventDefault();
        _commit();
        /* Move to next editable td */
        var tr = td.parentElement;
        var allTds = Array.from(tr.parentElement.querySelectorAll('tr[data-row-id]')).reduce(function (acc, r) {
          return acc.concat(Array.from(r.querySelectorAll('.hp-grid-editable')));
        }, []);
        var idx = allTds.indexOf(td);
        var next = allTds[e.shiftKey ? idx - 1 : idx + 1];
        if (next) {
          var nextRow = _findRow(inst, next.dataset.rowId);
          var nextCol = _findCol(inst.type, next.dataset.col);
          if (nextRow && nextCol) _activateEdit(inst, next, nextRow, nextCol);
        }
      }
    });

    input.addEventListener('blur', function () {
      /* Slight delay so that keydown (Enter/Escape/Tab) fires first */
      setTimeout(function () {
        if (td.querySelector('.hp-grid-input')) _commit();
      }, 80);
    });
  }

  function _updateProcDayTotals(inst, date) {
    /* Recalculate _totalDay for all proc rows on same date */
    var dayRows = inst._rows.filter(function (r) { return r._date === date; });
    var dayTotal = dayRows.reduce(function (acc, r) { return acc + (r.total || 0); }, 0);
    dayRows.forEach(function (r) {
      r._totalDay = dayTotal;
      _recompute(r, 'proc');
    });
    /* Refresh pctDia cells in DOM for that date */
    var tbody = inst._el.querySelector('tbody');
    if (!tbody) return;
    dayRows.forEach(function (r) {
      var tr = tbody.querySelector('tr[data-row-id="' + CSS.escape(r._id) + '"]');
      if (!tr) return;
      var pctTd = tr.querySelector('[data-col="pctDia"]');
      if (pctTd) pctTd.textContent = r.pctDia !== '—' ? r.pctDia + '%' : '—';
    });
  }

  function _findRow(inst, id) {
    return inst._rows.find(function (r) { return r._id === id; }) || null;
  }

  function _findCol(type, key) {
    return (COLS[type] || []).find(function (c) { return c.key === key; }) || null;
  }

  /* ─────────────────────────────────────────────────────────────
     Delete row
  ───────────────────────────────────────────────────────────── */
  function _deleteRow(inst, rowId, label, date) {
    var msg = 'Apagar "' + label + '" em ' + _formatDate(date) + '? Esta acção não pode ser desfeita.';
    if (!confirm(msg)) return;

    try {
      if (inst.type === 'summary') {
        /* Delete ALL data for that date */
        localStorage.removeItem(_storageKey('consultas', date));
        localStorage.removeItem(_storageKey('proc', date));
        localStorage.removeItem(_storageKey('mat', date));
        /* Update saved dates list */
        var saved = _safeParse(_safeGet('prenda_saved_dates'), []);
        saved = saved.filter(function (d) { return d !== date; });
        _safeSet('prenda_saved_dates', JSON.stringify(saved));
      } else if (inst.type === 'consultas') {
        var raw = _safeGet(_storageKey('consultas', date));
        var data = _safeParse(raw, {});
        delete data[label];
        _safeSet(_storageKey('consultas', date), JSON.stringify(data));
      } else if (inst.type === 'proc') {
        var raw = _safeGet(_storageKey('proc', date));
        var data = _safeParse(raw, {});
        delete data[label];
        _safeSet(_storageKey('proc', date), JSON.stringify(data));
      } else if (inst.type === 'mat') {
        var raw = _safeGet(_storageKey('mat', date));
        var data = _safeParse(raw, {});
        delete data[label];
        _safeSet(_storageKey('mat', date), JSON.stringify(data));
      }
    } catch (e) {
      console.error(LOG, 'Erro ao apagar linha:', e);
      _toast('Erro ao apagar: ' + e.message, 'err');
      return;
    }

    /* Clean up dirty state for deleted row */
    delete inst._dirty[rowId];

    _toast('Eliminado', 'del');
    if (typeof inst.opts.onDelete === 'function') inst.opts.onDelete(date, label);

    /* Re-read and re-render */
    _reloadData(inst);
  }

  /* ─────────────────────────────────────────────────────────────
     Reload data (used after delete / external refresh)
  ───────────────────────────────────────────────────────────── */
  function _reloadData(inst) {
    var allDates = _getSavedDates();
    var dates = _filterDatesByPeriod(allDates, inst._period, inst._dateFrom, inst._dateTo);
    inst._rows = _loadRows(inst.type, dates);
    inst._apply();
    _render(inst);
    _updateCount(inst);
  }

  function _updateCount(inst) {
    var countEl = inst._el.querySelector('.hp-grid-count');
    if (countEl) countEl.textContent = inst._filtered.length + ' registos';
  }

  /* ─────────────────────────────────────────────────────────────
     Event delegation setup
  ───────────────────────────────────────────────────────────── */
  function _bindEvents(inst) {
    var container = inst._el;

    /* Click on table body — editing or delete */
    var tableClickHandler = function (e) {
      var btn = e.target.closest('.hp-grid-del-btn');
      if (btn) {
        var rowId = btn.dataset.rowId;
        var label = btn.dataset.label;
        var date  = btn.dataset.date;
        _deleteRow(inst, rowId, label, date);
        return;
      }

      var td = e.target.closest('.hp-grid-editable');
      if (!td) return;
      /* Summary type is not editable */
      if (inst.type === 'summary') return;
      var rowId = td.dataset.rowId;
      var colKey = td.dataset.col;
      var row = _findRow(inst, rowId);
      var col = _findCol(inst.type, colKey);
      if (row && col && col.editable) {
        _activateEdit(inst, td, row, col);
      }
    };
    container.addEventListener('click', tableClickHandler);
    inst._listeners.push({ el: container, type: 'click', fn: tableClickHandler });

    /* Toolbar — type selector */
    var toolbar = container.querySelector('.hp-grid-toolbar');

    var typeSel = toolbar.querySelector('.hp-grid-type-sel');
    var typeHandler = function () {
      inst.type = typeSel.value;
      inst._dirty = {};
      _reloadData(inst);
    };
    typeSel.addEventListener('change', typeHandler);
    inst._listeners.push({ el: typeSel, type: 'change', fn: typeHandler });

    /* Toolbar — search */
    var searchEl = toolbar.querySelector('.hp-grid-search');
    var searchHandler = function () {
      inst._search = searchEl.value;
      inst._apply();
      _renderBody(inst);
      _updateCount(inst);
    };
    searchEl.addEventListener('input', searchHandler);
    inst._listeners.push({ el: searchEl, type: 'input', fn: searchHandler });

    /* Toolbar — period filter */
    var periodSel = toolbar.querySelector('.hp-grid-period-filter');
    var dateFrom  = toolbar.querySelector('.hp-grid-date-from');
    var dateTo    = toolbar.querySelector('.hp-grid-date-to');

    var periodHandler = function () {
      inst._period = periodSel.value;
      dateFrom.style.display = inst._period === 'range' ? '' : 'none';
      dateTo.style.display   = inst._period === 'range' ? '' : 'none';
      _reloadData(inst);
    };
    periodSel.addEventListener('change', periodHandler);
    inst._listeners.push({ el: periodSel, type: 'change', fn: periodHandler });

    var rangeHandler = function () {
      inst._dateFrom = dateFrom.value;
      inst._dateTo   = dateTo.value;
      _reloadData(inst);
    };
    dateFrom.addEventListener('change', rangeHandler);
    dateTo.addEventListener('change', rangeHandler);
    inst._listeners.push({ el: dateFrom, type: 'change', fn: rangeHandler });
    inst._listeners.push({ el: dateTo,   type: 'change', fn: rangeHandler });

    /* Toolbar — CSV */
    var csvBtn = toolbar.querySelector('.hp-grid-btn-csv');
    var csvHandler = function () { _exportCSV(inst); };
    csvBtn.addEventListener('click', csvHandler);
    inst._listeners.push({ el: csvBtn, type: 'click', fn: csvHandler });

    /* Toolbar — Excel */
    var excelBtn = toolbar.querySelector('.hp-grid-btn-excel');
    var excelHandler = function () { _exportExcel(inst); };
    excelBtn.addEventListener('click', excelHandler);
    inst._listeners.push({ el: excelBtn, type: 'click', fn: excelHandler });

    /* Toolbar — Refresh */
    var refreshBtn = toolbar.querySelector('.hp-grid-btn-refresh');
    var refreshHandler = function () { GridHP.refresh(container.id); };
    refreshBtn.addEventListener('click', refreshHandler);
    inst._listeners.push({ el: refreshBtn, type: 'click', fn: refreshHandler });

    /* Dirty banner — save now */
    var banner = container.querySelector('.hp-grid-dirty-banner');
    var saveBannerBtn = banner.querySelector('.hp-grid-dirty-save');
    var saveBannerHandler = function () { GridHP.flushChanges(container.id); };
    saveBannerBtn.addEventListener('click', saveBannerHandler);
    inst._listeners.push({ el: saveBannerBtn, type: 'click', fn: saveBannerHandler });

    /* Dirty banner — discard */
    var discardBtn = banner.querySelector('.hp-grid-dirty-banner-discard');
    var discardHandler = function () { GridHP.refresh(container.id); };
    discardBtn.addEventListener('click', discardHandler);
    inst._listeners.push({ el: discardBtn, type: 'click', fn: discardHandler });

    /* Header sort */
    var theadClickHandler = function (e) {
      var th = e.target.closest('.hp-grid-th.sortable');
      if (!th) return;
      var colDef = (COLS[inst.type] || []).find(function (c) { return c.key === th.dataset.col; });
      if (!colDef || !colDef.sortKey) return;
      var key = colDef.sortKey;
      if (inst._sortCol === key) {
        if (inst._sortDir === 'asc') { inst._sortDir = 'desc'; }
        else if (inst._sortDir === 'desc') { inst._sortCol = null; inst._sortDir = null; }
        else { inst._sortDir = 'asc'; }
      } else {
        inst._sortCol = key;
        inst._sortDir = 'asc';
      }
      inst._apply();
      /* Re-render header arrows */
      container.querySelectorAll('.hp-grid-th').forEach(function (t) {
        t.classList.remove('sort-asc', 'sort-desc');
        var arrow = t.querySelector('.sort-arrow');
        if (arrow) arrow.textContent = '↕';
      });
      if (inst._sortCol) {
        var activeTh = container.querySelector('.hp-grid-th[data-col="' + _keyToColKey(inst.type, inst._sortCol) + '"]');
        if (activeTh) {
          activeTh.classList.add(inst._sortDir === 'asc' ? 'sort-asc' : 'sort-desc');
          var arrow = activeTh.querySelector('.sort-arrow');
          if (arrow) arrow.textContent = inst._sortDir === 'asc' ? '▲' : '▼';
        }
      }
      _renderBody(inst);
      _updateCount(inst);
    };
    container.addEventListener('click', theadClickHandler);
    inst._listeners.push({ el: container, type: 'click', fn: theadClickHandler });
  }

  function _keyToColKey(type, sortKey) {
    var col = (COLS[type] || []).find(function (c) { return c.sortKey === sortKey; });
    return col ? col.key : sortKey;
  }

  /* ─────────────────────────────────────────────────────────────
     Apply sort + filter pipeline
  ───────────────────────────────────────────────────────────── */
  function _applyPipeline(inst) {
    var sorted = _sortRows(inst._rows, inst._sortCol, inst._sortDir);
    inst._filtered = _filterRows(sorted, inst._search);
  }

  /* ─────────────────────────────────────────────────────────────
     flushChanges — write dirty rows to localStorage
  ───────────────────────────────────────────────────────────── */
  function _flushChanges(inst) {
    var count = 0;
    var type = inst.type;

    /* Group dirty rows by date */
    var byDate = {};
    Object.keys(inst._dirty).forEach(function (rowId) {
      var row = _findRow(inst, rowId);
      if (!row) return;
      var date = row._date;
      if (!byDate[date]) byDate[date] = [];
      byDate[date].push({ row: row, changes: inst._dirty[rowId] });
    });

    Object.keys(byDate).forEach(function (date) {
      try {
        var storageType = type === 'summary' ? null : type;
        if (!storageType) return;

        var raw = _safeGet(_storageKey(storageType, date));
        var data = _safeParse(raw, {});

        byDate[date].forEach(function (entry) {
          var row = entry.row;
          var changes = entry.changes;
          var key = type === 'consultas' ? row.esp : type === 'proc' ? row.proc : row.mat;
          if (!key) return;
          if (!data[key]) data[key] = {};
          Object.keys(changes).forEach(function (field) {
            data[key][field] = changes[field];
          });
          count++;
        });

        _safeSet(_storageKey(storageType, date), JSON.stringify(data));

        /* Ensure date is in saved_dates */
        var saved = _safeParse(_safeGet('prenda_saved_dates'), []);
        if (saved.indexOf(date) === -1) {
          saved.push(date);
          saved.sort();
          _safeSet('prenda_saved_dates', JSON.stringify(saved));
        }
      } catch (e) {
        console.error(LOG, 'Erro ao guardar data', date, ':', e);
      }
    });

    /* Clear dirty state */
    inst._dirty = {};
    _updateDirtyBanner(inst);

    /* Remove dirty cell highlights */
    inst._el.querySelectorAll('.hp-grid-dirty').forEach(function (td) {
      td.classList.remove('hp-grid-dirty');
    });

    _toast(count + ' registo(s) guardado(s) com sucesso.', 'save');
    if (typeof inst.opts.onSave === 'function') inst.opts.onSave(count);
    console.log(LOG, 'flushChanges:', count, 'linhas guardadas.');
    return count;
  }

  /* ─────────────────────────────────────────────────────────────
     Export CSV
  ───────────────────────────────────────────────────────────── */
  function _exportCSV(inst) {
    var rows = inst._filtered;
    if (!rows.length) { _toast('Sem dados para exportar.', 'warn'); return; }
    var cols = COLS[inst.type].filter(function (c) { return c.key !== '_actions'; });
    var headers = cols.map(function (c) { return c.label; }).join(';');
    var lines = ['﻿' + headers];

    rows.forEach(function (row) {
      var cells = cols.map(function (col) {
        if (col.key === 'data') return row._dateLabel || row._label || '';
        if (col.key === 'pctRe' || col.key === 'pctCa' || col.key === 'pctDia' || col.key === 'pctConsumo') {
          var v = row[col.key];
          return v !== '—' ? v + '%' : '—';
        }
        var v = row[col.key];
        return v !== undefined ? v : '—';
      });
      lines.push(cells.join(';'));
    });

    var csv = lines.join('\r\n');
    var blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'Prenda_Grid_' + inst.type + '_' + _todayKey() + '.csv';
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { document.body.removeChild(a); URL.revokeObjectURL(url); }, 200);
    _toast('CSV exportado com ' + rows.length + ' linha(s).', 'ok');
  }

  /* ─────────────────────────────────────────────────────────────
     Export Excel — delegate to exportToExcel if available
  ───────────────────────────────────────────────────────────── */
  function _exportExcel(inst) {
    if (typeof global.exportToExcel === 'function') {
      var allDates = _getSavedDates();
      var dates = _filterDatesByPeriod(allDates, inst._period, inst._dateFrom, inst._dateTo);
      global.exportToExcel(dates, inst._period || 'grid');
    } else {
      _toast('exportToExcel não disponível — a usar CSV como substituto.', 'warn');
      _exportCSV(inst);
    }
  }

  /* ─────────────────────────────────────────────────────────────
     PUBLIC API — window.GridHP
  ───────────────────────────────────────────────────────────── */
  var GridHP = {

    /**
     * Creates a grid instance in the DOM element with given ID.
     * @param {string} containerId
     * @param {object} [options]  { type, onSave, onDelete }
     */
    init: function (containerId, options) {
      _injectCSS();

      var container = document.getElementById(containerId);
      if (!container) {
        console.error(LOG, 'init: elemento não encontrado:', containerId);
        return;
      }

      /* Destroy existing instance if present */
      if (_instances[containerId]) {
        GridHP.destroy(containerId);
      }

      options = options || {};
      var type = options.type || 'consultas';

      /* Create instance state */
      var inst = {
        id: containerId,
        type: type,
        opts: options,
        _el: container,
        _rows: [],
        _filtered: [],
        _dirty: {},     /* { rowId: { field: newValue } } */
        _search: '',
        _period: 'all',
        _dateFrom: '',
        _dateTo: '',
        _sortCol: '_date',
        _sortDir: 'desc',
        _listeners: []
      };

      /* apply = sort + filter pipeline shorthand */
      inst._apply = function () { _applyPipeline(inst); };

      /* Setup container */
      container.classList.add('hp-grid-container');

      /* Insert dirty banner first, then toolbar */
      var banner = _buildDirtyBanner(inst);
      container.appendChild(banner);

      var toolbar = _buildToolbar(inst);
      container.appendChild(toolbar);

      /* Load data */
      var allDates = _getSavedDates();
      var dates = _filterDatesByPeriod(allDates, inst._period, inst._dateFrom, inst._dateTo);
      inst._rows = _loadRows(type, dates);
      inst._apply();

      _render(inst);
      _updateCount(inst);

      /* Bind events */
      _bindEvents(inst);

      _instances[containerId] = inst;
      console.log(LOG, 'init: grid "' + containerId + '" criada. Tipo:', type, '| Linhas:', inst._rows.length);
    },

    /**
     * Re-reads data and re-renders the grid.
     */
    refresh: function (containerId) {
      var inst = _instances[containerId];
      if (!inst) { console.warn(LOG, 'refresh: instância não encontrada:', containerId); return; }
      inst._dirty = {};
      _reloadData(inst);
      _updateCount(inst);
      console.log(LOG, 'refresh:', containerId);
    },

    /**
     * Filters rows client-side.
     */
    setFilter: function (containerId, searchText) {
      var inst = _instances[containerId];
      if (!inst) { console.warn(LOG, 'setFilter: instância não encontrada:', containerId); return; }
      inst._search = searchText || '';
      var searchEl = inst._el.querySelector('.hp-grid-search');
      if (searchEl) searchEl.value = inst._search;
      inst._apply();
      _renderBody(inst);
      _updateCount(inst);
    },

    /**
     * Sets sort direction for a column.
     * @param {string} direction  'asc'|'desc'|null
     */
    setSort: function (containerId, colKey, direction) {
      var inst = _instances[containerId];
      if (!inst) { console.warn(LOG, 'setSort: instância não encontrada:', containerId); return; }
      inst._sortCol = colKey || null;
      inst._sortDir = direction || null;
      inst._apply();
      _renderBody(inst);
    },

    /**
     * Returns { totalRows, filteredRows, dirtyRows }.
     */
    getStats: function (containerId) {
      var inst = _instances[containerId];
      if (!inst) return { totalRows: 0, filteredRows: 0, dirtyRows: 0 };
      return {
        totalRows:    inst._rows.length,
        filteredRows: inst._filtered.length,
        dirtyRows:    _countDirty(inst)
      };
    },

    /**
     * Commits all dirty rows to localStorage.
     * Returns count of flushed rows.
     */
    flushChanges: function (containerId) {
      var inst = _instances[containerId];
      if (!inst) { console.warn(LOG, 'flushChanges: instância não encontrada:', containerId); return 0; }
      return _flushChanges(inst);
    },

    /**
     * Removes event listeners and clears the container.
     */
    destroy: function (containerId) {
      var inst = _instances[containerId];
      if (!inst) return;
      /* Remove all listeners */
      inst._listeners.forEach(function (l) {
        try { l.el.removeEventListener(l.type, l.fn); } catch (e) { /* ignore */ }
      });
      /* Clear container */
      var container = document.getElementById(containerId);
      if (container) {
        container.classList.remove('hp-grid-container');
        container.innerHTML = '';
      }
      delete _instances[containerId];
      console.log(LOG, 'destroy:', containerId);
    }
  };

  global.GridHP = GridHP;
  console.log(LOG, 'hprenda-grid.js carregado. window.GridHP disponível.');

}(window));
