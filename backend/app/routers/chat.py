from fastapi import APIRouter
from app.database import documents_db

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.get("/")
async def chat_assistant(query: str):
    q = query.lower()
    matched_docs = []
    
    for doc in documents_db:
        payload_str = str(doc["extracted_payload"]).lower()
        if q in doc["case_id"].lower() or q in payload_str or ("invoice" in q and doc["doc_type"] == "invoice") or ("agreement" in q and doc["doc_type"] == "legal_agreement"):
            matched_docs.append(doc)
            
    if not matched_docs:
        return {"reply": "I couldn't find any documents or cases matching that specific entity, value, or criteria."}
        
    reply = "Here is the data found for your query: \n\n"
    for doc in matched_docs:
        reply += f"📄 **Document ({doc['doc_type'].upper()})** bound to Tag **{doc['case_id']}**:\n"
        for k, v in doc["extracted_payload"].items():
            reply += f"- **{k.replace('_', ' ').title()}**: {v}\n"
        reply += f"- **Current Status**: {doc['status']}\n\n"
        
    return {"reply": reply}
