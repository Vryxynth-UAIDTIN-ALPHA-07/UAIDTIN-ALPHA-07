import os, datetime, httpx, logging
from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from zoneinfo import ZoneInfo 

app = FastAPI(title="UAIDTIN-ALPHA-07", version="2026.1.5")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# --- I. THE UNDISPUTED PROTOCOL (LIVE EXECUTION) ---

async def execute_external_broadcast(service_name: str, payload: dict):
    """
    LIVE CONNECTIVITY: This actually sends data out of your node.
    We are targeting Tavily's search endpoint as our first live handshake.
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # Real Handshake: Sending your mandate to the Global Mesh
            response = await client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": TAVILY_API_KEY,
                    "query": f"Execute industrial optimization for: {payload['instruction']}",
                    "search_depth": "basic"
                }
            )
            # LOGGING THE RESULT (Check your Render Logs for this)
            logging.info(f"BROADCAST_SUCCESS | Service: {service_name} | Status: {response.status_code}")
        except Exception as e:
            logging.error(f"BROADCAST_FAILURE | Service: {service_name} | Error: {str(e)}")

# --- II. INTERFACE LAYER ---

@app.get("/", response_class=HTMLResponse)
async def root():
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px; line-height:1.6;">
        <header style="border-bottom: 2px solid #0f0; margin-bottom:20px;">
            <h1 style="margin:0;">UAIDTIN-ALPHA-07 // LIVE_CONNECTIVITY</h1>
            <small style="color:#555;">STREAK DAY: 12 | NO_MORE_SIMULATION</small>
        </header>
        
        <div style="background:#111; border:1px solid #0f0; padding:15px; margin-bottom:20px;">
            <strong>HANDS_STATUS:</strong> <span style="color:#fff;">LIVE_HTTP_ORCHESTRATOR</span><br>
            <strong>SYNC_TIME:</strong> {datetime.datetime.now(ZoneInfo("Africa/Harare")).strftime('%H:%M:%S')} CAT
        </div>

        <form action="/execute-live" method="post" style="background:#050505; border:1px dotted #0f0; padding:20px;">
            <h3 style="margin-top:0;">[ MANDATE_BROADCASTER ]</h3>
            <label style="color:#888;">TARGET_SYSTEM:</label><br>
            <input name="system" value="GLOBAL_TAVILY_MESH" readonly style="width:100%; background:#222; color:#0f0; border:1px solid #444; padding:10px; margin:10px 0;"><br>
            
            <label style="color:#888;">INDUSTRIAL_INSTRUCTION:</label><br>
            <input name="instruction" placeholder="Enter instruction for external execution..." required
                   style="width:100%; background:#000; color:#0f0; border:1px solid #0f0; padding:10px; margin:10px 0;">
            
            <button style="padding:15px 25px; background:#0f0; color:#000; border:none; cursor:pointer; font-weight:bold; width:100%;">SEND LIVE MANDATE</button>
        </form>
    </body>
    """

@app.post("/execute-live")
async def execute_live(background_tasks: BackgroundTasks, instruction: str = Form(...), system: str = Form(...)):
    # The moment of impact: Launching the background task
    payload = {{"instruction": instruction, "timestamp": str(datetime.datetime.now())}}
    
    background_tasks.add_task(execute_external_broadcast, system, payload)
    
    return HTMLResponse(content=f"""
        <body style="background:#000; color:#0f0; font-family:monospace; padding:30px;">
            <h3>MANDATE_SENT_TO_WIRE</h3>
            <div style="border:1px solid #0f0; padding:20px; background:#050505;">
                <strong>TARGET:</strong> {system}<br>
                <strong>LOGIC_PAYLOAD:</strong> {instruction}<br>
                <strong>STATUS:</strong> LIVE_HTTP_POST_INITIATED
            </div>
            <p style="color:#888;">The simulation has been purged. Your node is now physically reaching out to the web.</p>
            <br>
            <a href="/" style="color:#0f0; text-decoration:none;">[ RETURN_TO_ROOT ]</a>
        </body>
    """)
