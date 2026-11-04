# Repzilla

Telegram fitness bot built with Python, aiogram 3, SQLAlchemy async and SQLite/PostgreSQL.

## Local run

1. Create a virtual environment and install dependencies:
   `python -m pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and fill in `BOT_TOKEN` (and optionally `GROQ_API_KEY`).
3. Start with `python bot.py`.

## Render deployment

- Deploy this repository as a **Background Worker** using the included Dockerfile.
- Set `BOT_TOKEN` in the Render environment. `GROQ_API_KEY` is optional; AI requests need it.
- For persistent user data, configure `DATABASE_URL` to a persistent database. Example for a Render persistent disk mounted at `/var/data`:
  `sqlite+aiosqlite:////var/data/bot.db`
- Or use PostgreSQL with `postgresql+asyncpg://...`; `asyncpg` is included in requirements.
- A worker does not need an HTTP health-check server. The bot runs Telegram long polling.

Never commit `.env`, database files, virtual environments, or API credentials.
