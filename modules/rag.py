from pathlib import Path


class RAGManager:
    def __init__(self, knowledge_path: str = "data/knowledge"):
        self.knowledge_path = Path(knowledge_path)

    def retrieve(self, query: str, limit: int = 5) -> list[str]:
        if not self.knowledge_path.exists():
            return []

        terms = {term.casefold() for term in query.split() if len(term) > 2}
        ranked_documents: list[tuple[int, str]] = []
        for path in self.knowledge_path.rglob("*"):
            if path.suffix.casefold() not in {".md", ".txt"}:
                continue
            text = path.read_text(encoding="utf-8")
            score = sum(text.casefold().count(term) for term in terms)
            if score:
                ranked_documents.append((score, text.strip()))

        ranked_documents.sort(key=lambda item: item[0], reverse=True)
        return [text for _, text in ranked_documents[:limit]]