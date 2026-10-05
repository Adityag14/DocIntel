from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models.schemas import DocumentResponse, SubmitPayload
from app.services.document_service import process_document, update_document_review
import os
import shutil

router = APIRouter(prefix="/api", tags=["documents"])

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    case_id: str = Form(...),
    client_name: str = Form(...),
    mode: str = Form("review")
):
    upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    doc_record = process_document(file.filename, case_id, client_name, mode, f"/uploads/{file.filename}", file_path)
    return doc_record

@router.post("/submit-review")
async def submit_review(payload: SubmitPayload):
    success, doc = update_document_review(payload.doc_id, payload.fields)
    if success:
        return {"status": "success", "document": doc}
    raise HTTPException(status_code=404, detail="Document not found")
