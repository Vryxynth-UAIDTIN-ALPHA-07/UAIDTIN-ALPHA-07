# --- SOVEREIGNTY DECLARATION ---
# NODE_ID: UAIDTIN-ALPHA-07 | PROTOCOL: MULTI-GATEWAY
# STATUS: INDUSTRIAL_INGESTION_ACTIVE
# --- NO EXTERNAL BINDINGS ACTIVE ---

import os, datetime
from typing import List, Dict, Any
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, validator
from zoneinfo import ZoneInfo 

app = FastAPI(title="UAIDTIN-ALPHA-07", version="2026.1.12")
HARARE_TZ = ZoneInfo("Africa/Harare")

# --- I. THE MAGISTRATE (RETAINED LAW) ---
class Mandate(BaseModel):
    instruction: str
    priority: int
    @validator('instruction')
    def must_be_industrial(cls, v):
        valid_sectors = ["OPTIMIZE", "SYNC", "NODE", "LEDGER", "HARARE", "SETTLE", "GALACTIC"]
        if not any(word in v.upper() for word in valid_sectors):
            raise ValueError('LAW_BREACH: Instruction falls outside Sovereign Industrial Scope.')
        return v.upper()

# --- II. THE TELEMETRY VAULT (NEW SENSES) ---
# This stores "Pulses" from the physical world
INDUSTRIAL_LEDGER: List[Dict[str, Any]] = []

# --- III. GATEWAY ENDPOINTS ---

@app.post("/ingest-telemetry")
async def ingest_telemetry(request: Request):
    """Allows external sensors to report to the Sovereign Root."""
    data = await request.json()
    entry = {
        "timestamp": datetime.datetime.now(HARARE_TZ).isoformat(),
        "source": data.get("source", "UNKNOWN_SENSOR"),
        "payload": data.get("payload", {}),
        "status": "VERIFIED"
    }
    INDUSTRIAL_LEDGER.append(entry)
    return {"status": "SUCCESS", "node_response": "PULSE_RECEIVED"}

# --- IV. INTERFACE LAYER ---

@app.get("/", response_class=HTMLResponse)
async def root():
    # Show the last 3 industrial ledger entries
    ledger_html = "".join([f"<li style='color:#888;'>[{p['timestamp']}] {p['source']}: {p['payload']}</li>" for p in INDUSTRIAL_LEDGER[-3:]])
    
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px; line-height:1.6;">
        <header style="border-bottom: 2px solid #0f0; margin-bottom:20px;">
            <h1 style="margin:0;">UAIDTIN-ALPHA-07 // GATEWAY</h1>
            <small style="color:#555;">STREAK DAY: 05 | NATIONAL_INFRASTRUCTURE_INGESTION</small>
        </header>
        
        <div style="background:#111; border:1px solid #0f0; padding:15px; margin-bottom:20px;">
            <h3 style="margin:0; color:#fff;">[ INDUSTRIAL_LEDGER_PULSE ]</h3>
            <ul>{ledger_html if INDUSTRIAL_LEDGER else "<li>WAITING_FOR_PHYSICAL_DATA...</li>"}</ul>
        </div>

        <div style="background:#050505; border:1px dotted #0f0; padding:20px;">
            <h3 style="margin-top:0; color:#fff;">[ ISSUE_SOVEREIGN_MANDATE ]</h3>
            <form action="/enforce" method="post">
                <input name="instruction" placeholder="e.g. SYNC HARARE LEDGER" required
                       style="width:100%; background:#000; color:#0f0; border:1px solid #0f0; padding:12px; margin:10px 0; font-family:monospace;">
                <input type="number" name="priority" value="1" style="display:none;">
                <button style="padding:15px 25px; background:#0f0; color:#000; border:none; cursor:pointer; font-weight:bold; width:100%;">VALIDATE & EXECUTE</button>
            </form>
        </div>
    </body>
    """

@app.post("/enforce")
async def enforce(instruction: str = Form(...), priority: int = Form(...)):
    # The Magistrate checks the law before allowing execution
    try:
        validated = Mandate(instruction=instruction, priority=priority)
        return HTMLResponse(f"<body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'><h3>LAW_ADHERED</h3><p>{validated.instruction} committed.</p><a href='/' style='color:#fff;'>BACK</a></body>")
    except Exception as e:
        return HTMLResponse(f"<body style='background:#000; color:#f00; font-family:monospace; padding:30px;'><h3>LAW_BREACHED</h3><p>{str(e)}</p><a href='/' style='color:#fff;'>BACK</a></body>")
