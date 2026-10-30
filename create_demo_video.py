from PIL import Image, ImageDraw, ImageFont, ImageOps
from pathlib import Path
import subprocess, wave, os, math, shutil

ROOT = Path(__file__).resolve().parent
AS = ROOT / 'docs' / 'assets'
WORK = ROOT / 'demo_video_work'
WORK.mkdir(exist_ok=True)
OUT = ROOT / 'ExamSphere_Project_Demo.mp4'
W, H = 1280, 720
NAVY=(13,28,54); NAVY2=(20,43,80); BLUE=(47,126,238); WHITE=(248,251,255); MUTED=(174,190,212); CYAN=(96,193,232); LINE=(61,82,113); GREEN=(70,199,159)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def f(sz,bold=False): return ImageFont.truetype(BOLD if bold else FONT,sz)
def draw_wrapped(draw, text, box, font, fill, spacing=9, max_lines=8):
    x,y,w,h=box; words=text.split(); lines=[]; cur=''
    for word in words:
        trial=(cur+' '+word).strip()
        if draw.textlength(trial,font=font) <= w: cur=trial
        else:
            if cur: lines.append(cur)
            cur=word
    if cur: lines.append(cur)
    lines=lines[:max_lines]
    draw.multiline_text((x,y),'\n'.join(lines),font=font,fill=fill,spacing=spacing)
    return len(lines)

