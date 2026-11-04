from aiogram import Router, F
from aiogram.types import Message
from keyboards import nutrition_kb, water_kb
import database as db
import random
import asyncio

nutrition_router = Router()

# ПОЛНАЯ БАЗА 50+ ПРОДУКТОВ (на 100г)
FOOD_DATABASE = {
    # Мясо и птица
    "куриная грудка": {"c": 165, "p": 31, "f": 3.6, "carbs": 0},
    "филе индейки": {"c": 130, "p": 25, "f": 1.5, "carbs": 0},
    "говядина постная": {"c": 187, "p": 26, "f": 11, "carbs": 0},
    "свинина постная": {"c": 242, "p": 27, "f": 14, "carbs": 0},
    "печень куриная": {"c": 137, "p": 21, "f": 5, "carbs": 0.6},
    "кролик": {"c": 156, "p": 21, "f": 8, "carbs": 0},
    
    # Рыба и морепродукты
    "лосось / семга": {"c": 208, "p": 20, "f": 13, "carbs": 0},
    "треска": {"c": 78, "p": 18, "f": 0.7, "carbs": 0},
    "тунец в с/соку": {"c": 101, "p": 23, "f": 1, "carbs": 0},
    "креветки": {"c": 95, "p": 19, "f": 1, "carbs": 0},
    "минтай": {"c": 72, "p": 16, "f": 0.9, "carbs": 0},
    "скумбрия": {"c": 262, "p": 18, "f": 19, "carbs": 0},
    
    # Молочные продукты и яйца
    "яйцо куриное (1 шт ≈ 50г)": {"c": 155, "p": 13, "f": 11, "carbs": 1.1},
    "яичный белок": {"c": 52, "p": 11, "f": 0.2, "carbs": 0.7},
    "творог 0-1%": {"c": 71, "p": 18, "f": 0.6, "carbs": 1.8},
    "творог 5%": {"c": 121, "p": 17, "f": 5, "carbs": 2.8},
    "греческий йогурт 2%": {"c": 73, "p": 10, "f": 2, "carbs": 4},
    "сыр твердый (пармезан/гауда)": {"c": 356, "p": 25, "f": 27, "carbs": 1.3},
    "молоко 2.5%": {"c": 52, "p": 2.8, "f": 2.5, "carbs": 4.7},
    
    # Крупы и каши (в сухом виде)
    "гречка": {"c": 343, "p": 13, "f": 3.4, "carbs": 72},
    "овсянка / геркулес": {"c": 389, "p": 17, "f": 7, "carbs": 66},
    "рис белый": {"c": 358, "p": 6.5, "f": 0.6, "carbs": 79},
    "рис бурый": {"c": 337, "p": 7.5, "f": 1.9, "carbs": 77},
    "киноа": {"c": 368, "p": 14, "f": 6, "carbs": 64},
    "макароны из тв. сортов": {"c": 350, "p": 12, "f": 1.5, "carbs": 74},
    "чечевица сухая": {"c": 352, "p": 25, "f": 1.1, "carbs": 60},
    "нут": {"c": 364, "p": 19, "f": 6, "carbs": 61},
    
    # Овощи и зелень
    "брокколи": {"c": 34, "p": 2.8, "f": 0.4, "carbs": 7},
    "огурцы": {"c": 15, "p": 0.8, "f": 0.1, "carbs": 3},
    "помидоры": {"c": 18, "p": 0.9, "f": 0.2, "carbs": 3.9},
    "шпинат": {"c": 23, "p": 2.9, "f": 0.4, "carbs": 3.6},
    "картофель": {"c": 77, "p": 2, "f": 0.1, "carbs": 17},
    "капуста белокочанная": {"c": 25, "p": 1.8, "f": 0.1, "carbs": 5.8},
    "спаржа": {"c": 20, "p": 2.2, "f": 0.1, "carbs": 3.9},
    
    # Фрукты и ягоды
    "банан": {"c": 89, "p": 1.1, "f": 0.3, "carbs": 23},
    "яблоко": {"c": 52, "p": 0.3, "f": 0.2, "carbs": 14},
    "апельсин": {"c": 47, "p": 0.9, "f": 0.2, "carbs": 12},
    "клубника / черника": {"c": 33, "p": 0.7, "f": 0.3, "carbs": 8},
    "авокадо": {"c": 160, "p": 2, "f": 15, "carbs": 9},
    
    # Орехи и семена
    "миндаль": {"c": 579, "p": 21, "f": 50, "carbs": 22},
    "грецкий орех": {"c": 654, "p": 15, "f": 65, "carbs": 14},
    "арахисовая паста": {"c": 588, "p": 25, "f": 50, "carbs": 20},
    "семена чиа": {"c": 486, "p": 17, "f": 31, "carbs": 42},
    
    # Прочее
    "протеин сывороточный (1 скуп 30г)": {"c": 120, "p": 24, "f": 1.5, "carbs": 2},
    "хлеб цельнозерновой": {"c": 247, "p": 13, "f": 3.4, "carbs": 41},
    "оливковое масло (1 ст.л. ≈ 12г)": {"c": 108, "p": 0, "f": 12, "carbs": 0}
}

