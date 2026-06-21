import ollama
import json

async def parse_user_intent(user_text):
    system_prompt = """
    Ты — интеллектуальный ассистент погодного бота. Твоя единственная задача — извлечь из текста пользователя город для прогноза погоды.
    
    Ты должен вернуть ответ СТРОГО в формате JSON с тремя ключами:
    1. "is_weather_request": (true или false) — относится ли запрос вообще к погоде, одежде по погоде или планам, зависящим от погоды. Если пользователь просит рецепт, анекдот или пишет бред — ставь false.
    2. "city": (строка или null) — название города на русском языке в именительном падеже.

    Запрещено писать любой текст, кроме JSON.
    """

    response = ollama.chat(
        model='qwen2.5:1.5b',
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ],
        format="json" 
    )
    
    return json.loads(response['message']['content'])