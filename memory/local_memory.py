# JSON / SQLite 實作

import json
from pathlib import Path


class LocalMemory:
    def __init__(self, path="memory.json"):
        self.path = Path(path)
        if not self.path.exists():
            self.path.write_text("{}", encoding="utf-8")

    def load(self):
        """Return raw JSON string for the agent prompt."""
        if not self.path.exists():
            return "{}"
        return self.path.read_text(encoding="utf-8")

    def _get_data(self):
        """Helper to get dict data."""
        try:
            content = self.path.read_text(encoding="utf-8")
            return json.loads(content) if content else {}
        except json.JSONDecodeError as e:
            raise ValueError(f"記憶檔案 JSON 格式錯誤，請檢查 {self.path}: {e}")

    def update_memory(self, key: str, value: str):
        data = self._get_data()

        data[key] = value

        self.path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        return f"已更新記憶: {key} = {value}"