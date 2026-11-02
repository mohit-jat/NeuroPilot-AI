from fastapi import APIRouter
from pydantic import BaseModel

from backend.schemas.chat import ChatRequest
from backend.services.chat_service import ChatService


router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"]
)

chat_service = ChatService()


# Request model for approval
class ApprovalRequest(BaseModel):

    thread_id: str
    decision: str


@router.post("/")
async def chat(request: ChatRequest):

    result = await chat_service.process_message(
        request.message,
        request.input_type,
        thread_id=request.thread_id
    )

    return result


# API for Approve and Reject
@router.post("/approval")
async def handle_approval(request: ApprovalRequest):

    if request.decision not in ["approve", "reject"]:

        return {
            "success": False,
            "message": "Invalid approval decision."
        }

    result = await chat_service.resume_approval(
        request.thread_id,
        request.decision
    )

    return result
