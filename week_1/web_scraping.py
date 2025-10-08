import os

import openai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from google import genai
from openai import OpenAI

load_dotenv(override=True)

choose = int(input("Which model do you want to use? \n 1. GEMINI\n 2. OPEN API\n>> "))

key = ""
if choose == 1:
    key = "GEMINI_API_KEY"
elif choose == 2:
    key = "OPENAI_API_KEY"

api_key = os.getenv(key)

if not api_key:
    print("No API key was found")
elif api_key.strip() != api_key:
    print("An API key was found, but it look like it might have some space or tab character")
else:
    print("Good! API key found")


openai = OpenAI()

class Website:
    def __init__(self, url):
        self.url = url

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No Title found"
        for irrelevant in soup.body(['script', 'style', 'img', 'input']):
            irrelevant.decompose()

        self.text = soup.body.get_text(separator="\n", strip=True)
        links = [link.get('href') for link in soup.find_all('a')]
        self.links = [link for link in links if link]

    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"

    def user_prompt(self):
        user_prompt = f'You are looking at a website titled {self.title}'
        user_prompt += "\nThe contents of this website is as follows; \
        please provide a short summary of this website in markdown. \
        If it includes news or announcements, then summarize these too.\n\n"
        user_prompt += self.text

        return user_prompt

    def system_prompt(self):
        system_prompt = "You are an assistant that analyzes the contents of a website \
                            and provides a short summary, ignoring text that might be navigation related. \
                            Respond in markdown."
        return system_prompt

    def messages_for(self):
        return [
            {"role": "system", "content": self.system_prompt()},
            {"role": "user", "content": self.user_prompt()}
        ]

    def summarize(self):
        user_response = self.user_prompt()
        result = None
        if choose == 1:
            print("GEMINI Loading...")
            response = genai.Client().models.generate_content(
                model="gemini-2.5-flash",
                contents=user_response
            )
            result = response.text
        elif choose == 2:
            print('OPEN AI Loading...')
            response = openai.chat.completions.create(
                model= 'gpt-4o-mini',
                messages = self.messages_for()
            )
            result = response.choices[0].message.content
        return result


