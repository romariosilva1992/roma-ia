from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from agents.writer import (
    AIConfigurationError,
    AIProviderError,
    AITimeoutError,
)
from core.config import settings
from core.orchestrator import RomaOrchestrator
from modules.feedback import FeedbackLearner

app = FastAPI(title=settings.PROJECT_NAME, version="0.1.0")
orchestrator = RomaOrchestrator()
feedback_learner = FeedbackLearner()
web_page = Path(__file__).parent / "static" / "index.html"


class ChapterCreateRequest(BaseModel):
    chapter_title: str = Field(min_length=1, max_length=200)
    topic_context: str = Field(min_length=1, max_length=20_000)
    custom_style: dict[str, str] | None = None


class ChapterCreateResponse(BaseModel):
    chapter_title: str
    draft: str


class AssistantChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=20_000)


class AssistantCommandRequest(BaseModel):
    command: str = Field(min_length=1, max_length=5_000)
    chapter_title: str = Field(default="", max_length=200)
    topic_context: str = Field(default="", max_length=20_000)
    draft: str = Field(default="", max_length=100_000)
    custom_style: dict[str, str] | None = None
    history: list[AssistantChatMessage] = Field(default_factory=list, max_length=10)


class AssistantCommandResponse(BaseModel):
    response: str


class ChapterFeedbackRequest(BaseModel):
    prompt_context: str = Field(min_length=1, max_length=20_000)
    generated_text: str = Field(min_length=1, max_length=100_000)
    human_edited_text: str = Field(min_length=1, max_length=100_000)


class ChapterFeedbackResponse(BaseModel):
    status: str
    total_records: int


@app.get("/", include_in_schema=False)
def home_page() -> FileResponse:
    return FileResponse(web_page, media_type="text/html")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/book/create", response_model=ChapterCreateResponse)
def create_chapter(request: ChapterCreateRequest) -> ChapterCreateResponse:
    try:
        draft = orchestrator.generate_chapter_pipeline(
            request.chapter_title,
            request.topic_context,
            request.custom_style,
        )
    except AIConfigurationError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except AITimeoutError as error:
        raise HTTPException(status_code=504, detail=str(error)) from error
    except AIProviderError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
    return ChapterCreateResponse(chapter_title=request.chapter_title, draft=draft)


@app.post(
    "/api/v1/assistant/command",
    response_model=AssistantCommandResponse,
)
def run_assistant_command(
    request: AssistantCommandRequest,
) -> AssistantCommandResponse:
    style_prompt = orchestrator.style_manager.get_style_prompt(request.custom_style)
    try:
        response = orchestrator.writer.command(
            command=request.command,
            chapter_title=request.chapter_title,
            topic_context=request.topic_context,
            draft=request.draft,
            style_prompt=style_prompt,
            history=[message.model_dump() for message in request.history],
        )
    except AIConfigurationError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except AITimeoutError as error:
        raise HTTPException(status_code=504, detail=str(error)) from error
    except AIProviderError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
    return AssistantCommandResponse(response=response)


@app.post("/api/v1/chapter/feedback", response_model=ChapterFeedbackResponse)
def submit_chapter_feedback(
    request: ChapterFeedbackRequest,
) -> ChapterFeedbackResponse:
    feedback_learner.log_edit(
        request.prompt_context,
        request.generated_text,
        request.human_edited_text,
    )
    return ChapterFeedbackResponse(
        status="recorded",
        total_records=feedback_learner.count_records(),
    )