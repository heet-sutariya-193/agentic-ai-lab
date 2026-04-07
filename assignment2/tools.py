"""
Assignment 2: Tool definitions for the agent (Enhanced Version)
Contains all external tools/functions the agent can use
"""

import datetime
import math
import random
import re

def calculate(expression):
    """
    Perform mathematical calculations with enhanced features
    Supports: +, -, *, /, %, **, parentheses, square root, power
    """
    import re
    
    try:
        original = expression
        expression = expression.replace(" ", "")
        
        # Handle "X% of Y" pattern - THIS IS THE KEY FIX
        # Matches: 25% of 200, 25%of200, 25% of200, 25%of 200
        pattern = re.compile(r'(\d+(?:\.\d+)?)%\s*[oO][fF]\s*(\d+(?:\.\d+)?)')
        
        def convert_percent_of(m):
            p = float(m.group(1))
            n = float(m.group(2))
            return str((p / 100) * n)
        
        # Apply the conversion repeatedly until no matches
        while pattern.search(expression):
            expression = pattern.sub(convert_percent_of, expression)
        
        # Handle remaining percentage signs (e.g., "50%")
        if '%' in expression:
            expression = re.sub(r'(\d+(?:\.\d+)?)%', r'(\1/100)', expression)
        
        # Handle square root
        if "sqrt" in expression:
            sqrt_match = re.search(r'sqrt\((\d+)\)', expression)
            if sqrt_match:
                num = float(sqrt_match.group(1))
                result = math.sqrt(num)
                return f"Result: {result}"
        
        # Handle power operator
        if "^" in expression:
            expression = expression.replace("^", "**")
        
        # Evaluate
        result = eval(expression)
        
        # Format result nicely
        if isinstance(result, float):
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 4)
        
        return f"Result: {result}"
        
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Error: {str(e)}"

# Tool 2: Enhanced Weather (with more cities)
def get_weather(location=None):
    """
    Enhanced weather function with more cities and conditions
    """
    # Comprehensive weather database
    weather_data = {
        # India
        "mumbai": "Humid, 32°C / 90°F, 70% humidity",
        "delhi": "Hazy, 35°C / 95°F, 45% humidity",
        "bangalore": "Pleasant, 25°C / 77°F, 60% humidity",
        "chennai": "Humid, 33°C / 91°F, 75% humidity",
        "kolkata": "Humid, 31°C / 88°F, 80% humidity",
        "surat": "Sunny, 34°C / 93°F, 55% humidity",
        "ahmedabad": "Hot, 36°C / 97°F, 40% humidity",
        "pune": "Pleasant, 28°C / 82°F, 65% humidity",
        "jaipur": "Sunny, 33°C / 91°F, 35% humidity",
        "lucknow": "Clear, 30°C / 86°F, 50% humidity",
        "nagpur": "Hot, 38°C / 100°F, 30% humidity",
        "indore": "Pleasant, 29°C / 84°F, 55% humidity",
        "bhopal": "Clear, 31°C / 88°F, 45% humidity",
        "patna": "Humid, 32°C / 90°F, 70% humidity",
        "vadodara": "Sunny, 35°C / 95°F, 50% humidity",
        "rajkot": "Sunny, 34°C / 93°F, 45% humidity",
        
        # International
        "new york": "Partly Cloudy, 22°C / 72°F, 60% humidity",
        "london": "Cloudy, 12°C / 54°F, 80% humidity",
        "tokyo": "Rainy, 18°C / 64°F, 85% humidity",
        "paris": "Cloudy, 15°C / 59°F, 75% humidity",
        "sydney": "Sunny, 24°C / 75°F, 55% humidity",
        "dubai": "Hot, 38°C / 100°F, 30% humidity",
        "singapore": "Rainy, 28°C / 82°F, 85% humidity",
        "beijing": "Hazy, 20°C / 68°F, 50% humidity",
        "moscow": "Snowy, -5°C / 23°F, 90% humidity",
        "berlin": "Cloudy, 10°C / 50°F, 70% humidity",
        "rome": "Sunny, 25°C / 77°F, 55% humidity",
    }
    
    if location:
        location_clean = location.strip().lower()
        
        if location_clean in weather_data:
            return f"Weather in {location.title()}: {weather_data[location_clean]}"
        else:
            # Generate realistic weather for unknown locations
            location_hash = sum(ord(c) for c in location_clean) % 100
            
            if location_hash < 20:
                condition = "Sunny"
                temp_c = random.randint(25, 38)
            elif location_hash < 40:
                condition = "Partly Cloudy"
                temp_c = random.randint(20, 30)
            elif location_hash < 60:
                condition = "Cloudy"
                temp_c = random.randint(15, 25)
            elif location_hash < 80:
                condition = "Light Rain"
                temp_c = random.randint(12, 22)
            else:
                condition = "Windy"
                temp_c = random.randint(10, 20)
            
            temp_f = int((temp_c * 9/5) + 32)
            humidity = random.randint(40, 90)
            
            return f"Weather in {location.title()}: {condition}, {temp_c}°C / {temp_f}°F, {humidity}% humidity (Estimated)"
    else:
        return f"Current weather: Partly cloudy, 21°C / 70°F, 65% humidity"

