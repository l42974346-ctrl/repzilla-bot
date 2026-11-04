from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import database as db
from keyboards import (main_menu_kb, gender_kb, goal_kb, activity_kb, fitness_level_kb, 
                       diet_kb, injuries_kb, location_kb, time_kb)

start_router = Router()

class Onboarding(StatesGroup):
    gender = State()
    age = State()
    weight = State()
    target_weight = State()
    height = State()
    goal = State()
    activity = State()
    fitness_level = State()
    diet = State()
    injuries = State()
    location = State()
    time = State()

@start_router.message(F.text == "🏠 Главное меню")
async def escape_to_main(message: Message, state: FSMContext):
    await state.clear()
    user = await db.get_user(message.from_user.id)
    name = user.first_name if user else "атлет"
    await message.answer(f"Вы вернулись в главное меню, {name}! 💪", reply_markup=main_menu_kb())

@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, command: CommandObject):
    user = await db.get_user(message.from_user.id)
    if user:
        await message.answer(
            f"🔥 **С возвращением, {user.first_name}!**\n\n"
            f"🏆 Ранг: {user.rank}\n"
            f"⚡ Уровень: {user.level} ({user.xp} XP)\n"
            f"🔥 Стрик: {user.streak} дн.\n\n"
            f"Готов продолжить путь к идеал-телу?", 
            reply_markup=main_menu_kb(), parse_mode="Markdown"
        )
    else:
        first_name = message.from_user.first_name or "Атлет"
        await state.update_data(first_name=first_name)
        
        # Обработка реферального приглашения
        ref_by = 0
        if command.args and command.args.isdigit():
            possible_ref = int(command.args)
            if possible_ref != message.from_user.id:
                ref_by = possible_ref
                await state.update_data(referred_by=ref_by)
                # Начисляем рефереру +200 XP
                await db.add_xp(ref_by, 200)
                await db.increment_stat(ref_by, "referrals_count")
        
        await message.answer(
            f"🔥 Привет, **{first_name}**!\n\n"
            f"Я — **Repzilla**, твой персональный фитнес-ИИ нового поколения.\n\n"
            f"🎯 Что я умею:\n"
            f"• Генерирую тренировки под твое тело, травмы и место\n"
            f"• Составляю меню под твои цели с точностью до грамма\n"
            f"• Прокачиваю твой ранг от 🥚 Новичка до 👑 Легенды\n"
            f"• Бросаю вызовы и обучаю спортивной физиологии\n\n"
            f"Ответь на 12 вопросов для подбора программы.\n\n"
            f"**Шаг 1 из 12:** Твой пол?", 
            reply_markup=gender_kb(), parse_mode="Markdown"
        )
        await state.set_state(Onboarding.gender)

async def check_escape(message: Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await escape_to_main(message, state)
        return True
    return False

@start_router.message(Onboarding.gender)
async def process_gender(message: Message, state: FSMContext):
    if await check_escape(message, state): return
    await state.update_data(gender=message.text)
    await message.answer("Сколько тебе полных лет? (напиши число)")
    await state.set_state(Onboarding.age)

@start_router.message(Onboarding.age)
async def process_age(message: Message, state: FSMContext):
    if await check_escape(message, state): return
    if not message.text.isdigit() or not (10 <= int(message.text) <= 90):
        await message.answer("Введи число (например: 25)")
        return
    await state.update_data(age=int(message.text))
    await message.answer("Твой текущий вес (в кг)?")
    await state.set_state(Onboarding.weight)

@start_router.message(Onboarding.weight)
async def process_weight(message: Message, state: FSMContext):
    if await check_escape(message, state): return
    try:
        w = float(message.text.replace(',', '.'))
        await state.update_data(weight=w)
        await message.answer("Твой целевой вес (кг)?")
        await state.set_state(Onboarding.target_weight)
    except ValueError:
        await message.answer("Введи число (например, 78.5)")

@start_router.message(Onboarding.target_weight)
async def process_target_weight(message: Message, state: FSMContext):
    if await check_escape(message, state): return
    try:
        await state.update_data(target_weight=float(message.text.replace(',', '.')))
        await message.answer("Твой рост (см)?")
        await state.set_state(Onboarding.height)
    except ValueError:
        await message.answer("Введи число (например, 180)")

@start_router.message(Onboarding.height)
async def process_height(message: Message, state: FSMContext):
    if await check_escape(message, state): return
    try:
        await state.update_data(height=float(message.text.replace(',', '.')))
        await message.answer("Какая твоя главная цель?", reply_markup=goal_kb())
        await state.set_state(Onboarding.goal)
    except ValueError:
        await message.answer("Введи число.")

@start_router.message(Onboarding.goal)
async def process_goal(message: Message, state: FSMContext):
    if await check_escape(message, state): return
    await state.update_data(goal=message.text)
    await message.answer("Выбери уровень дневной активности:", reply_markup=activity_kb())
    await state.set_state(Onboarding.activity)

@start_router.message(Onboarding.activity)
async def process_activity(message: Message, state: FSMContext):
    if await check_escape(message, state): return
    await state.update_data(activity=message.text)
    await message.answer("Оцени свой уровень подготовки:", reply_markup=fitness_level_kb())
    await state.set_state(Onboarding.fitness_level)

@start_router.message(Onboarding.fitness_level)
async def process_fitness(message: Message, state: FSMContext):
    if await check_escape(message, state): return
    await state.update_data(fitness_level=message.text)
    await message.answer("Какого типа питания ты придерживаешься?", reply_markup=diet_kb())
    await state.set_state(Onboarding.diet)

@start_router.message(Onboarding.diet)
async def process_diet(message: Message, state: FSMContext):
    if await check_escape(message, state): return
    await state.update_data(diet_type=message.text)
    await message.answer("Есть ли у тебя травмы или больные суставы?", reply_markup=injuries_kb())
    await state.set_state(Onboarding.injuries)

@start_router.message(Onboarding.injuries)
async def process_injuries(message: Message, state: FSMContext):
    if await check_escape(message, state): return
    await state.update_data(injuries=message.text)
    await message.answer("Где ты планируешь тренироваться?", reply_markup=location_kb())
    await state.set_state(Onboarding.location)

@start_router.message(Onboarding.location)
async def process_location(message: Message, state: FSMContext):
    if await check_escape(message, state): return
    await state.update_data(workout_location=message.text)
    await message.answer("Сколько времени готов выделять на 1 тренировку?", reply_markup=time_kb())
    await state.set_state(Onboarding.time)

@start_router.message(Onboarding.time)
async def process_time(message: Message, state: FSMContext):
    if await check_escape(message, state): return
    data = await state.get_data()
    data['telegram_id'] = message.from_user.id
    data['username'] = message.from_user.username or "atlet"
    data['time_per_workout'] = message.text
    
    await db.create_or_update_user(data)
    await state.clear()
    
    await message.answer(
        f"🧠 **ПРОФИЛЬ УСПЕШНО СФОРМИРОВАН!**\n\n"
        f"✅ Твои травмы ({data.get('injuries')}) приняты во внимание.\n"
        f"✅ План адаптирован под место: {data.get('workout_location')}.\n"
        f"✅ Учтен тип питания: {data.get('diet_type')}.\n\n"
        f"🎁 **Приветственный бонус:** +100 XP\n\n"
        f"Жми '💪 Тренировка' → '🤖 СГЕНЕРИРОВАТЬ УМНУЮ ТРЕНИРОВКУ'!",
        parse_mode="Markdown", reply_markup=main_menu_kb()
    )
    await db.add_xp(message.from_user.id, 100)
