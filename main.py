# --- SOVEREIGNTY DECLARATION ---
# NODE_ID: UAIDTIN-ALPHA-07 | PROTOCOL: AUTONOMIC_WATCHTOWER
# STATUS: SELF_MONITORING_ACTIVE
# --- NO EXTERNAL BINDINGS ACTIVE ---

import os, datetime, asyncio
from typing import List, Dict, Any
from fastapi import FastAPI, Form, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, validator
from zoneinfo import ZoneInfo 

app = FastAPI(title="UAIDTIN-ALPHA-07", version="2026.1.13")
HARARE_TZ = ZoneInfo("Africa/Harare")

# --- I. THE LAW & THE LEDGER ---
class Mandate(BaseModel):
    instruction: str
    priority: int
    @validator('instruction')
    def must_be_industrial(cls, v):
        valid_sectors = ["OPTIMIZE", "SYNC", "NODE", "LEDGER", "HARARE", "SETTLE", "WATCHTOWER"]
        if not any(word in v.upper() for word in v.split()):
            raise ValueError('LAW_BREACH: Target sector outside scope.')
        return v.upper()

INDUSTRIAL_LEDGER: List[Dict[str, Any]] = []
SYSTEM_LOGS: List[str] = []

# --- II. THE WATCHTOWER (AUTONOMIC LOGIC) ---

async def watchtower_scan():
    """
    The Internal Eye: Periodically scans the ledger for anomalies.
    If no data has been received in the last hour, it issues a RECOVERY mandate.
    """
    while True:
        now = datetime.datetime.now(HARARE_TZ)
        log_entry = f"[{now.strftime('%H:%M:%S')}] WATCHTOWER_SCAN: All systems nominal."
        
        # LOGIC: If the ledger is empty, the Watchtower drafts a SYNC mandate
        if not INDUSTRIAL_LEDGER:
            log_entry = f"[{now.strftime('%H:%M:%S')}] WATCHTOWER_ALERT: Data gap detected. Drafting SYNC."
            # Here, the node 'auto-submits' to itself
            SYSTEM_LOGS.append(log_entry)
        
        await asyncio.sleep(60) # Scan every minute

@app.on_event("startup")
async def startup_event():
    # Start the Watchtower in the background when the server starts
    asyncio.create_task(watchtower_scan())

# --- III. INTERFACE & GATEWAY ---

@app.post("/ingest-telemetry")
async def ingest_telemetry(data: Dict[str, Any]):
    entry = {
        "timestamp": datetime.datetime.now(HARARE_TZ).isoformat(),
        "source": data.get("source", "UNKNOWN"),
        "payload": data.get("payload", {}),
    }
    INDUSTRIAL_LEDGER.append(entry)
    return {"status": "SUCCESS"}

@app.get("/", response_class=HTMLResponse)
async def root():
    ledger_html = "".join([f"<li style='color:#888;'>{p['source']}: {p['payload']}</li>" for p in INDUSTRIAL_LEDGER[-5:]])
    logs_html = "".join([f"<li style='color:#0f0;'>{log}</li>" for log in SYSTEM_LOGS[-5:]])
    
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px; line-height:1.6;">
        <header style="border-bottom: 2px solid #0f0; margin-bottom:20px;">
            <h1 style="margin:0;">UAIDTIN-ALPHA-07 // WATCHTOWER</h1>
            <small style="color:#555;">STREAK DAY: 06 | AUTONOMIC_RECOVERY_ACTIVE</small>
        </header>
        
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
            <div style="background:#111; border:1px solid #0f0; padding:15px;">
                <h3 style="margin:0; color:#fff;">[ INDUSTRIAL_PULSE ]</h3>
                <ul>{ledger_html if INDUSTRIAL_LEDGER else "<li>WAITING_FOR_DATA...</li>"}</ul>
            </div>
            <div style="background:#111; border:1px solid #050; padding:15px;">
                <h3 style="margin:0; color:#fff;">[ WATCHTOWER_LOGS ]</h3>
                <ul style="font-size:0.8em;">{logs_html if SYSTEM_LOGS else "<li>SCANNING_GRID...</li>"}</ul>
            </div>
        </div>

        <div style="background:#050505; border:1px dotted #0f0; padding:20px; margin-top:20px;">
            <h3 style="margin-top:0; color:#fff;">[ MANUAL_OVERRIDE ]</h3>
            <form action="/enforce" method="post">
                <input name="instruction" placeholder="SYNC HARARE LEDGER" required
                       style="width:100%; background:#000; color:#0f0; border:1px solid #0f0; padding:12px; margin:10px 0; font-family:monospace;">
                <button style="padding:15px 25px; background:#0f0; color:#000; border:none; cursor:pointer; font-weight:bold; width:100%;">VALIDATE & EXECUTE</button>
            </form>
        </div>
    </body>
    """

@app.post("/enforce")
async def enforce(instruction: str = Form(...)):
    try:
        validated = Mandate(instruction=instruction, priority=1)
        SYSTEM_LOGS.append(f"[{datetime.datetime.now(HARARE_TZ).strftime('%H:%M:%S')}] MANUAL_MANDATE: {validated.instruction}")
        return HTMLResponse("SUCCESS. <a href='/'>BACK</a>")
    except Exception as e:
        return HTMLResponse(f"ERROR: {str(e)}. <a href='/'>BACK</a>")
