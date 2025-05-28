from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Global variable to track API lock status
api_locked = False

class LockStatusResponse(BaseModel):
    locked: bool
    message: str

@router.get("/config/lock-status", response_model=LockStatusResponse)
async def get_lock_status():
    return LockStatusResponse(
        locked=api_locked,
        message="API is locked" if api_locked else "API is unlocked"
    )

@router.post("/config/toggle-lock", response_model=LockStatusResponse)
async def toggle_lock():
    global api_locked
    api_locked = not api_locked
    return LockStatusResponse(
        locked=api_locked,
        message="API is now locked" if api_locked else "API is now unlocked"
    )
