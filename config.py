import os
from dotenv import load_dotenv
from agents import set_default_openai_key

# ✅ Load variables from .env file
load_dotenv()

# ✅ Get the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

# ✅ Ensure it's set, otherwise raise a clear error
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in environment. Please set it in your .env file.")

# ✅ Set key for OpenAI Agents SDK
set_default_openai_key(api_key)
