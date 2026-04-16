import requests
import re
import os
from datetime import datetime
from bs4 import BeautifulSoup

# ============================================
# Telegram (из секретов GitHub)
# ============================================
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# ============================================
# НАСТРОЙКИ
# ============================================
MIN_PRICE = 2000  # минимальная цена в рублях

# Ваши навыки (для фильтрации)
MY_SKILLS = [
    "дизайн", "логотип", "фигма", "photoshop", "illustrator",
    "python", "javascript", "html", "css", "сайт", "лендинг",
    "парсинг", "бот", "telegram", "api", "wordpress",
    "wb", "wildberries", "озон", "карточка", "инфографика",
    "анализ", "аналитика", "копирайтинг", "текст"
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
# ПАРСЕР KWORK (реальный парсинг HTML)
# ============================================
def parse_kwork():
    orders = []
    try:
        print("🔍 Парсим Kwork (реальный парсинг)...")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        url = "https://kwork.ru/projects"
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ищем все карточки проектов
        projects = soup.select('.project-card, .cards-list-item, [class*="project"]')
        
        for project in projects[:30]:
            try:
                # Название
                title_elem = project.select_one('.project-card__title, .card-title, h3, a')
                title = title_elem.text.strip() if title_elem else ""
                
                # Ссылка
                link_elem = project.select_one('a')
                if link_elem and link_elem.get('href'):
                    link = "https://kwork.ru" + link_elem.get('href')
                else:
                    continue
                
                # Цена
                price_text = project.text
                price_match = re.search(r'(\d+)\s*₽', price_text)
                price = int(price_match.group(1)) if price_match else 0
                
                # Проверка цены
                if price < MIN_PRICE and price > 0:
                    continue
                
                # Проверка навыков
                if not any(skill.lower() in title.lower() or skill.lower() in price_text.lower() for skill in MY_SKILLS):
                    continue
                
                price_str = f"💰 {price} ₽" if price > 0 else "💰 Цена не указана"
                
                orders.append({
                    "title": title[:100],
                    "link": link,
                    "price": price_str,
                    "platform": "🔥 Kwork"
                })
            except:
                continue
        
        print(f"   ✅ Найдено: {len(orders)}")
    except Exception as e:
        print(f"   ❌ Ошибка Kwork: {e}")
    return orders

# ============================================
# ПАРСЕР FREELANCEHUNT
# ============================================
def parse_freelancehunt():
    orders = []
    try:
        print("🔍 Парсим Freelancehunt...")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        url = "https://freelancehunt.com/projects"
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        projects = soup.select('.project, .project-item, [class*="project"]')
        
        for project in projects[:30]:
            try:
                title_elem = project.select_one('.project-title, .title, a')
                title = title_elem.text.strip() if title_elem else ""
                
                link_elem = project.select_one('a')
                if link_elem and link_elem.get('href'):
                    link = "https://freelancehunt.com" + link_elem.get('href')
                else:
                    continue
                
                price_text = project.text
                price_match = re.search(r'(\d+)\s*\$\s*', price_text)
                price_usd = int(price_match.group(1)) if price_match else 0
                price_rub = price_usd * 90
                
                if price_rub < MIN_PRICE and price_rub > 0:
                    continue
                
                if not any(skill.lower() in title.lower() or skill.lower() in price_text.lower() for skill in MY_SKILLS):
                    continue
                
                price_str = f"💰 {price_usd}$ (~{price_rub} ₽)" if price_usd > 0 else "💰 Цена не указана"
                
                orders.append({
                    "title": title[:100],
                    "link": link,
                    "price": price_str,
                    "platform": "⚡ Freelancehunt"
                })
            except:
                continue
        
        print(f"   ✅ Найдено: {len(orders)}")
    except Exception as e:
        print(f"   ❌ Ошибка Freelancehunt: {e}")
    return orders

# ============================================
# ПАРСЕР HABR
# ============================================
def parse_habr():
    orders = []
    try:
        print("🔍 Парсим Habr Freelance...")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        url = "https://freelance.habr.com/tasks"
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        tasks = soup.select('.task, .tasks-list-item, [class*="task"]')
        
        for task in tasks[:30]:
            try:
                title_elem = task.select_one('.task__title, a')
                title = title_elem.text.strip() if title_elem else ""
                
                link_elem = task.select_one('a')
                if link_elem and link_elem.get('href'):
                    link = "https://freelance.habr.com" + link_elem.get('href')
                else:
                    continue
                
                price_text = task.text
                price_match = re.search(r'(\d+)\s*₽', price_text)
                price = int(price_match.group(1)) if price_match else 0
                
                if price < MIN_PRICE and price > 0:
                    continue
                
                if not any(skill.lower() in title.lower() or skill.lower() in price_text.lower() for skill in MY_SKILLS):
                    continue
                
                price_str = f"💰 {price} ₽" if price > 0 else "💰 Цена не указана"
                
                orders.append({
                    "title": title[:100],
                    "link": link,
                    "price": price_str,
                    "platform": "📘 Habr Freelance"
                })
            except:
                continue
        
        print(f"   ✅ Найдено: {len(orders)}")
    except Exception as e:
        print(f"   ❌ Ошибка Habr: {e}")
    return orders

# ============================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================
def main():
    print("=" * 50)
    print(f"🤖 ЗАПУСК ПАРСЕРА (реальные ссылки)")
    print(f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print(f"💰 Мин. цена: {MIN_PRICE} ₽")
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
        msg += f"💰 От {MIN_PRICE} ₽\n"
        msg += f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
        msg += "─" * 30 + "\n\n"
        
        for order in all_orders[:15]:
            msg += f"<b>{order['platform']}</b>\n"
            msg += f"📌 {order['title']}\n"
            msg += f"{order['price']}\n"
            msg += f"🔗 <a href='{order['link']}'>ПРЯМАЯ ССЫЛКА НА ЗАКАЗ</a>\n\n"
        
        send_tg(msg)
    else:
        msg = f"😴 <b>Заказов от {MIN_PRICE} ₽ не найдено</b>\n\n📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n💡 Попробуйте снизить MIN_PRICE в коде"
        send_tg(msg)
    
    print("=" * 50)
    print("✅ ГОТОВО")
    print("=" * 50)

if __name__ == "__main__":
    main()