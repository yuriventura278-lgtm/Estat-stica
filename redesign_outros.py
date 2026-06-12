#!/usr/bin/env python3
"""
Aplica as actualizações visuais aos 5 serviços adicionais:
  • Splash com anel circular de 5 segundos + foto real do hospital
  • Botão de tema claro/escuro com preferência em localStorage
  • Barra de staff (nome do profissional + chefe de turno)
  • Prevenção de FOUC (flash of unstyled content)
  • Análise estatística com gráficos Chart.js + medidas + leitura/interpretação
"""

import re
import os

UPLOADS = '/root/.claude/uploads/039233f2-2ff9-45a6-bc34-cf6cd2d282ab'
OUT     = '/home/user/Estat-stica/procedimentos'

# (source_file, output_file, service_label, theme_default, file_type)
FILES = [
    ('43558ce6-blocooperatorio2.html', 'proc_bloco_operatorio2.html', 'Serviço de Bloco Operatório', 'dark',     'bloco_op2'),
    ('7b3a412c-laboratorio4.html',     'proc_laboratorio.html',       'Serviço de Laboratório',      'light',    'lab'),
    ('90a3f128-consultaexterna.html',  'proc_consulta_externa2.html', 'Consulta Externa',            'dark_nav', 'consulta_ext'),
    ('ee69e8a1-imagiologia5.html',     'proc_imagiologia.html',       'Serviço de Imagiologia',      'light',    'imag'),
    ('f2665fdb-fisioterapia111.html',  'proc_fisioterapia.html',      'Serviço de Fisioterapia',     'light',    'fisio'),
]

FILES_EXTRA = [
    ('/root/.claude/uploads/3eaa2d18-9bc1-4442-91a7-7c598dcde8ce/8b6b05f4-Cirurgia_Geral1.html',
     'proc_cirurgia_geral.html', 'Cirurgia Geral', 'light_cg', 'cirurgia'),
]

_CIRC = 263.9  # 2π × 42  (viewBox 100×100, r=42)

CHARTJS_CDN = '<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>'

# ─── helpers ─────────────────────────────────────────────────────────────────

def extract_hosp_img(content):
    m = re.search(r'src="(data:image/jpeg;base64,[^"]{200,})"', content)
    return m.group(1) if m else 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs='


def make_splash_html(hosp_img, service_label):
    return (
        '<div id="splash">\n'
        '  <div class="splash-inner">\n'
        '    <div class="splash-img-ring">\n'
        '      <div class="splash-img-circle">\n'
        f'        <img src="{hosp_img}" alt="Hospital do Prenda">\n'
        '      </div>\n'
        '      <svg class="splash-progress-svg" viewBox="0 0 100 100">\n'
        '        <circle class="spl-ring-bg" cx="50" cy="50" r="42"/>\n'
        f'        <circle class="spl-ring-fg" id="spl-ring" cx="50" cy="50" r="42"'
        f' stroke-dasharray="{_CIRC}" stroke-dashoffset="{_CIRC}"/>\n'
        '      </svg>\n'
        '    </div>\n'
        '    <p class="splash-hosp-lbl">Hospital do Prenda · Luanda</p>\n'
        f'    <h1 class="splash-svc-lbl">{service_label}</h1>\n'
        '    <div class="splash-pct" id="spl-pct">0%</div>\n'
        '  </div>\n'
        '</div>'
    )


SPLASH_CSS = '''
/* ── SPLASH RING ── */
#splash{position:fixed;inset:0;z-index:9999;background:var(--bg,#0c0f14);
  display:flex;align-items:center;justify-content:center;}
.splash-inner{display:flex;flex-direction:column;align-items:center;text-align:center;gap:14px;}
.splash-img-ring{position:relative;width:100px;height:100px;flex-shrink:0;}
.splash-img-circle{position:absolute;inset:8px;border-radius:50%;overflow:hidden;background:#1a2a3a;}
.splash-img-circle img{width:100%;height:100%;object-fit:cover;}
.splash-progress-svg{position:absolute;inset:0;width:100px;height:100px;transform:rotate(-90deg);}
.spl-ring-bg{fill:none;stroke:rgba(255,255,255,.12);stroke-width:4;}
.spl-ring-fg{fill:none;stroke:#00d4aa;stroke-width:4;stroke-linecap:round;}
.splash-hosp-lbl{font-size:.55rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;
  color:rgba(200,230,220,.65);font-family:var(--font-head,var(--fh,Inter,sans-serif));}
.splash-svc-lbl{font-size:.95rem;font-weight:700;color:#fff;max-width:300px;line-height:1.35;
  font-family:var(--font-head,var(--fh,Inter,sans-serif));}
.splash-pct{font-size:.65rem;color:#00d4aa;font-weight:600;letter-spacing:.05em;
  font-family:var(--font-body,var(--fb,monospace));}
'''

# ── Statistical analysis CSS ─────────────────────────────────────────────────

