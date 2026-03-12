# --- SOVEREIGNTY DECLARATION ---
# NODE_ID: UAIDTIN-ALPHA-07 | PROTOCOL: DISCORD_COMMAND_LINK
# STATUS: PROFESSIONAL_ALERTS_ACTIVE
# --- NO EXTERNAL BINDINGS ACTIVE ---

import os, httpx
from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from contracts import SmartContract 

app = FastAPI(title="UAIDTIN-ALPHA-07")
contract_engine = SmartContract()

# --- I. THE DISCORD ENVOY ---
DISCORD_URL = os.getenv("DISCORD_WEBHOOK_URL")

async def send_discord_alert(content: str):
    """Sends a clean, structured alert to your Discord Control Center."""
    if DISCORD_URL:
        payload = {
            "username": "UAIDTIN-ALPHA-07",
            "content": f"**[NODE_ALERT]** {content}"
        }
        async with httpx.AsyncClient() as client:
            await client.post(DISCORD_URL, json=payload)

# --- II. INTERFACE ---

@app.get("/", response_class=HTMLResponse)
async def root():
    status_color = "#0f0" if DISCORD_URL else "#f00"
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px;">
        <h1 style="border-bottom: 2px solid #0f0;">UAIDTIN-ALPHA-07 // DISCORD_LINK</h1>
        <p style="color:{status_color};">WEBHOOK_STATUS: {"CONNECTED" if DISCORD_URL else "DISCONNECTED"}</p>
        
        <form action="/sign-contract" method="post" style="background:#111; padding:20px; border:1px solid #0f0;">
            <h3>[ EXECUTE_SETTLEMENT ]</h3>
            <input type="number" name="amount" placeholder="Amount" required style="width:100%; margin-bottom:10px; padding:10px; background:#000; color:#0f0; border:1px solid #0f0;">
            <select name="condition" style="width:100%; margin-bottom:10px; padding:10px; background:#000; color:#0f0; border:1px solid #0f0;">
                <option value="true">VERIFIED</option>
                <option value="false">UNVERIFIED</option>
            </select>
            <button style="width:100%; padding:15px; background:#0f0; font-weight:bold; color:#000;">SIGN & ALERT DISCORD</button>
        </form>
    </body>
    """

@app.post("/sign-contract")
async def sign_contract(background_tasks: BackgroundTasks, amount: float = Form(...), condition: str = Form(...)):
    is_verified = (condition == "true")
    result = contract_engine.validate_agreement(amount, is_verified)
    
    if result['status'] == "EXECUTED":
        alert_msg = f"🟢 **Contract Executed!** \n**Amount:** {amount} \n**Timestamp:** {result.get('timestamp')}"
        background_tasks.add_task(send_discord_alert, alert_msg)
    
    return HTMLResponse(f"<body style='background:#000; color:#0f0; padding:30px;'><h3>{result['msg']}</h3><a href='/'>BACK</a></body>")
