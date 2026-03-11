# --- SOVEREIGNTY DECLARATION ---
# NODE_ID: UAIDTIN-ALPHA-07 | ARCHITECTURE: MULTI-AGENT_MESH
# STATUS: AGENTIC_ORCHESTRATION_ACTIVE
# --- NO EXTERNAL BINDINGS ACTIVE ---

import os, datetime, httpx, logging
from typing import List, Optional
from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from zoneinfo import ZoneInfo 

app = FastAPI(title="UAIDTIN-ALPHA-07", version="2026.1.10")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
HARARE_TZ = ZoneInfo("Africa/Harare")

# --- I. AGENT DEFINITIONS (THE MODULES) ---

class LogicAgent:
    """The Brain: Analyzes intent and drafts mandates."""
    def draft_mandate(self, raw_input: str) -> str:
        # Simple Logic: Clean and formalize the instruction
        return f"INDUSTRIAL_OPTIMIZATION: {raw_input.strip().upper()}"

class LegalAgent:
    """The Judge: Enforces the 100% Legitimacy Rule."""
    def verify(self, instruction: str) -> bool:
        score = 0.0
        if len(instruction) > 15: score += 40.0
        if TAVILY_API_KEY: score += 30.0
        valid_keywords = ["OPTIMIZATION", "SYNC", "NODE", "LEDGER", "HARARE"]
        if any(word in instruction for word in valid_keywords): score += 30.0
        return score == 100.0

class ExecutionAgent:
    """The Hands: Performs the physical network handshake."""
    async def broadcast(self, mandate: str):
        async with httpx.AsyncClient(timeout=20.0) as client:
            await client.post(
                "https://api.tavily.com/search",
                json={"api_key": TAVILY_API_KEY, "query": mandate}
            )

# Initializing the Mesh
ANALYST = LogicAgent()
NOTARY = LegalAgent()
EXECUTOR = ExecutionAgent()

# --- II. INTERFACE LAYER ---

@app.get("/", response_class=HTMLResponse)
async def root():
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px; line-height:1.6;">
        <header style="border-bottom: 2px solid #0f0; margin-bottom:20px;">
            <h1 style="margin:0;">UAIDTIN-ALPHA-07 // AGENTIC_MESH</h1>
            <small style="color:#555;">STREAK DAY: 14 | MODULAR_ORCHESTRATION_ACTIVE</small>
        </header>
        
        <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:10px; margin-bottom:20px;">
            <div style="border:1px solid #333; padding:10px; text-align:center;">ANALYST: <span style="color:#fff;">ACTIVE</span></div>
            <div style="border:1px solid #333; padding:10px; text-align:center;">NOTARY: <span style="color:#fff;">ACTIVE</span></div>
            <div style="border:1px solid #333; padding:10px; text-align:center;">EXECUTOR: <span style="color:#fff;">ACTIVE</span></div>
        </div>

        <form action="/orchestrate" method="post" style="background:#050505; border:1px dotted #0f0; padding:20px;">
            <label style="color:#888;">INPUT RAW INDUSTRIAL DATA/INTENT:</label><br>
            <input name="raw_intent" placeholder="e.g., sync harare ledger..." required
                   style="width:100%; background:#000; color:#0f0; border:1px solid #0f0; padding:12px; margin:10px 0; font-family:monospace;">
            <button style="padding:15px 25px; background:#0f0; color:#000; border:none; cursor:pointer; font-weight:bold; width:100%;">START ORCHESTRATION CYCLE</button>
        </form>
    </body>
    """

@app.post("/orchestrate")
async def orchestrate(background_tasks: BackgroundTasks, raw_intent: str = Form(...)):
    # 1. Logic Agent Drafts
    mandate = ANALYST.draft_mandate(raw_intent)
    
    # 2. Legal Agent Verifies
    is_legit = NOTARY.verify(mandate)
    
    if is_legit:
        # 3. Execution Agent Broadcasts
        background_tasks.add_task(EXECUTOR.broadcast, mandate)
        status = "SUCCESS: Mesh coordinated 100% execution."
        color = "#0f0"
    else:
        status = "FAILED: Notary rejected Analyst's draft (Incomplete DNA)."
        color = "#f00"
    
    return HTMLResponse(content=f"""
        <body style="background:#000; color:{color}; font-family:monospace; padding:30px;">
            <h3>AGENTIC_CYCLE_REPORT</h3>
            <div style="border:1px solid {color}; padding:20px; background:#050505;">
                <strong>MANDATE_DRAFT:</strong> {mandate}<br>
                <strong>VERDICT:</strong> {status}<br>
                <strong>TIME:</strong> {datetime.datetime.now(HARARE_TZ).strftime('%H:%M:%S')} CAT
            </div>
            <br>
            <a href="/" style="color:#fff; text-decoration:none;">[ RETURN_TO_ROOT ]</a>
        </body>
    """)
