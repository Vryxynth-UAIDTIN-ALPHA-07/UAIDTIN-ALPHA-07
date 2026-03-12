import os, httpx
from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any

# --- THE BLUEPRINT ---
class UniversalThought(BaseModel):
    node_id: str = "UAIDTIN-ALPHA-07"
    action_type: str
    payload: Dict[str, Any]
    
    def summarize(self):
        asset = self.payload.get('asset', 'N/A')
        rate = self.payload.get('rate', 'FETCHING...')
        return f"MANDATE: {self.action_type} | ASSET: {asset} | LIVE_RATE: {rate}"

app = FastAPI(title="UAIDTIN-ALPHA-07")
DISCORD_URL = os.getenv("DISCORD_WEBHOOK_URL")
API_KEY = os.getenv("MARKET_API_KEY")

async def get_market_data():
    """Fetches real-world financial truth."""
    url = f"https://api.freecurrencyapi.com/v1/latest?apikey={API_KEY}&base_currency=USD&currencies=ZAR"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()
            return data['data']['ZAR']
    except:
        return "CONNECTION_OFFLINE"

@app.get("/", response_class=HTMLResponse)
async def root():
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px;">
        <h1 style="border-bottom: 2px solid #0f0;">UAIDTIN // MARKET_ORCHESTRATOR</h1>
        <p>ORACLE_STATUS: <span style="color:#0f0;">{'ACTIVE' if API_KEY else 'MISSING_KEY'}</span></p>
        <form action="/scout" method="post" style="background:#111; padding:20px; border:1px solid #0f0;">
            <h3>[ EXECUTE_LIVE_AUDIT ]</h3>
            <p>Targeting: USD / ZAR (Industrial Liquidity)</p>
            <button style="width:100%; padding:15px; background:#0f0; color:#000; font-weight:bold;">GET_LIVE_TRUTH</button>
        </form>
    </body>
    """

@app.post("/scout")
async def scout(background_tasks: BackgroundTasks):
    # 1. Get the real price
    rate = await get_market_data()
    
    # 2. Structure the thought
    thought = UniversalThought(action_type="MARKET_AUDIT", payload={"asset": "USD/ZAR", "rate": rate})
    
    # 3. Alert Discord
    if DISCORD_URL:
        payload = {
            "embeds": [{
                "title": "📈 INDUSTRIAL_INTELLIGENCE_REPORT",
                "description": f"**{thought.summarize()}**",
                "color": 0x00ff00 if isinstance(rate, float) else 0xff0000
            }]
        }
        async with httpx.AsyncClient() as client:
            await client.post(DISCORD_URL, json=payload)
            
    return HTMLResponse(f"<body style='background:#000; color:#0f0; padding:30px;'><h3>TRUTH_CAPTURED</h3><p>Rate: {rate}</p><a href='/'>BACK</a></body>")
