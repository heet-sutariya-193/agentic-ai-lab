# Assignment 4: Multi-Step Agent (Planning with Gemini API)

## Objective

Build an intelligent agent that decomposes complex queries into multiple steps, generates a structured execution plan using an LLM, and executes each step sequentially with intermediate outputs.

---

## Features

### LLM-Based Planning (Gemini API)

* Uses **Google Gemini API (`gemini-2.5-flash`)** for task decomposition
* Converts user queries into a **JSON execution plan**
* Each step includes:

  * `step` (order)
  * `tool` (which tool to use)
  * `params` (input for the tool)

---

### Structured Plan Generation

* LLM returns structured JSON instead of plain text
* Example:

```json id="ex1"
[
  {"step": 1, "tool": "calculate", "params": "10+20+30"},
  {"step": 2, "tool": "calculate", "params": "(10+20+30)/3"},
  {"step": 3, "tool": "summarize", "params": "The average is"}
]
```

---

### Fallback Planning System

* If LLM fails or JSON parsing fails:

  * Uses **rule-based planning**
  * Handles:

    * Average calculations
    * Weather queries
    * Random numbers
    * Password generation
    * Unit conversion

---

### Sequential Execution Engine

* Executes steps in order
* Supports **result chaining between steps**
* Automatically extracts numeric outputs for reuse

Example:

* Step 1 → Result = 60
* Step 2 uses `(60)/3`

---

### Intermediate Output Display

* Shows detailed execution logs:

  * Planning phase
  * Step-by-step execution
  * Final output

---

## How to Run

```bash id="run1"
python multi_step_agent.py
```

> Note: API key is embedded in the code for lab/demo purposes

---

## Example Interactions

### Example 1: Average + Summary

```text id="ex2"
You: Find the average of 10, 20, 30 and then summarize the result

[PLANNING PHASE]
Plan Created:
  Step 1: calculate - 10+20+30
  Step 2: calculate - (10+20+30)/3
  Step 3: summarize - The average is

[EXECUTION PHASE]
[STEP 1] Result: 60
[STEP 2] Result: 20.0
[STEP 3] Result: Summary: The average is 20.0

FINAL OUTPUT
Step 1 Result: 60
Step 2 Result: 20.0
Step 3 Result: Summary: The average is 20.0

Agent: Completed! Final result: Summary: The average is 20.0
```

---

### Example 2: Multi-Step Mixed Task

```text id="ex3"
You: Get weather in London and then calculate 100/4

[PLANNING PHASE]
Plan Created:
  Step 1: weather - London
  Step 2: calculate - 100/4

[EXECUTION PHASE]
[STEP 1] Result: Weather in London: Cloudy, 12°C / 54°F
[STEP 2] Result: 25

Agent: Completed! Final result: 25
```

---

### Example 3: Random + Chaining

```text id="ex4"
You: Generate a random number and then add 10 to it

[PLANNING PHASE]
Plan Created:
  Step 1: random - 1,100
  Step 2: calculate - X+10

[EXECUTION PHASE]
[STEP 1] Result: 47
[STEP 2] Result: 57
```

---

## Code Structure

* `MultiStepAgent` class – Main planning agent 
* `create_plan()` – Calls Gemini API and parses JSON plan
* `fallback_plan()` – Rule-based backup planning
* `execute_plan()` – Executes steps with chaining logic
* `process()` – Full pipeline (Plan → Execute → Output)

---

## Planning Workflow

```
User Input
   ↓
LLM Planning (Gemini)
   ↓
JSON Plan (steps)
   ↓
Sequential Execution
   ↓
Intermediate Outputs
   ↓
Final Result
```

---

## Requirements

* Python 3.9 or above
* Install dependency:

  ```bash
  pip install requests
  ```

---

## Testing

Try the following:

* `Find the average of 10, 20, 30 and summarize the result`
* `Get weather in London and then calculate 100/4`
* `Generate a random number and then add 10 to it`
* `Generate a password of length 16`
* `Convert 100 km to miles`

---

## Key Learning Outcomes

* LLM-based task decomposition
* Structured planning using JSON
* Sequential execution with result chaining
* Prompt engineering for planning agents
* Robust fallback mechanisms
