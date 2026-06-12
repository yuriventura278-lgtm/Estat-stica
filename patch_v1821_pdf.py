#!/usr/bin/env python3
"""Apply PDF improvements to banco_urgencia_v1821.html"""

SRC  = '/home/user/Estat-stica/banco_urgencia_v1821.html'
DEST = '/home/user/Estat-stica/banco_urgencia_v1821.html'

with open(SRC, encoding='utf-8') as f:
    html = f.read()

original_len = len(html)

# ══════════════════════════════════════════════════════════════════════
# 1. pdfHeaderComLogo — logo 26×26 → 16×16, altura do banner 32→28mm
# ══════════════════════════════════════════════════════════════════════
OLD_HEADER = """function pdfHeaderComLogo(doc, titulo, sub) {
  const W = doc.internal.pageSize.getWidth();
  // Fundo azul escuro
  doc.setFillColor(15,43,74); doc.rect(0,0,W,32,'F');
  // Logo circular (se disponível)
  try {
    if(HP_LOGO_B64 && HP_LOGO_B64.startsWith('data:image')) {
      doc.addImage(HP_LOGO_B64,'JPEG',W-30,2,26,26,'','FAST');
    }
  } catch(e) {}
  doc.setTextColor(255,255,255);
  doc.setFontSize(13); doc.setFont('helvetica','bold'); doc.text('Hospital do Prenda',14,11);
  doc.setFontSize(8);  doc.setFont('helvetica','normal'); doc.text('GEPE — Departamento de Estatística Médica',14,17);
  doc.setFontSize(11); doc.setFont('helvetica','bold'); doc.text(titulo,14,24);
  if(sub){ doc.setFontSize(8); doc.setFont('helvetica','normal'); doc.text(sub, W-35, 28, {align:'right'}); }
  doc.setTextColor(0,0,0);
  return 38;
}"""

NEW_HEADER = """function pdfHeaderComLogo(doc, titulo, sub) {
  const W = doc.internal.pageSize.getWidth();
  doc.setFillColor(15,43,74); doc.rect(0,0,W,28,'F');
  try {
    if(HP_LOGO_B64 && HP_LOGO_B64.startsWith('data:image')) {
      doc.addImage(HP_LOGO_B64,'JPEG',W-20,3,16,16,'','FAST');
    }
  } catch(e) {}
  doc.setTextColor(255,255,255);
  doc.setFontSize(12); doc.setFont('helvetica','bold'); doc.text('Hospital do Prenda',14,10);
  doc.setFontSize(7.5); doc.setFont('helvetica','normal'); doc.text('GEPE — Departamento de Estatística Médica',14,16);
  doc.setFontSize(10); doc.setFont('helvetica','bold'); doc.text(titulo,14,22);
  if(sub){ doc.setFontSize(8); doc.setFont('helvetica','normal'); doc.text(sub, W-24, 26, {align:'right'}); }
  doc.setTextColor(0,0,0);
  return 34;
}"""

assert OLD_HEADER in html, "pdfHeaderComLogo not found!"
html = html.replace(OLD_HEADER, NEW_HEADER, 1)
print("OK — pdfHeaderComLogo: logo 26→16mm, banner 32→28mm")

# ══════════════════════════════════════════════════════════════════════
# 2. exportViewPDF — para serviços regulares: melhor resumo demográfico
#    + linha de totais a negrito + totais de procedimentos (peq_cir já
#    está bem, melhora os restantes com tabela de resumo)
# ══════════════════════════════════════════════════════════════════════
OLD_VIEW_TOTALS = """  // Totais
    const m=registos.filter(r=>r.genero==='Masculino'||r.genero==='M').length;
    const f=registos.filter(r=>r.genero==='Feminino'||r.genero==='F').length;
    const m15=registos.filter(r=>r.faixa==='<15').length;
    const M15=registos.filter(r=>r.faixa==='≥15').length;
    const alt=registos.filter(r=>r.destino==='Alta Médica').length;
    const obi=registos.filter(r=>r.destino==='Óbito').length;
    const fy=doc.lastAutoTable.finalY+4;
    doc.setFontSize(8);doc.setTextColor(100,116,139);
    doc.text(`Total: ${registos.length} · Masc.: ${m} · Fem.: ${f} · <15: ${m15} · ≥15: ${M15} · Altas: ${alt} · Óbitos: ${obi}`,14,fy);
  }"""

