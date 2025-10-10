import json
import ollama
import openai
import requests
from bs4 import BeautifulSoup
from google import genai



class Website:
    def __init__(self, url, choose):
        self.url = url
        self.choose = choose

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
        if self.choose == 1:
            print("GEMINI Loading...")
            response = genai.Client().models.generate_content(
                model="gemini-2.5-flash",
                contents=user_response
            )
            return response.text
        elif self.choose == 2:
            print('OPEN AI Loading...')
            response = openai.chat.completions.create(
                model= 'gpt-4o-mini',
                messages = self.messages_for()
            )
            result = response.choices[0].message.content
            return result
        elif self.choose == 3:
            print("OLLAMA Loading...")
            result = ollama.chat(model="llama3.2", messages=self.messages_for())
            return result['message']['content']

    def link_system_prompt(self):
        return (
            "You are given a list of links from a company's website. "
            "Your task is to identify which links are relevant to include in a company brochure "
            "(e.g., About, Company, Careers, Team, Leadership, News, Contact). "
            "Exclude Terms of Service, Privacy, and email links.\n\n"
            "Respond *only* with valid JSON, following this format:\n"
            "{\n"
            '  "links": [\n'
            '    {"type": "about page", "url": "https://example.com/about"},\n'
            '    {"type": "careers page", "url": "https://example.com/careers"}\n'
            "  ]\n"
            "}"
        )

    def get_links_user_prompt(self, website):
        user_prompt = f"Here is the list of links on the website of {website.url} - "
        user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
    Do not include Terms of Service, Privacy, email links.\n"
        user_prompt += "Links (some might be relative links):\n"
        user_prompt += "\n".join(website.links)
        return user_prompt

    def get_links(self, url):
        website = Website(url, self.choose)
        contents = self.link_system_prompt() + self.get_links_user_prompt(website)
        if self.choose == 3:
            response = ollama.chat(
                model='llama3.2',
                messages=[
                    {"role": "system", "content": self.link_system_prompt()},
                    {"role": "user", "content": self.get_links_user_prompt(website)}
                ],
            )
            jsonValue = response['message']['content']
            # Convert JSON string to dictionary
            if isinstance(jsonValue, str):
                jsonValue = json.loads(jsonValue)
            return jsonValue
        else:
            response = genai.Client().models.generate_content(
                model="gemini-2.5-flash",
                contents=contents
            )
            raw_text = response.text.strip()
            # Try to parse JSON safely
            try:
                start = raw_text.find('{')
                end = raw_text.rfind('}') + 1
                json_text = raw_text[start:end]
                data = json.loads(json_text)
            except Exception as e:
                print("⚠️ Error parsing JSON:", e)
                return {"links": []}

            return data

    def get_all_details(self, url):
        result = "Landing page:\n"
        result += Website(url, self.choose).get_contents()
        links = self.get_links(url)
        print("Found links:", links)
        for link in links["links"]:
            result += f"\n\n{link['type']}\n"
            result += Website(link["url"], self.choose).get_contents()
        return result

