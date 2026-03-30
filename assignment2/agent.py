"""
Assignment 2: Tool-Using Agent (Enhanced Version)
Agent that can decide which external tool to use based on input
Supports natural language understanding and multiple tools
"""

import re
from tools import TOOLS, get_tool_description

class ToolAgent:
    def __init__(self):
        self.name = "ToolAI"
        self.tools = TOOLS
        self.conversation_history = []
    
    def identify_intent_and_extract(self, user_input):
        """
        Enhanced intent identification with natural language understanding
        """
        user_input_lower = user_input.lower().strip()
        
        # 1. Calculator detection (natural language)
        calc_patterns = [
            r'calculate\s+(.+)',
            r'what is\s+(.+)',
            r'what\'s\s+(.+)',
            r'compute\s+(.+)',
            r'(\d+[\+\-\*/%\^]+\d+)',
            r'(\d+\s*[\+\-\*/]\s*\d+)'
        ]
        
        for pattern in calc_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                expression = match.group(1) if match.lastindex else match.group(0)
                # Clean expression
                expression = re.sub(r'[^0-9+\-*/%^()]', '', expression)
                return ("calculate", expression)
        
        # 2. Weather detection
        weather_patterns = [
            r'weather in\s+([a-zA-Z\s]+)',
            r'temperature in\s+([a-zA-Z\s]+)',
            r'forecast for\s+([a-zA-Z\s]+)'
        ]
        
        for pattern in weather_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                location = match.group(1).strip()
                return ("weather", location)
        
        if 'weather' in user_input_lower or 'temperature' in user_input_lower:
            return ("weather", None)
        
        # 3. Summarize detection
        summarize_patterns = [
            r'summarize\s+(.+)',
            r'summary of\s+(.+)',
            r'shorten\s+(.+)'
        ]
        
        for pattern in summarize_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                text = match.group(1).strip()
                return ("summarize", text)
        
        if 'summarize' in user_input_lower or 'summary' in user_input_lower:
            # Extract text after keyword
            parts = re.split(r'summarize|summary', user_input_lower)
            if len(parts) > 1 and parts[1].strip():
                return ("summarize", parts[1].strip())
            return ("summarize", "Please provide text to summarize")
        
        # 4. Random number detection
        random_patterns = [
            r'random number between\s+(\d+)\s+and\s+(\d+)',
            r'random\s+(\d+)\s+to\s+(\d+)',
            r'random\s+(\d+)-(\d+)'
        ]
        
        for pattern in random_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                return ("random", (match.group(1), match.group(2)))
        
        if 'random' in user_input_lower:
            numbers = re.findall(r'\d+', user_input_lower)
            if len(numbers) >= 2:
                return ("random", (numbers[0], numbers[1]))
            elif len(numbers) == 1:
                return ("random", (1, numbers[0]))
            return ("random", (1, 100))
        
        # 5. Unit conversion detection
        convert_patterns = [
            r'convert\s+(\d+(?:\.\d+)?)\s+([a-z]+)\s+to\s+([a-z]+)',
            r'(\d+(?:\.\d+)?)\s+([a-z]+)\s+in\s+([a-z]+)'
        ]
        
        for pattern in convert_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                value = float(match.group(1))
                from_unit = match.group(2)
                to_unit = match.group(3)
                return ("convert", (value, from_unit, to_unit))
        
        # 6. Password generation
        if 'password' in user_input_lower:
            numbers = re.findall(r'\d+', user_input_lower)
            length = int(numbers[0]) if numbers else 12
            return ("password", length)
        
        # Unknown intent
        return ("unknown", None)
    
    def execute_tool(self, tool_name, params):
        """
        Execute the selected tool with given parameters
        """
        if tool_name not in self.tools:
            return f"Tool '{tool_name}' not found. Available: {', '.join(self.tools.keys())}"
        
        try:
            if tool_name == "calculate":
                return self.tools[tool_name](params)
            
            elif tool_name == "weather":
                return self.tools[tool_name](params)
            
            elif tool_name == "summarize":
                return self.tools[tool_name](params)
            
            elif tool_name == "random":
                if isinstance(params, tuple) and len(params) >= 2:
                    return self.tools[tool_name](params[0], params[1])
                return self.tools[tool_name]()
            
            elif tool_name == "convert":
                if isinstance(params, tuple) and len(params) == 3:
                    return self.tools[tool_name](params[0], params[1], params[2])
                return "Please provide: convert value from_unit to_unit"
            
            elif tool_name == "password":
                return self.tools[tool_name](params if params else 12)
            
            else:
                return self.tools[tool_name](params)
                
        except Exception as e:
            return f"Error executing tool: {str(e)}"
    
    def process(self, user_input):
        """
        Main processing pipeline with conversation tracking
        """
        print(f"\n[INPUT] {user_input}")
        
        # Identify tool and parameters
        tool_name, params = self.identify_intent_and_extract(user_input)
        print(f"[DECISION] Using tool: {tool_name}")
        print(f"[PARAMETERS] {params}")
        
        # Execute tool
        if tool_name == "unknown":
            response = f"I don't know how to handle that.\n{get_tool_description()}"
        else:
            response = self.execute_tool(tool_name, params)
        
        # Store conversation
        self.conversation_history.append({
            "input": user_input,
            "tool": tool_name,
            "response": response
        })
        
        print(f"[ACTION] Tool executed")
        return response
    
    def show_history(self):
        """Display conversation history"""
        if not self.conversation_history:
            return "No conversation history"
        
        print("\n" + "="*50)
        print("CONVERSATION HISTORY")
        print("="*50)
        for i, entry in enumerate(self.conversation_history, 1):
            print(f"\n[{i}] You: {entry['input']}")
            print(f"    Tool: {entry['tool']}")
            print(f"    Agent: {entry['response'][:100]}...")

def main():
    """Interactive main function"""
    print("=" * 70)
    print("Tool-Using Agent - Assignment 2 (Enhanced)")
    print("=" * 70)
    print(get_tool_description())
    print("\n" + "="*70)
    print("Try natural language queries like:")
    print("  - What is 25 multiplied by 4?")
    print("  - Weather in Mumbai")
    print("  - Random number between 1 and 50")
    print("  - Summarize This is a long text...")
    print("  - Convert 10 km to miles")
    print("  - Generate a password of length 8")
    print("  - history - Show conversation history")
    print("  - exit to quit")
    print("="*70)
    
    agent = ToolAgent()
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye! Thanks for using ToolAI!")
            break
        
        if user_input.lower() == 'history':
            agent.show_history()
            continue
        
        if not user_input:
            continue
        
        response = agent.process(user_input)
        print(f"\nAgent: {response}")

if __name__ == "__main__":
    main()