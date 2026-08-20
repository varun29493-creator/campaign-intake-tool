"""Application configuration"""
import os

class Settings:
    APP_NAME = "Campaign Intake Tool"
    VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./campaign_intake.db")
    MIDWAY_AUTH_URL = os.getenv("MIDWAY_AUTH_URL", "https://midway-auth.amazon.com")
    MIDWAY_CLIENT_ID = os.getenv("MIDWAY_CLIENT_ID", "campaign-intake-tool")
    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")
    SLACK_CHANNEL = "#dvas-ops-intake"
    ADOPS_GROUPS = ["dvas-adops", "dvas-ops-team"]

settings = Settings()

# 