ANALYSIS_CSS = '''
/* ── HP STATISTICAL ANALYSIS ── */
.hp-analysis-wrap{margin-top:20px;border-radius:12px;overflow:hidden;
  border:1px solid rgba(0,212,170,.2);}
.hp-analysis-title{font-size:.68rem;font-weight:700;letter-spacing:.09em;
  text-transform:uppercase;padding:13px 18px;
  background:rgba(0,212,170,.08);border-bottom:1px solid rgba(0,212,170,.15);
  color:var(--text,#e2e8f0);}
html.light .hp-analysis-title{color:#1e293b;background:rgba(0,180,150,.07);}
.hp-stats-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));
  gap:8px;padding:14px 16px;}
.hp-stat{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.09);
  border-radius:8px;padding:10px 8px;text-align:center;}
html.light .hp-stat{background:#f8fafc;border-color:#e2e8f0;}
.hp-stat-label{font-size:.46rem;text-transform:uppercase;letter-spacing:.12em;
  color:rgba(148,163,184,.8);margin-bottom:5px;
  font-family:var(--font-head,var(--fh,Inter,sans-serif));}
html.light .hp-stat-label{color:#94a3b8;}
.hp-stat-val{font-size:1.25rem;font-weight:700;color:var(--text,#e2e8f0);font-family:monospace;}
html.light .hp-stat-val{color:#1e293b;}
.hp-chart-wrap{padding:12px 16px;height:200px;position:relative;}
.hp-interp-box{margin:0 16px 16px;padding:12px 16px;
  background:rgba(0,212,170,.06);border-left:3px solid #00d4aa;
  border-radius:0 8px 8px 0;font-size:.68rem;line-height:1.75;
  color:var(--text,#cbd5e1);}
html.light .hp-interp-box{background:rgba(0,180,150,.05);color:#1e293b;}
'''

# ── Common analysis JS ────────────────────────────────────────────────────────

