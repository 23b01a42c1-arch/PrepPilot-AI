import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_MODEL = "llama-3.1-8b-instant"

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)