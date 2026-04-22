from fastapi import APIRouter,Depends,HTTPException, Header
from app.services.user_service import get_user, update_location, update_fcm_token
from app.services.auth_service import verify_firebase_token

router = APIRouter(prefix="/users",tags = ["Users"])

def get_current_user(authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    return verify_firebase_token(token)


@router.get("/me")
def get_me(user=Depends(get_current_user)):
    data = get_user(user["uid"])
    if not data:
        raise HTTPException(status_code=404, detail="User not found")
    return data

@router.patch("/location")
def update_user_location(lat: float, lng: float, user=Depends(get_current_user)):
    return update_location(user["uid"], lat, lng)


@router.post("/fcm-token")
def update_token(fcm_token: str, user=Depends(get_current_user)):
    return update_fcm_token(user["uid"], fcm_token)