from app.firebase import db
from datetime import datetime, timezone
from app.utils.geo import haversine_distance
from app.services.fcm_service import get_nearby_user_tokens, send_sos_notification


def create_alert(user, data):
    try:
        doc_ref = db.collection("alerts").document()

        alert = {
            "id": doc_ref.id,
            "posted_by_uid": user["uid"],
            "category": data["category"],
            "description": data.get("description", ""),
            "lat": data["lat"],
            "lng": data["lng"],
            "status": "active",
            "responder_uid": None,
            "responder_name": None,
            "created_at": datetime.now(timezone.utc),
            "responded_at": None,
            "resolved_at": None
        }

        doc_ref.set(alert)
        try:
            tokens = get_nearby_user_tokens(alert["lat"], alert["lng"])
            if tokens:   # avoid empty list crash
                send_sos_notification(tokens, alert)
        except Exception as e:
            print("Notification failed:", e)

        return alert

    except Exception as e:
        print("ERROR IN CREATE ALERT:", e)
        raise e

def get_nearby_alerts(lat, lng, radius=500):
    alerts_ref = db.collection("alerts").where("status", "==", "active")
    docs = alerts_ref.stream()

    nearby = []

    for doc in docs:
        data = doc.to_dict()

        # safety checks
        if not data.get("lat") or not data.get("lng"):
            continue

        try:
            distance = haversine_distance(lat, lng, data["lat"], data["lng"])
        except Exception as e:
            print("Distance calc error:", e)
            continue

        if distance <= radius:
            data["distance"] = int(distance)
            nearby.append(data)

    return nearby

def get_alert_by_id(alert_id):
    doc = db.collection("alerts").document(alert_id).get()

    if not doc.exists:
        return None

    return doc.to_dict()

def resolve_alert(alert_id):
    ref = db.collection("alerts").document(alert_id)
    doc = ref.get()

    if not doc.exists:
        return None

    ref.update({
        "status": "resolved",
        "resolved_at": datetime.now(timezone.utc)
    })

    return {"message": "Alert resolved"}