from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ChatMode(str, Enum):
    qa = "qa"
    explain_term = "explain-term"
    simplify = "simplify"


class UploadResponse(BaseModel):
    session_id: str = Field(..., description="Server-generated session identifier")
    filename: Optional[str]
    chunk_count: int
    character_count: int


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=3)
    mode: ChatMode = ChatMode.qa


class ChatResponse(BaseModel):
    answer: str
    chunks: List[str]
