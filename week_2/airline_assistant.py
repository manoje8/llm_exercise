import json

import ollama


class AirAssistance:

    system_message = """You are a helpful assistant for an Airline called FlightAI.
    Give short, courteous answers, no more than 1 sentence.
    Always be accurate. If you don't know the answer, say so.
    
    When using tools:
        - For ticket prices, ONLY use the get_ticket_price tool with ONLY the destination_city parameter
        - Example: Customer: "How much to London?" → Use tool with {"destination_city": "london"}
        - Do NOT include airports, dates, or other parameters
    """

    ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}

    def get_ticket_price(self, destination_city):
        city = destination_city.lower()
        return self.ticket_prices.get(city, "Unknown")


    tools = [
        {
            "name": "get_ticket_price",
            "description": "Get the price of a return ticket to the destination city. Call this whenever you need to know the ticket price, for example when a customer asks 'How much is a ticket to this city'",
            "parameters": {
                "type": "object",
                "required": [
                    "destination_city"
                ],
                "properties": {
                    "destination_city": {
                        "type": "string",
                        "description": "The city that the customer wants to travel to"
                    },
                },
                "additionalProperties": False
            }
        }
    ]

    def chat(self, message):
        messages = [
            { "role" : "system", "content": self.system_message},
            { "role": "user", "content": message}
        ]
        print(messages)
        response = ollama.chat(model="llama3.2", messages=messages, tools=self.tools, options={"temperature": 0})

        msg = response['message']

        if "tool_calls" in msg:
            tool_call = msg['tool_calls'][0]

            if not tool_call['function'].get('name'):
                tool_call['function']['name'] = 'get_ticket_price'

            response, city = self.handle_tool_calls(tool_call)
            messages.append({
                "role": "assistant",
                "content": "",
                "tool_calls": msg['tool_calls']
            })
            messages.append(response)

            response = ollama.chat(model="llama3.2", messages=messages, options={"temperature": 0})

            print("trial", response)


        print("---FINAL---", response)
        return response['message']['content']

    def handle_tool_calls(self, tool_call):
        print("tools calls: ", tool_call)
        arguments = tool_call["function"]["arguments"]
        print("Arguments: ", arguments)
        city = arguments.get('destination_city' )
        price = self.get_ticket_price(city)
        response = {
            "role": "tools",
            "content": json.dumps({ "destination_city": city, "price": price}),
        }

        return response, city