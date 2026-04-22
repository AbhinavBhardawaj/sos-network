from app.firebase import db
from datetime import datetime,timezone

def respond_to_alert(alert_id:str,user:dict):
    ref = db.collection("alerts").document(alert_id)
    doc = ref.get()

    if not doc.exists:
        return {"error":"Alert not found"}
    data = doc.to_dict()

    if data["posted_by_uid"] == user["uid"]:
        return {"error": "You cannot respond to your own alert"}

    if data["status"] != "active":
        return {"error": "Alert already taken or resolved"}
    
    ref.update({
        "status":"responding",
        "responder_uid": user["uid"],
        "responder_name": user.get("phone", "Volunteer"),
        "responded_at": datetime.now(timezone.utc)
    })

    return {"message":"You are now responding."}