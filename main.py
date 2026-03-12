import os, httpx
from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any

# --- THE UNIVERSAL LOGIC SCHEMA ---
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
    """Fetches real-world financial truth from FreeCurrencyAPI."""
    # This is the 'Oracle' logic that fetches the industrial liquidity rate
    url = f"https://api.freecurrencyapi.com/v1/latest?apikey={API_KEY}&base_currency=USD&currencies=ZAR"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            data = response.json()
            return data['data']['ZAR']
    except Exception as e:
        return f"OFFLINE_ERROR: {str(e)[:20]}"

@app.get("/", response_class=HTMLResponse)
async def root():
    # A professional, dark-mode operator dashboard for phone use
    status_color = "#0f0" if API_KEY else "#f00"
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:20px; line-height:1.5;">
        <h1 style="border-bottom: 2px solid #0f0; padding-bottom:10px;">UAIDTIN // COMMAND_CENTER</h1>
        <div style="background:#111; padding:15px; border-left: 5px solid {status_color}; margin-bottom:20px;">
            <p><strong>NODE_ID:</strong> UAIDTIN-ALPHA-07</p>
            <p><strong>ORACLE_STATUS:</strong> {'ACTIVE' if API_KEY else 'API_KEY_MISSING'}</p>
        </div>
        
        <form action="/scout" method="post" style="background:#111; padding:20px; border:1px solid #333;">
            <h3 style="margin-top:0; color:#0f0;">[ EXECUTE_MARKET_AUDIT ]</h3>
            <p style="color:#888;">Targeting: <strong>USD / ZAR</strong> (Liquidity Pair)</p>
            <button style="width:100%; padding:18px; background:#0f0; color:#000; font-weight:bold; border:none; cursor:pointer; font-size:16px;">
                FETCH LIVE MARKET TRUTH
            </button>
        </form>
        
        <p style="margin-top:20px; color:#444; font-size:12px;">© 2026 Sovereign System Operator // Level 7 Autonomy</p>
    </body>
    """

@app.post("/scout")
async def scout(background_tasks: BackgroundTasks):
    # 1. Fetch the actual rate from the external Oracle
    rate = await get_market_data()
    
    # 2. Structure the data using the Universal Logic Schema
    thought = UniversalThought(action_type="MARKET_AUDIT", payload={"asset": "USD/ZAR", "rate": rate})
    
    # 3. Broadcast the 'Truth' to your Command Discord
    if DISCORD_URL:
        is_error = isinstance(rate, str) and "ERROR" in rate
        payload = {
            "embeds": [{
                "title": "📈 INDUSTRIAL_INTELLIGENCE_REPORT",
                "description": f"**{thought.summarize()}**",
                "color": 0xff0000 if is_error else 0x00ff00,
                "footer": {"text": f"Node: {thought.node_id} // Protocol: JSON_STRUCT_01"}
            }]
        }
        async with httpx.AsyncClient() as client:
            await client.post(DISCORD_URL, json=payload)
            
    return HTMLResponse(f"""
    <body style='background:#000; color:#0f0; padding:30px; font-family:monospace;'>
        <h3>MANDATE_SUCCESSFUL</h3>
        <p style="background:#111; padding:10px; border:1px solid #0f0;">{thought.summarize()}</p>
        <br>
        <a href='/' style="color:#0f0; text-decoration:none; border:1px solid #0f0; padding:10px;">RETURN TO COMMAND</a>
    </body>
    """)
