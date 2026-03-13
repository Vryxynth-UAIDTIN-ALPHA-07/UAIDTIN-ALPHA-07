import os
import time
import google.generativeai as genai
from flask import Flask

# 1. Initialize Render Web Server (Prevents "Port Binding" errors)
app = Flask(__name__)

@app.route('/')
def health_check():
    return "UAIDTIN-ALPHA-07 Status: ONLINE. Brain-Sync Active.", 200

# 2. Configure Gemini "Brain"
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("CRITICAL ERROR: GEMINI_API_KEY missing. Entering brainless state (Status 1).")
    exit(1)

genai.configure(api_key=API_KEY)

# Initialize model with code_execution enabled
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[{"code_execution": {}}]
)

def run_self_diagnostic():
    """
    The 'Self-Healing' mechanism. 
    The AI verifies its own environment to stop Status 1 loops.
    """
    print("--- UAIDTIN-ALPHA-07: Initiating Diagnostic ---")
    
    prompt = """
    You are UAIDTIN-ALPHA-07, an autonomous self-healing node. 
    Task: Verify your current environment. 
    1. Check if the environment variables are accessible.
    2. Confirm your ability to execute code.
    3. If you find any issues that would cause a 'Status 1' crash, 
       output a plan to bypass the error.
    """
    
    try:
        response = model.generate_content(prompt)
        print(f"Brain Response: {response.text}")
    except Exception as e:
        print(f"Diagnostic Failure: {e}")

def start_node():
    # Initial diagnostic on boot
    run_self_diagnostic()
    
    # Run the web server in the background (Render requirement)
    # Using port 10000 (Render default)
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    start_node()
