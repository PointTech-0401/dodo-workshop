# FastMCP Agent - MCP Client 實作

import json
import asyncio
from fastmcp import Client
from llm.client import chat_completion
from agent.prompt import SYSTEM_PROMPT
from memory.local_memory import LocalMemory


class FastMCPAgent:
    def __init__(self):
        self.memory = LocalMemory()
        self.history = []
        self.client = None
        self.tools_cache = []
    
    async def connect(self, server: str):
        """連接到 FastMCP Server
        
        Args:
            server: MCP Server 位置，支援以下格式：
                - 本地腳本: "mcp_server/tools_server.py"
                - SSE 連線: "http://192.168.1.168:8234/sse"
                - Streamable HTTP: "http://192.168.1.168:8234/mcp"
        """
        self.client = Client(server)
        await self.client.__aenter__()
        
        # 取得工具清單並轉換為 OpenAI 格式
        tools_result = await self.client.list_tools()
        self.tools_cache = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                }
            }
            for tool in tools_result
        ]
        print(f"✅ 已連接 MCP Server: {server}")
        print(f"   載入 {len(self.tools_cache)} 個工具")
        for tool in tools_result:
            print(f"   - {tool.name}: {tool.description[:50]}...")
    
    def get_memory_content(self):
        """取得記憶內容"""
        memory_content = self.memory.load()
        return f"Memory:\n{memory_content}"

    async def chat(self, user_input: str) -> str:
        """與 Agent 對話
        
        Args:
            user_input: 使用者輸入
            
        Returns:
            Agent 的回應
        """
        self.history.append({"role": "user", "content": user_input})

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": self.get_memory_content()}
        ] + self.history

        # 呼叫 LLM，帶入 MCP 工具
        message = chat_completion(messages, tools=self.tools_cache)

        # 如果 LLM 決定呼叫工具
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            tool_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            
            print(f"🔧 呼叫 MCP 工具: {tool_name}")
            print(f"   參數: {args}")
            
            # 透過 MCP Client 呼叫工具
            result = await self.client.call_tool(tool_name, args)
            
            # 取得工具回傳的文字內容
            # FastMCP 回傳 CallToolResult 物件，內容在 .content 屬性中
            if result and result.content:
                result_text = result.content[0].text
            else:
                result_text = "無結果"
            print(f"   結果: {result_text}")

            # 將工具呼叫和結果加入歷史
            self.history.append(message)
            self.history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result_text
            })

            # 重新載入記憶並讓 LLM 生成最終回應
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "system", "content": self.get_memory_content()}
            ] + self.history

            final = chat_completion(messages)
            self.history.append(final)
            return final.content

        # 沒有工具呼叫，直接回傳
        self.history.append(message)
        return message.content
    
    async def close(self):
        """關閉 MCP 連線"""
        if self.client:
            await self.client.__aexit__(None, None, None)
            print("👋 已關閉 MCP 連線")
