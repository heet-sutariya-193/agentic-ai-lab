# Assignment 1: Simple Rule-Based Agent

## Objective

Create a simple rule-based agent that identifies user intent using keyword matching and performs appropriate actions.

---

## Features

### 1. Greeting

* Responds to greetings like "hello", "hi", "hey"
* Time-based greetings (morning, afternoon, evening, night)

### 2. Calculations

* Performs basic arithmetic operations (`+`, `-`, `*`, `/`, `%`)
* Supports parentheses
* Handles natural language queries (e.g., "what is 2+3")

### 3. Date and Time

* Displays current date and time in multiple formats

### 4. Help System

* Shows available commands with examples

---

## Architecture

The agent follows a simple pipeline:

1. **Input Handler** – Accepts user input
2. **Decision Logic** – Identifies intent using keyword matching and regex
3. **Action Execution** – Executes the appropriate response

---

## How to Run

```bash
python simple_agent.py
```

---

## Example Interactions

```text
You: hello
Agent: Good afternoon! How can I help you today?

You: calculate 2+3
Agent: Result: 5

You: what is 10 * 5?
Agent: Result: 50

You: date
Agent: Current date and time:
  • 2026-03-30 14:30:25
  • Monday, March 30, 2026 at 02:30 PM

You: help
Agent: Available Commands:
  • hello, hi, hey - Greeting
  • calculate [expression] - Math operations
  • date, time, today - Show current date and time
  • help - Show this help message

You: exit
Agent: Goodbye! Have a great day!
```

---

## Code Structure

* `SimpleAgent` class – Core agent logic
* `identify_intent()` – Detects user intent using keywords
* `execute_action()` – Executes corresponding actions
* `process()` – Main pipeline handler
* `main()` – Interactive loop

---

## Requirements

* Python 3.9 or above
* No external dependencies

---

## Testing

Try the following inputs:

* `hello` → Greeting response
* `calculate 10+20` → 30
* `date` → Current date/time
* `what is 100/4` → 25
* `help` → Command list
* `exit` → Exit program
