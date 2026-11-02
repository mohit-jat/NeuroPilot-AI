import os
import uuid
import mimetypes

from fastapi import APIRouter, UploadFile, File, HTTPException, Form

from backend.services.chat_service import ChatService


router = APIRouter(
    prefix="/api/v1/media",
    tags=["Media Upload"]
)

chat_service = ChatService()

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_media(
    file: UploadFile = File(...),
    question: str = Form(""),
    thread_id: str = Form("neuropilot-default")
):

    # Supported file types
    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/jpg",
        "audio/mpeg",
        "audio/wav",
        "audio/x-wav",
        "audio/mp4",
        "audio/ogg",
        "audio/webm",
        "audio/x-m4a"
    ]

    # Get file type
    content_type = file.content_type

    if not content_type:
        content_type, encoding = mimetypes.guess_type(
            file.filename or ""
        )

    # Validate file type
    if not content_type or content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {content_type}"
        )

    # Create unique file name
    file_extension = os.path.splitext(file.filename or "")[1]

    new_filename = str(uuid.uuid4()) + file_extension

    file_path = os.path.join(
        UPLOAD_FOLDER,
        new_filename
    )

    # Read uploaded file
    file_content = await file.read()

    # Check file size
    if len(file_content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File size must be below 10 MB"
        )

    # Save file
    with open(file_path, "wb") as uploaded_file:
        uploaded_file.write(file_content)

    # Identify input type
    if content_type.startswith("image/"):
        input_type = "image"
    else:
        input_type = "audio"

    # Send file and question to ChatService
    result = await chat_service.process_message(
        file_path,
        input_type,
        question,
        thread_id=thread_id
    )

    return {
        "success": True,
        "file_name": new_filename,
        "input_type": input_type,
        "question": question,
        "agent_response": result["response"]
    }
