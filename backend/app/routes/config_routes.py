"""Configuration endpoints - serve dropdown data to frontend"""
import json, os
from fastapi import APIRouter

router = APIRouter()
CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config")

def load_config(filename):
    with open(os.path.join(CONFIG_DIR, filename)) as f:
        return json.load(f)

@router.get("/dropdowns")
def get_dropdowns():
    categories = load_config("categories.json")
    goals = load_config("goals_kpis.json")
    pacing = load_config("pacing_frequency.json")
    audiences = load_config("audience_codes.json")
    ne = load_config("ne_config.json")
    return {
        "categories": [c["code"] for c in categories["categories"]],
        "category_details": categories["categories"],
        "primary_goals": goals["primary_goals"],
        "secondary_goals": goals["secondary_goals"],
        "campaign_objectives": goals["campaign_objectives"],
        "pacing_profiles": pacing["pacing_profiles"],
        "frequency_types": pacing["frequency_types"],
        "frequency_presets": pacing["frequency_presets"],
        "audience_types": audiences["audience_types"],
        "ne_sub_categories": ne["ne_sub_categories"],
        "ne_pl_codes": ne["ne_pl_codes"]
    }

@router.get("/packages")
def get_packages():
    cpm = load_config("packages_cpm.json")
    sov = load_config("packages_sov.json")
    return {"cpm": cpm["packages"], "sov": sov["packages"]}

# 
