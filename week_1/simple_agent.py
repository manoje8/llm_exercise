import ollama


class Agent:
    def __init__(self, data, choose):
        self.prompt = data
        self.choose = choose

    system_prompt = """
        You are a helpful technical tutor who answers questions about programming, software engineering, data science and LLMs
    """

    def messages_for(self):
        user_prompt = "Please give a detailed explanation to the following question:" + self.prompt
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]

    def response(self):
        print("Loading...")
        response = ollama.chat(model='llama3.2', messages=self.messages_for())
        return response['message']['content']

