from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💪 Тренировка"), KeyboardButton(text="🍎 Питание")],
            [KeyboardButton(text="📈 Прогресс"), KeyboardButton(text="📚 База Знаний")],
            [KeyboardButton(text="🛠 Инструменты"), KeyboardButton(text="⚙️ Профиль")],
            [KeyboardButton(text="🎯 Совет дня"), KeyboardButton(text="🏆 Лидерборд")],
            [KeyboardButton(text="🎁 Поддержать проект")]
        ], resize_keyboard=True
    )

def gender_kb(): return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Мужской"), KeyboardButton(text="Женский")]], resize_keyboard=True)
def goal_kb(): return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Похудение"), KeyboardButton(text="Набор массы"), KeyboardButton(text="Поддержание")]], resize_keyboard=True)
def activity_kb(): return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Минимум (сидячая)"), KeyboardButton(text="Слабая (1-3 дня)")], [KeyboardButton(text="Средняя (3-5 дней)"), KeyboardButton(text="Высокая (6-7 дней)")], [KeyboardButton(text="Экстрим (тяжелая работа)")]], resize_keyboard=True)
def fitness_level_kb(): return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Новичок"), KeyboardButton(text="Средний"), KeyboardButton(text="Профи")]], resize_keyboard=True)
def diet_kb(): return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Обычное"), KeyboardButton(text="Вегетарианское")], [KeyboardButton(text="Веганское"), KeyboardButton(text="Кето")]], resize_keyboard=True)
def injuries_kb(): return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Нет травм")], [KeyboardButton(text="Спина/Поясница"), KeyboardButton(text="Колени/Суставы")], [KeyboardButton(text="Плечи/Шея")]], resize_keyboard=True)
def location_kb(): return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Тренажерный зал"), KeyboardButton(text="Дома (без инвентаря)")], [KeyboardButton(text="Улица/Воркаут")]], resize_keyboard=True)
def time_kb(): return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Быстро (30 мин)"), KeyboardButton(text="Оптимально (45-60 мин)")], [KeyboardButton(text="Долго (более 1 часа)")]], resize_keyboard=True)

def workout_kb(): return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🤖 СГЕНЕРИРОВАТЬ УМНУЮ ТРЕНИРОВКУ")], [KeyboardButton(text="Программы для Зала"), KeyboardButton(text="Программы для Дома")], [KeyboardButton(text="🎲 Рулетка упражнений"), KeyboardButton(text="⏱ Таймер отдыха")], [KeyboardButton(text="🏠 Главное меню")]], resize_keyboard=True)
def gym_programs_kb(): return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Full Body (3 дня)"), KeyboardButton(text="Сплит Тяни-Толкай (6 дней)")], [KeyboardButton(text="Верх/Низ (4 дня)"), KeyboardButton(text="Мужская: Масса")], [KeyboardButton(text="Женская: Ягодицы и Тонус"), KeyboardButton(text="🏠 Главное меню")]], resize_keyboard=True)
def home_programs_kb(): return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Новичок (без инвентаря)"), KeyboardButton(text="С гантелями")], [KeyboardButton(text="HIIT Жиросжигание"), KeyboardButton(text="Растяжка / Мобильность")], [KeyboardButton(text="🏠 Главное меню")]], resize_keyboard=True)

def nutrition_kb(): return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🤖 УМНЫЙ ПЛАН ПИТАНИЯ")], [KeyboardButton(text="Моя КБЖУ норма"), KeyboardButton(text="База продуктов")], [KeyboardButton(text="ПП Рецепты"), KeyboardButton(text="💧 Трекер воды")], [KeyboardButton(text="🏠 Главное меню")]], resize_keyboard=True)
def water_kb(): return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🥤 +250 мл воды"), KeyboardButton(text="🔄 Сбросить воду")], [KeyboardButton(text="🏠 Главное меню")]], resize_keyboard=True)

def progress_kb(): return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Внести вес"), KeyboardButton(text="Мой график")], [KeyboardButton(text="История"), KeyboardButton(text="🏠 Главное меню")]], resize_keyboard=True)
def tools_kb(): return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🎯 Бросить Вызов (Челлендж)")], [KeyboardButton(text="Калькулятор 1ПМ"), KeyboardButton(text="ИМТ и Идеальный вес")], [KeyboardButton(text="Калькулятор Калорий"), KeyboardButton(text="Калькулятор Креатина")], [KeyboardButton(text="Калькулятор Сна"), KeyboardButton(text="Разминка")], [KeyboardButton(text="🏠 Главное меню")]], resize_keyboard=True)
def assistant_kb(): return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🧬 Гормоны и Физиология"), KeyboardButton(text="🔬 Биомеханика")], [KeyboardButton(text="🚫 Мифы о фитнесе"), KeyboardButton(text="💊 Спортивное питание")], [KeyboardButton(text="Техника упражнений"), KeyboardButton(text="Сон и восстановление")], [KeyboardButton(text="Психология и мотивация"), KeyboardButton(text="Профилактика травм")], [KeyboardButton(text="Плато"), KeyboardButton(text="Цитаты легенд")], [KeyboardButton(text="🏠 Главное меню")]], resize_keyboard=True)
def settings_kb(): return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🔄 Изменить профиль"), KeyboardButton(text="🏠 Главное меню")]], resize_keyboard=True)
def support_kb(): return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🏠 Главное меню")]], resize_keyboard=True)

# Алиасы для старого кода
nutrition_menu_kb = nutrition_kb
meas_kb = progress_kb
tools_menu_kb = tools_kb
knowledge_kb = assistant_kb
