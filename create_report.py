from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path

ROOT=Path(__file__).resolve().parent
AS=ROOT/'docs'/'assets'
OUT=ROOT/'ExamSphere_Project_Report.docx'
NAVY='102B56'; BLUE='2878ED'; LIGHT='EAF2FF'; PALE='F5F8FC'; MUTED='6F8097'; INK='263F5C'; GREEN='159A7B'

def shade(cell,color):
    tcPr=cell._tc.get_or_add_tcPr(); shd=OxmlElement('w:shd'); shd.set(qn('w:fill'),color); tcPr.append(shd)
def set_cell_text(cell,text,bold=False,color=INK,size=9):
    cell.text=''
    p=cell.paragraphs[0]; p.paragraph_format.space_after=Pt(1); p.paragraph_format.space_before=Pt(1)
    r=p.add_run(str(text)); r.bold=bold; r.font.name='Aptos'; r.font.size=Pt(size); r.font.color.rgb=RGBColor.from_string(color)
    cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER

def set_cell_margins(cell, top=80, start=110, bottom=80, end=110):
    tc=cell._tc; tcPr=tc.get_or_add_tcPr(); tcMar=tcPr.first_child_found_in('w:tcMar')
    if tcMar is None: tcMar=OxmlElement('w:tcMar'); tcPr.append(tcMar)
    for m,v in [('top',top),('start',start),('bottom',bottom),('end',end)]:
        el=tcMar.find(qn('w:'+m))
        if el is None: el=OxmlElement('w:'+m); tcMar.append(el)
        el.set(qn('w:w'),str(v)); el.set(qn('w:type'),'dxa')

def set_repeat_table_header(row):
    trPr=row._tr.get_or_add_trPr(); tblHeader=OxmlElement('w:tblHeader'); tblHeader.set(qn('w:val'),'true'); trPr.append(tblHeader)

def add_table(doc, headers, rows, widths=None, font_size=8.5):
    t=doc.add_table(rows=1, cols=len(headers)); t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.autofit=False
    for i,h in enumerate(headers):
        set_cell_text(t.rows[0].cells[i],h,True,'FFFFFF',font_size); shade(t.rows[0].cells[i],NAVY); set_cell_margins(t.rows[0].cells[i]);
        if widths: t.rows[0].cells[i].width=Inches(widths[i])
    set_repeat_table_header(t.rows[0])
    for row in rows:
        cells=t.add_row().cells
        for i,val in enumerate(row):
            set_cell_text(cells[i],val,False,INK,font_size); set_cell_margins(cells[i])
            if len(t.rows)%2==0: shade(cells[i],'F5F8FC')
            if widths: cells[i].width=Inches(widths[i])
    doc.add_paragraph().paragraph_format.space_after=Pt(0)
    return t

_page_break_pending = False
def add_heading(doc,text,level=1):
    global _page_break_pending
    p=doc.add_paragraph(style=f'Heading {level}')
    if _page_break_pending:
        p.paragraph_format.page_break_before=True
        _page_break_pending=False
    p.paragraph_format.keep_with_next=True
    r=p.add_run(text)
    return p

def add_body(doc,text, boldlead=None):
    p=doc.add_paragraph(style='Normal')
    p.paragraph_format.space_after=Pt(6); p.paragraph_format.line_spacing=1.12
    if boldlead and text.startswith(boldlead):
        r=p.add_run(boldlead); r.bold=True; p.add_run(text[len(boldlead):])
    else: p.add_run(text)
    return p

def add_bullet(doc,text):
    p=doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent=Inches(.22); p.paragraph_format.first_line_indent=Inches(-.13); p.paragraph_format.space_after=Pt(3); p.paragraph_format.line_spacing=1.05
    p.add_run(text)
    return p

def add_picture_caption(doc,path,caption,width=6.9):
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after=Pt(3)
    p.add_run().add_picture(str(path),width=Inches(width))
    cp=doc.add_paragraph(); cp.alignment=WD_ALIGN_PARAGRAPH.CENTER; cp.paragraph_format.space_after=Pt(7)
    r=cp.add_run(caption); r.italic=True; r.font.size=Pt(8); r.font.color.rgb=RGBColor.from_string(MUTED)

