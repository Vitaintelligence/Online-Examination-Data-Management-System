from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import textwrap, math, random

ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'docs'/'assets'
ASSETS.mkdir(parents=True,exist_ok=True)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def font(sz,bold=False): return ImageFont.truetype(BOLD if bold else FONT,sz)
NAVY=(16,43,86); BLUE=(40,120,237); CYAN=(54,198,216); INK=(29,54,84); MUTED=(119,137,160); BG=(245,248,252); LINE=(228,236,246); WHITE=(255,255,255); GREEN=(19,168,137); VIOLET=(129,99,233); AMBER=(217,139,39); RED=(217,76,101)

def rr(d,box,r,fill,outline=None,width=1): d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)
def txt(d,xy,s,sz=18,fill=INK,bold=False,anchor=None): d.text(xy,s,font=font(sz,bold),fill=fill,anchor=anchor)
def wrap(d,xy,s,width,sz=16,fill=MUTED,bold=False,spacing=5):
    words=s.split(); lines=[]; line=''
    for word in words:
        test=(line+' '+word).strip()
        if d.textlength(test,font=font(sz,bold))<=width: line=test
        else:
            if line: lines.append(line)
            line=word
    if line: lines.append(line)
    d.multiline_text(xy,'\n'.join(lines),font=font(sz,bold),fill=fill,spacing=spacing)
    return len(lines)*(sz+spacing)

def base_screen(title,crumb,view='admin'):
    im=Image.new('RGB',(1440,900),BG); d=ImageDraw.Draw(im)
    d.rectangle((0,0,1440,78),fill=WHITE); d.line((0,77,1440,77),fill=LINE,width=2)
    rr(d,(54,20,91,57),12,BLUE); txt(d,(72,38),'E',21,WHITE,True,'mm'); txt(d,(104,19),'examsphere',24,NAVY,True); txt(d,(105,46),'EXAMINATION MANAGEMENT',9,MUTED,True)
    nav=[('Overview','admin'),('Exams','exams'),('Question bank','questions'),('Results','results')]
    xx=525
    for label,key in nav:
        txt(d,(xx,39),label,13,BLUE if key==view else MUTED,True,'mm'); xx+=135
    rr(d,(1260,22,1294,56),17,(232,241,255)); txt(d,(1277,39),'A',13,BLUE,True,'mm'); txt(d,(1305,39),'Administrator',11,INK,True,'lm')
    txt(d,(66,126),crumb.upper(),10,(106,136,173),True); txt(d,(66,165),title,32,NAVY,True)
    return im,d

def metric(d,x,y,w,label,value,desc,color=BLUE,icon='▤'):
    rr(d,(x,y,x+w,y+145),15,WHITE,LINE,2); rr(d,(x+18,y+18,x+55,y+55),11,(238,245,255)); txt(d,(x+36,y+36),icon,18,color,True,'mm')
    txt(d,(x+18,y+76),label,12,MUTED,True); vsize=17 if len(str(value))>4 else 25; txt(d,(x+18,y+99),value,vsize,NAVY,True); txt(d,(x+18,y+132),desc,8,(146,160,180))

