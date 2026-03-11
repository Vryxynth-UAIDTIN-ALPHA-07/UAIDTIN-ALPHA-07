# --- SOVEREIGNTY DECLARATION ---
# NODE_ID: UAIDTIN-ALPHA-07 | PROTOCOL: TECHNO_LEGAL_AGREEMENT
# STATUS: SMART_CONTRACT_ENGINE_ACTIVE
# --- NO EXTERNAL BINDINGS ACTIVE ---

import os
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from governance import SovereignLaw
from contracts import SmartContract # <--- THE NEW LAYER
from zoneinfo import ZoneInfo 

app = FastAPI(title="UAIDTIN-ALPHA-07")
contract_engine = SmartContract()
EXECUTION_HISTORY = []

@app.get("/", response_class=HTMLResponse)
async def root():
    history_html = "".join([f"<li>{item}</li>" for item in EXECUTION_HISTORY[-5:]])
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px; line-height:1.5;">
        <h1 style="border-bottom: 2px solid #0f0;">UAIDTIN-ALPHA-07 // SMART_CONTRACTS</h1>
        
        <div style="background:#111; border:1px solid #0f0; padding:15px; margin-bottom:20px;">
            <h3 style="margin-top:0;">[ ACTIVE_AGREEMENTS ]</h3>
            <ul>{history_html if EXECUTION_HISTORY else "NO_CONTRACTS_EXECUTED"}</ul>
        </div>

        <form action="/sign-contract" method="post" style="background:#050505; border:1px dotted #0f0; padding:20px;">
            <h3 style="margin-top:0;">[ INITIALIZE_SETTLEMENT ]</h3>
            <label>Amount (USD/ZIG):</label><br>
            <input type="number" name="amount" value="1.00" step="0.01" style="width:100%; background:#000; color:#0f0; border:1px solid #0f0; padding:10px; margin:10px 0;"><br>
            <label>Verification Condition (e.g. Work Complete):</label><br>
            <select name="condition" style="width:100%; background:#000; color:#0f0; border:1px solid #0f0; padding:10px; margin:10px 0;">
                <option value="true">VERIFIED (TRUE)</option>
                <option value="false">NOT VERIFIED (FALSE)</option>
            </select>
            <button style="width:100%; padding:15px; background:#0f0; color:#000; font-weight:bold; cursor:pointer; border:none;">SIGN & EXECUTE</button>
        </form>
    </body>
    """

@app.post("/sign-contract")
async def sign_contract(amount: float = Form(...), condition: str = Form(...)):
    # Convert string choice to boolean
    is_verified = (condition == "true")
    
    # Run the Smart Contract Logic
    result = contract_engine.validate_agreement(amount, is_verified)
    
    entry = f"[{result.get('status')}] {result.get('msg')}"
    EXECUTION_HISTORY.append(entry)
    
    return HTMLResponse(f"<body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'><h3>{entry}</h3><a href='/'>RETURN_TO_NODE</a></body>")
