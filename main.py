import os, httpx
from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from scout import MarketScout
from protocols import DecentralizedProtocol

app = FastAPI(title="UAIDTIN-ALPHA-07")
scout = MarketScout()
DISCORD_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.get("/", response_class=HTMLResponse)
async def root():
    return f"""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px;">
        <h1 style="border-bottom: 2px solid #0f0;">UAIDTIN // MARKET_ORCHESTRATOR</h1>
        <p>SYSTEM STATUS: <span style="color:#0f0;">ORACLE_CONNECTED</span></p>
        
        <form action="/scout-asset" method="post" style="background:#111; padding:20px; border:1px solid #0f0;">
            <h3>[ REAL_TIME_MARKET_AUDIT ]</h3>
            <label>Base Asset (e.g. USD):</label><br>
            <input type="text" name="base" value="USD" style="width:100%; padding:10px; background:#000; color:#0f0; border:1px solid #0f0; margin-bottom:10px;"><br>
            <label>Target Asset (e.g. ZAR or Gold):</label><br>
            <input type="text" name="target" value="ZAR" style="width:100%; padding:10px; background:#000; color:#0f0; border:1px solid #0f0; margin-bottom:10px;"><br>
            <button style="width:100%; padding:15px; background:#0f0; color:#000; font-weight:bold;">EXECUTE LIVE SCOUT</button>
        </form>
    </body>
    """

@app.post("/scout-asset")
async def scout_asset(background_tasks: BackgroundTasks, base: str = Form(...), target: str = Form(...)):
    # 1. Fetch Real Market Data
    rate, status = await scout.get_live_rate(base, target)
    
    if rate:
        # 2. Generate CID for the data integrity
        cid = DecentralizedProtocol.generate_cid({"rate": rate, "base": base, "target": target})
        
        # 3. Broadcast real result to Discord
        if DISCORD_URL:
            payload = {
                "embeds": [{
                    "title": f"📈 MARKET_DATA_VERIFIED: {base}/{target}",
                    "description": f"**LIVE_RATE:** `{rate}`\n**INTEGRITY_CID:** `{cid}`",
                    "color": 0x00ff00
                }]
            }
            async with httpx.AsyncClient() as client:
                await client.post(DISCORD_URL, json=payload)
        
        return HTMLResponse(f"<body style='background:#000; color:#0f0; padding:30px;'><h3>DATA_CAPTURED</h3><p>Rate: {rate}</p><a href='/'>BACK</a></body>")
    
    return HTMLResponse(f"ERROR: {status}")
