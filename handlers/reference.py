from aiogram import Router, F
from aiogram.types import Message
from keyboards import ref_kb, ref_ex_kb

router = Router()

@router.message(F.text == "📚 База упражнений")
async def ref_main(message: Message):
    await message.answer("📚 <b>База упражнений Repzilla:</b>\nВыберите группу мышц:", parse_mode="HTML", reply_markup=ref_ex_kb())