def screenshot_admin():
    im,d=base_screen('Control centre.','ADMINISTRATION / OVERVIEW','admin')
    wrap(d,(68,208),'Manage assessments, keep the question bank organised and review student performance.',760,13,MUTED)
    rr(d,(1180,124,1372,166),10,BLUE); txt(d,(1276,145),'+  Create an exam',12,WHITE,True,'mm')
    metric(d,66,240,310,'Registered students','128','Student accounts',BLUE,'♙'); metric(d,395,240,310,'Total examinations','12','Published and draft',VIOLET,'▤'); metric(d,724,240,310,'Question bank','246','Assessment questions',GREEN,'◈'); metric(d,1053,240,310,'Completed attempts','384','Submitted assessments',AMBER,'✓')
    quick=[('Exam management','Create, publish and organise assessments.'),('Question bank','Add, review and search MCQ records.'),('Results & analytics','Sort performance data and export CSV.')]
    for i,(a,b) in enumerate(quick):
        x=66+i*438; rr(d,(x,412,x+420,494),13,WHITE,LINE,2); rr(d,(x+16,430,x+54,468),11,(238,245,255)); txt(d,(x+35,449),['▤','◈','▥'][i],17,BLUE,True,'mm'); txt(d,(x+72,439),a,13,INK,True); txt(d,(x+72,464),b,10,MUTED); txt(d,(x+393,451),'↗',16,(126,158,196),True,'mm')
    txt(d,(67,548),'Latest submissions',18,NAVY,True); txt(d,(68,574),'Most recent activity across all examinations.',10,MUTED)
    rr(d,(66,602,1372,850),14,WHITE,LINE,2); d.rectangle((68,604,1370,642),fill=(248,250,253))
    heads=['STUDENT','EXAMINATION','SUBMITTED','SCORE','STATUS']; xs=[90,340,800,1100,1250]
    for x,h in zip(xs,heads): txt(d,(x,624),h,9,(137,153,174),True,'lm')
    rows=[('Aarav Sharma','Database Management Systems','30 Oct 2026 · 11:24','25 / 30','Submitted'),('Ishita Verma','Database Management Systems','30 Oct 2026 · 10:58','28 / 30','Submitted'),('Rohan Mehta','Python Fundamentals','30 Oct 2026 · 10:41','21 / 25','Submitted')]
    for j,row in enumerate(rows):
        yy=684+j*54; d.line((68,yy-17,1370,yy-17),fill=LINE,width=1)
        for k,(x,v) in enumerate(zip(xs,row)):
            if k==4:
                rr(d,(x-2,yy-13,x+76,yy+13),12,(230,248,243)); txt(d,(x+37,yy),v,8,GREEN,True,'mm')
            else: txt(d,(x,yy),v,10,INK if k==0 else MUTED,k==0,'lm')
    return im

def screenshot_student():
    im,d=base_screen('Good to see you, Aarav.','STUDENT WORKSPACE','student')
    wrap(d,(68,208),'Pick up where you left off or explore an available assessment.',800,13,MUTED)
    metric(d,66,240,405,'Available exams','3','Published assessments',BLUE,'▣'); metric(d,493,240,405,'Submitted attempts','2','Recent activity',VIOLET,'✓'); metric(d,920,240,443,'Next step','Stay ready','Review instructions before starting',GREEN,'◷')
    txt(d,(66,432),'Available examinations',18,NAVY,True); txt(d,(66,460),'Published assessments ready for you.',10,MUTED)
    exams=[('Database Management Systems','SQL, relational concepts, keys, normalization and transactions.','30 min','30 marks'),('Python Fundamentals','Core Python syntax, functions, collections and problem solving.','25 min','25 marks'),('Computer Networks','Network models, protocols, addressing and data transmission.','40 min','40 marks')]
    for i,(title,desc,dur,marks) in enumerate(exams):
        x=66+i*438; rr(d,(x,490,x+420,828),15,WHITE,LINE,2); rr(d,(x+20,514,x+57,551),11,(238,245,255)); txt(d,(x+38,533),'▤',17,BLUE,True,'mm'); rr(d,(x+294,521,x+395,545),12,(230,248,243)); txt(d,(x+345,533),'PUBLISHED',8,GREEN,True,'mm'); txt(d,(x+20,584),title,15,NAVY,True); wrap(d,(x+20,612),desc,370,10,MUTED,False,4); d.line((x+20,696,x+395,696),fill=LINE,width=1); txt(d,(x+22,721),'◷  '+dur,10,MUTED,True); txt(d,(x+150,721),'◎  '+marks,10,MUTED,True); rr(d,(x+20,762,x+395,805),10,BLUE); txt(d,(x+208,784),'Start examination  →',11,WHITE,True,'mm')
    return im

