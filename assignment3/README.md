# Assignment 3: LLM-Based Agent (Gemini API)

## Objective

Enhance the agent by integrating a Language Model (LLM) for intelligent decision-making while maintaining a fallback rule-based system and interaction logging.

---

## Features

### LLM Integration (Gemini API)

* Uses **Google Gemini API (`gemini-2.5-flash`)** for decision-making
* Sends user queries via HTTP request (`requests` library)
* Determines which tool to use and extracts parameters
* Uses structured output format: `tool|parameters`
* Falls back to rule-based logic if API fails

---

### Hybrid Decision System

* **Primary**: LLM-based tool selection
* **Fallback**: Rule-based parsing using regex and keyword matching
* Ensures reliability even without API access

---

### Logging System

* Stores every interaction in `agent_logs.json`
* Each log contains:

  * Timestamp
  * User input
  * Selected tool
  * Parameters
  * Output

---

### Tool Support

All tools from Assignment 2 are integrated:

* calculate
* weather
* summarize
* random
* convert
* password

---

## How to Run

```bash
python llm_agent.py
```

> Note: API key is already embedded in the code (for lab purposes)

---

## Example Interactions

```text
You: random number
==================================================
[INPUT] random number
Thinking...
[GEMINI RESPONSE] random|1,100
[DECISION] Using tool: random
[PARAMS] 1,100
[OUTPUT] Random number between 1 and 100: 42

Agent: Random number between 1 and 100: 42
```

```text
You: calculate 100 divided by 4
==================================================
[INPUT] calculate 100 divided by 4
Thinking...
[GEMINI RESPONSE] calculate|100/4
[DECISION] Using tool: calculate
[PARAMS] 100/4
[OUTPUT] Result: 25

Agent: Result: 25
```

---

## How LLM Decision Works

The agent sends a structured prompt to Gemini:

* Lists all available tools
* Instructs model to respond in format:

  ```
  tool_name|parameters
  ```

Example:

* Input: `what is 2+3` → `calculate|2+3`
* Input: `weather in Mumbai` → `weather|Mumbai`

---

## Code Structure

* `LLMAgent` class – Core agent implementation 
* `llm_decision()` – Calls Gemini API and parses response
* `rule_based_decision()` – Backup logic using regex
* `execute_tool()` – Executes selected tool
* `clean_expression()` – Sanitizes math expressions
* `process()` – Main pipeline (Input → Decision → Execution → Logging)
* `show_logs()` – Displays interaction history

---

## Logging Format

```json
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

## Requirements

* Python 3.9 or above
* Install dependency:

  ```bash
  pip install requests
  ```

---

## View Logs

```bash
type agent_logs.json
```

Or type `exit` in the program to display logs before quitting.

---

## Testing

Try the following:

* `what is 100 divided by 4?`
* `random number`
* `weather in Mumbai`
* `convert 10 km to miles`
* `password length 16`

---

## Key Learning Outcomes

* LLM-based tool selection
* Prompt engineering for structured output
* API integration using HTTP requests
* Hybrid AI + rule-based systems
* Logging and debugging AI decisions
