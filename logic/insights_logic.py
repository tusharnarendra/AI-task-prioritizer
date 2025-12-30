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
        # 1) Total completed tasks
        self.cur.execute('SELECT COUNT(*) FROM task_info WHERE completed = 1')
        count_result = self.cur.fetchone()[0]
        self.total_completed = count_result

        # If no CSV, skip the rest
        if self.df is None or len(self.df) == 0:
            self.accepted_top_percent = 0
            self.avg_actual_duration = None
            self.avg_estimated_duration = None
            self.avg_feedback_score = None
            return (
                self.total_completed,
                self.accepted_top_percent,
                self.avg_actual_duration,
                self.avg_estimated_duration,
                self.avg_feedback_score
            )
        # 2) Percent of accepted top suggestion
        accepted_top_series = self.df['accepted_top_suggestion'].fillna(False)
        self.accepted_top_percent = accepted_top_series.sum() / len(accepted_top_series) * 100

        # 3) Average actual duration
        actual_duration_series = self.df['actual_duration'].dropna()
        self.avg_actual_duration = actual_duration_series.mean() if len(actual_duration_series) > 0 else None

        # 4) Average estimated duration
        est_duration_series = self.df['est_duration'].dropna()
        self.avg_estimated_duration = est_duration_series.mean() if len(est_duration_series) > 0 else None
        
        # 5) Avg feedback score
        feedback_series = self.df["feedback"].dropna()
        self.avg_feedback_score = feedback_series.mean() if len(feedback_series) > 0 else None
            
        return (
            self.total_completed,
            self.accepted_top_percent,
            self.avg_actual_duration,
            self.avg_estimated_duration,
            self.avg_feedback_score
        )


    def task_completion_trends(self, window_size=5):
        if self.df is None:
            raise ValueError("No CSV data loaded for analysis.")

        #Copy df so the original doesn't change
        df = self.df.copy()

        df['created_time'] = pd.to_datetime(df['created_time'], errors='coerce')
        df['started_time'] = pd.to_datetime(df['started_time'], errors='coerce')
        df['completed_time'] = pd.to_datetime(df['completed_time'], errors='coerce')

        df = df.dropna(subset=['completed_time', 'actual_duration'])

        # Time-based columns
        df['completed_day'] = df['completed_time'].dt.date
        df['completed_week'] = df['completed_time'].dt.isocalendar().week
        df['completed_month'] = df['completed_time'].dt.month
        df['completed_hour'] = df['completed_time'].dt.hour
        df['completed_weekday'] = df['completed_time'].dt.day_name()

        # Grouping counts
        self.daily_counts = df.groupby('completed_day').size()
        self.weekly_counts = df.groupby('completed_week').size()
        self.hourly_counts = df.groupby('completed_hour').size()
        self.weekday_counts = df.groupby('completed_weekday').size()

        # Category duration mean
        self.avg_duration_by_category = df.groupby('category')['actual_duration'].mean()

        # Rolling average duration
        df_sorted = df.sort_values('completed_time')
        df_sorted['rolling_avg_duration'] = (
            df_sorted['actual_duration'].rolling(window=window_size).mean()
        )

        self.df_sorted = df_sorted  # store for plotting later
  
        return {
            'daily_counts': self.daily_counts,
            'weekly_counts': self.weekly_counts,
            'hourly_counts': self.hourly_counts,
            'weekday_counts': self.weekday_counts,
            'avg_duration_by_category': self.avg_duration_by_category,
            'rolling_avg_duration': df_sorted[['completed_time', 'rolling_avg_duration']]
        }
