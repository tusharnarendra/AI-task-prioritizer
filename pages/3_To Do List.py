import streamlit as st
from database.db import init_db, delete_task, complete_task, list_tasks, highest_score
from logic.ranking import rank_tasks
from datetime import datetime
from models.logging import log_task_completion
import pandas as pd
import os

init_db()
st.title("Today's To Do List 📋")

# Fetch tasks
rows = list_tasks(include_completed=False)
tasks_list = [
    {
        'id': r[0],
        'title': r[1],
        'category': r[2],
        'importance': r[3],
        'est_duration': r[4],
        'due_date': r[6],
        'energy_level': r[7],
        'completed': r[9],
    }
    for r in rows
]

# Compute priority scores and attach to each task
for task in tasks_list:
    score, why_this = rank_tasks( 
        task['importance'],
        task['est_duration'],
        task['energy_level'],
        task['due_date']
    )
    task['priority_score'] = score
    task['why_this'] = why_this


# Sort tasks by priority_score in descending order
tasks_list_sorted = sorted(tasks_list, key=lambda t: t['priority_score'], reverse=True)

if not rows:
    st.info("No tasks. Add one in the Add Task page!")
else:
    for current_task in tasks_list_sorted:
        task_id = current_task['id']
        title = current_task['title']
        category = current_task['category']
        importance = current_task['importance']
        est_duration = current_task['est_duration']
        due_date = current_task['due_date']
        completed = current_task['completed']
        
        # Completed/incomplete
        status_emoji = "✅" if completed else "⏳"
        
        # Task text
        task_text = f"{status_emoji} **{title}**"
        
        # Additional info
        secondary_text = f"Category: `{category}` | Importance: **{importance}** | Est: `{est_duration} min` | Energy: `{current_task['energy_level']}`"
        if due_date:
            secondary_text += f" | Due: `{due_date}`"
        
        # Display in card-like container
        with st.container():
            st.markdown("---")  # separator
            col_task, col_buttons = st.columns([6, 3])
            with col_task:
                st.markdown(task_text, unsafe_allow_html=True)
                st.markdown(f"<span style='color:gray'>{secondary_text}</span>", unsafe_allow_html=True)
                
            with col_buttons:
                message = None  # ✅ To store messages shown after button actions
                btn_col1, btn_col2, btn_col3, btn_col4 = st.columns([1, 1, 1, 1])

                with btn_col1:
                    if not completed and st.button("✅", key=f"complete_{task_id}"):
                        complete_task(task_id)
                        #Compare to highest score for accepted top suggestion
                        highest_current_score = max(t['priority_score'] for t in tasks_list_sorted)
                        accepted_top = current_task['priority_score'] == highest_current_score
                        #Calculate statistics for models and insights
                        completed_time = datetime.now().isoformat()
                        if os.path.isfile("tasks_log.csv"):
                            df = pd.read_csv("tasks_log.csv")
                            match = df.loc[df["task_id"] == task_id]
                            if not match.empty and not pd.isna(match.iloc[0]["started_time"]):
                                start_time = pd.to_datetime(match.iloc[0]["started_time"])
                                completed_time_dt = pd.to_datetime(completed_time)
                                actual_duration = (completed_time_dt - start_time).total_seconds() / 60  # minutes
                                delay_before_start = (start_time - pd.to_datetime(match.iloc[0]["created_time"])).total_seconds() / 60
                            else:
                                actual_duration = None
                                delay_before_start = None
                        else:
                            actual_duration = None
                            delay_before_start = None
                       
                        #log using the function in logging.py     
                        log_task_completion(
                            task_id=task_id,
                            completed_time=completed_time,
                            actual_duration=actual_duration,
                            delay_before_start=delay_before_start,
                            user_feedback=None,
                            accepted_top_suggestion=accepted_top 
                        )
                        message = f"✅ Task {title} marked complete and logged!"                           

                with btn_col2:
                    if st.button("❌", key=f"delete_{task_id}"):
                        delete_task(task_id)
                        message = f"🗑️ Task {title} deleted!"

                with btn_col3:
                    if st.button("▶️", key=f"start_{task_id}"):
                        start_time = datetime.now().isoformat()
                        log_task_completion(
                            task_id=task_id,
                            start_time=start_time
                        )
                        message = f"▶️ Task '{title}' started!"

                with btn_col4:
                    with st.popover("💬"):
                        user_feedback = st.slider("How would you rate this to do recommendation?", 1, 5, key=f"feedback_slider_{task_id}")
                        if st.button("Submit", key=f"submit_feedback_{task_id}"):
                            log_task_completion(
                                task_id=task_id,
                                user_feedback=user_feedback
                            )
                            message = f"💬 Feedback recorded for {title}!"
                
                # ✅ Show message nicely below the buttons
                if message:
                    st.success(message)
                    
        st.markdown(f"**Score:** {current_task['priority_score']:.2f}")
        st.markdown(f"💡 *Why this:* {current_task['why_this']}")
