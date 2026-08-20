"""Pydantic Schemas"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class LineItemSchema(BaseModel):
    inventory: Optional[str] = "O&O"
    screen: Optional[str] = "Mobile"
    channel: Optional[str] = "Amazon.in"
    deal_type: str
    package: str
    placements: Optional[str] = ""
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    ad_type_size: Optional[str] = ""
    audience_type: Optional[str] = ""
    audience_code: Optional[str] = ""
    segment_string: Optional[str] = ""
    frequency_type: Optional[str] = "Default Uncapped Frequency"
    frequency_value: Optional[str] = None
    sov_percentage: Optional[int] = None
    rate: Optional[float] = None
    impressions: Optional[int] = None
    estimated_cost: Optional[float] = None
    pacing_profile: Optional[str] = "Even"
    pacing_catchup_boost: Optional[str] = "No"

class SubmissionCreate(BaseModel):
    category: str
    advertiser: str
    client: Optional[str] = ""
    product_category: Optional[str] = ""
    campaign_objective: Optional[str] = ""
    campaign_name: str
    creative_type: Optional[str] = ""
    landing_page: Optional[str] = ""
    campaign_start_date: str
    campaign_end_date: str
    event_type: str
    event_name: str
    budget: float
    primary_goal: Optional[str] = ""
    primary_goal_value: Optional[str] = ""
    secondary_goal: Optional[str] = None
    secondary_goal_value: Optional[str] = None
    opportunity_id: Optional[str] = ""
    po_number: Optional[str] = ""
    account_executive: Optional[str] = ""
    account_manager: Optional[str] = ""
    ne_sub_category: Optional[str] = None
    ne_pl_code: Optional[str] = None
    is_test_campaign: Optional[str] = "N"
    line_items: List[LineItemSchema]
    asins: List[str] = []

class AssignRequest(BaseModel):
    assigned_to: str

class StatusUpdateRequest(BaseModel):
    status: str
    comment: Optional[str] = ""

class CommentRequest(BaseModel):
    message: str
    comment_type: str = "general"

# 
