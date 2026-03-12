import os, httpx
from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from protocols import SovereignProtocol

# --- THE UNIVERSAL THOUGHT SCHEMA ---
class UniversalThought(BaseModel):
    action_type: str
    payload: dict
    cid: str

app = FastAPI(title="UAIDTIN-ALPHA-07")
DISCORD_URL = os.getenv("DISCORD_WEBHOOK_URL")
API_KEY = os.getenv("MARKET_API_KEY")

@app.get("/", response_class=HTMLResponse)
async def root():
    # A professional, high-contrast dashboard for Mobile Workstation use.
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:20px; border:1px solid #0f0;">
        <h1 style="border-bottom: 2px solid #0f0; padding-bottom:10px;">UAIDTIN // SOVEREIGN_NODE_07</h1>
        <div style="background:#111; padding:15px; border-left: 4px solid #0f0; margin-bottom:20px;">
            <p><strong>MISSION:</strong> TOTAL_DECOUPLING</p>
            <p><strong>PROTOCOL:</strong> P2P_NEUTRALIZATION_ACTIVE</p>
        </div>
        
        <form action="/execute-mandate" method="post" style="background:#111; padding:20px; border:1px solid #333;">
            <h3 style="margin-top:0;">[ EXECUTE_INDUSTRIAL_LOGIC ]</h3>
            <p style="color:#888;">Target: USD/ZAR Liquidity Audit</p>
            <button style="width:100%; padding:20px; background:#0f0; color:#000; font-weight:bold; border:none; cursor:pointer;">
                ACTIVATE REGENERATIVE VALUE
            </button>
        </form>
    </body>
    """

@app.post("/execute-mandate")
async def execute_mandate(background_tasks: BackgroundTasks):
    # 1. Fetch Real-World Truth (Open Source API Client)
    url = f"https://api.freecurrencyapi.com/v1/latest?apikey={API_KEY}&base_currency=USD&currencies=ZAR"
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        rate = res.json()['data']['ZAR']
    
    # 2. Apply Decentralized Protocol (Generate CID)
    data_payload = {"asset": "USD/ZAR", "rate": rate}
    cid = SovereignProtocol.generate_cid(data_payload)
    
    # 3. Broadcast to Command Mesh (Discord)
    if DISCORD_URL:
        payload = {
            "embeds": [{
                "title": f"🏛️ HEGEMONIC_MANDATE: {cid}",
                "description": f"**TRUTH_CAPTURED:** `{rate} ZAR/USD`\n**STATUS:** `SYSTEMIC_NEUTRAL_VERIFIED`",
                "color": 0x00ff00,
                "footer": {"text": f"Issuer: {SovereignProtocol.NODE_ID} // Autarchy Level 7"}
            }]
        }
        async with httpx.AsyncClient() as client:
            await client.post(DISCORD_URL, json=payload)

    return HTMLResponse(f"<body style='background:#000; color:#0f0; padding:30px;'><h3>MANDATE_CAPTURED</h3><p>CID: {cid}</p><a href='/'>RETURN</a></body>")