def add_page_break(doc):
    global _page_break_pending
    _page_break_pending = True

doc=Document()
sec=doc.sections[0]
sec.top_margin=Inches(.67); sec.bottom_margin=Inches(.65); sec.left_margin=Inches(.72); sec.right_margin=Inches(.72)
sec.header_distance=Inches(.28); sec.footer_distance=Inches(.28)
styles=doc.styles
styles['Normal'].font.name='Aptos'; styles['Normal'].font.size=Pt(9.5); styles['Normal'].font.color.rgb=RGBColor.from_string(INK)
styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'),'Aptos')
for name,size,color in [('Heading 1',18,NAVY),('Heading 2',12,BLUE),('Heading 3',10,INK)]:
    st=styles[name]; st.font.name='Aptos Display'; st.font.size=Pt(size); st.font.bold=True; st.font.color.rgb=RGBColor.from_string(color); st.paragraph_format.space_before=Pt(8); st.paragraph_format.space_after=Pt(5)
# Header and footer
header=sec.header.paragraphs[0]; header.alignment=WD_ALIGN_PARAGRAPH.RIGHT
rr=header.add_run('EXAMSPHERE  /  PROJECT REPORT'); rr.font.size=Pt(8); rr.bold=True; rr.font.color.rgb=RGBColor.from_string(BLUE)
footer=sec.footer.paragraphs[0]; footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
fr=footer.add_run('SGT University  •  B.Tech CSE (AIML)  |  Page '); fr.font.size=Pt(8); fr.font.color.rgb=RGBColor.from_string(MUTED)
fld=OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),'PAGE'); footer._p.append(fld)

# COVER PAGE
p=doc.add_paragraph(); p.paragraph_format.space_before=Pt(32); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run('SGT UNIVERSITY'); r.bold=True; r.font.name='Aptos Display'; r.font.size=Pt(19); r.font.color.rgb=RGBColor.from_string(NAVY)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after=Pt(44)
r=p.add_run('B. TECH  ·  CSE (AIML)  ·  ACADEMIC YEAR 2026–2027'); r.bold=True; r.font.size=Pt(9); r.font.color.rgb=RGBColor.from_string(BLUE)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after=Pt(3)
r=p.add_run('EXAMSPHERE'); r.bold=True; r.font.name='Aptos Display'; r.font.size=Pt(36); r.font.color.rgb=RGBColor.from_string(BLUE)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after=Pt(15)
r=p.add_run('Online Examination Data Management System'); r.bold=True; r.font.size=Pt(17); r.font.color.rgb=RGBColor.from_string(NAVY)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after=Pt(45)
r=p.add_run('Secure assessment. Clear insights. Better outcomes.'); r.italic=True; r.font.size=Pt(11); r.font.color.rgb=RGBColor.from_string(MUTED)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
p.add_run().add_picture(str(AS/'screen_admin.png'),width=Inches(4.7))
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_before=Pt(12)
r=p.add_run('PROJECT TEAM'); r.bold=True; r.font.size=Pt(9); r.font.color.rgb=RGBColor.from_string(BLUE)
add_table(doc,['TEAM MEMBER','REGISTRATION NUMBER'],[
    ('Shubham','251302294'),('Bharat','251302272'),('Yash','2513022263')],[3.1,3.1],9)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_before=Pt(7)
r=p.add_run('Submitted to: Mr. Vivek  |  Trainer, ByteXL'); r.font.size=Pt(9); r.font.color.rgb=RGBColor.from_string(INK)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run('October 2026'); r.font.size=Pt(9); r.font.color.rgb=RGBColor.from_string(MUTED)