def contain(im, box, bg=(244,248,253)):
    x,y,w,h=box
    pic=Image.open(im).convert('RGB')
    pic.thumbnail((w,h),Image.Resampling.LANCZOS)
    frame=Image.new('RGB',(w,h),bg)
    frame.paste(pic,((w-pic.width)//2,(h-pic.height)//2))
    return frame

scenes=[
    {
        'title':'Meet ExamSphere',
        'eyebrow':'PROJECT OVERVIEW',
        'copy':'An online examination data management system that brings exam setup, student assessments and result reporting into one consistent workspace.',
        'points':['Administrator and student roles','Objective MCQ assessments','Centralised result records'],
        'image':'screen_admin.png',
        'voice':'Welcome to ExamSphere, an online examination data management system developed by our team at SGT University. The system brings examination setup, student assessments and result reporting into one consistent workspace.'
    },
    {
        'title':'Administrator dashboard',
        'eyebrow':'ADMINISTRATION',
        'copy':'A single control centre summarises key examination activity and provides quick access to everyday administrative tasks.',
        'points':['Registered student accounts','Examination and question-bank totals','Submitted attempts and result records'],
        'image':'screen_admin.png',
        'voice':'The administrator dashboard summarises registered students, created examinations, question bank records and completed attempts. Quick links open exam management, question bank and result analytics.'
    },
    {
        'title':'Exams and question bank',
        'eyebrow':'ASSESSMENT SETUP',
        'copy':'Administrators maintain reusable question records and connect them to published examinations.',
        'points':['Exam title, duration and marks','Four options and one correct answer','Question marks and difficulty level'],
        'image':'screen_questions.png',
        'voice':'Administrators can create an examination, set its duration and total marks, choose its publication status, and add multiple-choice questions. Each question stores four options, one correct answer, marks and difficulty.'
    },
    {
        'title':'Student workspace',
        'eyebrow':'STUDENT EXPERIENCE',
        'copy':'Students sign in to a dedicated workspace and view the assessments that are available to them.',
        'points':['Published examination catalogue','Duration and marks at a glance','Direct entry into an assessment'],
        'image':'screen_student.png',
        'voice':'Students sign in to a separate workspace and see the examinations that are published. Each exam card shows its duration and total marks.'
    },
    {
        'title':'Attempt an examination',
        'eyebrow':'ONLINE ASSESSMENT',
        'copy':'The assessment interface presents the question, answer choices, remaining time and progress in one view.',
        'points':['Select one option per question','Visible timer and answer progress','Submit responses for evaluation'],
        'image':'screen_exam.png',
        'voice':'During an attempt, the student selects one answer per question. The screen shows the remaining time and the answered-question progress. Submitting sends the responses to the server for evaluation.'
    },
    {
        'title':'Results and performance',
        'eyebrow':'AUTOMATIC EVALUATION',
        'copy':'Submitted answers are compared with the stored answer key and the resulting score is retained for review.',
        'points':['Answer-level correctness records','Score calculation and review','Administrator result table and CSV export'],
        'image':'screen_results.png',
        'voice':'ExamSphere compares each response with the answer key, stores the selected option and correctness, and calculates the final score. Students can review their answers and administrators can inspect submitted attempts.'
    },
    {
        'title':'Data model and safeguards',
        'eyebrow':'TECHNICAL DESIGN',
        'copy':'A relational model links accounts, examinations, questions, attempts and submitted answers.',
        'points':['Queue for ordered answer processing','Linear search for question lookup','Merge sort for result ranking','Password hashing and role checks'],
        'image':'architecture.png',
        'voice':'The data model connects users, examinations, questions, attempts and answers. Python structures and algorithms demonstrate a queue for answer processing, linear search for question lookup and merge sort for result ranking. Password hashes and role checks support safer access.'
    },
    {
        'title':'Team and next steps',
        'eyebrow':'TA-1 / TA-2 SUBMISSION',
        'copy':'Thank you for reviewing the ExamSphere project walkthrough.',
        'points':['Shubham  |  251302294','Bharat  |  251302272','Yash  |  2513022263','Create and add the mandatory GitHub repository URL'],
        'image':None,
        'voice':'This concludes the ExamSphere walkthrough. Team members are Shubham, Bharat and Yash. Before submission, the team should publish the code to its GitHub repository and insert the required public repository link. Thank you.'
    }
]

# Build narrated visual frames and per-scene speech audio.
for idx, scene in enumerate(scenes,1):
    im=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(im)
    # Top identity bar and section eyebrow.
    d.rounded_rectangle((46,34,86,74),radius=12,fill=BLUE)
    d.text((66,54),'E',font=f(23,True),fill=WHITE,anchor='mm')
    d.text((102,38),'EXAMSPHERE',font=f(18,True),fill=WHITE)
    d.text((102,62),'ONLINE EXAMINATION DATA MANAGEMENT',font=f(9,True),fill=MUTED)
    d.text((W-50,55),f'{idx:02d} / {len(scenes):02d}',font=f(13,True),fill=MUTED,anchor='rm')
    d.line((46,94,W-46,94),fill=LINE,width=2)
    d.text((58,132),scene['eyebrow'],font=f(12,True),fill=CYAN)
    draw_wrapped(d,scene['title'],(58,168,440,110),f(38,True),WHITE,spacing=8,max_lines=2)
    draw_wrapped(d,scene['copy'],(60,292,410,140),f(18),MUTED,spacing=8,max_lines=5)
    py=464
    for point in scene['points']:
        d.ellipse((62,py+5,73,py+16),fill=GREEN)
        lines=draw_wrapped(d,point,(88,py,365,48),f(14,True),WHITE,spacing=4,max_lines=2)
        py += max(42,lines*24+10)
    # Screenshot / technical graphic stage.
    if scene['image']:
        frame=contain(AS/scene['image'],(0,0,720,450),bg=(244,248,253))
        x,y=508,170
        d.rounded_rectangle((x-10,y-10,x+730,y+460),radius=18,fill=(6,17,36),outline=(74,105,151),width=2)
        im.paste(frame,(x,y))
    else:
        # Team closing card rather than a fake application screenshot.
        d.rounded_rectangle((510,174,1214,622),radius=22,fill=NAVY2,outline=(74,105,151),width=2)
        d.text((560,218),'PROJECT TEAM',font=f(14,True),fill=CYAN)
        team=[('SHUBHAM','251302294'),('BHARAT','251302272'),('YASH','2513022263')]
        ty=278
        for name,reg in team:
            d.rounded_rectangle((558,ty,1168,ty+76),radius=12,fill=(30,59,101))
            d.text((586,ty+38),name,font=f(20,True),fill=WHITE,anchor='lm')
            d.text((1138,ty+38),reg,font=f(18,True),fill=MUTED,anchor='rm')
            ty+=94
        d.rounded_rectangle((558,ty+4,1168,ty+65),radius=12,fill=(43,82,139))
        d.text((863,ty+34),'GITHUB REPOSITORY URL REQUIRED',font=f(14,True),fill=WHITE,anchor='mm')
    # Footer disclosure, deliberately transparent about the type of demo.
    d.line((46,660,W-46,660),fill=LINE,width=1)
    d.text((58,682),'NARRATED PROTOTYPE UI WALKTHROUGH  •  GENERATED INTERFACE CAPTURES',font=f(10,True),fill=(149,169,194))
    d.text((W-58,682),'EXAMSPHERE',font=f(10,True),fill=MUTED,anchor='rm')
    frame_path=WORK/f'scene_{idx:02d}.png'; im.save(frame_path,optimize=True)
    wav_path=WORK/f'scene_{idx:02d}.wav'
    subprocess.run(['espeak','-v','en-us','-s','148','-p','42','-a','175','-w',str(wav_path),scene['voice']],check=True)

# Encode each scene to H.264 + AAC, then concatenate all scene segments.
segments=[]
for idx in range(1,len(scenes)+1):
    frame=WORK/f'scene_{idx:02d}.png'; wav=WORK/f'scene_{idx:02d}.wav'; seg=WORK/f'segment_{idx:02d}.mp4'
    subprocess.run([
        'ffmpeg','-y','-loglevel','error','-loop','1','-framerate','25','-i',str(frame),'-i',str(wav),
        '-c:v','libx264','-preset','medium','-tune','stillimage','-c:a','aac','-b:a','128k',
        '-pix_fmt','yuv420p','-r','25','-shortest','-movflags','+faststart',str(seg)
    ],check=True)
    segments.append(seg)
concat=WORK/'concat.txt'
concat.write_text('\n'.join(f"file '{p.as_posix()}'" for p in segments)+'\n')
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(OUT)],check=True)
print(f'Created {OUT} ({OUT.stat().st_size:,} bytes)')
