import os, datetime, httpx, logging
from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from zoneinfo import ZoneInfo 

app = FastAPI(title="UAIDTIN-ALPHA-07", version="2026.1.7")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
HARARE_TZ = ZoneInfo("Africa/Harare")

# --- I. THE TECHNO-LEGAL SCHEMA ---

class SmartContract(BaseModel):
    contract_id: str = "TL-001-GENESIS"
    parties: List[str] = ["UAIDTIN-ROOT", "GLOBAL_MESH"]
    law: str = "The node shall only execute if TAVILY_API_KEY is present and query length > 5."
    status: str = "ACTIVE"
    execution_count: int = 0

# Initializing the first "Code-is-Law" agreement
GENESIS_CONTRACT = SmartContract()

# --- II. CONTRACT ENFORCEMENT ENGINE ---

def validate_legal_logic(query: str) -> bool:
    """
    The 'Judge': This function decides if the 'Law' is being followed.
    """
    # Rule 1: Key must exist
    if not TAVILY_API_KEY: return False
    # Rule 2: Instruction must be substantial
    if len(query) < 5: return False
    return True

async def execute_contractual_broadcast(instruction: str):
    """The Executioner: Only called if the Law allows."""
    async with httpx.AsyncClient(timeout=20.0) as client:
        await client.post(
            "https://api.tavily.com/search",
            json={"api_key": TAVILY_API_KEY, "query": f"LEGAL_MANDATE: {instruction}"}
        )
        GENESIS_CONTRACT.execution_count += 1

# --- III. INTERFACE LAYER ---

@app.get("/", response_class=HTMLResponse)
async def root():
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px; line-height:1.6;">
        <header style="border-bottom: 2px solid #0f0; margin-bottom:20px;">
            <h1 style="margin:0;">UAIDTIN-ALPHA-07 // SMART_CONTRACT_ENGINE</h1>
            <small style="color:#555;">STREAK DAY: 13 | CODE_AS_LAW_INITIALIZED</small>
        </header>
        
        <div style="background:#111; border:1px solid #0f0; padding:15px; margin-bottom:20px;">
            <h3 style="margin:0; color:#fff;">[ ACTIVE_CONTRACT: {GENESIS_CONTRACT.contract_id} ]</h3>
            <p style="color:#888;"><strong>GOVERNING_LAW:</strong> {GENESIS_CONTRACT.law}</p>
            <strong>STATUS:</strong> {GENESIS_CONTRACT.status}<br>
            <strong>EXECUTIONS:</strong> {GENESIS_CONTRACT.execution_count}
        </div>

        <form action="/sign-and-execute" method="post" style="background:#050505; border:1px dotted #0f0; padding:20px;">
            <label style="color:#888;">SUBMIT MANDATE FOR LEGAL REVIEW:</label><br>
            <input name="instruction" placeholder="Enter instruction..." required
                   style="width:100%; background:#000; color:#0f0; border:1px solid #0f0; padding:10px; margin:10px 0;">
            <button style="padding:15px 25px; background:#0f0; color:#000; border:none; cursor:pointer; font-weight:bold; width:100%;">SIGN & EXECUTE</button>
        </form>
    </body>
    """

@app.post("/sign-and-execute")
async def sign_execute(background_tasks: BackgroundTasks, instruction: str = Form(...)):
    # The 'Trial': Checking if the mandate follows the law
    if validate_legal_logic(instruction):
        background_tasks.add_task(execute_contractual_broadcast, instruction)
        status_msg = "LAW_ADHERED: Mandate signed and sent to wire."
        color = "#0f0"
    else:
        status_msg = "LAW_BREACHED: Mandate rejected by Smart Contract TL-001."
        color = "#f00"
    
    return HTMLResponse(content=f"""
        <body style="background:#000; color:{color}; font-family:monospace; padding:30px;">
            <h3>CONTRACT_VERDICT</h3>
            <div style="border:1px solid {color}; padding:20px; background:#050505;">
                <strong>RESULT:</strong> {status_msg}<br>
                <strong>TIMESTAMP:</strong> {datetime.datetime.now(HARARE_TZ).strftime('%H:%M:%S')} CAT
            </div>
            <br>
            <a href="/" style="color:#fff; text-decoration:none;">[ RETURN_TO_ROOT ]</a>
        </body>
    """)
