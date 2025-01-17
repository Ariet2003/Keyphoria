from dotenv import load_dotenv
import requests
import base64
import os

load_dotenv()
# Получаем токен из переменных окружения
TOKEN = os.getenv("GITHUB_TOKEN")
print(TOKEN)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPENAI_API_KEY)

# Поисковый запрос
query = "OPENAI_API_KEY='sk"  # Ищем строку "OPENAI_API_KEY='sk"
url = f"https://api.github.com/search/code?q={query}&type=code"

# Заголовки для авторизации
headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

# ANSI коды для цветов
GREEN_TEXT = "\033[92m"
YELLOW_TEXT = "\033[93m"
RESET_TEXT = "\033[0m"
CYAN_TEXT = "\033[96m"
BOLD_TEXT = "\033[1m"

# Функция для получения содержимого файла
def get_file_content(file_url):
    response = requests.get(file_url, headers=headers)
    if response.status_code == 200:
        file_data = response.json()
        content = base64.b64decode(file_data["content"]).decode("utf-8")
        return content
    return None

# Отправка запроса на поиск
response = requests.get(url, headers=headers)

if response.status_code == 200:
    results = response.json()
    print(f"{CYAN_TEXT}{BOLD_TEXT}Найдено {results['total_count']} совпадений:{RESET_TEXT}")
    for index, item in enumerate(results["items"][:500], start=1):  # Нумерация результатов
        file_name = item["name"]
        repo_name = item["repository"]["full_name"]
        file_url = item["html_url"]
        api_file_url = item["url"]

        # Получаем содержимое файла
        content = get_file_content(api_file_url)
        if content:
            # Ищем ключевую строку и извлекаем текст до закрывающей кавычки
            start_index = content.find(query)
            if start_index != -1:
                # Начинаем с конца ключевой фразы и ищем закрывающую кавычку
                end_index = content.find("'", start_index + len(query))
                if end_index != -1:
                    extracted_key = content[start_index + len(query) - 2:end_index]
                    print(f"{YELLOW_TEXT}{BOLD_TEXT}{index}. {GREEN_TEXT}{extracted_key} : {RESET_TEXT}{file_url}{RESET_TEXT}")
                else:
                    print(f"{YELLOW_TEXT}{BOLD_TEXT}{index}. Ключ найден, но закрывающая кавычка отсутствует : {file_url}{RESET_TEXT}")
            else:
                print(f"{YELLOW_TEXT}{BOLD_TEXT}{index}. Ключевая фраза не найдена в файле {file_name} : {file_url}{RESET_TEXT}")
else:
    print(f"{CYAN_TEXT}{BOLD_TEXT}Ошибка при поиске:{RESET_TEXT} {response.status_code} - {response.json()}")
