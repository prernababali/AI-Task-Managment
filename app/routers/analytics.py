from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.models import Task, Document, ActivityLog
from app.utils.auth import require_admin

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/")
def get_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    total_tasks = db.query(Task).count()
    completed_tasks = db.query(Task).filter(Task.status == "completed").count()
    pending_tasks = db.query(Task).filter(Task.status == "pending").count()
    total_documents = db.query(Document).count()
    total_searches = db.query(ActivityLog).filter(
        ActivityLog.action == "search"
    ).count()

    # ✅ Most searched queries
    most_searched = db.query(
        ActivityLog.details,
        func.count(ActivityLog.details).label("count")
    ).filter(
        ActivityLog.action == "search"
    ).group_by(
        ActivityLog.details
    ).order_by(
        func.count(ActivityLog.details).desc()
    ).limit(5).all()

    most_searched_list = [
        {"query": row.details.replace("Searched: ", ""), "count": row.count}
        for row in most_searched
    ]

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "total_documents": total_documents,
        "total_searches": total_searches,
        "most_searched_queries": most_searched_list  # ✅ Added
    }