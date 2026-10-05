import os
import uuid
from typing import Dict, Any, Tuple, Optional
from app.database import cases_db, documents_db
from app.services.ai_agent import analyze_document_with_ai

def process_document(file_name: str, case_id: str, client_name: str, mode: str, file_url: str, file_path: str = "") -> Dict[str, Any]:
    if case_id not in cases_db:
        cases_db[case_id] = {"case_id": case_id, "client_name": client_name}
        
    doc_id = f"DOC-{uuid.uuid4().hex[:6].upper()}"
    
    if not file_path:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_dir, "uploads", file_name)

    # Invoke Gemini LLM AI Agent for classification & extraction
    doc_type, extracted_fields = analyze_document_with_ai(file_path, file_name, client_name)

    doc_record = {
        "doc_id": doc_id,
        "case_id": case_id,
        "doc_type": doc_type,
        "filename": file_name,
        "file_url": file_url,
        "extracted_payload": extracted_fields,
        "processing_mode": mode,
        "status": "Submitted (Auto)" if mode == "auto" else "Pending Review"
    }
    
    documents_db.append(doc_record)
    return doc_record

def update_document_review(doc_id: str, fields: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]]]:
    for doc in documents_db:
        if doc["doc_id"] == doc_id:
            doc["extracted_payload"] = fields
            doc["status"] = "Submitted (Verified)"
            return True, doc
    return False, None
