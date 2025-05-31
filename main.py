from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI(title="Agentforce API Wrapper")

class Message(BaseModel):
    message: str

@app.post("/agentforce")
def call_agentforce(msg: Message):
    token = os.getenv("SF_ACCESS_TOKEN")
    instance_url = os.getenv("SF_INSTANCE_URL")
    if not token or not instance_url:
        raise HTTPException(status_code=500, detail="Salesforce credentials not configured.")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(
            f"{instance_url}/services/apexrest/agentforce",
            headers=headers,
            json={"message": msg.message}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
