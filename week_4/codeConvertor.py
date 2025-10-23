import ollama


class CodeConvertor:
    def __init__(self, model_name):
        self.model_name = model_name
        self.__system_message = [
            {"role": 'system',
             "content":"""
             Your task is to convert Python code into high performance C++ code.
            Respond only with C++ code. Do not provide any explanation other than occasional comments.
            The C++ response needs to produce an identical output in the fastest possible time.
             """
             }
        ]
        self.compile_command = ["clang++", "-std=c++13", "-Ofast", "-mcpu=native", "-flto=thin", "-fvisibility=hidden", "-DNDEBUG", "main.cpp", "-o", "main"]


    def user_prompt(self, code):
        message = {
            "role": 'user',
            "content": f"""
            Port this Python code to C++ with the fastest possible implementation that produces identical output in the least time.
            Your response will be written to a file called main.cpp and then compiled and executed; the compilation command is:
            {self.compile_command}
            Respond only with C++ code.
            Python code to port:
            ```python
            {code}
            ```
            """
        }
        return message

    def write_output(self, code):
        with open('week_4/main.cpp', 'w', encoding='utf-8') as f:
            f.write(code)


    def gemini_generator(self, message):
        return message

    def llama_generator(self, code):
        print("Loading...")
        self.__system_message.append(self.user_prompt(code))
        response = ollama.chat(
            model="llama3.2",
            messages=self.__system_message
        )
        result = response.message.content
        rep = result.replace('```cpp', '').replace('```', '')
        self.write_output(rep)
        return rep

    def convert(self, code):
        result = None
        if self.model_name == "LLAMA":
            result = self.llama_generator(code)
        elif self.model_name == "GEMINI":
            result = self.gemini_generator(code)
        else:
            result = "Choose different model!"
        return result




