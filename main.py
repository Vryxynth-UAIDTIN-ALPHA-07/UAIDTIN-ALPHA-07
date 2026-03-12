# --- SOVEREIGNTY DECLARATION ---
# NODE_ID: UAIDTIN-ALPHA-07 | PROTOCOL: UNIVERSAL_LOGIC_SCHEMA
# STATUS: STRUCTURED_THOUGHT_ENABLED
# --- NO EXTERNAL BINDINGS ACTIVE ---

import os, httpx
from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from schema import UniversalThought # <--- IMPORT THE BRAIN MAP
from zoneinfo import ZoneInfo 

app = FastAPI(title="UAIDTIN-ALPHA-07")
DISCORD_URL = os.getenv("DISCORD_WEBHOOK_URL")

async def send_discord_thought(thought: UniversalThought):
    """Broadcasts a structured thought to Discord."""
    if DISCORD_URL:
        payload = {
            "username": "UAIDTIN-LOGIC-ENGINE",
            "embeds": [{
                "title": f"MANDATE_AUTHORIZED: {thought.action_type}",
                "description": thought.summarize(),
                "color": 0x00ff00,
                "fields": [
                    {"name": "Payload", "value": str(thought.payload), "inline": True},
                    {"name": "Metadata", "value": str(thought.metadata), "inline": True}
                ]
            }]
        }
        async with httpx.AsyncClient() as client:
            await client.post(DISCORD_URL, json=payload)

@app.get("/", response_class=HTMLResponse)
async def root():
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px;">
        <h1 style="border-bottom: 2px solid #0f0;">UAIDTIN-ALPHA-07 // LOGIC_SCHEMA</h1>
        <form action="/process-logic" method="post" style="background:#111; padding:20px; border:1px solid #0f0;">
            <h3>[ BROADCAST_STRUCTURED_INTENT ]</h3>
            <label>Action Type:</label><br>
            <select name="action" style="width:100%; padding:10px; background:#000; color:#0f0; border:1px solid #0f0; margin-bottom:10px;">
                <option value="SETTLEMENT">SETTLEMENT</option>
                <option value="MARKET_SCOUT">MARKET_SCOUT</option>
                <option value="SYSTEM_SYNC">SYSTEM_SYNC</option>
            </select><br>
            <label>Asset Name:</label><br>
            <input type="text" name="asset" placeholder="e.g. LITHIUM" required style="width:100%; padding:10px; background:#000; color:#0f0; border:1px solid #0f0; margin-bottom:10px;"><br>
            <button style="width:100%; padding:15px; background:#0f0; font-weight:bold; color:#000;">ENFORCE_LOGIC</button>
        </form>
    </body>
    """

@app.post("/process-logic")
async def process_logic(background_tasks: BackgroundTasks, action: str = Form(...), asset: str = Form(...)):
    # Create the structured 'Thought'
    thought = UniversalThought(
        action_type=action,
        payload={"asset": asset, "status": "VERIFIED"}
    )
    
    # Send it to Discord as a structured log
    background_tasks.add_task(send_discord_thought, thought)
    
    return HTMLResponse(f"<body style='background:#000; color:#0f0; padding:30px;'><h3>LOGIC_EMBEDDED</h3><p>{thought.summarize()}</p><a href='/'>BACK</a></body>")
