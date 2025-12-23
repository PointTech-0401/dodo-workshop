# tool definitions

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": (
                "Get current weather information for a given city. "
                "Useful when the user talks about mood, plans, or daily activities."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        #"description":  "City name."
                        "description": "City name in English (e.g. Taipei, Tokyo). If the user provides a Chinese name, translate it to English."
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_memory",
            "description": (
                "讀取使用者的個人資料與記憶內容。"
                "當需要了解使用者是誰、他的喜好、或之前說過什麼時使用。"
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_memory",
            "description": (
                "記住或更新使用者的個人資訊。"
                "當使用者告訴你與他相關的事情時，主動使用此工具儲存。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "資訊的類別 (例如: '姓名', '年齡', '愛好', '喜歡的食物', '居住地', '不喜歡的食物', '用藥資訊', '醫生講的話')"
                    },
                    "value": {
                        "type": "string",
                        "description": "要記住的內容 (繁體中文)"
                    }
                },
                "required": ["key", "value"]
            }
        }
    }
]
