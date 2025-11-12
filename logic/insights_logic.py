import sqlite3
import pandas as pd
from database.db import list_tasks  

class UserInsights:
    def __init__(self, csv_path=None, db_path="focusflow.db"):
        self.con = sqlite3.connect(db_path)
        self.cur = self.con.cursor()
        
        self.rows = list_tasks(include_completed=True)
        self.tasks_list = [
            {
                'id': r[0],
                'title': r[1],
                'category': r[2],
                'importance': r[3],
                'est_duration': r[4],
                'due_date': r[6],
                'completed': r[9],
            }
            for r in self.rows
        ]
        
        self.df = pd.read_csv(csv_path) if csv_path else None
    def compute_overall_summary(self):
        self.cur.execute('SELECT COUNT(*) FROM task_info WHERE completed = 1')
        count_result = self.cur.fetchone()[0]
        self.total_completed = count_result
        accepted_top_series = dataset['accepted_top_suggestion']
        self.accepted_top_percent = accepted_top_series.sum() / len(accepted_top_series) * 100