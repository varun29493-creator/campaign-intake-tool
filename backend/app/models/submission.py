"""SQLAlchemy Models"""
from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, Text
from sqlalchemy.sql import func
from app.db.database import Base
import uuid
from datetime import datetime

def generate_id():
    return f"SUB-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(String, primary_key=True, default=generate_id)
    status = Column(String, default="Ready for Ad Ops")
    assigned_to = Column(String, nullable=True)
    
    # Header fields
    category = Column(String, nullable=False)
    advertiser = Column(String, nullable=False)
    client = Column(String)
    product_category = Column(String)
    campaign_objective = Column(String)
    campaign_name = Column(String, nullable=False)
    creative_type = Column(String)
    landing_page = Column(String)
    campaign_start_date = Column(DateTime)
    campaign_end_date = Column(DateTime)
    event_type = Column(String)
    event_name = Column(String)
    budget = Column(Float)
    primary_goal = Column(String)
    primary_goal_value = Column(String)
    secondary_goal = Column(String)
    secondary_goal_value = Column(String)
    opportunity_id = Column(String)
    po_number = Column(String)
    account_executive = Column(String)
    account_manager = Column(String)
    ne_sub_category = Column(String)
    ne_pl_code = Column(String)
    is_test_campaign = Column(String, default="N")
    
    # JSON fields
    line_items_json = Column(JSON)
    asins_json = Column(JSON)
    csd_output_json = Column(JSON)
    comments_json = Column(JSON, default=list)
    
    # Metadata
    submitted_by = Column(String)
    submitted_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

# 
