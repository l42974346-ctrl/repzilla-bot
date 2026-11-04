import random
from aiogram import Router, F
from aiogram.types import Message
from keyboards import fun_kb

router = Router()

@router.message(F.text == "🎰 Рулетка тренировки")
async def workout_roulette(message: Message):
    exercises = [
        "🔥 50 отжиманий за минимальное время!",
        "🔥 Планочный марафон: 3 подхода по 1.5 минуты!",
        "🔥 100 приседаний без перерыва!",
        "🔥 40 берпи на максимум выносливости!",
        "🔥 50 скручиваний на пресс + 1 минута вакуума!"
    ]
    res = random.choice(exercises)
    await message.answer(f"🎰 <b>Рулетка выбила задание на сегодня:</b>\n\n{res}\n\nПриступайте прямо сейчас! 💪", parse_mode="HTML")

@router.message(F.text == "😴 Калькулятор сна")
async def fun_sleep(message: Message):
    await message.answer("😴 <b>Калькулятор сна:</b> Доступен в разделе 🛠 Инструменты!", parse_mode="HTML")

@router.message(F.text == "📐 Идеальный вес")
async def ideal_weight(message: Message):
    text = (
        "📐 <b>Расчёт идеального веса (по формуле Лоренца):</b>\n\n"
        "• <b>Мужчины:</b> (Рост - 100) - (Рост - 150) / 4\n"
        "• <b>Женщины:</b> (Рост - 100) - (Рост - 150) / 2.5\n\n"
        "<i>При росте 180 см идеальный вес составляет около 72.5 кг.</i>"
    )
    await message.answer(text, parse_mode="HTML")

@router.message(F.text == "🔥 Челлендж дня")
async def daily_challenge(message: Message):
    challenges = [
        "💧 Выпить 2.5 литра чистой воды за день.",
        "🚶 Пройти не менее 10,000 шагов.",
        "😴 Лягте спать до 23:00.",
        "🥗 Полностью отказаться от сахара и фастфуда сегодня."
    ]
    res = random.choice(challenges)
    await message.answer(f"🔥 <b>Ваш челлендж на сегодня:</b>\n\n{res}", parse_mode="HTML")
