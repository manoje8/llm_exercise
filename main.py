import os
import streamlit as st
from jinja2.compiler import CodeGenerator

from week_1.simple_chat import Chat
from dotenv import load_dotenv
from openai import OpenAI

from week_1.web_scraping import Website
from week_1.week1 import summarize, agent
from week_2.airline_assistant import AirAssistance
from week_3.open_llm import OpenLLMModel
import time

from week_4.codeConvertor import CodeConvertor


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
    bot = AirAssistance()

    if st.button("Restart Chat"):
        st.session_state.messages = []
        st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    if prompt := st.chat_input("Say buddy! Don't hold your questions?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = bot.chat(prompt)

        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})


def week_3():
    st.header("LLM Model")
    user_input = st.text_input(label="Say something")
    if st.button("Send") and user_input.strip():
        st.info("AI model loading...")
        result = OpenLLMModel('google/gemma-3-270m-it')
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ]
        st.info("Model generating")
        output = result.generate(messages)
        st.markdown(output)

def week_4():
    st.title("Python → C++ Converter")
    convertor = CodeConvertor("LLAMA")
    pi = """
    import time

    def calculate(iterations, param1, param2):
        result = 1.0
        for i in range(1, iterations+1):
            j = i * param1 - param2
            result -= (1/j)
            j = i * param1 + param2
            result += (1/j)
        return result

    start_time = time.time()
    result = calculate(200_000_000, 4, 1) * 4
    end_time = time.time()

    print(f"Result: {result:.12f}")
    print(f"Execution Time: {(end_time - start_time):.6f} seconds")
    """
    cols1, cols2 = st.columns(2)
    with cols1:
        cols1.header("Python Code")
        py_input = st.text_area(
            "Enter your Python code here:",
            value=pi,
            height="content"
        )


    cols2.header("C++ Code")
    if st.button("Convert"):
        with cols2:
            result = convertor.convert(py_input)
            output = st.empty()
            collected_text = ""
            for chunk in result:
                if "message" in chunk and "content" in chunk["message"]:
                    collected_text += chunk["message"]["content"]
                    output.text(collected_text)





if __name__ == "__main__":
    st.set_page_config(layout="wide")
    col1, col2 = st.columns([1,3], gap="large")

    with col1:

        st.title("LLM practice")
        week = st.selectbox(
            "Choose the weekly exercise?",
            ("Week 1", "Week 2", "Week 3", "Week 4")
        )
    with col2:
        if week == "Week 1":
            week1()
        elif week == "Week 2":
            week_2()
        elif week == "Week 3":
            week_3()
        elif week == "Week 4":
            week_4()
        else:
            st.warning("No exercises")
