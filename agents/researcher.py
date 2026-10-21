from modules.rag import RAGManager


class ResearcherAgent:
    def __init__(self, rag_manager: RAGManager):
        self.rag_manager = rag_manager

    def research(self, topic: str) -> list[str]:
        return self.rag_manager.retrieve(topic)