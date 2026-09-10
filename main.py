import ollama
import asyncio
from tools import *
from tools.execute import execute_tool
from tools.schema import tool_schema
from agent.loop import loop
from context.context import build_system_prompt


messages = [
    {"role": "system", "content": build_system_prompt()},
    {"role": "user", "content": "Help me wrote a program that substract two numbers, save it in ~/AgentWorkspace/sub.py"},
]

tools = tool_schema

#While loop main
await loop(
    messages=messages,
    tools=tools,
)

print(messages)






