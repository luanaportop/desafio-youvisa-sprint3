# backend/src/api/router.py
from fastapi import APIRouter, UploadFile, BackgroundTasks
from pipeline.pipeline import process_document, get_process_status

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok", "message": "YOUVISA API online"}


@router.post("/upload")
async def upload_document(
    file: UploadFile,
    background_tasks: BackgroundTasks
):
    document = await process_document(file, background_tasks)
    return {"message": "document_received", "document": document}


@router.get("/status")
def get_status():
    return get_process_status()