# PAGE 2: overview
add_page_break(doc)
add_heading(doc,'CONTENTS',1)
add_table(doc,['SECTION','DESCRIPTION'],[
('01','Abstract and introduction'),('02','Objectives and technology stack'),('03','System architecture and functional modules'),('04','Application workflow'),('05','Database design'),('06','Data structures, algorithms and security'),('07','User interface, testing and deployment'),('08','Limitations, future scope and conclusion')],[.8,5.7],8.5)
add_heading(doc,'1. Abstract',1)
add_body(doc,'ExamSphere is a web-based Online Examination Data Management System designed to centralise the complete objective-assessment workflow. The application provides separate administrator and student workspaces. Administrators can create and publish examinations, maintain a question bank, review registered accounts, inspect submitted attempts and export result records. Students can register, sign in, take published multiple-choice examinations, submit answers and review automatically evaluated results.')
add_body(doc,'The academic implementation uses Python with the Flask web framework and SQLite for persistent relational storage. Passwords are stored as salted hashes, role-based route protection separates administrative functions from student functions, and parameterised SQL statements are used for database operations. A small Data Structures and Algorithms module demonstrates a FIFO queue, linear search and merge sort within meaningful application workflows.')
add_heading(doc,'2. Introduction',1)
add_body(doc,'Traditional examination administration can involve separate spreadsheets, paper-based question sets, manual answer checking and disconnected result records. These processes make it harder to maintain consistent assessment data, retrieve historical attempts and communicate performance in a timely way.')
add_body(doc,'ExamSphere brings exam setup, question storage, assessment attempts and result management into a single application. The current scope focuses on objective multiple-choice assessments so that the system can demonstrate a complete and understandable end-to-end workflow while remaining straightforward to run locally.')
add_heading(doc,'Project scope',2)
add_body(doc,'The project covers user authentication, administrator and student roles, exam creation and publication, MCQ question management, timed assessment presentation, automatic scoring, answer review, result ranking and CSV export. Online proctoring, descriptive-answer evaluation and production-scale deployment are outside the current academic scope.')

# PAGE 3
add_page_break(doc)
add_heading(doc,'3. Objectives',1)
for x in [
    'Create a responsive web interface for examination administration and student assessment.',
    'Provide secure student registration and sign-in with salted password hashing.',
    'Separate administrative and student capabilities through role-based access checks.',
    'Allow administrators to create examinations and maintain multiple-choice question records.',
    'Present published exams with duration, marks and instructions to students.',
    'Evaluate objective answers automatically and persist scores with attempt history.',
    'Provide result review, score ranking and CSV export for academic reporting.',
    'Apply core data structures and algorithms to real system operations.'
]: add_bullet(doc,x)
add_heading(doc,'4. Technology stack',1)
add_table(doc,['TECHNOLOGY','ROLE IN THE PROJECT'],[
('Python 3.10+','Main programming language for routes, validation, scoring and data processing.'),
('Flask','Lightweight web framework for routing, request handling, sessions and template rendering.'),
('SQLite','Relational database for users, examinations, questions, attempts and answers.'),
('HTML5 / CSS3','Semantic page structure, responsive layout, visual components and dashboards.'),
('JavaScript','Client-side interactions, answer progress and examination countdown timer.'),
('Werkzeug','Password hashing and password verification utilities used by Flask.'),
('Git / GitHub','Version control workflow and source-code collaboration target.')],[1.55,4.95],8)
add_page_break(doc)
add_heading(doc,'5. System architecture',1)
add_body(doc,'ExamSphere follows a layered web architecture. The browser presents the student and administrator interfaces. Flask handles routes, authentication, permissions, form validation and evaluation logic. A database access layer executes parameterised SQL statements against the SQLite database. The database stores the persistent records used by the system.')
add_picture_caption(doc,AS/'architecture.png','Figure 1. Logical architecture of the ExamSphere application.',6.85)
add_heading(doc,'5.1 Project structure',2)
add_body(doc,'The project keeps the application routes, algorithm implementations, SQL schema, templates and static assets in separate files. The instance folder is created at runtime and stores the local SQLite database; it is excluded from version control.')
add_table(doc,['FILE / FOLDER','RESPONSIBILITY'],[('app.py','Flask application, routes, sessions, role checks and evaluation.'),('dsa.py','Queue, linear search and merge sort implementations.'),('schema.sql','Relational database tables, constraints and indexes.'),('templates/','Jinja2 pages for student and administrator workspaces.'),('static/','Responsive CSS and client-side timer/progress behavior.'),('instance/','Generated local database; not included in source control.')],[1.55,4.95],8)

