from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards import progress_kb, main_menu_kb
import database as db
import os

progress_router = Router()

class WeightInput(StatesGroup):
    waiting = State()

@progress_router.message(F.text == "📈 Прогресс")
async def progress_menu(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user: return
    
    txt = f"📊 **ПРОФИЛЬ И СТАТИСТИКА**\n\n"
    txt += f"👤 Имя: **{user.first_name}**\n"
    txt += f"🏆 Ранг: **{user.rank}**\n"
    txt += f"⚡ Уровень: **{user.level}** ({user.xp} XP)\n"
    txt += f"🔥 Стрик: **{user.streak} дней**\n\n"
    txt += f"💪 Завершено тренировок: **{user.workouts_done}**\n"
    txt += f"🎯 Вызовов выполнено: **{user.challenges_done}**\n"
    txt += f"👥 Друзей приглашено: **{user.referrals_count}**\n\n"
    txt += f"⚖️ Текущий вес: **{user.weight} кг** → Цель: **{user.target_weight} кг**"
    
    await message.answer(txt, parse_mode="Markdown", reply_markup=progress_kb())

@progress_router.message(F.text == "Внести вес")
async def input_weight(message: Message, state: FSMContext):
    await message.answer("Введи свой текущий вес в кг (например, 76.4):")
    await state.set_state(WeightInput.waiting)

@progress_router.message(WeightInput.waiting)
async def save_weight(message: Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await state.clear(); await message.answer("Вы вернулись в меню", reply_markup=main_menu_kb()); return
    try:
        w = float(message.text.replace(',', '.'))
        await db.add_weight_log(message.from_user.id, w)
        await db.add_xp(message.from_user.id, 20)
        await state.clear()
        await message.answer(f"✅ Новый вес **{w} кг** записан! +20 XP", parse_mode="Markdown", reply_markup=progress_kb())
    except ValueError:
        await message.answer("Пожалуйста, введи только число.")

@progress_router.message(F.text == "Мой график")
async def show_chart(message: Message):
    logs = await db.get_weight_logs(message.from_user.id)
    if len(logs) < 2:
        await message.answer("Нужно хотя бы 2 записи веса для построения графика. Жми 'Внести вес'!")
        return
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        dates = [l.date.strftime("%d.%m") for l in logs]
        weights = [l.weight for l in logs]
        plt.figure(figsize=(9, 4.5))
        plt.plot(dates, weights, marker='o', color='#FF5722', linewidth=2.5)
        plt.title("Динамика изменения веса", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        path = f"/tmp/chart_{message.from_user.id}.png"
        plt.savefig(path)
        plt.close()
        await message.answer_photo(FSInputFile(path), caption="📈 Твой прогресс веса!")
        os.remove(path)
    except Exception as e:
        await message.answer(f"Ошибка построения графика: {e}")

@progress_router.message(F.text == "История")
async def history(message: Message):
    logs = await db.get_weight_logs(message.from_user.id)
    if not logs:
        await message.answer("История веса пока пуста.")
        return
    txt = "📋 **ИСТОРИЯ ВЗВЕШИВАНИЙ:**\n\n"
    for l in logs[-10:]:
        txt += f"• {l.date.strftime('%d.%m.%Y')} — **{l.weight} кг**\n"
    await message.answer(txt, parse_mode="Markdown")
