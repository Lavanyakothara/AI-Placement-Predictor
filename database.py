import sqlite3

conn = sqlite3.connect('students.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    cgpa REAL,
    python_skill INTEGER,
    dsa_skill INTEGER,
    projects INTEGER,
    score REAL
)
''')

conn.commit()
conn.close()

print("Database Created Successfully!")