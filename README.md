# 🦤 Dodo Workshop - AI 陪伴助手

> 一個用 Python 打造的 AI 聊天機器人，具備記憶功能和天氣查詢能力！
> 
> 適合初學者學習 AI Agent 和 MCP (Model Context Protocol) 的入門專案。

---

## 📋 目錄

- [這是什麼？](#-這是什麼)
- [功能介紹](#-功能介紹)
- [事前準備](#-事前準備)
- [安裝步驟](#-安裝步驟)
- [執行程式](#-執行程式)
- [進階：內網 SSE 模式](#-進階內網-sse-模式)
- [專案結構說明](#-專案結構說明)
- [兩種版本差異](#-兩種版本差異)
- [常見問題](#-常見問題)

---

## 🤔 這是什麼？

這是一個 **AI 陪伴助手**，它可以：
- 🗣️ 和你聊天
- 🧠 記住你告訴它的事情（姓名、喜好等）
- 🌤️ 查詢世界各地的天氣

本專案提供 **兩種版本**：
1. **基礎版** - 使用 Function Calling（適合入門）
2. **MCP 版** - 使用 Model Context Protocol（進階架構）

---

## ✨ 功能介紹

| 功能 | 說明 | 範例對話 |
|------|------|----------|
| 💬 聊天 | 像朋友一樣陪你聊天 | 「今天好累喔」 |
| 🧠 記憶 | 自動記住你分享的資訊 | 「我叫小明，喜歡吃拉麵」 |
| 🌤️ 天氣 | 查詢任何城市的天氣 | 「台北天氣如何？」 |

---

## 📦 事前準備

在開始之前，請確認你的電腦已經安裝以下工具：

### 1️⃣ 安裝 Python（需要 3.12 以上版本）

前往 [Python 官網](https://www.python.org/downloads/) 下載並安裝。

安裝完成後，打開終端機（Windows 按 `Win + R`，輸入 `cmd`），輸入：
```bash
python --version
```
如果顯示 `Python 3.12.x` 就代表安裝成功！

### 2️⃣ 安裝 uv（Python 套件管理工具）

在終端機輸入：

**Windows (PowerShell)：**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux：**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

安裝完成後，重新開啟終端機，輸入：
```bash
uv --version
```
如果顯示版本號就代表安裝成功！

### 3️⃣ 取得 OpenAI API Key

1. 前往 [OpenAI Platform](https://platform.openai.com/api-keys)
2. 註冊或登入帳號
3. 點選「Create new secret key」建立金鑰
4. 複製金鑰（只會顯示一次，請妥善保存！）

### 4️⃣ 取得天氣 API Key（免費）

1. 前往 [OpenWeatherMap](https://openweathermap.org/api)
2. 註冊帳號
3. 到 [API Keys 頁面](https://home.openweathermap.org/api_keys) 複製你的 API Key

---

## 🚀 安裝步驟

### Step 1：下載專案

```bash
git clone https://github.com/your-username/dodo-workshop.git
cd dodo-workshop
```

或者直接下載 ZIP 檔案並解壓縮。

### Step 2：安裝相依套件

```bash
uv sync
```

這會自動建立虛擬環境並安裝所有需要的套件。

### Step 3：設定環境變數

在專案根目錄建立 `.env` 檔案：

**Windows (PowerShell)：**
```powershell
New-Item .env -ItemType File
```

**macOS / Linux：**
```bash
touch .env
```

然後用記事本或任何文字編輯器打開 `.env`，貼上以下內容：

```env
OPENAI_API_KEY=你的OpenAI金鑰貼在這裡
WEATHER_API_KEY=你的天氣API金鑰貼在這裡
```

> ⚠️ **注意**：不要有空格，也不要加引號！

**範例：**
```env
OPENAI_API_KEY=sk-proj-abc123xyz456...
WEATHER_API_KEY=a1b2c3d4e5f6...
```

---

## ▶️ 執行程式

### 方法一：基礎版（Function Calling）

```bash
uv run python app.py
```

畫面會顯示：
```
AI Companion is ready. Type 'exit' to quit.

User: 
```

現在你可以開始和 AI 聊天了！

### 方法二：MCP 版（Model Context Protocol）

```bash
uv run python app_fastmcp.py
```

畫面會顯示：
```
🚀 正在啟動 FastMCP Agent...
✅ 已連接 MCP Server: mcp_server/tools_server.py
   載入 3 個工具
   - get_weather: 取得指定城市的即時天氣資訊...
   - read_memory: 讀取使用者的個人資料與記憶內容。...
   - update_memory: 記住或更新使用者的個人資訊。...

==================================================
🤖 FastMCP 陪伴助手已啟動！
   輸入 'exit' 或 'quit' 離開
==================================================

User: 
```

### 對話範例

```
User: 我叫小明
AI: 你好小明！很高興認識你～我已經把你的名字記下來了！有什麼想聊的嗎？

User: 台北天氣如何
🔧 呼叫 MCP 工具: get_weather
   參數: {'city': 'Taipei'}
   結果: 天氣概況: clear sky, 溫度: 22.5°C, 濕度: 75%
AI: 小明，台北現在天氣很好呢！晴朗的天空，溫度約 22.5 度，蠻舒適的～

User: 再見
🤖 再見！期待下次見面~
```

---

## 🌐 進階：內網 SSE 模式

MCP 支援透過網路連線，讓 Client 和 Server 可以在**不同電腦**上執行。這對團隊協作或部署到伺服器非常有用！

### 連線模式比較

| 模式 | 說明 | 使用場景 |
|------|------|----------|
| **stdio** | 本地模式，Client 自動啟動 Server | 開發、測試 |
| **SSE** | 網路模式，Server 獨立運行 | 內網部署、團隊共用 |

### 架構圖

```
【本地模式 - stdio（預設）】
┌────────────────────────────────────────┐
│            同一台電腦                   │
│  ┌─────────┐  subprocess  ┌──────────┐ │
│  │ Client  │◀────────────▶│  Server  │ │
│  └─────────┘    stdio     └──────────┘ │
└────────────────────────────────────────┘

【內網模式 - SSE】
┌─────────────┐                ┌─────────────┐
│   電腦 A     │                │   電腦 B     │
│  (Server)   │    HTTP/SSE    │  (Client)   │
│ ┌─────────┐ │◀──────────────▶│ ┌─────────┐ │
│ │ MCP     │ │  192.168.x.x   │ │  Agent  │ │
│ │ Server  │ │                │ │         │ │
│ └─────────┘ │                │ └─────────┘ │
└─────────────┘                └─────────────┘
```

### 使用方式

#### Step 1：在電腦 A 啟動 MCP Server

打開終端機，進入專案目錄，執行：

```bash
uv run python mcp_server/tools_server.py --sse 0.0.0.0 8234
```

畫面會顯示：
```
🌐 MCP Server 啟動於 http://0.0.0.0:8234/sse
```

> 💡 **參數說明：**
> - `--sse`：啟用 SSE 模式
> - `0.0.0.0`：監聽所有網路介面（讓其他電腦可以連入）
> - `8234`：使用的 Port 號

> ⚠️ **注意**：Server 要保持執行，不要關閉這個終端機視窗！

#### Step 2：查詢電腦 A 的 IP 位址

**Windows：**
```powershell
ipconfig
```
找到「IPv4 位址」，例如：`192.168.1.168`

**macOS / Linux：**
```bash
ifconfig
# 或
ip addr
```

#### Step 3：在電腦 B 連接 MCP Server

```bash
uv run python app_fastmcp.py http://192.168.1.168:8234/sse
```

> 把 `192.168.1.168` 換成電腦 A 的實際 IP 位址

畫面會顯示：
```
🚀 正在啟動 FastMCP Agent...
✅ 已連接 MCP Server: http://192.168.1.168:8234/sse
   載入 3 個工具
   - get_weather: 取得指定城市的即時天氣資訊...
   - read_memory: 讀取使用者的個人資料與記憶內容。...
   - update_memory: 記住或更新使用者的個人資訊。...

==================================================
🤖 FastMCP 陪伴助手已啟動！
==================================================
```

現在電腦 B 的 Agent 會透過網路呼叫電腦 A 的工具！

### 連線方式總整理

| 連線目標 | 指令範例 |
|---------|---------|
| 本地腳本 | `uv run python app_fastmcp.py` |
| 內網 SSE | `uv run python app_fastmcp.py http://192.168.1.168:8234/sse` |
| 本機 SSE | `uv run python app_fastmcp.py http://localhost:8234/sse` |

### 常見問題

#### Q: 連線被拒絕 (Connection refused)

**可能原因：**
1. Server 沒有啟動
2. IP 位址打錯
3. Port 被防火牆擋住

**解決方法：**
1. 確認 Server 終端機有顯示「🌐 MCP Server 啟動於...」
2. 用 `ping 192.168.1.168` 測試網路是否通
3. 暫時關閉防火牆測試，或開放 8000 Port

#### Q: Server 的 `.env` 設定

SSE 模式下，**環境變數需要設定在 Server 那台電腦**，不是 Client。

因為工具（天氣查詢）是在 Server 上執行的！

---

## 📁 專案結構說明

```
dodo-workshop/
├── 📄 app.py                 # 基礎版主程式
├── 📄 app_fastmcp.py         # MCP 版主程式
├── 📄 .env                   # 環境變數（API 金鑰）
├── 📄 memory.json            # AI 的記憶儲存檔
├── 📄 pyproject.toml         # 專案設定檔
│
├── 📁 agent/                 # Agent 核心邏輯
│   ├── agent.py              # 基礎版 Agent
│   ├── agent_fastmcp.py      # MCP 版 Agent
│   └── prompt.py             # AI 的人設提示詞
│
├── 📁 agent_tool/            # 工具函式（基礎版使用）
│   ├── tools.py              # 工具定義
│   ├── weather.py            # 天氣查詢
│   └── storage.py            # 記憶讀寫
│
├── 📁 mcp_server/            # MCP Server（MCP 版使用）
│   └── tools_server.py       # FastMCP 工具伺服器
│
├── 📁 llm/                   # LLM 呼叫
│   └── client.py             # OpenAI API 封裝
│
└── 📁 memory/                # 記憶管理
    └── local_memory.py       # 本地記憶實作
```

---

## 🔄 兩種版本差異

| 比較項目 | 基礎版 (`app.py`) | MCP 版 (`app_fastmcp.py`) |
|---------|-------------------|---------------------------|
| 工具呼叫方式 | 直接呼叫 Python 函式 | 透過 MCP 協定呼叫 |
| 架構 | 單一程式 | Client-Server 分離 |
| 擴充性 | 需修改程式碼 | 可動態新增 Server |
| 適合場景 | 學習、小專案 | 生產環境、團隊協作 |
| 程式碼 | `agent/agent.py` | `agent/agent_fastmcp.py` |

### 什麼是 MCP？

**MCP (Model Context Protocol)** 是 Anthropic 公司制定的開放標準，用於讓 AI Agent 與外部工具溝通。

簡單來說：
- **基礎版**：AI 直接呼叫程式裡的函式
- **MCP 版**：AI 透過網路協定呼叫獨立的「工具伺服器」

```
【基礎版】
┌─────────────────────────┐
│        app.py           │
│  AI ──直接呼叫──▶ 工具   │
└─────────────────────────┘

【MCP 版】
┌───────────┐  MCP協定  ┌───────────┐
│  Client   │◀────────▶│  Server   │
│  (AI)     │          │  (工具)    │
└───────────┘          └───────────┘
```

---

## ❓ 常見問題

### Q1: 出現 `OPENAI_API_KEY` 錯誤

**錯誤訊息：**
```
openai.AuthenticationError: Incorrect API key provided
```

**解決方法：**
1. 確認 `.env` 檔案存在於專案根目錄
2. 確認 API Key 格式正確（以 `sk-` 開頭）
3. 確認沒有多餘的空格或引號

---

### Q2: 出現 `WEATHER_API_KEY` 錯誤

**錯誤訊息：**
```
錯誤：未設定 WEATHER_API_KEY 環境變數
```

**解決方法：**
確認 `.env` 檔案中有設定 `WEATHER_API_KEY`

---

### Q3: 天氣查詢失敗

**錯誤訊息：**
```
無法取得 xxx 的天氣資訊
```

**解決方法：**
- 城市名稱必須用**英文**（例如：Taipei、Tokyo、New York）
- 中文城市名稱不支援

---

### Q4: 找不到模組錯誤

**錯誤訊息：**
```
ModuleNotFoundError: No module named 'openai'
```

**解決方法：**
```bash
uv sync
```

---

### Q5: MCP 版無法連接

**錯誤訊息：**
```
Connection refused
```

**解決方法：**
確認 `mcp_server/tools_server.py` 路徑正確（注意是 `mcp_server` 不是 `mcp_servers`）

---

## 🎓 學習資源

- [OpenAI API 文件](https://platform.openai.com/docs)
- [MCP 官方文件](https://modelcontextprotocol.io/)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)

---

## 📝 授權

MIT License

---

## 🙋 有問題嗎？

歡迎開 Issue 或 Pull Request！

Happy Coding! 🚀
