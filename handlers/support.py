from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import database as db

support_router = Router()

@support_router.message(F.text == "🎁 Поддержать проект")
async def support_project(message: Message):
    user = await db.get_user(message.from_user.id)
    bot_info = await message.bot.get_me()
    ref_link = f"https://t.me/{bot_info.username}?start={message.from_user.id}"
    
    txt = f"🎁 **ПОДДЕРЖКА И РЕФЕРАЛКА**\n\n"
    txt += f"Привет! Бот создается и поддерживается разработчиком **Богдан К.**\n\n"
    txt += f"Если бот принес тебе пользу, ты можешь поддержать разработки донатом!\n\n"
    txt += f"━━━━━━━━━━━━━━━━━\n"
    txt += f"👥 **Твоя ссылка для друзей:**\n`{ref_link}`\n\n"
    txt += f"За каждого друга ты получишь **+200 XP**!\n"
    txt += f"Уже приведено друзей: **{user.referrals_count if user else 0}**"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Поддержать (Богдан К.)", url="https://www.tbank.ru/cf/8z9T4P7S0nL")],
        [InlineKeyboardButton(text="📤 Отправить другу", url=f"https://t.me/share/url?url={ref_link}&text=Попробуй%20умного%20ИИ-тренера%20Repzilla!")]
    ])
    await message.answer(txt, parse_mode="Markdown", reply_markup=kb)
