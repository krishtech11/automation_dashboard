from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
from app.services import web_automation

router = APIRouter()

class WebAutomationRequest(BaseModel):
    url: str
    username: Optional[str] = None
    password: Optional[str] = None
    search_query: Optional[str] = None

@router.post("/web-automate")
async def web_automate(request: WebAutomationRequest):
    """
    Perform web automation tasks like login and search.
    
    - **url**: The URL of the website to interact with
    - **username**: Username for login (if required)
    - **password**: Password for login (if required)
    - **search_query**: Text to search for (if any)
    """
    try:
        result = web_automation.automate_web_interaction(
            url=request.url,
            username=request.username,
            password=request.password,
            search_query=request.search_query
        )
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message", "Web automation failed"))
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
