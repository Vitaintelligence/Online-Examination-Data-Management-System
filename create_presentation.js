const pptxgen = require('pptxgenjs');
const path = require('path');
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'ExamSphere Team';
pptx.subject = 'TA-1/2 Project Presentation';
pptx.title = 'ExamSphere - Online Examination Data Management System';
pptx.company = 'SGT University';
pptx.lang = 'en-IN';
pptx.theme = { headFontFace: 'Aptos Display', bodyFontFace: 'Aptos', lang: 'en-IN' };
pptx.defineSlideMaster({
  title: 'MASTER', background: { color: 'F5F8FC' },
  objects: [
    { line: { x: 0.48, y: 7.12, w: 12.35, h: 0, line: { color: 'E2EAF4', width: 0.8 } } },
    { text: { text: 'EXAMSPHERE  •  ONLINE EXAMINATION DATA MANAGEMENT SYSTEM', options: { x: 0.5, y: 7.17, w: 7.5, h: 0.16, fontFace: 'Aptos', fontSize: 7, color: '8A9BB0', charSpacing: 1.1, margin: 0 } } },
    { text: { text: 'SGT UNIVERSITY  |  2026–2027', options: { x: 10.1, y: 7.17, w: 2.7, h: 0.16, fontFace: 'Aptos', fontSize: 7, color: '8A9BB0', align: 'right', margin: 0 } } },
  ],
  slideNumber: { x: 12.8, y: 7.15, color: '8A9BB0', fontFace: 'Aptos', fontSize: 7 }
});
const C = { navy:'102B56', blue:'2878ED', cyan:'36C6D8', ink:'263F5C', muted:'74869E', white:'FFFFFF', line:'E4EBF4', pale:'EAF2FF', green:'159A7B', violet:'8163E9', amber:'D98B27', bg:'F5F8FC' };
const A = path.join(__dirname,'docs','assets');
const img = name => path.join(A,name);
function txt(slide,text,x,y,w,h,opt={}) { slide.addText(text,{x,y,w,h,fontFace:opt.fontFace||'Aptos',fontSize:opt.fontSize||12,color:opt.color||C.ink,bold:opt.bold||false,margin:opt.margin===undefined?0:opt.margin,breakLine: false,fit:'shrink',valign:opt.valign||'mid',align:opt.align||'left',paraSpaceAfterPt:opt.paraSpaceAfterPt||0,bullet:opt.bullet,transparency:opt.transparency||0,italic:opt.italic||false,charSpacing:opt.charSpacing||0}); }
function rect(slide,x,y,w,h,fill,rad=0.14,line='E4EBF4') { slide.addShape(pptx.ShapeType.roundRect,{x,y,w,h,rectRadius:rad,fill:{color:fill},line:{color:line,width:0.8},radius:rad}); }
function title(slide,kicker,heading,sub='') { txt(slide,kicker.toUpperCase(),0.62,0.40,10,0.2,{fontSize:8,bold:true,color:C.blue,charSpacing:1.6}); txt(slide,heading,0.62,0.73,12,0.45,{fontSize:25,bold:true,color:C.navy,fontFace:'Aptos Display'}); if(sub) txt(slide,sub,0.64,1.24,11.8,0.34,{fontSize:10,color:C.muted}); }
function card(slide,x,y,w,h,number,heading,body,color=C.blue) { rect(slide,x,y,w,h,C.white); slide.addShape(pptx.ShapeType.roundRect,{x:x+0.18,y:y+0.18,w:0.42,h:0.42,rectRadius:0.08,fill:{color:color,transparency:84},line:{color:color,transparency:100}}); txt(slide,number,x+0.18,y+0.19,0.42,0.37,{fontSize:13,bold:true,color}); txt(slide,heading,x+0.18,y+0.76,w-0.36,0.28,{fontSize:13,bold:true,color:C.navy}); txt(slide,body,x+0.18,y+1.12,w-0.36,h-1.25,{fontSize:9,color:C.muted,valign:'top'}); }
function addImageFit(slide,file,x,y,w,h) { slide.addImage({path:file,x,y,w,h,sizingContain:true}); }

