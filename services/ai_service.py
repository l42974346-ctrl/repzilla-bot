from openai import AsyncOpenAI
from config import GROQ_API_KEY, AI_MODEL
import asyncio

client = AsyncOpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")

SYSTEM = "Ты FitBot — фитнес-тренер. Отвечай кратко на русском с эмодзи. Не давай мед. диагнозов."

async def get_ai_response(messages, profile=None):
    try:
        sys = SYSTEM
        if profile:
            p = ""
            if profile.get("gender"): p += f"Пол:{'м' if profile['gender']=='male' else 'ж'} "
            if profile.get("weight"): p += f"Вес:{profile['weight']}кг "
            if profile.get("goal"): p += f"Цель:{profile['goal']} "
            if p: sys += " " + p
        # Берём только последние 6 сообщений чтобы не превышать лимит
        recent = messages[-6:] if len(messages) > 6 else messages
        api_msgs = [{"role":"system","content":sys}] + recent
        for attempt in range(3):
            try:
                r = await client.chat.completions.create(
                    model=AI_MODEL,
                    messages=api_msgs,
                    max_tokens=800,
                    temperature=0.7
                )
                return r.choices[0].message.content
            except Exception as e:
                if "429" in str(e) and attempt < 2:
                    await asyncio.sleep(5)
                    continue
                raise
    except Exception as e:
        if "429" in str(e):
            return "⏳ Лимит запросов исчерпан. Подожди 1-2 минуты и попробуй снова!"
        return f"Ошибка ИИ: {e}"

async def generate_meal_plan(profile, macros):
    try:
        r = await client.chat.completions.create(model=AI_MODEL, messages=[
            {"role":"system","content":"Нутрициолог. Короткий план. Русский."},
            {"role":"user","content":f"План питания. Вес:{profile.get('weight')}кг Цель:{profile.get('goal')} К:{macros['calories']} Б:{macros['protein']} Ж:{macros['fats']} У:{macros['carbs']}. 4 приёма с граммовками."}
        ], max_tokens=800, temperature=0.7)
        return r.choices[0].message.content
    except Exception as e:
        if "429" in str(e):
            return "⏳ Лимит. Подожди 1-2 минуты."
        return f"Ошибка: {e}"

async def lookup_food(food):
    try:
        r = await client.chat.completions.create(model=AI_MODEL, messages=[
            {"role":"system","content":"КБЖУ на 100г. Коротко."},
            {"role":"user","content":f"КБЖУ: {food}"}
        ], max_tokens=400, temperature=0.3)
        return r.choices[0].message.content
    except Exception as e:
        if "429" in str(e):
            return "⏳ Лимит. Подожди минуту."
        return f"Ошибка: {e}"
