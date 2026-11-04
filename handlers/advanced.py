from aiogram import Router, F
from aiogram.types import Message
from keyboards import advanced_kb
from database import get_user, get_progress

router = Router()

@router.message(F.text == "🛑 Детектор плато")
async def plateau_detector(message: Message):
    text = (
        "🛑 <b>Преодоление застоя (плато) в результатах:</b>\n\n"
        "1. <b>Разгрузочная неделя (Deload):</b> Снизьте вес на 40-50% на 7 дней.\n"
        "2. <b>Изменение диапазона:</b> Перейдите с 8-10 повторов на 3-5 повторов на 2 недели.\n"
        "3. <b>Калорийность:</b> Увеличьте суточный рацион на 200 ккал.\n"
        "4. <b>Замена базовых упражнений:</b> Замените классический жим на жим гантелей."
    )
    await message.answer(text, parse_mode="HTML")

@router.message(F.text == "📅 Недельный отчёт")
async def weekly_report(message: Message):
    user = await get_user(message.from_user.id)
    logs = await get_progress(message.from_user.id)
    
    if not logs:
        weight_str = "Записей веса пока нет (используйте '⚖️ Записать вес')."
    else:
        weight_str = f"Зафиксировано замеров: {len(logs)}. Последний вес: {logs[-1].weight} кг."
        
    text = (
        f"📅 <b>Ваш недельный отчёт Repzilla:</b>\n\n"
        f"🎯 Текущая цель: <b>{user.goal if user else 'Похудение'}</b>\n"
        f"📊 Динамика веса: <b>{weight_str}</b>\n"
        f"⚡️ Очки XP: <b>{user.xp if user else 100}</b>\n"
        f"🏆 Уровень профиля: <b>{user.level if user else 1}</b>\n\n"
        f"<i>Продолжайте регулярные тренировки и отслеживание питания!</i>"
    )
    await message.answer(text, parse_mode="HTML")