COMMON_ANALYSIS_JS = r'''
// ── HP STATISTICAL ANALYSIS ENGINE ──
var _hpCharts={};
function _hpCalcStats(vals){
  if(!vals||!vals.length)return null;
  var n=vals.length,sum=vals.reduce(function(a,b){return a+b;},0),mean=sum/n;
  var sorted=vals.slice().sort(function(a,b){return a-b;});
  var mid=Math.floor(n/2),median=n%2?sorted[mid]:(sorted[mid-1]+sorted[mid])/2;
  var freq={};vals.forEach(function(v){freq[v]=(freq[v]||0)+1;});
  var maxF=Math.max.apply(null,Object.values(freq));
  var modes=Object.keys(freq).filter(function(k){return freq[k]===maxF;})
    .map(Number).sort(function(a,b){return a-b;});
  var variance=vals.reduce(function(s,v){return s+(v-mean)*(v-mean);},0)/n;
  return{n:n,sum:sum,mean:+(mean.toFixed(2)),median:+(median.toFixed(2)),
    mode:modes,min:sorted[0],max:sorted[n-1],std:+(Math.sqrt(variance).toFixed(2))};
}
function _hpStatsHtml(s){
  if(!s)return '';
  var modeStr=s.mode.length>3?s.mode.slice(0,3).join('/')+'+':s.mode.join('/');
  return '<div class="hp-stats-grid">'
    +'<div class="hp-stat"><div class="hp-stat-label">N dias</div><div class="hp-stat-val">'+s.n+'</div></div>'
    +'<div class="hp-stat"><div class="hp-stat-label">Média</div><div class="hp-stat-val">'+s.mean+'</div></div>'
    +'<div class="hp-stat"><div class="hp-stat-label">Mediana</div><div class="hp-stat-val">'+s.median+'</div></div>'
    +'<div class="hp-stat"><div class="hp-stat-label">Moda</div><div class="hp-stat-val">'+modeStr+'</div></div>'
    +'<div class="hp-stat"><div class="hp-stat-label">Mínimo</div><div class="hp-stat-val">'+s.min+'</div></div>'
    +'<div class="hp-stat"><div class="hp-stat-label">Máximo</div><div class="hp-stat-val">'+s.max+'</div></div>'
    +'<div class="hp-stat"><div class="hp-stat-label">Desv. Pad.</div><div class="hp-stat-val">'+s.std+'</div></div>'
    +'<div class="hp-stat"><div class="hp-stat-label">Total</div><div class="hp-stat-val">'+s.sum+'</div></div>'
    +'</div>';
}
function _hpInterpText(s,label){
  if(!s||s.n<2)return '<em>Insuficientes dados para análise estatística (mínimo 2 dias com registos).</em>';
  var cv=s.mean>0?+(s.std/s.mean*100).toFixed(1):0;
  var stab=cv<15?'baixa — fluxo estável':cv<30?'moderada — ligeira irregularidade':'elevada — fluxo irregular';
  var symm=(s.n>=4&&Math.abs(s.mean-s.median)>s.std*0.5)
    ?'distribuição assimétrica, com dias de valores atípicos'
    :'distribuição aproximadamente simétrica';
  var modeStr=s.mode.length===1
    ?'O valor mais frequente foi <strong>'+s.mode[0]+'</strong>.'
    :'Os valores mais frequentes foram <strong>'+s.mode.slice(0,3).join(', ')+'</strong>.';
  return '<strong>Leitura e Análise:</strong> Analisados <strong>'+s.n+'</strong> dias'
    +' com registos de <em>'+label+'</em>.'
    +' Média diária de <strong>'+s.mean+'</strong> (mediana: <strong>'+s.median+'</strong>),'
    +' entre <strong>'+s.min+'</strong> e <strong>'+s.max+'</strong>.'
    +' Desvio padrão <strong>'+s.std+'</strong> (CV='+cv+'%) — variabilidade '+stab+'.'
    +' '+modeStr
    +' Observa-se '+symm+'.'
    +' Total acumulado no período: <strong>'+s.sum+'</strong>.';
}
function _hpDrawChart(cid,labels,datasets){
  var canvas=document.getElementById(cid);
  if(!canvas||typeof Chart==='undefined')return;
  if(_hpCharts[cid]){try{_hpCharts[cid].destroy();}catch(e){}delete _hpCharts[cid];}
  var isDark=!document.documentElement.classList.contains('light');
  var gridCol=isDark?'rgba(148,163,184,.1)':'rgba(0,0,0,.06)';
  var tickCol=isDark?'#94a3b8':'#64748b';
  _hpCharts[cid]=new Chart(canvas.getContext('2d'),{
    type:'bar',
    data:{labels:labels,datasets:datasets},
    options:{
      responsive:true,maintainAspectRatio:false,
      plugins:{
        legend:{display:datasets.length>1,
          labels:{color:tickCol,font:{size:10},boxWidth:10,padding:8}},
        tooltip:{backgroundColor:'rgba(15,23,42,.9)',titleColor:'#e2e8f0',
          bodyColor:'#cbd5e1',cornerRadius:6,padding:8}
      },
      scales:{
        x:{ticks:{color:tickCol,maxRotation:55,font:{size:9}},
           grid:{color:gridCol}},
        y:{ticks:{color:tickCol,font:{size:10}},
           grid:{color:gridCol},beginAtZero:true}
      },
      animation:{duration:500}
    }
  });
}
function _hpAppendAnalysis(container,labels,valSets,title){
  if(!container||!labels||!labels.length||!valSets||!valSets.length)return;
  var mainVals=valSets[0].data;
  var s=_hpCalcStats(mainVals);
  if(!s||s.n<1)return;
  var cid='hpc'+(Math.random().toString(36).slice(2,8));
  var palette=['rgba(0,212,170,.75)','rgba(59,130,246,.75)','rgba(245,158,11,.75)',
               'rgba(239,68,68,.75)','rgba(139,92,246,.75)'];
  var borders=['#00d4aa','#3b82f6','#f59e0b','#ef4444','#8b5cf6'];
  var datasets=valSets.map(function(vs,i){return{
    label:vs.label,data:vs.data,
    backgroundColor:palette[i%palette.length],
    borderColor:borders[i%borders.length],
    borderWidth:1.5,borderRadius:3
  };});
  var wrap=document.createElement('div');
  wrap.className='hp-analysis-wrap';
  wrap.innerHTML=
    '<div class="hp-analysis-title">📊 Análise Estatística · '+title+'</div>'
    +_hpStatsHtml(s)
    +'<div class="hp-chart-wrap"><canvas id="'+cid+'"></canvas></div>'
    +'<div class="hp-interp-box">'+_hpInterpText(s,title)+'</div>';
  container.appendChild(wrap);
  setTimeout(function(){_hpDrawChart(cid,labels,datasets);},80);
}
'''

# ── Per-file render-function patches ─────────────────────────────────────────

ANALYSIS_PATCH_LAB = r'''
// ── LABORATÓRIO — análise estatística ──
(function(){
  var _orig=renderLabStats;
  renderLabStats=function(allData,period){
    _orig(allData,period);
    var container=document.getElementById('lab-stats-content');
    if(!container||!allData||!Object.keys(allData).length)return;
    var dates=_getLabDatesForPeriod(period);
    var fd=dates.filter(function(d){return allData&&allData[d];});
    if(fd.length<2)return;
    var totals=fd.map(function(d){var a=_aggregateLabDates([d],allData);return a._grandBu+a._grandInt;});
    var buVals=fd.map(function(d){var a=_aggregateLabDates([d],allData);return a._grandBu;});
    var intVals=fd.map(function(d){var a=_aggregateLabDates([d],allData);return a._grandInt;});
    var lbls=fd.map(function(d){return d.slice(8,10)+'/'+d.slice(5,7);});
    _hpAppendAnalysis(container,lbls,
      [{label:'Total',data:totals},{label:'B.Urgência',data:buVals},{label:'Internamento',data:intVals}],
      'Total de Exames por Dia');
  };
})();
'''

