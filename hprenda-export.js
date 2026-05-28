/**
 * hprenda-export.js — Exportação adicional: Excel (SheetJS) e PDF helpers
 * Hospital do Prenda — Consulta Externa
 *
 * Expõe (em window):
 *   exportToExcel(dates, period)   → async — exporta workbook XLSX com 3 folhas
 *   generateSummaryCard(date)      → gera PDF de página única com totais do dia
 *   printSection(sectionId)        → imprime apenas uma secção
 *   prepareForPrint()              → adiciona classe CSS de impressão ao body
 */

(function (global) {
  'use strict';

  var LOG = '[hprenda-export]';

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
    var p = d.split('-');
    return p[2] + '/' + p[1] + '/' + p[0];
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
    var esp = _ESPECIALIDADES();
    var agg = {};
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
    var proc = _PROCEDIMENTOS();
    var agg = {};
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
    var mats = _MATERIAIS();
    var agg = {};
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

  /* ─────────────────────────────────────────────────────────────
     SheetJS loader dinâmico
  ───────────────────────────────────────────────────────────── */
  var SHEETJS_CDN = 'https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js';
  var _sheetJsLoading = false;
  var _sheetJsReady   = false;
  var _sheetJsQueue   = [];

  function _loadSheetJS() {
    return new Promise(function (resolve, reject) {
      if (_sheetJsReady && global.XLSX) { resolve(global.XLSX); return; }
      _sheetJsQueue.push({resolve: resolve, reject: reject});
      if (_sheetJsLoading) return;
      _sheetJsLoading = true;
      var s = document.createElement('script');
      s.src = SHEETJS_CDN;
      s.onload = function () {
        _sheetJsReady = true;
        _sheetJsLoading = false;
        console.log(LOG, 'SheetJS carregado com sucesso.');
        _sheetJsQueue.forEach(function (q) { q.resolve(global.XLSX); });
        _sheetJsQueue = [];
      };
      s.onerror = function () {
        _sheetJsLoading = false;
        var err = new Error('Falha ao carregar SheetJS de: ' + SHEETJS_CDN);
        _sheetJsQueue.forEach(function (q) { q.reject(err); });
        _sheetJsQueue = [];
      };
      document.head.appendChild(s);
    });
  }

  /* ═══════════════════════════════════════════════════════════════
     1.  exportToExcel(dates, period) — workbook XLSX com 3 folhas
  ═══════════════════════════════════════════════════════════════ */
  /**
   * Gera e descarrega um ficheiro Excel (.xlsx) com 3 folhas.
   * @param {string[]} dates  — array de YYYY-MM-DD
   * @param {string}   period — 'dia' | 'semana' | 'mes' | outro (usado no nome do ficheiro)
   */
  global.exportToExcel = async function (dates, period) {
    if (!dates || dates.length === 0) {
      _toast('Nenhuma data seleccionada para exportação Excel.', 'warn');
      return;
    }
    period = period || 'periodo';
    console.log(LOG, 'exportToExcel — datas:', dates.length, 'período:', period);
    _toast('A preparar ficheiro Excel…', 'info');

    var XLSX;
    try {
      XLSX = await _loadSheetJS();
    } catch (e) {
      _toast('Não foi possível carregar SheetJS. Verifique a ligação à internet.', 'err');
      console.error(LOG, 'SheetJS load error:', e);
      return;
    }

    var esp  = _ESPECIALIDADES();
    var proc = _PROCEDIMENTOS();
    var mats = _MATERIAIS();
    var cAgg = _aggConsultas(dates);
    var pAgg = _aggProc(dates);
    var mAgg = _aggMat(dates);

    /* ── Folha 1: Consultas ── */
    var consultasData = [];
    consultasData.push(['Hospital do Prenda — Consulta Externa']);
    consultasData.push(['Período: ' + dates.map(_formatDate).join(', ')]);
    consultasData.push([]); /* linha vazia */
    consultasData.push(['Especialidade', 'Agendadas', 'Realizadas', 'Canceladas', '<15 Anos', '>15 Anos', 'Total Atend.', '% Realização', '% Cancelamento']);

    var tAg=0, tRe=0, tCa=0, tm15=0, tM15=0;
    esp.forEach(function (e) {
      var d = cAgg[e];
      tAg+=d.ag; tRe+=d.re; tCa+=d.ca; tm15+=d.m15; tM15+=d.M15;
      var tot = d.m15 + d.M15;
      consultasData.push([
        e, d.ag, d.re, d.ca, d.m15, d.M15, tot,
        d.ag > 0 ? parseFloat((d.re/d.ag*100).toFixed(1)) : 0,
        d.ag > 0 ? parseFloat((d.ca/d.ag*100).toFixed(1)) : 0
      ]);
    });
    /* Linha de totais */
    consultasData.push([
      'TOTAL GERAL', tAg, tRe, tCa, tm15, tM15, tm15+tM15,
      tAg > 0 ? parseFloat((tRe/tAg*100).toFixed(1)) : 0,
      tAg > 0 ? parseFloat((tCa/tAg*100).toFixed(1)) : 0
    ]);

    /* ── Folha 2: Procedimentos ── */
    var procData = [];
    procData.push(['Hospital do Prenda — Consulta Externa']);
    procData.push(['Período: ' + dates.map(_formatDate).join(', ')]);
    procData.push([]);
    procData.push(['Procedimento', 'Manhã', 'Tarde', 'Total']);

    var tManha=0, tTarde=0;
    proc.forEach(function (p) {
      var d = pAgg[p];
      tManha += d.manha; tTarde += d.tarde;
      procData.push([p, d.manha, d.tarde, d.manha + d.tarde]);
    });
    procData.push(['TOTAL', tManha, tTarde, tManha + tTarde]);

    /* ── Folha 3: Material ── */
    var matData = [];
    matData.push(['Hospital do Prenda — Consulta Externa']);
    matData.push(['Período: ' + dates.map(_formatDate).join(', ')]);
    matData.push([]);
    matData.push(['Material', 'Unidade', 'Stock', 'Usado', 'Saldo']);

    var tStock=0, tUsado=0;
    mats.forEach(function (mat) {
      var d = mAgg[mat.nome];
      tStock += d.stock; tUsado += d.usado;
      matData.push([mat.nome, mat.unit, d.stock, d.usado, Math.max(0, d.stock - d.usado)]);
    });
    matData.push(['TOTAL', '', tStock, tUsado, Math.max(0, tStock - tUsado)]);

    /* ── Construção do workbook ── */
    var wb = XLSX.utils.book_new();

    var wsConsultas = XLSX.utils.aoa_to_sheet(consultasData);
    var wsProc      = XLSX.utils.aoa_to_sheet(procData);
    var wsMat       = XLSX.utils.aoa_to_sheet(matData);

    /* Larguras das colunas */
    wsConsultas['!cols'] = [
      {wch:28},{wch:12},{wch:12},{wch:12},{wch:10},{wch:10},{wch:14},{wch:14},{wch:16}
    ];
    wsProc['!cols'] = [{wch:28},{wch:12},{wch:12},{wch:12}];
    wsMat['!cols']  = [{wch:28},{wch:10},{wch:10},{wch:10},{wch:10}];

    XLSX.utils.book_append_sheet(wb, wsConsultas, 'Consultas');
    XLSX.utils.book_append_sheet(wb, wsProc,      'Procedimentos');
    XLSX.utils.book_append_sheet(wb, wsMat,       'Material');

    /* ── Download ── */
    var dateStr = new Date().toISOString().slice(0, 10);
    var periodLabel = {dia:'Diario', semana:'Semanal', mes:'Mensal'}[period] || period;
    var filename = 'Prenda_Consulta_Externa_' + periodLabel + '_' + dateStr + '.xlsx';

    try {
      XLSX.writeFile(wb, filename);
      _toast('Excel exportado: ' + filename, 'ok');
      console.log(LOG, 'Excel exportado:', filename);
    } catch (e) {
      console.error(LOG, 'Erro ao escrever ficheiro Excel:', e);
      _toast('Erro ao gerar Excel: ' + e.message, 'err');
    }
  };

  /* ═══════════════════════════════════════════════════════════════
     2.  generateSummaryCard(date) — PDF de página única (totais)
  ═══════════════════════════════════════════════════════════════ */
  /**
   * Gera um PDF compacto de página única com os totais do dia.
   * @param {string} [date] — YYYY-MM-DD (default: hoje)
   */
  global.generateSummaryCard = function (date) {
    date = date || _todayKey();
    console.log(LOG, 'generateSummaryCard:', date);

    if (!global.jspdf || !global.jspdf.jsPDF) {
      _toast('jsPDF não está disponível. Certifique-se de que o script foi carregado.', 'err');
      console.error(LOG, 'jsPDF não encontrado em window.jspdf');
      return;
    }

    var jsPDF = global.jspdf.jsPDF;
    var esp   = _ESPECIALIDADES();
    var proc  = _PROCEDIMENTOS();
    var mats  = _MATERIAIS();

    var cRaw = _safeGet(_storageKey('consultas', date));
    var pRaw = _safeGet(_storageKey('proc', date));
    var mRaw = _safeGet(_storageKey('mat', date));
    var cData = cRaw ? JSON.parse(cRaw) : {};
    var pData = pRaw ? JSON.parse(pRaw) : {};
    var mData = mRaw ? JSON.parse(mRaw) : {};

    /* Calcular totais */
    var tAg=0, tRe=0, tCa=0, tm15=0, tM15=0;
    esp.forEach(function (e) {
      var d = cData[e] || {ag:0,re:0,ca:0,m15:0,M15:0};
      tAg+=d.ag; tRe+=d.re; tCa+=d.ca; tm15+=d.m15; tM15+=d.M15;
    });
    var tProc=0;
    proc.forEach(function (p) {
      var d = pData[p] || {manha:0,tarde:0};
      tProc += d.manha + d.tarde;
    });
    var tStock=0, tUsado=0;
    mats.forEach(function (mat) {
      var d = mData[mat.nome] || {stock:0,usado:0};
      tStock += d.stock; tUsado += d.usado;
    });
    var pctR = tAg > 0 ? (tRe/tAg*100).toFixed(1) + '%' : '—';
    var pctC = tAg > 0 ? (tCa/tAg*100).toFixed(1) + '%' : '—';

    /* Criar PDF */
    var doc = new jsPDF({orientation:'portrait', unit:'mm', format:'a5'});
    var W = 148, margin = 14;
    var navy  = [26, 86, 219];
    var green = [5, 150, 105];
    var amber = [217, 119, 6];
    var grey  = [100, 116, 139];
    var light = [239, 246, 255];

    /* Cabeçalho */
    doc.setFillColor(26, 86, 219);
    doc.rect(0, 0, W, 28, 'F');
    doc.setTextColor(255, 255, 255);
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(13);
    doc.text('HOSPITAL DO PRENDA', margin, 10);
    doc.setFontSize(9);
    doc.setFont('helvetica', 'normal');
    doc.text('Consulta Externa — Resumo do Dia', margin, 17);
    doc.setFontSize(8);
    doc.setTextColor(147, 197, 253);
    doc.text('Data: ' + _formatDate(date), margin, 24);
    doc.text('Emitido: ' + _formatDate(_todayKey()), W - margin, 24, {align:'right'});

    var y = 35;

    /* KPI Grid 2×3 */
    var kpis = [
      {l:'Agendadas',  v:String(tAg),  c:navy},
      {l:'Realizadas', v:String(tRe),  c:green},
      {l:'Canceladas', v:String(tCa),  c:amber},
      {l:'<15 Anos',   v:String(tm15), c:navy},
      {l:'>15 Anos',   v:String(tM15), c:navy},
      {l:'% Realiz.',  v:pctR,         c:green}
    ];
    var cols = 3;
    var kw = (W - 2*margin - (cols-1)*4) / cols;
    var kh = 18;
    kpis.forEach(function (k, i) {
      var col = i % cols;
      var row = Math.floor(i / cols);
      var x = margin + col * (kw + 4);
      var ky = y + row * (kh + 4);
      doc.setFillColor(239, 246, 255);
      doc.roundedRect(x, ky, kw, kh, 2, 2, 'F');
      doc.setFont('helvetica', 'bold');
      doc.setFontSize(14);
      doc.setTextColor(k.c[0], k.c[1], k.c[2]);
      doc.text(k.v, x + kw/2, ky + 10, {align:'center'});
      doc.setFont('helvetica', 'normal');
      doc.setFontSize(7);
      doc.setTextColor(grey[0], grey[1], grey[2]);
      doc.text(k.l, x + kw/2, ky + 15.5, {align:'center'});
    });
    y += 2 * (kh + 4) + 6;

    /* Linha divisória */
    doc.setDrawColor(200, 210, 230);
    doc.setLineWidth(0.4);
    doc.line(margin, y, W-margin, y);
    y += 6;

    /* Secção: Procedimentos e Material */
    var _row = function (label, value, cy) {
      doc.setFont('helvetica', 'normal');
      doc.setFontSize(9);
      doc.setTextColor(grey[0], grey[1], grey[2]);
      doc.text(label, margin, cy);
      doc.setFont('helvetica', 'bold');
      doc.setTextColor(26, 86, 219);
      doc.text(String(value), W - margin, cy, {align:'right'});
    };

    doc.setFont('helvetica', 'bold');
    doc.setFontSize(9);
    doc.setTextColor(navy[0], navy[1], navy[2]);
    doc.text('Resumo de Procedimentos e Material', margin, y);
    y += 6;

    _row('Total de Procedimentos:', tProc, y); y += 5.5;
    _row('Stock Total Registado:', tStock, y); y += 5.5;
    _row('Material Consumido:', tUsado, y); y += 5.5;
    _row('Saldo de Material:', Math.max(0, tStock-tUsado), y); y += 5.5;
    _row('% Cancelamento:', pctC, y); y += 8;

    /* Rodapé */
    doc.setFillColor(248, 250, 252);
    doc.rect(0, doc.internal.pageSize.getHeight()-14, W, 14, 'F');
    doc.setFont('helvetica', 'italic');
    doc.setFontSize(7);
    doc.setTextColor(grey[0], grey[1], grey[2]);
    doc.text('Hospital do Prenda — Documento gerado automaticamente', W/2, doc.internal.pageSize.getHeight()-5, {align:'center'});

    var filename = 'Prenda_Resumo_' + date + '.pdf';
    doc.save(filename);
    _toast('Cartão PDF gerado: ' + filename, 'pdf');
    console.log(LOG, 'Summary card PDF gerado:', filename);
  };

  /* ═══════════════════════════════════════════════════════════════
     3.  printSection(sectionId) — imprimir apenas uma secção
  ═══════════════════════════════════════════════════════════════ */
  /**
   * Imprime apenas o conteúdo de uma secção específica.
   * Cria um iframe temporário para isolar o conteúdo.
   * @param {string} sectionId — ID do elemento HTML a imprimir
   */
  global.printSection = function (sectionId) {
    var el = document.getElementById(sectionId);
    if (!el) {
      _toast('Secção não encontrada: ' + sectionId, 'err');
      console.error(LOG, 'printSection: elemento não encontrado:', sectionId);
      return;
    }

    console.log(LOG, 'printSection:', sectionId);

    /* Recolher estilos existentes */
    var styles = '';
    Array.from(document.querySelectorAll('style,link[rel="stylesheet"]')).forEach(function (node) {
      if (node.tagName === 'STYLE') {
        styles += '<style>' + node.innerHTML + '</style>';
      } else if (node.href) {
        styles += '<link rel="stylesheet" href="' + node.href + '">';
      }
    });

    var content = el.innerHTML;
    var iframe = document.createElement('iframe');
    iframe.style.cssText = 'position:fixed;top:-9999px;left:-9999px;width:210mm;height:297mm;border:none;';
    document.body.appendChild(iframe);

    var iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
    iframeDoc.open();
    iframeDoc.write('<!DOCTYPE html><html lang="pt"><head><meta charset="UTF-8">' + styles +
      '<style>@media print{body{margin:0;padding:16px;}}.no-print{display:none!important;}</style>' +
      '</head><body>' + content + '</body></html>');
    iframeDoc.close();

    iframe.onload = function () {
      setTimeout(function () {
        iframe.contentWindow.focus();
        iframe.contentWindow.print();
        setTimeout(function () { document.body.removeChild(iframe); }, 1000);
      }, 300);
    };
  };

  /* ═══════════════════════════════════════════════════════════════
     4.  prepareForPrint() — adicionar classe CSS para impressão
  ═══════════════════════════════════════════════════════════════ */
  /**
   * Adiciona a classe 'print-mode' ao body e lança window.print().
   * Remove a classe após a impressão.
   */
  global.prepareForPrint = function () {
    console.log(LOG, 'prepareForPrint chamado');
    document.body.classList.add('print-mode');

    /* Injectar CSS de impressão específico, se não existir */
    if (!document.getElementById('hprenda-print-style')) {
      var style = document.createElement('style');
      style.id = 'hprenda-print-style';
      style.innerHTML = [
        '@media print {',
        '  body.print-mode .no-print { display: none !important; }',
        '  body.print-mode .sidebar  { display: none !important; }',
        '  body.print-mode .topbar   { display: none !important; }',
        '  body.print-mode .main     { padding: 0 !important; }',
        '  body.print-mode .section:not(.active) { display: none !important; }',
        '  body.print-mode .btn      { display: none !important; }',
        '  body.print-mode table     { page-break-inside: auto; }',
        '  body.print-mode tr        { page-break-inside: avoid; }',
        '}'
      ].join('\n');
      document.head.appendChild(style);
    }

    /* Aguardar que os estilos sejam aplicados e depois imprimir */
    setTimeout(function () {
      global.print();
      /* Remover classe após diálogo de impressão ser fechado */
      setTimeout(function () {
        document.body.classList.remove('print-mode');
        console.log(LOG, 'Classe print-mode removida do body.');
      }, 1500);
    }, 150);
  };

  console.log(LOG, 'hprenda-export.js carregado.');

}(window));
