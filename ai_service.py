import os
import aiohttp
import random

# База готовых советов на случай сбоя ИИ
BACKUP_ANSWERS = [
    "💪 Для роста мышц старайся делать 8-12 повторений с весом, который тяжело доделать до конца.",
    "🍎 Питание — это 70% успеха. Держи белок на уровне 1.6-2г на кг веса.",
    "💧 Не забывай пить воду во время тренировки, это поддерживает твою выносливость.",
    "😴 Сон — главный жиросжигатель. Старайся спать не меньше 7-8 часов.",
    "🍗 Лучшие источники белка: куриное филе, яйца, творог и белая рыба.",
    "🏃‍♂️ Если хочешь похудеть, добавь 20 минут легкого кардио после основной тренировки."
]

async def generate_ai_response(prompt: str, system_prompt: str = "") -> str:
    groq_key = os.getenv("GROQ_API_KEY", "").strip()
    
    # Пытаемся достучаться до ИИ
    if groq_key:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {groq_key}"},
                    json={
                        "model": "llama3-8b-8192",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 300
                    },
                    timeout=5 # Быстрый тайм-аут, чтобы не ждать долго
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data["choices"][0]["message"]["content"]
        except:
            pass # Если не вышло, идем к запасному варианту ниже

    # Если ИИ не ответил за 5 секунд или ключа нет
    return f"🤖 Сейчас я очень загружен, но вот тебе важный совет:\n\n{random.choice(BACKUP_ANSWERS)}"