NEW_VIEW_TOTALS = """  // Totais e resumo demográfico
    const m=registos.filter(r=>r.genero==='Masculino'||r.genero==='M').length;
    const f=registos.filter(r=>r.genero==='Feminino'||r.genero==='F').length;
    const m15=registos.filter(r=>r.faixa==='<15').length;
    const M15=registos.filter(r=>r.faixa==='≥15').length;
    const alt=registos.filter(r=>r.destino==='Alta Médica').length;
    const intern=registos.filter(r=>r.destino==='Internamento'||(r.destino||'').toLowerCase().includes('intern')).length;
    const obi=registos.filter(r=>r.destino==='Óbito').length;
    const transf=registos.filter(r=>(r.destino||'').toLowerCase().includes('transfer')).length;
    const sinist=registos.filter(r=>r.sinist&&r.sinist!=='').length;

    let fy=doc.lastAutoTable.finalY+5;

    // Tabela de resumo demográfico
    doc.setFontSize(9); doc.setFont('helvetica','bold'); doc.setTextColor(15,43,74);
    doc.text('Resumo Demográfico e de Destinos', 14, fy); fy+=4;
    doc.autoTable({ startY:fy,
      head:[['','Masculino','Feminino','Total']],
      body:[
        ['≥ 15 Anos', registos.filter(r=>(r.genero==='Masculino'||r.genero==='M')&&r.faixa!=='<15').length, registos.filter(r=>(r.genero==='Feminino'||r.genero==='F')&&r.faixa!=='<15').length, M15],
        ['< 15 Anos', registos.filter(r=>(r.genero==='Masculino'||r.genero==='M')&&r.faixa==='<15').length, registos.filter(r=>(r.genero==='Feminino'||r.genero==='F')&&r.faixa==='<15').length, m15],
        ['TOTAL', m, f, registos.length]
      ],
      styles:{fontSize:8,font:'helvetica',cellPadding:2.5},
      headStyles:{fillColor:[15,43,74],textColor:255,fontStyle:'bold',halign:'center'},
      bodyStyles:{halign:'center'},
      columnStyles:{0:{fontStyle:'bold',halign:'left'}},
      alternateRowStyles:{fillColor:[248,250,252]},
      margin:{left:14,right:14}, tableWidth:110 });
    fy = doc.lastAutoTable.finalY+3;

    // Tabela de destinos
    const destinos = {};
    registos.forEach(r=>{ const d=(r.destino||'Não especificado'); destinos[d]=(destinos[d]||0)+1; });
    const destRows = Object.entries(destinos).sort((a,b)=>b[1]-a[1]).map(([d,n])=>[d,n,(n/registos.length*100).toFixed(1)+'%']);
    destRows.push(['TOTAL GERAL', registos.length, '100%']);
    doc.autoTable({ startY:fy,
      head:[['Destino','N.º','%']],
      body:destRows,
      styles:{fontSize:8,font:'helvetica',cellPadding:2.5},
      headStyles:{fillColor:[8,145,178],textColor:255,fontStyle:'bold'},
      alternateRowStyles:{fillColor:[248,250,252]},
      margin:{left:14,right:14}, tableWidth:100 });

    if(sinist) {
      fy = doc.lastAutoTable.finalY+3;
      const sinistMap = {};
      registos.forEach(r=>{ if(r.sinist) sinistMap[r.sinist]=(sinistMap[r.sinist]||0)+1; });
      const sinistRows = Object.entries(sinistMap).sort((a,b)=>b[1]-a[1]);
      doc.autoTable({ startY:fy,
        head:[['Sinistralidade','N.º']],
        body:sinistRows,
        styles:{fontSize:8,font:'helvetica',cellPadding:2.5},
        headStyles:{fillColor:[220,38,38],textColor:255,fontStyle:'bold'},
        alternateRowStyles:{fillColor:[254,242,242]},
        margin:{left:14,right:14}, tableWidth:100 });
    }
  }"""