# Tool 3: Enhanced Text Summarizer
def summarize_text(text, max_sentences=3):
    """
    Enhanced text summarizer with better sentence detection
    """
    if not text:
        return "No text provided to summarize"
    
    # Split into sentences (handles multiple punctuation)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) <= max_sentences:
        summary = text
    else:
        summary = '. '.join(sentences[:max_sentences]) + '...'
    
    # Add word count info
    word_count = len(text.split())
    summary_word_count = len(summary.split())
    
    return f"Summary ({summary_word_count} words, original {word_count} words):\n{summary}"

# Tool 4: Enhanced Random Number Generator
def random_number(min_val=1, max_val=100):
    """
    Generate random numbers with multiple formats
    """
    try:
        min_val = int(min_val)
        max_val = int(max_val)
        
        if min_val > max_val:
            min_val, max_val = max_val, min_val
        
        result = random.randint(min_val, max_val)
        
        # Add fun fact
        facts = [
            "That's your lucky number!",
            "Interesting choice!",
            "Here's your random number.",
            "Randomness delivered!"
        ]
        
        return f"Random number between {min_val} and {max_val}: {result}\n{random.choice(facts)}"
    except Exception as e:
        return f"Error: {str(e)}"

# Tool 5: Bonus - Unit Converter
def convert_units(value, from_unit, to_unit):
    """
    Convert between different units (length, weight, temperature)
    """
    conversions = {
        # Length
        "km_to_miles": 0.621371,
        "miles_to_km": 1.60934,
        "m_to_feet": 3.28084,
        "feet_to_m": 0.3048,
        
        # Weight
        "kg_to_lbs": 2.20462,
        "lbs_to_kg": 0.453592,
        
        # Temperature
        "c_to_f": lambda c: (c * 9/5) + 32,
        "f_to_c": lambda f: (f - 32) * 5/9,
    }
    
    key = f"{from_unit}_to_{to_unit}"
    
    if key in conversions:
        if callable(conversions[key]):
            result = conversions[key](value)
        else:
            result = value * conversions[key]
        return f"Conversion: {value} {from_unit} = {result:.2f} {to_unit}"
    else:
        return "Conversion not supported. Try: km_to_miles, kg_to_lbs, c_to_f"

# Tool 6: Bonus - Password Generator
def generate_password(length=12):
    """
    Generate a random password
    """
    import string
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(characters) for _ in range(int(length)))
    return f"Generated password: {password}"

# Dictionary mapping tool names to functions
TOOLS = {
    "calculate": calculate,
    "weather": get_weather,
    "summarize": summarize_text,
    "random": random_number,
    "convert": convert_units,
    "password": generate_password
}

def get_tool_description():
    """Return description of available tools"""
    return """
Available tools:
1. calculate - Perform math operations (+, -, *, /, %, ^, sqrt)
2. weather - Get weather for cities worldwide
3. summarize - Summarize long text
4. random - Generate random numbers
5. convert - Convert units (km_to_miles, kg_to_lbs, c_to_f)
6. password - Generate random password

Examples:
  - calculate 2+3
  - weather in Mumbai
  - summarize Your long text here...
  - random number between 1 and 100
  - convert 10 km_to_miles
  - password 12
"""