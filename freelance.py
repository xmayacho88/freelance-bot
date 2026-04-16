import requests
import feedparser
import os
import re
from datetime import datetime

# ============================================
# Telegram (берутся из секретов GitHub)
# ============================================
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# ============================================
# ВАШИ НАВЫКИ (отредактируйте под себя)
# ============================================MY_SKILLS = [
    # Программирование
    "python", "javascript", "html", "css", "php", "java", "c#", "c++",
    "react", "vue", "angular", "node.js", "django", "flask",
    "wordpress", "tilda", "сайт", "лендинг", "верстка",
    
    # Дизайн
    "дизайн", "логотип", "фигма", "photoshop", "illustrator",
    "баннер", "визитка", "упаковка", "брендинг",
    
    # Контент
    "копирайтинг", "текст", "статья", "пост", "контент",
    "перевод", "английский", "переводчик",
    
    # Парсинг и боты
    "парсинг", "бот", "telegram", "api", "скрапинг",
    
    # Видео и SMM
    "видеомонтаж", "smm", "instagram", "tiktok", "рилс",
    "капкат", "премьера", "after effects",
    
    # Общие (важно!)
    "нужен", "помощь", "сделать", "разработка",
    "создать", "написать", "сверстать"
]
]

# ============================================
# ФУНКЦИЯ ОТПРАВКИ В TELEGRAM
# ============================================
def send_tg(text):
    if not TOKEN or not CHAT_ID:
        print("❌ Нет токенов Telegram")
        return
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": text[:4000], "disable_web_page_preview": True}, timeout=30)
        print("✅ Отправлено в Telegram")
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")

# ============================================
# ПАРСЕРЫ БИРЖ
# ============================================

def parse_kwork():
    """Kwork.ru"""
    orders = []
    try:
        print("🔍 Парсим Kwork...")
        feed = feedparser.parse("https://kwork.ru/projects/rss")
        for entry in feed.entries[:15]:
            title = entry.title
            if any(skill.lower() in title.lower() for skill in MY_SKILLS):
                # Извлекаем цену
                price = "💰 Цена не указана"
                if "₽" in title:
                    match = re.search(r'(\d+)\s*₽', title)
                    if match:
                        price = f"💰 {match.group(1)} ₽"
                orders.append({
                    "title": title[:80],
                    "link": entry.link,
                    "price": price,
                    "platform": "🔥 Kwork"
                })
        print(f"   ✅ Найдено: {len(orders)}")
    except Exception as e:
        print(f"   ❌ Ошибка Kwork: {e}")
    return orders

def parse_freelancehunt():
    """Freelancehunt.com"""
    orders = []
    try:
        print("🔍 Парсим Freelancehunt...")
        feed = feedparser.parse("https://freelancehunt.com/rss/ru/projects.xml")
        for entry in feed.entries[:15]:
            title = entry.title
            if any(skill.lower() in title.lower() for skill in MY_SKILLS):
                price = "💰 Цена не указана"
                if "$" in title:
                    match = re.search(r'(\d+)\s*\$\s*', title)
                    if match:
                        price = f"💰 {match.group(1)}$"
                orders.append({
                    "title": title[:80],
                    "link": entry.link,
                    "price": price,
                    "platform": "⚡ Freelancehunt"
                })
        print(f"   ✅ Найдено: {len(orders)}")
    except Exception as e:
        print(f"   ❌ Ошибка Freelancehunt: {e}")
    return orders

def parse_habr():
    """Habr Freelance"""
    orders = []
    try:
        print("🔍 Парсим Habr Freelance...")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        url = "https://freelance.habr.com/tasks"
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            # Простая проверка (для RSS у Habr нет ленты)
            orders.append({
                "title": "Посмотрите свежие заказы на Habr",
                "link": "https://freelance.habr.com/tasks",
                "price": "💰 Смотрите на сайте",
                "platform": "📘 Habr Freelance"
            })
        print(f"   ✅ Habr обработан")
    except Exception as e:
        print(f"   ❌ Ошибка Habr: {e}")
    return orders

def parse_weblancer():
    """Weblancer.net"""
    orders = []
    try:
        print("🔍 Парсим Weblancer...")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        url = "https://www.weblancer.net/projects/"
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            orders.append({
                "title": "Свежие заказы на Weblancer",
                "link": "https://www.weblancer.net/projects/",
                "price": "💰 Смотрите на сайте",
                "platform": "🌐 Weblancer"
            })
        print(f"   ✅ Weblancer обработан")
    except Exception as e:
        print(f"   ❌ Ошибка Weblancer: {e}")
    return orders

# ============================================
# ГЕНЕРАЦИЯ ИДЕЙ ДЛЯ КОНТЕНТА
# ============================================
def generate_content_idea():
    ideas = [
        "🎬 ИДЕЯ ДЛЯ РИЛС: Покажи, как ты находишь заказ за 5 минут",
        "📝 ПОСТ ДЛЯ БЛОГА: 5 ошибок новичка на фрилансе",
        "🎥 СЦЕНАРИЙ РИЛС: Чек-лист из 3 шагов для старта",
        "📊 КОНТЕНТ-ПЛАН: Что публиковать каждый день фрилансеру",
        "💡 ЛАЙФХАК: Как поднять цену на свои услуги",
        "🔥 ТРЕНД: Самые востребованные навыки 2026"
    ]
    import random
    return random.choice(ideas)

# ============================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================
def main():
    print("=" * 50)
    print(f"🤖 ЗАПУСК ПАРСЕРА ФРИЛАНС-БИРЖ")
    print(f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print("=" * 50)
    
    # Собираем заказы со всех бирж
    all_orders = []
    all_orders.extend(parse_kwork())
    all_orders.extend(parse_freelancehunt())
    all_orders.extend(parse_habr())
    all_orders.extend(parse_weblancer())
    
    # Формируем отчёт
    if all_orders:
        # Группируем по платформам
        grouped = {}
        for order in all_orders:
            plat = order['platform']
            if plat not in grouped:
                grouped[plat] = []
            grouped[plat].append(order)
        
        # Создаём сообщение
        msg = f"<b>🔍 НАЙДЕНО ЗАКАЗОВ: {len(all_orders)}</b>\n"
        msg += f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
        msg += "─" * 30 + "\n\n"
        
        for platform, orders in grouped.items():
            msg += f"<b>{platform}</b> ({len(orders)})\n"
            for order in orders[:5]:
                msg += f"📌 <b>{order['title']}</b>\n"
                msg += f"{order['price']}\n"
                msg += f"🔗 <a href='{order['link']}'>Смотреть заказ</a>\n\n"
        
        # Добавляем идею для контента
        msg += "─" * 30 + "\n"
        msg += f"<b>💡 {generate_content_idea()}</b>\n\n"
        msg += "<i>🤖 Отправлено автоматически из GitHub Actions</i>"
        
        send_tg(msg)
    else:
        msg = f"😴 <b>Новых подходящих заказов нет</b>\n\n"
        msg += f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
        msg += f"🎯 Ваши навыки: {', '.join(MY_SKILLS[:5])}...\n\n"
        msg += f"💡 {generate_content_idea()}\n\n"
        msg += "<i>Попробуйте расширить список навыков в настройках</i>"
        send_tg(msg)
    
    print("=" * 50)
    print("✅ Парсер завершил работу")
    print("=" * 50)

if __name__ == "__main__":
    main()