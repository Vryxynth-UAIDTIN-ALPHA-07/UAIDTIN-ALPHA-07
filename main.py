import os, httpx, re, datetime, logging
from typing import List, Optional, Tuple
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

# --- I. SYSTEM LOGGING & TELEMETRY ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("UAIDTIN-NODE-07")

app = FastAPI(title="UAIDTIN-ALPHA-07", version="2026.1.0")

# --- II. UNIVERSAL LOGIC SCHEMA (MODELS) ---
class AgentResponse(BaseModel):
    insight: str = Field(..., description="The core logic extracted from the mesh")
    actions: List[str] = Field(default_factory=list, description="Available mandates for execution")
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)
    status: str = "VALIDATED"

# --- III. ONTOLOGICAL CONSTANTS ---
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
SECTOR_01_ID = "ZWE_INDUSTRIAL_MESH"

# --- IV. CORE INTELLIGENCE LAYER (HARDENED) ---
async def process_universal_logic(query: str) -> AgentResponse:
    """
    Performs 'Digital Alchemy' with strict error boundaries.
    Ensures the node remains stateless and resilient.
    """
    if not TAVILY_API_KEY:
        logger.error("MISSION_CRITICAL: TAVILY_API_KEY is null.")
        return AgentResponse(insight="INTERNAL_ERROR: Intelligence bridge offline.", actions=["RETRY_SYNC"])

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": f"Industrial impact of {query} Zimbabwe 2026",
        "search_depth": "smart",
        "include_answer": True
    }

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status() # Trigger exception for 4xx/5xx
            
            data = response.json()
            results = data.get("results", [])
            
            if not results:
                return AgentResponse(insight=f"SIGNAL_LOW: No external data for '{query}'.", actions=["EXPAND_SEARCH"])

            # Logic: Extracting the top insight and determining mandates
            raw_insight = results[0].get('content', 'No content.')[:500]
            suggested_actions = ["SYNC_LEDGER"]
            if "money" in query.lower() or "finance" in query.lower():
                suggested_actions.append("ORCHESTRATE_SETTLEMENT")

            return AgentResponse(insight=raw_insight, actions=suggested_actions)

    except httpx.HTTPStatusError as e:
        logger.error(f"GATEWAY_FRICTION: {e.response.status_code}")
        return AgentResponse(insight="GATEWAY_REJECTED: External bridge denied access.", actions=["CHECK_API_KEY"])
    except Exception as e:
        logger.error(f"UNEXPECTED_ENTROPY: {str(e)}")
        return AgentResponse(insight="COGNITIVE_FRICTION: Logic loop interrupted.", actions=["REBOOT_NODE"])

# --- V. INTERFACE & BROADCAST LAYER ---
@app.get("/", response_class=HTMLResponse)
async def root():
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px; line-height:1.6;">
        <header style="border-bottom: 2px solid #0f0; margin-bottom:20px;">
            <h1 style="margin:0;">UAIDTIN-ALPHA-07 // ROOT</h1>
            <small style="color:#555;">UNIVERSAL LOGIC SCHEMA | STREAK DAY: HARDENED</small>
        </header>
        
        <div style="background:#111; border:1px solid #0f0; padding:20px; margin-bottom:20px;">
            <strong>CORE_STATUS:</strong> <span style="color:#fff;">OPERATIONAL</span><br>
            <strong>MESH_GATEWAY:</strong> {"CONNECTED" if TAVILY_API_KEY else "DISCONNECTED"}
        </div>

        <form action="/execute" method="post">
            <input name="query" placeholder="Submit Mandate to the Node..." required
                   style="width:75%; background:#000; color:#0f0; border:1px solid #0f0; padding:15px; font-family:monospace;">
            <button style="padding:15px 25px; background:#0f0; color:#000; border:none; cursor:pointer; font-weight:bold;">EXECUTE</button>
        </form>
    </body>
    """

@app.post("/execute", response_class=HTMLResponse)
async def execute_mandate(query: str = Form(...)):
    agent_data = await process_universal_logic(query)
    
    action_buttons = "".join([
        f'<button style="margin-right:10px; padding:10px; background:#222; color:#0f0; border:1px solid #0f0; cursor:pointer;">[ {a} ]</button>' 
        for a in agent_data.actions
    ])

    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px;">
        <h2 style="color:#fff;">MANDATE_RESULT</h2>
        <div style="border:1px solid #0f0; padding:20px; background:#050505; margin-bottom:20px;">
            <p><strong>TIMESTAMP:</strong> {agent_data.timestamp}</p>
            <p><strong>INSIGHT:</strong> {agent_data.insight}</p>
        </div>
        
        <div style="background:#111; padding:15px; border:1px dotted #0f0;">
            <p style="color:#888; margin-top:0;">AUTONOMOUS_ACTIONS:</p>
            {action_buttons}
        </div>
        <br>
        <a href="/" style="color:#0f0; text-decoration:none;">[ RETURN_TO_ROOT ]</a>
    </body>
    """
