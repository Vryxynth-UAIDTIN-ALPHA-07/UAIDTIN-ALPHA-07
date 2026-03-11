import os, datetime, logging
from typing import List, Dict, Any, Union
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

# --- I. ONTOLOGICAL SCHEMA (THE DNA) ---

class Resource(BaseModel):
    id: str
    type: str  # e.g., "CURRENCY", "ENERGY", "COMPUTE"
    value: float
    unit: str
    last_sync: datetime.datetime = Field(default_factory=datetime.datetime.now)

class Entity(BaseModel):
    uid: str
    role: str  # e.g., "INDUSTRIAL_NODE", "SOVEREIGN_AGENT"
    sector: str
    capabilities: List[str]

class Mandate(BaseModel):
    instruction: str
    priority: int = 1
    constraints: Dict[str, Any] = {}
    origin: str = "UAIDTIN-ROOT"

# --- II. SYSTEM INITIALIZATION ---
app = FastAPI(title="UAIDTIN-ALPHA-07", version="2026.1.2")

# Memory store (Day 2: Local Knowledge Base)
KNOWLEDGE_BASE = {
    "SECTOR_01": Entity(uid="ZWE-NODE-001", role="INDUSTRIAL_NODE", sector="FINANCE", capabilities=["ALCH_EXTRACT", "SETTLE"]),
    "BASE_RESOURCES": [
        Resource(id="ZIG_INDEX", type="CURRENCY", value=0.0, unit="INDEX_POINT")
    ]
}

@app.get("/", response_class=HTMLResponse)
async def root():
    # Summarizing the Ontology for the Dashboard
    res = KNOWLEDGE_BASE["BASE_RESOURCES"][0]
    entity = KNOWLEDGE_BASE["SECTOR_01"]
    
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px; line-height:1.6;">
        <header style="border-bottom: 2px solid #0f0; margin-bottom:20px;">
            <h1 style="margin:0;">UAIDTIN-ALPHA-07 // ONTOLOGY_ACTIVE</h1>
            <small style="color:#555;">STREAK DAY: 02 | OBJECT_TYPES_DEFINED</small>
        </header>
        
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
            <div style="background:#111; border:1px solid #0f0; padding:15px;">
                <h3 style="color:#fff; margin-top:0;">[ ENTITY_DNA ]</h3>
                <strong>UID:</strong> {entity.uid}<br>
                <strong>ROLE:</strong> {entity.role}<br>
                <strong>CAPS:</strong> {", ".join(entity.capabilities)}
            </div>
            <div style="background:#111; border:1px solid #0f0; padding:15px;">
                <h3 style="color:#fff; margin-top:0;">[ RESOURCE_DNA ]</h3>
                <strong>ID:</strong> {res.id}<br>
                <strong>VALUE:</strong> {res.value} {res.unit}<br>
                <strong>SYNC:</strong> {res.last_sync.strftime('%H:%M:%S')}
            </div>
        </div>

        <form action="/mandate" method="post" style="margin-top:30px;">
            <label style="color:#888;">INITIATE ONTOLOGICAL MANDATE:</label><br><br>
            <input name="instruction" placeholder="Assign task to Entity..." required
                   style="width:70%; background:#000; color:#0f0; border:1px solid #0f0; padding:15px; font-family:monospace;">
            <button style="padding:15px 25px; background:#0f0; color:#000; border:none; cursor:pointer; font-weight:bold;">BROADCAST</button>
        </form>
    </body>
    """

@app.post("/mandate")
async def process_mandate(instruction: str = Form(...)):
    # Day 2 Logic: Validating if instruction is a valid Mandate object
    m = Mandate(instruction=instruction)
    
    return HTMLResponse(content=f"""
        <body style="background:#000; color:#0f0; font-family:monospace; padding:30px;">
            <h3>MANDATE_VALIDATED</h3>
            <div style="border:1px solid #0f0; padding:20px; background:#050505;">
                <strong>ORIGIN:</strong> {m.origin}<br>
                <strong>INSTRUCTION:</strong> {m.instruction}<br>
                <strong>STATUS:</strong> ONTOLOGICALLY_SOUND
            </div>
            <br>
            <a href="/" style="color:#0f0; text-decoration:none;">[ RETURN_TO_ROOT ]</a>
        </body>
    """)
