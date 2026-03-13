import os
from fastapi import FastAPI
from google import genai
from google.genai import types

app = FastAPI()

# Initialize the Gemini 3 Flash Executive Agent
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.post("/execute")
async def self_healing_loop(goal: str):
    """
    Colab-style loop: The AI writes, tests, and verifies code 
    in its own sandbox before returning it to you.
    """
    config = types.GenerateContentConfig(
        tools=[types.Tool(code_execution=types.CodeExecution())],
        system_instruction="You are the UAIDTIN System Node. Use Python to solve the user's goal. TEST your code internally before responding."
    )
    
    response = client.models.generate_content(
        model='gemini-2.0-flash', # Optimized for sub-second orchestration
        contents=goal,
        config=config
    )
    return {"status": "SUCCESS", "analysis": response.text}

@app.get("/health")
async def health():
    return {"status": "active", "node": "UAIDTIN-ALPHA-07"}
