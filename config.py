import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
AI_MODEL = os.getenv("AI_MODEL", "llama-3.3-70b-versatile")
DATABASE_URL = "sqlite+aiosqlite:///fitness_bot.db"
