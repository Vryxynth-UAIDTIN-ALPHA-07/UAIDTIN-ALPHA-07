# --- SOVEREIGNTY DECLARATION ---
# NODE_ID: UAIDTIN-ALPHA-07 | PROTOCOL: PERSISTENT_LEDGER
# STATUS: DATABASE_SYNCHRONIZATION_ACTIVE
# --- NO EXTERNAL BINDINGS ACTIVE ---

import os, datetime
from typing import List
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, validator
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from zoneinfo import ZoneInfo 

# --- I. DATABASE ARCHITECTURE ---
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    # SQLAlchemy requires 'postgresql://' instead of 'postgres://'
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class LedgerEntry(Base):
    __tablename__ = "industrial_ledger"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(ZoneInfo("Africa/Harare")))
    source = Column(String)
    sector = Column(String)
    payload = Column(JSON)

# Physically manifest the table
Base.metadata.create_all(bind=engine)

app = FastAPI(title="UAIDTIN-ALPHA-07", version="2026.1.16")
HARARE_TZ = ZoneInfo("Africa/Harare")

# --- II. THE MAGISTRATE (REFINED) ---
class Mandate(BaseModel):
    instruction: str
    @validator('instruction')
    def must_be_industrial(cls, v):
        valid_sectors = ["OPTIMIZE", "SYNC", "NODE", "LEDGER", "HARARE", "SETTLE", "WATCHTOWER"]
        if not any(word in v.upper() for word in valid_sectors):
            raise ValueError('LAW_BREACH: Target sector outside scope.')
        return v.upper()

# --- III. INTERFACE & PERSISTENCE ---

@app.get("/", response_class=HTMLResponse)
async def root():
    db = SessionLocal()
    # Fetch last 10 entries from the permanent disk
    entries = db.query(LedgerEntry).order_by(LedgerEntry.timestamp.desc()).limit(10).all()
    db.close()
    
    ledger_html = "".join([
        f"<li style='color:#888;'>[{e.timestamp.strftime('%H:%M:%S')}] {e.source}: {e.sector} -> {e.payload}</li>" 
        for e in entries
    ])
    
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px; line-height:1.6;">
        <header style="border-bottom: 2px solid #0f0; margin-bottom:20px;">
            <h1 style="margin:0;">UAIDTIN-ALPHA-07 // PERSISTENCE</h1>
            <small style="color:#555;">STREAK DAY: 09 | PERMANENT_HISTORY_ENGAGED</small>
        </header>
        
        <div style="background:#111; border:1px solid #0f0; padding:15px; margin-bottom:20px;">
            <h3 style="margin:0; color:#fff;">[ PERMANENT_INDUSTRIAL_LEDGER ]</h3>
            <ul>{ledger_html if entries else "<li>LEDGER_EMPTY: Awaiting first permanent pulse...</li>"}</ul>
        </div>

        <div style="background:#050505; border:1px dotted #0f0; padding:20px;">
            <h3 style="margin-top:0; color:#fff;">[ COMMIT_TO_HISTORY ]</h3>
            <form action="/enforce" method="post">
                <input name="instruction" placeholder="e.g. SYNC HARARE LEDGER" required
                       style="width:100%; background:#000; color:#0f0; border:1px solid #0f0; padding:12px; margin:10px 0; font-family:monospace;">
                <button style="padding:15px 25px; background:#0f0; color:#000; border:none; cursor:pointer; font-weight:bold; width:100%;">VALIDATE & ETCH</button>
            </form>
        </div>
    </body>
    """

@app.post("/enforce")
async def enforce(instruction: str = Form(...)):
    try:
        validated = Mandate(instruction=instruction)
        db = SessionLocal()
        new_entry = LedgerEntry(
            source="MANUAL_OVERRIDE",
            sector=validated.instruction.split()[0],
            payload={"action": validated.instruction}
        )
        db.add(new_entry)
        db.commit()
        db.close()
        return HTMLResponse("LAW_ETCHED_IN_HISTORY. <a href='/'>BACK</a>")
    except Exception as e:
        return HTMLResponse(f"ERROR: {str(e)}. <a href='/'>BACK</a>")