def screenshot_questions():
    im,d=base_screen('Question bank.','ADMINISTRATION / CONTENT','questions')
    wrap(d,(68,208),'Build a reusable library of objective questions for each examination.',800,13,MUTED)
    rr(d,(66,240,617,850),15,WHITE,LINE,2); txt(d,(90,273),'Add a question',17,NAVY,True); txt(d,(90,298),'Four options and one correct answer.',10,MUTED)
    y=334
    fields=[('EXAMINATION','Database Management Systems'),('QUESTION TEXT','Which SQL command is used to retrieve data from a table?'),('OPTION A','GET'),('OPTION B','SELECT'),('OPTION C','FETCH ALL'),('OPTION D','OPEN'),('CORRECT OPTION','B      •      MARKS 5')]
    for i,(label,val) in enumerate(fields):
        txt(d,(91,y),label,8,(97,119,145),True); rr(d,(90,y+14,592,y+48),7,(250,252,254),LINE,1); txt(d,(103,y+31),val,9,INK,False,'lm'); y+=67 if i<1 else 58
    rr(d,(90,790,592,831),9,BLUE); txt(d,(341,810),'Add to question bank  →',11,WHITE,True,'mm')
    rr(d,(642,240,1372,850),15,WHITE,LINE,2); txt(d,(668,274),'Question records',17,NAVY,True); txt(d,(668,298),'Search and maintain questions by their content.',10,MUTED)
    questions=[('Which SQL command is used to retrieve data from a table?','DBMS  ·  EASY  ·  5 MARKS'),('Which key uniquely identifies each row in a relation?','DBMS  ·  EASY  ·  5 MARKS'),('What does ACID stand for in transaction processing?','DBMS  ·  MEDIUM  ·  5 MARKS'),('Which normal form removes partial dependencies?','DBMS  ·  MEDIUM  ·  5 MARKS'),('Which SQL clause filters grouped records?','DBMS  ·  MEDIUM  ·  5 MARKS')]
    for i,(q,meta) in enumerate(questions):
        yy=350+i*90; d.line((667,yy-9,1345,yy-9),fill=LINE,width=1); txt(d,(668,yy+9),meta,8,(130,151,176),True); wrap(d,(668,yy+33),q,600,10,INK,True,3); rr(d,(1280,yy+1,1340,yy+25),11,(230,248,243)); txt(d,(1310,yy+13),'ACTIVE',7,GREEN,True,'mm')
    return im

def screenshot_exam():
    im,d=base_screen('Database Management Systems','ONLINE ASSESSMENT','student')
    rr(d,(66,208,1372,292),14,NAVY); txt(d,(90,231),'ONLINE ASSESSMENT',9,(156,197,238),True); txt(d,(90,265),'Database Management Systems',20,WHITE,True); txt(d,(1337,247),'IN PROGRESS',8,(255,223,160),True,'rm')
    questions=[('QUESTION 01 OF 06','Which SQL command is used to retrieve data from a table?', ['GET','SELECT','FETCH ALL','OPEN']),('QUESTION 02 OF 06','Which key uniquely identifies each row in a relation?',['Foreign key','Candidate attribute','Primary key','Composite view'])]
    for j,(num,q,opts) in enumerate(questions):
        x=66;y=317+j*250;rr(d,(x,y,1010,y+226),14,WHITE,LINE,2);txt(d,(x+22,y+25),num,8,(107,136,173),True);rr(d,(919,y+13,981,y+38),10,(238,245,255));txt(d,(950,y+25),'5 MARKS',7,BLUE,True,'mm');wrap(d,(x+22,y+65),q,840,13,INK,True,4)
        for k,opt in enumerate(opts):
            yy=y+113+k*25; rr(d,(x+22,yy,x+920,yy+22),6,(239,246,255) if k==1 else (252,253,255),BLUE if k==1 else LINE,1); rr(d,(x+31,yy+4,x+48,yy+21),8,BLUE if k==1 else (242,245,249));txt(d,(x+39,yy+12),chr(65+k),7,WHITE if k==1 else MUTED,True,'mm');txt(d,(x+59,yy+12),opt,8,INK if k==1 else MUTED,False,'lm')
    rr(d,(1032,317,1372,478),14,WHITE,LINE,2);txt(d,(1054,344),'TIME ALLOWED',8,(110,137,171),True);txt(d,(1054,395),'24:18',33,NAVY,True);txt(d,(1054,430),'Keep an eye on your remaining time.',8,MUTED)
    rr(d,(1032,493,1372,675),14,WHITE,LINE,2);txt(d,(1054,522),'Assessment progress',11,INK,True);rr(d,(1054,547,1350,555),4,(235,241,249));rr(d,(1054,547,1153,555),4,BLUE);txt(d,(1054,578),'2 of 6 answered',8,MUTED)
    for i in range(6): rr(d,(1054+i*46,603,1082+i*46,631),7,(238,245,255) if i<2 else WHITE,BLUE if i<2 else LINE,1);txt(d,(1068+i*46,617),str(i+1),8,BLUE if i<2 else MUTED,True,'mm')
    rr(d,(1032,691,1372,850),14,WHITE,LINE,2);txt(d,(1054,718),'Before you submit',10,INK,True);wrap(d,(1054,744),'Review your selections. Once submitted, your responses are evaluated and saved to the result ledger.',282,9,MUTED,False,4)
    rr(d,(66,835,1010,878),10,BLUE);txt(d,(538,856),'Submit assessment  →',11,WHITE,True,'mm')
    return im