assert OLD_VIEW_TOTALS in html, "exportViewPDF totals block not found!"
html = html.replace(OLD_VIEW_TOTALS, NEW_VIEW_TOTALS, 1)
print("OK — exportViewPDF: tabela demográfica + destinos + sinistralidade")

# ══════════════════════════════════════════════════════════════════════
# 3. exportDashPDF — adicionar secção de procedimentos de enfermagem
#    (actos da peq_cir) e melhorar layout
# ══════════════════════════════════════════════════════════════════════
OLD_DASH_END = """  pdfFooter(doc);
  doc.save(`BU_Resumo_${yy}${mm}${dd}.pdf`);
  showToast('PDF do resumo exportado!');
}"""

NEW_DASH_END = """  // Secção: Procedimentos de Enfermagem (Pequena Cirurgia)
  const regPcr = dayData.registos['peq_cir']||[];
  if(regPcr.length){
    const actosCount = {};
    regPcr.forEach(r=>(r.actos_pcr||[]).forEach(a=>{actosCount[a]=(actosCount[a]||0)+1;}));
    const actosRows = Object.entries(actosCount).sort((a,b)=>b[1]-a[1]).map(([a,n])=>[a,n,(n/regPcr.length*100).toFixed(1)+'%']);
    if(actosRows.length){
      let yA=doc.lastAutoTable.finalY+8;
      if(yA>250){doc.addPage();yA=20;}
      doc.setFontSize(9); doc.setFont('helvetica','bold'); doc.setTextColor(0,0,0);
      doc.text('Procedimentos de Enfermagem — Pequena Cirurgia', 14, yA); yA+=4;
      doc.autoTable({startY:yA,
        head:[['Procedimento / Acto','N.º de Casos','%']],
        body:actosRows,
        styles:{fontSize:8,font:'helvetica',cellPadding:2.5},
        headStyles:{fillColor:[8,145,178],textColor:255,fontStyle:'bold'},
        alternateRowStyles:{fillColor:[240,249,255]},margin:{left:14,right:14}});
    }
  }

  pdfFooter(doc);
  doc.save(`BU_Resumo_${yy}${mm}${dd}.pdf`);
  showToast('PDF do resumo exportado!');
}"""

assert OLD_DASH_END in html, "exportDashPDF end block not found!"
html = html.replace(OLD_DASH_END, NEW_DASH_END, 1)
print("OK — exportDashPDF: secção procedimentos de enfermagem adicionada")

# ══════════════════════════════════════════════════════════════════════
# 4. exportViewPDF (peq_cir) — adicionar linha de totais nas actos
# ══════════════════════════════════════════════════════════════════════
OLD_ACTOS_ROWS = """    const actosRows = Object.entries(actosCount).sort((a,b)=>b[1]-a[1]).map(([a,n])=>[a,n]);
    if(actosRows.length) {
      y = doc.lastAutoTable.finalY + 8;
      doc.setFontSize(9); doc.setFont('helvetica','bold');
      doc.text('Resumo — Actos e Procedimentos Realizados', 14, y); y+=5;
      doc.autoTable({
        startY:y,
        head:[['Acto / Procedimento','N.º de Casos']],
        body:actosRows,
        styles:{fontSize:8,font:'helvetica',cellPadding:2.5},
        headStyles:{fillColor:[8,145,178],textColor:255,fontStyle:'bold',fontSize:7.5},
        alternateRowStyles:{fillColor:[248,250,252]},
        margin:{left:14,right:14}
      });
    }"""