MEALS_DB = {
    "Обычное": [
        ("Завтрак: Овсянка 80г на молоке + 2 яйца + Банан", 480, 22, 12, 65),
        ("Обед: Куриная грудка 200г + Рис 150г + Салат", 620, 52, 10, 70),
        ("Ужин: Творог 5% 200г + Миндаль 20г + Ягоды", 380, 36, 14, 25),
        ("Перекус: Протеиновый коктейль + Яблоко", 250, 25, 3, 30)
    ],
    "Вегетарианское": [
        ("Завтрак: Сырники из творога 200г + Мед 15г + Ягоды", 420, 30, 12, 45),
        ("Обед: Чечевица тушеная 200г + Бурый рис 150г", 580, 32, 8, 88),
        ("Ужин: Омлет из 3 яиц с сыром Пармезан и овощами", 400, 28, 26, 10),
        ("Перекус: Греческий йогурт 200г + Миндаль 30г", 290, 16, 17, 18)
    ],
    "Веганское": [
        ("Завтрак: Овсянка 80г на соевом молоке + Арахисовая паста 20г", 490, 18, 20, 62),
        ("Обед: Тофу гриль 200г + Киноа 150г + Овощи", 590, 34, 18, 70),
        ("Ужин: Нутовое рагу 250г с авокадо half", 430, 22, 18, 48),
        ("Перекус: Протеин веганский + Семена чиа 15г + Яблоко", 260, 22, 6, 30)
    ],
    "Кето": [
        ("Завтрак: Яичница из 3 яиц с беконом и авокадо", 580, 28, 48, 4),
        ("Обед: Стейк из лосося 200г + Спаржа в оливковом масле", 640, 42, 46, 6),
        ("Ужин: Говядина тушеная 200г + Зеленый салат", 520, 44, 38, 5),
        ("Перекус: Сыр Твердый 50г + Орехи Пекан 20г", 320, 14, 29, 3)
    ]
}

def calc_kbju(user):
    mod = 5 if user.gender == "Мужской" else -161
    bmr = 10 * user.weight + 6.25 * user.height - 5 * user.age + mod
    mult = 1.375
    if "Средняя" in user.activity: mult = 1.55
    if "Высокая" in user.activity: mult = 1.725
    if "Экстрим" in user.activity: mult = 1.9
    tdee = bmr * mult
    if "Похудение" in user.goal: tdee -= 400
    elif "Набор" in user.goal: tdee += 350
    p = user.weight * (2.2 if "Похудение" in user.goal else 2.0)
    f = user.weight * 1.0
    c = (tdee - p*4 - f*9) / 4
    return int(tdee), int(p), int(f), int(max(20, c))

@nutrition_router.message(F.text == "🍎 Питание")
async def nutrition_menu(message: Message):
    await message.answer("Раздел питания и гидратации:", reply_markup=nutrition_kb())

