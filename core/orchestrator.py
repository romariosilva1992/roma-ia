from agents.editor import EditorAgent
from agents.researcher import ResearcherAgent
from agents.writer import WriterAgent
from modules.memory import MemoryManager
from modules.rag import RAGManager
from modules.style import StyleManager


class RomaOrchestrator:
    def __init__(self):
        self.style_manager = StyleManager()
        self.memory_manager = MemoryManager()
        self.rag_manager = RAGManager()
        self.researcher = ResearcherAgent(self.rag_manager)
        self.writer = WriterAgent()
        self.editor = EditorAgent()

    def generate_chapter_pipeline(
        self, chapter_title: str, topic_context: str, custom_style: dict | None = None
    ) -> str:
        style_prompt = self.style_manager.get_style_prompt(custom_style)
        book_context = self.memory_manager.get_context()
        research_notes = self.researcher.research(topic_context)
        draft = self.writer.write(
            chapter_title=chapter_title,
            topic_context=topic_context,
            research_notes=research_notes,
            book_context=book_context,
            style_prompt=style_prompt,
        )
        return self.editor.review(draft)