# PAGE 4
add_page_break(doc)
add_heading(doc,'6. Functional modules',1)
add_heading(doc,'6.1 Administrator module',2)
for x in [
    'Overview dashboard: displays counts of registered students, examinations, questions and completed attempts.',
    'Exam management: creates an examination with title, description, duration, total marks and publication status (Draft, Published or Archived).',
    'Question bank: adds MCQ questions with four options, one correct option, marks and difficulty level; supports searching question text.',
    'Student records: displays the registered accounts and their access roles.',
    'Result management: lists submitted attempts in descending score order and exports the result ledger as CSV.'
]: add_bullet(doc,x)
add_heading(doc,'6.2 Student module',2)
for x in [
    'Registration and sign-in: creates student accounts and verifies credentials before opening protected pages.',
    'Assessment catalogue: displays published examinations with their duration, marks and description.',
    'Online attempt: presents one multiple-choice question at a time in a structured form, with a visible timer and answered-question progress.',
    'Automatic evaluation: compares submitted options with the stored answer key and calculates the score.',
    'Result review: displays the final score, percentage, selected answers and correct options.'
]: add_bullet(doc,x)
add_heading(doc,'6.3 Examination lifecycle',2)
add_table(doc,['STAGE','SYSTEM ACTION'],[
('Create','Administrator enters exam details and saves a Draft or Published exam.'),
('Prepare','Questions are associated with the examination and stored in the question bank.'),
('Publish','Published assessments appear in the student catalogue.'),
('Attempt','Student starts an attempt; the system records the start time and status.'),
('Submit','Selected answers are processed and the attempt is marked Submitted.'),
('Evaluate','The system calculates marks and stores answer-level correctness.'),
('Review','Student reviews the result; administrator can rank and export attempts.')],[1.2,5.3],8)
add_picture_caption(doc,AS/'screen_student.png','Figure 2. Student workspace showing published examinations.',6.85)

# PAGE 5
add_heading(doc,'7. Database design',1)
add_body(doc,'The system uses five core relational tables. Primary keys uniquely identify records; foreign keys connect users to attempts, exams to questions and attempts to answers. The schema also defines lookup indexes for common student, examination and question queries.')
add_picture_caption(doc,AS/'database_model.png','Figure 3. Core relational data model. PK = primary key; FK = foreign key.',6.85)
add_heading(doc,'7.1 Core table dictionary',2)
add_table(doc,['TABLE','PURPOSE','IMPORTANT FIELDS'],[
('users','Stores account identity and access role.','id, name, email, password_hash, role, created_at'),
('exams','Stores assessment configuration and publication status.','id, title, duration_minutes, total_marks, status'),
('questions','Stores the question text, options, answer key and marks.','id, exam_id, question_text, options_json, correct_option, marks'),
('attempts','Stores each student examination attempt and final score.','id, user_id, exam_id, started_at, submitted_at, status, score'),
('answers','Stores the selected option and correctness for each question.','id, attempt_id, question_id, selected_option, is_correct')],[.95,2.15,3.4],7.5)
add_heading(doc,'7.2 Database design decisions',2)
for x in [
    'Referential integrity: foreign-key constraints protect relationships between the core entities.',
    'Unique identity: user email addresses are unique and compared case-insensitively.',
    'Answer traceability: each answer row stores the selected option and correctness for a specific attempt and question.',
    'Safe SQL: user-provided values are passed as bound parameters rather than concatenated into SQL strings.',
    'Historical records: submitted attempts and answers are retained to support result review and export.'
]: add_bullet(doc,x)

