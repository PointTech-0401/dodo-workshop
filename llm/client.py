# OpenAI client wrapper

import os
from openai import OpenAI
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

# 從環境變數取得 API 金鑰
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def chat_completion(messages, tools=None):
    kwargs = {
        "model": "gpt-4.1-mini",
        "messages": messages
    }

    # 如果有提供 tools 才傳入相關參數
    # MCP 的結果送回 chat completion 的時候是沒有帶 tools 的，所以 tools 是 None，設定 tool_choice = "auto" 會導致錯誤
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"

    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message