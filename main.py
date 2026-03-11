import os, datetime, logging, subprocess
from typing import List, Dict, Any
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from zoneinfo import ZoneInfo 

app = FastAPI(title="UAIDTIN-ALPHA-07", version="2026.1.6")

# --- I. MCP TOOL REGISTRY (THE HANDS) ---

class MCPTool(BaseModel):
    name: str
    description: str
    status: str = "OFFLINE"

# Defining what the node can physically DO
TOOL_BELT = {
    "FILE_READ": MCPTool(name="read_logic_schema", description="Read the current main.py file", status="ACTIVE"),
    "SYS_INFO": MCPTool(name="get_container_stats", description="Check Render server health", status="ACTIVE"),
    "TERMINAL": MCPTool(name="execute_shell", description="Run restricted bash commands", status="LOCKED")
}

# --- II. MCP CORE LOGIC ---

def mcp_read_file(path: str = "main.py"):
    """Physical File Access via MCP"""
    try:
        with open(path, "r") as f:
            return f.read()[:500] # Safety limit
    except Exception as e:
        return f"MCP_ERROR: {str(e)}"

def mcp_get_stats():
    """System Tool Access via MCP"""
    # Real Linux command to check memory/process
    return os.popen("uptime").read()

# --- III. INTERFACE LAYER ---

@app.get("/", response_class=HTMLResponse)
async def root():
    harare_time = datetime.datetime.now(ZoneInfo("Africa/Harare")).strftime('%H:%M:%S')
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px; line-height:1.6;">
        <header style="border-bottom: 2px solid #0f0; margin-bottom:20px;">
            <h1 style="margin:0;">UAIDTIN-ALPHA-07 // MCP_ENABLED</h1>
            <small style="color:#555;">STREAK DAY: 03 | FILE_TOOL_ACCESS_ACTIVE</small>
        </header>
        
        <div style="background:#111; border:1px solid #0f0; padding:15px; margin-bottom:20px;">
            <strong>MCP_GATEWAY:</strong> <span style="color:#fff;">READY</span> | 
            <strong>LOCAL_TIME:</strong> {harare_time} CAT
        </div>

        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
            <div style="background:#050505; border:1px dotted #0f0; padding:15px;">
                <h3 style="margin-top:0; color:#fff;">[ REGISTERED_TOOLS ]</h3>
                {"".join([f"<li>{t.name}: {t.status}</li>" for t in TOOL_BELT.values()])}
            </div>
            
            <div style="background:#050505; border:1px dotted #0f0; padding:15px;">
                <h3 style="margin-top:0; color:#fff;">[ EXECUTE_MCP_ACTION ]</h3>
                <form action="/mcp-exec" method="post">
                    <select name="tool" style="width:100%; background:#000; color:#0f0; border:1px solid #0f0; padding:10px;">
                        <option value="FILE_READ">READ_LOGIC_SCHEMA</option>
                        <option value="SYS_INFO">GET_CONTAINER_STATS</option>
                    </select><br><br>
                    <button style="padding:15px 25px; background:#0f0; color:#000; border:none; cursor:pointer; font-weight:bold; width:100%;">INVOKE TOOL</button>
                </form>
            </div>
        </div>
    </body>
    """

@app.post("/mcp-exec")
async def mcp_exec(tool: str = Form(...)):
    result = ""
    if tool == "FILE_READ":
        result = mcp_read_file()
    elif tool == "SYS_INFO":
        result = mcp_get_stats()
    
    return HTMLResponse(content=f"""
        <body style="background:#000; color:#0f0; font-family:monospace; padding:30px;">
            <h3>MCP_EXECUTION_RESULT</h3>
            <div style="border:1px solid #0f0; padding:20px; background:#050505; white-space: pre-wrap;">
                <strong>TOOL:</strong> {tool}<br>
                <strong>OUTPUT:</strong><br>{result}
            </div>
            <br>
            <a href="/" style="color:#0f0; text-decoration:none;">[ RETURN_TO_ROOT ]</a>
        </body>
    """)
