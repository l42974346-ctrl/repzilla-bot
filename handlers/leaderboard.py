from aiogram import Router, F
from aiogram.types import Message
import database as db

leaderboard_router = Router()

@leaderboard_router.message(F.text == "🏆 Лидерборд")
async def show_leaderboard(message: Message):
    top = await db.get_top_users(15)
    user = await db.get_user(message.from_user.id)
    
    txt = "🏆 **ТОП-15 АТЛЕТОВ REPZILLA**\n\n"
    medals = ["🥇", "🥈", "🥉"] + ["🎖"] * 12
    for i, u in enumerate(top):
        name = u.first_name or u.username or "Атлет"
        txt += f"{medals[i]} **{name}** — {u.rank}\n   Lvl {u.level} • {u.xp} XP\n\n"
    
    if user:
        txt += f"━━━━━━━━━━━━━━\n"
        txt += f"👤 **ТВОЙ СТАТУС:** {user.rank}\n"
        txt += f"⚡ Уровень {user.level} ({user.xp} XP)"
    
    await message.answer(txt, parse_mode="Markdown")