# PAGE 6
add_page_break(doc)
add_heading(doc,'8. Data structures and algorithms',1)
add_body(doc,'A separate dsa.py module implements core structures and algorithms explicitly. These implementations are connected to application features so that the project demonstrates applied use rather than only standalone examples.')
add_heading(doc,'8.1 FIFO queue',2)
add_body(doc,'The Queue class follows first-in, first-out order. During assessment submission, question-and-response pairs are enqueued in question order and dequeued sequentially for answer evaluation and database insertion. This provides a clear, deterministic processing sequence.')
add_heading(doc,'8.2 Linear search',2)
add_body(doc,'The linear_search function scans the question records and returns those whose question text contains the administrator search term, ignoring letter case. Its time complexity is O(n) for n stored question records.')
add_heading(doc,'8.3 Merge sort',2)
add_body(doc,'The merge_sort function recursively divides the submitted-attempt list, sorts each half and merges the halves in order. The result-management screen uses this implementation to rank submitted attempts by score. Its average and worst-case time complexity is O(n log n).')
add_heading(doc,'9. Security and data integrity',1)
for x in [
    'Password protection: Werkzeug generate_password_hash and check_password_hash are used; plaintext passwords are not stored.',
    'Role-based authorisation: administrator routes require an authenticated admin session; student routes require a student session.',
    'Form tokens: state-changing POST forms include a session-bound CSRF token check.',
    'Attempt ownership: a student can open only attempts linked to their own account.',
    'Parameterized SQL: all values from forms and URLs are bound through SQLite placeholders.',
    'Cookie settings: the session cookie is HTTP-only and uses SameSite=Lax.',
    'Configuration: SECRET_KEY can be supplied through environment configuration; the built-in key is for local demonstration only.'
]: add_bullet(doc,x)
add_heading(doc,'10. Application workflow',1)
add_picture_caption(doc,AS/'screen_exam.png','Figure 4. Student examination screen with timer, answer choices and progress panel.',6.85)
add_body(doc,'On submission, the server reloads the attempt for the authenticated student, evaluates each stored question against its answer key, saves the answer rows, calculates the score and updates the attempt status to Submitted. A completed attempt is redirected to its result page rather than allowing another submission.')

# PAGE 7
add_page_break(doc)
add_heading(doc,'11. User interface',1)
add_body(doc,'The interface uses a shared navigation and styling system across administrator and student views. The visual language uses a restrained blue palette, clear typography, consistent cards and compact status labels. Responsive layout rules adapt the navigation, metric cards, forms and question screens to narrower devices.')
add_picture_caption(doc,AS/'screen_questions.png','Figure 5. Administrator question-bank interface.',6.85)
add_heading(doc,'12. Testing and validation',1)
add_body(doc,'The project package includes smoke checks for the independent DSA module and database schema. The following table records what was checked in the preparation environment and what still requires a full local application run.')
add_table(doc,['TEST AREA','CHECK PERFORMED','STATUS'],[
('Queue','Enqueue and dequeue order; empty-queue state.','PASS'),
('Linear search','Case-insensitive matching of question text.','PASS'),
('Merge sort','Descending score ordering.','PASS'),
('SQLite schema','All five core tables and foreign-key definitions load in an in-memory database.','PASS'),
('Flask routes / browser flow','Dependency was not available in the document-generation environment; run the provided local smoke checklist after installing requirements.','PENDING LOCAL RUN')],[1.3,4.1,1.1],7.5)
add_heading(doc,'12.1 Recommended acceptance checklist',2)
for x in [
    'Start the application and verify the /health response.',
    'Sign in as admin; create an exam and add at least one question.',
    'Publish the exam and sign in as a student in a separate browser session.',
    'Start the exam, submit answers and confirm the score and answer review.',
    'Return to the admin account, verify the submitted attempt and download the CSV export.'
]: add_bullet(doc,x)
add_heading(doc,'13. Deployment and version control',1)
add_body(doc,'The application is designed for straightforward local execution on a machine with Python installed. It uses Flask for HTTP routing and server-rendered pages, while SQLite creates the local database under instance/ during first startup. The following workflow describes how the team can run, evaluate and publish the source package.')
add_heading(doc,'13.1 Local setup workflow',2)
for x in [
    'Extract ExamSphere_Code.zip into a working directory and open a terminal in the extracted project folder.',
    'Create and activate a virtual environment, then install the packages listed in requirements.txt.',
    'Copy .env.example to .env and replace the development SECRET_KEY with a long, random value before using the application beyond a local demo.',
    'Run python app.py and open the local address printed by Flask. The first startup creates the SQLite database and seeds clearly labelled demonstration accounts and sample data.',
    'Evaluate both roles: use the administrator account to publish an examination, then sign in as a student to attempt it and review the generated result. Demo credentials are documented in README.md.'
]: add_bullet(doc,x)
add_heading(doc,'13.2 GitHub source publication',2)
add_body(doc,'The mandatory GitHub repository must be created by the team in its own GitHub account. After extracting the code package, initialise Git, stage the project files, create an initial commit and connect the repository URL supplied by GitHub. Push the main branch and verify that the README and source folders are visible to the evaluator. The .gitignore excludes local environment secrets, the generated SQLite database, virtual environments and Python cache files; these exclusions should be retained.')
add_body(doc,'No public GitHub repository or hosted website has been created as part of this generated package. The team must replace the pending repository field in the team-details text file with the real repository URL before submission. The website field may remain marked as not deployed if no public hosting is available.')

