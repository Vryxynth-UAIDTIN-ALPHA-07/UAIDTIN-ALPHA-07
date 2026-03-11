# --- SOVEREIGNTY DECLARATION ---
# NODE_ID: UAIDTIN-ALPHA-07 | PROTOCOL: CODE_AS_LAW
# STATUS: AUTOMATED_ENFORCEMENT_ACTIVE
# --- NO EXTERNAL BINDINGS ACTIVE ---

import os, datetime, logging
from typing import List, Optional
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, validator
from zoneinfo import ZoneInfo 

app = FastAPI(title="UAIDTIN-ALPHA-07", version="2026.1.11")
HARARE_TZ = ZoneInfo("Africa/Harare")

# --- I. THE CONSTITUTION (IMMUTABLE RULES) ---

class Mandate(BaseModel):
    instruction: str
    priority: int
    
    # CODE AS LAW: This physically enforces the 2031-2036 Industrial Scope
    @validator('instruction')
    def must_be_industrial(cls, v):
        valid_sectors = ["OPTIMIZE", "SYNC", "NODE", "LEDGER", "HARARE", "SETTLE", "GALACTIC"]
        if not any(word in v.upper() for word in valid_sectors):
            raise ValueError('LAW_BREACH: Instruction falls outside Sovereign Industrial Scope.')
        return v.upper()

# --- II. ENFORCEMENT ENGINE ---

def execute_legal_audit(instruction: str, priority: int):
    """
    The Magistrate: Validates the mandate against the Constitution.
    """
    try:
        # If this fails, the 'Law' is broken and execution stops immediately.
        validated_mandate = Mandate(instruction=instruction, priority=priority)
        return {"status": "LEGAL", "data": validated_mandate}
    except Exception as e:
        # Extracting the specific validation error message
        error_msg = str(e).split('value_error.')[-1] if 'value_error.' in str(e) else str(e)
        return {"status": "ILLEGAL", "error": error_msg}

# --- III. INTERFACE LAYER ---

@app.get("/", response_class=HTMLResponse)
async def root():
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px; line-height:1.6;">
        <header style="border-bottom: 2px solid #0f0; margin-bottom:20px;">
            <h1 style="margin:0;">UAIDTIN-ALPHA-07 // CODE_AS_LAW</h1>
            <small style="color:#555;">STREAK DAY: 04 | AUTOMATED_ENFORCEMENT_ACTIVE</small>
        </header>
        
        <div style="background:#111; border:1px solid #0f0; padding:15px; margin-bottom:20px;">
            <h3 style="margin:0; color:#fff;">[ THE_CONSTITUTION ]</h3>
            <ul style="color:#888; font-size:0.9em;">
                <li>RULE_01: Every mandate must include a valid Industrial Sector keyword.</li>
                <li>RULE_02: Non-industrial instructions are physically rejected (422).</li>
                <li>RULE_03: Sovereignty is maintained through 100% Validation.</li>
            </ul>
        </div>

        <form action="/enforce" method="post" style="background:#050505; border:1px dotted #0f0; padding:20px;">
            <label style="color:#888;">SUBMIT MANDATE FOR LEGAL VALIDATION:</label><br>
            <input name="instruction" placeholder="e.g., SYNC HARARE LEDGER" required
                   style="width:100%; background:#000; color:#0f0; border:1px solid #0f0; padding:12px; margin:10px 0; font-family:monospace;">
            
            <label style="color:#888;">PRIORITY_LEVEL (1-10):</label><br>
            <input type="number" name="priority" value="1" 
                   style="width:100%; background:#000; color:#0f0; border:1px solid #0f0; padding:12px; margin:10px 0; font-family:monospace;">
            
            <button style="padding:15px 25px; background:#0f0; color:#000; border:none; cursor:pointer; font-weight:bold; width:100%;">VALIDATE & EXECUTE</button>
        </form>
    </body>
    """

@app.post("/enforce")
async def enforce(instruction: str = Form(...), priority: int = Form(...)):
    audit = execute_legal_audit(instruction, priority)
    
    if audit["status"] == "LEGAL":
        color = "#0f0"
        verdict = "LAW_ADHERED: Mandate committed to the Sovereign Ledger."
        details = f"INSTRUCTION: {audit['data'].instruction} | PRIORITY: {audit['data'].priority}"
    else:
        color = "#f00"
        verdict = "LAW_BREACHED: Execution Terminated by Magistrate."
        details = f"REASON: {audit['error']}"
    
    return HTMLResponse(content=f"""
        <body style="background:#000; color:{color}; font-family:monospace; padding:30px;">
            <h3>MAGISTRATE_VERDICT</h3>
            <div style="border:1px solid {color}; padding:20px; background:#050505;">
                <strong>STATUS:</strong> {verdict}<br>
                <strong>DETAILS:</strong> {details}<br>
                <strong>TIMESTAMP:</strong> {datetime.datetime.now(HARARE_TZ).strftime('%H:%M:%S')} CAT
            </div>
            <br>
            <a href="/" style="color:#fff; text-decoration:none;">[ RETURN_TO_ROOT ]</a>
        </body>
    """)
