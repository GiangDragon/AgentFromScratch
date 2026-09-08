tool_schema = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate mathematical expressions accurately.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression, e.g. '(120 * 1.15) / 3'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type" : "function",
        "function" : {
            "name" : "current_date_and_time",
            "description" : "Return current date and time of this computer in ISO format"
        },
        "parameters" : {
            "type" : "object",
            "properties" : {},
            "required" : [],
        }
    }
]