
import os
import uuid

from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from backend.services.chat_service import ChatService
from backend.core.database import save_document, get_document


router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Document RAG"]
)

chat_service = ChatService()

DOCUMENT_FOLDER = "uploads/documents"

os.makedirs(DOCUMENT_FOLDER, exist_ok=True)


# Upload document and save its memory
@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in [".pdf", ".txt"]:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported."
        )

    document_id = str(uuid.uuid4())

    filename = document_id + extension

    file_path = os.path.join(DOCUMENT_FOLDER, filename)

    content = await file.read()

    with open(file_path, "wb") as document:
        document.write(content)

    save_document(
        document_id,
        file.filename,
        file_path
    )

    return {
        "success": True,
        "document_id": document_id,
        "file_name": file.filename,
        "message": "Document uploaded and saved in memory."
    }


# Ask questions using saved document
@router.post("/ask-saved")
async def ask_saved_document(
    document_id: str = Form(...),
    question: str = Form(...)
):

    document = get_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found in memory."
        )

    if not os.path.exists(document["file_path"]):
        raise HTTPException(
            status_code=404,
            detail="Document file is missing."
        )

    result = await chat_service.process_message(
        document["file_path"],
        "document",
        question
    )

    return {
        "success": True,
        "document_id": document_id,
        "file_name": document["file_name"],
        "question": question,
        "answer": result["response"]
    }


# Existing upload-and-ask endpoint (kept for current frontend)
@router.post("/ask")
async def ask_document(
    file: UploadFile = File(...),
    question: str = Form(...)
):

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in [".pdf", ".txt"]:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported."
        )

    filename = str(uuid.uuid4()) + extension

    file_path = os.path.join(DOCUMENT_FOLDER, filename)

    content = await file.read()

    with open(file_path, "wb") as document:
        document.write(content)

    result = await chat_service.process_message(
        file_path,
        "document",
        question
    )

    return {
        "success": True,
        "question": question,
        "answer": result["response"]
    }
