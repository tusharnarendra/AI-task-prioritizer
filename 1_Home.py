import streamlit as st
from database.db import init_db, add_task, delete_task, complete_task, list_tasks, update_task_predictions

init_db()
st.set_page_config(
    page_title="Home",
    page_icon="👋"
)

st.title("AI task prioritizer ")
st.sidebar.success("Select a page above.")

