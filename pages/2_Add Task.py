import streamlit as st
from database.db import add_task

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
    add_task(
        title=title,
        category=category,
        importance=importance,
        est_duration=duration,
        due_date=due.isoformat() if due else None,
        energy_level=energy,
        completed=0,   # new tasks are incomplete
        score=0        # default score
    )
    st.success("Task added successfully!")