// 1 - Cover
{
 const s=pptx.addSlide(); s.background={color:'F5F8FC'};
 s.addShape(pptx.ShapeType.rect,{x:0,y:0,w:13.333,h:0.16,fill:{color:C.blue},line:{color:C.blue}});
 txt(s,'SGT UNIVERSITY',0.7,0.56,5.5,0.35,{fontSize:18,bold:true,color:C.navy,fontFace:'Aptos Display'});
 txt(s,'B. TECH  •  CSE (AIML)  •  ACADEMIC YEAR 2026–2027',0.72,0.95,7.0,0.22,{fontSize:8,bold:true,color:C.blue,charSpacing:1.2});
 txt(s,'EXAMSPHERE',0.68,1.58,6.5,0.72,{fontSize:40,bold:true,color:C.blue,fontFace:'Aptos Display'});
 txt(s,'Online Examination Data Management System',0.72,2.35,7.0,0.45,{fontSize:19,bold:true,color:C.navy,fontFace:'Aptos Display'});
 txt(s,'Secure assessment. Clear insights. Better outcomes.',0.75,2.88,6.5,0.3,{fontSize:11,color:C.muted,italic:true});
 rect(s,8.0,0.55,4.65,3.0,C.white);
 addImageFit(s,img('screen_admin.png'),8.12,0.70,4.4,2.67);
 txt(s,'PROJECT TEAM',0.75,3.65,2.5,0.22,{fontSize:8,bold:true,color:C.blue,charSpacing:1.4});
 const members=[['Shubham','251302294'],['Bharat','251302272'],['Yash','2513022263']];
 members.forEach((m,i)=>{ const x=0.75+i*2.35; rect(s,x,3.98,2.13,0.82,C.white); txt(s,m[0],x+0.15,4.10,1.83,0.22,{fontSize:13,bold:true,color:C.navy}); txt(s,m[1],x+0.15,4.42,1.83,0.18,{fontSize:9,color:C.muted}); });
 txt(s,'Submitted to: Mr. Vivek  |  Trainer, ByteXL',0.75,5.10,6.5,0.26,{fontSize:10,color:C.ink,bold:true});
 rect(s,0.75,5.68,11.85,0.75,C.navy); txt(s,'BUILT WITH PYTHON + FLASK + SQLITE',1.05,5.88,5.7,0.25,{fontSize:12,bold:true,color:C.white}); txt(s,'TA-1 / TA-2 PROJECT SUBMISSION',8.0,5.89,4.2,0.22,{fontSize:9,bold:true,color:'B7D4F5',align:'right'});
}
// 2 - Problem and solution
{
 const s=pptx.addSlide('MASTER'); title(s,'01 / Context','Why ExamSphere?','A single workspace to connect examination setup, student attempts and academic result records.');
 card(s,0.65,1.95,3.85,2.65,'01','The challenge','Manual assessment workflows can scatter question sets, student responses and result records across separate tools.',C.amber);
 card(s,4.72,1.95,3.85,2.65,'02','Our solution','A browser-based system that connects exam creation, a central question bank, objective assessment and result management.',C.blue);
 card(s,8.78,1.95,3.85,2.65,'03','The outcome','A clearer and more traceable assessment workflow with saved attempts, automatic scoring and exportable result data.',C.green);
 rect(s,0.65,5.05,11.98,1.05,'EAF2FF','0.12','DCE8FA'); txt(s,'CORE IDEA',0.92,5.27,1.1,0.2,{fontSize:8,bold:true,color:C.blue,charSpacing:1.1}); txt(s,'Bring exam administration and student assessment into one consistent system.',0.92,5.58,11.2,0.29,{fontSize:16,bold:true,color:C.navy,fontFace:'Aptos Display'});
}
// 3 - Features
{
 const s=pptx.addSlide('MASTER'); title(s,'02 / Product capabilities','One workflow. Two workspaces.','Role-based features for the people who create assessments and the students who take them.');
 const arr=[['01','Exam management','Create exams and control Draft, Published and Archived states.',C.blue],['02','Question bank','Store MCQs with four choices, answer keys, marks and difficulty.',C.violet],['03','Student workspace','Browse published assessments and access personal attempt history.',C.green],['04','Timed assessment','Answer objective questions with timer and completion progress.',C.amber],['05','Auto evaluation','Calculate scores and preserve question-level response records.',C.cyan],['06','Result reporting','Rank submitted attempts and export structured CSV records.',C.red||'D94C65']];
 arr.forEach((a,i)=>{let x=0.65+(i%3)*4.05,y=1.95+Math.floor(i/3)*2.15;card(s,x,y,3.82,1.82,a[0],a[1],a[2],a[3]);});
}
// 4 - Architecture
{
 const s=pptx.addSlide('MASTER'); title(s,'03 / Engineering','System architecture','A layered design keeps browser presentation, application logic and persistent data responsibilities distinct.');
 addImageFit(s,img('architecture.png'),0.65,1.82,12.0,4.45);
 txt(s,'Browser → Flask routes → database access → SQLite tables',1.1,6.42,11.1,0.25,{fontSize:11,bold:true,color:C.navy,align:'center'});
}
// 5 - Database
{
 const s=pptx.addSlide('MASTER'); title(s,'04 / Data model','Relational database design','Five core tables capture identity, assessment structure, attempts and selected answers.');
 addImageFit(s,img('database_model.png'),0.68,1.75,11.95,4.85);
 txt(s,'Primary keys identify records; foreign keys maintain the relationships between users, exams, questions, attempts and answers.',0.85,6.62,11.65,0.23,{fontSize:9,color:C.muted,align:'center'});
}
// 6 - Workflow
{
 const s=pptx.addSlide('MASTER'); title(s,'05 / Student journey','From exam publication to result review','Every step updates a persistent assessment record.');
 const steps=[['01','Create','Admin defines exam'],['02','Prepare','Add MCQ questions'],['03','Publish','Exam becomes visible'],['04','Attempt','Student answers MCQs'],['05','Submit','Responses are saved'],['06','Review','Score and answers shown']];
 steps.forEach((a,i)=>{let x=0.55+i*2.12;rect(s,x,2.2,1.88,1.55,C.white);s.addShape(pptx.ShapeType.ellipse,{x:x+0.13,y:2.36,w:0.38,h:0.38,fill:{color:C.blue},line:{color:C.blue}});txt(s,a[0],x+0.13,2.38,0.38,0.32,{fontSize:9,bold:true,color:C.white,align:'center'});txt(s,a[1],x+0.13,2.9,1.6,0.25,{fontSize:12,bold:true,color:C.navy});txt(s,a[2],x+0.13,3.23,1.6,0.35,{fontSize:8,color:C.muted,valign:'top'}); if(i<5){s.addShape(pptx.ShapeType.line,{x:x+1.88,y:2.98,w:0.22,h:0,line:{color:'9CB8D9',width:1.4,beginArrowType:'none',endArrowType:'triangle'}})}});
 addImageFit(s,img('screen_exam.png'),1.08,4.25,8.9,2.65);
 rect(s,10.2,4.5,2.45,1.75,'EAF2FF','0.12','DCE8FA'); txt(s,'AUTOMATED',10.42,4.78,1.9,0.18,{fontSize:8,bold:true,color:C.blue,charSpacing:1}); txt(s,'Score calculation',10.42,5.14,2.0,0.28,{fontSize:13,bold:true,color:C.navy}); txt(s,'The submitted responses are compared with the answer key and stored with the final attempt.',10.42,5.55,1.95,0.48,{fontSize:8,color:C.muted,valign:'top'});
}
// 7 - DSA
{
 const s=pptx.addSlide('MASTER'); title(s,'06 / Computer science concepts','Data structures and algorithms in use','The project connects three classic concepts to visible features in the application.');
 const ds=[['FIFO QUEUE','Submission processing','Question-response pairs are enqueued and processed in order during evaluation.',C.blue],['LINEAR SEARCH','Question bank search','Search scans question text and returns matching records without case sensitivity.',C.violet],['MERGE SORT','Result ranking','Submitted attempts are ordered by score using a stable divide-and-merge algorithm.',C.green]];
 ds.forEach((a,i)=>{let x=0.7+i*4.05;rect(s,x,2.0,3.75,2.4,C.white);txt(s,a[0],x+0.22,2.3,3.2,0.25,{fontSize:9,bold:true,color:a[3],charSpacing:1.2});txt(s,a[1],x+0.22,2.78,3.3,0.3,{fontSize:16,bold:true,color:C.navy,fontFace:'Aptos Display'});txt(s,a[2],x+0.22,3.32,3.25,0.72,{fontSize:10,color:C.muted,valign:'top'});});
 rect(s,0.7,4.85,11.85,1.15,C.navy); txt(s,'WHY IT MATTERS',0.98,5.12,1.7,0.18,{fontSize:8,bold:true,color:'8AB8F4',charSpacing:1.3}); txt(s,'The concepts are demonstrated inside real workflows rather than as isolated console programs.',0.98,5.48,10.95,0.26,{fontSize:14,bold:true,color:C.white});
}
// 8 - Security and stack
{
 const s=pptx.addSlide('MASTER'); title(s,'07 / Implementation','Technology and security foundations','A lightweight stack for an academic prototype with clear upgrade paths.');
 const tech=[['PYTHON','Application logic'],['FLASK','Routing + sessions'],['SQLITE','Relational storage'],['HTML / CSS','Responsive interface'],['JAVASCRIPT','Timer + progress'],['WERKZEUG','Password hashing']];
 tech.forEach((a,i)=>{let x=0.72+(i%3)*4.05,y=1.95+Math.floor(i/3)*1.1;rect(s,x,y,3.76,0.86,C.white);txt(s,a[0],x+0.18,y+0.16,1.4,0.2,{fontSize:9,bold:true,color:C.blue,charSpacing:0.8});txt(s,a[1],x+1.5,y+0.16,2.0,0.23,{fontSize:10,bold:true,color:C.navy});});
 txt(s,'SECURITY CONTROLS',0.72,4.38,4.0,0.22,{fontSize:9,bold:true,color:C.blue,charSpacing:1.2});
 const controls=['Salted password hashes','Role-based route protection','Session-bound form tokens','Attempt ownership checks','Parameterized SQL queries','HTTP-only + SameSite cookie'];
 controls.forEach((t,i)=>{let x=0.72+(i%3)*4.05,y=4.8+Math.floor(i/3)*0.57;s.addShape(pptx.ShapeType.ellipse,{x,y:y+0.03,w:0.2,h:0.2,fill:{color:'DDF6EF'},line:{color:'DDF6EF'}});txt(s,'✓',x,y+0.02,0.2,0.2,{fontSize:8,bold:true,color:C.green,align:'center'});txt(s,t,x+0.3,y,3.5,0.24,{fontSize:9,color:C.ink});});
}
// 9 - Screens
{
 const s=pptx.addSlide('MASTER'); title(s,'08 / Interface preview','Designed for clear, focused tasks','Consistent layouts make the administrator and student workspaces feel like one system.');
 const cards=[['ADMIN OVERVIEW','screen_admin.png'],['STUDENT WORKSPACE','screen_student.png'],['QUESTION BANK','screen_questions.png']];
 cards.forEach((a,i)=>{let x=0.62+i*4.2;rect(s,x,1.95,4.0,3.65,C.white);txt(s,a[0],x+0.18,2.13,3.65,0.2,{fontSize:8,bold:true,color:C.blue,charSpacing:1});addImageFit(s,img(a[1]),x+0.12,2.48,3.76,2.35);});
 rect(s,0.62,5.9,12.2,0.62,'EAF2FF','0.1','DCE8FA'); txt(s,'Responsive cards  •  readable status labels  •  compact forms  •  consistent navigation',0.88,6.1,11.7,0.2,{fontSize:10,bold:true,color:C.navy,align:'center'});
}
// 10 - Conclusion/team
{
 const s=pptx.addSlide('MASTER'); title(s,'09 / Wrap-up','A connected foundation for digital assessments','ExamSphere connects examination creation, student attempts and performance data in one browser-based application.');
 rect(s,0.68,1.88,5.55,3.95,C.navy); txt(s,'PROJECT OUTCOME',0.98,2.2,3.5,0.22,{fontSize:8,bold:true,color:'8AB8F4',charSpacing:1.3}); txt(s,'Create.\nAssess.\nUnderstand.',0.98,2.72,4.7,1.65,{fontSize:31,bold:true,color:C.white,fontFace:'Aptos Display',valign:'top'}); txt(s,'A functional academic prototype with persistent assessment data and automatic MCQ evaluation.',0.98,4.85,4.65,0.55,{fontSize:10,color:'C8D9EF',valign:'top'});
 rect(s,6.55,1.88,6.05,3.95,C.white); txt(s,'PROJECT TEAM',6.88,2.2,2.8,0.22,{fontSize:8,bold:true,color:C.blue,charSpacing:1.3});
 const ms=[['Shubham','251302294'],['Bharat','251302272'],['Yash','2513022263']]; ms.forEach((m,i)=>{let y=2.75+i*0.75;txt(s,m[0],6.9,y,2.3,0.25,{fontSize:14,bold:true,color:C.navy});txt(s,m[1],9.65,y,2.2,0.25,{fontSize:11,color:C.muted});});
 txt(s,'Submitted to: Mr. Vivek (ByteXL Trainer)',6.9,5.2,4.8,0.24,{fontSize:9,bold:true,color:C.ink});
 rect(s,0.68,6.05,11.92,0.68,'EAF2FF','0.1','DCE8FA'); txt(s,'GitHub repository: To be published by the team before submission (mandatory)',0.9,6.27,7.7,0.2,{fontSize:9,bold:true,color:C.navy}); txt(s,'Website: Not deployed',9.2,6.27,3.1,0.2,{fontSize:9,color:C.muted,align:'right'});
}

pptx.writeFile({ fileName: path.join(__dirname,'ExamSphere_Project_Presentation.pptx') });
