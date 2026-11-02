from fastapi import FastAPI

from backend.routes.healthy import router as health_router
from backend.routes.chat import router as chat_router
from backend.routes.media import router as media_router
from backend.routes.history import router as history_router
from backend.routes.documents import router as documents_router

from backend.core.database import create_tables


app = FastAPI(
    title="NeuroPilot AI",
    description="Multimodal Agentic AI Assistant",
    version="1.0.0"
)


create_tables()


app.include_router(health_router)
app.include_router(chat_router)
app.include_router(media_router)
app.include_router(history_router)
app.include_router(documents_router)


@app.get("/")
async def home():

    return {
        "success": True,
        "message": "Welcome to NeuroPilot AI"
    }