from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

support_router = Router()

@support_router.message(F.text == "🎁 Поддержать проект")
async def support_project(message: Message):
    txt = (
        "🎁 **ПОДДЕРЖКА ПРОЕКТА REPZILLA**\n\n"
        "Привет! Я единственный создатель бота👋\n\n"
        "Repzilla — это полностью бесплатный проект, который я развиваю на собственном энтузиазме. "
        "Я постоянно дорабатываю алгоритмы, расширяю базу знаний и добавляю новые фишки, чтобы у тебя был "
        "лучший персональный фитнес-помощник.\n\n"
        "Если бот приносит тебе пользу, помогает тренироваться или следить за питанием, ты можешь "
        "поддержать проект любой суммой. Это дает огромную мотивацию и ресурсы развивать Repzilla дальше!\n\n"
        "Огромное спасибо каждому за поддержку! 💪🔥"
    )
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Поддержать копеечкой", url="https://www.tbank-online.com/rm/r_QULlbQJdfc.TzDCxOjSOy/CmfNt95465")]
    ])
    
    await message.answer(txt, parse_mode="Markdown", reply_markup=kb)
