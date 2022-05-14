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

async def getinfo(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   parse_mode='Markdown', text='Напишите номер вашего заказа')

async def gethelp(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   parse_mode='Markdown', text='Какой вопрос вы хотите задать?')

async def getdoc(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   parse_mode='Markdown', text='Номер документа который необходимо загрузить')


if __name__ == '__main__':
    application = ApplicationBuilder().token(json.load(open('telegram_conf.json', 'r'))['token']).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    getinfo_handler = CommandHandler('getinfo', getinfo)
    application.add_handler(getinfo_handler)

    gethelp_handler = CommandHandler('gethelp', gethelp)
    application.add_handler(gethelp_handler)

    getdoc_handler = CommandHandler('getdoc', getdoc)
    application.add_handler(getdoc_handler)

    application.run_polling()