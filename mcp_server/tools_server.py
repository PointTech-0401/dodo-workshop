# FastMCP Server - 整合所有工具
# 執行方式: uv run python mcp_server/tools_server.py

import os
import json
import requests
from pathlib import Path
from fastmcp import FastMCP
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 建立 FastMCP Server
mcp = FastMCP("dodo-workshop-tools")

# ===== 天氣工具 =====
@mcp.tool()
def get_weather(city: str) -> str:
    """取得指定城市的即時天氣資訊
    
    Args:
        city: 英文城市名稱 (例如: Taipei, Tokyo, London)
    """
    api_key = os.getenv("WEATHER_API_KEY")
    
    if not api_key:
        return "錯誤：未設定 WEATHER_API_KEY 環境變數"

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        print(f"Received weather code: {response.status_code}")

        if response.status_code != 200:
            return f"無法取得 {city} 的天氣資訊，請確認城市名稱是否正確(只支援英文城市名稱)。"
        
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]

        return f"天氣概況: {weather_desc}, 溫度: {temp}°C, 濕度: {humidity}%"
    except Exception as e:
        return f"取得天氣時發生錯誤: {str(e)}"


# ===== 記憶體工具 =====
MEMORY_FILE = Path("memory.json")

# 確保記憶檔案存在
if not MEMORY_FILE.exists():
    MEMORY_FILE.write_text("{}", encoding="utf-8")

def _get_memory_data() -> dict:
    """內部函式：取得記憶體資料"""
    if not MEMORY_FILE.exists():
        return {}
    try:
        content = MEMORY_FILE.read_text(encoding="utf-8")
        return json.loads(content) if content else {}
    except json.JSONDecodeError as e:
        raise ValueError(f"記憶檔案 JSON 格式錯誤，請檢查 {MEMORY_FILE}: {e}")


@mcp.tool()
def read_memory() -> str:
    """讀取使用者的個人資料與記憶內容。
    當需要了解使用者是誰、他的喜好、或之前說過什麼時使用。
    """
    if not MEMORY_FILE.exists():
        return "{}"
    return MEMORY_FILE.read_text(encoding="utf-8")


@mcp.tool()
def update_memory(key: str, value: str) -> str:
    """記住或更新使用者的個人資訊。
    當使用者告訴你與他相關的事情時，主動使用此工具儲存。
    
    Args:
        key: 資訊的類別 (例如: '姓名', '年齡', '愛好', '喜歡的食物', '居住地')
        value: 要記住的內容 (繁體中文)
    """
    data = _get_memory_data()
    data[key] = value
    
    MEMORY_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    
    return f"已更新記憶: {key} = {value}"


# 啟動 Server
if __name__ == "__main__":
    import sys
    
    # 根據參數選擇啟動模式
    if len(sys.argv) > 1 and sys.argv[1] == "--sse":
        # SSE 模式（內網/遠端連線）
        # 啟動: uv run python mcp_server/tools_server.py --sse
        host = sys.argv[2] if len(sys.argv) > 2 else "0.0.0.0"
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 8234
        print(f"🌐 MCP Server 啟動於 http://{host}:{port}/sse")
        mcp.run(transport="sse", host=host, port=port)
    else:
        # stdio 模式（本地連線）
        # 啟動: uv run python mcp_server/tools_server.py
        mcp.run()
