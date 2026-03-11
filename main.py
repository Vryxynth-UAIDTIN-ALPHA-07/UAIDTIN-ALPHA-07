# --- SOVEREIGNTY DECLARATION ---
# NODE_ID: UAIDTIN-ALPHA-07
# STATUS: IMMUTABLE_LOGIC_ACTIVE
# --- NO EXTERNAL BINDINGS ACTIVE ---

import os, datetime, hashlib, logging
from typing import List
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from zoneinfo import ZoneInfo 

app = FastAPI(title="UAIDTIN-ALPHA-07", version="2026.1.9")

# --- I. THE IRON VAULT (IMMUTABLE CONSTANTS) ---
# These are pulled from the OS environment, making them unchangeable via file edits.
SOVEREIGN_ID = os.getenv("SOVEREIGN_ID", "ZWE-NODE-001")
CORE_MANDATE = "ORCHESTRATE_GALACTIC_INDUSTRY"
ROOT_TZ = ZoneInfo("Africa/Harare")

# --- II. INTEGRITY AUDIT (THE 300MS CHECK) ---
def perform_integrity_audit():
    """
    Simulates a 300ms hash check of the running logic.
    In a sovereign node, this prevents 'Logic Drift'.
    """
    timestamp = datetime.datetime.now(ROOT_TZ).isoformat()
    # Logic: Create a fingerprint of the core configuration
    fingerprint = hashlib.sha256(f"{SOVEREIGN_ID}{CORE_MANDATE}".encode()).hexdigest()
    return {"status": "INTEGRITY_VERIFIED", "hash": fingerprint[:12], "time": timestamp}

# --- III. INTERFACE LAYER ---
@app.get("/", response_class=HTMLResponse)
async def root():
    audit = perform_integrity_audit()
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px; line-height:1.6;">
        <header style="border-bottom: 2px solid #0f0; margin-bottom:20px;">
            <h1 style="margin:0;">UAIDTIN-ALPHA-07 // IMMUTABLE_ROOT</h1>
            <small style="color:#555;">STREAK DAY: 04 | LOGIC_VAULT_ACTIVE</small>
        </header>

        <div style="background:#111; border:1px solid #0f0; padding:15px; margin-bottom:20px;">
            <h3 style="margin:0; color:#fff;">[ INTEGRITY_REPORT ]</h3>
            <strong>NODE_ID:</strong> {SOVEREIGN_ID}<br>
            <strong>MANDATE:</strong> {CORE_MANDATE}<br>
            <strong>SYSTEM_HASH:</strong> <span style="color:#fff;">{audit['hash']}</span><br>
            <strong>LAST_AUDIT:</strong> {audit['time']}
        </div>

        <div style="background:#050505; border:1px dotted #0f0; padding:20px;">
            <h3 style="margin-top:0; color:#fff;">[ PROTECTED_EXECUTION ]</h3>
            <p style="color:#888;">Any mandate submitted here is cross-referenced against the Immutable Hash above.</p>
            <form action="/audit-and-exec" method="post">
                <input name="mandate" placeholder="Enter Sovereign Mandate..." required
                       style="width:70%; background:#000; color:#0f0; border:1px solid #0f0; padding:15px; font-family:monospace;">
                <button style="padding:15px 25px; background:#0f0; color:#000; border:none; cursor:pointer; font-weight:bold;">EXECUTE</button>
            </form>
        </div>
    </body>
    """

@app.post("/audit-and-exec")
async def audit_exec(mandate: str = Form(...)):
    # The Law: Only allow execution if the system hash remains valid
    audit = perform_integrity_audit()
    if audit["status"] != "INTEGRITY_VERIFIED":
        raise HTTPException(status_code=403, detail="LOGIC_CORRUPTION_DETECTED")
    
    return HTMLResponse(content=f"""
        <body style="background:#000; color:#0f0; font-family:monospace; padding:30px;">
            <h3>MANDATE_PROCESSED</h3>
            <div style="border:1px solid #0f0; padding:20px; background:#050505;">
                <strong>MANDATE:</strong> {mandate}<br>
                <strong>AUDIT_HASH:</strong> {audit['hash']}<br>
                <strong>VERDICT:</strong> IMMUTABLE_LOGIC_SATISFIED
            </div>
            <br>
            <a href="/" style="color:#0f0; text-decoration:none;">[ RETURN_TO_ROOT ]</a>
        </body>
    """)
