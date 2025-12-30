import streamlit as st
import pandas as pd
import altair as alt
import os
from logic.insights_logic import UserInsights

csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tasks_log.csv"))
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "focusflow.db"))

st.title("Your Productivity Insights 📊")

insights = UserInsights(csv_path=csv_path, db_path=db_path)

total_completed, accepted_top_percent, avg_actual_duration, avg_estimated_duration, avg_feedback_score = insights.compute_overall_summary()
trends = insights.task_completion_trends()

#A few brief overall summary statistics
with st.container():
    st.subheader("Overall Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tasks Completed", total_completed)
    col2.metric("Accepted Top Suggestion %", f"{accepted_top_percent:.1f}%")
    col3.metric("Avg Feedback Score", f"{avg_feedback_score:.2f}" if avg_feedback_score else "N/A")

#Estimated vs actual duration bar chart
with st.container():
    if avg_estimated_duration and avg_actual_duration:
        duration_df = pd.DataFrame({"Metric": ["Estimated", "Actual"], "Minutes": [avg_estimated_duration, avg_actual_duration]})
        chart = (alt.Chart(duration_df).mark_bar(color='teal').encode(x='Metric', y='Minutes').properties(title="Estimated vs Actual Duration", width = 400))
        st.altair_chart(chart, use_container_width=True)

#Tasks completed per day line graph
with st.container():
    if not trends['daily_counts'].empty:
        daily_df = trends['daily_counts'].reset_index()
        daily_df.columns = ['Date', 'Count']
        daily_chart = alt.Chart(daily_df).mark_line(point=True).encode(x='Date',y='Count').properties(title="Tasks Completed Per Day")
        st.altair_chart(daily_chart, use_container_width=True)

#Tasks completed per hour bar chart distribution
with st.container():
    if not trends['hourly_counts'].empty:
        hourly_df = trends['hourly_counts'].reset_index()
        hourly_df.columns = ['Hour', 'Count']
        hourly_chart = alt.Chart(hourly_df).mark_bar(point=True).encode(x='Hour',y='Count').properties(title="Tasks Completed by Hour")
        st.altair_chart(hourly_chart, use_container_width=True)
        
#Weekly distribution
with st.container():
    if not trends['weekday_counts'].empty:
        weekday_df = trends['weekday_counts'].reset_index()
        weekday_df.columns = ['Weekday', 'Count']
        weekday_order = ["Monday", "Tuesday", "Wednesday","Thursday", "Friday", "Saturday", "Sunday"]
        weekday_chart = alt.Chart(weekday_df).mark_bar(color='green').encode(x=alt.X('Weekday', sort=weekday_order), y='Count').properties(title="Tasks Completed by Weekday")
        st.altair_chart(weekday_chart, use_container_width=True)

#Average duration ber category type
with st.container():
    if not trends['avg_duration_by_category'].empty:
        category_df = trends['avg_duration_by_category'].reset_index()
        category_df.columns = ['Category', 'Avg Duration (min)']
        category_chart = alt.Chart(category_df).mark_bar(color='purple').encode(x='Category', y='Avg Duration (min)').properties(title="Average Duration by Category")
        st.altair_chart(category_chart, use_container_width=True)

#Rollign average task duration
with st.container():
    if not trends['rolling_avg_duration'].empty:
        rolling_df = trends['rolling_avg_duration']
        rolling_chart = alt.Chart(rolling_df).mark_line(color='red').encode(x='completed_time', y='rolling_avg_duration').properties(title=f"Rolling Average Task Duration (window={5})")
        st.altair_chart(rolling_chart, use_container_width=True)
