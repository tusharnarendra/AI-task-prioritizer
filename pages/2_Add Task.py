import streamlit as st
from database.db import add_task
from models.logging import log_task_creation
from datetime import datetime

st.title("Add a task!")

# Inputs
title = st.text_input("Task Title")
duration = st.number_input("Estimated Duration (minutes)", min_value=0, step=1)
category = st.selectbox("Category", [
    "Work", 
    "Study", 
    "Personal", 
    "Health/Fitness", 
    "Social", 
    "Hobbies/Creative", 
    "Finance/Admin", 
    "Misc"
])
importance = st.slider("Importance", 1, 5)
energy = st.slider("Energy Level", 1, 5)
due = st.date_input("Due date")

# Add button
if st.button("Add"):
    task_id = add_task(
        title=title,
        category=category,
        importance=importance,
        est_duration=duration,
        due_date=due.isoformat() if due else None,
        energy_level=energy,
        completed=0,   # new tasks are incomplete
        score=0        # default score
    )
    log_task_creation(
        task_id=task_id,
        user_energy=energy,
        timestamp=str(datetime.now()),
        importance=importance,
        estimated_duration=duration,
        category=category
    )
    st.success("Task added successfully!")
