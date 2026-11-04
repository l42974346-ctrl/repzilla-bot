from aiogram import Router, F
from aiogram.types import Message
from keyboards import workout_kb, gym_programs_kb, home_programs_kb
import database as db
import random
import asyncio

workout_router = Router()

EXERCISES_POOL = [
    {"name": "Приседания со штангой", "loc": ["Тренажерный зал"], "danger": ["Колени/Суставы", "Спина/Поясница"]},
    {"name": "Жим лежа на горизонтальной скамье", "loc": ["Тренажерный зал"], "danger": ["Плечи/Шея"]},
    {"name": "Становая тяга классическая", "loc": ["Тренажерный зал"], "danger": ["Спина/Поясница"]},
    {"name": "Подтягивания широким хватом", "loc": ["Тренажерный зал", "Улица/Воркаут"], "danger": ["Плечи/Шея"]},
    {"name": "Отжимания от пола", "loc": ["Дома (без инвентаря)", "Улица/Воркаут", "Тренажерный зал"], "danger": []},
    {"name": "Выпады с гантелями в шаге", "loc": ["Тренажерный зал"], "danger": ["Колени/Суставы"]},
    {"name": "Жим гантелей сидя вверх", "loc": ["Тренажерный зал"], "danger": ["Плечи/Шея", "Спина/Поясница"]},
    {"name": "Скручивания на пресс", "loc": ["Дома (без инвентаря)", "Тренажерный зал", "Улица/Воркаут"], "danger": ["Спина/Поясница"]},
    {"name": "Тяга штанги в наклоне", "loc": ["Тренажерный зал"], "danger": ["Спина/Поясница"]},
    {"name": "Болгарские сплит-приседания", "loc": ["Тренажерный зал", "Дома (без инвентаря)"], "danger": ["Колени/Суставы"]},
    {"name": "Махи гантелями через стороны", "loc": ["Тренажерный зал"], "danger": []},
    {"name": "Берпи", "loc": ["Дома (без инвентаря)", "Тренажерный зал", "Улица/Воркаут"], "danger": ["Колени/Суставы"]},
    {"name": "Планка классическая", "loc": ["Дома (без инвентаря)", "Тренажерный зал", "Улица/Воркаут"], "danger": []},
    {"name": "Ягодичный мостик со штангой/весом", "loc": ["Дома (без инвентаря)", "Тренажерный зал"], "danger": []},
    {"name": "Отжимания на брусьях", "loc": ["Тренажерный зал", "Улица/Воркаут"], "danger": ["Плечи/Шея"]},
    {"name": "Гиперэкстензия", "loc": ["Тренажерный зал"], "danger": []}
]

@workout_router.message(F.text == "💪 Тренировка")
async def workout_menu(message: Message):
    await message.answer("Выбери режим тренировки:", reply_markup=workout_kb())

