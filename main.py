import ollama
from tools import *
from tools.execute import execute_tool
from tools.schema import tool_schema

messages = [
    {"role": "system", "content": "You are a helpful assistant. Use tools to get real-time information when needed."},
    {"role": "user", "content": "What time is it"},
]

tools = tool_schema

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
        print(tool_call)
        tool_result = execute_tool(tool_call.function.name, tool_call.function.arguments)
        messages.append({
            "role" : "tool",
            "tool_name" : tool_call.function.name,
            "content" : tool_result,
        })

print(messages)






