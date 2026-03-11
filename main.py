# --- SOVEREIGNTY DECLARATION ---
# NODE_ID: UAIDTIN-ALPHA-07 | PROTOCOL: CODE_AS_LAW
# STATUS: GOVERNANCE_ENFORCED
# --- NO EXTERNAL BINDINGS ACTIVE ---

import os, datetime
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from governance import SovereignLaw # <--- IMPORTING THE LAW
from zoneinfo import ZoneInfo 

app = FastAPI(title="UAIDTIN-ALPHA-07")
HARARE_TZ = ZoneInfo("Africa/Harare")
LEDGER = []

@app.get("/", response_class=HTMLResponse)
async def root():
    ledger_items = "".join([f"<li>{item}</li>" for item in LEDGER[-5:]])
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px;">
        <h2>UAIDTIN-ALPHA-07 // GOVERNANCE_ROOT</h2>
        <div style="border:1px solid #0f0; padding:15px; background:#111;">
            <h3>[ IMMUTABLE_LEDGER ]</h3>
            <ul>{ledger_items if LEDGER else "NO_ENTRIES_FOUND"}</ul>
        </div>
        <form action="/execute" method="post" style="margin-top:20px;">
            <input name="mandate" placeholder="MANDATE (e.g. SYNC HARARE)" required 
                   style="width:100%; background:#000; color:#0f0; border:1px solid #0f0; padding:10px;">
            <button style="width:100%; margin-top:10px; padding:10px; background:#0f0; font-weight:bold;">EXECUTE_LAW</button>
        </form>
    </body>
    """

@app.post("/execute")
async def execute(mandate: str = Form(...)):
    # The node checks the hardcoded Governance file before acting
    is_legal, reason = SovereignLaw.validate_mandate(mandate)
    
    if is_legal:
        timestamp = datetime.datetime.now(HARARE_TZ).strftime('%H:%M:%S')
        entry = f"[{timestamp}] SUCCESS: {mandate.upper()}"
        LEDGER.append(entry)
        return HTMLResponse(f"<body style='background:#000; color:#0f0;'><h3>{entry}</h3><a href='/'>BACK</a></body>")
    else:
        return HTMLResponse(f"<body style='background:#000; color:#f00;'><h3>GOVERNANCE_REJECTION: {reason}</h3><a href='/'>BACK</a></body>")
