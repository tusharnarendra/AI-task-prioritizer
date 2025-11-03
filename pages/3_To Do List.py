import streamlit as st
from database.db import init_db, delete_task, complete_task, list_tasks
from logic.ranking import rank_tasks

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
            col_task, col_buttons = st.columns([5, 1])
            with col_task:
                st.markdown(task_text, unsafe_allow_html=True)
                st.markdown(f"<span style='color:gray'>{secondary_text}</span>", unsafe_allow_html=True)
                
            with col_buttons:
                btn_col1, btn_col2 = st.columns([1, 1])
                with btn_col1:
                    if not completed and st.button("✅", key=f"complete_{task_id}"):
                        complete_task(task_id)
                with btn_col2:
                    if st.button("❌", key=f"delete_{task_id}"):
                        delete_task(task_id)
        st.markdown(f"**Score:** {current_task['priority_score']:.2f}")
        st.markdown(f"💡 *Why this:* {current_task['why_this']}")