from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1",
    tags=["Health"]
)


@router.get("/health")
async def health_check():
    return {
        "success": True,
        "application": "NeuroPilot AI",
        "status": "Healthy",
        "message": "NeuroPilot backend is running successfully"
    }