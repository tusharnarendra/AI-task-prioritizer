import streamlit as st
import openai

st.title("Settings")

# Input box for API key
api_input = st.text_input("OpenAI API Key", type="password")

# Button to save key
if st.button("Save API Key"):
    if not api_input:
        st.warning("Please enter your OpenAI API Key.")
    elif not api_input.startswith("sk-"):
        st.error("Invalid API Key format. It should start with 'sk-'.")
    else:
        # Test the API key with a lightweight call
        try:
            openai.api_key = api_input
            openai.Engine.list()  # lightweight test call
            st.session_state["OPENAI_API_KEY"] = api_input
            st.success("API Key is valid and saved!")
        except Exception as e:
            st.error(f"API Key seems invalid: {e}")

# Display stored key
if "OPENAI_API_KEY" in st.session_state:
    st.info("API Key is stored in session state.")
