from firebase_admin import auth
from app.firebase import db
from datetime import datetime, timezone

def verify_firebase_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)

        uid = decoded_token["uid"]
        phone = decoded_token.get("phone_number")

        user_ref = db.collection("users").document(uid)
        user_doc = user_ref.get()

        if not user_doc.exists:
            user_data = {
                "uid": uid,
                "phone": phone,
                "name": "",
                "fcm_token": "",
                "lat": None,
                "lng": None,
                "last_seen": datetime.now(timezone.utc),
                "skills": []
            }
            user_ref.set(user_data)
        else:
            user_ref.update({
                "last_seen": datetime.now(timezone.utc)
            })

        return {
            "uid": uid,
            "phone": phone
        }

    except Exception as e:
        raise Exception(f"Token verification failed: {str(e)}")