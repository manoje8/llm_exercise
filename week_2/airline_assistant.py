from google import genai
from google.genai import types


class AirAssistance:

    system_message = """You are a helpful assistant for an Airline called FlightAI.
    Give short, courteous answers, no more than 1 sentence.
    Always be accurate. If you don't know the answer, say so.
    
    When using tools:
        - For greeting messages, general questions, or non-price inquiries, respond normally without tools
        - For ticket prices, ONLY use the get_ticket_price tool with ONLY the destination_city parameter
        - Example: Customer: "How much to London?" → Use tool with {"destination_city": "london"}
    """

    ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}

    def get_ticket_price(self, destination_city):
        city = destination_city.lower()
        return self.ticket_prices.get(city, "Unknown")


    get_ticket_function = {
        "name": "get_ticket_price",
        "description": "Get the price of a return ticket to the destination city. Call this whenever you need to know the ticket price, for example when a customer asks 'How much is a ticket to this city'",
        "parameters": {
            "type": "object",
            "required": [ "destination_city" ],
            "properties": {
                "destination_city": {
                    "type": "string",
                    "description": "The city that the customer wants to travel to"
                },
            },
        }
    }


    def chat(self, message):
        messages = [
            types.Content(role="model", parts=[types.Part(text=self.system_message)]),
            types.Content(role="user", parts=[types.Part(text=message)])
        ]


        client = genai.Client()
        tools = types.Tool(function_declarations=[self.get_ticket_function])
        config = types.GenerateContentConfig(tools=[tools])

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents= messages,
            config=config
        )

        if response.candidates[0].content.parts[0].function_call:
            model_resp = response.candidates[0].content
            function_call = response.candidates[0].content.parts[0].function_call
            response, city = self.handle_tool_calls(function_call)
            messages.append(model_resp)
            messages.append(response)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
            )
            return response.text

        else:
            return response.text

    def handle_tool_calls(self, tool_call):
        arguments = tool_call.args
        city = arguments.get('destination_city')
        price = self.get_ticket_price(city)
        function_response_part = types.Part.from_function_response(
            name=tool_call.name,
            response={"destination_city": city, "price": price},
        )
        response = types.Content(
            role="user",
            parts=[function_response_part]
        )

        return response, city