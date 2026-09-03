from tools.get_time import get_current_time 
import ollama

get_current_time_schema = {
    "type": "function",
    "function": {
        "name": "get_current_time",
        "description": "Get the current local date and time from the system.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
}

question = "What time is it right now ?"
system_prompt = "You are an AI Agent"
history = []

tools = [
    get_current_time_schema
]

tool_functions = {
    "get_current_time": get_current_time
}

message = []
message.append({"role" : "user", "content" : question})
message.append({"role" : "system", "content" : system_prompt})

response = ollama.chat(
    model="qwen3.5:4b",
    messages=message,
    tools=tools
)

print(response)
tool_calls = response.message.tool_calls or None

for tool_call in tool_calls:
    function_name = tool_call.function.name
    arguments = tool_call.function.arguments

    print(function_name)
    print(arguments)

    function = tool_functions[function_name]
    result = function(**arguments)
    print(result)