NEW_ACTOS_ROWS = """    const totalActos = Object.values(actosCount).reduce((a,b)=>a+b,0);
    const actosRows = Object.entries(actosCount).sort((a,b)=>b[1]-a[1]).map(([a,n])=>[a,n,(n/registos.length*100).toFixed(1)+'%']);
    actosRows.push(['TOTAL DE ACTOS', totalActos, '']);
    if(actosRows.length) {
      y = doc.lastAutoTable.finalY + 8;
      doc.setFontSize(9); doc.setFont('helvetica','bold'); doc.setTextColor(15,43,74);
      doc.text('Resumo — Procedimentos de Enfermagem Realizados', 14, y); y+=5;
      doc.setTextColor(0,0,0);
      doc.autoTable({
        startY:y,
        head:[['Procedimento / Acto','N.º de Casos','% Doentes']],
        body:actosRows,
        styles:{fontSize:8,font:'helvetica',cellPadding:2.5},
        headStyles:{fillColor:[8,145,178],textColor:255,fontStyle:'bold'},
        alternateRowStyles:{fillColor:[240,249,255]},
        bodyStyles:{},
        didParseCell:function(data){ if(data.row.index===actosRows.length-1){ data.cell.styles.fontStyle='bold'; data.cell.styles.fillColor=[15,43,74]; data.cell.styles.textColor=255; } },
        margin:{left:14,right:14}
      });
    }"""

assert OLD_ACTOS_ROWS in html, "peq_cir actos rows block not found!"
html = html.replace(OLD_ACTOS_ROWS, NEW_ACTOS_ROWS, 1)
print("OK — exportViewPDF (peq_cir): totais de procedimentos com % e linha total")

# ══════════════════════════════════════════════════════════════════════
# 5. exportViewPDF header — melhorar exibição da equipa
# ══════════════════════════════════════════════════════════════════════
OLD_VIEW_HEADER = """  // Cabeçalho do dia com equipa completa
  const cb=dayData.cabecalhos[svId]||{};
  const medicos = (cb.medicos||[]).filter(Boolean).join(', ')||'—';
  const chefe = cb.chefe||'—';
  const supClin = cb.sup_clin||'—';
  const supEnf = cb.sup_enf||'—';
  doc.setFontSize(8);doc.setTextColor(100,116,139);
  doc.text(`Chefe de Equipa: ${chefe}   Médicos: ${medicos}`,14,y); y+=5;
  doc.text(`Supervisor Clínico: ${supClin}   Supervisor Enfermagem: ${supEnf}`,14,y); y+=7;"""

NEW_VIEW_HEADER = """  // Cabeçalho — equipa do dia em caixa
  const cb=dayData.cabecalhos[svId]||{};
  const medicos = (cb.medicos||[]).filter(Boolean).join(', ')||'—';
  const chefe = cb.chefe||'—';
  const supClin = cb.sup_clin||'—';
  const supEnf = cb.sup_enf||'—';
  const W2=doc.internal.pageSize.getWidth();
  doc.setFillColor(236,242,255); doc.roundedRect(14,y,W2-28,22,2,2,'F');
  doc.setDrawColor(180,200,240); doc.roundedRect(14,y,W2-28,22,2,2,'S');
  doc.setFontSize(7.5); doc.setFont('helvetica','bold'); doc.setTextColor(15,43,74);
  doc.text('EQUIPA DE BANCO',16,y+6);
  doc.setFont('helvetica','normal'); doc.setFontSize(8); doc.setTextColor(0,0,0);
  doc.text(`Chefe de Equipa: ${chefe}`,16,y+12);
  doc.text(`Supervisor Clínico: ${supClin}   Supervisor Enf.ª: ${supEnf}`,16,y+17);
  doc.text(`Médicos: ${medicos}`,W2/2,y+12);
  y+=26;"""

