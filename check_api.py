import os
from openai import OpenAI
from dotenv import load_dotenv

def request_to_ai(question):
    # Загружаем переменные окружения из файла .env
    load_dotenv()

    # Создаем клиента OpenAI
    client = OpenAI()
    # Устанавливаем API-ключ из переменной окружения
    client.api_key = os.getenv('OPENAI_API_KEY')

    ai_response = ""

    # Формируем запрос для модели AI
    prompt = (
        "У меня есть вопрос, пожалуйста, ответь: " + question
    )

    # Создаем список сообщений для запроса
    prompt_list = [{"role": "user", "content": prompt}]

    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=prompt_list,
        stream=True
    )

    for chunk in stream:
        # Получение текстового ответа
        response = chunk.choices[0].delta.content
        # print(response, end="")
        if response:
            ai_response += response

    return ai_response

