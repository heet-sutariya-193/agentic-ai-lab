# Agentic AI Lab Assignments

## Overview

This repository contains four progressive assignments demonstrating Agentic AI concepts, ranging from basic rule-based agents to advanced multi-step planning agents with LLM integration.

---

## Assignments

### Assignment 1: Simple Rule-Based Agent

A basic agent that uses keyword matching to identify user intent and perform actions.

* **Location**: `/assignment1`
* **Key Features**:

  * Intent identification
  * Basic calculations
  * Date and time handling
  * Greeting responses

---

### Assignment 2: Tool-Using Agent

An agent with modular tools that can perform various tasks based on user input.

* **Location**: `/assignment2`
* **Key Features**:

  * Multiple tools (calculate, weather, summarize, random, convert, password)
  * Modular architecture
  * Tool selection based on input

---

### Assignment 3: LLM-Based Agent

An agent that uses Groq's LLM API for intelligent decision-making with logging support.

* **Location**: `/assignment3`
* **Key Features**:

  * LLM integration
  * Rule-based fallback system
  * Interaction logging

---

### Assignment 4: Multi-Step Agent

An agent that breaks complex tasks into multiple steps and executes them sequentially.

* **Location**: `/assignment4`
* **Key Features**:

  * Task decomposition
  * Sequential execution
  * Intermediate outputs

---

## Requirements

* Python 3.9 or above
* Required package:

  ```bash
  pip install openai
  ```
* Groq API key (optional, for Assignment 3 LLM mode)

---

## How to Run

```bash
# Assignment 1
cd assignment1
python simple_agent.py

# Assignment 2
cd assignment2
python agent.py

# Assignment 3
cd assignment3
python llm_agent.py

# Assignment 4
cd assignment4
python multi_step_agent.py
```

---

## Project Structure

```text
agentic-ai-lab/
├── assignment1/
│   ├── simple_agent.py
│   └── README.md
├── assignment2/
│   ├── tools.py
│   ├── agent.py
│   └── README.md
├── assignment3/
│   ├── llm_agent.py
│   └── README.md
├── assignment4/
│   ├── multi_step_agent.py
│   └── README.md
└── README.md
```

---

## Learning Outcomes

* Understanding agent architecture (Input → Decision → Action)
* Tool abstraction and modular programming
* LLM integration for intelligent decision-making
* Task decomposition and sequential planning
* Logging and error handling

---

## Author

Heet Sutariya

---

## Date

March 2026
