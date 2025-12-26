from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# =========================
# Environment Variables
# =========================
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
ZAP_SECRET = os.getenv("ZAP_SECRET")

DISCORD_API_BASE = "https://discord.com/api/v10"


# =========================
# Request Model
# =========================
class RoleRequest(BaseModel):
    secret: str
    discord_user_id: str
    role_id: str


# =========================
# Health Check (optional)
# =========================
@app.get("/")
def health_check():
    return {"status": "ok"}


# =========================
# Assign Role Endpoint
# =========================
@app.post("/assign-role")
def assign_role(data: RoleRequest):

    # Security check (Zapier secret)
    if data.secret != ZAP_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not DISCORD_BOT_TOKEN or not GUILD_ID:
        raise HTTPException(status_code=500, detail="Server not configured")

    url = f"{DISCORD_API_BASE}/guilds/{GUILD_ID}/members/{data.discord_user_id}/roles/{data.role_id}"

    headers = {
        "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.put(url, headers=headers)

    if response.status_code not in (200, 204):
        raise HTTPException(
            status_code=500,
            detail=f"Discord API error: {response.text}"
        )

    return {"success": True}

