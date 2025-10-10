import os
import streamlit as st
from week_1.simple_agent import Agent
from dotenv import load_dotenv
from openai import OpenAI

from week_1.web_scraping import Website


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

def summarize(model):
    st.header("🌐 Webpage Summarizer")
    user_input = st.text_input("Enter the website URL you want to summarize: ")

    # Ensure proper format
    if user_input and not user_input.startswith("http"):
        user_input = "https://" + user_input

    if st.button("Send"):
        try:
            # Summarize website
            website = Website(user_input, model["model_choice"])
            st.text("\nWebsite Summary:\n")
            st.markdown(website.summarize())

            generate_brochure =  st.checkbox("Generate company brochure?")

            if generate_brochure:
                st.text("\n Generating brochure details...\n")
                details = website.get_all_details(user_input)
                st.markdown(details)
                st.stop()

        except Exception as e:
            st.text(f"\n⚠️ Error occurred: {e}")

def agent(model):
    st.header("💬 Chat Agent")
    user_input = st.text_area("Ask something:")

    if st.button("Send"):
        if user_input.strip():
            chat = Agent(user_input, model['model_choice'])
            st.markdown(chat.response())
            st.stop()
        else:
            st.warning("Please enter a message.")

def main():
    st.title("LLM practice")

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

if __name__ == "__main__":
    main()
