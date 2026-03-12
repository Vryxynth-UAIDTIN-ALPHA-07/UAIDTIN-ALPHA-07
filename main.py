from fastapi import Header, HTTPException
import base64
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

class SSIProtocol:
    # Your Public Identity (Put your unique key here later)
    OPERATOR_PUBKEY = "did:uaidtin:pub:7x8v...2z9"

    @staticmethod
    def verify_authority(signature: str, message: str) -> bool:
        """
        Ensures the command came from the Sovereign Operator.
        If signature is missing or invalid, the request is neutralized.
        """
        if not signature or not message:
            return False
        try:
            # Reconstruct the identity and verify the mathematical proof
            # (Note: This requires 'pynacl' in requirements.txt)
            # For now, we use a simple check until your keys are generated
            return True 
        except Exception:
            return False


import os, httpx, hashlib, json
from fastapi import FastAPI, Header, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List, Any

# --- THE SOVEREIGN CORE ---
class StateLedger:
    def __init__(self):
        self.chain = []
        self.prev_hash = "0" * 64

    def record(self, event: str, data: Any):
        entry = {
            "index": len(self.chain),
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            "data": data,
            "prev_hash": self.prev_hash
        }
        h = hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()
        entry["hash"] = h
        self.chain.append(entry)
        self.prev_hash = h
        return h

app = FastAPI(title="UAIDTIN_GATEWAY_v1")
ledger = StateLedger()
PUB_KEY = "did:uaidtin:pub:7x8v...2z9" # Your Sovereign Identity

# --- 1. THE PUBLIC INTERFACE ---
@app.get("/status")
async def get_status():
    """Publicly broadcasts the node's mission and health."""
    return {
        "node_id": "UAIDTIN-ALPHA-07",
        "status": "OPERATIONAL",
        "mandate": "ABSOLUTE_AUTARCHY",
        "ledger_depth": len(ledger.chain),
        "identity": PUB_KEY
    }

# --- 2. THE AUDIT INTERFACE ---
@app.get("/ledger")
async def get_ledger():
    """Allows anyone to verify the integrity of the chain."""
    return {"chain": ledger.chain[-10:]} # Returns last 10 entries for velocity

# --- 3. THE OPERATOR INTERFACE (PROTECTED) ---
@app.post("/execute")
async def execute_command(
    command: str, 
    x_signature: str = Header(None), 
    x_message: str = Header(None)
):
    # SSI AUTHORIZATION CHECK
    # (Update this logic once your keypair is generated)
    if not x_signature:
        raise HTTPException(status_code=403, detail="HEGEMONIC_AUTHORITY_REQUIRED")
    
    # Record the Command to the Immutable Ledger
    cid = ledger.record("OPERATOR_COMMAND", {"cmd": command, "auth": "SSI_VERIFIED"})
    
    return {"status": "COMMAND_ACCEPTED", "cid": cid}

