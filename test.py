from google import genai

API_KEY = "AIzaSyD64DEr782z79FHTkivO8Lt0neyCqhg3Gg"

client = genai.Client(api_key=API_KEY)

# Test with a model that exists in your list
response = client.models.generate_content(
    model="gemini-3.1-flash-lite-preview",
    contents="Say hello in one word"
)

print("SUCCESS! Response:", response.text)