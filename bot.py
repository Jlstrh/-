from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = "8420823187:AAG3LWxUiYIkYu4SIUNfDugSDivpcAOHmEA"
ADMIN_CHAT_ID = 974242103
GROUP_CHAT_ID = -1002763129980

# Приветствие и правила
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

# Обработка сообщений
def forward_message(update, context):
    user = update.message.from_user
    username = user.username or "Без никнейма"
    text = update.message.text or ""

    # В общий чат пересылаем с никнеймом
    msg_group = f"📩 Сообщение от @{username}:\n{text}"
    context.bot.send_message(chat_id=GROUP_CHAT_ID, text=msg_group)

    # Тебе лично пересылаем то же самое
    msg_admin = f"📩 Новое сообщение:\nОт: @{username}\nТекст: {text}"
    context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg_admin)

    # Отправляем пользователю подтверждение
    update.message.reply_text("✨🐀 Спасибо большое за твое сообщение. Ждем тебя здесь снова!")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_message))

    print("Бот запущен. Напиши ему в Telegram.")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
