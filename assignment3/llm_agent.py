"""
Assignment 3: LLM-Based Agent with Direct Gemini API
"""

import requests
import json
import datetime
import sys
import re

sys.path.append('C:\\Users\\Heet sutariya\\agentic-ai-lab')
from assignment2.tools import TOOLS, get_tool_description

# Your Gemini API Key directly here
API_KEY = "key"
MODEL_NAME = "gemini-2.5-flash"

class LLMAgent:
    def __init__(self):
        self.name = "LLMAI"
        self.tools = TOOLS
        self.logs = []
        self.use_llm = True
        print(f"Connected to Gemini API using model: {MODEL_NAME}")
    
    def clean_expression(self, expression):
        if not expression:
            return ""
        
        expression = expression.replace(" ", "")
        expression = re.sub(r'[^0-9+\-*/()]', '', expression)
        expression = re.sub(r'\+\+', '+', expression)
        expression = re.sub(r'--', '+', expression)
        
        return expression
    
    def rule_based_decision(self, user_input):
        user_input_lower = user_input.lower()
        
        if any(op in user_input_lower for op in ['+', '-', '*', '/', 'calculate', 'calc']):
            if 'calculate' in user_input_lower:
                expression = user_input.split('calculate')[-1].strip()
            elif 'calc' in user_input_lower:
                expression = user_input.split('calc')[-1].strip()
            else:
                expression = user_input
            
            expression = self.clean_expression(expression)
            return {"tool": "calculate", "params": expression}
        
        elif 'weather' in user_input_lower:
            location_match = re.search(r'in\s+(\w+)', user_input_lower)
            if location_match:
                return {"tool": "weather", "params": location_match.group(1)}
            return {"tool": "weather", "params": None}
        
        elif 'summarize' in user_input_lower:
            text = user_input.split('summarize')[-1].strip()
            return {"tool": "summarize", "params": text}
        
        elif 'random' in user_input_lower:
            return {"tool": "random", "params": "1,100"}
        
        elif 'password' in user_input_lower:
            numbers = re.findall(r'\d+', user_input)
            length = numbers[0] if numbers else 12
            return {"tool": "password", "params": length}
        
        elif 'convert' in user_input_lower:
            return {"tool": "convert", "params": user_input}
        
        else:
            return {"response": "Try: calculate 2+3, weather in Mumbai, random, summarize, convert, or password"}
    
    def llm_decision(self, user_input):
        """Use Gemini API to decide which tool to use"""
        
        # System prompt with ALL tools
        system_prompt = """
You are a decision-making agent. You have these tools:
1. 'calculate': use this for mathematical equations (+, -, *, /, parentheses, %)
2. 'weather': use this for weather inquiries
3. 'summarize': use this to summarize text
4. 'random': use this to generate random numbers
5. 'convert': use this for unit conversions (km to miles, kg to lbs, C to F)
6. 'password': use this to generate random passwords

Based on the user's query, respond ONLY with the exact name of the tool to use, followed by a pipe '|', followed by the argument to pass to the tool.

Examples:
- User: "what is 2+3" → calculate|2+3
- User: "20% of 500" → calculate|(20/100)*500
- User: "weather in Mumbai" → weather|Mumbai
- User: "summarize this text" → summarize|this text
- User: "random number" → random|1,100
- User: "random between 1 and 50" → random|1,50
- User: "convert 10 km to miles" → convert|10 km to miles
- User: "password length 16" → password|16
- User: "generate password" → password|12
- User: "hello" → none|none

Important: Use exact tool names: calculate, weather, summarize, random, convert, password

If you cannot answer, respond with 'none|none'.
"""
        
        # The URL for Gemini API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"
        
        # Payload for the API
        payload = {
            "contents": [{
                "parts": [{"text": f"System Instructions: {system_prompt}\n\nUser Query: {user_input}"}]
            }],
            "generationConfig": {
                "temperature": 0.0
            }
        }
        
        try:
            print("Thinking...")
            response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                llm_text = data['candidates'][0]['content']['parts'][0]['text'].strip()
                print(f"[GEMINI RESPONSE] {llm_text}")
                
                # Parse the decision
                if '|' in llm_text:
                    parts = llm_text.split('|')
                    tool_name = parts[0].strip().lower()
                    params = parts[1].strip() if len(parts) > 1 else None
                    
                    print(f"[DEBUG] Tool: {tool_name}, Params: {params}")
                    
                    # Handle tool selection
                    if tool_name == "calculate":
                        return {"tool": "calculate", "params": params}
                    elif tool_name == "weather":
                        return {"tool": "weather", "params": params}
                    elif tool_name == "summarize":
                        return {"tool": "summarize", "params": params}
                    elif tool_name == "random":
                        return {"tool": "random", "params": params}
                    elif tool_name == "convert":
                        return {"tool": "convert", "params": params}
                    elif tool_name == "password":
                        return {"tool": "password", "params": params}
                    elif tool_name == "none":
                        return {"response": "I don't know how to help with that. Try: calculate, weather, summarize, random, convert, or password"}
                    else:
                        print(f"[DEBUG] Unknown tool, falling back to rule-based")
                        return self.rule_based_decision(user_input)
                else:
                    print(f"[DEBUG] No pipe found, falling back to rule-based")
                    return self.rule_based_decision(user_input)
            else:
                print(f"API Error: {response.status_code}")
                return self.rule_based_decision(user_input)
                
        except Exception as e:
            print(f"API Error: {e}")
            return self.rule_based_decision(user_input)
    
    def execute_tool(self, tool_name, params):
        if tool_name not in self.tools:
            return f"Tool '{tool_name}' not found"
        
        try:
            if tool_name == "calculate":
                if params:
                    params = self.clean_expression(params)
                return self.tools[tool_name](params)
            elif tool_name == "weather":
                return self.tools[tool_name](params)
            elif tool_name == "summarize":
                return self.tools[tool_name](params)
            elif tool_name == "random":
                if params and ',' in params:
                    parts = params.split(',')
                    return self.tools[tool_name](parts[0], parts[1])
                return self.tools[tool_name]()
            elif tool_name == "convert":
                return self.tools[tool_name](params)
            elif tool_name == "password":
                # Extract number from params
                if params:
                    numbers = re.findall(r'\d+', str(params))
                    length = int(numbers[0]) if numbers else 12
                else:
                    length = 12
                return self.tools[tool_name](length)
            else:
                return self.tools[tool_name](params)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def process(self, user_input):
        print(f"\n{'='*50}")
        print(f"[INPUT] {user_input}")
        
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "input": user_input
        }
        
        decision = self.llm_decision(user_input)
        
        if "tool" in decision:
            tool_name = decision["tool"]
            params = decision.get("params", None)
            print(f"[DECISION] Using tool: {tool_name}")
            print(f"[PARAMS] {params}")
            log_entry["selected_tool"] = tool_name
            log_entry["parameters"] = params
            response = self.execute_tool(tool_name, params)
        else:
            response = decision.get("response", "I don't understand")
            print(f"[DECISION] Direct response")
            log_entry["selected_tool"] = "none"
        
        log_entry["output"] = response
        self.logs.append(log_entry)
        
        with open("agent_logs.json", "w") as f:
            json.dump(self.logs, f, indent=2)
        
        print(f"[OUTPUT] {response}")
        return response
    
    def show_logs(self):
        print("\n" + "="*50)
        print("INTERACTION LOGS")
        print("="*50)
        for i, log in enumerate(self.logs, 1):
            print(f"\n[{i}] {log['timestamp']}")
            print(f"   Input: {log['input']}")
            print(f"   Tool: {log.get('selected_tool', 'N/A')}")
            print(f"   Output: {log['output']}")

def main():
    print("=" * 60)
    print("Assignment 3: LLM-Based Agent with Gemini API")
    print("=" * 60)
    print(get_tool_description())
    print("\n" + "="*60)
    print("Try these examples:")
    print("  calculate 100/(9-5)")
    print("  weather in Mumbai")
    print("  random number")
    print("  summarize This is a test text.")
    print("  password length 16")
    print("  convert 10 km to miles")
    print("  What is 25 multiplied by 4?")
    print("  exit to quit")
    print("="*60)
    
    agent = LLMAgent()
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                agent.show_logs()
                print("\nGoodbye!")
                break
            
            if not user_input:
                continue
            
            response = agent.process(user_input)
            print(f"\nAgent: {response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break

if __name__ == "__main__":
    main()
