tool_schema = [
    #calculator schema
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
    #datetime
    {
        "type" : "function",
        "function" : {
            "name" : "current_date_and_time",
            "description" : "Return current date and time of this computer in ISO format",
            "parameters" : {
                "type" : "object",
                "properties" : {},
                "required" : [],
            }
        },
    },
    #file system 
    {
        "type" : "function",
        "function" : {
            "name" : "read_file",
            "description" : "read a file and return utf-8 encoded content",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "path" : {
                        "type" : "string",
                        "description" : "direct path to the file"
                    }
                },
                "required" : ["path"],
            }
        },
    },
    {
        "type" : "function",
        "function" : {
            "name" : "write_file",
            "description" : "Write content to a file",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "path" : {
                        "type" : "string",
                        "description" : "direct path to the file"
                    },
                    "content" : {
                        "type" : "string",
                        "description" : "content that is going to be write in the file"
                    }
                },
                "required" : ["path", "content"],
            }
        },
    },
]