/**
 * hprenda-mail.js — Integração de email para exportação de relatórios
 * Hospital do Prenda — Consulta Externa
 *
 * Carregado com defer. Expõe (em window):
 *   buildEmailBody(dates, period)      → string (texto simples em português)
 *   prepareEmailWithData(mode)         → abre mailto: ou mostra modal
 *   showEmailModal(subject, body, attachment) → modal de pré-visualização
 */

(function (global) {
  'use strict';

  var LOG = '[hprenda-mail]';

  /* ─────────────────────────────────────────────────────────────
     Helpers internos
  ───────────────────────────────────────────────────────────── */

  function _safeGet(k) {
    try { return localStorage.getItem(k); } catch (e) { return null; }
  }
  function _storageKey(type, date) { return 'prenda_' + type + '_' + date; }
  function _todayKey() { return new Date().toISOString().slice(0, 10); }
  function _formatDate(d) {
    if (!d) return '—';
    var p = d.split('-'); return p[2] + '/' + p[1] + '/' + p[0];
  }
  function _formatDateTime() {
    var now = new Date();
    return now.toLocaleString('pt-PT', {
      day:'2-digit', month:'2-digit', year:'numeric',
      hour:'2-digit', minute:'2-digit'
    });
  }

  function _toast(msg, type) {
    if (typeof global.toast === 'function') { global.toast(msg, type || 'info'); }
    else { console.info(LOG, '[toast]', msg); }
  }

  function _ESPECIALIDADES() {
    return global.ESPECIALIDADES || [
      'Medicina Interna','Ortopedia','Cirurgia Geral','Proctologia',
      'Cardiologia','Reumatologia','Estomatologia','Oftalmologia',
      'Optometria','Anestesiologia','Maxilo Facial','Neurocirurgia',
      'Gastroenterologia','Neurologia','Otorrinolaringologia'
    ];
  }
  function _PROCEDIMENTOS() {
    return global.PROCEDIMENTOS || [
      'Curativos feitos','Pontos retirados','Gessos retirados',
      'Gessos aplicados','Algálias retiradas','Talas colocadas',
      'Talas retiradas','Injeções','Infiltrações',
      'Exodontia simples','Exodontia complicada'
    ];
  }
  function _MATERIAIS() {
    return global.MATERIAIS || [
      {nome:'Fitas de glicemia',unit:'unidade'},
      {nome:'Rolo de gesso',unit:'unidade'},
      {nome:'Ligadura',unit:'unidade'},
      {nome:'Seringas',unit:'unidade'},
      {nome:'Ampolas injectáveis',unit:'unidade'},
      {nome:'Compressas',unit:'unidade'},
      {nome:'Bisturi',unit:'unidade'},
      {nome:'Sacos de colectores',unit:'unidade'},
      {nome:'Luvas descartáveis',unit:'par'},
      {nome:'Algodão',unit:'grama'},
      {nome:'Soro fisiológico',unit:'frasco'},
      {nome:'Algália',unit:'unidade'}
    ];
  }

  /* Aggregation helpers */
  function _aggConsultas(dates) {
    var esp = _ESPECIALIDADES(), agg = {};
    esp.forEach(function (e) { agg[e] = {ag:0,re:0,ca:0,m15:0,M15:0}; });
    dates.forEach(function (d) {
      var raw = _safeGet(_storageKey('consultas', d));
      var c = raw ? JSON.parse(raw) : {};
      esp.forEach(function (e) {
        if (c[e]) ['ag','re','ca','m15','M15'].forEach(function (f) { agg[e][f] += (c[e][f]||0); });
      });
    });
    return agg;
  }
  function _aggProc(dates) {
    var proc = _PROCEDIMENTOS(), agg = {};
    proc.forEach(function (p) { agg[p] = {manha:0,tarde:0}; });
    dates.forEach(function (d) {
      var raw = _safeGet(_storageKey('proc', d));
      var p = raw ? JSON.parse(raw) : {};
      proc.forEach(function (pr) {
        if (p[pr]) ['manha','tarde'].forEach(function (f) { agg[pr][f] += (p[pr][f]||0); });
      });
    });
    return agg;
  }
  function _aggMat(dates) {
    var mats = _MATERIAIS(), agg = {};
    mats.forEach(function (m) { agg[m.nome] = {stock:0,usado:0,unit:m.unit}; });
    dates.forEach(function (d) {
      var raw = _safeGet(_storageKey('mat', d));
      var m = raw ? JSON.parse(raw) : {};
      mats.forEach(function (mat) {
        if (m[mat.nome]) ['stock','usado'].forEach(function (f) { agg[mat.nome][f] += (m[mat.nome][f]||0); });
      });
    });
    return agg;
  }

  function _line(ch, n) { return Array(n+1).join(ch); }
  function _rpad(str, w) { str = String(str); while (str.length < w) str += ' '; return str; }
  function _lpad(str, w) { str = String(str); while (str.length < w) str = ' ' + str; return str; }

  /* ═══════════════════════════════════════════════════════════════
     1.  buildEmailBody(dates, period) → string
  ═══════════════════════════════════════════════════════════════ */
  /**
   * Constrói o corpo de um email em texto simples com o resumo dos dados.
   * @param {string[]} dates  — array de YYYY-MM-DD
   * @param {string}   period — 'dia' | 'semana' | 'mes' | outro
   * @returns {string}
   */
  global.buildEmailBody = function (dates, period) {
    if (!dates || dates.length === 0) { dates = [_todayKey()]; }
    period = period || 'dia';

    var esp  = _ESPECIALIDADES();
    var proc = _PROCEDIMENTOS();
    var mats = _MATERIAIS();
    var cAgg = _aggConsultas(dates);
    var pAgg = _aggProc(dates);
    var mAgg = _aggMat(dates);

    /* Totais */
    var tAg=0, tRe=0, tCa=0, tm15=0, tM15=0;
    Object.values(cAgg).forEach(function (v) { tAg+=v.ag; tRe+=v.re; tCa+=v.ca; tm15+=v.m15; tM15+=v.M15; });
    var tProc=0;
    Object.values(pAgg).forEach(function (v) { tProc += v.manha + v.tarde; });
    var tStock=0, tUsado=0;
    Object.values(mAgg).forEach(function (v) { tStock += v.stock; tUsado += v.usado; });

    var pctR = tAg > 0 ? (tRe/tAg*100).toFixed(1) + '%' : 'N/D';
    var pctC = tAg > 0 ? (tCa/tAg*100).toFixed(1) + '%' : 'N/D';

    var periodLabel = {
      dia:    'Relatório Diário',
      semana: 'Relatório Semanal',
      mes:    'Relatório Mensal'
    }[period] || 'Relatório';

    var dateRange = dates.length === 1
      ? _formatDate(dates[0])
      : _formatDate(dates[0]) + ' a ' + _formatDate(dates[dates.length-1]);

    var sep  = _line('=', 60);
    var sep2 = _line('-', 60);
    var lines = [];

    /* Cabeçalho */
    lines.push(sep);
    lines.push('HOSPITAL DO PRENDA — CONSULTA EXTERNA');
    lines.push(periodLabel.toUpperCase() + ' | ' + dateRange);
    lines.push('Emitido em: ' + _formatDateTime());
    lines.push(sep);
    lines.push('');

    /* Resumo executivo */
    lines.push('RESUMO EXECUTIVO');
    lines.push(sep2);
    lines.push(_rpad('Consultas Agendadas:',      30) + _lpad(tAg,   8));
    lines.push(_rpad('Consultas Realizadas:',     30) + _lpad(tRe,   8));
    lines.push(_rpad('Consultas Canceladas:',     30) + _lpad(tCa,   8));
    lines.push(_rpad('Pacientes < 15 Anos:',      30) + _lpad(tm15,  8));
    lines.push(_rpad('Pacientes > 15 Anos:',      30) + _lpad(tM15,  8));
    lines.push(_rpad('Taxa de Realização:',       30) + _lpad(pctR,  8));
    lines.push(_rpad('Taxa de Cancelamento:',     30) + _lpad(pctC,  8));
    lines.push(_rpad('Total de Procedimentos:',   30) + _lpad(tProc, 8));
    lines.push(_rpad('Material Consumido:',       30) + _lpad(tUsado,8));
    lines.push(_rpad('Saldo de Material:',        30) + _lpad(Math.max(0, tStock-tUsado), 8));
    lines.push('');

    /* Tabela de consultas por especialidade */
    lines.push('CONSULTAS POR ESPECIALIDADE');
    lines.push(sep2);
    lines.push(_rpad('Especialidade', 28) + _lpad('Ag.', 6) + _lpad('Re.', 6) +
               _lpad('Ca.', 6) + _lpad('<15', 6) + _lpad('>15', 6) + _lpad('% Re.', 8));
    lines.push(sep2);
    esp.forEach(function (e) {
      var d = cAgg[e];
      if (d.ag === 0 && d.re === 0 && d.ca === 0) return;
      var pR = d.ag > 0 ? (d.re/d.ag*100).toFixed(0) + '%' : '—';
      lines.push(
        _rpad(e.length > 27 ? e.slice(0, 25) + '…' : e, 28) +
        _lpad(d.ag,  6) + _lpad(d.re,  6) + _lpad(d.ca, 6) +
        _lpad(d.m15, 6) + _lpad(d.M15, 6) + _lpad(pR,   8)
      );
    });
    lines.push(sep2);
    lines.push(
      _rpad('TOTAL GERAL', 28) +
      _lpad(tAg, 6) + _lpad(tRe, 6) + _lpad(tCa, 6) +
      _lpad(tm15, 6) + _lpad(tM15, 6) + _lpad(pctR, 8)
    );
    lines.push('');

    /* Tabela de procedimentos */
    lines.push('PROCEDIMENTOS');
    lines.push(sep2);
    lines.push(_rpad('Procedimento', 28) + _lpad('Manhã', 8) + _lpad('Tarde', 8) + _lpad('Total', 8));
    lines.push(sep2);
    var hasProc = false;
    proc.forEach(function (p) {
      var d = pAgg[p];
      if (d.manha === 0 && d.tarde === 0) return;
      hasProc = true;
      lines.push(
        _rpad(p.length > 27 ? p.slice(0, 25) + '…' : p, 28) +
        _lpad(d.manha, 8) + _lpad(d.tarde, 8) + _lpad(d.manha+d.tarde, 8)
      );
    });
    if (!hasProc) lines.push('  (nenhum procedimento registado)');
    lines.push(_rpad('TOTAL', 28) + _lpad('', 8) + _lpad('', 8) + _lpad(tProc, 8));
    lines.push('');

    /* Tabela de material */
    lines.push('MATERIAL CLÍNICO');
    lines.push(sep2);
    lines.push(_rpad('Material', 28) + _lpad('Stock', 8) + _lpad('Usado', 8) + _lpad('Saldo', 8));
    lines.push(sep2);
    var hasMat = false;
    mats.forEach(function (mat) {
      var d = mAgg[mat.nome];
      if (d.stock === 0 && d.usado === 0) return;
      hasMat = true;
      var saldo = Math.max(0, d.stock - d.usado);
      var alert = saldo < 10 && d.stock > 0 ? ' (!)' : '';
      lines.push(
        _rpad((mat.nome.length > 27 ? mat.nome.slice(0, 25) + '…' : mat.nome) + alert, 28) +
        _lpad(d.stock, 8) + _lpad(d.usado, 8) + _lpad(saldo, 8)
      );
    });
    if (!hasMat) lines.push('  (nenhum material registado)');
    lines.push(_rpad('TOTAL', 28) + _lpad(tStock, 8) + _lpad(tUsado, 8) + _lpad(Math.max(0, tStock-tUsado), 8));
    lines.push('');

    /* Nota */
    lines.push(sep);
    lines.push('Nota: (!) indica material com saldo inferior a 10 unidades.');
    lines.push('Este relatório foi gerado automaticamente pelo sistema de Consulta Externa.');
    lines.push('Para informações adicionais contacte o Serviço de Consulta Externa.');
    lines.push(sep);

    var body = lines.join('\n');
    console.log(LOG, 'buildEmailBody — ' + lines.length + ' linhas, período:', period);
    return body;
  };

  /* ═══════════════════════════════════════════════════════════════
     2.  prepareEmailWithData(mode) — abrir cliente de email
  ═══════════════════════════════════════════════════════════════ */
  /**
   * Prepara e abre um cliente de email com o relatório.
   * @param {string} [mode] — 'summary' | 'full' (default: 'full')
   */
  global.prepareEmailWithData = function (mode) {
    mode = mode || 'full';
    console.log(LOG, 'prepareEmailWithData — modo:', mode);

    /* Obter destino do email */
    var destInput = document.getElementById('email-dest');
    var dest = destInput ? destInput.value.trim() : '';

    /* Obter período seleccionado */
    var periodSelect = document.getElementById('export-period');
    var period = periodSelect ? periodSelect.value : 'dia';

    /* Calcular datas */
    var allDates = JSON.parse(_safeGet('prenda_saved_dates') || '[]');
    var dates = [];
    var today = _todayKey();

    if (period === 'dia') {
      dates = allDates.includes(today) ? [today] : [today];
    } else if (period === 'semana') {
      var mon = _weekOf(today);
      var sat = new Date(mon + 'T00:00:00'); sat.setDate(sat.getDate() + 6);
      var satStr = sat.toISOString().slice(0, 10);
      dates = allDates.filter(function (d) { return d >= mon && d <= satStr; });
      if (dates.length === 0) dates = [today];
    } else if (period === 'mes') {
      var m = today.slice(0, 7);
      dates = allDates.filter(function (d) { return d.startsWith(m); });
      if (dates.length === 0) dates = [today];
    } else if (period === 'custom') {
      var startEl = document.getElementById('range-start');
      var endEl   = document.getElementById('range-end');
      var start   = startEl ? startEl.value : today;
      var end     = endEl   ? endEl.value   : today;
      dates = allDates.filter(function (d) { return d >= start && d <= end; });
      if (dates.length === 0) dates = [today];
    } else {
      dates = [today];
    }

    /* Construir assunto */
    var periodLabels = {
      dia:    'Relatório Diário',
      semana: 'Relatório Semanal',
      mes:    'Relatório Mensal',
      custom: 'Relatório Personalizado'
    };
    var dateRange = dates.length === 1
      ? _formatDate(dates[0])
      : _formatDate(dates[0]) + ' a ' + _formatDate(dates[dates.length-1]);
    var subject = 'Hospital do Prenda — Consulta Externa — ' +
                  (periodLabels[period] || 'Relatório') + ' — ' + dateRange;

    /* Construir corpo */
    var body;
    if (mode === 'summary') {
      body = _buildSummaryEmailBody(dates, period);
    } else {
      body = global.buildEmailBody(dates, period);
    }

    /* Tentar abrir mailto: */
    var mailtoLimit = 1800; /* caracteres — alguns clientes têm limite */
    var bodyForMailto = body.length > mailtoLimit
      ? body.slice(0, mailtoLimit) + '\n\n[... conteúdo truncado. Ver ficheiro em anexo ...]'
      : body;

    var mailto = 'mailto:' + encodeURIComponent(dest) +
                 '?subject=' + encodeURIComponent(subject) +
                 '&body=' + encodeURIComponent(bodyForMailto);

    /* Verificar se o mailto é aberto com sucesso */
    var opened = false;
    try {
      var win = global.open(mailto, '_blank');
      /* Alguns browsers retornam null se o protocolo não for suportado */
      if (win !== null) opened = true;
    } catch (e) {
      console.warn(LOG, 'Erro ao abrir mailto:', e);
    }

    if (!opened || body.length > mailtoLimit) {
      /* Fallback: mostrar modal com o conteúdo */
      console.log(LOG, 'Fallback: a mostrar modal de email.');
      global.showEmailModal(subject, body, null);
    } else {
      _toast('Cliente de email aberto com o relatório.', 'ok');
    }
  };

  /* Helper: semana de uma data (segunda-feira) */
  function _weekOf(d) {
    var dt = new Date(d + 'T00:00:00');
    var day = dt.getDay();
    var diff = dt.getDate() - day + (day === 0 ? -6 : 1);
    var mon = new Date(dt); mon.setDate(diff);
    return mon.toISOString().slice(0, 10);
  }

  /* Versão resumida (só totais) */
  function _buildSummaryEmailBody(dates, period) {
    var esp  = _ESPECIALIDADES();
    var proc = _PROCEDIMENTOS();
    var mats = _MATERIAIS();
    var cAgg = _aggConsultas(dates);
    var pAgg = _aggProc(dates);
    var mAgg = _aggMat(dates);

    var tAg=0, tRe=0, tCa=0, tm15=0, tM15=0;
    Object.values(cAgg).forEach(function (v) { tAg+=v.ag; tRe+=v.re; tCa+=v.ca; tm15+=v.m15; tM15+=v.M15; });
    var tProc=0;
    Object.values(pAgg).forEach(function (v) { tProc += v.manha + v.tarde; });
    var tStock=0, tUsado=0;
    Object.values(mAgg).forEach(function (v) { tStock += v.stock; tUsado += v.usado; });

    var pctR = tAg > 0 ? (tRe/tAg*100).toFixed(1) + '%' : 'N/D';
    var pctC = tAg > 0 ? (tCa/tAg*100).toFixed(1) + '%' : 'N/D';
    var dateRange = dates.length === 1 ? _formatDate(dates[0])
      : _formatDate(dates[0]) + ' a ' + _formatDate(dates[dates.length-1]);
    var periodLabel = {dia:'Diário',semana:'Semanal',mes:'Mensal'}[period] || '';

    return [
      'Exmos. Senhores,',
      '',
      'Serve o presente para transmitir o resumo do Relatório ' + periodLabel +
      ' da Consulta Externa do Hospital do Prenda, referente ao período de ' + dateRange + '.',
      '',
      'RESUMO:',
      '  - Consultas Agendadas:    ' + tAg,
      '  - Consultas Realizadas:   ' + tRe + ' (' + pctR + ')',
      '  - Consultas Canceladas:   ' + tCa + ' (' + pctC + ')',
      '  - Pacientes < 15 Anos:    ' + tm15,
      '  - Pacientes > 15 Anos:    ' + tM15,
      '  - Total Procedimentos:    ' + tProc,
      '  - Material Consumido:     ' + tUsado + ' unid.',
      '  - Saldo de Material:      ' + Math.max(0, tStock-tUsado) + ' unid.',
      '',
      'Com os melhores cumprimentos,',
      'Serviço de Consulta Externa',
      'Hospital do Prenda',
      '',
      'Emitido em: ' + _formatDateTime()
    ].join('\n');
  }

  /* ═══════════════════════════════════════════════════════════════
     3.  showEmailModal(subject, body, attachment)
  ═══════════════════════════════════════════════════════════════ */
  /**
   * Mostra um modal com a pré-visualização do email.
   * @param {string}      subject    — assunto do email
   * @param {string}      body       — corpo em texto simples
   * @param {string|null} attachment — nome do ficheiro em anexo (opcional)
   */
  global.showEmailModal = function (subject, body, attachment) {
    console.log(LOG, 'showEmailModal — assunto:', subject);

    /* Remover modal anterior se existir */
    var existing = document.getElementById('hprenda-email-modal');
    if (existing) existing.remove();

    /* CSS injectado inline para independência */
    var style = document.createElement('style');
    style.id = 'hprenda-email-modal-style';
    style.textContent = [
      '#hprenda-email-modal {',
      '  position:fixed;inset:0;z-index:99999;background:rgba(0,0,0,0.55);',
      '  display:flex;align-items:center;justify-content:center;padding:16px;',
      '}',
      '#hprenda-email-modal .em-box {',
      '  background:#fff;border-radius:12px;box-shadow:0 20px 60px rgba(0,0,0,0.25);',
      '  width:100%;max-width:680px;max-height:90vh;display:flex;flex-direction:column;',
      '  overflow:hidden;',
      '}',
      '#hprenda-email-modal .em-header {',
      '  background:#1a56db;color:#fff;padding:16px 22px;',
      '  display:flex;align-items:center;justify-content:space-between;flex-shrink:0;',
      '}',
      '#hprenda-email-modal .em-title {',
      '  font-family:Inter,sans-serif;font-size:15px;font-weight:700;',
      '}',
      '#hprenda-email-modal .em-close {',
      '  background:rgba(255,255,255,0.15);border:none;color:#fff;',
      '  width:28px;height:28px;border-radius:50%;cursor:pointer;',
      '  font-size:16px;display:flex;align-items:center;justify-content:center;',
      '}',
      '#hprenda-email-modal .em-close:hover { background:rgba(255,255,255,0.25); }',
      '#hprenda-email-modal .em-body { padding:18px 22px;overflow-y:auto;flex:1; }',
      '#hprenda-email-modal .em-field { margin-bottom:14px; }',
      '#hprenda-email-modal .em-label {',
      '  font-family:Inter,sans-serif;font-size:11px;font-weight:700;',
      '  color:#6B7280;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:5px;',
      '}',
      '#hprenda-email-modal .em-subject-val {',
      '  font-family:Inter,sans-serif;font-size:13px;font-weight:600;color:#1A1A2E;',
      '  padding:10px 14px;background:#F8F9FB;border-radius:8px;border:1px solid #e5e7eb;',
      '}',
      '#hprenda-email-modal .em-attach {',
      '  display:inline-flex;align-items:center;gap:6px;',
      '  padding:6px 14px;background:#EEF2FF;border-radius:20px;',
      '  font-size:12px;font-weight:600;color:#4338ca;',
      '}',
      '#hprenda-email-modal .em-body-pre {',
      '  font-family:"Roboto Mono",monospace;font-size:11px;line-height:1.6;',
      '  white-space:pre-wrap;word-break:break-word;',
      '  padding:14px;background:#F8F9FB;border-radius:8px;border:1px solid #e5e7eb;',
      '  max-height:320px;overflow-y:auto;color:#374151;',
      '}',
      '#hprenda-email-modal .em-footer {',
      '  padding:14px 22px;border-top:1px solid #e5e7eb;',
      '  display:flex;gap:10px;justify-content:flex-end;flex-shrink:0;flex-wrap:wrap;',
      '}',
      '#hprenda-email-modal .em-btn {',
      '  display:inline-flex;align-items:center;gap:7px;',
      '  padding:9px 18px;border-radius:8px;font-family:Inter,sans-serif;',
      '  font-size:13px;font-weight:500;cursor:pointer;border:none;',
      '}',
      '#hprenda-email-modal .em-btn-primary { background:#1a56db;color:#fff; }',
      '#hprenda-email-modal .em-btn-primary:hover { background:#1447c0; }',
      '#hprenda-email-modal .em-btn-outline {',
      '  background:transparent;border:1px solid #d1d5db;color:#374151;',
      '}',
      '#hprenda-email-modal .em-btn-outline:hover { background:#F3F4F6; }',
      '#hprenda-email-modal .em-btn-green { background:#059669;color:#fff; }',
      '#hprenda-email-modal .em-btn-green:hover { background:#047857; }'
    ].join('\n');

    /* Remover estilo anterior se existir */
    var oldStyle = document.getElementById('hprenda-email-modal-style');
    if (oldStyle) oldStyle.remove();
    document.head.appendChild(style);

    /* Construir HTML do modal */
    var attachHtml = attachment
      ? '<div class="em-field"><div class="em-label">Anexo</div>' +
        '<span class="em-attach">📎 ' + attachment + '</span></div>'
      : '';

    var modal = document.createElement('div');
    modal.id = 'hprenda-email-modal';
    modal.innerHTML =
      '<div class="em-box">' +
        '<div class="em-header">' +
          '<span class="em-title">📧 Pré-visualização do Email</span>' +
          '<button class="em-close" id="em-close-btn" title="Fechar">&times;</button>' +
        '</div>' +
        '<div class="em-body">' +
          '<div class="em-field">' +
            '<div class="em-label">Assunto</div>' +
            '<div class="em-subject-val" id="em-subject-val">' + _escHtml(subject) + '</div>' +
          '</div>' +
          attachHtml +
          '<div class="em-field">' +
            '<div class="em-label">Corpo do Email</div>' +
            '<pre class="em-body-pre" id="em-body-pre">' + _escHtml(body) + '</pre>' +
          '</div>' +
        '</div>' +
        '<div class="em-footer">' +
          '<button class="em-btn em-btn-outline" id="em-copy-btn">📋 Copiar para área de transferência</button>' +
          '<button class="em-btn em-btn-green" id="em-mailto-btn">✉ Abrir cliente de email</button>' +
          '<button class="em-btn em-btn-primary" id="em-close-btn2">Fechar</button>' +
        '</div>' +
      '</div>';

    document.body.appendChild(modal);

    /* Fechar ao clicar no fundo */
    modal.addEventListener('click', function (e) {
      if (e.target === modal) _closeEmailModal();
    });

    /* Fechar com Escape */
    function _escHandler(e) {
      if (e.key === 'Escape') { _closeEmailModal(); document.removeEventListener('keydown', _escHandler); }
    }
    document.addEventListener('keydown', _escHandler);

    function _closeEmailModal() {
      var m = document.getElementById('hprenda-email-modal');
      if (m) { m.style.opacity = '0'; m.style.transition = 'opacity 0.2s'; setTimeout(function () { m.remove(); }, 220); }
      var s = document.getElementById('hprenda-email-modal-style');
      if (s) setTimeout(function () { s.remove(); }, 300);
    }

    document.getElementById('em-close-btn').addEventListener('click', _closeEmailModal);
    document.getElementById('em-close-btn2').addEventListener('click', _closeEmailModal);

    /* Copiar para clipboard */
    document.getElementById('em-copy-btn').addEventListener('click', function () {
      var fullText = 'Assunto: ' + subject + '\n\n' + body;
      if (navigator.clipboard) {
        navigator.clipboard.writeText(fullText).then(function () {
          _toast('Conteúdo copiado para a área de transferência.', 'ok');
          document.getElementById('em-copy-btn').textContent = '✅ Copiado!';
        }).catch(function (err) {
          console.error(LOG, 'Erro ao copiar:', err);
          _fallbackCopy(fullText);
        });
      } else {
        _fallbackCopy(fullText);
      }
    });

    /* Abrir cliente de email */
    document.getElementById('em-mailto-btn').addEventListener('click', function () {
      var destInput = document.getElementById('email-dest');
      var dest = destInput ? destInput.value.trim() : '';
      var shortBody = body.length > 1800 ? body.slice(0, 1800) + '\n\n[...]' : body;
      var mailto = 'mailto:' + encodeURIComponent(dest) +
                   '?subject=' + encodeURIComponent(subject) +
                   '&body=' + encodeURIComponent(shortBody);
      global.open(mailto, '_blank');
      _toast('A abrir cliente de email…', 'info');
    });
  };

  /* Escape HTML para inserção segura no DOM */
  function _escHtml(str) {
    return String(str)
      .replace(/&/g,  '&amp;')
      .replace(/</g,  '&lt;')
      .replace(/>/g,  '&gt;')
      .replace(/"/g,  '&quot;');
  }

  /* Fallback de cópia via textarea para browsers antigos */
  function _fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.cssText = 'position:fixed;top:-9999px;left:-9999px;';
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand('copy');
      _toast('Conteúdo copiado para a área de transferência.', 'ok');
    } catch (e) {
      _toast('Não foi possível copiar automaticamente. Seleccione o texto manualmente.', 'warn');
    }
    document.body.removeChild(ta);
  }

  console.log(LOG, 'hprenda-mail.js carregado (defer).');

}(window));
