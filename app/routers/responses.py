from fastapi import APIRouter,Depends,HTTPException
from app.services.response_service import respond_to_alert
from app.routers.users import get_current_user

router  = APIRouter(prefix="/alerts",tags=["Responses"])
@router.post("/{alert_id}/respond")
def respond(alert_id:str, user= Depends(get_current_user)):
    result = respond_to_alert(alert_id, user)
    
    if "error" in result:
        raise HTTPException(status_code=400,detail=result["error"])
    return result
