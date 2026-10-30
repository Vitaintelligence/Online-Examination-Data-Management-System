# ExamSphere - Online Examination Data Management System

A role-based web application for managing online examinations, question banks, student attempts and result records.

## Technology
- Python 3.10+
- Flask (web framework)
- SQLite (relational database; created automatically in `instance/`)
- HTML5, CSS3 and JavaScript
- Werkzeug password hashing

## Run locally

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy .env.example to .env and set a unique SECRET_KEY
# The application reads SECRET_KEY from the environment. For local demo use,
# the built-in development key is accepted; do not use it in production.

# 4. Start the application
python app.py

# 5. Open http://127.0.0.1:5000
```

The database and demonstration data are initialized automatically on first startup.

## Demo accounts
These accounts are for local evaluation only. Change passwords and the secret key before any public deployment.

| Role | Email | Password |
|---|---|---|
| Administrator | `admin@examsphere.local` | `Admin@12345` |
| Student | `student@examsphere.local` | `Student@12345` |

A second sample student is `ishita@examsphere.local` with password `Student@12345`.

## Main workflows

### Administrator
1. Sign in using the administrator demo account.
2. Review the overview dashboard.
3. Create an examination under **Exams**.
4. Add multiple-choice questions under **Question bank**.
5. Publish an exam so students can access it.
6. Review submitted scores and download the result ledger as CSV.

### Student
1. Create a student account or use the demo student account.
2. Open the student dashboard.
3. Start a published assessment and choose one option for each question.
4. Submit the assessment to generate an automatically evaluated result.
5. Review selected and correct answers in the result page.


## Preview and walkthrough
- `preview/demo.html` is a standalone, clickable UI preview using sample data; it is not connected to the Flask database.
- `ExamSphere_Project_Demo.mp4` in the submission package is a narrated prototype walkthrough assembled from generated interface captures. It is not a live browser screen recording. Record a fresh live walkthrough after running the application locally if the evaluator specifically requires a real screen recording.

## Data model
`users`, `exams`, `questions`, `attempts` and `answers` form the core relational schema. Foreign keys protect relationships. Indexes support lookups by exam and student. Passwords are stored as salted hashes, and SQL statements use parameter binding.

## Data structures and algorithms
- **Queue:** answer records are processed in first-in, first-out order during submission.
- **Linear search:** the administrator question-bank search filters records by question text.
- **Merge sort:** submitted attempts are ordered by score for the result ranking view.

## Important academic-project limitations
- The sample implementation supports objective multiple-choice examinations; descriptive answers and plagiarism detection are outside the current scope.
- The browser timer improves the student experience, but this academic build does not provide a tamper-proof proctoring or server-enforced anti-cheating environment.
- Demo credentials are intentionally documented for local evaluation. Replace them and configure a strong random `SECRET_KEY` before deployment.
- The project uses SQLite for straightforward local setup. A production rollout would typically use managed PostgreSQL/MySQL, HTTPS, CSRF middleware, rate limiting, backups and a hardened deployment configuration.
- No public website or GitHub repository has been configured by this generated package. Publish the source code to your team's GitHub repository and add its URL to the submission text file before submitting.

## Project structure

```text
ExamSphere_Project/
├── app.py
├── dsa.py
├── schema.sql
├── requirements.txt
├── .env.example
├── templates/
├── static/
│   ├── css/style.css
│   └── js/app.js
├── instance/               # generated database (not committed)
└── README.md
```

## Health endpoint
`GET /health` returns a small JSON status response for basic service checks.
