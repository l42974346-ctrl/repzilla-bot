from aiogram import Router, F
from aiogram.types import Message
from keyboards import tools_kb
import database as db
import random

tools_router = Router()

CHALLENGES = [
    "🔥 **Челлендж дня:** Сделай 100 отжиманий за сегодня в любых подходах!",
    "⚡ **Челлендж дня:** Простой в планке 3 минуты суммарно за день!",
    "🦵 **Челлендж дня:** 100 приседаний без веса прямо сейчас!",
    "🏃‍♂️ **Челлендж дня:** 50 берпи на время!",
    "💧 **Челлендж дня:** Выпей 3 литра чистой воды за день без отговорок!"
]

@tools_router.message(F.text == "🛠 Инструменты")
async def tools_menu(message: Message):
    await message.answer("Выбери инструмент для фитнес-хакинга:", reply_markup=tools_kb())

@tools_router.message(F.text == "🎯 Бросить Вызов (Челлендж)")
async def challenge(message: Message):
    ch = random.choice(CHALLENGES)
    await db.increment_stat(message.from_user.id, "challenges_done")
    await db.add_xp(message.from_user.id, 30)
    await message.answer(f"{ch}\n\n*Вызов принят! Тебе начислено +30 XP!*", parse_mode="Markdown")

@tools_router.message(F.text == "Калькулятор 1ПМ")
async def calc_1pm(message: Message):
    await message.answer(
        "🧮 **КАЛЬКУЛЯТОР 1ПМ (Одноповторный максимум)**\n\n"
        "Формула Бжицки: `1ПМ = Вес * (36 / (37 - Повторы))`\n\n"
        "**Примеры расчета:**\n"
        "• 60 кг на 10 раз → 1ПМ = **80 кг**\n"
        "• 80 кг на 6 раз → 1ПМ = **95 кг**\n"
        "• 100 кг на 5 раз → 1ПМ = **116 кг**\n\n"
        "Используй 1ПМ для расчета рабочих весов (70-80% от 1ПМ)!", parse_mode="Markdown")

@tools_router.message(F.text == "ИМТ и Идеальный вес")
async def calc_bmi(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user: return
    bmi = user.weight / ((user.height / 100) ** 2)
    ideal = 22 * ((user.height / 100) ** 2)
    
    status = "Норма"
    if bmi < 18.5: status = "Дефицит массы"
    elif bmi > 25: status = "Избыточная масса"
    
    await message.answer(
        f"📊 **ТВОИ ПОКАЗАТЕЛИ МАССЫ ТЕЛА:**\n\n"
        f"• Индекс массы тела (ИМТ): **{bmi:.1f}** ({status})\n"
        f"• Идеальный вес по Броку: ≈ **{ideal:.1f} кг**", parse_mode="Markdown")

@tools_router.message(F.text == "Калькулятор Калорий")
async def calc_calories(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user: return
    await message.answer(f"Твой подробный калькулятор калорий доступен в разделе **'🍎 Питание' → 'Моя КБЖУ норма'**.")

@tools_router.message(F.text == "Калькулятор Креатина")
async def calc_creatine(message: Message):
    user = await db.get_user(message.from_user.id)
    dose = 5 if not user else max(3, int(user.weight * 0.06))
    await message.answer(
        f"💊 **КАЛЬКУЛЯТОР ДОЗИРОВКИ КРЕАТИНА**\n\n"
        f"Твоя оптимальная суточная доза: **{dose} грамм**.\n\n"
        f"💡 Фаза загрузки не обязательна! Просто принимай по {dose}г каждый день в одно время.", parse_mode="Markdown")

@tools_router.message(F.text == "Калькулятор Сна")
async def calc_sleep(message: Message):
    await message.answer(
        "😴 **КАЛЬКУЛЯТОР ЦИКЛОВ СНА (по 90 минут)**\n\n"
        "Чтобы проснуться бодрым, засыпай с учетом полных циклов + 15 мин на засыпание:\n\n"
        "Если вставать в **07:00**:\n"
        "• 22:45 (6 циклов = 9 часов)\n"
        "• 00:15 (5 циклов = 7.5 часов — отлично!)\n"
        "• 01:45 (4 цикла = 6 часов)", parse_mode="Markdown")

@tools_router.message(F.text == "Разминка")
async def warmup(message: Message):
    await message.answer(
        "🤸‍♂️ **УНИВЕРСАЛЬНЫЙ КОМПЛЕКС РАЗМИНКИ (5-7 мин):**\n\n"
        "1. Вращения шеи, плеч, кистей (по 10 раз)\n"
        "2. Махи руками и наклоны корпуса (15 раз)\n"
        "3. Вращения тазом и коленями (10 раз)\n"
        "4. 20 легких приседаний без веса\n"
        "5. 10 отжиманий от пола", parse_mode="Markdown")
