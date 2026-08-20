"""AM-facing submission routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.auth.midway import get_current_user
from app.models.submission import Submission, generate_id
from app.schemas.submission import SubmissionCreate
from app.services.transformer import CSDTransformer
from app.services.validator import validate_submission
from app.services.notification import notify_adops_new_submission
from datetime import datetime

router = APIRouter()
transformer = CSDTransformer()

@router.post("/", status_code=201)
async def create_submission(data: SubmissionCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """AM submits a new campaign"""
    warnings = validate_submission(data.dict())
    csd_output = transformer.transform(data.dict())
    
    submission = Submission(
        id=generate_id(),
        status="Ready for Ad Ops",
        category=data.category,
        advertiser=data.advertiser,
        client=data.client,
        product_category=data.product_category,
        campaign_objective=data.campaign_objective,
        campaign_name=data.campaign_name,
        creative_type=data.creative_type,
        landing_page=data.landing_page,
        campaign_start_date=datetime.fromisoformat(data.campaign_start_date),
        campaign_end_date=datetime.fromisoformat(data.campaign_end_date),
        event_type=data.event_type,
        event_name=data.event_name,
        budget=data.budget,
        primary_goal=data.primary_goal,
        primary_goal_value=data.primary_goal_value,
        secondary_goal=data.secondary_goal,
        secondary_goal_value=data.secondary_goal_value,
        opportunity_id=data.opportunity_id,
        po_number=data.po_number,
        account_executive=data.account_executive,
        account_manager=data.account_manager,
        ne_sub_category=data.ne_sub_category,
        ne_pl_code=data.ne_pl_code,
        is_test_campaign=data.is_test_campaign,
        line_items_json=[li.dict() for li in data.line_items],
        asins_json=data.asins,
        csd_output_json=csd_output,
        submitted_by=user["alias"],
    )
    
    db.add(submission)
    db.commit()
    db.refresh(submission)
    await notify_adops_new_submission(submission)
    
    return {"id": submission.id, "status": submission.status, "campaign_name": submission.campaign_name, "warnings": warnings}

@router.get("/")
def list_submissions(status: str = None, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """List AM's own submissions"""
    query = db.query(Submission).filter(Submission.submitted_by == user["alias"])
    if status:
        query = query.filter(Submission.status == status)
    return query.order_by(Submission.submitted_at.desc()).all()

@router.get("/{submission_id}")
def get_submission(submission_id: str, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    return sub

# 
