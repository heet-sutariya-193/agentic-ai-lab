# Assignment 3: LLM-Based Agent

## Objective

Replace rule-based decision logic with a Language Model (LLM) to improve decision-making and maintain interaction logs.

---

## Features

### LLM Integration

* Uses Groq API with a Llama model for intelligent decision-making
* Falls back to rule-based mode if API is unavailable
* Handles natural language queries effectively

### Logging System

* Records every interaction
* Logs include timestamp, input, selected tool, parameters, and output
* Stored in `agent_logs.json` for later analysis

### Tool Support

All tools from Assignment 2 are supported:

* calculate
* weather
* summarize
* random
* convert
* password

---

## How to Run

```bash id="1m4jsh"
# Without API key (rule-based mode)
python llm_agent.py

# With Groq API key (LLM mode)
set GROQ_API_KEY=your_key_here
python llm_agent.py
```

---

## Example Interactions

```text id="0kkk5d"
You: random number
==================================================
[INPUT] random number
[DECISION] Using tool: random
[PARAMS] 1,100
[OUTPUT] Random number between 1 and 100: 42

Agent: Random number between 1 and 100: 42
Randomness delivered!

You: calculate 100 divided by 4
==================================================
[INPUT] calculate 100 divided by 4
[DECISION] Using tool: calculate
[PARAMS] 100/4
[OUTPUT] Result: 25

Agent: Result: 25
```

---

## Log File Format

`agent_logs.json` stores interactions:

```json id="q9c2mn"
[
  {
    "timestamp": "2026-03-30T14:30:25.123456",
    "input": "random number",
    "selected_tool": "random",
    "parameters": "1,100",
    "output": "Random number between 1 and 100: 42"
  }
]
```

---

## Code Structure

* `__init__()` – Initializes Groq API client with fallback
* `llm_decision()` – Uses LLM to select appropriate tool
* `rule_based_decision()` – Fallback logic
* `execute_tool()` – Executes selected tool
* `process()` – Main pipeline with logging
* `show_logs()` – Displays interaction history

---

## Requirements

* Python 3.9 or above
* Install dependency:

  ```bash
  pip install openai
  ```
* Groq API key (optional, for LLM mode)

---

## View Logs

After running the agent:

```bash id="n3l2qz"
type agent_logs.json
```

Or type `exit` inside the program to display logs before quitting.

---

## Testing

Try the following:

* Natural language: `what is 100 divided by 4?`
* Direct commands: `random number`
* Multi-word queries: `weather in Mumbai`
