import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler
import json

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

stat_text = """*Этот бот поможет вам*:

/start Возможности бота
/getinfo Получить информацию по заказу
/gethelp Связаться со службой поддержки
/getdoc Загрузить необходимый документ
"""

async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    print(update['message']['date'])
    print(update['message']['from'])
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   parse_mode='Markdown', text=stat_text)


if __name__ == '__main__':
    application = ApplicationBuilder().token(json.load(open('telegram_conf.json', 'r'))['token']).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()