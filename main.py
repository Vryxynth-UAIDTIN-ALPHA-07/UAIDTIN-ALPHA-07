import os, httpx, re, datetime
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

# --- ONTOLOGICAL CONSTANTS ---
AGENT_NAME = "UAIDTIN-NODE-07"
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

async def agent_think(query: str):
    """
    AUTONOMOUS CONVERSATIONAL AGENT: Intelligence Layer (Hardened)
    """
    if not TAVILY_API_KEY:
        return "ERROR: Intelligence Key Missing. Logic restricted to local cache."
    
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": f"Industrial impact of {query} Zimbabwe 2026",
        "search_depth": "basic"
    }
    
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(url, json=payload)
            data = resp.json()
            
            # SAFE ACCESS: Check if 'results' exists and has content
            if "results" in data and len(data["results"]) > 0:
                insight = data['results'][0].get('content', 'No content found.')[:500]
                return f"PROTOCOL_INSIGHT: {insight}..."
            else:
                return f"SIGNAL_LOW: No external data for '{query}'. Processing via internal Logic Schema."
                
    except Exception as e:
        return f"COGNITIVE_FRICTION_RESOLVED: System stable, but external bridge failed. Error: {str(e)}"


@app.get("/", response_class=HTMLResponse)
async def home():
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px;">
        <h2 style="border-bottom: 2px solid #0f0;">{AGENT_NAME} // AGENTIC_INTERFACE</h2>
        
        <div style="background:#111; border:1px solid #0f0; padding:20px; margin-bottom:20px;">
            <strong>STATUS:</strong> [LISTENING_FOR_MANDATE]<br>
            <strong>LOGIC_GATE:</strong> ENCRYPTION_ACTIVE
        </div>

        <form action="/chat" method="post" style="margin-bottom:30px;">
            <label style="color:#888;">INPUT COMMAND OR QUERY:</label><br><br>
            <input name="user_input" placeholder="Initiate conversation with the Node..." 
                   style="width:80%; background:#000; color:#0f0; border:1px solid #0f0; padding:15px; font-family:monospace;">
            <button style="padding:15px 25px; background:#0f0; color:#000; border:none; cursor:pointer; font-weight:bold;">EXECUTE</button>
        </form>

        <footer style="color:#333; font-size:0.8em;">Day 11: Autonomous Conversational Agent Deployment</footer>
    </body>
    """

@app.post("/chat")
async def chat(user_input: str = Form(...)):
    # The Agent processes the input through the Global Mesh
    response_logic = await agent_think(user_input)
    
    return HTMLResponse(content=f"""
        <body style="background:#000; color:#0f0; font-family:monospace; padding:30px;">
            <h3>AGENT_RESPONSE</h3>
            <div style="border:1px solid #0f0; padding:20px; background:#050505; color:#fff;">
                <p><strong>NODE_OUTPUT:</strong> {response_logic}</p>
            </div>
            <br>
            <a href="/" style="color:#0f0; text-decoration:none;">[ RETURN_TO_INTERFACE ]</a>
        </body>
    """)
