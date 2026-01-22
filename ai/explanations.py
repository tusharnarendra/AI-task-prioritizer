import openai
import streamlit as st

def gpt_reasoning(title, category, estimate, importance, energy, due):
    if "OPENAI_API_KEY" not in st.session_state:
        return None

    openai.api_key = st.session_state["OPENAI_API_KEY"]

    prompt = f"""
    Task: {title}
    Category: {category}
    Estimated duration: {estimate} minutes
    Importance: {importance}/5
    Energy level: {energy}/5
    Due date: {due}

    In 1–2 short sentences, explain how the user should prioritize this task.
    Be concise and practical.
    """

    response = openai.ChatCompletion.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": "You are a helpful productivity assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=80,
        temperature=0.5
    )

    return response.choices[0].message["content"].strip()
