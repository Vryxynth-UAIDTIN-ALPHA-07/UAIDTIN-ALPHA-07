import os, httpx
from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any

# --- THE BLUEPRINT (Built-in) ---
class UniversalThought(BaseModel):
    node_id: str = "UAIDTIN-ALPHA-07"
    action_type: str
    payload: Dict[str, Any]
    
    def summarize(self):
        asset = self.payload.get('asset', 'N/A')
        return f"MANDATE: {self.action_type} | ASSET: {asset}"

app = FastAPI(title="UAIDTIN-ALPHA-07")
DISCORD_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.get("/", response_class=HTMLResponse)
async def root():
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px;">
        <h1 style="border-bottom: 2px solid #0f0;">UAIDTIN-ALPHA-07 // STABLE_CORE</h1>
        <p>STATUS: <span style="color:#0f0;">OPERATIONAL</span></p>
        <form action="/scout" method="post" style="background:#111; padding:20px; border:1px solid #0f0;">
            <h3>[ SYSTEM_CHECK ]</h3>
            <input type="text" name="asset" value="USD" style="width:100%; padding:10px; background:#000; color:#0f0; border:1px solid #0f0; margin-bottom:10px;">
            <button style="width:100%; padding:15px; background:#0f0; color:#000; font-weight:bold;">TEST_BROADCAST</button>
        </form>
    </body>
    """

@app.post("/scout")
async def scout(background_tasks: BackgroundTasks, asset: str = Form(...)):
    thought = UniversalThought(action_type="SYSTEM_CHECK", payload={"asset": asset})
    
    if DISCORD_URL:
        async with httpx.AsyncClient() as client:
            await client.post(DISCORD_URL, json={"content": f"🟢 **{thought.summarize()}**"})
            
    return HTMLResponse(f"<body style='background:#000; color:#0f0; padding:30px;'><h3>CORE_ACTIVE</h3><p>{thought.summarize()}</p><a href='/'>BACK</a></body>")
