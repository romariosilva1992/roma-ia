import json
from pathlib import Path


class FeedbackLearner:
    def __init__(self, storage_path: str = "data/feedback_logs.jsonl"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def log_edit(
        self, prompt_context: str, generated_text: str, human_edited_text: str
    ) -> None:
        record = {
            "context": prompt_context,
            "generated": generated_text,
            "edited": human_edited_text,
        }
        with self.storage_path.open("a", encoding="utf-8") as feedback_file:
            feedback_file.write(json.dumps(record, ensure_ascii=False) + "\n")

    def count_records(self) -> int:
        if not self.storage_path.exists():
            return 0
        with self.storage_path.open("r", encoding="utf-8") as feedback_file:
            return sum(1 for line in feedback_file if line.strip())