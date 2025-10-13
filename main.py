import os
import streamlit as st
from week_1.simple_chat import Chat
from dotenv import load_dotenv
from openai import OpenAI

from week_1.web_scraping import Website
from week_1.week1 import summarize, agent
from week_2.airline_assistant import AirAssistance


def choose_model():
    load_dotenv(override=True)

    choose = st.selectbox(
        "Which model do you want to use?",
        ("GEMINI", "OPEN API", "OLLAMA"),
    )

    key = ""
    if choose == "GEMINI":
        key = "GEMINI_API_KEY"
    elif choose == "OPEN API":
        key = "OPENAI_API_KEY"
    elif choose == "OLLAMA":
        key = "OLLAMA_API"
    else:
        st.text("Invalid choice!")
        return None

    api_key = os.getenv(key)

    if not api_key:
        st.text("No API key was found")
    elif api_key.strip() != api_key:
        st.text("An API key was found, but it look like it might have some space or tab character")
    else:
        st.text("Good! API key found")

    return {
        "model_choice": choose,
        "key": key,
        "api_key": api_key
    }


def week1():
    model = choose_model()
    if not model:
        st.text("Exiting due to missing model configuration.")
        st.stop()
    choose = st.radio(
        "Which one do you want to try?",
        ("Web page summarize", "Chat Bot")
    )

    if choose == "Web page summarize":
        summarize(model)
    else:
        agent(model)

def week_2():
    assistance = AirAssistance()
    assistance.get_ticket_price("berlin")
    resp = assistance.chat("How much is a ticket to Paris?")
    st.text("completed")
    st.markdown(resp)

if __name__ == "__main__":
    st.title("LLM practice")
    week = st.selectbox(
        "Choose the weekly exercise?",
        ("Week 1", "Week 2")
    )
    if week == "Week 1":
        week1()
    else:
        week_2()
        st.text("Coming Soon")