assert OLD_VIEW_HEADER in html, "exportViewPDF header block not found!"
html = html.replace(OLD_VIEW_HEADER, NEW_VIEW_HEADER, 1)
print("OK — exportViewPDF: equipa em caixa visual")

# ══════════════════════════════════════════════════════════════════════
# 6. exportDashPDF — melhorar tabela de serviços com faixas etárias
# ══════════════════════════════════════════════════════════════════════
OLD_DASH_SV = """  y=doc.lastAutoTable.finalY+8;
  const svRows=[];
  SERVICOS.forEach(sv=>{
    const rr=dayData.registos[sv.id]||[];if(!rr.length)return;
    const m=rr.filter(r=>r.genero==='Masculino'||r.genero==='M').length;
    const alt=rr.filter(r=>r.destino==='Alta Médica').length;
    const obi=rr.filter(r=>r.destino==='Óbito').length;
    svRows.push([sv.label,rr.length,m,rr.length-m,alt,obi]);
  });
  if(svRows.length){
    doc.autoTable({startY:y,head:[['Serviço','Atend.','Masc.','Fem.','Altas','Óbitos']],body:svRows,
      styles:{fontSize:8,font:'helvetica',cellPadding:2.5},
      headStyles:{fillColor:[15,43,74],textColor:255,fontStyle:'bold',fontSize:7.5},
      alternateRowStyles:{fillColor:[248,250,252]},margin:{left:14,right:14}});
  }"""

NEW_DASH_SV = """  y=doc.lastAutoTable.finalY+8;
  const svRows=[];
  SERVICOS.forEach(sv=>{
    const rr=dayData.registos[sv.id]||[];if(!rr.length)return;
    const m=rr.filter(r=>r.genero==='Masculino'||r.genero==='M').length;
    const f=rr.length-m;
    const men15=rr.filter(r=>r.faixa==='<15').length;
    const mai15=rr.length-men15;
    const alt=rr.filter(r=>r.destino==='Alta Médica').length;
    const intern=rr.filter(r=>(r.destino||'').toLowerCase().includes('intern')).length;
    const obi=rr.filter(r=>r.destino==='Óbito').length;
    svRows.push([sv.label,rr.length,m,f,mai15,men15,alt,intern,obi]);
  });
  if(svRows.length){
    doc.setFontSize(9); doc.setFont('helvetica','bold'); doc.text('Atendimentos por Serviço',14,y); y+=4;
    doc.autoTable({startY:y,head:[['Serviço','Total','Masc.','Fem.','≥15','<15','Altas','Intern.','Óbitos']],body:svRows,
      styles:{fontSize:7.5,font:'helvetica',cellPadding:2},
      headStyles:{fillColor:[15,43,74],textColor:255,fontStyle:'bold',fontSize:7,halign:'center'},
      bodyStyles:{halign:'center'},
      columnStyles:{0:{halign:'left',fontStyle:'bold'}},
      alternateRowStyles:{fillColor:[248,250,252]},margin:{left:14,right:14}});
  }"""

assert OLD_DASH_SV in html, "exportDashPDF svRows block not found!"
html = html.replace(OLD_DASH_SV, NEW_DASH_SV, 1)
print("OK — exportDashPDF: tabela de serviços com faixas etárias e internamentos")

# ══════════════════════════════════════════════════════════════════════
# 7. exportServiceDayPDF — ajustar y inicial pois header ficou menor
# ══════════════════════════════════════════════════════════════════════
# pdfHeaderComLogo now returns 34 instead of 38, autoTable will adjust

# ══════════════════════════════════════════════════════════════════════
# VERIFICAR e GRAVAR
# ══════════════════════════════════════════════════════════════════════
with open(DEST, 'w', encoding='utf-8') as f:
    f.write(html)

new_len = len(html)
print(f"\nDone. {original_len:,} → {new_len:,} chars (+{new_len-original_len:,})")
print(f"Saved to: {DEST}")
