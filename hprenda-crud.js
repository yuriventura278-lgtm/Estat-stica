/**
 * hprenda-crud.js — CRUD helpers and extended data management
 * Hospital do Prenda — Consulta Externa
 *
 * Expõe (em window):
 *   importFromCSV(csvText, type)
 *   validateDayData(date)       → string[]
 *   calcWeekStats(weekDates)    → object
 *   calcMonthStats(monthDates)  → object
 *   exportToCSV(date)
 *   bulkExportCSV(dates)
 *   importDayFromJSON(jsonString)
 *   createBackup()
 *   restoreBackup(jsonString)
 */

(function (global) {
  'use strict';

  var LOG = '[hprenda-crud]';

  /* ─────────────────────────────────────────────────────────────
     Helpers internos — espelha o que o HTML já define,
     mas com protecção para quando o ficheiro carrega antes.
  ───────────────────────────────────────────────────────────── */

  function _safeGet(k) {
    try { return localStorage.getItem(k); } catch (e) { return null; }
  }
  function _safeSet(k, v) {
    try { localStorage.setItem(k, v); return true; } catch (e) {
      console.warn(LOG, 'localStorage cheio ao escrever chave:', k);
      return false;
    }
  }
  function _storageKey(type, date) {
    return 'prenda_' + type + '_' + date;
  }
  function _todayKey() {
    return new Date().toISOString().slice(0, 10);
  }
  function _formatDate(d) {
    if (!d) return '—';
    var parts = d.split('-');
    return parts[2] + '/' + parts[1] + '/' + parts[0];
  }

  /* Referências seguras às constantes do HTML */
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

  function _toast(msg, type) {
    if (typeof global.toast === 'function') {
      global.toast(msg, type || 'info');
    } else {
      console.info(LOG, '[toast]', msg);
    }
  }

  /* ─────────────────────────────────────────────────────────────
     Trigger browser download for a text blob
  ───────────────────────────────────────────────────────────── */
  function _triggerDownload(content, filename, mimeType) {
    var blob = new Blob([content], { type: mimeType || 'text/plain;charset=utf-8' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    setTimeout(function () {
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 200);
  }

  /* ─────────────────────────────────────────────────────────────
     Aggregate helpers (mirror do HTML para uso interno)
  ───────────────────────────────────────────────────────────── */
  function _aggConsultas(dates) {
    var esp = _ESPECIALIDADES();
    var agg = {};
    esp.forEach(function (e) { agg[e] = {ag:0,re:0,ca:0,m15:0,M15:0}; });
    dates.forEach(function (d) {
      var raw = _safeGet(_storageKey('consultas', d));
      var c = raw ? JSON.parse(raw) : {};
      esp.forEach(function (e) {
        if (c[e]) {
          ['ag','re','ca','m15','M15'].forEach(function (f) {
            agg[e][f] += (c[e][f] || 0);
          });
        }
      });
    });
    return agg;
  }

  function _aggProc(dates) {
    var proc = _PROCEDIMENTOS();
    var agg = {};
    proc.forEach(function (p) { agg[p] = {manha:0,tarde:0}; });
    dates.forEach(function (d) {
      var raw = _safeGet(_storageKey('proc', d));
      var p = raw ? JSON.parse(raw) : {};
      proc.forEach(function (pr) {
        if (p[pr]) {
          ['manha','tarde'].forEach(function (f) { agg[pr][f] += (p[pr][f] || 0); });
        }
      });
    });
    return agg;
  }

  function _aggMat(dates) {
    var mats = _MATERIAIS();
    var agg = {};
    mats.forEach(function (m) { agg[m.nome] = {stock:0,usado:0}; });
    dates.forEach(function (d) {
      var raw = _safeGet(_storageKey('mat', d));
      var m = raw ? JSON.parse(raw) : {};
      mats.forEach(function (mat) {
        if (m[mat.nome]) {
          ['stock','usado'].forEach(function (f) { agg[mat.nome][f] += (m[mat.nome][f] || 0); });
        }
      });
    });
    return agg;
  }

  /* ═══════════════════════════════════════════════════════════════
     1.  importFromCSV(csvText, type)
  ═══════════════════════════════════════════════════════════════ */
  /**
   * Importa dados de um CSV e preenche o dia actual.
   * @param {string} csvText  — conteúdo CSV (separado por vírgula ou ponto-e-vírgula)
   * @param {string} type     — 'consultas' | 'proc' | 'mat'
   */
  global.importFromCSV = function (csvText, type) {
    console.log(LOG, 'importFromCSV chamado, tipo:', type);
    if (!csvText || typeof csvText !== 'string') {
      _toast('CSV inválido ou vazio.', 'err');
      return;
    }
    var sep = csvText.indexOf(';') > csvText.indexOf(',') ? ';' : ',';
    var lines = csvText.trim().split(/\r?\n/).filter(function (l) { return l.trim(); });
    if (lines.length < 2) {
      _toast('CSV sem dados (necessário cabeçalho + pelo menos 1 linha).', 'err');
      return;
    }

    var headers = lines[0].split(sep).map(function (h) { return h.trim().replace(/^"|"$/g,''); });
    var today = _todayKey();
    var result = {};
    var imported = 0;
    var errors = 0;

    try {
      if (type === 'consultas') {
        /* Colunas esperadas: Especialidade, Agendadas, Realizadas, Canceladas, <15Anos, >15Anos */
        var esp = _ESPECIALIDADES();
        lines.slice(1).forEach(function (line) {
          var cols = line.split(sep).map(function (c) { return c.trim().replace(/^"|"$/g,''); });
          var nome = cols[0];
          if (!nome) return;
          var matched = esp.find(function (e) { return e.toLowerCase() === nome.toLowerCase(); }) || nome;
          result[matched] = {
            ag:   parseInt(cols[1],10) || 0,
            re:   parseInt(cols[2],10) || 0,
            ca:   parseInt(cols[3],10) || 0,
            m15:  parseInt(cols[4],10) || 0,
            M15:  parseInt(cols[5],10) || 0
          };
          imported++;
        });
        _safeSet(_storageKey('consultas', today), JSON.stringify(result));

      } else if (type === 'proc') {
        /* Colunas esperadas: Procedimento, Manhã, Tarde */
        lines.slice(1).forEach(function (line) {
          var cols = line.split(sep).map(function (c) { return c.trim().replace(/^"|"$/g,''); });
          var nome = cols[0];
          if (!nome) return;
          result[nome] = {
            manha: parseInt(cols[1],10) || 0,
            tarde: parseInt(cols[2],10) || 0
          };
          imported++;
        });
        _safeSet(_storageKey('proc', today), JSON.stringify(result));

      } else if (type === 'mat') {
        /* Colunas esperadas: Material, Unidade, Stock, Usado */
        lines.slice(1).forEach(function (line) {
          var cols = line.split(sep).map(function (c) { return c.trim().replace(/^"|"$/g,''); });
          var nome = cols[0];
          if (!nome) return;
          result[nome] = {
            stock: parseInt(cols[2],10) || 0,
            usado: parseInt(cols[3],10) || 0
          };
          imported++;
        });
        _safeSet(_storageKey('mat', today), JSON.stringify(result));

      } else {
        _toast('Tipo desconhecido: ' + type + '. Use consultas, proc ou mat.', 'err');
        return;
      }
    } catch (e) {
      console.error(LOG, 'Erro ao analisar CSV:', e);
      _toast('Erro ao analisar o CSV: ' + e.message, 'err');
      return;
    }

    _toast(imported + ' linhas importadas com sucesso para "' + type + '".', 'ok');
    console.log(LOG, 'CSV importado:', imported, 'linhas,', errors, 'erros. Tipo:', type);

    /* Recarregar a tabela se o loadDay estiver disponível */
    if (typeof global.loadDay === 'function') {
      global.loadDay(today);
    }
  };

  /* ═══════════════════════════════════════════════════════════════
     2.  validateDayData(date) → string[]
  ═══════════════════════════════════════════════════════════════ */
  /**
   * Valida a qualidade dos dados de um determinado dia.
   * @param {string} date  — formato YYYY-MM-DD
   * @returns {string[]}   — lista de avisos (vazia se tudo OK)
   */
  global.validateDayData = function (date) {
    var warnings = [];
    var esp = _ESPECIALIDADES();
    var mats = _MATERIAIS();

    var cRaw = _safeGet(_storageKey('consultas', date));
    var pRaw = _safeGet(_storageKey('proc', date));
    var mRaw = _safeGet(_storageKey('mat', date));

    var cData = cRaw ? JSON.parse(cRaw) : {};
    var pData = pRaw ? JSON.parse(pRaw) : {};
    var mData = mRaw ? JSON.parse(mRaw) : {};

    /* Verificar se há algum dado */
    var totalRe = 0, totalAg = 0;
    esp.forEach(function (e) {
      var d = cData[e] || {ag:0,re:0,ca:0,m15:0,M15:0};
      totalAg += d.ag;
      totalRe += d.re;
    });

    if (totalAg === 0 && totalRe === 0) {
      warnings.push('Nenhuma consulta registada para ' + _formatDate(date) + '.');
    }

    /* Especialidades sem nenhuma consulta realizada */
    esp.forEach(function (e) {
      var d = cData[e] || {ag:0,re:0,ca:0};
      if (d.ag > 0 && d.re === 0) {
        warnings.push('Especialidade ' + e + ': ' + d.ag + ' consulta(s) agendada(s) mas nenhuma realizada.');
      }
      if (d.re === 0 && d.ag === 0) {
        warnings.push('Nenhuma consulta realizada em ' + e + '.');
      }
    });

    /* Taxa de cancelamento elevada (> 20%) por especialidade */
    esp.forEach(function (e) {
      var d = cData[e] || {ag:0,re:0,ca:0};
      if (d.ag > 0) {
        var pctCanc = d.ca / d.ag;
        if (pctCanc > 0.20) {
          warnings.push('Taxa de cancelamento elevada em ' + e + ': ' + (pctCanc*100).toFixed(0) + '% (meta ≤ 20%).');
        }
      }
    });

    /* Realizadas > Agendadas (possível erro de introdução) */
    esp.forEach(function (e) {
      var d = cData[e] || {ag:0,re:0};
      if (d.re > 0 && d.ag > 0 && d.re > d.ag) {
        warnings.push('Erro possível em ' + e + ': realizadas (' + d.re + ') > agendadas (' + d.ag + ').');
      }
    });

    /* Materiais com stock abaixo de 10 unidades */
    mats.forEach(function (mat) {
      var d = mData[mat.nome] || {stock:0,usado:0};
      var saldo = d.stock - d.usado;
      if (d.stock > 0 && saldo < 10) {
        warnings.push('Stock de ' + mat.nome + ' abaixo de 10 ' + mat.unit + 's (saldo: ' + saldo + ').');
      }
      if (d.usado > d.stock && d.stock > 0) {
        warnings.push('Consumo de ' + mat.nome + ' excede o stock registado (' + d.usado + ' > ' + d.stock + ').');
      }
    });

    /* Procedimentos sem nenhum registo quando há consultas */
    if (totalRe > 0) {
      var totalProc = 0;
      _PROCEDIMENTOS().forEach(function (p) {
        var d = pData[p] || {manha:0,tarde:0};
        totalProc += d.manha + d.tarde;
      });
      if (totalProc === 0) {
        warnings.push('Há consultas registadas mas nenhum procedimento foi introduzido.');
      }
    }

    console.log(LOG, 'validateDayData(' + date + '):', warnings.length, 'aviso(s).');
    return warnings;
  };

  /* ═══════════════════════════════════════════════════════════════
     3.  calcWeekStats(weekDates) / calcMonthStats(monthDates)
  ═══════════════════════════════════════════════════════════════ */
  function _calcPeriodStats(dates) {
    if (!dates || dates.length === 0) {
      return { totalConsultas:0, totalProc:0, avgPerDay:0, topEsp:null, topProc:null,
               totalAgendadas:0, totalCanceladas:0, pctRealizacao:'—', pctCancelamento:'—', numDays:0 };
    }
    var cAgg = _aggConsultas(dates);
    var pAgg = _aggProc(dates);

    var totalAg = 0, totalRe = 0, totalCa = 0;
    Object.values(cAgg).forEach(function (v) { totalAg += v.ag; totalRe += v.re; totalCa += v.ca; });

    var totalProc = 0;
    Object.values(pAgg).forEach(function (v) { totalProc += v.manha + v.tarde; });

    /* Top especialidade (por realizadas) */
    var topEsp = null;
    var maxEsp = -1;
    Object.keys(cAgg).forEach(function (e) {
      if (cAgg[e].re > maxEsp) { maxEsp = cAgg[e].re; topEsp = e; }
    });
    if (maxEsp === 0) topEsp = null;

    /* Top procedimento */
    var topProc = null;
    var maxProc = -1;
    Object.keys(pAgg).forEach(function (p) {
      var tot = pAgg[p].manha + pAgg[p].tarde;
      if (tot > maxProc) { maxProc = tot; topProc = p; }
    });
    if (maxProc === 0) topProc = null;

    return {
      totalConsultas:    totalRe,
      totalAgendadas:    totalAg,
      totalCanceladas:   totalCa,
      totalProc:         totalProc,
      avgPerDay:         dates.length > 0 ? Math.round(totalRe / dates.length * 10) / 10 : 0,
      topEsp:            topEsp,
      topProc:           topProc,
      pctRealizacao:     totalAg > 0 ? (totalRe / totalAg * 100).toFixed(1) + '%' : '—',
      pctCancelamento:   totalAg > 0 ? (totalCa / totalAg * 100).toFixed(1) + '%' : '—',
      numDays:           dates.length
    };
  }

  /**
   * Estatísticas para uma semana (array de datas YYYY-MM-DD).
   */
  global.calcWeekStats = function (weekDates) {
    console.log(LOG, 'calcWeekStats — datas:', weekDates ? weekDates.length : 0);
    return _calcPeriodStats(weekDates || []);
  };

  /**
   * Estatísticas para um mês (array de datas YYYY-MM-DD).
   */
  global.calcMonthStats = function (monthDates) {
    console.log(LOG, 'calcMonthStats — datas:', monthDates ? monthDates.length : 0);
    return _calcPeriodStats(monthDates || []);
  };

  /* ═══════════════════════════════════════════════════════════════
     4.  exportToCSV(date) — download CSV para uma data
  ═══════════════════════════════════════════════════════════════ */
  /**
   * Gera e descarrega um CSV com todos os dados de um determinado dia.
   * @param {string} date  — formato YYYY-MM-DD
   */
  global.exportToCSV = function (date) {
    date = date || _todayKey();
    console.log(LOG, 'exportToCSV:', date);

    var esp = _ESPECIALIDADES();
    var proc = _PROCEDIMENTOS();
    var mats = _MATERIAIS();

    var cRaw = _safeGet(_storageKey('consultas', date));
    var pRaw = _safeGet(_storageKey('proc', date));
    var mRaw = _safeGet(_storageKey('mat', date));

    var cData = cRaw ? JSON.parse(cRaw) : {};
    var pData = pRaw ? JSON.parse(pRaw) : {};
    var mData = mRaw ? JSON.parse(mRaw) : {};

    var lines = [];

    /* Bloco: consultas */
    lines.push('=== CONSULTAS — ' + _formatDate(date) + ' ===');
    lines.push('Especialidade;Agendadas;Realizadas;Canceladas;<15Anos;>15Anos;Total');
    esp.forEach(function (e) {
      var d = cData[e] || {ag:0,re:0,ca:0,m15:0,M15:0};
      lines.push([e, d.ag, d.re, d.ca, d.m15, d.M15, (d.m15+d.M15)].join(';'));
    });
    lines.push('');

    /* Bloco: procedimentos */
    lines.push('=== PROCEDIMENTOS — ' + _formatDate(date) + ' ===');
    lines.push('Procedimento;Manhã;Tarde;Total');
    proc.forEach(function (p) {
      var d = pData[p] || {manha:0,tarde:0};
      lines.push([p, d.manha, d.tarde, (d.manha+d.tarde)].join(';'));
    });
    lines.push('');

    /* Bloco: material */
    lines.push('=== MATERIAL — ' + _formatDate(date) + ' ===');
    lines.push('Material;Unidade;Stock;Usado;Saldo');
    mats.forEach(function (mat) {
      var d = mData[mat.nome] || {stock:0,usado:0};
      lines.push([mat.nome, mat.unit, d.stock, d.usado, Math.max(0, d.stock-d.usado)].join(';'));
    });

    var csvContent = '﻿' + lines.join('\n'); /* BOM para Excel */
    var filename = 'Prenda_CE_' + date + '.csv';
    _triggerDownload(csvContent, filename, 'text/csv;charset=utf-8');
    _toast('CSV exportado: ' + filename, 'ok');
    console.log(LOG, 'CSV exportado:', filename);
  };

  /* ═══════════════════════════════════════════════════════════════
     5.  bulkExportCSV(dates) — CSV multi-dia com coluna de data
  ═══════════════════════════════════════════════════════════════ */
  /**
   * Exporta múltiplos dias num único CSV, com coluna de data em cada linha.
   * @param {string[]} dates — array de YYYY-MM-DD
   */
  global.bulkExportCSV = function (dates) {
    if (!dates || dates.length === 0) {
      _toast('Nenhuma data fornecida para exportação em lote.', 'warn');
      return;
    }
    console.log(LOG, 'bulkExportCSV — datas:', dates.length);

    var esp = _ESPECIALIDADES();
    var proc = _PROCEDIMENTOS();
    var mats = _MATERIAIS();
    var lines = [];

    /* === CONSULTAS === */
    lines.push('=== CONSULTAS ===');
    lines.push('Data;Especialidade;Agendadas;Realizadas;Canceladas;<15Anos;>15Anos;Total');
    dates.forEach(function (date) {
      var raw = _safeGet(_storageKey('consultas', date));
      var cData = raw ? JSON.parse(raw) : {};
      esp.forEach(function (e) {
        var d = cData[e] || {ag:0,re:0,ca:0,m15:0,M15:0};
        if (d.ag || d.re || d.ca || d.m15 || d.M15) {
          lines.push([date, e, d.ag, d.re, d.ca, d.m15, d.M15, (d.m15+d.M15)].join(';'));
        }
      });
    });
    lines.push('');

    /* === PROCEDIMENTOS === */
    lines.push('=== PROCEDIMENTOS ===');
    lines.push('Data;Procedimento;Manhã;Tarde;Total');
    dates.forEach(function (date) {
      var raw = _safeGet(_storageKey('proc', date));
      var pData = raw ? JSON.parse(raw) : {};
      proc.forEach(function (p) {
        var d = pData[p] || {manha:0,tarde:0};
        if (d.manha || d.tarde) {
          lines.push([date, p, d.manha, d.tarde, (d.manha+d.tarde)].join(';'));
        }
      });
    });
    lines.push('');

    /* === MATERIAL === */
    lines.push('=== MATERIAL ===');
    lines.push('Data;Material;Unidade;Stock;Usado;Saldo');
    dates.forEach(function (date) {
      var raw = _safeGet(_storageKey('mat', date));
      var mData = raw ? JSON.parse(raw) : {};
      mats.forEach(function (mat) {
        var d = mData[mat.nome] || {stock:0,usado:0};
        if (d.stock || d.usado) {
          lines.push([date, mat.nome, mat.unit, d.stock, d.usado, Math.max(0, d.stock-d.usado)].join(';'));
        }
      });
    });

    var csvContent = '﻿' + lines.join('\n');
    var first = dates[0], last = dates[dates.length-1];
    var filename = 'Prenda_CE_Lote_' + first + '_a_' + last + '.csv';
    _triggerDownload(csvContent, filename, 'text/csv;charset=utf-8');
    _toast('CSV exportado com ' + dates.length + ' dia(s): ' + filename, 'ok');
    console.log(LOG, 'Bulk CSV exportado:', filename);
  };

  /* ═══════════════════════════════════════════════════════════════
     6.  importDayFromJSON(jsonString) — importar dia a partir de JSON
  ═══════════════════════════════════════════════════════════════ */
  /**
   * Importa dados de um dia a partir de um JSON (mesmo formato do localStorage).
   * Espera: { date, consultas, proc, mat } ou { consultas, proc, mat }
   * @param {string} jsonString — JSON como string
   */
  global.importDayFromJSON = function (jsonString) {
    console.log(LOG, 'importDayFromJSON chamado');
    var obj;
    try {
      obj = JSON.parse(jsonString);
    } catch (e) {
      _toast('JSON inválido: ' + e.message, 'err');
      return;
    }

    var date = obj.date || _todayKey();
    var consultas = obj.consultas || null;
    var proc = obj.proc || null;
    var mat = obj.mat || null;

    if (!consultas && !proc && !mat) {
      _toast('O JSON não contém dados válidos (consultas, proc ou mat).', 'err');
      return;
    }

    var count = 0;
    if (consultas) { _safeSet(_storageKey('consultas', date), JSON.stringify(consultas)); count++; }
    if (proc)      { _safeSet(_storageKey('proc',      date), JSON.stringify(proc));      count++; }
    if (mat)       { _safeSet(_storageKey('mat',       date), JSON.stringify(mat));       count++; }

    /* Registar data na lista de datas guardadas */
    var savedDates = JSON.parse(_safeGet('prenda_saved_dates') || '[]');
    if (!savedDates.includes(date)) {
      savedDates.push(date);
      savedDates.sort();
      _safeSet('prenda_saved_dates', JSON.stringify(savedDates));
    }

    _toast('Dados importados para ' + _formatDate(date) + ' (' + count + ' secção(ões)).', 'ok');
    console.log(LOG, 'JSON importado para', date, '— secções:', count);

    /* Recarregar se for o dia de hoje */
    if (date === _todayKey() && typeof global.loadDay === 'function') {
      global.loadDay(date);
    }
  };

  /* ═══════════════════════════════════════════════════════════════
     7.  createBackup() — exportar todo o localStorage prenda_*
  ═══════════════════════════════════════════════════════════════ */
  /**
   * Exporta todas as chaves prenda_* do localStorage como um único ficheiro JSON.
   */
  global.createBackup = function () {
    console.log(LOG, 'createBackup iniciado');
    var backup = {
      _meta: {
        createdAt:   new Date().toISOString(),
        version:     '1.0',
        application: 'Hospital do Prenda — Consulta Externa'
      }
    };
    var count = 0;
    try {
      for (var i = 0; i < localStorage.length; i++) {
        var k = localStorage.key(i);
        if (k && k.startsWith('prenda_')) {
          backup[k] = _safeGet(k);
          count++;
        }
      }
    } catch (e) {
      console.error(LOG, 'Erro ao ler localStorage para backup:', e);
      _toast('Erro ao criar backup: ' + e.message, 'err');
      return;
    }

    var jsonStr = JSON.stringify(backup, null, 2);
    var dateStr = new Date().toISOString().slice(0, 10);
    var filename = 'Prenda_Backup_' + dateStr + '.json';
    _triggerDownload(jsonStr, filename, 'application/json;charset=utf-8');
    _toast('Backup criado com ' + count + ' chave(s): ' + filename, 'save');
    console.log(LOG, 'Backup exportado:', filename, '—', count, 'chaves.');
  };

  /* ═══════════════════════════════════════════════════════════════
     8.  restoreBackup(jsonString) — restaurar backup
  ═══════════════════════════════════════════════════════════════ */
  /**
   * Restaura dados de um ficheiro de backup JSON previamente criado por createBackup().
   * @param {string} jsonString — conteúdo do ficheiro de backup
   */
  global.restoreBackup = function (jsonString) {
    console.log(LOG, 'restoreBackup iniciado');
    var obj;
    try {
      obj = JSON.parse(jsonString);
    } catch (e) {
      _toast('JSON de backup inválido: ' + e.message, 'err');
      return;
    }

    if (!obj || typeof obj !== 'object') {
      _toast('Backup inválido — estrutura não reconhecida.', 'err');
      return;
    }

    var restored = 0;
    var skipped = 0;
    Object.keys(obj).forEach(function (k) {
      if (k === '_meta') return; /* ignorar metadados */
      if (!k.startsWith('prenda_')) { skipped++; return; }
      if (_safeSet(k, obj[k])) {
        restored++;
      } else {
        skipped++;
      }
    });

    _toast('Backup restaurado: ' + restored + ' chave(s) reposta(s).', 'save');
    console.log(LOG, 'Backup restaurado —', restored, 'chaves,', skipped, 'ignoradas.');

    /* Recarregar a página para reflectir os dados restaurados */
    if (restored > 0) {
      setTimeout(function () {
        if (typeof global.loadDay === 'function') {
          global.loadDay(_todayKey());
        }
        if (typeof global.renderHistory === 'function') {
          global.renderHistory('dia');
        }
      }, 600);
    }
  };

  /* ─────────────────────────────────────────────────────────────
     Hook automático: validar após saveAllData
     Aguarda que o DOM e as funções do HTML estejam prontas.
  ───────────────────────────────────────────────────────────── */
  document.addEventListener('DOMContentLoaded', function () {
    var _origSave = global.saveAllData;
    if (typeof _origSave === 'function') {
      global.saveAllData = function () {
        var result = _origSave.apply(this, arguments);
        /* Validar após guardar (com pequeno atraso para deixar o async terminar) */
        setTimeout(function () {
          var warnings = global.validateDayData(_todayKey());
          if (warnings.length > 0) {
            console.warn(LOG, 'Avisos de validação:', warnings);
            /* Mostrar apenas o primeiro aviso para não sobrecarregar */
            _toast('Aviso: ' + warnings[0], 'warn');
          }
        }, 800);
        return result;
      };
      console.log(LOG, 'Hook de validação automática instalado em saveAllData.');
    }
  });

  console.log(LOG, 'hprenda-crud.js carregado.');

}(window));
