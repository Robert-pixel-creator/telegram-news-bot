import telebot
import requests
import time

# Укажи свой API-ключ Telegram бота
API_TOKEN = "7690832130:AAEAvY4qF_f76lg9T9wh-pCQfMU5HGK09LU"
CHAT_ID = "-1002391744807"

# API-ключ для NewsAPI (замени на свой)
NEWS_API_KEY = "0da7b6442d05447e920ceb0f108c043b"
NEWS_API_URL = "https://newsapi.org/v2/everything"

bot = telebot.TeleBot(API_TOKEN)

def get_ai_news():
    params = {
        "apiKey": NEWS_API_KEY,
        "q": "искусственный интеллект",
        "language": "ru",
        "pageSize": 5,
        "sortBy": "publishedAt"
    }
    
    try:
        response = requests.get(NEWS_API_URL, params=params)
        data = response.json()
        
        if response.status_code != 200:
            return f"Ошибка API: {data.get('message', 'Неизвестная ошибка')}"

        articles = data.get("articles", [])
        if not articles:
            return "Ошибка: Нет данных из NewsAPI"

        return articles
    except Exception as e:
        return f"Ошибка API: {e}"

def send_news():
    news = get_ai_news()
    if isinstance(news, str) and "Ошибка" in news:
        print(news)  # Логируем ошибку
        return

    if news:
        article = news[0]  # Берем первую новость
        title = article.get("title", "Без заголовка")
        description = article.get("description", "Описание отсутствует.")
        url = article.get("url", "#")
        image_url = article.get("urlToImage", None)
        
        message = f"📰 <b>{title}</b>\n\n{description}\n\n🔗 <a href='{url}'>Читать далее</a>"
        
        if image_url:
            bot.send_photo(CHAT_ID, image_url, caption=message, parse_mode="HTML")
        else:
            bot.send_message(CHAT_ID, message, parse_mode="HTML")

if __name__ == "__main__":
    print("Бот запущен")
    while True:
        send_news()
        time.sleep(21600)  # Ожидание 6 часов (21600 секунд)