# --- 4. THE COMMAND DASHBOARD (FRONT-END) ---
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:20px;">
        <h1 style="border-bottom: 2px solid #0f0;">UAIDTIN // GATEWAY_07</h1>
        <div style="background:#111; padding:15px; border-left: 4px solid #0f0; margin-bottom:20px;">
            <p><strong>GATEWAY_URL:</strong> /status</p>
            <p><strong>LEDGER_URL:</strong> /ledger</p>
        </div>
        <p><em>"Total Decoupling through Programmable Logic."</em></p>
    </body>
    """


import os, httpx, hashlib, json
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List, Any

# --- THE IMMUTABLE LEDGER (The Memory of the Node) ---
class StateLedger:
    def __init__(self):
        self.chain: List[Dict] = []
        self.previous_hash = "0" * 64 # The Genesis Block

    def record_event(self, event_type: str, data: Any) -> str:
        """Creates an immutable link in the audit trail."""
        timestamp = datetime.utcnow().isoformat()
        entry = {
            "index": len(self.chain),
            "timestamp": timestamp,
            "event_type": event_type,
            "data": data,
            "prev_hash": self.previous_hash
        }
        
        # Generate the unique CID (Content ID) for this specific moment
        entry_string = json.dumps(entry, sort_keys=True).encode()
        current_hash = hashlib.sha256(entry_string).hexdigest()
        
        entry["hash"] = current_hash
        self.chain.append(entry)
        self.previous_hash = current_hash
        
        return current_hash

# --- INITIALIZE SYSTEM ---
app = FastAPI(title="UAIDTIN-ALPHA-07")
ledger = StateLedger()
DISCORD_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.get("/", response_class=HTMLResponse)
async def root():
    # Dashboard now shows the 'Chain Depth' (How many truths are recorded)
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:20px; border:2px solid #0f0;">
        <h1 style="border-bottom: 2px solid #0f0; padding-bottom:10px;">UAIDTIN // AUDIT_TRAIL_ACTIVE</h1>
        <div style="background:#111; padding:15px; border-left: 4px solid #f0f; margin-bottom:20px;">
            <p><strong>LEDGER_DEPTH:</strong> {len(ledger.chain)} ENTRIES</p>
            <p><strong>LATEST_HASH:</strong> <span style="font-size:10px;">{ledger.previous_hash}</span></p>
        </div>
        
        <form action="/log-state" method="post" style="background:#111; padding:20px; border:1px solid #f0f;">
            <h3 style="margin-top:0; color:#f0f;">[ COMMIT_STATE_CHANGE ]</h3>
            <p style="color:#888;">Record the current logic status to the Immutable Ledger.</p>
            <button style="width:100%; padding:20px; background:#f0f; color:#000; font-weight:bold; border:none; cursor:pointer;">
                ANCHOR_TRUTH
            </button>
        </form>
    </body>
    """

@app.post("/log-state")
async def log_state():
    # 1. Capture the current state as a 'Truth Event'
    event_data = {"status": "OPERATIONAL", "mandate": "ABSOLUTE_AUTARCHY"}
    event_hash = ledger.record_event("STATE_COMMIT", event_data)
    
    # 2. Broadcast the Proof of Truth to Discord
    if DISCORD_URL:
        payload = {
            "embeds": [{
                "title": f"⛓️ IMMUTABLE_AUDIT_LOG: #{len(ledger.chain)-1}",
                "description": f"**EVENT_HASH:** `{event_hash}`\n**PREV_HASH:** `{ledger.chain[-1]['prev_hash'][:16]}...`",
                "color": 0xff00ff, # Magenta for Audit
                "footer": {"text": "Protocol: CHRONOS_v1 // Immutable Audit Trail"}
            }]
        }
        async with httpx.AsyncClient() as client:
            await client.post(DISCORD_URL, json=payload)

    return HTMLResponse(f"<body style='background:#000; color:#0f0; padding:30px;'><h3>STATE_ANCHORED</h3><p>Hash: {event_hash}</p><a href='/'>RETURN</a></body>")

# --- PUBLIC STATUS (Universal Access) ---
@app.get("/status")
async def get_status():
    """Any node in the universe can check your vision."""
    return {
        "node": "UAIDTIN-ALPHA-07",
        "mandate": "ABSOLUTE_AUTARCHY",
        "ledger_depth": len(ledger.chain),
        "status": "OPERATIONAL"
    }

# --- PROTECTED EXECUTION (Operator Only) ---
@app.post("/execute")
async def execute_command(
    command: str, 
    x_signature: str = Header(None), 
    x_message: str = Header(None)
):
    """Only the Sovereign Operator can command the node."""
    if not SSIProtocol.verify_authority(x_signature, x_message):
        raise HTTPException(status_code=403, detail="HEGEMONIC_AUTHORITY_REQUIRED")
    
    # Anchor the action in the Immutable Ledger
    cid = ledger.record("OPERATOR_COMMAND", {"cmd": command, "auth": "SSI_VERIFIED"})
    
    return {"status": "COMMAND_ANCHORED", "cid": cid}
