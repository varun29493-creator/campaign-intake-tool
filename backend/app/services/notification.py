"""Notification service - Slack alerts"""
import httpx
from app.config import settings

async def notify_adops_new_submission(submission):
    if not settings.SLACK_WEBHOOK_URL: return
    message = {
        "channel": settings.SLACK_CHANNEL,
        "text": f"📥 *New Campaign Submission*\n*{submission.campaign_name}*\nCategory: {submission.category} | Event: {submission.event_type} - {submission.event_name}\nBudget: INR {submission.budget:,.0f} | Lines: {len(submission.line_items_json)}\nSubmitted by: {submission.submitted_by}\nID: `{submission.id}`"
    }
    async with httpx.AsyncClient() as client:
        await client.post(settings.SLACK_WEBHOOK_URL, json=message)

async def notify_am_status_update(submission):
    if not settings.SLACK_WEBHOOK_URL: return
    emoji = {"Completed": "✅", "In Progress": "🔄", "Clarification Needed": "❓"}.get(submission.status, "📋")
    message = {"text": f"{emoji} *Campaign Status Update*\n*{submission.campaign_name}*\nStatus: {submission.status}\nID: `{submission.id}`"}
    async with httpx.AsyncClient() as client:
        await client.post(settings.SLACK_WEBHOOK_URL, json=message)
