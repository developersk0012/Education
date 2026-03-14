// script.js - SK Education PDF Generator
// Loaded via <script src="js/script.js"> AFTER jsPDF CDN

function getSKUser(){return JSON.parse(localStorage.getItem('sk_user')||'{}');}

window.downloadCard=function(){
  if(!window.jspdf){alert('PDF library load nahi hua. Page reload karein.');return;}
  const{jsPDF}=window.jspdf;
  const u=getSKUser();
  const doc=new jsPDF({orientation:'portrait',unit:'mm',format:'a5'});
  const w=148,h=210;
  // Background
  doc.setFillColor(13,27,94);doc.rect(0,0,w,h,'F');
  doc.setFillColor(255,255,255);doc.roundedRect(7,7,134,196,8,8,'F');
  // Header
  doc.setFillColor(26,35,126);doc.roundedRect(7,7,134,50,8,8,'F');
  doc.setFillColor(26,35,126);doc.rect(7,43,134,14,'F');
  doc.setDrawColor(255,214,0);doc.setLineWidth(1.5);doc.line(7,57,141,57);
  doc.setTextColor(255,214,0);doc.setFontSize(16);doc.setFont('helvetica','bold');
  doc.text('SK EDUCATION',74,24,{align:'center'});
  doc.setTextColor(255,255,255);doc.setFontSize(8);doc.setFont('helvetica','normal');
  doc.text('Swami Vivekanand Study Point',74,33,{align:'center'});
  doc.text('Direction to Success',74,41,{align:'center'});
  // Title
  doc.setTextColor(26,35,126);doc.setFontSize(11);doc.setFont('helvetica','bold');
  doc.text('STUDENT IDENTITY CARD',74,69,{align:'center'});
  // Avatar
  doc.setFillColor(232,234,246);doc.circle(74,92,17,'F');
  doc.setDrawColor(255,111,0);doc.setLineWidth(1.2);doc.circle(74,92,17,'S');
  doc.setTextColor(26,35,126);doc.setFontSize(22);doc.setFont('helvetica','bold');
  doc.text((u.name||'S').charAt(0).toUpperCase(),74,98,{align:'center'});
  // Name
  doc.setFontSize(14);doc.setFont('helvetica','bold');doc.setTextColor(26,35,126);
  doc.text(u.name||'Student',74,118,{align:'center'});
  doc.setDrawColor(230,230,230);doc.setLineWidth(0.4);doc.line(16,124,132,124);
  // Details
  const rows=[['Email',u.email||'-'],['Mobile',u.phone||'-'],['Class','10th (2026-27)'],
    ['Institution','Swami Vivekanand Study Point'],
    ['Registered',u.registeredAt?new Date(u.registeredAt).toLocaleDateString('en-IN'):'-']];
  let y=133;
  rows.forEach(([label,value])=>{
    doc.setFontSize(7.5);doc.setFont('helvetica','normal');doc.setTextColor(150,150,150);
    doc.text(label,16,y);
    doc.setFont('helvetica','bold');doc.setTextColor(33,33,33);
    const val=value.length>33?value.substring(0,33)+'...':value;
    doc.text(val,16,y+5);y+=13;
  });
  // Footer
  doc.setFillColor(255,111,0);doc.rect(7,188,134,15,'F');
  doc.setTextColor(255,255,255);doc.setFontSize(7);doc.setFont('helvetica','normal');
  doc.text('skeducation.in  •  Valid: Academic Year 2026-27',74,197,{align:'center'});
  doc.save('SK_ID_Card_'+(u.name||'student').replace(/ /g,'_')+'.pdf');
};

window.downloadAccountPDF=function(){
  if(!window.jspdf){alert('PDF library load nahi hua. Page reload karein.');return;}
  const{jsPDF}=window.jspdf;
  const u=getSKUser();
  const doc=new jsPDF({orientation:'portrait',unit:'mm',format:'a4'});
  doc.setFillColor(240,242,255);doc.rect(0,0,210,297,'F');
  doc.setFillColor(26,35,126);doc.rect(0,0,210,45,'F');
  doc.setTextColor(255,214,0);doc.setFontSize(22);doc.setFont('helvetica','bold');
  doc.text('SK EDUCATION',105,18,{align:'center'});
  doc.setTextColor(255,255,255);doc.setFontSize(10);doc.setFont('helvetica','normal');
  doc.text('Swami Vivekanand Study Point – Account Details',105,28,{align:'center'});
  doc.text('Generated on: '+new Date().toLocaleString('en-IN'),105,37,{align:'center'});
  doc.setFillColor(255,255,255);doc.roundedRect(15,55,180,220,8,8,'F');
  doc.setFillColor(232,234,246);doc.circle(105,88,22,'F');
  doc.setDrawColor(255,111,0);doc.setLineWidth(1.5);doc.circle(105,88,22,'S');
  doc.setTextColor(26,35,126);doc.setFontSize(26);doc.setFont('helvetica','bold');
  doc.text((u.name||'S').charAt(0).toUpperCase(),105,95,{align:'center'});
  doc.setFontSize(18);doc.setFont('helvetica','bold');doc.setTextColor(26,35,126);
  doc.text(u.name||'Student',105,122,{align:'center'});
  doc.setFontSize(10);doc.setFont('helvetica','normal');doc.setTextColor(120,120,120);
  doc.text('Class 10th • SK Education Member',105,131,{align:'center'});
  doc.setDrawColor(230,230,240);doc.setLineWidth(0.5);doc.line(30,138,180,138);
  const details=[['Full Name',u.name||'-'],['Email Address',u.email||'-'],
    ['Mobile Number',u.phone||'Not added'],['Class','10th (2026-27)'],
    ['School','Swami Vivekanand Study Point'],['Account Type','Student'],
    ['Registration Date',u.registeredAt?new Date(u.registeredAt).toLocaleString('en-IN'):'-'],
    ['User ID',u.uid?u.uid.substring(0,20)+'...':'-']];
  let dy=152;
  details.forEach(([label,value])=>{
    doc.setFillColor(240,242,255);doc.roundedRect(25,dy-5,70,14,3,3,'F');
    doc.setFontSize(8.5);doc.setFont('helvetica','bold');doc.setTextColor(26,35,126);
    doc.text(label,60,dy+4,{align:'center'});
    doc.setFontSize(9);doc.setFont('helvetica','normal');doc.setTextColor(33,33,33);
    const val=value.length>38?value.substring(0,38)+'...':value;
    doc.text(val,100,dy+4);dy+=17;
  });
  doc.setFillColor(26,35,126);doc.rect(0,277,210,20,'F');
  doc.setTextColor(255,255,255);doc.setFontSize(8);doc.setFont('helvetica','normal');
  doc.text('SK Education • skeducation.in • Auto-generated document',105,289,{align:'center'});
  doc.save('SK_Account_'+(u.name||'student').replace(/ /g,'_')+'.pdf');
};