ANALYSIS_PATCH_IMAG = r'''
// ── IMAGIOLOGIA — análise estatística ──
(function(){
  var _orig=renderStats;
  renderStats=function(allData,period){
    _orig(allData,period);
    var container=document.getElementById('stats-content');
    if(!container||!allData||!Object.keys(allData).length)return;
    var dates=_getDatesForPeriod(period);
    var fd=dates.filter(function(d){return allData&&allData[d];});
    if(fd.length<2)return;
    var totals=fd.map(function(d){var a=_aggregate([d],allData);return a._grandBu+a._grandAut+a._grandInt;});
    var buVals=fd.map(function(d){var a=_aggregate([d],allData);return a._grandBu;});
    var autVals=fd.map(function(d){var a=_aggregate([d],allData);return a._grandAut;});
    var intVals=fd.map(function(d){var a=_aggregate([d],allData);return a._grandInt;});
    var lbls=fd.map(function(d){return d.slice(8,10)+'/'+d.slice(5,7);});
    _hpAppendAnalysis(container,lbls,
      [{label:'Total',data:totals},{label:'B.Urgência',data:buVals},
       {label:'Autorizados',data:autVals},{label:'Internamentos',data:intVals}],
      'Total de Exames por Dia');
  };
})();
'''

ANALYSIS_PATCH_FISIO = r'''
// ── FISIOTERAPIA — análise estatística ──
(function(){
  var _orig=renderFisioStats;
  renderFisioStats=function(allData,period){
    _orig(allData,period);
    var container=document.getElementById('fisio-stats-content');
    if(!container||!allData||!Object.keys(allData).length)return;
    var dates=_getFsDatesForPeriod(period);
    var fd=dates.filter(function(d){return allData&&allData[d];});
    if(fd.length<2)return;
    var totals=fd.map(function(d){var a=_aggregateFsioDates([d],allData);return a._intTotal+a._extTotal;});
    var intVals=fd.map(function(d){var a=_aggregateFsioDates([d],allData);return a._intTotal;});
    var extVals=fd.map(function(d){var a=_aggregateFsioDates([d],allData);return a._extTotal;});
    var lbls=fd.map(function(d){return d.slice(8,10)+'/'+d.slice(5,7);});
    _hpAppendAnalysis(container,lbls,
      [{label:'Total',data:totals},{label:'Internos',data:intVals},{label:'Externos',data:extVals}],
      'Total de Doentes por Dia');
  };
})();
'''

ANALYSIS_PATCH_BLOCO_OP2 = r'''
// ── BLOCO OPERATÓRIO 2 — análise estatística ──
(function(){
  var _orig=renderStats;
  renderStats=function(allData,period){
    _orig(allData,period);
    var container=document.getElementById('stats-content');
    if(!container||!allData||!Object.keys(allData).length)return;
    var range=_getDateRange(period);
    var fk=Object.keys(allData).filter(function(k){
      var d=_dateKeyToDate(k);return d>=range.start&&d<=range.end;
    }).sort();
    if(fk.length<2)return;
    var urgVals=fk.map(function(k){
      return((allData[k].surgeries&&allData[k].surgeries.urg)||[]).length;});
    var eletVals=fk.map(function(k){
      return((allData[k].surgeries&&allData[k].surgeries.elet)||[]).length;});
    var totals=fk.map(function(k,i){return urgVals[i]+eletVals[i];});
    var lbls=fk.map(function(k){return k.slice(6,8)+'/'+k.slice(4,6);});
    _hpAppendAnalysis(container,lbls,
      [{label:'Total',data:totals},{label:'Urgentes',data:urgVals},{label:'Eletivas',data:eletVals}],
      'Total de Cirurgias por Dia');
  };
})();
'''

ANALYSIS_PATCH_CONSULTA_EXT = r'''
// ── CONSULTA EXTERNA — análise estatística ──
(function(){
  var _orig=renderMonitorPeriod;
  renderMonitorPeriod=function(mode){
    _orig(mode);
    var monDiv=document.getElementById('monitor-'+mode);
    if(!monDiv)return;
    var prev=monDiv.querySelector('.hp-analysis-wrap');
    if(prev)prev.remove();
    var today=todayKey();
    var allDates=JSON.parse(localStorage.getItem('prenda_saved_dates')||'[]');
    var dates=[];
    if(mode==='dia'){
      dates=allDates.includes(today)?[today]:[];
    } else if(mode==='semana'){
      var mon=weekOf(today);
      var sat=new Date(mon+'T00:00:00');sat.setDate(sat.getDate()+6);
      dates=allDates.filter(function(d){return d>=mon&&d<=sat.toISOString().slice(0,10);});
    } else if(mode==='mes'){
      var m=today.slice(0,7);
      dates=allDates.filter(function(d){return d.startsWith(m);});
    }
    if(dates.length<2)return;
    var totals=dates.map(function(d){
      var c=JSON.parse(localStorage.getItem(storageKey('consultas',d))||'{}');
      return Object.values(c).reduce(function(s,v){return s+(v.re||0);},0);
    });
    var lbls=dates.map(function(d){return d.slice(8,10)+'/'+d.slice(5,7);});
    _hpAppendAnalysis(monDiv,lbls,
      [{label:'Consultas Realizadas',data:totals}],
      'Consultas Realizadas por Dia');
  };
})();
'''

