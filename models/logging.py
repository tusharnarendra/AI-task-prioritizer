"""Recording data about user's interactions with the suggested to do list, to help train ML models to give more personalized suggested to do list
"""

import csv
import os

filename = "tasks_log.csv"
fieldnames = [
    "task_id",
    "category",
    "importance",
    "est_duration",
    "energy_at_creation",
    "created_time",
    "started_time",
    "completed_time",
    "actual_duration",
    "delay_before_start",
    "feedback",
    "accepted_top_suggestion"
]

#What the user inputed for the task
def log_task_creation(task_id, user_energy, timestamp, importance, estimated_duration, category):
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        # Write a new row
        writer.writerow({
            "task_id": task_id,
            "category": category,
            "importance": importance,
            "est_duration": estimated_duration,
            "energy_at_creation": user_energy,
            "created_time": timestamp
        })

#Actual statistics of the users interaction
def log_task_completion(task_id, start_time=None, completed_time=None, actual_duration=None, delay_before_start=None, user_feedback=None, accepted_top_suggestion=None):
    #Update an existing task row with completion stats.

    if not os.path.isfile(filename):
        return 

    rows = []
    with open(filename, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["task_id"] == str(task_id):
                row["started_time"] = start_time
                row["completed_time"] = completed_time
                row["actual_duration"] = actual_duration
                row["delay_before_start"] = delay_before_start
                row["feedback"] = user_feedback
                row["accepted_top_suggestion"] = accepted_top_suggestion
            rows.append(row)

    # Write back all rows
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    