"""CSD Transformer - The BRAIN of the tool
Converts media plan input into CSD-ready output (Sheets 3, 4, 6)"""
import json, os
from datetime import datetime

CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config")

class CSDTransformer:
    def __init__(self):
        self.audience_codes = self._load("audience_codes.json")["audience_types"]
        self.cpm_packages = self._load("packages_cpm.json")["packages"]
        self.sov_packages = self._load("packages_sov.json")["packages"]
        self.field_map = self._load("csd_field_map.json")
        self.audience_map = {a["type"]: a["code"] for a in self.audience_codes}
        self.rate_map = {p["name"]: p["rate"] for p in self.cpm_packages}

    def _load(self, filename):
        with open(os.path.join(CONFIG_DIR, filename)) as f:
            return json.load(f)

    def transform(self, data: dict) -> dict:
        return {
            "campaign_details": self._build_campaign_details(data),
            "order_details": self._build_order_details(data),
            "asin_list": data.get("asins", [])
        }

    def _build_campaign_details(self, data: dict) -> dict:
        return {
            "basic_info": {
                "campaign_name": data.get("campaign_name", ""),
                "campaign_type": "Billable",
                "salesforce_opp_id": data.get("opportunity_id", ""),
                "portfolio": "Ungrouped"
            },
            "account_details": {
                "account_manager": data.get("account_manager", ""),
                "account_executive": data.get("account_executive", ""),
                "advertiser_category": "Non Vendor" if data.get("category") == "NE" else "Vendor",
                "product_line": data.get("product_category", "")
            },
            "billing_details": {"currency": "INR", "po_number": data.get("po_number", "")},
            "schedule": {
                "timezone": "Asia/Kolkata",
                "start_date_time": self._format_datetime(data.get("campaign_start_date")),
                "end_date_time": self._format_datetime(data.get("campaign_end_date"))
            }
        }

    def _build_order_details(self, data: dict) -> list:
        line_items = data.get("line_items", [])
        orders = []
        for i, li in enumerate(line_items[:25]):
            item = li if isinstance(li, dict) else li.dict()
            deal_type = item.get("deal_type", "")
            package_name = item.get("package", "")
            audience_type = item.get("audience_type", "")
            order = {
                "package_number": i + 1,
                "product_type": deal_type,
                "product_package": package_name,
                "start_date_time": self._format_datetime(item.get("start_date")),
                "end_date_time": self._format_datetime(item.get("end_date")),
                "requested_budget": item.get("estimated_cost", ""),
                "takeover_percentage": item.get("sov_percentage", "") if deal_type == "SOV" else "",
                "order_rate": self.rate_map.get(package_name, 0) if deal_type == "CPM" else "",
                "audience_targeting": audience_type,
                "audience_tag": self.audience_map.get(audience_type, ""),
                "targeting": item.get("segment_string", ""),
                "frequency_cap": item.get("frequency_type", ""),
                "frequency_value": item.get("frequency_value", ""),
                "pacing_profile": item.get("pacing_profile", "Even"),
                "pacing_catchup_boost": item.get("pacing_catchup_boost", "No"),
                "primary_goal": data.get("primary_goal", ""),
                "primary_goal_value": data.get("primary_goal_value", "")
            }
            orders.append(order)
        return orders

    def _format_datetime(self, dt_value) -> str:
        if not dt_value: return ""
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        if isinstance(dt_value, str):
            try: dt_value = datetime.fromisoformat(dt_value.replace("Z", "+00:00"))
            except: return dt_value
        hour = dt_value.hour % 12 or 12
        ampm = "AM" if dt_value.hour < 12 else "PM"
        return f"{dt_value.day}-{months[dt_value.month-1]} {hour}:{dt_value.minute:02d} {ampm}"

# 
