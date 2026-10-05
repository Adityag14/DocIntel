from fastapi import APIRouter
from app.database import cases_db, documents_db
from app.models.schemas import CaseResponse

router = APIRouter(prefix="/api/cases", tags=["cases"])

@router.get("/dashboard/stats")
async def get_dashboard_stats():
    total_docs = len(documents_db)
    verified = sum(1 for d in documents_db if "Verified" in d.get("status", "") or "Auto" in d.get("status", ""))
    pending = sum(1 for d in documents_db if "Pending" in d.get("status", ""))
    
    categories = {
        "bank_statement": 0,
        "legal_agreement": 0,
        "check": 0,
        "tax_return": 0,
        "invoice": 0
    }
    
    for d in documents_db:
        t = d.get("doc_type", "bank_statement")
        if t in categories:
            categories[t] += 1
        else:
            categories[t] = 1
            
    recent_activity = documents_db[-10:][::-1] if documents_db else []
    
    return {
        "total_documents": total_docs,
        "verified_count": verified,
        "pending_count": pending,
        "accuracy_rate": "98.8%",
        "avg_processing_time": "1.1s",
        "category_breakdown": categories,
        "recent_activity": recent_activity
    }

@router.get("/{case_id}", response_model=CaseResponse)
async def get_case_details(case_id: str):
    case_info = cases_db.get(case_id, {"case_id": case_id, "client_name": "Unknown Customer"})
    docs = [d for d in documents_db if d["case_id"] == case_id]
    return {"case": case_info, "documents": docs}