ANALYSIS_PATCH_CIRURGIA = r'''
// ── CIRURGIA GERAL — análise estatística ──
(function(){
  var _orig=loadMov;
  loadMov=function(){
    _orig();
    var el=document.getElementById('mov-out');
    if(!el)return;
    var dates=getMPDates();
    if(!dates||dates.length<2)return;
    var daysWithData=dates.filter(function(d){
      var mv=calcMovDia(d);
      return mv.tent>0||mv.tsai>0||mv.dp>0;
    });
    if(daysWithData.length<2)return;
    var admVals=daysWithData.map(function(d){return calcMovDia(d).tent||0;});
    var saiVals=daysWithData.map(function(d){return calcMovDia(d).tsai||0;});
    var dpVals=daysWithData.map(function(d){return calcMovDia(d).dp||0;});
    var lbls=daysWithData.map(function(d){return d.slice(8,10)+'/'+d.slice(5,7);});
    _hpAppendAnalysis(el,lbls,
      [{label:'Admitidos',data:admVals},
       {label:'Saídos',data:saiVals},
       {label:'Dias Doente',data:dpVals}],
      'Movimento Hospitalar por Dia');
  };
})();
'''


def get_analysis_js(file_type):
    return {
        'lab':         ANALYSIS_PATCH_LAB,
        'imag':        ANALYSIS_PATCH_IMAG,
        'fisio':       ANALYSIS_PATCH_FISIO,
        'bloco_op2':   ANALYSIS_PATCH_BLOCO_OP2,
        'consulta_ext':ANALYSIS_PATCH_CONSULTA_EXT,
        'cirurgia':    ANALYSIS_PATCH_CIRURGIA,
    }.get(file_type, '')


SPLASH_RING_JS = r'''
// ── SPLASH RING ──
(function(){
  var DURATION=5000,ring=document.getElementById('spl-ring'),
      pct=document.getElementById('spl-pct'),CIRC=263.9,start=null;
  if(!ring)return;
  function step(ts){
    if(!start)start=ts;
    var p=Math.min((ts-start)/DURATION,1);
    var e=p<.5?2*p*p:-1+(4-2*p)*p;
    ring.style.strokeDashoffset=CIRC*(1-e);
    if(pct)pct.textContent=Math.round(e*100)+'%';
    if(p<1){requestAnimationFrame(step);return;}
    var s=document.getElementById('splash');
    if(s){s.style.transition='opacity .45s';s.style.opacity='0';
      setTimeout(function(){s.style.display='none';},450);}
  }
  requestAnimationFrame(step);
})();
'''

STAFF_JS = r'''
// ── STAFF INFO ──
function loadStaffInfo(){
  var raw=localStorage.getItem('_staff');var d=raw?JSON.parse(raw):{};
  var pi=document.getElementById('inp-profissional');
  var ci=document.getElementById('inp-chefe');
  if(pi)pi.value=d.profissional||'';if(ci)ci.value=d.chefe||'';
}
function saveStaffInfo(){
  var pi=document.getElementById('inp-profissional');
  var ci=document.getElementById('inp-chefe');
  localStorage.setItem('_staff',JSON.stringify({
    profissional:pi?pi.value.trim():'',chefe:ci?ci.value.trim():''}));
}
setTimeout(loadStaffInfo,80);
'''


def staff_bar_html():
    return (
        '<div class="hp-staff-bar" id="hp-staff-bar">'
        '<span class="hp-staff-lbl">Profissional</span>'
        '<input type="text" id="inp-profissional" class="hp-staff-inp" '
        'placeholder="Nome do profissional" autocomplete="name" oninput="saveStaffInfo()">'
        '<span class="hp-staff-sep">·</span>'
        '<span class="hp-staff-lbl">Chefe de Turno</span>'
        '<input type="text" id="inp-chefe" class="hp-staff-inp" '
        'placeholder="Nome do chefe de turno" autocomplete="name" oninput="saveStaffInfo()">'
        '</div>'
    )


