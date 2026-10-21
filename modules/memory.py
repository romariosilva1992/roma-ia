import json
from pathlib import Path
from typing import Any


class MemoryManager:
    def __init__(self, storage_path: str = "data/book_memory.json"):
        self.storage_path = Path(storage_path)

    def get_context(self) -> str:
        if not self.storage_path.exists():
            return ""
        data: dict[str, Any] = json.loads(self.storage_path.read_text(encoding="utf-8"))
        return str(data.get("context", ""))

    def update_context(self, context: str) -> None:
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.storage_path.write_text(
            json.dumps({"context": context}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )