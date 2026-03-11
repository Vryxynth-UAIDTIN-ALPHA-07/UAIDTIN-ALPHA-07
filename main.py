# --- SOVEREIGNTY DECLARATION ---
# NODE_ID: UAIDTIN-ALPHA-07 | PROTOCOL: LOGIC_SYNC_SCHEMA
# STATUS: PEER_AWARENESS_INITIALIZED
# --- NO EXTERNAL BINDINGS ACTIVE ---

import os, datetime, httpx, asyncio
from typing import List, Dict
from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from zoneinfo import ZoneInfo 

app = FastAPI(title="UAIDTIN-ALPHA-07", version="2026.3.11")
HARARE_TZ = ZoneInfo("Africa/Harare")

# --- I. THE PEER REGISTRY ---
# In the future, you add the URLs of your other nodes here.
KNOWN_PEERS = [] 
SYNC_LOGS: List[str] = []

# --- II. SYNC LOGIC ---

async def broadcast_logic(mandate: str):
    """Broadcasts a validated mandate to all known peers."""
    for peer in KNOWN_PEERS:
        try:
            async with httpx.AsyncClient() as client:
                # This 'handshakes' with other nodes to align the Law
                await client.post(f"{peer}/ingest-logic", json={"mandate": mandate})
        except Exception as e:
            SYNC_LOGS.append(f"SYNC_FAIL: Peer {peer} unreachable.")

# --- III. INTERFACE & GATEWAY ---

@app.get("/", response_class=HTMLResponse)
async def root():
    sync_status = "SOLO_NODE" if not KNOWN_PEERS else f"SYNCING_WITH_{len(KNOWN_PEERS)}_PEERS"
    logs_html = "".join([f"<li style='color:#0f0;'>{log}</li>" for log in SYNC_LOGS[-5:]])
    
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px; line-height:1.6;">
        <header style="border-bottom: 2px solid #0f0; margin-bottom:20px;">
            <h1 style="margin:0;">UAIDTIN-ALPHA-07 // SYNC_GATEWAY</h1>
            <small style="color:#555;">STREAK DAY: 09 | SCHEMA: CROSS_NODE_ALIGNMENT</small>
        </header>
        
        <div style="background:#111; border:1px solid #0f0; padding:15px; margin-bottom:20px;">
            <h3 style="margin:0; color:#fff;">[ NETWORK_STATUS ]</h3>
            <p>MODE: {sync_status}</p>
            <ul>{logs_html if SYNC_LOGS else "<li>AWAITING_NETWORK_PULSE...</li>"}</ul>
        </div>

        <form action="/sync-mandate" method="post" style="background:#050505; border:1px dotted #0f0; padding:20px;">
            <h3 style="margin-top:0; color:#fff;">[ BROADCAST_UNIVERSAL_LAW ]</h3>
            <input name="instruction" placeholder="e.g. SETTLE ALL ACCOUNTS" required
                   style="width:100%; background:#000; color:#0f0; border:1px solid #0f0; padding:12px; margin:10px 0; font-family:monospace;">
            <button style="padding:15px 25px; background:#0f0; color:#000; border:none; cursor:pointer; font-weight:bold; width:100%;">VALIDATE & BROADCAST</button>
        </form>
    </body>
    """

@app.post("/sync-mandate")
async def sync_mandate(background_tasks: BackgroundTasks, instruction: str = Form(...)):
    # 1. Local execution
    timestamp = datetime.datetime.now(HARARE_TZ).strftime('%H:%M:%S')
    log_entry = f"[{timestamp}] LOCAL_EXECUTION: {instruction.upper()}"
    SYNC_LOGS.append(log_entry)
    
    # 2. Network broadcast (runs in the background so the UI doesn't freeze)
    background_tasks.add_task(broadcast_logic, instruction.upper())
    
    return HTMLResponse(f"LOGIC_ALIGNED. <a href='/'>BACK</a>")

@app.post("/ingest-logic")
async def ingest_logic(data: Dict):
    """Endpoint for other nodes to send their logic to this one."""
    mandate = data.get("mandate")
    SYNC_LOGS.append(f"[{datetime.datetime.now(HARARE_TZ).strftime('%H:%M:%S')}] PEER_MANDATE_RECEIVED: {mandate}")
    return {"status": "ALIGNED"}
