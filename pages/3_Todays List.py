import streamlit as st
from database.db import init_db, delete_task, complete_task, list_tasks

init_db()
st.title("Today's To Do List ✅")

rows = list_tasks(include_completed=True)

if not rows:
    st.info("No tasks. Add one in the Add Task page!")
else:
    for row in rows:
        task_id = row[0]
        title = row[1]
        category = row[2]
        importance = row[3]
        est_duration = row[4]
        due_date = row[6]
        completed = row[9]

        # Task text formatting
        task_text = f"{title} | Category: {category} | Importance: {importance} | Est: {est_duration} min"
        if due_date:
            task_text += f" | Due: {due_date}"
        if completed:
            task_text = "✅ " + task_text
        else:
            task_text = "⏳ " + task_text

        # Display task text + buttons for completion and deletion
        col_task, col_buttons = st.columns([6, 1])
        with col_task:
            st.write(task_text)

        with col_buttons:
            btn_col1, btn_col2 = st.columns([1, 1])  # nested columns for buttons
            with btn_col1:
                if not completed and st.button("✅", key=f"complete_{task_id}"):
                    complete_task(task_id)
            with btn_col2:
                if st.button("❌ ", key=f"delete_{task_id}"):
                    delete_task(task_id)
