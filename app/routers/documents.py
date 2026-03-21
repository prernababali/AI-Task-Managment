from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import os
from app.database import get_db
from app.models.models import Document, ActivityLog
from app.utils.auth import require_admin, get_current_user
from app.models.models import User
from app.utils.ai_search import build_index

router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = "uploads"

@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files allowed")
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)
    new_doc = Document(
        filename=file.filename,
        filepath=file_path,
        uploaded_by=current_user.id
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    log = ActivityLog(
        user_id=current_user.id,
        action="document_upload",
        details=f"Uploaded {file.filename}"
    )
    db.add(log)
    db.commit()
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
    build_index(documents_for_index)
    return {"message": "Document uploaded successfully", "doc_id": new_doc.id}

@router.get("/")
def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    docs = db.query(Document).all()
    return docs