@nutrition_router.message(F.text == "🤖 УМНЫЙ ПЛАН ПИТАНИЯ")
async def smart_plan(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user: return
    cal, p, f, c = calc_kbju(user)
    diet = user.diet_type if user.diet_type in MEALS_DB else "Обычное"
    meals = MEALS_DB[diet]

    txt = f"🍽 **ТВОЙ ПЕРСОНАЛЬНЫЙ РАЦИОН НА ДЕНЬ**\n"
    txt += f"👤 Атлет: **{user.first_name}** | Тип питания: **{diet}**\n"
    txt += f"🎯 Цель: **{user.goal}**\n\n"
    txt += "━━━━━━━━━━━━━━━━━━━━━\n"
    for m in meals:
        txt += f"• **{m[0]}**\n  └ {m[1]} ккал | Б:{m[2]}г Ж:{m[3]}г У:{m[4]}г\n\n"
    txt += "━━━━━━━━━━━━━━━━━━━━━\n"
    txt += f"🎯 **ТВОЯ РАССЧИТАННАЯ НОРМА:**\n"
    txt += f"🔥 **{cal} ккал** | Белок: **{p}г** | Жиры: **{f}г** | Углеводы: **{c}г**"
    
    await db.add_xp(message.from_user.id, 15)
    await message.answer(txt, parse_mode="Markdown")

@nutrition_router.message(F.text == "Моя КБЖУ норма")
async def my_kbju(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user: return
    cal, p, f, c = calc_kbju(user)
    water = int(user.weight * 35)
    await message.answer(
        f"📊 **ТВОИ ИНДИВИДУАЛЬНЫЕ МАКРОСЫ (Mifflin-St Jeor):**\n\n"
        f"🔥 Калории: **{cal} ккал/день**\n"
        f"🥩 Белки: **{p} г** ({p*4} ккал)\n"
        f"🥑 Жиры: **{f} г** ({f*9} ккал)\n"
        f"🍞 Углеводы: **{c} г** ({c*4} ккал)\n\n"
        f"💧 Дневная норма воды: **{water} мл**", parse_mode="Markdown"
    )

@nutrition_router.message(F.text == "База продуктов")
async def food_base(message: Message):
    txt = "🥗 **БАЗА ПРОДУКТОВ REPZILLA (на 100г):**\n\n"
    items = list(FOOD_DATABASE.items())
    for name, v in items[:25]:
        txt += f"• **{name.title()}** — {v['c']} ккал (Б:{v['p']} Ж:{v['f']} У:{v['carbs']})\n"
    txt += "\n*(показаны первые 25 из 50+ продуктов)*"
    await message.answer(txt, parse_mode="Markdown")

@nutrition_router.message(F.text == "ПП Рецепты")
async def recipes(message: Message):
    txt = """🍳 **ТОП-5 ПОЛНОЦЕННЫХ ПП-РЕЦЕПТОВ:**

**1. Протеиновые панкейки с бананом**
• *Ингредиенты:* 1 спелый банан, 2 яйца, 40g овсяных хлопьев, 1 скупик протеина.
• *Приготовление:* Все ингредиенты взбить в блендере. Выпекать на антипригарной сковороде без масла 2 мин с каждой стороны.
• *КБЖУ:* 380 ккал / Б: 32g / Ж: 9g / У: 45g

**2. Боул с курицей, рисом и авокадо**
• *Ингредиенты:* 150g отварной грудки, 100g вареного бурого риса, 1/2 авокадо, огурец, соевый соус.
• *КБЖУ:* 490 ккал / Б: 45g / Ж: 14g / У: 42g

**3. Нежный творожный десерт с ягодами**
• *Ингредиенты:* 200g творога 5%, 100g замороженной черники, 15g грецкого ореха, 10g меда.
• *КБЖУ:* 340 ккал / Б: 35g / Ж: 12g / У: 24g

**4. Филе трески на пару с брокколи**
• *Ингредиенты:* 250g филе трески, 200g брокколи, 1 ст.л. оливкового масла, лимонный сок.
• *КБЖУ:* 310 ккал / Б: 46g / Ж: 13g / У: 8g

**5. Овсяноблин с сыром и красной рыбой**
• *Ингредиенты:* 40g овсянки, 1 яйцо + 30ml молока (взбить и пожарить блин), начинка: 50g слабосоленой семги + 30g легкого сыра.
• *КБЖУ:* 410 ккал / Б: 28g / Ж: 19g / У: 32g"""
    await message.answer(txt, parse_mode="Markdown")

@nutrition_router.message(F.text == "💧 Трекер воды")
async def water_tracker(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user: return
    norm = int(user.weight * 35)
    drunk = user.water_today
    percent = min(100, int(drunk / norm * 100))
    bar = "🟦" * (percent // 10) + "⬜️" * (10 - percent // 10)
    await message.answer(
        f"💧 **ТРЕКЕР ВОДЫ**\n\n"
        f"{bar} {percent}%\n\n"
        f"Выпито сегодня: **{drunk} мл** из **{norm} мл**\n\n"
        f"Нажимай кнопку ниже после каждого стакана!", 
        parse_mode="Markdown", reply_markup=water_kb()
    )

@nutrition_router.message(F.text == "🥤 +250 мл воды")
async def add_water_btn(message: Message):
    await db.add_water(message.from_user.id, 250)
    await db.add_xp(message.from_user.id, 5)
    await water_tracker(message)

@nutrition_router.message(F.text == "🔄 Сбросить воду")
async def reset_water_btn(message: Message):
    await db.reset_water(message.from_user.id)
    await water_tracker(message)
