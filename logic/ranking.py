"""
Basic Deterministic ranking system before incorporation of AI/ML models. 
Compute a priority score for a task based on importance, duration, energy, and due date.
Normalizes each factor to a 0–1 scale and applies weighted scoring.
"""

from database.db import list_tasks
from datetime import datetime, date

def rank_tasks(importance, estimate, energy, due):

    # Fetch all tasks to determine normalization constants
    rows = list_tasks(include_completed=False)
    tasks_list = [
        {
            'id': r[0],
            'title': r[1],
            'category': r[2],
            'importance': r[3],
            'est_duration': r[4],
            'due_date': r[6],
            'completed': r[9],
        }
        for r in rows
    ]

    # Find maximum duration and days left for normalization
    max_duration = max((t['est_duration'] for t in tasks_list), default=1)
    all_days_left = []
    for t in tasks_list:
        if t['due_date']:
            due_date_obj = datetime.strptime(t['due_date'], "%Y-%m-%d").date()
            all_days_left.append(max(0, (due_date_obj - date.today()).days))

    max_days = max(all_days_left, default=1)

    # Compute current task's due date difference
    due_date_current = datetime.strptime(due, "%Y-%m-%d").date()
    days_left_current = max(0, (due_date_current - date.today()).days)

    # Normalize values on a 1-5 scale
    importance_norm = importance / 5
    energy_norm = energy / 5  
    duration_norm = 1 - (estimate / max_duration) #Shorter tasks are given a higher score as they can be more easily completed
    due_norm = 1 - (days_left_current / max_days) #Closer due dates are given higher score

    # Weighted sum
    priority_score = (
        (importance_norm * 0.4)
        + (duration_norm * 0.15)
        + (due_norm * 0.25)
        + (energy_norm * 0.2)
    )

    # Clamp result to ensure that the result is on a 0 to 1 scale
    priority_score = max(0, min(priority_score, 1))
    return priority_score
