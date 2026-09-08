from tools import *
from tools.registry import TOOL_REGISTRY

def execute_tool(name, arguments):
    handler = TOOL_REGISTRY.get(name)
    if handler is None:
        raise ValueError(f"Unknown tool: {name}")

    return handler(**arguments)