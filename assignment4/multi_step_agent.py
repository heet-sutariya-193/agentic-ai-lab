"""
Assignment 4: Multi-Step Planning Agent with Gemini API
"""

import requests
import json
import datetime
import sys
import re

sys.path.append('C:\\Users\\Heet sutariya\\agentic-ai-lab')
try:
    from assignment2.tools import TOOLS
except ImportError:
    print("Error: Could not find tools.py in assignment2 folder.")
    TOOLS = {}

# Your Gemini API Key
API_KEY = "AIzaSyD64DEr782z79FHTkivO8Lt0neyCqhg3Gg"
MODEL_NAME = "gemini-2.5-flash"

class MultiStepAgent:
    def __init__(self):
        self.name = "PlannerAI"
        self.tools = TOOLS
        self.use_llm = True
        print(f"Connected to Gemini API using model: {MODEL_NAME}")

    def create_plan(self, user_query):
        """
        Task Decomposition: Uses LLM to break query into a sequence of steps.
        """
        system_prompt = f"""
You are a planning agent. Break the user request into a list of sequential steps.
Available tools: calculate, weather, summarize, random, convert, password.

User Request: "{user_query}"

Return ONLY a JSON list of objects. Each object must have:
"step": (integer),
"tool": (tool_name),
"params": (the specific input for that tool)

Important rules:
- For calculate, params should be a math expression like "10+20+30" or "(10+20+30)/3"
- For weather, params should be a city name
- For summarize, params should be the text to summarize
- For random, params should be like "1,100"
- For convert, params should be like "10 km to miles"
- For password, params should be like "16"

Examples:
Example for "Find average of 5, 10, 15":
[
    {{"step": 1, "tool": "calculate", "params": "5+10+15"}},
    {{"step": 2, "tool": "calculate", "params": "(5+10+15)/3"}}
]

Example for "Find average of 10, 20, 30 and summarize":
[
    {{"step": 1, "tool": "calculate", "params": "10+20+30"}},
    {{"step": 2, "tool": "calculate", "params": "(10+20+30)/3"}},
    {{"step": 3, "tool": "summarize", "params": "The average is"}}
]

Example for "Get weather and then calculate":
[
    {{"step": 1, "tool": "weather", "params": "London"}},
    {{"step": 2, "tool": "calculate", "params": "100/4"}}
]

Return ONLY the JSON list, no other text.
"""
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"
        
        payload = {
            "contents": [{
                "parts": [{"text": system_prompt}]
            }],
            "generationConfig": {
                "temperature": 0.0
            }
        }
        
        try:
            print("Planning...")
            response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                content = data['candidates'][0]['content']['parts'][0]['text'].strip()
                print(f"[PLAN RAW] {content}")
                
                # Parse the JSON response
                try:
                    data = json.loads(content)
                    
                    if isinstance(data, list):
                        return data
                    elif isinstance(data, dict):
                        if "steps" in data:
                            return data["steps"]
                        elif "plan" in data:
                            return data["plan"]
                        else:
                            for value in data.values():
                                if isinstance(value, list):
                                    return value
                            return []
                    else:
                        return []
                        
                except json.JSONDecodeError as e:
                    print(f"JSON Parse Error: {e}")
                    return self.fallback_plan(user_query)
            else:
                print(f"API Error: {response.status_code}")
                return self.fallback_plan(user_query)
                
        except Exception as e:
            print(f"Planning Error: {e}")
            return self.fallback_plan(user_query)
    
    def fallback_plan(self, user_query):
        """Simple rule-based fallback if LLM planning fails"""
        query_lower = user_query.lower()
        plan = []
        
        # Check for average calculation
        if "average" in query_lower or "avg" in query_lower:
            numbers = re.findall(r'\d+', user_query)
            if len(numbers) >= 2:
                numbers_str = '+'.join(numbers)
                plan.append({
                    "step": 1,
                    "tool": "calculate",
                    "params": numbers_str
                })
                plan.append({
                    "step": 2,
                    "tool": "calculate",
                    "params": f"({numbers_str})/{len(numbers)}"
                })
                
                if "summarize" in query_lower or "summary" in query_lower:
                    plan.append({
                        "step": 3,
                        "tool": "summarize",
                        "params": "average result"
                    })
                return plan
        
        # Check for weather
        elif "weather" in query_lower:
            location_match = re.search(r'in\s+(\w+)', query_lower)
            location = location_match.group(1) if location_match else "default"
            plan.append({
                "step": 1,
                "tool": "weather",
                "params": location
            })
            return plan
        
        # Check for random number
        elif "random" in query_lower:
            plan.append({
                "step": 1,
                "tool": "random",
                "params": "1,100"
            })
            return plan
        
        # Check for password
        elif "password" in query_lower:
            numbers = re.findall(r'\d+', user_query)
            length = numbers[0] if numbers else 12
            plan.append({
                "step": 1,
                "tool": "password",
                "params": length
            })
            return plan
        
        # Check for convert
        elif "convert" in query_lower:
            plan.append({
                "step": 1,
                "tool": "convert",
                "params": user_query
            })
            return plan
        
        # Default single-step plan
        plan.append({
            "step": 1,
            "tool": "calculate",
            "params": user_query
        })
        return plan

    def execute_plan(self, plan):
        results = []
        previous_result = None
        
        print("\n" + "="*50)
        print("EXECUTION PHASE")
        print("="*50)
        
        for step in plan:
            step_num = step.get("step")
            tool_name = step.get("tool")
            params = step.get("params")
            
            print(f"\n[STEP {step_num}] Tool: {tool_name}")
            print(f"[STEP {step_num}] Params: {params}")
            
            if tool_name not in self.tools:
                result = f"Error: Tool '{tool_name}' not found"
                print(f"[STEP {step_num}] Result: {result}")
                results.append(result)
                continue
            
            try:
                if tool_name == "calculate":
                    if params:
                        # Handle placeholders for previous results
                        if previous_result is not None and "X" in str(params):
                            match = re.search(r'\d+\.?\d*', str(previous_result))
                            if match:
                                num = match.group()
                                params = str(params).replace("X", num)
                        result = self.tools[tool_name](params)
                    else:
                        result = "Error: No calculation provided"
                
                elif tool_name == "weather":
                    result = self.tools[tool_name](params)
                
                elif tool_name == "summarize":
                    if previous_result is not None:
                        match = re.search(r'\d+\.?\d*', str(previous_result))
                        if match:
                            number = match.group()
                            if "average" in str(params).lower():
                                result = self.tools[tool_name](f"The average is {number}")
                            else:
                                result = self.tools[tool_name](f"The result is {number}")
                        else:
                            result = self.tools[tool_name](str(previous_result))
                    else:
                        result = self.tools[tool_name](params if params else "No text to summarize")
                
                elif tool_name == "random":
                    if params and ',' in str(params):
                        parts = str(params).split(',')
                        result = self.tools[tool_name](parts[0].strip(), parts[1].strip())
                    else:
                        result = self.tools[tool_name]()
                
                elif tool_name == "password":
                    length = int(params) if params else 12
                    result = self.tools[tool_name](length)
                
                elif tool_name == "convert":
                    result = self.tools[tool_name](params)
                
                else:
                    result = self.tools[tool_name](params)
                
                print(f"[STEP {step_num}] Result: {result}")
                results.append(result)
                
                # Store result for potential use in next steps
                match = re.search(r'[-+]?\d*\.?\d+', str(result))
                if match:
                    previous_result = float(match.group())
                else:
                    previous_result = result
                    
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                print(f"[STEP {step_num}] {error_msg}")
                results.append(error_msg)
        
        return results

    def process(self, user_query):
        """
        Main Pipeline: Input -> Plan -> Action -> Output
        """
        print(f"\n{'='*60}")
        print(f"QUERY: {user_query}")
        print("="*60)
        
        # Step 1: Create plan (Task Decomposition)
        print("\n[PLANNING PHASE]")
        plan = self.create_plan(user_query)
        
        if not plan:
            return "Failed to create a plan. Please try a simpler query."
        
        # Display the plan
        print("\nPlan Created:")
        for step in plan:
            print(f"  Step {step['step']}: {step['tool']} - {step['params']}")
        
        # Step 2: Execute plan sequentially
        results = self.execute_plan(plan)
        
        # Step 3: Generate final output
        print("\n" + "="*50)
        print("FINAL OUTPUT")
        print("="*50)
        
        if results:
            for i, result in enumerate(results, 1):
                print(f"Step {i} Result: {result}")
            
            return f"Completed! Final result: {results[-1]}"
        else:
            return "No results generated."

def main():
    print("="*60)
    print("Assignment 4: Multi-Step Planning Agent with Gemini API")
    print("="*60)
    print("\nThis agent can break complex tasks into multiple steps.")
    print("\nExample queries:")
    print("  - Find the average of 10, 20, 30 and then summarize the result")
    print("  - Get weather in London and then calculate 100/4")
    print("  - Generate a random number and then add 10 to it")
    print("  - Generate a password of length 16")
    print("  - Convert 100 km to miles")
    print("\nType 'exit' to quit")
    print("="*60)
    
    agent = MultiStepAgent()
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            response = agent.process(user_input)
            print(f"\nAgent: {response}")
            
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()