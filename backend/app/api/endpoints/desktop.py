from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel
from app.services import desktop_automation

router = APIRouter()

class DesktopAutomationRequest(BaseModel):
    app_name: str
    action: str
    text: Optional[str] = None

@router.post("/desktop-automate")
async def desktop_automate(request: DesktopAutomationRequest):
    """
    Perform desktop automation tasks like opening apps and typing text.
    
    - **app_name**: Name of the application (e.g., 'notepad', 'wordpad')
    - **action**: Action to perform ('open', 'close', 'type')
    - **text**: Text to type (required for 'type' action)
    """
    try:
        # Validate action
        valid_actions = ['open', 'close', 'type']
        if request.action not in valid_actions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid action. Must be one of: {', '.join(valid_actions)}"
            )
        
        # Validate text is provided for 'type' action
        if request.action == 'type' and not request.text:
            raise HTTPException(
                status_code=400,
                detail="Text is required for 'type' action"
            )
        
        result = desktop_automation.automate_desktop(
            app_name=request.app_name,
            action=request.action,
            text=request.text
        )
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message", "Desktop automation failed"))
            
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
