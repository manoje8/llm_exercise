import json

from google import genai

from week_1.web_scraping import Website


def link_system_prompt():
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

def get_links_user_prompt(website):
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt



def get_links(url):
    website = Website(url)
    contents = link_system_prompt() + get_links_user_prompt(website)
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


def get_all_details(url):
    result = "Landing page:\n"
    result += Website(url).get_contents()
    links = get_links(url)
    print("Found links:", links)
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Website(link["url"]).get_contents()
    return result
