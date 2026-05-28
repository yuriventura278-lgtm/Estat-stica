/**
 * hprenda-analytics.js — Motor de análise para Hospital do Prenda — Consulta Externa
 *
 * Expõe (em window):
 *   KPI_THRESHOLDS
 *   getDateRange(mode, referenceDate)
 *   getBaselineDateRange(mode, referenceDate)
 *   buildPeriodStats(dates)
 *   buildComparativeStats(currentStats, baselineStats)
 *   scoreKPIs(stats)
 *   generateNarrative(currentStats, comparativeStats, periodLabel, baselineLabel)
 *   getAllFlatRecords(type)
 *   getAllPeriodSummaries()
 *   getAvailablePeriods()
 */

(function (global) {
  'use strict';

  var LOG = '[hprenda-analytics]';

  /* ─────────────────────────────────────────────────────────────
     Dados de referência
  ───────────────────────────────────────────────────────────── */
  var ESPECIALIDADES = [
    'Medicina Interna','Ortopedia','Cirurgia Geral','Proctologia','Cardiologia',
    'Reumatologia','Estomatologia','Oftalmologia','Optometria','Anestesiologia',
    'Maxilo Facial','Neurocirurgia','Gastroenterologia','Neurologia',
    'Otorrinolaringologia'
  ];

  var PROCEDIMENTOS = [
    'Curativos feitos','Pontos retirados','Gessos retirados','Gessos aplicados',
    'Algálias retiradas','Talas colocadas','Talas retiradas','Injeções',
    'Infiltrações','Exodontia simples','Exodontia complicada'
  ];

  var MATERIAIS = [
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

  var PT_MONTHS = [
    'Janeiro','Fevereiro','Março','Abril','Maio','Junho',
    'Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'
  ];

  /* ─────────────────────────────────────────────────────────────
     1.  KPI_THRESHOLDS
  ───────────────────────────────────────────────────────────── */
  var KPI_THRESHOLDS = {
    realizacao:    { green: 85, amber: 70 },
    cancelamento:  { amber: 10, red: 20 },
    stockCobertura:{ green: 40, amber: 20 },
    procPorDia:    { green: 15, amber: 8  }
  };
  global.KPI_THRESHOLDS = KPI_THRESHOLDS;

  /* ─────────────────────────────────────────────────────────────
     Helpers internos
  ───────────────────────────────────────────────────────────── */

  /** Formata YYYY-MM-DD → "15 de Janeiro de 2025" */
  function _ptDate(dateStr) {
    var parts = dateStr.split('-');
    var y = parseInt(parts[0], 10);
    var m = parseInt(parts[1], 10) - 1;
    var d = parseInt(parts[2], 10);
    return d + ' de ' + PT_MONTHS[m] + ' de ' + y;
  }

  /** Formata número → "87,4%" (localização PT) */
  function _ptPct(n) {
    var rounded = Math.round(n * 10) / 10;
    return rounded.toFixed(1).replace('.', ',') + '%';
  }

  /** Devolve "+12" ou "-12" */
  function _sign(n) {
    var rounded = Math.round(n);
    return (rounded >= 0 ? '+' : '') + rounded;
  }

  /** Lê do localStorage com tratamento de erros. Devolve null em caso de falha. */
  function _lsGet(key) {
    try {
      var raw = localStorage.getItem(key);
      if (raw === null || raw === undefined) return null;
      return JSON.parse(raw);
    } catch (e) {
      console.warn(LOG, 'Erro ao ler localStorage key="' + key + '":', e);
      return null;
    }
  }

  /** Obtém a lista de datas gravadas em prenda_saved_dates (array de strings). */
  function _getSavedDates() {
    var dates = _lsGet('prenda_saved_dates');
    if (!Array.isArray(dates)) return [];
    return dates;
  }

  /** Converte YYYY-MM-DD → Date UTC */
  function _parseDate(str) {
    var p = str.split('-');
    return new Date(Date.UTC(parseInt(p[0],10), parseInt(p[1],10)-1, parseInt(p[2],10)));
  }

  /** Converte Date UTC → YYYY-MM-DD */
  function _fmtDate(d) {
    var y = d.getUTCFullYear();
    var m = String(d.getUTCMonth() + 1).padStart(2, '0');
    var day = String(d.getUTCDate()).padStart(2, '0');
    return y + '-' + m + '-' + day;
  }

  /** Adiciona `n` dias a uma data UTC. */
  function _addDays(d, n) {
    var r = new Date(d.getTime());
    r.setUTCDate(r.getUTCDate() + n);
    return r;
  }

  /** Obtém todas as datas no intervalo [start, end] inclusive, como array de YYYY-MM-DD. */
  function _datesInRange(start, end) {
    var result = [];
    var cur = new Date(start.getTime());
    while (cur <= end) {
      result.push(_fmtDate(cur));
      cur = _addDays(cur, 1);
    }
    return result;
  }

  /**
   * Filtra um array de datas candidatas para incluir apenas as que existem
   * no conjunto de datas gravadas.
   */
  function _filterSaved(candidates) {
    var saved = _getSavedDates();
    var set = {};
    saved.forEach(function(d){ set[d] = true; });
    return candidates.filter(function(d){ return set[d]; });
  }

  /* ─────────────────────────────────────────────────────────────
     2.  getDateRange
  ───────────────────────────────────────────────────────────── */
  function getDateRange(mode, referenceDate) {
    var ref = referenceDate || _fmtDate(new Date());
    var d = _parseDate(ref);
    var y = d.getUTCFullYear();
    var m = d.getUTCMonth(); // 0-based
    var candidates = [];

    switch (mode) {
      case 'dia':
        candidates = [ref];
        break;

      case 'semana': {
        // Monday of week containing ref (ISO: Mon=1 … Sun=7)
        var dow = d.getUTCDay(); // 0=Sun,1=Mon,...,6=Sat
        var diffToMon = (dow === 0) ? -6 : 1 - dow;
        var mon = _addDays(d, diffToMon);
        var sun = _addDays(mon, 6);
        candidates = _datesInRange(mon, sun);
        break;
      }

      case 'mes': {
        var start = new Date(Date.UTC(y, m, 1));
        var end   = new Date(Date.UTC(y, m + 1, 0));
        candidates = _datesInRange(start, end);
        break;
      }

      case 'trimestre': {
        var q = Math.floor(m / 3); // 0-based quarter (0..3)
        var qStart = new Date(Date.UTC(y, q * 3, 1));
        var qEnd   = new Date(Date.UTC(y, q * 3 + 3, 0));
        candidates = _datesInRange(qStart, qEnd);
        break;
      }

      case 'semestre': {
        var h = m < 6 ? 0 : 1;
        var hStart = new Date(Date.UTC(y, h * 6, 1));
        var hEnd   = new Date(Date.UTC(y, h * 6 + 6, 0));
        candidates = _datesInRange(hStart, hEnd);
        break;
      }

      case 'ano': {
        var yStart = new Date(Date.UTC(y, 0, 1));
        var yEnd   = new Date(Date.UTC(y, 12, 0));
        candidates = _datesInRange(yStart, yEnd);
        break;
      }

      default:
        console.warn(LOG, 'getDateRange: modo desconhecido "' + mode + '"');
        return [];
    }

    return _filterSaved(candidates);
  }
  global.getDateRange = getDateRange;

  /* ─────────────────────────────────────────────────────────────
     3.  getBaselineDateRange
  ───────────────────────────────────────────────────────────── */
  function getBaselineDateRange(mode, referenceDate) {
    var ref = referenceDate || _fmtDate(new Date());
    var d = _parseDate(ref);
    var y = d.getUTCFullYear();
    var m = d.getUTCMonth();
    var candidates = [];

    switch (mode) {
      case 'dia': {
        // Same weekday previous week
        var prev = _addDays(d, -7);
        candidates = [_fmtDate(prev)];
        break;
      }

      case 'semana': {
        // Previous calendar week (Mon-Sun)
        var dow = d.getUTCDay();
        var diffToMon = (dow === 0) ? -6 : 1 - dow;
        var thisMon = _addDays(d, diffToMon);
        var prevMon = _addDays(thisMon, -7);
        var prevSun = _addDays(prevMon, 6);
        candidates = _datesInRange(prevMon, prevSun);
        break;
      }

      case 'mes': {
        // Same month previous year
        var bStart = new Date(Date.UTC(y - 1, m, 1));
        var bEnd   = new Date(Date.UTC(y - 1, m + 1, 0));
        candidates = _datesInRange(bStart, bEnd);
        break;
      }

      case 'trimestre': {
        var q = Math.floor(m / 3);
        var bqStart = new Date(Date.UTC(y - 1, q * 3, 1));
        var bqEnd   = new Date(Date.UTC(y - 1, q * 3 + 3, 0));
        candidates = _datesInRange(bqStart, bqEnd);
        break;
      }

      case 'semestre': {
        var h = m < 6 ? 0 : 1;
        var bhStart = new Date(Date.UTC(y - 1, h * 6, 1));
        var bhEnd   = new Date(Date.UTC(y - 1, h * 6 + 6, 0));
        candidates = _datesInRange(bhStart, bhEnd);
        break;
      }

      case 'ano': {
        var byStart = new Date(Date.UTC(y - 1, 0, 1));
        var byEnd   = new Date(Date.UTC(y - 1, 12, 0));
        candidates = _datesInRange(byStart, byEnd);
        break;
      }

      default:
        console.warn(LOG, 'getBaselineDateRange: modo desconhecido "' + mode + '"');
        return [];
    }

    return _filterSaved(candidates);
  }
  global.getBaselineDateRange = getBaselineDateRange;

  /* ─────────────────────────────────────────────────────────────
     4.  buildPeriodStats
  ───────────────────────────────────────────────────────────── */
  function buildPeriodStats(dates) {
    var stats = {
      numDays: dates ? dates.length : 0,
      totalAgendadas:    0,
      totalRealizadas:   0,
      totalCanceladas:   0,
      totalMenor15:      0,
      totalMaior15:      0,
      totalProc:         0,
      totalStockInicial: 0,
      totalConsumido:    0,
      taxaRealizacao:    0,
      taxaCancelamento:  0,
      stockCobertura:    0,
      procPorDia:        0,
      byEspecialidade:   {},
      byProcedimento:    {},
      byMaterial:        {},
      topEspecialidade:  '',
      topProcedimento:   '',
      alertaMateriais:   []
    };

    if (!dates || dates.length === 0) return stats;

    // Init accumulators
    ESPECIALIDADES.forEach(function(esp) {
      stats.byEspecialidade[esp] = { ag:0, re:0, ca:0, m15:0, M15:0, taxaReal:0, taxaCanc:0 };
    });
    PROCEDIMENTOS.forEach(function(proc) {
      stats.byProcedimento[proc] = { manha:0, tarde:0, total:0 };
    });
    MATERIAIS.forEach(function(mat) {
      stats.byMaterial[mat.nome] = { stock:0, usado:0, saldo:0, pctConsumo:0 };
    });

    dates.forEach(function(date) {
      // Consultas
      var consultas = _lsGet('prenda_consultas_' + date);
      if (consultas && typeof consultas === 'object') {
        ESPECIALIDADES.forEach(function(esp) {
          var row = consultas[esp];
          if (!row) return;
          var ag  = Number(row.ag  || 0);
          var re  = Number(row.re  || 0);
          var ca  = Number(row.ca  || 0);
          var m15 = Number(row.m15 || 0);
          var M15 = Number(row.M15 || 0);
          stats.totalAgendadas  += ag;
          stats.totalRealizadas += re;
          stats.totalCanceladas += ca;
          stats.totalMenor15    += m15;
          stats.totalMaior15    += M15;
          stats.byEspecialidade[esp].ag  += ag;
          stats.byEspecialidade[esp].re  += re;
          stats.byEspecialidade[esp].ca  += ca;
          stats.byEspecialidade[esp].m15 += m15;
          stats.byEspecialidade[esp].M15 += M15;
        });
      }

      // Procedimentos
      var proc = _lsGet('prenda_proc_' + date);
      if (proc && typeof proc === 'object') {
        PROCEDIMENTOS.forEach(function(p) {
          var row = proc[p];
          if (!row) return;
          var manha = Number(row.manha || 0);
          var tarde = Number(row.tarde || 0);
          stats.byProcedimento[p].manha += manha;
          stats.byProcedimento[p].tarde += tarde;
          stats.byProcedimento[p].total += manha + tarde;
          stats.totalProc += manha + tarde;
        });
      }

      // Materiais
      var mat = _lsGet('prenda_mat_' + date);
      if (mat && typeof mat === 'object') {
        MATERIAIS.forEach(function(m) {
          var row = mat[m.nome];
          if (!row) return;
          var stock = Number(row.stock || 0);
          var usado = Number(row.usado || 0);
          stats.byMaterial[m.nome].stock += stock;
          stats.byMaterial[m.nome].usado += usado;
          stats.totalStockInicial += stock;
          stats.totalConsumido    += usado;
        });
      }
    });

    // Computed percentages for especialidades
    ESPECIALIDADES.forEach(function(esp) {
      var e = stats.byEspecialidade[esp];
      e.taxaReal = e.ag > 0 ? (e.re / e.ag) * 100 : 0;
      e.taxaCanc = e.ag > 0 ? (e.ca / e.ag) * 100 : 0;
    });

    // Computed for materiais
    MATERIAIS.forEach(function(m) {
      var b = stats.byMaterial[m.nome];
      b.saldo      = b.stock - b.usado;
      b.pctConsumo = b.stock > 0 ? (b.usado / b.stock) * 100 : 0;
    });

    // Overall KPI rates
    stats.taxaRealizacao   = stats.totalAgendadas  > 0 ? (stats.totalRealizadas / stats.totalAgendadas)  * 100 : 0;
    stats.taxaCancelamento = stats.totalAgendadas  > 0 ? (stats.totalCanceladas / stats.totalAgendadas)  * 100 : 0;
    stats.stockCobertura   = stats.totalStockInicial > 0 ? (1 - stats.totalConsumido / stats.totalStockInicial) * 100 : 0;
    stats.procPorDia       = dates.length > 0 ? stats.totalProc / dates.length : 0;

    // Top especialidade (by realizadas)
    var topEsp = '';
    var topEspVal = -1;
    ESPECIALIDADES.forEach(function(esp) {
      if (stats.byEspecialidade[esp].re > topEspVal) {
        topEspVal = stats.byEspecialidade[esp].re;
        topEsp    = esp;
      }
    });
    stats.topEspecialidade = topEspVal > 0 ? topEsp : '';

    // Top procedimento (by total)
    var topProc = '';
    var topProcVal = -1;
    PROCEDIMENTOS.forEach(function(p) {
      if (stats.byProcedimento[p].total > topProcVal) {
        topProcVal = stats.byProcedimento[p].total;
        topProc    = p;
      }
    });
    stats.topProcedimento = topProcVal > 0 ? topProc : '';

    // Alertas materiais: stockCobertura < 20%
    MATERIAIS.forEach(function(m) {
      var b = stats.byMaterial[m.nome];
      var cobertura = b.stock > 0 ? (1 - b.usado / b.stock) * 100 : 0;
      if (b.stock > 0 && cobertura < KPI_THRESHOLDS.stockCobertura.amber) {
        stats.alertaMateriais.push(m.nome);
      }
    });

    return stats;
  }
  global.buildPeriodStats = buildPeriodStats;

  /* ─────────────────────────────────────────────────────────────
     5.  buildComparativeStats
  ───────────────────────────────────────────────────────────── */
  function buildComparativeStats(currentStats, baselineStats) {
    var KPIs = [
      'taxaRealizacao','taxaCancelamento','totalAgendadas','totalRealizadas',
      'totalCanceladas','totalMenor15','totalMaior15','totalProc',
      'totalStockInicial','totalConsumido','stockCobertura','procPorDia'
    ];

    // Friendly mapping for output keys
    var keyMap = {
      taxaRealizacao:    'realizacao',
      taxaCancelamento:  'cancelamento',
      totalAgendadas:    'totalAgendadas',
      totalRealizadas:   'totalConsultas',
      totalCanceladas:   'totalCanceladas',
      totalMenor15:      'totalMenor15',
      totalMaior15:      'totalMaior15',
      totalProc:         'totalProc',
      totalStockInicial: 'totalStockInicial',
      totalConsumido:    'totalConsumido',
      stockCobertura:    'stockCobertura',
      procPorDia:        'procPorDia'
    };

    var result = {};

    KPIs.forEach(function(kpi) {
      var cur  = currentStats  ? (currentStats[kpi]  || 0) : 0;
      var base = baselineStats ? (baselineStats[kpi] || 0) : 0;
      var delta = cur - base;
      var pct   = base !== 0 ? (delta / Math.abs(base)) * 100 : (cur !== 0 ? 100 : 0);
      var direction = 'stable';
      if (Math.abs(pct) >= 2) {
        direction = delta > 0 ? 'up' : 'down';
      }
      result[keyMap[kpi]] = {
        current:   cur,
        baseline:  base,
        delta:     delta,
        pct:       pct,
        direction: direction
      };
    });

    return result;
  }
  global.buildComparativeStats = buildComparativeStats;

  /* ─────────────────────────────────────────────────────────────
     6.  scoreKPIs
  ───────────────────────────────────────────────────────────── */
  function scoreKPIs(stats) {
    var scores = {};

    // Realização: ≥85 green, 70-84 amber, <70 red
    var r = stats.taxaRealizacao;
    scores.realizacao = r >= KPI_THRESHOLDS.realizacao.green ? 'green'
                      : r >= KPI_THRESHOLDS.realizacao.amber ? 'amber'
                      : 'red';

    // Cancelamento: ≤10 green, 11-20 amber, >20 red
    var c = stats.taxaCancelamento;
    scores.cancelamento = c <= KPI_THRESHOLDS.cancelamento.amber ? 'green'
                        : c <= KPI_THRESHOLDS.cancelamento.red   ? 'amber'
                        : 'red';

    // Stock cobertura: ≥40 green, 20-39 amber, <20 red
    var s = stats.stockCobertura;
    scores.stockCobertura = s >= KPI_THRESHOLDS.stockCobertura.green ? 'green'
                          : s >= KPI_THRESHOLDS.stockCobertura.amber ? 'amber'
                          : 'red';

    // Proc por dia: ≥15 green, 8-14 amber, <8 red
    var p = stats.procPorDia;
    scores.procPorDia = p >= KPI_THRESHOLDS.procPorDia.green ? 'green'
                      : p >= KPI_THRESHOLDS.procPorDia.amber ? 'amber'
                      : 'red';

    return scores;
  }
  global.scoreKPIs = scoreKPIs;

  /* ─────────────────────────────────────────────────────────────
     7.  generateNarrative
  ───────────────────────────────────────────────────────────── */
  function generateNarrative(currentStats, comparativeStats, periodLabel, baselineLabel) {
    if (!currentStats) return 'Sem dados disponíveis para o período seleccionado.';

    var parts = [];
    var scores = scoreKPIs(currentStats);

    // Period summary
    var daysText = currentStats.numDays === 1
      ? '1 dia com dados'
      : currentStats.numDays + ' dias com dados';
    parts.push(
      'Em ' + periodLabel + ' (' + daysText + '), realizaram-se ' +
      currentStats.totalRealizadas.toLocaleString('pt-PT') + ' consultas,' +
      ' correspondendo a uma taxa de realização de ' + _ptPct(currentStats.taxaRealizacao) +
      ' (Meta: ≥' + KPI_THRESHOLDS.realizacao.green + '% ' +
      (scores.realizacao === 'green' ? '✓' : scores.realizacao === 'amber' ? '~' : '✗') + ').'
    );

    // Top specialty
    if (currentStats.topEspecialidade) {
      var topRe = currentStats.byEspecialidade[currentStats.topEspecialidade]
        ? currentStats.byEspecialidade[currentStats.topEspecialidade].re
        : 0;
      parts.push(
        'A especialidade mais activa foi ' + currentStats.topEspecialidade +
        ' com ' + topRe.toLocaleString('pt-PT') + ' consultas.'
      );
    }

    // Cancellation rate
    var cancTag = scores.cancelamento === 'green'
      ? 'dentro do limite aceitável'
      : scores.cancelamento === 'amber'
      ? 'acima do ideal — atenção recomendada'
      : 'elevada — intervenção necessária';
    parts.push(
      'A taxa de cancelamento situou-se em ' + _ptPct(currentStats.taxaCancelamento) +
      ', ' + cancTag + '.'
    );

    // Procedure load
    if (currentStats.totalProc > 0) {
      var ppd = Math.round(currentStats.procPorDia * 10) / 10;
      parts.push(
        'Foram executados ' + currentStats.totalProc.toLocaleString('pt-PT') +
        ' procedimentos (' + ppd.toFixed(1).replace('.', ',') + '/dia).'
      );
    }

    // Comparative analysis
    if (comparativeStats && baselineLabel) {
      var compSentences = [];

      var consComp = comparativeStats.totalConsultas;
      if (consComp && consComp.baseline > 0 && Math.abs(consComp.pct) >= 2) {
        var dir = consComp.direction === 'up' ? 'subiram' : 'desceram';
        compSentences.push(
          'as consultas realizadas ' + dir + ' ' +
          _ptPct(Math.abs(consComp.pct)) +
          ' (' + _sign(consComp.delta) + ')'
        );
      }

      var cancComp = comparativeStats.cancelamento;
      if (cancComp && cancComp.baseline > 0 && Math.abs(cancComp.pct) >= 2) {
        var cancDeltaRounded = Math.round(Math.abs(cancComp.delta) * 10) / 10;
        var cancDir = cancComp.direction === 'down' ? 'melhorou' : 'piorou';
        compSentences.push(
          'o cancelamento ' + cancDir + ' ' +
          cancDeltaRounded.toFixed(1).replace('.', ',') + ' p.p.'
        );
      }

      if (compSentences.length > 0) {
        parts.push(
          'Comparativamente a ' + baselineLabel + ', ' +
          compSentences.join('. ') + '.'
        );
      }
    }

    // Material alerts
    if (currentStats.alertaMateriais && currentStats.alertaMateriais.length > 0) {
      currentStats.alertaMateriais.forEach(function(matNome) {
        var mb = currentStats.byMaterial[matNome];
        if (mb) {
          var cob = mb.stock > 0 ? Math.round((1 - mb.usado / mb.stock) * 100) : 0;
          parts.push(
            'O material ' + matNome + ' apresenta cobertura de stock crítica (' + cob + '%).'
          );
        }
      });
    }

    // Concluding sentence
    var overallScore;
    var scoreValues = [scores.realizacao, scores.cancelamento, scores.stockCobertura, scores.procPorDia];
    var reds   = scoreValues.filter(function(s){ return s === 'red';   }).length;
    var ambers = scoreValues.filter(function(s){ return s === 'amber'; }).length;
    var greens = scoreValues.filter(function(s){ return s === 'green'; }).length;

    if (greens >= 3 && reds === 0) {
      overallScore = 'FAVORÁVEL';
    } else if (reds >= 2) {
      overallScore = 'DESFAVORÁVEL';
    } else {
      overallScore = 'MODERADA';
    }

    parts.push('Situação geral: ' + overallScore + '.');

    return parts.join(' ');
  }
  global.generateNarrative = generateNarrative;

  /* ─────────────────────────────────────────────────────────────
     8.  getAllFlatRecords
  ───────────────────────────────────────────────────────────── */
  function getAllFlatRecords(type) {
    var saved = _getSavedDates();
    var records = [];

    saved.forEach(function(date) {
      if (type === 'consultas') {
        var consultas = _lsGet('prenda_consultas_' + date);
        if (!consultas) return;
        ESPECIALIDADES.forEach(function(esp) {
          var row = consultas[esp];
          if (!row) return;
          var ag  = Number(row.ag  || 0);
          var re  = Number(row.re  || 0);
          var ca  = Number(row.ca  || 0);
          var m15 = Number(row.m15 || 0);
          var M15 = Number(row.M15 || 0);
          if (ag + re + ca + m15 + M15 === 0) return;
          var taxaReal = ag > 0 ? (re / ag) * 100 : 0;
          var taxaCanc = ag > 0 ? (ca / ag) * 100 : 0;
          records.push({ date: date, especialidade: esp, ag: ag, re: re, ca: ca, m15: m15, M15: M15, taxaReal: taxaReal, taxaCanc: taxaCanc });
        });

      } else if (type === 'proc') {
        var proc = _lsGet('prenda_proc_' + date);
        if (!proc) return;
        PROCEDIMENTOS.forEach(function(p) {
          var row = proc[p];
          if (!row) return;
          var manha = Number(row.manha || 0);
          var tarde = Number(row.tarde || 0);
          var total = manha + tarde;
          if (total === 0) return;
          records.push({ date: date, procedimento: p, manha: manha, tarde: tarde, total: total });
        });

      } else if (type === 'mat') {
        var mat = _lsGet('prenda_mat_' + date);
        if (!mat) return;
        MATERIAIS.forEach(function(m) {
          var row = mat[m.nome];
          if (!row) return;
          var stock = Number(row.stock || 0);
          var usado = Number(row.usado || 0);
          if (stock + usado === 0) return;
          var saldo      = stock - usado;
          var pctConsumo = stock > 0 ? (usado / stock) * 100 : 0;
          records.push({ date: date, material: m.nome, unit: m.unit, stock: stock, usado: usado, saldo: saldo, pctConsumo: pctConsumo });
        });
      }
    });

    // Sort: date descending, then name ascending
    records.sort(function(a, b) {
      if (a.date > b.date) return -1;
      if (a.date < b.date) return  1;
      var nameA = a.especialidade || a.procedimento || a.material || '';
      var nameB = b.especialidade || b.procedimento || b.material || '';
      return nameA.localeCompare(nameB, 'pt');
    });

    return records;
  }
  global.getAllFlatRecords = getAllFlatRecords;

  /* ─────────────────────────────────────────────────────────────
     9.  getAllPeriodSummaries
  ───────────────────────────────────────────────────────────── */
  function getAllPeriodSummaries() {
    var saved = _getSavedDates();
    var summaries = [];

    saved.forEach(function(date) {
      var totalAgendadas  = 0;
      var totalRealizadas = 0;
      var totalCanceladas = 0;
      var totalMenor15    = 0;
      var totalMaior15    = 0;
      var totalProc       = 0;
      var totalStockInicial = 0;
      var totalConsumido  = 0;

      var consultas = _lsGet('prenda_consultas_' + date);
      if (consultas && typeof consultas === 'object') {
        ESPECIALIDADES.forEach(function(esp) {
          var row = consultas[esp];
          if (!row) return;
          totalAgendadas  += Number(row.ag  || 0);
          totalRealizadas += Number(row.re  || 0);
          totalCanceladas += Number(row.ca  || 0);
          totalMenor15    += Number(row.m15 || 0);
          totalMaior15    += Number(row.M15 || 0);
        });
      }

      var proc = _lsGet('prenda_proc_' + date);
      if (proc && typeof proc === 'object') {
        PROCEDIMENTOS.forEach(function(p) {
          var row = proc[p];
          if (!row) return;
          totalProc += Number(row.manha || 0) + Number(row.tarde || 0);
        });
      }

      var mat = _lsGet('prenda_mat_' + date);
      if (mat && typeof mat === 'object') {
        MATERIAIS.forEach(function(m) {
          var row = mat[m.nome];
          if (!row) return;
          totalStockInicial += Number(row.stock || 0);
          totalConsumido    += Number(row.usado  || 0);
        });
      }

      var taxaRealizacao   = totalAgendadas    > 0 ? (totalRealizadas / totalAgendadas)    * 100 : 0;
      var taxaCancelamento = totalAgendadas    > 0 ? (totalCanceladas / totalAgendadas)    * 100 : 0;
      var stockCobertura   = totalStockInicial > 0 ? (1 - totalConsumido / totalStockInicial) * 100 : 0;

      summaries.push({
        date:              date,
        totalAgendadas:    totalAgendadas,
        totalRealizadas:   totalRealizadas,
        totalCanceladas:   totalCanceladas,
        totalMenor15:      totalMenor15,
        totalMaior15:      totalMaior15,
        totalProc:         totalProc,
        totalStockInicial: totalStockInicial,
        totalConsumido:    totalConsumido,
        taxaRealizacao:    taxaRealizacao,
        taxaCancelamento:  taxaCancelamento,
        stockCobertura:    stockCobertura
      });
    });

    // Sort date descending
    summaries.sort(function(a, b) {
      if (a.date > b.date) return -1;
      if (a.date < b.date) return  1;
      return 0;
    });

    return summaries;
  }
  global.getAllPeriodSummaries = getAllPeriodSummaries;

  /* ─────────────────────────────────────────────────────────────
     10.  getAvailablePeriods
  ───────────────────────────────────────────────────────────── */
  function getAvailablePeriods() {
    var saved = _getSavedDates();

    var weeksSet   = {};
    var monthsSet  = {};
    var quartersSet= {};
    var semestersSet={};
    var yearsSet   = {};

    saved.forEach(function(date) {
      var d = _parseDate(date);
      var y = d.getUTCFullYear();
      var m = d.getUTCMonth(); // 0-based

      // ISO week number
      // ISO weeks: Jan 4th is always in week 1
      var jan4 = new Date(Date.UTC(y, 0, 4));
      var jan4Dow = jan4.getUTCDay() || 7; // Monday=1..Sunday=7
      var weekStart = new Date(jan4.getTime() - (jan4Dow - 1) * 86400000);
      var diffMs = d.getTime() - weekStart.getTime();
      var weekNum = Math.floor(diffMs / (7 * 86400000)) + 1;
      // Handle edge cases for week 0 or week 53+ that belong to adjacent year
      var isoYear = y;
      if (weekNum < 1) {
        isoYear = y - 1;
        var jan4Prev = new Date(Date.UTC(isoYear, 0, 4));
        var jan4PrevDow = jan4Prev.getUTCDay() || 7;
        var weekStartPrev = new Date(jan4Prev.getTime() - (jan4PrevDow - 1) * 86400000);
        weekNum = Math.floor((d.getTime() - weekStartPrev.getTime()) / (7 * 86400000)) + 1;
      } else {
        // Check if this is week 1 of next year
        var jan4Next = new Date(Date.UTC(y + 1, 0, 4));
        var jan4NextDow = jan4Next.getUTCDay() || 7;
        var weekStartNext = new Date(jan4Next.getTime() - (jan4NextDow - 1) * 86400000);
        if (d >= weekStartNext) {
          isoYear = y + 1;
          weekNum = 1;
        }
      }
      var weekLabel = isoYear + '-W' + String(weekNum).padStart(2, '0');
      weeksSet[weekLabel] = true;

      // Month
      monthsSet[y + '-' + String(m + 1).padStart(2, '0')] = true;

      // Quarter
      var q = Math.floor(m / 3) + 1;
      quartersSet[y + '-Q' + q] = true;

      // Semester
      var h = m < 6 ? 1 : 2;
      semestersSet[y + '-H' + h] = true;

      // Year
      yearsSet[String(y)] = true;
    });

    var sortedWeeks     = Object.keys(weeksSet).sort();
    var sortedMonths    = Object.keys(monthsSet).sort();
    var sortedQuarters  = Object.keys(quartersSet).sort();
    var sortedSemesters = Object.keys(semestersSet).sort();
    var sortedYears     = Object.keys(yearsSet).sort();

    var min = saved.length > 0 ? saved[0] : '';
    var max = saved.length > 0 ? saved[saved.length - 1] : '';
    // saved_dates is sorted ascending per spec
    // but just in case, compute min/max safely
    if (saved.length > 0) {
      var sortedDates = saved.slice().sort();
      min = sortedDates[0];
      max = sortedDates[sortedDates.length - 1];
    }

    return {
      totalDays:  saved.length,
      weeks:      sortedWeeks,
      months:     sortedMonths,
      quarters:   sortedQuarters,
      semesters:  sortedSemesters,
      years:      sortedYears,
      dateRange:  { min: min, max: max }
    };
  }
  global.getAvailablePeriods = getAvailablePeriods;

  /* ─────────────────────────────────────────────────────────────
     Expor helpers de formatação (úteis para templates externos)
  ───────────────────────────────────────────────────────────── */
  global._hprendaFmt = {
    ptDate: _ptDate,
    ptPct:  _ptPct,
    sign:   _sign
  };

  console.log(LOG, 'hprenda-analytics.js carregado. Funções disponíveis em window: getDateRange, getBaselineDateRange, buildPeriodStats, buildComparativeStats, scoreKPIs, generateNarrative, getAllFlatRecords, getAllPeriodSummaries, getAvailablePeriods.');

}(window));
