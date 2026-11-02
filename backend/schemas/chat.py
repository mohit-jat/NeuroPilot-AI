from typing import Literal
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):

    message: str = Field(
        min_length=1,
        max_length=2000
    )

    input_type: Literal["text", "image", "audio"] = "text"
    thread_id: str = "neuropilot-default"
