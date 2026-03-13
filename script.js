// js/script.js - SK Education PDF Generator
// Requires jsPDF loaded before this file

function getSKUser() {
  return JSON.parse(localStorage.getItem('sk_user') || '{}');
}

/* ────── STUDENT ID CARD ────── */
window.downloadCard = function () {
  if (!window.jspdf) { alert('PDF library load nahi hua. Page reload karein.'); return; }
  const { jsPDF } = window.jspdf;
  const u = getSKUser();
  const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a5' });
  const W = 148, H = 210;

  doc.setFillColor(13,27,94); doc.rect(0,0,W,H,'F');
  doc.setFillColor(255,255,255); doc.roundedRect(7,7,134,196,8,8,'F');
  doc.setFillColor(26,35,126); doc.roundedRect(7,7,134,50,8,8,'F');
  doc.setFillColor(26,35,126); doc.rect(7,43,134,14,'F');
  doc.setDrawColor(255,214,0); doc.setLineWidth(1.5); doc.line(7,57,141,57);

  doc.setTextColor(255,214,0); doc.setFontSize(16); doc.setFont('helvetica','bold');
  doc.text('SK EDUCATION',74,24,{align:'center'});
  doc.setTextColor(255,255,255); doc.setFontSize(8); doc.setFont('helvetica','normal');
  doc.text('Swami Vivekanand Study Point',74,33,{align:'center'});
  doc.text('Direction to Success',74,41,{align:'center'});

  doc.setTextColor(26,35,126); doc.setFontSize(11); doc.setFont('helvetica','bold');
  doc.text('STUDENT IDENTITY CARD',74,69,{align:'center'});

  doc.setFillColor(232,234,246); doc.circle(74,93,17,'F');
  doc.setDrawColor(255,111,0); doc.setLineWidth(1.2); doc.circle(74,93,17,'S');
  doc.setTextColor(26,35,126); doc.setFontSize(22); doc.setFont('helvetica','bold');
  doc.text((u.name||'S').charAt(0).toUpperCase(),74,99,{align:'center'});

  doc.setFontSize(14); doc.text(u.name||'Student',74,119,{align:'center'});

  doc.setDrawColor(230,230,230); doc.setLineWidth(0.4); doc.line(16,125,132,125);

  const rows=[
    ['Email', u.email||'-'],
    ['Mobile', u.phone||'Not added'],
    ['Class', '10th (2026-27)'],
    ['Institution', 'Swami Vivekanand Study Point'],
    ['Registered', u.registeredAt?new Date(u.registeredAt).toLocaleDateString('en-IN'):'-'],
  ];
  let y=134;
  rows.forEach(([lbl,val])=>{
    doc.setFontSize(7.5); doc.setFont('helvetica','normal'); doc.setTextColor(150,150,150); doc.text(lbl,16,y);
    doc.setFont('helvetica','bold'); doc.setTextColor(33,33,33);
    doc.text(val.length>33?val.substring(0,33)+'...':val, 16, y+5);
    y+=13;
  });

  doc.setFillColor(255,111,0); doc.rect(7,188,134,15,'F');
  doc.setTextColor(255,255,255); doc.setFontSize(7); doc.setFont('helvetica','normal');
  doc.text('skeducation.in  •  Valid: Academic Year 2026-27',74,197,{align:'center'});
  doc.save('SK_ID_Card_'+(u.name||'student').replace(/ /g,'_')+'.pdf');
};

/* ────── ACCOUNT DETAILS PDF ────── */
window.downloadAccountPDF = function () {
  if (!window.jspdf) { alert('PDF library load nahi hua. Page reload karein.'); return; }
  const { jsPDF } = window.jspdf;
  const u = getSKUser();
  const doc = new jsPDF({ orientation:'portrait', unit:'mm', format:'a4' });

  doc.setFillColor(240,242,255); doc.rect(0,0,210,297,'F');
  doc.setFillColor(26,35,126); doc.rect(0,0,210,46,'F');
  doc.setTextColor(255,214,0); doc.setFontSize(22); doc.setFont('helvetica','bold');
  doc.text('SK EDUCATION',105,18,{align:'center'});
  doc.setTextColor(255,255,255); doc.setFontSize(10); doc.setFont('helvetica','normal');
  doc.text('Swami Vivekanand Study Point – Account Details',105,29,{align:'center'});
  doc.text('Generated: '+new Date().toLocaleString('en-IN'),105,38,{align:'center'});

  doc.setFillColor(255,255,255); doc.roundedRect(15,55,180,215,8,8,'F');
  doc.setDrawColor(200,205,240); doc.setLineWidth(0.5); doc.roundedRect(15,55,180,215,8,8,'S');

  doc.setFillColor(232,234,246); doc.circle(105,88,22,'F');
  doc.setDrawColor(255,111,0); doc.setLineWidth(1.5); doc.circle(105,88,22,'S');
  doc.setTextColor(26,35,126); doc.setFontSize(26); doc.setFont('helvetica','bold');
  doc.text((u.name||'S').charAt(0).toUpperCase(),105,95,{align:'center'});

  doc.setFontSize(18); doc.text(u.name||'Student',105,122,{align:'center'});
  doc.setFontSize(10); doc.setFont('helvetica','normal'); doc.setTextColor(120,120,120);
  doc.text('Class 10th  •  SK Education Member',105,131,{align:'center'});

  doc.setDrawColor(230,230,240); doc.setLineWidth(0.5); doc.line(30,138,180,138);

  const details=[
    ['Full Name',     u.name||'-'],
    ['Email',         u.email||'-'],
    ['Mobile',        u.phone||'Not added'],
    ['Class',         '10th (2026-27)'],
    ['School',        'Swami Vivekanand Study Point'],
    ['Account Type',  'Student'],
    ['Member Since',  u.registeredAt?new Date(u.registeredAt).toLocaleString('en-IN'):'-'],
    ['User ID',       u.uid?u.uid.substring(0,22)+'...':'-'],
  ];
  let dy=150;
  details.forEach(([lbl,val])=>{
    doc.setFillColor(240,242,255); doc.roundedRect(25,dy-5,68,14,3,3,'F');
    doc.setFontSize(8.5); doc.setFont('helvetica','bold'); doc.setTextColor(26,35,126);
    doc.text(lbl,59,dy+4,{align:'center'});
    doc.setFontSize(9); doc.setFont('helvetica','normal'); doc.setTextColor(33,33,33);
    doc.text(val.length>36?val.substring(0,36)+'...':val, 98, dy+4);
    dy+=17;
  });

  doc.setFillColor(26,35,126); doc.rect(0,277,210,20,'F');
  doc.setTextColor(255,255,255); doc.setFontSize(8); doc.setFont('helvetica','normal');
  doc.text('SK Education  •  skeducation.in  •  Auto-generated document',105,289,{align:'center'});
  doc.save('SK_Account_'+(u.name||'student').replace(/ /g,'_')+'.pdf');
};
