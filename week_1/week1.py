import streamlit as st

from week_1.simple_chat import Chat
from week_1.web_scraping import Website


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
            chat = Chat(user_input, model['model_choice'])
            st.markdown(chat.response())
            st.stop()
        else:
            st.warning("Please enter a message.")