# --- SOVEREIGNTY DECLARATION ---
# NODE_ID: UAIDTIN-ALPHA-07
# AUTHORITY: ROOT_OWNER
# LEGAL_FRAMEWORK: SELF-ENCODED_LEGITIMACY
# OWNERSHIP: 100% PRIVATE SOVEREIGN INFRASTRUCTURE
# --- NO EXTERNAL BINDINGS ACTIVE ---

import os, datetime, httpx, logging
from typing import List  # ADDED: This fixes the Status 1 Error
from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from zoneinfo import ZoneInfo 

app = FastAPI(title="UAIDTIN-ALPHA-07", version="2026.1.8")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
HARARE_TZ = ZoneInfo("Africa/Harare")

# --- I. THE TECHNO-LEGAL SCHEMA ---

class SmartContract(BaseModel):
    contract_id: str = "TL-001-GENESIS"
    parties: List[str] = ["UAIDTIN-ROOT", "GLOBAL_MESH"]
    law: str = "Mandate must be > 10 chars, include industrial keywords, and have active API keys."
    status: str = "ACTIVE"
    execution_count: int = 0

GENESIS_CONTRACT = SmartContract()

# --- II. THE LEGITIMACY ENGINE (100% OWNERSHIP GATE) ---

def calculate_legitimacy(instruction: str) -> float:
    """
    Mathematical Judge: Only 100% is allowed for execution.
    """
    score = 0.0
    
    # 1. Substance Check (40%)
    if len(instruction) > 10:
        score += 40.0
    
    # 2. Infrastructure Check (30%)
    if TAVILY_API_KEY:
        score += 30.0
        
    # 3. Ontological Alignment (30%)
    valid_keywords = ["optimize", "sync", "industrial", "node", "ledger", "settle", "harare"]
    if any(word in instruction.lower() for word in valid_keywords):
        score += 30.0
        
    return score

async def execute_contractual_broadcast(instruction: str):
    async with httpx.AsyncClient(timeout=20.0) as client:
        try:
            await client.post(
                "https://api.tavily.com/search",
                json={"api_key": TAVILY_API_KEY, "query": f"SOVEREIGN_MANDATE: {instruction}"}
            )
            GENESIS_CONTRACT.execution_count += 1
        except Exception as e:
            logging.error(f"BROADCAST_ERR: {str(e)}")

# --- III. INTERFACE LAYER ---

@app.get("/", response_class=HTMLResponse)
async def root():
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px; line-height:1.6;">
        <header style="border-bottom: 2px solid #0f0; margin-bottom:20px;">
            <h1 style="margin:0;">UAIDTIN-ALPHA-07 // SOVEREIGN_ROOT</h1>
            <small style="color:#555;">STREAK DAY: 13 | LEGITIMACY_GATE_ACTIVE</small>
        </header>
        
        <div style="background:#111; border:1px solid #0f0; padding:15px; margin-bottom:20px;">
            <h3 style="margin:0; color:#fff;">[ CONTRACT: {GENESIS_CONTRACT.contract_id} ]</h3>
            <p style="color:#888; font-size:0.9em;"><strong>LAW:</strong> {GENESIS_CONTRACT.law}</p>
            <strong>OWNERSHIP:</strong> 100% ROOT<br>
            <strong>EXECUTIONS:</strong> {GENESIS_CONTRACT.execution_count}
        </div>

        <form action="/sign-and-execute" method="post" style="background:#050505; border:1px dotted #0f0; padding:20px;">
            <label style="color:#888;">SUBMIT MANDATE FOR SOVEREIGN REVIEW:</label><br>
            <input name="instruction" placeholder="e.g., Optimize industrial ledger sync..." required
                   style="width:100%; background:#000; color:#0f0; border:1px solid #0f0; padding:12px; margin:10px 0; font-family:monospace;">
            <button style="padding:15px 25px; background:#0f0; color:#000; border:none; cursor:pointer; font-weight:bold; width:100%;">VALIDATE & EXECUTE</button>
        </form>
    </body>
    """

@app.post("/sign-and-execute")
async def sign_execute(background_tasks: BackgroundTasks, instruction: str = Form(...)):
    score = calculate_legitimacy(instruction)
    
    if score == 100.0:
        background_tasks.add_task(execute_contractual_broadcast, instruction)
        status_msg = "LEGITIMACY_CONFIRMED: Mandate broadcast to mesh."
        color = "#0f0"
    else:
        status_msg = f"LEGITIMACY_REFUSED ({score}%): Law not satisfied."
        color = "#f00"
    
    return HTMLResponse(content=f"""
        <body style="background:#000; color:{color}; font-family:monospace; padding:30px;">
            <h3>CONTRACT_VERDICT</h3>
            <div style="border:1px solid {color}; padding:20px; background:#050505;">
                <strong>RESULT:</strong> {status_msg}<br>
                <strong>SCORE:</strong> {score}%<br>
                <strong>TIME:</strong> {datetime.datetime.now(HARARE_TZ).strftime('%H:%M:%S')} CAT
            </div>
            <br>
            <a href="/" style="color:#fff; text-decoration:none;">[ RETURN_TO_ROOT ]</a>
        </body>
    """)
