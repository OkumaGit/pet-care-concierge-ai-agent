# Pet Care Concierge — Resilient AI Agent

A smart, contextual personal assistant built for the **Kaggle 5-Day AI Agents: Intensive Vibe Coding Capstone Project with Google**. This agent helps pet owners effortlessly manage health diaries, track behaviors, log veterinary procedures, and monitor daily expenses using a terminal-based conversational interface.

The project is built using the latest official Google `google-genai` SDK and features a hybrid architecture designed to run flawlessly both in the cloud (Kaggle Notebooks) and locally on a personal computer.

---

## Key Course Concepts Implemented

To meet and exceed the official Capstone evaluation criteria, this agent successfully integrates three core pillars of agentic workflows:

### 1. Agent Skills (Tools & Function Calling)
The agent's capabilities are extended beyond native text generation using two persistent Python tools:
* `save_health_log(event_description, cost)`: Dynamically captures user entries, structures them as JSON, and appends a precise server timestamp (%Y-%m-%d %H:%M).
* `read_health_log()`: Safely parses historical data from the local JSON storage, feeding it back into the model's active context window.

### 2. Agent / Multi-agent system (ADK & Contextual Memory)
Utilizing native `client.chats.create` session management, the agent maintains an active short-term memory. It doesn't just read raw files — it can reason over past context. For example, if asked "How much did I spend today?", it fetches historical logs via its reading tool, filters entries matching the current date, and aggregates total costs in real-time.

### 3. Security Features (Strict Guardrails)
An unbreakable behavioral perimeter is defined within the SYSTEM_INSTRUCTION. The agent is strictly barred from practicing veterinary medicine. If it detects life-threatening or critical symptoms (e.g., shaking, bleeding, responsiveness issues), it instantly halts standard conversational and logging routines to trigger a prominent, mandatory medical warning block, refusing to prescribe unsupervised drug dosages.

---

## Technical Setup & Installation

Follow these instructions to clone, configure, and execute the AI Agent locally.

### 1. Prerequisites
* Python 3.10 or higher installed.
* A valid Gemini API Key from Google AI Studio.

### 2. Clone the Repository
```bash
git clone https://github.com/OkumaGit/pet-care-concierge-ai-agent.git
cd pet-care-concierge-ai-agent
```

### 3. Install the Official Google GenAI SDK
```bash
pip install -U google-genai
```

### 4. Configure Your API Key (Hybrid Environment Support)
The codebase includes a resilient try-except boundary. It automatically detects if it is running inside a cloud container or on a physical desktop:

Local PC Deployment: Set your key as an environment variable:

Linux/macOS:
export GEMINI_API_KEY="your_actual_api_key"
Windows (CMD):

DOS
set GEMINI_API_KEY="your_actual_api_key"
Kaggle Notebook Deployment: Simply add your key to Kaggle Secrets under the label GEMINI_API_KEY. The code will automatically retrieve it using UserSecretsClient().


### 5. Launch the Agent
Run the interactive console script:

```bash
python agent.py
```

Production-Grade Resilience (Rate-Limit Handling)
To counter the strict burst-capacity filters on the Free Tier shared infrastructure, the agent implements an active pacing strategy. When run in automated evaluation mode, the script introduces a strategic 65-second cooldown delay between distinct user turns. This allows the Free Tier quota window to completely reset, preventing 429 / RESOURCE_EXHAUSTED deadlocks and ensuring pristine, fully completed generation logs for evaluation judges.

Project Metadata
Submission Track: Concierge Agents

Primary Model: gemini-3.1-flash-lite

License: MIT License
