"""ExamSphere - Online Examination Data Management System.

A Flask + SQLite academic project demonstrating role-based examination workflows.
Run: pip install -r requirements.txt && python app.py
"""
from __future__ import annotations

import csv
import io
import json
import os
import secrets
import sqlite3
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from flask import (Flask, Response, abort, flash, g, redirect,
                   render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from dsa import linear_search, merge_sort, Queue

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
INSTANCE_DIR = BASE_DIR / "instance"
DB_PATH = INSTANCE_DIR / "examsphere.db"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        INSTANCE_DIR.mkdir(exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        g.db = conn
    return g.db


def close_db(_error=None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    INSTANCE_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    schema = (BASE_DIR / "schema.sql").read_text(encoding="utf-8")
    conn.executescript(schema)
    # Demo accounts are created only for a fresh database.
    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        users = [
            ("System Administrator", "admin@examsphere.local", generate_password_hash("Admin@12345"), "admin", utc_now()),
            ("Aarav Sharma", "student@examsphere.local", generate_password_hash("Student@12345"), "student", utc_now()),
            ("Ishita Verma", "ishita@examsphere.local", generate_password_hash("Student@12345"), "student", utc_now()),
        ]
        conn.executemany("INSERT INTO users(name,email,password_hash,role,created_at) VALUES(?,?,?,?,?)", users)
        conn.execute(
            "INSERT INTO exams(title,description,duration_minutes,total_marks,status,created_at) VALUES(?,?,?,?,?,?)",
            ("Database Management Systems", "A foundational assessment covering SQL, relational concepts, keys, normalization and transactions.", 30, 30, "Published", utc_now()),
        )
        exam_id = conn.execute("SELECT id FROM exams LIMIT 1").fetchone()[0]
        sample_questions = [
            (exam_id, "Which SQL command is used to retrieve data from a table?", ["GET", "SELECT", "FETCH ALL", "OPEN"], 1, 5, "Easy"),
            (exam_id, "Which key uniquely identifies each row in a relation?", ["Foreign key", "Candidate attribute", "Primary key", "Composite view"], 2, 5, "Easy"),
            (exam_id, "What does ACID stand for in transaction processing?", ["Atomicity, Consistency, Isolation, Durability", "Accuracy, Control, Integrity, Dependency", "Atomicity, Clarity, Isolation, Data", "Access, Consistency, Indexing, Durability"], 0, 5, "Medium"),
            (exam_id, "Which normal form removes partial dependencies?", ["1NF", "2NF", "3NF", "BCNF only"], 1, 5, "Medium"),
            (exam_id, "Which SQL clause filters grouped records?", ["WHERE", "ORDER BY", "HAVING", "DISTINCT"], 2, 5, "Medium"),
            (exam_id, "A foreign key is primarily used to maintain which property?", ["Entity integrity", "Referential integrity", "Domain independence", "Physical independence"], 1, 5, "Hard"),
        ]
        for exam, q, opts, correct, marks, difficulty in sample_questions:
            conn.execute(
                "INSERT INTO questions(exam_id,question_text,options_json,correct_option,marks,difficulty,created_at) VALUES(?,?,?,?,?,?,?)",
                (exam, q, json.dumps(opts), correct, marks, difficulty, utc_now()),
            )
    conn.commit()
    conn.close()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please sign in to continue.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def role_required(role: str):
    def decorator(view):
        @wraps(view)
        @login_required
        def wrapped(*args, **kwargs):
            if session.get("role") != role:
                flash("You do not have permission to access that page.", "danger")
                return redirect(url_for("home"))
            return view(*args, **kwargs)
        return wrapped
    return decorator


def csrf_protect(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if request.method == "POST":
            submitted = request.form.get("csrf_token", "")
            if not submitted or not secrets.compare_digest(submitted, session.get("csrf_token", "")):
                abort(400, description="Invalid form token. Refresh the page and try again.")
        return view(*args, **kwargs)
    return wrapped


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "development-only-change-this-key"),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.environ.get("SESSION_COOKIE_SECURE", "0") == "1",
        MAX_CONTENT_LENGTH=2 * 1024 * 1024,
    )
    app.teardown_appcontext(close_db)
    app.jinja_env.filters["loads"] = json.loads

    @app.before_request
    def ensure_csrf():
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_urlsafe(24)
        if session.get("user_id"):
            user = get_db().execute("SELECT id,name,email,role FROM users WHERE id=?", (session["user_id"],)).fetchone()
            if user is None:
                session.clear()

    @app.context_processor
    def inject_globals():
        return {"csrf_token": session.get("csrf_token", ""), "current_user": session.get("name"), "current_role": session.get("role")}

    @app.get("/")
    def home():
        if session.get("role") == "admin":
            return redirect(url_for("admin_dashboard"))
        if session.get("role") == "student":
            return redirect(url_for("student_dashboard"))
        return render_template("landing.html")

    @app.route("/login", methods=["GET", "POST"])
    @csrf_protect
    def login():
        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            user = get_db().execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
            if user and check_password_hash(user["password_hash"], password):
                session.clear()
                session.update(user_id=user["id"], name=user["name"], role=user["role"], csrf_token=secrets.token_urlsafe(24))
                flash(f"Welcome back, {user['name'].split()[0]}.", "success")
                return redirect(url_for("home"))
            flash("Email or password is incorrect.", "danger")
        return render_template("login.html")

    @app.route("/register", methods=["GET", "POST"])
    @csrf_protect
    def register():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            if len(name) < 2 or "@" not in email or len(password) < 8:
                flash("Enter a valid name and email. Password must contain at least 8 characters.", "warning")
            else:
                try:
                    get_db().execute(
                        "INSERT INTO users(name,email,password_hash,role,created_at) VALUES(?,?,?,?,?)",
                        (name, email, generate_password_hash(password), "student", utc_now()),
                    )
                    get_db().commit()
                    flash("Account created. You can now sign in.", "success")
                    return redirect(url_for("login"))
                except sqlite3.IntegrityError:
                    flash("An account with this email already exists.", "danger")
        return render_template("register.html")

    @app.get("/logout")
    def logout():
        session.clear()
        flash("You have been signed out.", "info")
        return redirect(url_for("home"))

    @app.get("/student")
    @role_required("student")
    def student_dashboard():
        db = get_db()
        exams = db.execute("SELECT * FROM exams WHERE status='Published' ORDER BY id DESC").fetchall()
        attempts = db.execute(
            "SELECT a.*, e.title FROM attempts a JOIN exams e ON e.id=a.exam_id WHERE a.user_id=? ORDER BY a.id DESC LIMIT 6",
            (session["user_id"],),
        ).fetchall()
        return render_template("student_dashboard.html", exams=exams, attempts=attempts)

    @app.post("/student/exam/<int:exam_id>/start")
    @role_required("student")
    @csrf_protect
    def start_exam(exam_id: int):
        db = get_db()
        exam = db.execute("SELECT * FROM exams WHERE id=? AND status='Published'", (exam_id,)).fetchone()
        if not exam:
            abort(404)
        existing = db.execute("SELECT id FROM attempts WHERE user_id=? AND exam_id=? AND status='In Progress'", (session["user_id"], exam_id)).fetchone()
        if existing:
            return redirect(url_for("take_exam", attempt_id=existing["id"]))
        questions = db.execute("SELECT COUNT(*) FROM questions WHERE exam_id=?", (exam_id,)).fetchone()[0]
        if not questions:
            flash("This exam does not have any questions yet.", "warning")
            return redirect(url_for("student_dashboard"))
        cur = db.execute(
            "INSERT INTO attempts(user_id,exam_id,started_at,status) VALUES(?,?,?,?)",
            (session["user_id"], exam_id, utc_now(), "In Progress"),
        )
        db.commit()
        return redirect(url_for("take_exam", attempt_id=cur.lastrowid))

    @app.route("/attempt/<int:attempt_id>", methods=["GET", "POST"])
    @role_required("student")
    @csrf_protect
    def take_exam(attempt_id: int):
        db = get_db()
        attempt = db.execute(
            "SELECT a.*,e.title,e.duration_minutes,e.total_marks FROM attempts a JOIN exams e ON e.id=a.exam_id WHERE a.id=? AND a.user_id=?",
            (attempt_id, session["user_id"]),
        ).fetchone()
        if not attempt:
            abort(404)
        if attempt["status"] == "Submitted":
            return redirect(url_for("result", attempt_id=attempt_id))
        questions = db.execute("SELECT * FROM questions WHERE exam_id=? ORDER BY id", (attempt["exam_id"],)).fetchall()
        if request.method == "POST":
            # Queue preserves deterministic answer-processing order before database writes.
            answer_queue = Queue()
            for q in questions:
                answer_queue.enqueue((q, request.form.get(f"question_{q['id']}")))
            score = 0
            while not answer_queue.is_empty():
                q, selected = answer_queue.dequeue()
                selected_idx = int(selected) if selected is not None and selected.isdigit() and int(selected) in range(4) else None
                is_correct = selected_idx == q["correct_option"]
                if is_correct:
                    score += q["marks"]
                db.execute(
                    "INSERT INTO answers(attempt_id,question_id,selected_option,is_correct) VALUES(?,?,?,?)",
                    (attempt_id, q["id"], selected_idx, int(is_correct)),
                )
            db.execute("UPDATE attempts SET submitted_at=?,status='Submitted',score=? WHERE id=?", (utc_now(), score, attempt_id))
            db.commit()
            flash("Your examination has been submitted successfully.", "success")
            return redirect(url_for("result", attempt_id=attempt_id))
        return render_template("take_exam.html", attempt=attempt, questions=questions)

    @app.get("/result/<int:attempt_id>")
    @role_required("student")
    def result(attempt_id: int):
        attempt = get_db().execute(
            "SELECT a.*,e.title,e.total_marks,u.name FROM attempts a JOIN exams e ON e.id=a.exam_id JOIN users u ON u.id=a.user_id WHERE a.id=? AND a.user_id=?",
            (attempt_id, session["user_id"]),
        ).fetchone()
        if not attempt:
            abort(404)
        if attempt["status"] != "Submitted":
            return redirect(url_for("take_exam", attempt_id=attempt_id))
        answers = get_db().execute(
            "SELECT an.*,q.question_text,q.options_json,q.correct_option,q.marks FROM answers an JOIN questions q ON q.id=an.question_id WHERE an.attempt_id=? ORDER BY q.id",
            (attempt_id,),
        ).fetchall()
        return render_template("result.html", attempt=attempt, answers=answers)

    @app.get("/admin")
    @role_required("admin")
    def admin_dashboard():
        db = get_db()
        stats = {
            "students": db.execute("SELECT COUNT(*) FROM users WHERE role='student'").fetchone()[0],
            "exams": db.execute("SELECT COUNT(*) FROM exams").fetchone()[0],
            "questions": db.execute("SELECT COUNT(*) FROM questions").fetchone()[0],
            "attempts": db.execute("SELECT COUNT(*) FROM attempts WHERE status='Submitted'").fetchone()[0],
        }
        recent = db.execute(
            "SELECT a.*,u.name,e.title FROM attempts a JOIN users u ON u.id=a.user_id JOIN exams e ON e.id=a.exam_id ORDER BY a.id DESC LIMIT 7"
        ).fetchall()
        return render_template("admin_dashboard.html", stats=stats, recent=recent)

    @app.route("/admin/exams", methods=["GET", "POST"])
    @role_required("admin")
    @csrf_protect
    def admin_exams():
        db = get_db()
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip()
            duration = request.form.get("duration", "30")
            marks = request.form.get("marks", "30")
            status = request.form.get("status", "Draft")
            try:
                duration_i, marks_i = int(duration), int(marks)
                if not title or duration_i < 1 or marks_i < 1 or status not in ("Draft", "Published", "Archived"):
                    raise ValueError
                db.execute("INSERT INTO exams(title,description,duration_minutes,total_marks,status,created_at) VALUES(?,?,?,?,?,?)", (title, description, duration_i, marks_i, status, utc_now()))
                db.commit()
                flash("Exam created. Add questions from the Question Bank.", "success")
                return redirect(url_for("admin_exams"))
            except (ValueError, sqlite3.IntegrityError):
                flash("Enter valid exam details.", "danger")
        exams = db.execute("SELECT e.*,COUNT(q.id) question_count FROM exams e LEFT JOIN questions q ON q.exam_id=e.id GROUP BY e.id ORDER BY e.id DESC").fetchall()
        return render_template("admin_exams.html", exams=exams)

    @app.route("/admin/questions", methods=["GET", "POST"])
    @role_required("admin")
    @csrf_protect
    def admin_questions():
        db = get_db()
        if request.method == "POST":
            exam_id = request.form.get("exam_id", "")
            question_text = request.form.get("question_text", "").strip()
            options = [request.form.get(f"option_{i}", "").strip() for i in range(4)]
            correct = request.form.get("correct_option", "")
            marks = request.form.get("marks", "1")
            difficulty = request.form.get("difficulty", "Easy")
            try:
                correct_i, marks_i, exam_i = int(correct), int(marks), int(exam_id)
                if not question_text or any(not x for x in options) or correct_i not in range(4) or marks_i < 1 or difficulty not in ("Easy", "Medium", "Hard"):
                    raise ValueError
                db.execute("INSERT INTO questions(exam_id,question_text,options_json,correct_option,marks,difficulty,created_at) VALUES(?,?,?,?,?,?,?)", (exam_i, question_text, json.dumps(options), correct_i, marks_i, difficulty, utc_now()))
                db.commit()
                flash("Question added to the bank.", "success")
                return redirect(url_for("admin_questions"))
            except (ValueError, sqlite3.IntegrityError):
                flash("Complete all fields with valid values.", "danger")
        search = request.args.get("q", "").strip()
        exams = db.execute("SELECT id,title FROM exams ORDER BY id DESC").fetchall()
        all_questions = [dict(row) for row in db.execute("SELECT q.*,e.title exam_title FROM questions q JOIN exams e ON e.id=q.exam_id ORDER BY q.id DESC").fetchall()]
        if search:
            all_questions = linear_search(all_questions, search, "question_text")
        return render_template("admin_questions.html", questions=all_questions, exams=exams, search=search)

    @app.post("/admin/questions/<int:question_id>/delete")
    @role_required("admin")
    @csrf_protect
    def delete_question(question_id: int):
        db = get_db()
        used = db.execute("SELECT 1 FROM answers WHERE question_id=? LIMIT 1", (question_id,)).fetchone()
        if used:
            flash("This question is part of a submitted result and cannot be deleted.", "warning")
        else:
            db.execute("DELETE FROM questions WHERE id=?", (question_id,))
            db.commit()
            flash("Question deleted.", "info")
        return redirect(url_for("admin_questions"))

    @app.get("/admin/results")
    @role_required("admin")
    def admin_results():
        db = get_db()
        attempts = [dict(row) for row in db.execute("SELECT a.*,u.name student_name,u.email,e.title exam_title,e.total_marks FROM attempts a JOIN users u ON u.id=a.user_id JOIN exams e ON e.id=a.exam_id WHERE a.status='Submitted'").fetchall()]
        attempts = merge_sort(attempts, key=lambda x: (x.get("score") or 0), reverse=True)
        return render_template("admin_results.html", attempts=attempts)

    @app.get("/admin/results/export.csv")
    @role_required("admin")
    def export_results():
        rows = get_db().execute("SELECT a.id,u.name,u.email,e.title,a.score,e.total_marks,a.submitted_at FROM attempts a JOIN users u ON u.id=a.user_id JOIN exams e ON e.id=a.exam_id WHERE a.status='Submitted' ORDER BY a.submitted_at DESC").fetchall()
        stream = io.StringIO()
        writer = csv.writer(stream)
        writer.writerow(["Attempt ID", "Student", "Email", "Exam", "Score", "Total Marks", "Submitted At"])
        writer.writerows([tuple(r) for r in rows])
        return Response(stream.getvalue(), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=examsphere-results.csv"})

    @app.get("/admin/users")
    @role_required("admin")
    def admin_users():
        users = get_db().execute("SELECT id,name,email,role,created_at FROM users ORDER BY role,name").fetchall()
        return render_template("admin_users.html", users=users)

    @app.get("/health")
    def health():
        return {"status": "ok", "application": "ExamSphere"}

    @app.errorhandler(400)
    def bad_request(error):
        return render_template("error.html", code=400, message=getattr(error, "description", "Bad request.")), 400

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("error.html", code=403, message="You are not allowed to access this resource."), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template("error.html", code=404, message="The page you requested could not be found."), 404

    init_db()
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=os.environ.get("FLASK_DEBUG") == "1")
