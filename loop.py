import ollama

def loop(messages, tools):

    while True:
        response = ollama.chat(
            model = "qwen3.5:8b",
            messages = messages,
            tools = tools,
        )

        if not response.message.tool_calls:
            return response.message.content

        for tool_call in response.message.tool_calls:
            tool_result = None
            message.append()
        