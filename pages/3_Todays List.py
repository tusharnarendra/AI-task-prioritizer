import streamlit as st
from database.db import init_db, delete_task, complete_task, list_tasks

init_db()
st.title("Today's To Do List 📋")

rows = list_tasks(include_completed=False)

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
        
        #Completed/incomplete
        status_emoji = "✅" if completed else "⏳"
        
        #Including HTML tags to be used with st.markdown for better visuals
        task_text = f"{status_emoji} **{title}**"
        
        # Formatting for additional text
        secondary_text = f"Category: `{category}` | Importance: **{importance}** | Est: `{est_duration} min`"
        if due_date:
            secondary_text += f" | Due: `{due_date}`"
        
        #Card-like container
        with st.container():
            st.markdown("---")  # separator 
            col_task, col_buttons = st.columns([5, 1]) #Using columns to separate task info and buttons
            with col_task:
                st.markdown(task_text, unsafe_allow_html=True)
                st.markdown(f"<span style='color:gray'>{secondary_text}</span>", unsafe_allow_html=True)
                
            with col_buttons:
                btn_col1, btn_col2 = st.columns([1, 1])
                with btn_col1:
                    if not completed and st.button("✅", key=f"complete_{task_id}"):
                        complete_task(task_id)
                with btn_col2:
                    if st.button("❌ ", key=f"delete_{task_id}"):
                        delete_task(task_id)
