import telebot
import os
import time
from datetime import datetime

# ========== БЕРЕМ ТОКЕН ИЗ ПЕРЕМЕННЫХ ХОСТИНГА ==========
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("❌ ОШИБКА: Токен не найден в переменных окружения!")
    print("Добавьте переменную BOT_TOKEN в панели Bothost")
    exit()

# ========== ИНИЦИАЛИЗАЦИЯ ==========
bot = telebot.TeleBot(TOKEN)
START_TIME = time.time()

# ========== КОМАНДЫ ==========

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = f"""
🤖 *Бот успешно запущен!*

📌 *Информация:*
🆔 Ваш ID: {message.chat.id}
👤 Юзер: @{message.from_user.username or 'нет'}

🛠 *Команды:*
/start - Приветствие
/help - Справка
/time - Время
/status - Статус
/echo [текст] - Повторить

✅ *Работает на Bothost.ru*
    """
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
📚 *Доступные команды:*

/start - Показать приветствие
/help - Показать эту справку
/time - Текущее время и дата
/status - Статус бота (время работы)
/echo [текст] - Повторить ваш текст

📦 *Версия библиотеки:* 3.1.1
    """
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['time'])
def send_time(message):
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    bot.reply_to(message, f"🕐 *Текущее время:*\n{now}", parse_mode='Markdown')

@bot.message_handler(commands=['status'])
def send_status(message):
    uptime = int(time.time() - START_TIME)
    hours = uptime // 3600
    minutes = (uptime % 3600) // 60
    seconds = uptime % 60
    
    status_text = f"""
📊 *Статус бота:*

✅ Бот: *Работает*
⏱ Время работы: {hours}ч {minutes}м {seconds}с
📦 Версия: 3.1.1
🖥 Хостинг: Bothost.ru
    """
    bot.reply_to(message, status_text, parse_mode='Markdown')

@bot.message_handler(commands=['echo'])
def send_echo(message):
    # Убираем команду /echo из текста
    text = message.text.replace('/echo', '', 1).strip()
    if text:
        bot.reply_to(message, f"🔊 *Эхо:* {text}", parse_mode='Markdown')
    else:
        bot.reply_to(message, "❌ Напишите текст после команды\nПример: `/echo Привет!`", parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Ответ на любое сообщение (для теста)
    bot.reply_to(message, f"📩 Вы написали: {message.text}")

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print(f"✅ Бот {bot.get_me().first_name} запущен!")
    print(f"🆔 Username: @{bot.get_me().username}")
    print("🔄 Ожидание сообщений...")
    bot.polling(none_stop=True)
