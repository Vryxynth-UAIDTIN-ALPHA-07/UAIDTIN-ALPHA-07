from google import genai
from google.genai import types
import os

# 1. Initialize the Executive Agent with Code Execution enabled
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.post("/execute")
async def ai_executive_loop(goal: str):
    """
    Executes a Colab-style loop: Write -> Run -> Fix -> Deploy.
    """
    # Enable the 'code_execution' tool so the AI can test its own fixes
    config = types.GenerateContentConfig(
        tools=[types.Tool(code_execution=types.CodeExecution())],
        system_instruction="You are the UAIDTIN Executive Agent. Your goal is to write and TEST Python code to achieve the user's objective. Always run the code to verify it works before providing the final block."
    )

    response = client.models.generate_content(
        model='gemini-2.0-flash', # Or gemini-3-flash
        contents=goal,
        config=config
    )

    # The response will contain the code AND the execution results
    return {
        "final_logic": response.text,
        "execution_steps": [part.executable_code for part in response.candidates[0].content.parts if part.executable_code]
    }
