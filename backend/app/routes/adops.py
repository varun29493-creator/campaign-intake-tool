"""Ad Ops dashboard routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.auth.midway import require_adops
from app.models.submission import Submission
from app.schemas.submission import AssignRequest, StatusUpdateRequest, CommentRequest
from app.services.notification import notify_am_status_update
from datetime import datetime

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db), user: dict = Depends(require_adops)):
    total = db.query(Submission).count()
    pending = db.query(Submission).filter(Submission.status == "Ready for Ad Ops").count()
    in_progress = db.query(Submission).filter(Submission.status == "In Progress").count()
    clarification = db.query(Submission).filter(Submission.status == "Clarification Needed").count()
    completed = db.query(Submission).filter(Submission.status == "Completed").count()
    return {"total": total, "pending": pending, "in_progress": in_progress, "clarification": clarification, "completed": completed}

@router.get("/submissions")
def get_all_submissions(status: str = None, category: str = None, event_type: str = None, assigned_to: str = None, db: Session = Depends(get_db), user: dict = Depends(require_adops)):
    query = db.query(Submission)
    if status: query = query.filter(Submission.status == status)
    if category: query = query.filter(Submission.category == category)
    if event_type: query = query.filter(Submission.event_type == event_type)
    if assigned_to: query = query.filter(Submission.assigned_to == assigned_to)
    return query.order_by(Submission.submitted_at.desc()).all()

@router.get("/submissions/{submission_id}")
def get_submission_detail(submission_id: str, db: Session = Depends(get_db), user: dict = Depends(require_adops)):
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub: raise HTTPException(status_code=404, detail="Not found")
    return sub

@router.patch("/submissions/{submission_id}/assign")
async def assign_submission(submission_id: str, data: AssignRequest, db: Session = Depends(get_db), user: dict = Depends(require_adops)):
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub: raise HTTPException(status_code=404, detail="Not found")
    sub.assigned_to = data.assigned_to
    if sub.status == "Ready for Ad Ops": sub.status = "In Progress"
    db.commit()
    return {"message": "Assigned", "assigned_to": data.assigned_to, "status": sub.status}

@router.patch("/submissions/{submission_id}/status")
async def update_status(submission_id: str, data: StatusUpdateRequest, db: Session = Depends(get_db), user: dict = Depends(require_adops)):
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub: raise HTTPException(status_code=404, detail="Not found")
    sub.status = data.status
    if data.comment:
        comments = sub.comments_json or []
        comments.append({"author": user["alias"], "message": data.comment, "type": "status_change", "timestamp": datetime.now().isoformat()})
        sub.comments_json = comments
    db.commit()
    await notify_am_status_update(sub)
    return {"message": "Status updated", "status": sub.status}

@router.post("/submissions/{submission_id}/comments")
async def add_comment(submission_id: str, data: CommentRequest, db: Session = Depends(get_db), user: dict = Depends(require_adops)):
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub: raise HTTPException(status_code=404, detail="Not found")
    comments = sub.comments_json or []
    comments.append({"author": user["alias"], "message": data.message, "comment_type": data.comment_type, "timestamp": datetime.now().isoformat()})
    sub.comments_json = comments
    if data.comment_type == "clarification": sub.status = "Clarification Needed"
    db.commit()
    return {"message": "Comment added", "comments": sub.comments_json}

# 
