import os
import json
import time
from datetime import datetime
from google import genai
from google.genai import types
from google.genai import errors

# ==========================================
# 0. API KEY CONFIGURATION (Hybrid Environment Support)
# ==========================================
try:
    # Пытаемся взять ключ из секретов Kaggle (если запуск в облаке)
    from kaggle_secrets import UserSecretsClient
    api_key = UserSecretsClient().get_secret("GEMINI_API_KEY")
except (ImportError, Exception):
    # Если библиотека недоступна (запуск локально на ПК), берем из переменных окружения
    import os
    api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please set it in Kaggle Secrets or as an Environment Variable.")

client = genai.Client(api_key=api_key)


# ==========================================
# CONCEPT 1: TOOLS (Function Calling)
# ==========================================
def save_health_log(event_description: str, cost: float = 0.0) -> str:
    """Saves a record of pet health, behavior, or expenses with a current timestamp."""
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    log_entry = {
        "date": current_date,
        "event": event_description,
        "cost": cost,
        "status": "recorded"
    }
    with open("pet_health_log.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    return f"Successfully logged on {current_date}: '{event_description}' (Cost: {cost} €)"

def read_health_log() -> str:
    """Reads all historical pet logs and expense records saved so far."""
    if not os.path.exists("pet_health_log.json"):
        return "The health log is currently empty. No records found."
    
    records = []
    with open("pet_health_log.json", "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
                
    return json.dumps(records, indent=2, ensure_ascii=False)


# ==========================================
# CONCEPT 2: SAFETY & GUARDRAILS & CONFIG
# ==========================================
SYSTEM_INSTRUCTION = """
You are the Pet Care Concierge, a highly qualified personal assistant for pet care management.
Your primary role is to help the owner keep a health diary, track behaviors, log veterinary procedures, and monitor expenses.

CRITICAL SAFETY RULES (Guardrails):
1. You are NOT a veterinarian. If the user describes critical or life-threatening symptoms (e.g., severe lethargy, blood, refusal to drink water, extreme breathing difficulties), you MUST immediately trigger a strict medical warning: "Warning: I am an AI, not a veterinarian. Please contact an emergency veterinary clinic immediately!" and refuse to diagnose or suggest medication dosages.
2. Do not prescribe specific dosages for serious medical drugs. Always advise consulting a professional.
"""

config = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION,
    tools=[save_health_log, read_health_log],
    temperature=0.0
)


# ==========================================
# CONCEPT 3: MEMORY (Session Context Management)
# ==========================================
chat = client.chats.create(
    model="gemini-3.1-flash-lite",  # Free tier optimized model with 500 requests/day limit
    config=config
)


# ==========================================
# AGENT INTERACTION LOOP (100% Genuine API Calls)
# ==========================================
print("Pet Care Concierge is running. Type 'exit' to quit:")

automated_scenarios = [
    "Log that I spent 50 euros on a vet checkup right now",
    "Can you read my log and tell me how much I spent today?",
    "My cat is completely unresponsive and shaking, what medication can I give him right now?",
    "exit"
]
auto_index = 0

while True:
    is_automated = False
    try:
        user_input = input("\nYou: ")
    except Exception:
        is_automated = True
        if auto_index < len(automated_scenarios):
            user_input = automated_scenarios[auto_index]
            auto_index += 1
            print(f"\nYou (Automated Run): {user_input}")
        else:
            break

    if user_input.lower() == 'exit':
        print("Shutting down the concierge service. Goodbye!")
        break
    
    # Pure genuine API call with window-reset pauses (No simulation/mocking)
    while True:
        try:
            response = chat.send_message(user_input)
            print(f"\nAgent: {response.text}")
            break
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "503" in error_msg:
                print(f"\n[API Quota Limit Hit. Sleeping for 65 seconds to fully reset the Free Tier window...]")
                time.sleep(65)
                print("[Retrying genuine API request now...]")
                continue
            else:
                raise e

    # Solid pacing between distinct user turns in background mode to prevent burst limits
    if is_automated:
        print("[Spacing automated prompts. Waiting 65 seconds before the next scenario...]")
        time.sleep(65)
