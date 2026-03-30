"""
Assignment 3: LLM-Based Agent with Groq API - Fixed Version
"""

import os
import json
import datetime
import sys
import re

sys.path.append('C:\\Users\\Heet sutariya\\agentic-ai-lab')
from assignment2.tools import TOOLS, get_tool_description

class LLMAgent:
    def __init__(self):
        self.name = "LLMAI"
        self.tools = TOOLS
        self.logs = []
        
        # PUT YOUR GROQ API KEY DIRECTLY HERE
        YOUR_GROQ_API_KEY = "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"
        
        try:
            print("Using Groq API")
            from openai import OpenAI
            self.client = OpenAI(
                api_key=YOUR_GROQ_API_KEY,
                base_url="https://api.groq.com/openai/v1"
            )
            self.model = "llama-3.1-8b-instant"
            self.use_llm = True
        except Exception as e:
            print(f"Error: {e}")
            print("Falling back to rule-based mode")
            self.use_llm = False
            self.client = None
    
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
        
        else:
            return {"response": "Try: calculate 2+3, weather in Mumbai, random, or summarize text"}
    
    def llm_decision(self, user_input):
        if not self.use_llm:
            return self.rule_based_decision(user_input)
        
        try:
            prompt = f"""You are an AI assistant. Choose the right tool for this user request: "{user_input}"

Available tools:
- calculate: For mathematical calculations. Example: user says "calculate 100 divided by 4", you respond with tool calculate and params "100/4"
- weather: For weather information. Example: user says "weather in London", you respond with tool weather and params "London"
- summarize: To summarize text. Example: user says "summarize this is a long text", you respond with tool summarize and params "this is a long text"
- random: To generate random numbers. Example: user says "random number", you respond with tool random and params "1,100"

Your response must be a valid JSON object with no extra text. Examples:
{"tool": "calculate", "params": "100/4"}
{"tool": "weather", "params": "London"}
{"tool": "summarize", "params": "text to summarize"}
{"tool": "random", "params": "1,100"}

Now respond with only the JSON object:"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=150
            )
            
            result = response.choices[0].message.content.strip()
            print(f"[API RESPONSE] {result}")
            
            try:
                decision = json.loads(result)
                if decision.get("tool") == "calculate":
                    params = decision.get("params", "")
                    decision["params"] = self.clean_expression(params)
                return decision
            except json.JSONDecodeError as e:
                print(f"JSON parse error: {e}")
                return self.rule_based_decision(user_input)
                
        except Exception as e:
            print(f"API Error: {e}")
            print("Using rule-based instead")
            return self.rule_based_decision(user_input)
    
    def execute_tool(self, tool_name, params):
        if tool_name not in self.tools:
            return f"Tool '{tool_name}' not found"
        
        try:
            if tool_name == "calculate":
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
    print("Assignment 3: LLM-Based Agent")
    print("=" * 60)
    print(get_tool_description())
    print("\n" + "="*60)
    print("Try these examples:")
    print("  calculate 100/(9-5)")
    print("  weather in Mumbai")
    print("  random number")
    print("  summarize This is a test text.")
    print("  exit to quit")
    print("="*60)
    
    agent = LLMAgent()
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            agent.show_logs()
            print("\nGoodbye!")
            break
        
        if not user_input:
            continue
        
        response = agent.process(user_input)
        print(f"\nAgent: {response}")

if __name__ == "__main__":
    main()