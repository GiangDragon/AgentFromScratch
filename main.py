import ollama

def execute_tool(name, arguments):
    if name == "get_current_time":
        return '{"datetime": "2025-09-13T05:18:47", "day_of_week": "Saturday"}'
    elif name == "get_weather":
        return '{"temperature": 13.2, "unit": "celsius", "conditions": "clear", "humidity": 93}'

messages = [
    {"role": "system", "content": "You are a helpful assistant. Use tools to get real-time information when needed."},
    {"role": "user", "content": "What's the current time and weather in Vancouver?"},
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and time in a specific timezone",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {"type": "string", "description": "Timezone name, e.g.America/Vancouver"}
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a specific city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
            },
        },
    },
]


#While loop main
while True:
    response = ollama.chat(
        model = "qwen3.5:4b",
        messages = messages,
        tools = tools,
    )

    assistant_message = response.message
    messages.append(assistant_message)

    if not response.message.tool_calls:
        print(response.message.content)
        break

    for tool_call in response.message.tool_calls:
        tool_result = execute_tool(tool_call.function.name, tool_call.function.arguments)
        messages.append({
            "role" : "tool",
            "tool_call_id" : tool_call.id,
            "content" : tool_result,
        })