def staff_bar_css(staff_h=38, header_h_var='var(--header-h)', bg='rgba(0,100,80,.15)',
                  border='rgba(0,212,170,.2)', label_color='rgba(110,231,183,.7)',
                  inp_color='#e8f4f0', inp_border='rgba(0,212,170,.3)'):
    return f'''
/* ── STAFF BAR ── */
.hp-staff-bar{{position:fixed;top:{header_h_var};left:0;right:0;z-index:190;
  height:{staff_h}px;background:{bg};border-bottom:1px solid {border};
  display:flex;align-items:center;gap:12px;padding:0 20px;}}
.hp-staff-lbl{{font-size:.48rem;color:{label_color};font-weight:600;
  text-transform:uppercase;letter-spacing:1.5px;white-space:nowrap;
  font-family:var(--font-head,var(--fh,'Inter',sans-serif));}}
.hp-staff-sep{{color:{inp_border};font-size:.8rem;margin:0 2px;}}
.hp-staff-inp{{background:transparent;border:none;border-bottom:1px solid {inp_border};
  color:{inp_color};font-family:var(--font-head,var(--fh,'Inter',sans-serif));
  font-size:.68rem;padding:2px 6px;outline:none;min-width:150px;max-width:210px;
  transition:border-color .13s;}}
.hp-staff-inp::placeholder{{opacity:.5;}}
.hp-staff-inp:focus{{border-bottom-color:rgba(0,212,170,.8);}}
'''


# ─── per-theme extras ─────────────────────────────────────────────────────────

DARK_MODE_LIGHT_PAGES = '''
/* ── DARK MODE ── */
html.dark{
  --bg:#0c0f14!important;--surface:#141820!important;--surface2:#0f1520!important;
  --border:#1e2840!important;--text:#e2e8f0!important;--muted:#64748b!important;
}
html.dark body{background:#0c0f14!important;color:#e2e8f0!important;}
html.dark header{background:#141820!important;border-bottom-color:#1e2840!important;}
html.dark .sidebar{background:#141820!important;border-right-color:#1e2840!important;}
html.dark .card,html.dark .table-container{background:#141820!important;border-color:#1e2840!important;}
html.dark input,html.dark select,html.dark textarea{
  background:#0f1520!important;color:#e2e8f0!important;border-color:#1e2840!important;}
html.dark .hp-staff-bar{background:rgba(30,40,64,.85)!important;border-bottom-color:#1e2840!important;}
html.dark .hp-staff-inp{color:#e2e8f0!important;border-bottom-color:#1e2840!important;}
html.dark .hp-staff-lbl{color:#64748b!important;}
html.dark #theme-toggle{color:#60a5fa!important;}
'''

DARK_TOGGLE_JS_LIGHT = r'''
// ── THEME TOGGLE (light default) ──
function toggleTheme(){
  var dark=document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme',dark?'dark':'light');
  var btn=document.getElementById('theme-toggle');
  if(btn)btn.title=dark?'Mudar para tema claro':'Mudar para tema escuro';
}
'''

FOUC_LIGHT = '<script>if(localStorage.getItem("theme")==="dark")document.documentElement.classList.add("dark");</script>'


LIGHT_MODE_DARK_PAGES = '''
/* ── LIGHT MODE ── */
html.light{
  --bg:#f8fafc!important;--surface:#ffffff!important;--surface2:#f1f5f9!important;
  --border:#e2e8f0!important;--text:#0f172a!important;--muted:#64748b!important;
}
html.light body{background:#f8fafc!important;color:#0f172a!important;}
html.light header,.html.light header{
  background:#ffffff!important;border-bottom:1px solid #e2e8f0!important;}
html.light .sidebar{background:#ffffff!important;border-right-color:#e2e8f0!important;}
html.light .card{background:#ffffff!important;border-color:#e2e8f0!important;}
html.light input,html.light select,html.light textarea{
  background:#ffffff!important;color:#0f172a!important;border-color:#e2e8f0!important;}
html.light .hp-staff-bar{background:oklch(97% .01 155)!important;border-bottom-color:#e2e8f0!important;}
html.light .hp-staff-inp{color:#0f172a!important;border-bottom-color:#e2e8f0!important;}
html.light .hp-staff-lbl{color:#6b7280!important;}
html.light #theme-toggle{color:#0f172a!important;}
'''

LIGHT_TOGGLE_JS_DARK = r'''
// ── THEME TOGGLE (dark default) ──
function toggleTheme(){
  var light=document.documentElement.classList.toggle('light');
  localStorage.setItem('theme',light?'light':'dark');
  var btn=document.getElementById('theme-toggle');
  if(btn)btn.title=light?'Mudar para tema escuro':'Mudar para tema claro';
}
'''

FOUC_DARK = '<script>if(localStorage.getItem("theme")==="light")document.documentElement.classList.add("light");</script>'


DARK_MODE_DARK_NAV = '''
/* ── DARK MODE ── */
html.dark .main{background:#0c0f14!important;color:#e2e8f0!important;}
html.dark .layout{background:#0c0f14!important;}
html.dark .card,html.dark [class*="card"],html.dark .table-container{
  background:#141820!important;border-color:#1e2840!important;}
html.dark input,html.dark select,html.dark textarea{
  background:#0f1520!important;color:#e2e8f0!important;border-color:#1e2840!important;}
html.dark .hp-staff-bar{background:rgba(0,50,80,.9)!important;border-bottom-color:rgba(6,182,212,.25)!important;}
html.dark .hp-staff-inp{color:#e2e8f0!important;}
html.dark .hp-staff-lbl{color:#94a3b8!important;}
html.dark #theme-toggle{color:#06b6d4!important;}
'''

