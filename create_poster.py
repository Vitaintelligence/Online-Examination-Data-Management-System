from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
ROOT=Path(__file__).resolve().parent; AS=ROOT/'docs'/'assets'; OUT=ROOT/'ExamSphere_Project_Poster.png'
W,H=1500,2400
NAVY=(16,43,86); NAVY2=(24,64,112); BLUE=(40,120,237); CYAN=(54,198,216); INK=(31,56,85); MUTED=(111,130,153); BG=(246,249,253); WHITE=(255,255,255); LINE=(221,231,244); GREEN=(20,157,125); VIOLET=(126,96,228); AMBER=(218,139,37); RED=(217,76,101)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def f(n,b=False):return ImageFont.truetype(BOLD if b else FONT,n)
def rounded(d,box,r,fill,outline=None,w=2):d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=w)
def drawtext(d,xy,text,size=18,color=INK,bold=False,anchor=None):d.text(xy,text,font=f(size,bold),fill=color,anchor=anchor)
def wraptext(d,x,y,text,maxw,size=17,color=MUTED,bold=False,lh=7):
 words=text.split(); lines=[]; line=''
 for word in words:
  test=(line+' '+word).strip()
  if d.textlength(test,font=f(size,bold))<=maxw:line=test
  else:
   if line:lines.append(line)
   line=word
 if line:lines.append(line)
 for line in lines:
  drawtext(d,(x,y),line,size,color,bold);y+=size+lh
 return y

def section(d,x,y,w,h,num,title,accent=BLUE):
 rounded(d,(x,y,x+w,y+h),18,WHITE,LINE,2)
 # header band
 d.rounded_rectangle((x,y,x+w,y+48),radius=18,fill=accent)
 d.rectangle((x,y+27,x+w,y+48),fill=accent)
 drawtext(d,(x+18,y+24),f'{num}. {title.upper()}',22,WHITE,True,'lm')

def bullet(d,x,y,text,width,size=16,color=INK,dot=GREEN,lh=5):
 d.ellipse((x,y+7,x+13,y+20),fill=dot)
 end=wraptext(d,x+26,y,text,width-26,size,color,False,lh)
 return end+7

im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
# Header bar
for yy in range(0,145):
 t=yy/145; col=tuple(int(NAVY[i]*(1-t)+NAVY2[i]*t) for i in range(3)); d.line((0,yy,W,yy),fill=col)
rounded(d,(45,28,128,112),20,WHITE)
drawtext(d,(86,70),'SGT',21,NAVY,True,'mm')
drawtext(d,(153,37),'SGT UNIVERSITY',40,WHITE,True)
drawtext(d,(155,87),'B. TECH CSE (AIML)   •   ACADEMIC YEAR 2026–2027',17,(191,215,245),True)
rounded(d,(1115,35,1450,110),18,(255,255,255,25),outline=(86,128,184),w=2)
drawtext(d,(1282,57),'TA-1 / TA-2',18,NAVY,True,'mm');drawtext(d,(1282,87),'PROJECT SUBMISSION',13,BLUE,True,'mm')
# Hero block
rounded(d,(45,168,1455,460),26,WHITE,LINE,2)
rounded(d,(78,205,144,271),18,BLUE);drawtext(d,(111,238),'E',36,WHITE,True,'mm')
drawtext(d,(170,210),'EXAMSPHERE',58,BLUE,True)
drawtext(d,(82,294),'Online Examination Data Management System',26,NAVY,True)
wraptext(d,82,346,'A secure, centralised platform for examination setup, question-bank management, student assessments, automatic evaluation and result reporting.',620,19,MUTED,False,8)
# screenshot on right
scr=Image.open(AS/'screen_admin.png').convert('RGB');scr.thumbnail((680,415))
rounded(d,(795,190,1425,438),20,(239,245,253),LINE,2)
scr.thumbnail((605,218));im.paste(scr,(805,203))
# Feature strip
features=[('▤','EXAM CONTROL'),('◈','QUESTION BANK'),('✓','AUTO EVALUATION'),('▥','RESULT ANALYTICS'),('⇩','CSV EXPORT')]
for i,(ic,label) in enumerate(features):
 x=60+i*290
 rounded(d,(x,480,x+265,552),15,WHITE,LINE,2);rounded(d,(x+14,496,x+54,536),11,(235,243,255));drawtext(d,(x+34,516),ic,20,BLUE,True,'mm');drawtext(d,(x+70,516),label,14,NAVY,True,'lm')
# Overview, objectives, modules
section(d,45,575,455,290,'1','Project overview',BLUE)
wraptext(d,68,643,'ExamSphere is a browser-based examination management application. It brings administrators and students into one connected workflow, from exam publication to evaluated result records.',408,17,INK,False,7)
wraptext(d,68,780,'Built with Python, Flask and SQLite for an approachable local setup.',408,16,MUTED,False,6)
section(d,520,575,455,290,'2','Objectives',AMBER)
y=642
for b in ['Create and publish online examinations.','Maintain structured MCQ question records.','Provide separate admin and student access.','Evaluate submitted answers automatically.','Store attempts and export result data.']:
 y=bullet(d,545,y,b,410,15,INK,GREEN,4)