def screenshot_results():
    im,d=base_screen('Results & performance.','ADMINISTRATION / PERFORMANCE','results')
    wrap(d,(68,208),'Review submitted attempts, compare scores and export structured result records.',820,13,MUTED)
    rr(d,(1160,124,1372,166),10,BLUE);txt(d,(1266,145),'↓  Export CSV',11,WHITE,True,'mm')
    metric(d,66,240,625,'Submitted assessments','384','Completed attempts in result ledger',BLUE,'▥');metric(d,715,240,648,'Highest score','29','Sorted with merge sort (descending)',GREEN,'↗')
    rr(d,(66,420,1372,850),15,WHITE,LINE,2);d.rectangle((68,422,1370,466),fill=(248,250,253));heads=[('RANK',90),('STUDENT',190),('EXAMINATION',525),('SCORE',1000),('SUBMITTED',1145)]
    for h,x in heads: txt(d,(x,444),h,9,(137,153,174),True,'lm')
    rows=[('01','Ishita Verma','Database Management Systems','29 / 30','30 Oct 2026 · 10:58'),('02','Aarav Sharma','Database Management Systems','25 / 30','30 Oct 2026 · 11:24'),('03','Rohan Mehta','Python Fundamentals','21 / 25','30 Oct 2026 · 10:41'),('04','Diya Kapoor','Computer Networks','38 / 40','29 Oct 2026 · 16:12')]
    for i,row in enumerate(rows):
        y=520+i*77;d.line((68,y-20,1370,y-20),fill=LINE,width=1)
        for j,(v,(_,x)) in enumerate(zip(row,heads)):
            txt(d,(x,y),v,10,NAVY if j==1 else MUTED,j==1,'lm')
        rr(d,(990,y-10,1100,y-4),3,(237,242,249));rr(d,(990,y-10,990+int(110*[.96,.83,.84,.95][i]),y-4),3,BLUE)
    return im

