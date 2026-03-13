import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {
        "status": "online",
        "node": "UAIDTIN-ALPHA-07",
        "msg": "Sovereign Baseline Established"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