@workout_router.message(F.text == "🤖 СГЕНЕРИРОВАТЬ УМНУЮ ТРЕНИРОВКУ")
async def generate_smart_workout(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user:
        await message.answer("Пройди /start"); return

    msg = await message.answer("🤖 *Анализирую параметры твоей медицинской анкеты...*", parse_mode="Markdown")
    await asyncio.sleep(0.7)
    await msg.edit_text(f"🤖 *Исключаю нагрузки с риском для: {user.injuries}...*", parse_mode="Markdown")
    await asyncio.sleep(0.7)

    filtered = []
    for ex in EXERCISES_POOL:
        if user.injuries in ex["danger"]:
            continue
        filtered.append(ex)

    ex_count = 5
    if "30" in user.time_per_workout: ex_count = 4
    if "Долго" in user.time_per_workout: ex_count = 7

    selected = random.sample(filtered, min(ex_count, len(filtered)))

    plan = f"🔥 **ПЕРСОНАЛЬНАЯ УМНАЯ ТРЕНИРОВКА** 🔥\n\n"
    plan += f"👤 Атлет: **{user.first_name}**\n"
    plan += f"📍 Локация: **{user.workout_location}**\n"
    plan += f"⏱ Время: **{user.time_per_workout}**\n"
    plan += f"🛡 Безопасно для: **{user.injuries}**\n\n"
    plan += f"━━━━━━━━━━━━━━━━━━━━━\n"

    for i, ex in enumerate(selected, 1):
        sets = random.choice(["3 подхода x 12 повторений", "4 подхода x 10 повторений", "3 подхода x 15 повторений"])
        plan += f"{i}. **{ex['name']}**\n   └ {sets}\n"

    plan += f"━━━━━━━━━━━━━━━━━━━━━\n"
    plan += "\n💡 *После окончания не забудь занести вес в разделе '📈 Прогресс'!*"

    await db.increment_stat(message.from_user.id, "workouts_done")
    await db.add_xp(message.from_user.id, 35)
    await msg.edit_text(plan, parse_mode="Markdown")

@workout_router.message(F.text == "Программы для Зала")
async def gym_progs(message: Message):
    await message.answer("Выбери специализированную программу для зала:", reply_markup=gym_programs_kb())

@workout_router.message(F.text == "Full Body (3 дня)")
async def full_body_plan(message: Message):
    txt = """💪 **ПРОГРАММА FULL BODY (3 дня в неделю)**

**День 1 (Понедельник):**
1. Приседания со штангой — 3х8-10
2. Жим лежа — 3х8-10
3. Тяга блока к груди — 3х10-12
4. Жим гантелей сидя — 3х12
5. Скручивания — 3х15

**День 2 (Среда):**
1. Румынская тяга — 3х10
2. Отжимания на брусьях / Жим гантелей на инклине — 3х10
3. Подтягивания — 3хMAX
4. Махи гантелями — 3х15
5. Планка — 3х60 сек

**День 3 (Пятница):**
1. Жим ногами — 3х12
2. Тяга штанги в наклоне — 3х8-10
3. Жим лежа узким хватом — 3х10
4. Сгибание рук со штангой на бицепс — 3х12
5. Подъем ног в висе — 3х12"""
    await message.answer(txt, parse_mode="Markdown")

@workout_router.message(F.text == "Сплит Тяни-Толкай (6 дней)")
async def ppl_plan(message: Message):
    txt = """🔥 **ПРОГРАММА PUSH / PULL / LEGS (6 дней)**

**Push (Толкай):** Жим лежа 4х8, Жим гантелей под углом 3х10, Жим стоя 3х10, Брусья 3х12, Французский жим 3х12.
**Pull (Тяни):** Подтягивания 4х8, Тяга гантели в наклоне 3х10, Махи задняя дельта 3х15, Бицепс со штангой 3х10.
**Legs (Ноги):** Приседания 4х8, Румынская тяга 3х10, Выпады 3х12, Икры 4х15."""
    await message.answer(txt, parse_mode="Markdown")

@workout_router.message(F.text == "Верх/Низ (4 дня)")
async def upper_lower_plan(message: Message):
    txt = """⚡ **ПРОГРАММА ВЕРХ / НИЗ (4 дня)**

Понедельник — Верх (Силовой)
Вторник — Низ (Силовой)
Четверг — Верх (Гипертрофия)
Пятница — Низ (Гипертрофия)"""
    await message.answer(txt, parse_mode="Markdown")

@workout_router.message(F.text == "Мужская: Масса")
async def male_mass_plan(message: Message):
    txt = """🏋️‍♂️ **МУЖСКОЙ МАССА-НАБОР (Тяжелая база)**

Фокус на больших весах, 6-8 повторений, отдых 2.5 минуты между подходами. Базовый рост гарантирован!"""
    await message.answer(txt, parse_mode="Markdown")

@workout_router.message(F.text == "Женская: Ягодицы и Тонус")
async def female_plan(message: Message):
    txt = """🍑 **ЖЕНСКАЯ ПРОГРАММА: ЯГОДИЦЫ И ТОНУС**

1. Ягодичный мостик со штангой — 4х12
2. Болгарские сплит-приседания — 3х12
3. Румынская тяга с гантелями — 4х10
4. Отведение ноги в кроссовере — 3х15
5. Пресс / Гиперэкстензия — 3х15"""
    await message.answer(txt, parse_mode="Markdown")

@workout_router.message(F.text == "Программы для Дома")
async def home_progs(message: Message):
    await message.answer("Выбери домашнюю программу:", reply_markup=home_programs_kb())

@workout_router.message(F.text == "Новичок (без инвентаря)")
async def home_novice(message: Message):
    txt = """🏠 **ДОМАШНЯЯ ПРОГРАММА (Собственный вес)**

1. Отжимания от пола (или с колен) — 3х12
2. Приседания без веса — 3х20
3. Выпады назад — 3х12 на ногу
4. Лодочка на спину — 3х15
5. Планка — 3х45 сек"""
    await message.answer(txt, parse_mode="Markdown")

@workout_router.message(F.text == "С гантелями")
async def home_dumbbells(message: Message):
    txt = """🏋️‍♀️ **ДОМА С ГАНТЕЛЯМИ**

1. Жим гантелей лежа на полу — 3х12
2. Приседания с гантелью у груди (Гоблет) — 3х15
3. Тяга гантелей к поясу в наклоне — 3х12
4. Жим гантелей стоя — 3х12
5. Сгибание на бицепс + Разгибание на трицепс — 3х15"""
    await message.answer(txt, parse_mode="Markdown")

@workout_router.message(F.text == "HIIT Жиросжигание")
async def home_hiit(message: Message):
    txt = """🔥 **HIIT ИНТЕРВАЛЬНАЯ ТРЕНИРОВКА (40 сек работа / 20 сек отдых)**

1. Берпи
2. Джампинг Джек (Прыжки)
3. Скалолаз (Mountain Climbers)
4. Приседания с прыжком
5. Планка с касанием плеч
*Сделай 4 круга!*"""
    await message.answer(txt, parse_mode="Markdown")

@workout_router.message(F.text == "Растяжка / Мобильность")
async def home_stretch(message: Message):
    txt = """🧘‍♂️ **РАСТЯЖКА И МОБИЛЬНОСТЬ СУСТАВОВ**

1. Собака мордой вниз / вверх — 1 мин
2. Поза голубя (растяжка ягодичных) — 1 мин на сторону
3. Растяжка бицепса бедра сидя — 1 мин
4. Раскрытие грудного отдела ("Кошка-Корова") — 15 повторов"""
    await message.answer(txt, parse_mode="Markdown")

@workout_router.message(F.text == "🎲 Рулетка упражнений")
async def roulette(message: Message):
    ex = random.choice(EXERCISES_POOL)["name"]
    await db.add_xp(message.from_user.id, 10)
    await message.answer(f"🎲 Выпало: **{ex}**\nСделай 20 повторов прямо сейчас! (+10 XP)", parse_mode="Markdown")

@workout_router.message(F.text == "⏱ Таймер отдыха")
async def rest_timer(message: Message):
    await message.answer("⏱ **Рекомендации по отдыху:**\n\n• Тяжелые упражнения (Присед, Жим, Тяга): **2-3 минуты**\n• Изолирующие упражнения: **60-90 секунд**\n• Пресс и икры: **45-60 секунд**")
