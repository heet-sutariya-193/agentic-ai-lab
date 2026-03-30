"""
Assignment 1: Simple Rule-Based Agent (Enhanced Version)
A basic agent that uses keyword matching to identify intent and perform actions
"""

import datetime
import random
import re

class SimpleAgent:
    def __init__(self):
        """Initialize the agent with basic responses"""
        self.name = "SimpleAI"
        self.greetings = ["hello", "hi", "hey", "good morning", "good evening", "howdy", "greetings"]
        self.farewells = ["bye", "goodbye", "see you", "take care"]
        self.help_keywords = ["help", "what can you do", "commands", "assist"]
        
    def calculate(self, expression):
        """
        Safely evaluate mathematical expressions with enhanced error handling
        """
        try:
            # Remove spaces
            expression = expression.replace(" ", "")
            
            # Handle percentage calculations
            if '%' in expression:
                expression = expression.replace('%', '/100')
            
            # Validate characters
            allowed_chars = set("0123456789+-*/()%. ")
            if not all(c in allowed_chars for c in expression):
                return "I can only handle basic math (+, -, *, /, %, parentheses)"
            
            # Evaluate the expression
            result = eval(expression)
            
            # Format result nicely
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 4)
            
            return f"Result: {result}"
            
        except ZeroDivisionError:
            return "Error: Cannot divide by zero"
        except SyntaxError:
            return "Error: Invalid expression. Example: calculate 2+3"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_date(self):
        """Return current date and time in multiple formats"""
        now = datetime.datetime.now()
        
        # Multiple format options
        formats = [
            now.strftime('%Y-%m-%d %H:%M:%S'),
            now.strftime('%A, %B %d, %Y at %I:%M %p'),
            now.strftime('%d/%m/%Y %H:%M')
        ]
        
        return f"Current date and time:\n  • {formats[0]}\n  • {formats[1]}"
    
    def greet(self):
        """Return a personalized greeting"""
        hour = datetime.datetime.now().hour
        
        # Time-based greeting
        if hour < 12:
            time_greeting = "Good morning"
        elif hour < 17:
            time_greeting = "Good afternoon"
        elif hour < 20:
            time_greeting = "Good evening"
        else:
            time_greeting = "Good night"
        
        responses = [
            f"{time_greeting}! How can I help you today?",
            f"Hello! {time_greeting}! What can I do for you?",
            f"Hi there! {time_greeting}! Ready to assist you."
        ]
        
        return random.choice(responses)
    
    def show_help(self):
        """Display available commands"""
        return """
Available Commands:
  • hello, hi, hey - Greeting
  • calculate [expression] - Math operations (+, -, *, /, %)
    Examples: calculate 2+3, calculate 10*5, calculate 100/4
  • date, time, today - Show current date and time
  • help, commands - Show this help message
  • exit, quit, bye - Exit the program

I can understand natural language too! Try:
  • "What is 2 plus 3?"
  • "Show me the time"
  • "Say hello"
"""
    
    def identify_intent(self, user_input):
        """
        Enhanced intent identification with natural language understanding
        """
        user_input_lower = user_input.lower().strip()
        
        # Check for help intent
        if any(keyword in user_input_lower for keyword in self.help_keywords):
            return ("help", None)
        
        # Check for farewell
        if any(word in user_input_lower for word in self.farewells):
            return ("farewell", None)
        
        # Enhanced calculation detection (natural language)
        calc_patterns = [
            r'calculate\s+(.+)',
            r'what is\s+(.+)',
            r'what\'s\s+(.+)',
            r'compute\s+(.+)',
            r'(\d+[\+\-\*/\%]\d+)'
        ]
        
        for pattern in calc_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                expression = match.group(1) if match.lastindex else match.group(0)
                return ("calculate", expression)
        
        # Date/time detection
        if any(word in user_input_lower for word in ["date", "time", "today", "current date", "current time"]):
            return ("date", None)
        
        # Greeting detection
        if any(greet in user_input_lower for greet in self.greetings):
            return ("greet", None)
        
        # Unknown intent with suggestion
        return ("unknown", None)
    
    def execute_action(self, intent, data):
        """Execute action based on identified intent"""
        if intent == "calculate":
            if data:
                return self.calculate(data)
            else:
                return "Please provide a calculation. Example: calculate 2+3 or what is 10*5?"
        
        elif intent == "date":
            return self.get_date()
        
        elif intent == "greet":
            return self.greet()
        
        elif intent == "help":
            return self.show_help()
        
        elif intent == "farewell":
            return "Goodbye! Have a great day!"
        
        else:
            return "I'm not sure how to help. Type 'help' to see what I can do."
    
    def process(self, user_input):
        """Main processing pipeline: Input -> Decision -> Action"""
        print(f"\n[INPUT] {user_input}")
        
        # Identify intent
        intent, data = self.identify_intent(user_input)
        print(f"[DECISION] Intent identified: {intent}")
        
        # Execute action
        response = self.execute_action(intent, data)
        print(f"[ACTION] Response generated")
        
        return response

def main():
    """Main interactive loop"""
    print("=" * 60)
    print("Simple AI Agent - Assignment 1 (Enhanced)")
    print("=" * 60)
    print("\nI'm a rule-based AI agent that can:")
    print("  • Greet you based on time of day")
    print("  • Perform calculations")
    print("  • Show current date and time")
    print("  • Help you with commands")
    print("\nType 'help' to see all commands")
    print("Type 'exit' to quit")
    print("=" * 60)
    
    agent = SimpleAgent()
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
            print("\nAgent: Goodbye! Have a great day!")
            break
        
        if not user_input:
            continue
        
        response = agent.process(user_input)
        print(f"\nAgent: {response}")

if __name__ == "__main__":
    main()