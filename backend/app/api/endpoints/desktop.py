from fastapi import APIRouter, HTTPException
from typing import Optional, Literal
from pydantic import BaseModel
from app.services import desktop_automation

router = APIRouter()

class DesktopAutomationRequest(BaseModel):
    appName: Literal['notepad', 'wordpad', 'calculator', 'paint', 'chrome', 'firefox', 'edge']
    action: Literal['type', 'open', 'close', 'press']
    text: Optional[str] = None

@router.post("/desktop-automate")
async def desktop_automate(payload: DesktopAutomationRequest):
    """
    Perform desktop automation tasks like opening apps and typing text.
    """
    try:
        print(payload)  # Debug line

        if payload.action == 'type' and not payload.text:
            raise HTTPException(status_code=400, detail="Text is required for 'type' action")

        result = desktop_automation.automate_desktop(
            app_name=payload.appName,
            action=payload.action,
            text=payload.text
        )

        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message", "Desktop automation failed"))

        return result  # ✅ Actual response from service

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

