# --- SOVEREIGNTY DECLARATION ---
# NODE_ID: UAIDTIN-ALPHA-07 | PROTOCOL: HIGH_VELOCITY_ROOT
# STATUS: STABLE_OPERATIONS_RESTORED
# --- NO EXTERNAL BINDINGS ACTIVE ---

import os, datetime
from typing import List, Dict, Any
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, validator
from zoneinfo import ZoneInfo 

app = FastAPI(title="UAIDTIN-ALPHA-07", version="2026.1.17")
HARARE_TZ = ZoneInfo("Africa/Harare")

# --- I. THE LAW ---
class Mandate(BaseModel):
    instruction: str
    @validator('instruction')
    def must_be_industrial(cls, v):
        valid_sectors = ["OPTIMIZE", "SYNC", "NODE", "LEDGER", "HARARE", "SETTLE", "WATCHTOWER"]
        if not any(word in v.upper() for word in v.split()):
            raise ValueError('LAW_BREACH: Target sector outside scope.')
        return v.upper()

# Temporary memory (Resets on restart, but STABLE)
SESSION_LOGS: List[str] = []

# --- II. INTERFACE ---

@app.get("/", response_class=HTMLResponse)
async def root():
    logs_html = "".join([f"<li style='color:#0f0;'>{log}</li>" for log in SESSION_LOGS[-10:]])
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px; line-height:1.6;">
        <header style="border-bottom: 2px solid #0f0; margin-bottom:20px;">
            <h1 style="margin:0;">UAIDTIN-ALPHA-07 // STABLE_ROOT</h1>
            <small style="color:#555;">STREAK DAY: 09 | FRICTION_ELIMINATED</small>
        </header>
        
        <div style="background:#111; border:1px solid #0f0; padding:15px; margin-bottom:20px;">
            <h3 style="margin:0; color:#fff;">[ SESSION_LOGS ]</h3>
            <ul>{logs_html if SESSION_LOGS else "<li>NODE_STABLE: Awaiting manual mandate...</li>"}</ul>
        </div>

        <form action="/enforce" method="post" style="background:#050505; border:1px dotted #0f0; padding:20px;">
            <h3 style="margin-top:0; color:#fff;">[ ISSUE_MANDATE ]</h3>
            <input name="instruction" placeholder="e.g. SYNC HARARE LEDGER" required
                   style="width:100%; background:#000; color:#0f0; border:1px solid #0f0; padding:12px; margin:10px 0; font-family:monospace;">
            <button style="padding:15px 25px; background:#0f0; color:#000; border:none; cursor:pointer; font-weight:bold; width:100%;">VALIDATE & EXECUTE</button>
        </form>
    </body>
    """

@app.post("/enforce")
async def enforce(instruction: str = Form(...)):
    try:
        validated = Mandate(instruction=instruction)
        log_entry = f"[{datetime.datetime.now(HARARE_TZ).strftime('%H:%M:%S')}] EXECUTED: {validated.instruction}"
        SESSION_LOGS.append(log_entry)
        return HTMLResponse(f"<body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'><h3>LAW_ADHERED</h3><p>{log_entry}</p><a href='/' style='color:#fff;'>BACK</a></body>")
    except Exception as e:
        return HTMLResponse(f"<body style='background:#000; color:#f00; font-family:monospace; padding:30px;'><h3>LAW_BREACHED</h3><p>{str(e)}</p><a href='/' style='color:#fff;'>BACK</a></body>")
