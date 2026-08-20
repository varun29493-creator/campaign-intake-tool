"""Midway Authentication"""
from fastapi import Depends, HTTPException, Request
from app.config import settings

async def get_current_user(request: Request):
    """Extract user from Midway token/cookie"""
    if settings.DEBUG:
        return {
            "alias": "varun",
            "name": "Varun",
            "email": "varun@amazon.com",
            "groups": ["dvas-adops", "dvas-ops-team"]
        }
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    # Production: validate with Midway
    raise HTTPException(status_code=401, detail="Invalid token")

def require_adops(user: dict = Depends(get_current_user)):
    """Require Ad Ops group membership"""
    if not any(g in settings.ADOPS_GROUPS for g in user.get("groups", [])):
        raise HTTPException(status_code=403, detail="Ad Ops access required")
    return user

# 
