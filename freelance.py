import requests
import feedparser
import os
import re
from datetime import datetime

# ============================================
# Telegram
# ============================================
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# ============================================
# МАКСИМАЛЬНО РАСШИРЕННЫЕ КЛЮЧЕВЫЕ СЛОВА
# ============================================
KEYWORDS = [
    # Создание сайтов
    "сайт", "лендинг", "landing", "интернет-магазин", "интернет магазин",
    "веб-сайт", "web-сайт", "web site", "website", "wp", "wordpress",
    "тильда", "tilda", "bitrix", "битрикс", "html", "css", "верстка",
    "посадочная страница", "корпоративный сайт", "сайт визитка",
    
    # Кодинг / Разработка
    "python", "javascript", "js", "react", "vue", "angular", "node.js",
    "django", "flask", "fastapi", "api", "бот", "telegram бот", "telegram",
    "парсинг", "скрапинг", "автоматизация", "скрипт", "программа",
    "приложение", "desktop app", "web app", "backend", "frontend",
    "база данных", "sql", "postgresql", "mysql", "php", "c#", "c++",
    "java", "spring", "rest api", "интеграция", "excel", "google sheets",
    
    # Логотипы и дизайн
    "логотип", "лого", "logo", "фирменный стиль", "брендинг", "айдентика",
    "фигма", "figma", "photoshop", "psd", "illustrator", "ai", "corel",
    "дизайн", "дизайнер", "web дизайн", "веб дизайн", "ui дизайн",
    "ux дизайн", "интерфейс", "mobile design", "app design",
    
    # Под ключ / для бизнеса
    "под ключ", "под-ключ", "полный цикл", "все включено",
    "малый бизнес", "средний бизнес", "для бизнеса", "бизнесу",
    "компания", "ип", "ооо", "стартап", "проект",
    
    # Создание чего-либо
    "создать", "разработать", "сделать", "написать", "сверстать",
    "нарисовать", "отрисовать", "разработка", "создание",
    
    # Карточки WB / Ozon
    "wb", "wildberries", "озон", "ozon", "маркетплейс", "карточка товара",
    "инфографика wb", "сео wb", "продвижение wb", "озон карточка",
    
    # Дополнительно
    "нужен", "помощь", "требуется", "ищу", "специалист", "фриланс"
]

# ============================================
# ОТПРАВКА В TELEGRAM
# ============================================
def send_tg(text):
    if not TOKEN or not CHAT_ID:
        print("❌ Нет токенов")
        return
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": text[:4000], "parse_mode": "HTML", "disable_web_page_preview": False}, timeout=30)
        print("✅ Отправлено")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

# ============================================
# ФИЛЬТРАЦИЯ (пропускает почти всё)
# ============================================
def is_relevant(title, description):
    """Проверяет, подходит ли заказ (очень широко)"""
    text = (title + " " + description).lower()
    # Если есть хоть одно ключевое слово — пропускаем
    for kw in KEYWORDS:
        if kw.lower() in text:
            return True
    # Если нет ключевых слов, но заказ короткий — тоже пропускаем
    if len(title) > 5 and len(title) < 100:
        return True
    return False

def extract_price(text):
    """Извлекает цену"""
    numbers = re.findall(r'(\d+)\s*₽', text)
    for num in numbers:
        try:
            return int(num)
        except:
            pass
    return None

# ============================================
# ПАРСЕРЫ
# ============================================

def parse_kwork():
    orders = []
    try:
        print("🔍 Kwork...")
        feed = feedparser.parse("https://kwork.ru/projects/rss")
        for entry in feed.entries[:50]:
            title = entry.title
            link = entry.link
            description = entry.description if hasattr(entry, 'description') else ""
            
            if not is_relevant(title, description):
                continue
            
            price = extract_price(title + description)
            price_str = f"💰 {price} ₽" if price else "💰 Цена не указана"
            
            orders.append({
                "title": title[:120],
                "link": link,
                "price": price_str,
                "platform": "🔥 Kwork"
            })
        print(f"   ✅ Найдено: {len(orders)}")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    return orders

def parse_freelancehunt():
    orders = []
    try:
        print("🔍 Freelancehunt...")
        feed = feedparser.parse("https://freelancehunt.com/rss/ru/projects.xml")
        for entry in feed.entries[:50]:
            title = entry.title
            link = entry.link
            description = entry.description if hasattr(entry, 'description') else ""
            
            if not is_relevant(title, description):
                continue
            
            dollars = re.findall(r'(\d+)\s*\$\s*', title + description)
            if dollars:
                price_usd = int(dollars[0])
                price_rub = price_usd * 90
                price_str = f"💰 {price_usd}$ (~{price_rub} ₽)"
            else:
                price_str = "💰 Цена не указана"
            
            orders.append({
                "title": title[:120],
                "link": link,
                "price": price_str,
                "platform": "⚡ Freelancehunt"
            })
        print(f"   ✅ Найдено: {len(orders)}")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    return orders

def parse_habr():
    orders = []
    try:
        print("🔍 Habr Freelance...")
        feed = feedparser.parse("https://freelance.habr.com/tasks/rss")
        for entry in feed.entries[:30]:
            title = entry.title
            link = entry.link
            
            orders.append({
                "title": title[:120],
                "link": link,
                "price": "💰 Смотрите на сайте",
                "platform": "📘 Habr Freelance"
            })
        print(f"   ✅ Найдено: {len(orders)}")
    except Exception as e:
        print(f"   ❌ Ошибка Habr: {e}")
    return orders

# ============================================
# ГЛАВНАЯ
# ============================================

def main():
    print("=" * 50)
    print(f"🤖 ЗАПУСК ПАРСЕРА")
    print(f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print(f"📊 Ключевых слов: {len(KEYWORDS)}")
    print("=" * 50)
    
    all_orders = []
    all_orders.extend(parse_kwork())
    all_orders.extend(parse_freelancehunt())
    all_orders.extend(parse_habr())
    
    # Удаляем дубликаты
    seen = set()
    unique_orders = []
    for order in all_orders:
        if order['link'] not in seen:
            seen.add(order['link'])
            unique_orders.append(order)
    all_orders = unique_orders
    
    if all_orders:
        msg = f"<b>🔍 НАЙДЕНО ЗАКАЗОВ: {len(all_orders)}</b>\n"
        msg += f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
        msg += "─" * 30 + "\n\n"
        
        for order in all_orders[:20]:
            msg += f"<b>{order['platform']}</b>\n"
            msg += f"📌 {order['title']}\n"
            msg += f"{order['price']}\n"
            msg += f"🔗 <a href='{order['link']}'>Прямая ссылка на заказ</a>\n\n"
        
        send_tg(msg)
    else:
        msg = f"<b>⚠️ ЗАКАЗОВ НЕ НАЙДЕНО</b>\n\n"
        msg += f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
        msg += "─" * 30 + "\n\n"
        msg += "<b>Возможные причины:</b>\n"
        msg += "• На биржах сейчас мало заказов\n"
        msg += "• RSS-лента обновляется раз в несколько часов\n\n"
        msg += "<b>Что делать:</b>\n"
        msg += "• Запустите ещё раз через 2-3 часа\n"
        msg += "• Добавьте свои ключевые слова в KEYWORDS"
        
        send_tg(msg)
    
    print("=" * 50)
    print("✅ ГОТОВО")
    print("=" * 50)

if __name__ == "__main__":
    main()