# Agent loop（決策核心）

import json
from llm.client import chat_completion
from agent.prompt import SYSTEM_PROMPT
from memory.local_memory import LocalMemory
from agent_tool.tools import TOOLS
from agent_tool.weather import get_weather
from agent_tool.storage import read_memory, update_memory

# 建立工具名稱與函式的對照表
AVAILABLE_TOOLS = {
    "get_weather": get_weather,
    "read_memory": read_memory,
    "update_memory": update_memory
}

class CompanionAgent:
    def __init__(self):
        self.memory = LocalMemory()
        self.history = [] # 對話歷史
    
    def get_memory_content(self):
        memory_content = self.memory.load()
        return f"Memory:\n{memory_content}"

    def chat(self, user_input):
        self.history.append({"role": "user", "content": user_input})

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            #{"role": "system", "content": self.get_memory_content()} # memory 1/2
        ] + self.history

        message = chat_completion(messages, tools=TOOLS)

        if message.tool_calls:
            print(f"Tool calls got {len(message.tool_calls)} calls")
            # 逐一處理所有 tool_calls，避免遺漏造成 400 錯誤
            self.history.append(message)
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name

                if tool_name in AVAILABLE_TOOLS:
                    tool_function = AVAILABLE_TOOLS[tool_name]
                    args = json.loads(tool_call.function.arguments or "{}")
                    result = tool_function(**args)
                    print(f"Tool result ({tool_name}): {result}")
                    tool_msg_content = str(result)
                else:
                    # 未知工具也回覆一則 tool 訊息以滿足 API 要求
                    tool_msg_content = f"Unsupported tool: {tool_name}"

                self.history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_msg_content
                })

            # 工具執行完成後，重新載入記憶並生成最終回應
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                #{"role": "system", "content": self.get_memory_content()} # memory 2/2
            ] + self.history

            final = chat_completion(messages)
            self.history.append(final)
            return final.content

        self.history.append(message)
        return message.content