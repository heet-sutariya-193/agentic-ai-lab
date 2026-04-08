# Assignment 2: Tool-Using Agent

## Objective

Extend the simple agent to use external tools (functions/APIs) with a modular architecture.

---

## Tools Available

| Tool          | Description                                            | Examples                                     |
| ------------- | ------------------------------------------------------ | -------------------------------------------- |
| **calculate** | Math operations (`+`, `-`, `*`, `/`, `%`, `^`, `sqrt`) | `calculate 2+3`, `what is 10*5`              |
| **weather**   | Weather for cities worldwide                           | `weather in Mumbai`, `temperature in London` |
| **summarize** | Text summarization with word count                     | `summarize Your long text here...`           |
| **random**    | Random number generation                               | `random number`, `random between 1 and 50`   |
| **convert**   | Unit conversion (km/miles, kg/lbs, C/F)                | `convert 10 km to miles`                     |
| **password**  | Random password generator                              | `password 12`                                |

---

## Features

### Natural Language Understanding

* Understands queries like "what is 25 multiplied by 4?"
* Extracts parameters intelligently from user input

### Conversation History

* Tracks all interactions
* Use `history` to view previous conversations

### Modular Architecture

* `tools.py`: Contains all tool implementations
* `agent.py`: Handles tool selection and execution

---

## How to Run

```bash id="q1r7mx"
python agent.py
```

---

## Example Interactions

```text id="k8z2vn"
You: weather in Mumbai
Agent: Weather in Mumbai: Humid, 32°C / 90°F, 70% humidity

You: random number between 1 and 50
Agent: Random number between 1 and 50: 27
That's your lucky number!

You: summarize The quick brown fox jumps over the lazy dog. This is a test sentence.
Agent: Summary (10 words, original 15 words):
The quick brown fox jumps over the lazy dog. This is a test sentence.

You: convert 10 km to miles
Agent: Conversion: 10 km = 6.21 miles

You: password 8
Agent: Generated password: aB3@xY7#

You: history
Agent: Shows conversation history
```

---

## Code Structure

### tools.py

* `calculate()` – Advanced calculator (sqrt, power, percentage)
* `get_weather()` – Weather data for multiple cities
* `summarize_text()` – Text summarization with word count
* `random_number()` – Random number generator
* `convert_units()` – Unit conversion utility
* `generate_password()` – Secure password generator

### agent.py

* `identify_intent_and_extract()` – Parses user input
* `execute_tool()` – Executes tools with error handling
* `process()` – Main pipeline
* `show_history()` – Displays conversation history

---

## Requirements

* Python 3.9 or above
* No external dependencies

---

## Testing

Try the following:

* `calculate 100/4` → 25
* `weather in New York` → Weather data
* `random` → Random number
* `summarize your text` → Summary
* `convert 5 kg to lbs` → 11.02 lbs
* `password` → Generated password
* `history` → Conversation log

# screenshot of result
<img width="569" height="397" alt="image" src="https://github.com/user-attachments/assets/efe4ceae-f03d-482b-b521-322897a37a5b" />
<img width="539" height="500" alt="Screenshot 2026-04-08 111741" src="https://github.com/user-attachments/assets/ddcf5be9-deb5-40b2-bae9-e58b4e9b3ee4" />

