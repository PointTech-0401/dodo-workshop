# 後端資料寫入 - 記憶體 MCP 工具

from memory.local_memory import LocalMemory

memory = LocalMemory()


def read_memory():
    """讀取所有記憶內容"""
    return memory.load()


def update_memory(key: str, value: str):
    """更新記憶中的特定欄位"""
    return memory.update_memory(key, value)

