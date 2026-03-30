# Assignment 4: Multi-Step Agent (Planning)

## Objective

Build an agent capable of decomposing complex queries into multiple steps, planning execution, and producing intermediate outputs.

---

## Features

### Task Decomposition

* Breaks complex queries into sequential steps
* Uses LLM (Groq API) for intelligent planning
* Falls back to rule-based planning if LLM is unavailable

### Sequential Execution

* Executes steps in order
* Chains outputs between steps
* Displays intermediate results at each stage

### Multi-Step Capabilities

* Average calculation with summarization
* Random number generation workflows
* Combined operations (e.g., weather + calculation)

---

## How to Run

```bash id="d1h8zk"
python multi_step_agent.py
```

---

## Example Interactions

### Example 1: Average with Summary

```text id="l2p9va"
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

### Example 2: Random Number

```text id="v7k2sm"
You: random number

[PLANNING PHASE]
Plan Created:
  Step 1: random - 1,100

[EXECUTION PHASE]
[STEP 1] Result: Random number between 1 and 100: 47

Agent: Completed! Final result: Random number between 1 and 100: 47
```

---

### Example 3: Weather with Calculation

```text id="j9t3qw"
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

## Code Structure

* `__init__()` – Initializes Groq API client
* `create_plan()` – Uses LLM to generate execution plan
* `fallback_plan()` – Rule-based planning logic
* `execute_plan()` – Executes steps sequentially with chaining
* `process()` – Main pipeline (Plan → Execute → Output)

---

## Planning Examples

| Query                   | Plan Steps                |
| ----------------------- | ------------------------- |
| Find average of numbers | Sum → Average             |
| Average and summarize   | Sum → Average → Summarize |
| Random number           | Generate random number    |
| Weather query           | Fetch weather             |
| Weather + calculation   | Weather → Calculate       |

---

## Requirements

* Python 3.9 or above
* Install dependency:

  ```bash
  pip install openai
  ```
* Groq API key (optional, for LLM planning)

---

## Testing

Try the following inputs:

* `Find the average of 10, 20, 30 and summarize the result`
* `random number`
* `weather in Mumbai`
* `Get weather in London and then calculate 100/4`

---

## Key Learning Outcomes

* Task decomposition strategies
* Sequential execution with result chaining
* LLM-based planning techniques
* Intermediate output visualization
* Error handling in multi-step workflows