section(d,995,575,460,290,'3','Core modules',RED)
mods=[('User access','Registration, login and role checks.'),('Exam management','Create, publish and organise exams.'),('Question bank','Four choices, answer key and marks.'),('Student assessment','Timer, answer choices and progress.'),('Result ledger','Score review, ranking and CSV export.')]
y=640
for h,b in mods:
 drawtext(d,(1020,y),h,16,NAVY,True);y=wraptext(d,1020,y+24,b,400,13,MUTED,False,4)+9
# Architecture and data design
section(d,45,890,710,380,'4','System architecture',BLUE)
arch=Image.open(AS/'architecture.png').convert('RGB');arch.thumbnail((670,285));im.paste(arch,(65,953))
section(d,780,890,675,380,'5','Database design',AMBER)
db=Image.open(AS/'database_model.png').convert('RGB');db.thumbnail((635,285));im.paste(db,(800,953))
# Tech stack
section(d,45,1295,1410,145,'6','Technology stack',NAVY2)
stack=[('PYTHON','Backend'),('FLASK','Web framework'),('SQLITE','Database'),('HTML5','Structure'),('CSS3','Styling'),('JAVASCRIPT','Interactivity'),('WERKZEUG','Security'),('GIT','Version control')]
for i,(name,sub) in enumerate(stack):
 x=70+i*172
 if i>0:d.line((x-9,1360,x-9,1418),fill=LINE,width=2)
 drawtext(d,(x+72,1366),name,15,BLUE if i%2==0 else NAVY,True,'mm');drawtext(d,(x+72,1400),sub,12,MUTED,False,'mm')
# screenshots and output
section(d,45,1465,930,375,'7','Sample interface screens',BLUE)
ss=[('ADMIN OVERVIEW','screen_admin.png'),('STUDENT DASHBOARD','screen_student.png'),('EXAM ATTEMPT','screen_exam.png')]
for i,(label,name) in enumerate(ss):
 x=70+i*295; drawtext(d,(x,1535),label,13,NAVY,True)
 sc=Image.open(AS/name).convert('RGB');sc.thumbnail((270,215));rounded(d,(x-4,1563,x+276,1777),12,(246,249,253),LINE,2);im.paste(sc,(x,1572))
section(d,1000,1465,455,375,'8','Results / output',RED)
y=1540
for b in ['Admin dashboard with system counts.','Published exams visible to students.','MCQ responses scored on submission.','Question-level answer review available.','Submitted attempts ranked by score.','CSV file generated for reporting.']:
 y=bullet(d,1025,y,b,400,15,INK,GREEN,4)
# Team and project details
section(d,45,1865,930,260,'9','Team details',BLUE)
# Table header
rounded(d,(75,1932,935,1976),8,(239,245,251),LINE,1)
drawtext(d,(95,1954),'NAME',13,NAVY,True,'lm');drawtext(d,(420,1954),'REGISTRATION NUMBER',13,NAVY,True,'lm');drawtext(d,(760,1954),'ROLE',13,NAVY,True,'lm')
for i,(name,reg) in enumerate([('Shubham','251302294'),('Bharat','251302272'),('Yash','2513022263')]):
 y=1995+i*39
 drawtext(d,(95,y),name,15,INK,True,'lm');drawtext(d,(420,y),reg,15,INK,False,'lm');drawtext(d,(760,y),'Team member',14,MUTED,False,'lm')
 d.line((75,y+19,935,y+19),fill=LINE,width=1)
section(d,1000,1865,455,260,'10','Next steps',AMBER)
y=1937
for b in ['Run final browser acceptance tests.','Publish the code to the team GitHub repo.','Add the repository URL to team details.','Deploy a public website only after security review.']:
 y=bullet(d,1025,y,b,400,14,INK,AMBER,4)
# Footer block
rounded(d,(45,2150,1455,2350),22,NAVY)
drawtext(d,(80,2190),'SECURE ASSESSMENT. CLEAR INSIGHTS. BETTER OUTCOMES.',23,WHITE,True)
drawtext(d,(80,2243),'Submitted to: Mr. Vivek  •  Trainer, ByteXL',17,(193,216,241),True)
drawtext(d,(80,2288),'Team: ExamSphere',15,(193,216,241))
drawtext(d,(1420,2245),'GITHUB',13,(137,189,246),True,'ra')
drawtext(d,(1420,2280),'MANDATORY LINK',12,(193,216,241),True,'ra')
drawtext(d,(750,2375),'ExamSphere  |  SGT University  |  October 2026',13,MUTED,False,'mm')
im.save(OUT,dpi=(200,200),optimize=True)
print(OUT)
