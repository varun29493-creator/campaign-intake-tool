"""Submission Validator"""
from datetime import datetime

def validate_submission(data: dict) -> list:
    warnings = []
    start = data.get("campaign_start_date", "")
    end = data.get("campaign_end_date", "")
    if start and end:
        try:
            s = datetime.fromisoformat(start)
            e = datetime.fromisoformat(end)
            if e <= s: warnings.append({"level": "error", "field": "campaign_end_date", "message": "End date must be after start date"})
            if s < datetime.now(): warnings.append({"level": "warning", "field": "campaign_start_date", "message": "Start date is in the past"})
        except: pass
    
    budget = data.get("budget", 0)
    line_items = data.get("line_items", [])
    line_total = sum(li.get("estimated_cost", 0) or 0 for li in line_items)
    if line_total > 0 and abs(line_total - budget) > 1:
        warnings.append({"level": "warning", "field": "budget", "message": f"Line item total ({line_total}) != header budget ({budget})"})
    
    if data.get("category") == "NE":
        if not data.get("ne_sub_category"): warnings.append({"level": "warning", "field": "ne_sub_category", "message": "NE campaigns should have a sub-category"})
        if not data.get("ne_pl_code"): warnings.append({"level": "warning", "field": "ne_pl_code", "message": "NE campaigns should have a PL code"})
    
    for i, li in enumerate(line_items):
        if li.get("deal_type") == "SOV" and not li.get("sov_percentage"):
            warnings.append({"level": "error", "field": f"line_items[{i}].sov_percentage", "message": "SOV packages require a takeover percentage"})
    return warnings

# 
