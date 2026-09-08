import ollama

def loop(messages, tools):
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
            return messages

        for tool_call in response.message.tool_calls:
            print(tool_call)
            tool_result = execute_tool(tool_call.function.name, tool_call.function.arguments)
            messages.append({
                "role" : "tool",
                "tool_name" : tool_call.function.name,
                "content" : tool_result,
            })