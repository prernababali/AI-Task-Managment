from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import ActivityLog, Document
from app.schemas.schemas import SearchQuery
from app.utils.auth import get_current_user
from app.utils.ai_search import search_documents, build_index
from app.models.models import User

router = APIRouter(prefix="/search", tags=["Search"])

@router.post("/")
def search(
    search_query: SearchQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    all_docs = db.query(Document).all()
    documents_for_index = []
    for doc in all_docs:
        try:
            with open(doc.filepath, "r") as f:
                text = f.read()
            documents_for_index.append({
                "id": doc.id,
                "filename": doc.filename,
                "content": text
            })
        except:
            pass
            
    if documents_for_index:
        build_index(documents_for_index)
    results = search_documents(search_query.query)
    log = ActivityLog(
        user_id=current_user.id,
        action="search",
        details=f"Searched: {search_query.query}"
    )
    db.add(log)
    db.commit()
    return {"query": search_query.query, "results": results}