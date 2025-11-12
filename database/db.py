import sqlite3
from datetime import datetime

#Initialization function for the database table
def init_db():
    #Open database connection using a with statement to ensure clean connection handling
    with sqlite3.connect("focusflow.db") as con:
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
        #Indices for optimized look ups in later functions
        cur.execute("CREATE INDEX IF NOT EXISTS idx_completed ON task_info (completed)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_due_date ON task_info (due_date)")
    
#Function for adding tasks to the table
def add_task(title, category, importance, est_duration, due_date, energy_level, completed, score):
    with sqlite3.connect("focusflow.db") as con:
        cur = con.cursor()
        created_at = datetime.now().isoformat()

        # Updating table values
        cur.execute("""
            INSERT INTO task_info 
            (title, category, importance, est_duration, due_date, energy_level, created_at, completed, score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, category, importance, est_duration, due_date, energy_level, created_at, completed, score))

        task_id = cur.lastrowid

    return task_id

#Function to delete a selected task from the table
def delete_task(task_id):
    with sqlite3.connect("focusflow.db") as con:
        cur = con.cursor()
        cur.execute('DELETE FROM task_info WHERE id = ?', (task_id,))

#Function for updating completed task
def complete_task(task_id):
    with sqlite3.connect("focusflow.db") as con:
        cur = con.cursor()
        completed_at = datetime.now().isoformat()
        cur.execute('UPDATE task_info SET completed = 1, completed_at = ? WHERE id = ?', (completed_at, task_id))



#Function to fetch either all tasks or only the completed ones
def list_tasks(include_completed=False):
    with sqlite3.connect("focusflow.db") as con:
        cur = con.cursor()
        if include_completed:
            cur.execute('SELECT * FROM task_info')
        else:
            cur.execute('SELECT * FROM task_info WHERE completed = 0')
        rows = cur.fetchall()
    return rows

#Function to update predictions and GPT fields
def update_task_predictions(task_id, pred_duration=None, cluster_label=None, gpt_explanation=None):
    with sqlite3.connect("focusflow.db") as con:
        cur = con.cursor()
        cur.execute("""
            UPDATE task_info
            SET pred_duration = COALESCE(?, pred_duration),
                cluster_label = COALESCE(?, cluster_label),
                gpt_explanation = COALESCE(?, gpt_explanation)
            WHERE id = ?
        """, (pred_duration, cluster_label, gpt_explanation, task_id))
        
def highest_score():
    with sqlite3.connect("focusflow.db") as con:
        cur = con.cursor()
        cur.execute("SELECT MAX(score) FROM task_info")
        highest_score = cur.fetchone()[0] 
    return highest_score