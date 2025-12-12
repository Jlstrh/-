import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = os.getenv("BOT_TOKEN")               # токен из переменной окружения
DOMAIN = os.getenv("WEBHOOK_DOMAIN")         # например: https://имя.onrender.com
PORT = int(os.getenv("PORT", "10000"))       # Render задаёт автоматически

ADMIN_CHAT_ID = 974242103
GROUP_CHAT_ID = -1002763129980

def start(update, context):
    rules = (
        "✨🐀 Привет! Это Витебская кдшная подслушка ✨🐀\n"
        " Пиши сюда, чем ты хочешь поделиться с нами в этот раз!\n\n"
        " Правила для постов подслушки:\n"
        "• Придерживайтесь темы кпопа и кд\n"
        "• Прямые оскорбления не публикуются\n"
        "• Призыв к хейту не публикуется\n"
        "• Неинформативные посты на 2-3 слова не публикуются\n"
    )
    update.message.reply_text(rules)

def forward_message(update, context):
    user = update.message.from_user
    username = user.username or "Без никнейма"
    text = update.message.text or ""

    msg_group = f"📩 Сообщение от @{username}:\n{text}"
    context.bot.send_message(chat_id=GROUP_CHAT_ID, text=msg_group)

    msg_admin = f"📩 Новое сообщение:\nОт: @{username}\nТекст: {text}"
    context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg_admin)

    update.message.reply_text("✨🐀 Спасибо большое за твое сообщение. Ждем тебя здесь снова!")

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN не задан в переменных окружения")
    if not DOMAIN:
        raise RuntimeError("WEBHOOK_DOMAIN не задан в переменных окружения (например https://имя.onrender.com)")

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_message))

    # Запуск webhook (обязательно для Web Service)
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN
    )
    updater.bot.set_webhook(f"{DOMAIN}/{TOKEN}")

    print(f"Webhook установлен: {DOMAIN}/{TOKEN}, слушаю порт {PORT}")
    updater.idle()

if __name__ == "__main__":
    main()
