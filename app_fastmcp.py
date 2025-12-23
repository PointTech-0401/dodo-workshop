# FastMCP 版本的主程式入口
# 執行方式: 
#   本地模式: uv run python app_fastmcp.py
#   SSE 模式: uv run python app_fastmcp.py http://192.168.1.168:8234/sse

import sys
import asyncio
from agent.agent_fastmcp import FastMCPAgent


async def main():
    agent = FastMCPAgent()
    
    # 從命令列參數取得 MCP Server 位置，預設使用本地腳本
    if len(sys.argv) > 1:
        server = sys.argv[1]  # 例如: http://192.168.1.168:8234/sse
    else:
        server = "mcp_server/tools_server.py"  # 本地模式
    
    # 連接 FastMCP Server
    print("🚀 正在啟動 FastMCP Agent...")
    await agent.connect(server)
    
    print("\n" + "=" * 50)
    print("🤖 FastMCP 陪伴助手已啟動！")
    print("   輸入 'exit' 或 'quit' 離開")
    print("=" * 50 + "\n")
    
    try:
        while True:
            user_input = input("User: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit", "bye", "掰掰", "再見"]:
                print("🤖 再見！期待下次見面~")
                break
            
            response = await agent.chat(user_input)
            print(f"AI: {response}\n")
    
    except KeyboardInterrupt:
        print("\n👋 收到中斷訊號，正在關閉...")
    
    finally:
        await agent.close()


if __name__ == "__main__":
    asyncio.run(main())
