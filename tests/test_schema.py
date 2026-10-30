import sqlite3
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class SchemaTests(unittest.TestCase):
    def test_core_tables_create(self):
        conn = sqlite3.connect(':memory:')
        conn.execute('PRAGMA foreign_keys = ON')
        conn.executescript((ROOT / 'schema.sql').read_text(encoding='utf-8'))
        names = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertTrue({'users', 'exams', 'questions', 'attempts', 'answers'}.issubset(names))
        conn.close()

if __name__ == '__main__':
    unittest.main()
