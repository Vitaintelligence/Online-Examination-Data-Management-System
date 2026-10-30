PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE COLLATE NOCASE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin','student')),
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    duration_minutes INTEGER NOT NULL CHECK(duration_minutes > 0),
    total_marks INTEGER NOT NULL CHECK(total_marks > 0),
    status TEXT NOT NULL CHECK(status IN ('Draft','Published','Archived')) DEFAULT 'Draft',
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_id INTEGER NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    options_json TEXT NOT NULL,
    correct_option INTEGER NOT NULL CHECK(correct_option BETWEEN 0 AND 3),
    marks INTEGER NOT NULL CHECK(marks > 0),
    difficulty TEXT NOT NULL CHECK(difficulty IN ('Easy','Medium','Hard')),
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    exam_id INTEGER NOT NULL REFERENCES exams(id),
    started_at TEXT NOT NULL,
    submitted_at TEXT,
    status TEXT NOT NULL CHECK(status IN ('In Progress','Submitted')),
    score INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attempt_id INTEGER NOT NULL REFERENCES attempts(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL REFERENCES questions(id),
    selected_option INTEGER CHECK(selected_option BETWEEN 0 AND 3),
    is_correct INTEGER NOT NULL DEFAULT 0 CHECK(is_correct IN (0,1)),
    UNIQUE(attempt_id, question_id)
);
CREATE INDEX IF NOT EXISTS idx_attempts_user ON attempts(user_id);
CREATE INDEX IF NOT EXISTS idx_attempts_exam ON attempts(exam_id);
CREATE INDEX IF NOT EXISTS idx_questions_exam ON questions(exam_id);