# PAGE 8
add_page_break(doc)
add_heading(doc,'14. Limitations and future scope',1)
add_heading(doc,'Current limitations',2)
for x in [
    'The current assessment engine supports objective multiple-choice questions only.',
    'The timer is implemented in the browser for the academic demonstration; the system is not a secure remote-proctoring solution and does not provide tamper-proof time enforcement.',
    'There is no real-time invigilation, webcam monitoring, plagiarism analysis or identity verification.',
    'SQLite is appropriate for a local academic prototype but is not the intended database for a large concurrent production deployment.',
    'The demo accounts and development secret are provided only for local evaluation and must be replaced before public deployment.'
]: add_bullet(doc,x)
add_heading(doc,'Future enhancements',2)
for x in [
    'Support descriptive questions, file uploads and teacher-assisted evaluation.',
    'Introduce server-enforced time limits, autosave, attempt recovery and stronger audit logging.',
    'Add exam scheduling, per-student access windows, randomised question order and question pools.',
    'Move to managed PostgreSQL or MySQL and add automated backups and monitoring.',
    'Add analytics such as score distributions, question difficulty analysis and topic-wise performance.',
    'Add email notifications, downloadable student scorecards and an institutional single-sign-on option.'
]: add_bullet(doc,x)
add_heading(doc,'15. Conclusion',1)
add_body(doc,'ExamSphere provides a structured academic prototype for managing online objective examinations and their associated data. It connects user access, examination setup, question storage, student attempts, automatic evaluation and result reporting within one application. The project also demonstrates relational database design, password hashing, role-based access control and practical data-structure and algorithm use. The included smoke checks validate the DSA utilities and relational schema; a full browser acceptance run remains a required final step on a machine with the listed Flask dependencies installed.')
add_heading(doc,'16. Acknowledgement',1)
add_body(doc,'We sincerely thank Mr. Vivek, our trainer at ByteXL, for his guidance, encouragement and support during the development of this project. We also acknowledge the official documentation for Python, Flask, SQLite and Werkzeug used to understand and implement the application.')
add_heading(doc,'17. References',1)
for x in [
    'Python documentation: https://docs.python.org/3/',
    'Flask documentation: https://flask.palletsprojects.com/',
    'SQLite documentation: https://www.sqlite.org/docs.html',
    'Werkzeug security utilities: https://werkzeug.palletsprojects.com/en/stable/utils/',
    'Git documentation: https://git-scm.com/doc'
]: add_bullet(doc,x)

# Metadata
props=doc.core_properties
props.title='ExamSphere - Online Examination Data Management System'
props.subject='TA-1/2 Project Report'
props.author='ExamSphere Team'
props.keywords='Online Examination, Data Management, Flask, SQLite, Python'

doc.save(OUT)
print(OUT)
