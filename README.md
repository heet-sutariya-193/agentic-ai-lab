# Agentic AI Lab Assignments

## Overview

This repository contains four progressive assignments demonstrating Agentic AI concepts, from rule-based agents to multi-step LLM-powered planning systems. Each assignment builds on the previous one to show the evolution of intelligent agents.

---

## Key Highlights

* 4 complete agent implementations
* 6+ tools (calculate, weather, summarize, random, convert, password)
* Direct LLM integration using Gemini API
* Multi-step planning and execution
* Natural language understanding
* Fallback mechanisms for reliability
* Interaction logging using JSON

---

## Assignments

### Assignment 1: Rule-Based Agent

Basic agent using keyword matching and regex for intent detection.

**Features:**

* Greeting responses
* Mathematical calculations
* Date and time handling
* Help system

---

### Assignment 2: Tool-Using Agent

Modular agent with multiple tools and better input handling.

**Tools:**

* Calculate
* Weather
* Summarize
* Random
* Convert
* Password

**Features:**

* Tool selection based on input
* Parameter extraction
* Conversation history

---

### Assignment 3: LLM-Based Agent

Agent enhanced with Gemini API for intelligent tool selection.

**Features:**

* LLM-based decision making
* Rule-based fallback
* Structured tool selection (`tool | params`)
* Interaction logging (`agent_logs.json`)

---

### Assignment 4: Multi-Step Planning Agent

Advanced agent that breaks complex queries into multiple steps and executes them sequentially.

**Features:**

* LLM-based task decomposition
* JSON-based execution plan
* Sequential execution with chaining
* Intermediate outputs
* Fallback planning

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

## Requirements

* Python 3.9+
* Install dependency:

```bash
pip install requests
```

---

## Project Structure

```text
agentic-ai-lab/
├── assignment1/
├── assignment2/
├── assignment3/
├── assignment4/
└── README.md
```

---

## Learning Outcomes

* Agent architecture (Input → Decision → Action)
* Tool abstraction and modular design
* LLM integration and prompt engineering
* Task decomposition and planning
* Sequential execution and state handling

---

## Author

Heet Sutariya

## Date

April 2026
