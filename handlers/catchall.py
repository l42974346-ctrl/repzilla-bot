from aiogram import Router
from aiogram.types import Message
from keyboards import main_menu_kb

router = Router()

@router.message()
async def catch_all_handler(message: Message):
    await message.answer(
        "🤖 Я не совсем понял команду. Воспользуйся меню ниже:",
        reply_markup=main_menu_kb()
    )
