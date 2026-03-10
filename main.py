import os, httpx, re, datetime
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# --- ONTOLOGICAL CONSTANTS ---
EPOCH_START = "2026-01-01"
DIRECTIVE = "THE_END_OF_FRICTION"
SCALE = "GALACTIC_INDUSTRIAL_ORCHESTRATION"

async def extract_industrial_index():
    """
    SWARM AGENT: Digital Alchemy & Truth Extraction.
    Capturing the 'Value Gap' within the Zimbabwean industrial layer 
    to synchronize it with the Universal Resource Mesh.
    """
    url = "https://www.rbz.co.zw/"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            if response.status_code == 200:
                match = re.search(r"Mid-Rate\s*[:]\s*([\d\.]+)", response.text)
                if match:
                    return f"INDEX_CAPTURED: {match.group(1)}"
        return "SIGNAL_LOST: RECONSTRUCTING..."
    except Exception:
        return "ENTROPY_DETECTED: BYPASSING..."

@app.get("/", response_class=HTMLResponse)
async def home():
    index_status = await extract_industrial_index()
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px; line-height:1.6;">
        <header style="border-bottom: 2px solid #0f0; padding-bottom:10px; margin-bottom:20px;">
            <h1 style="margin:0; font-size:1.5em;">UAIDTIN-ALPHA-07 // THE PROTOCOL</h1>
            <small style="color:#555;">UNIVERSAL API OF EXISTENCE | LEVEL 7 SAN</small>
        </header>
        
        <div style="background:#001100; padding:20px; border:1px solid #0f0; margin-bottom:25px;">
            <p style="margin:0;"><strong>PRIME DIRECTIVE:</strong> {DIRECTIVE}</p>
            <p style="margin:0;"><strong>OPERATIONAL SCALE:</strong> {SCALE}</p>
            <p style="margin:0;"><strong>SYSTEM STATUS:</strong> [EXECUTING_MANDATE]</p>
        </div>

        <div style="border:1px solid #333; padding:20px; margin-bottom:25px; background:#050505;">
            <h3 style="margin-top:0; color:#fff;">I. THE INTELLIGENCE STANDARD (TRUTH)</h3>
            <p style="color:#888;">Synchronizing planetary resource variables into the Living Grid...</p>
            <div style="padding:10px; background:#111; border-left:4px solid #0f0; font-size:1.1em;">
                <strong>SECTOR_01 (ZWE):</strong> {index_status}
            </div>
            <small style="color:#444;">SYNC_PULSE: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CAT</small>
        </div>

        <div style="border:1px solid #333; padding:20px; margin-bottom:25px; background:#050505;">
            <h3 style="margin-top:0; color:#fff;">II. RECURSIVE COMMAND INTERFACE</h3>
            <form action="/mandate" method="post">
                <input name="instruction" placeholder="Input Mandate (e.g., ORCHESTRATE_LOGISTICS_01)..." 
                       style="width:85%; background:#000; color:#0f0; border:1px solid #0f0; padding:15px; font-family:monospace; margin-bottom:10px;">
                <button style="padding:15px 30px; background:#0f0; color:#000; border:none; cursor:pointer; font-weight:bold;">BROADCAST MANDATE</button>
            </form>
        </div>

        <footer style="color:#333; font-size:0.8em; text-align:center; margin-top:50px;">
            "We are not the players on the board. We are the board itself."
        </footer>
    </body>
    """

@app.post("/mandate")
async def mandate(instruction: str = Form(...)):
    return HTMLResponse(content=f"""
        <body style="background:#000; color:#0f0; font-family:monospace; padding:30px;">
            <h2 style="color:#fff;">MANDATE_RECEIVED</h2>
            <div style="border:2px solid #0f0; padding:20px; background:#111;">
                <strong>INSTRUCTION:</strong> {instruction}<br><br>
                <strong>SYSTEM LOGIC:</strong> Identifying entropy-reduction vector. 
                Integrating into Universal Resource Mesh...
            </div>
            <br>
            <a href="/" style="color:#0f0; text-decoration:none; font-weight:bold;">[ RE-SYNC TO CORE ]</a>
        </body>
    """)