FOUC_DARK_NAV = '<script>if(localStorage.getItem("theme")==="dark")document.documentElement.classList.add("dark");</script>'

DARK_TOGGLE_JS_DARK_NAV = r'''
// ── THEME TOGGLE (dark nav) ──
function toggleTheme(){
  var dark=document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme',dark?'dark':'light');
}
'''

DARK_MODE_CG = '''
/* ── DARK MODE (Cirurgia Geral) ── */
html.dark{
  --bg:#0c0f14!important;--s1:#141820!important;--s2:#0f1520!important;
  --bd:rgba(30,40,64,0.8)!important;--txt:#e2e8f0!important;--mut:#64748b!important;
}
html.dark body{background:#0c0f14!important;color:#e2e8f0!important;}
html.dark header{background:#141820!important;border-bottom-color:#1e2840!important;box-shadow:none!important;}
html.dark .sidebar{background:#141820!important;border-right-color:#1e2840!important;}
html.dark .di{background:#0f1520!important;color:#e2e8f0!important;border-color:#1e2840!important;}
html.dark .hp-staff-bar{background:rgba(20,24,32,.95)!important;border-bottom-color:#1e2840!important;}
html.dark .hp-staff-inp{color:#e2e8f0!important;border-bottom-color:#1e2840!important;}
html.dark .hp-staff-lbl{color:#64748b!important;}
html.dark #theme-toggle{color:#60a5fa!important;border-color:#1e2840!important;}
'''


# ─── SVG icons for buttons ────────────────────────────────────────────────────

SVG_MOON = '<svg style="display:inline-block;width:13px;height:13px;stroke:currentColor;fill:none;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round;vertical-align:-2px"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
SVG_SUN  = '<svg style="display:inline-block;width:13px;height:13px;stroke:currentColor;fill:none;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round;vertical-align:-2px"><circle cx="12" cy="12" r="4"/><line x1="12" y1="2" x2="12" y2="4"/><line x1="12" y1="20" x2="12" y2="22"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="2" y1="12" x2="4" y2="12"/><line x1="20" y1="12" x2="22" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'


# ─── main transformer ─────────────────────────────────────────────────────────

