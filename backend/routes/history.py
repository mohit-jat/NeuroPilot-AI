from fastapi import APIRouter

from backend.core.database import (
    get_chat_history,
    clear_chat_history,
    get_all_sessions
)


router = APIRouter(
    prefix="/api/v1/history",
    tags=["Chat History"]
)


# Get all sessions for ChatGPT-style sidebar
@router.get("/sessions")
async def list_sessions():

    sessions = get_all_sessions()

    return {
        "success": True,
        "sessions": sessions
    }


# Get chat history for a specific session
@router.get("/session/{session_id}")
async def get_session_history(session_id: str):

    chats = get_chat_history(session_id=session_id)

    return {
        "success": True,
        "session_id": session_id,
        "total_chats": len(chats),
        "history": chats
    }


# Clear a specific session
@router.delete("/session/{session_id}")
async def clear_session(session_id: str):

    clear_chat_history(session_id=session_id)

    return {
        "success": True,
        "session_id": session_id,
        "message": f"Session {session_id} deleted successfully"
    }


# Get all chat history (Default/Legacy)
@router.get("/")
async def history():

    chats = get_chat_history()

    return {
        "success": True,
        "total_chats": len(chats),
        "history": chats
    }


# Clear all chat history
@router.delete("/clear")
async def clear_history():

    clear_chat_history()

    return {
        "success": True,
        "message": "All chat history cleared successfully"
    }
