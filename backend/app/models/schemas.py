from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class SubmitPayload(BaseModel):
    doc_id: str
    fields: Dict[str, Any]

class DocumentResponse(BaseModel):
    doc_id: str
    case_id: str
    doc_type: str
    filename: str
    file_url: str
    extracted_payload: Dict[str, Any]
    processing_mode: str
    status: str

class CaseResponse(BaseModel):
    case: Dict[str, str]
    documents: List[DocumentResponse]
