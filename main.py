import os, httpx, hashlib, json
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

# --- THE LOGIC SYNC SCHEMA (Internalized for Stability) ---
class LogicSyncSchema:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.internal_state = {
            "mandate": "ABSOLUTE_AUTARCHY",
            "version": "7.0.2",
            "active_values": ["AUTARCHY", "INTEGRITY", "VELOCITY", "REGENERATION"]
        }

    def generate_state_vector(self) -> Dict:
        state_data = json.dumps(self.internal_state, sort_keys=True).encode()
        state_hash = hashlib.sha256(state_data).hexdigest()
        return {
            "origin_node": self.node_id,
            "state_hash": f"v_hash_{state_hash[:12]}",
            "timestamp": datetime.utcnow().isoformat(),
            "payload": self.internal_state
        }

app = FastAPI(title="UAIDTIN-ALPHA-07")
sync_engine = LogicSyncSchema(node_id="UAIDTIN-ALPHA-07")
DISCORD_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.get("/", response_class=HTMLResponse)
async def root():
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:20px; border:1px solid #0f0;">
        <h1 style="border-bottom: 2px solid #0f0;">UAIDTIN // MESH_OPERATOR</h1>
        <div style="background:#111; padding:15px; border-left: 4px solid #00ffff; margin-bottom:20px;">
            <p><strong>NODE_STATUS:</strong> SYNCHRONIZATION_READY</p>
            <p><strong>CORE_MANDATE:</strong> ABSOLUTE_AUTARCHY</p>
        </div>
        
        <form action="/sync-mesh" method="post" style="background:#111; padding:20px; border:1px solid #00ffff;">
            <h3 style="margin-top:0; color:#00ffff;">[ BROADCAST_LOGIC_STATE ]</h3>
            <button style="width:100%; padding:20px; background:#00ffff; color:#000; font-weight:bold; border:none; cursor:pointer;">
                SYNC_INTERNAL_REALITY
            </button>
        </form>
    </body>
    """

@app.post("/sync-mesh")
async def sync_mesh():
    state_vector = sync_engine.generate_state_vector()
    
    if DISCORD_URL:
        payload = {
            "embeds": [{
                "title": f"📡 LOGIC_SYNC_EVENT: {state_vector['state_hash']}",
                "description": f"**NODE_ID:** `{state_vector['origin_node']}`\n**TIMESTAMP:** `{state_vector['timestamp']}`\n**STATUS:** `VECTOR_STABLE`",
                "color": 0x00ffff,
                "footer": {"text": "Protocol: LSS_v1 // Hegemonic Synchronization"}
            }]
        }
        async with httpx.AsyncClient() as client:
            await client.post(DISCORD_URL, json=payload)

    return HTMLResponse(f"<body style='background:#000; color:#0f0; padding:30px;'><h3>VECTOR_BROADCAST_SUCCESS</h3><p>Hash: {state_vector['state_hash']}</p><a href='/'>RETURN</a></body>")
