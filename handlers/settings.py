from aiogram import Router, F
from aiogram.types import Message
from keyboards import settings_kb
import database as db

settings_router = Router()

@settings_router.message(F.text == "⚙️ Профиль")
async def profile(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user: return
    txt = f"⚙️ **НАСТРОЙКИ И ПРОФИЛЬ**\n\n"
    txt += f"👤 Имя: {user.first_name}\n"
    txt += f"📊 Пол: {user.gender} | Возраст: {user.age}\n"
    txt += f"⚖️ Вес: {user.weight} кг | Рост: {user.height} см\n"
    txt += f"🎯 Цель: {user.goal}\n"
    txt += f"🥗 Диета: {user.diet_type}\n"
    txt += f"🛡 Травмы: {user.injuries}\n"
    txt += f"📍 Место: {user.workout_location}\n\n"
    txt += "Хочешь заново пройти опрос и сбросить параметры? Нажми '🔄 Изменить профиль'"
    await message.answer(txt, parse_mode="Markdown", reply_markup=settings_kb())

@settings_router.message(F.text == "🔄 Изменить профиль")
async def re_register(message: Message):
    await message.answer("Чтобы обновить профиль, отправь команду /start")