# Draw a clean layered architecture diagram.
def architecture():
    im=Image.new('RGB',(1500,560),WHITE);d=ImageDraw.Draw(im)
    txt(d,(50,34),'SYSTEM ARCHITECTURE',22,NAVY,True)
    boxes=[(55,150,365,360,'CLIENT / BROWSER','Student + Admin','HTML · CSS · JavaScript',BLUE), (435,150,745,360,'APPLICATION LAYER','Flask Application','Routes · Validation · Roles',VIOLET), (815,150,1125,360,'DATA ACCESS','Database Module','Parameterized SQL · ORM-free',GREEN), (1195,150,1445,360,'DATABASE','SQLite Store','Users · Exams · Results',AMBER)]
    for x1,y1,x2,y2,t1,t2,t3,c in boxes:
        rr(d,(x1,y1,x2,y2),20,(249,251,254),c,3);rr(d,(x1+24,y1+25,x1+65,y1+66),11,c);txt(d,(x1+44,y1+46),['01','02','03','04'][boxes.index((x1,y1,x2,y2,t1,t2,t3,c))],12,WHITE,True,'mm');txt(d,(x1+24,y1+104),t1,14,c,True);txt(d,(x1+24,y1+143),t2,18,NAVY,True);txt(d,(x1+24,y1+179),t3,10,MUTED)
    for x in [374,754,1134]:
        d.line((x,255,x+52,255),fill=(129,157,190),width=4);d.polygon([(x+52,247),(x+66,255),(x+52,263)],fill=(129,157,190))
    rr(d,(230,425,1270,505),15,(238,246,255));txt(d,(750,451),'SECURITY + CONFIGURATION',10,BLUE,True,'mm');txt(d,(750,480),'Password hashing  ·  Session-based roles  ·  CSRF form tokens  ·  Environment-based secret key',11,NAVY,True,'mm')
    return im

def database_diagram():
    im=Image.new('RGB',(1500,700),WHITE);d=ImageDraw.Draw(im)
    txt(d,(50,30),'RELATIONAL DATABASE MODEL',22,NAVY,True)
    tables=[(55,130,390,360,'USERS',['id  PK','name','email  UNIQUE','password_hash','role','created_at'],BLUE),(570,130,930,320,'EXAMS',['id  PK','title','duration_minutes','total_marks','status','created_at'],VIOLET),(1090,130,1445,390,'QUESTIONS',['id  PK','exam_id  FK','question_text','options_json','correct_option','marks','difficulty'],GREEN),(210,465,590,660,'ATTEMPTS',['id  PK','user_id  FK','exam_id  FK','started_at / submitted_at','status / score'],AMBER),(880,465,1260,660,'ANSWERS',['id  PK','attempt_id  FK','question_id  FK','selected_option','is_correct'],RED)]
    for x1,y1,x2,y2,title,fields,c in tables:
        rr(d,(x1,y1,x2,y2),13,(250,252,254),c,2);d.rounded_rectangle((x1,y1,x2,y1+45),radius=13,fill=c);d.rectangle((x1,y1+30,x2,y1+45),fill=c);txt(d,(x1+18,y1+23),title,13,WHITE,True,'lm')
        yy=y1+67
        for f in fields: txt(d,(x1+20,yy),('• '+f),10,INK); yy+=24
    # Relationship connectors (intentional simple paths)
    d.line((930,210,1090,210),fill=(140,157,181),width=3)
    d.line((260,360,260,465),fill=(140,157,181),width=3);d.line((750,320,750,420),fill=(140,157,181),width=3);d.line((400,420,750,420),fill=(140,157,181),width=3);d.line((400,420,400,465),fill=(140,157,181),width=3)
    d.line((1260,310,1350,310),fill=(140,157,181),width=3);d.line((1350,310,1350,555),fill=(140,157,181),width=3);d.line((1260,555,1350,555),fill=(140,157,181),width=3);d.line((880,555,590,555),fill=(140,157,181),width=3)
    txt(d,(968,190),'1 : many',9,MUTED,True);txt(d,(275,410),'1 : many',9,MUTED,True);txt(d,(620,535),'1 : many',9,MUTED,True)
    return im

# save preview screenshots and diagrams
imgs={
 'screen_admin.png': screenshot_admin(),
 'screen_student.png': screenshot_student(),
 'screen_questions.png': screenshot_questions(),
 'screen_exam.png': screenshot_exam(),
 'screen_results.png': screenshot_results(),
 'architecture.png': architecture(),
 'database_model.png': database_diagram(),
}
# Interface screenshots (docs/assets/screen_*.png) are real captures of the running app; only diagrams are generated here.
for name,img in imgs.items():
    if not name.startswith('screen_'): img.save(ASSETS/name,optimize=True)
print('Assets written:', ', '.join(imgs))
