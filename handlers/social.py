import random
from aiogram import Router, F
from aiogram.types import Message
from keyboards import social_kb

router = Router()

@router.message(F.text == "🎮 Соцсети/Игры")
async def social_main(message: Message):
    await message.answer("🎮 <b>Геймификация и фитнес-игры Repzilla:</b>", parse_mode="HTML", reply_markup=social_kb())

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
    await message.answer(f"🎰 <b>Рулетка выбила вам задание на сегодня:</b>\n\n{res}\n\nПриступайте прямо сейчас! 💪", parse_mode="HTML")

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

@router.message(F.text == "🏆 Лидерборд")
async def leaderboard(message: Message):
    await message.answer(
        "🏆 <b>Топ атлетов Repzilla в лиге:</b>\n\n"
        "1. 🥇 Алекс — 1450 XP (Легенда)\n"
        "2. 🥈 Дмитрий — 1120 XP (Мастер)\n"
        "3. 🥉 Богдан — 950 XP (Атлет)\n"
        "4. 🎗 Иван — 820 XP (Любитель)\n"
        "5. 🎗 Сергей — 610 XP (Новичок)",
        parse_mode="HTML"
    )

@router.message(F.text == "🎯 Мой профиль / XP")
async def profile_xp(message: Message):
    await message.answer(
        "🎯 <b>Ваш фитнес-профиль:</b>\n\n"
        "• 🏅 Уровень: <b>2 (Продвинутый)</b>\n"
        "• ⚡️ Накоплено XP: <b>350 / 500</b>\n"
        "• 🔥 Серия дней в боте: <b>3 дня подряд</b>\n"
        "• 📜 Ранг: <b>Атлет Repzilla</b>",
        parse_mode="HTML"
    )

@router.message(F.text == "🔗 Реферальная ссылка")
async def ref_link(message: Message):
    link = f"https://t.me/repzilla_bot?start={message.from_user.id}"
    await message.answer(
        f"🔗 <b>Ваша реферальная ссылка:</b>\n<code>{link}</code>\n\n"
        f"Приглашайте друзей! За каждого зарегистрированного друга вы получаете <b>+200 XP</b>.",
        parse_mode="HTML"
    )
