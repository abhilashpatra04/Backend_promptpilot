# # mcp_server/utils/firebase_utils.py

from fastapi import APIRouter, HTTPException, Query, FastAPI
from pydantic import BaseModel
from google.cloud import firestore
from datetime import datetime
import os
import requests
import json

# Firestore client will be initialized lazily so the app can start even when
# Application Default Credentials (ADC) are not configured (e.g. during a
# Render deployment). Endpoints that require Firestore will return a 503 with
# a helpful message until credentials are provided.
db = None

def get_db():
    """Return a firestore.Client instance or None if credentials are not configured.

    Behavior:
    - If FIREBASE_CREDENTIALS_JSON is set, parse it and use service account creds.
    - If GOOGLE_APPLICATION_CREDENTIALS is set and points to a file, use default behavior.
    - Otherwise, attempt to create a client (this may raise); catch and return None.
    """
    global db
    if db is not None:
        return db

    try:
        # If JSON credentials are provided directly via env var, use them.
        firebase_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
        cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if firebase_json:
            from google.oauth2 import service_account
            info = json.loads(firebase_json)
            creds = service_account.Credentials.from_service_account_info(info)
            db = firestore.Client(credentials=creds, project=info.get("project_id"))
            return db

        if cred_path and os.path.exists(cred_path):
            # Let the google library pick up credentials from the file pointed to by
            # GOOGLE_APPLICATION_CREDENTIALS.
            db = firestore.Client()
            return db

        # Final attempt: try default credentials (may raise DefaultCredentialsError).
        db = firestore.Client()
        return db
    except Exception:
        # Don't raise during import. Return None so callers can handle missing creds.
        db = None
        return None


class ChatRequest(BaseModel):
    uid: str
    prompt: str
    model: str
    chat_id: str = None 
    title: str = "Untitled"


class ChatResponse(BaseModel):
    reply: str
    chat_id: str


def create_new_chat(uid: str, title: str) -> str:
    client = get_db()
    if client is None:
        raise HTTPException(status_code=503, detail="Firestore is not configured. Set GOOGLE_APPLICATION_CREDENTIALS or FIREBASE_CREDENTIALS_JSON in environment.")

    doc_ref = client.collection("conversations").document()
    doc_ref.set({
        "id": doc_ref.id,
        "title": title,
        "createdAt": firestore.SERVER_TIMESTAMP,
        "uid": uid
    })
    return doc_ref.id


def get_chat_threads(uid: str) -> list:
    client = get_db()
    if client is None:
        raise HTTPException(status_code=503, detail="Firestore is not configured. Set GOOGLE_APPLICATION_CREDENTIALS or FIREBASE_CREDENTIALS_JSON in environment.")

    threads_ref = client.collection("conversations").where("uid", "==", uid)
    threads = threads_ref.order_by("createdAt", direction=firestore.Query.DESCENDING).stream()
    return [doc.to_dict() for doc in threads]


def store_message(uid: str, chat_id: str, user_msg: str, ai_msg: str) -> bool:
    client = get_db()
    if client is None:
        raise HTTPException(status_code=503, detail="Firestore is not configured. Set GOOGLE_APPLICATION_CREDENTIALS or FIREBASE_CREDENTIALS_JSON in environment.")

    client.collection("messages").add({
        "id": str(datetime.utcnow().timestamp()),
        "conversationId": chat_id,
        "question": user_msg,
        "answer": ai_msg,
        "createdAt": firestore.SERVER_TIMESTAMP,
        "uid": uid
    })
    return True


def get_chat_messages(uid: str, chat_id: str) -> list:
    client = get_db()
    if client is None:
        raise HTTPException(status_code=503, detail="Firestore is not configured. Set GOOGLE_APPLICATION_CREDENTIALS or FIREBASE_CREDENTIALS_JSON in environment.")

    messages_ref = client.collection("messages").where("conversationId", "==", chat_id).order_by("createdAt")
    messages = messages_ref.stream()
    return [doc.to_dict() for doc in messages]
