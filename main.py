import os
from week_1.simple_agent import Agent
from dotenv import load_dotenv
from openai import OpenAI

from week_1.web_scraping import Website


def choose_model():
    load_dotenv(override=True)

    choose = int(input("Which model do you want to use? \n 1. GEMINI\n 2. OPEN API \n3. Ollama\n>> "))

    key = ""
    if choose == 1:
        key = "GEMINI_API_KEY"
    elif choose == 2:
        key = "OPENAI_API_KEY"
    elif choose == 3:
        key = "OLLAMA_API"
    else:
        print("Invalid choice!")
        return None

    api_key = os.getenv(key)

    if not api_key:
        print("No API key was found")
    elif api_key.strip() != api_key:
        print("An API key was found, but it look like it might have some space or tab character")
    else:
        print("Good! API key found")

    return {
        "model_choice": choose,
        "key": key,
        "api_key": api_key
    }

def summarize(model):
    user_input = input("Enter the website URL you want to summarize: ").strip()

    # Ensure proper format
    if not user_input.startswith("http"):
        user_input = "https://" + user_input

    try:
        # Summarize website
        website = Website(user_input, model["model_choice"])
        print("\nWebsite Summary:\n")
        print(website.summarize())

        generate_brochure = input("\nDo you want to generate the company brochure? (y/n): ").strip().lower()
        if generate_brochure == "y":
            print("\n Generating brochure details...\n")
            details = website.get_all_details(user_input)
            print(details)

    except Exception as e:
        print(f"\n⚠️ Error occurred: {e}")

def agent(model):
    user_input = input("")
    chat = Agent(user_input, model['model_choice'])
    print(chat.response())

def main():
    model = choose_model()
    if not model:
        print("Exiting due to missing model configuration.")
        return
    # summarize(model)
    agent(model)

if __name__ == "__main__":
    main()
