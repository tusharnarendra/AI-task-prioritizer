import sqlite3
from datetime import datetime

def init_db():
    #Open database connection
    con = sqlite3.connect("focusflow.db")
    #Database cursor
    cur = con.cursor()
    #Database table (some of these columns may not be used or implemented later)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS task_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT,
            importance INTEGER,
            est_duration REAL,
            pred_duration REAL,
            due_date TEXT,
            energy_level INTEGER,
            created_at TEXT,
            completed INTEGER DEFAULT 0,
            completed_at TEXT,
            score REAL,
            cluster_label TEXT,
            gpt_explanation TEXT
        )
    """)
    con.commit()
    con.close()
    

def add_task(title, category, importance, est_duration, due_date, energy_level, completed, score):
    con = sqlite3.connect("focusflow.db")
    cur = con.cursor()

    created_at = datetime.utcnow().isoformat()

    #Updating table values
    cur.execute("""
        INSERT INTO task_info 
        (title, category, importance, est_duration, due_date, energy_level, created_at, completed, score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (title, category, importance, est_duration, due_date, energy_level, created_at, completed, score))

    con.commit()
    con.close()


def complete_task(task_id):
    con = sqlite3.connect(DB)
    cur = conn.cursor()
    c.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