def transform(content, service_label, theme_default, file_type=None):
    hosp_img = extract_hosp_img(content)
    new_splash = make_splash_html(hosp_img, service_label)

    # ── 1. Replace / inject splash ──────────────────────────────────────────
    if 'id="splash"' in content:
        content = re.sub(
            r'<div id="splash">.*?(?=\n<header>|\n\n<header>|\n<div class="layout">|\n<div id="app)',
            new_splash,
            content,
            flags=re.DOTALL
        )
    else:
        content = content.replace('<body>\n', f'<body>\n{new_splash}\n', 1)
        if '<body>\n' + new_splash not in content:
            content = content.replace('<body>', f'<body>\n{new_splash}', 1)

    # ── 2. Inject splash CSS ─────────────────────────────────────────────────
    content = re.sub(r'\s*animation\s*:\s*splashFadeOut[^;]+;', '', content)
    content = re.sub(r'@keyframes\s+splashFadeOut\s*\{[^}]+\}', '', content)
    content = re.sub(r'@keyframes\s+splashRing\s*\{[^}]+\}', '', content)
    content = re.sub(r'@keyframes\s+splashProgress\s*\{[^}]+\}', '', content)
    OLD_SPLASH_CLASSES = (
        r'\.(splash-logo-wrap|splash-logo-ring|splash-logo-img|splash-logo|splash-hospital|'
        r'splash-name|splash-country|splash-divider|splash-dept|splash-title|splash-sub|'
        r'splash-service|splash-bar-wrap|splash-bar|splash-timer|splash-mark|splash-rule|'
        r'splash-inner|splash-hosp-lbl|splash-svc-lbl|splash-pct)'
        r'\s*\{[^}]+\}'
    )
    content = re.sub(OLD_SPLASH_CLASSES, '', content)
    content = content.replace('</style>', SPLASH_CSS + '</style>', 1)

    # ── 3. Theme CSS + staff bar CSS + analysis CSS ──────────────────────────
    if theme_default == 'light':
        extra_css = DARK_MODE_LIGHT_PAGES
        staff_css = staff_bar_css(
            header_h_var='var(--header-h)',
            bg='oklch(97% .01 200)',
            border='oklch(89% .02 200)',
            label_color='var(--muted,#64748b)',
            inp_color='var(--text,#0f172a)',
            inp_border='oklch(85% .02 200)'
        )
    elif theme_default == 'light_cg':
        extra_css = DARK_MODE_CG
        staff_css = staff_bar_css(
            header_h_var='var(--hh)',
            bg='oklch(97% .01 220)',
            border='oklch(88% .03 220)',
            label_color='var(--mut,#64748b)',
            inp_color='var(--txt,#1a1a2e)',
            inp_border='oklch(84% .03 220)'
        )
    elif theme_default == 'dark':
        extra_css = LIGHT_MODE_DARK_PAGES
        staff_css = staff_bar_css()
    else:  # dark_nav (consulta externa)
        extra_css = DARK_MODE_DARK_NAV
        staff_css = staff_bar_css(
            header_h_var='62px',
            bg='rgba(10,22,40,.95)',
            border='rgba(255,255,255,.08)',
            label_color='rgba(148,163,184,.8)',
            inp_color='#e2e8f0',
            inp_border='rgba(255,255,255,.2)'
        )

    content = content.replace('</style>', extra_css + staff_css + ANALYSIS_CSS + '</style>', 1)

    # ── 4. FOUC prevention in <head> ────────────────────────────────────────
    if theme_default in ('light', 'dark_nav', 'light_cg'):
        fouc = FOUC_LIGHT
    else:
        fouc = FOUC_DARK
    content = content.replace('</head>', fouc + '\n</head>', 1)

    # ── 5. Chart.js CDN in <head> (skip cirurgia_geral which already has it) ─
    if file_type != 'cirurgia' and CHARTJS_CDN not in content:
        content = content.replace('</head>', CHARTJS_CDN + '\n</head>', 1)

    # ── 6. Theme toggle button in header ────────────────────────────────────
    if theme_default == 'dark':
        icon = SVG_SUN
        title = 'Mudar para tema claro'
    else:
        icon = SVG_MOON
        title = 'Mudar para tema escuro'

    theme_btn = (
        f'<button id="theme-toggle" onclick="toggleTheme()" title="{title}" '
        f'style="padding:5px 11px;border-radius:4px;cursor:pointer;background:transparent;'
        f'border:1px solid rgba(255,255,255,.2);color:inherit;font-size:.57rem;font-weight:600;'
        f'letter-spacing:.4px;text-transform:uppercase;display:inline-flex;align-items:center;'
        f'gap:5px;white-space:nowrap;">'
        f'{icon} Tema</button>'
    )

    for btn_area in ['<div class="header-right">', '<div class="topbar-right">', '<div class="hr">']:
        if btn_area in content:
            content = content.replace(btn_area, btn_area + '\n    ' + theme_btn, 1)
            break

    # ── 7. Staff bar injection ───────────────────────────────────────────────
    sb = staff_bar_html()
    if theme_default == 'dark_nav':
        content = content.replace('</div>\n\n<div class="sidebar-overlay"',
                                  f'</div>\n{sb}\n<div class="sidebar-overlay"', 1)
        content = content.replace('top: 62px;', 'top: 100px;')
        content = content.replace('min-height: calc(100vh - 62px)', 'min-height: calc(100vh - 100px)')
    else:
        content = content.replace('\n<header>', '\n' + sb + '\n<header>', 1)
        for hvar in ('--header-h', '--hh'):
            content = content.replace(
                f'top:var({hvar});', f'top:calc(var({hvar}) + 38px);')
            content = content.replace(
                f'top: var({hvar});', f'top: calc(var({hvar}) + 38px);')
            content = content.replace(
                f'padding-top:var({hvar})', f'padding-top:calc(var({hvar}) + 38px)')
            content = content.replace(
                f'padding-top: var({hvar})', f'padding-top: calc(var({hvar}) + 38px)')

    # ── 8. Inject JS before </body> ──────────────────────────────────────────
    if theme_default in ('light', 'light_cg'):
        toggle_js = DARK_TOGGLE_JS_LIGHT
    elif theme_default == 'dark':
        toggle_js = LIGHT_TOGGLE_JS_DARK
    else:
        toggle_js = DARK_TOGGLE_JS_DARK_NAV

    # Base JS (splash + staff + theme toggle)
    base_js = '<script>\n' + SPLASH_RING_JS + STAFF_JS + toggle_js + '</script>\n'

    # Analysis JS (common utilities + file-specific patch)
    analysis_patch = get_analysis_js(file_type) if file_type else ''
    if analysis_patch:
        analysis_js = '<script>\n' + COMMON_ANALYSIS_JS + analysis_patch + '</script>\n'
    else:
        analysis_js = ''

    content = content.replace('</body>', base_js + analysis_js + '</body>', 1)

    return content


# ─── execution ────────────────────────────────────────────────────────────────

os.makedirs(OUT, exist_ok=True)

all_files = [(os.path.join(UPLOADS, s), d, l, t, ft) for s, d, l, t, ft in FILES]
all_files += [(s, d, l, t, ft) for s, d, l, t, ft in FILES_EXTRA]

for src_path, out_name, label, theme, ftype in all_files:
    out_path = os.path.join(OUT, out_name)
    print(f'A processar {os.path.basename(src_path)}…')
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = transform(content, label, theme, ftype)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  ✓  {out_name}')

print(f'\n✓ {len(all_files)} ficheiros gerados em {OUT}/')
