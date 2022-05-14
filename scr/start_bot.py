import logging
from telegram import Update
from telegram.ext import \
    ApplicationBuilder, \
    CallbackContext, \
    CommandHandler, \
    ConversationHandler, \
    MessageHandler, \
    filters
import json

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

stat_text = """*Этот бот поможет вам*:

/start Возможности бота
/getinfo Получить информацию по заказу
/gethelp Связаться со службой поддержки
/getdoc Загрузить необходимый документ
/cancel Закончить общение
"""

MENU, SEND_ID_INFO, SEND_ANSWER, SEND_DOC = range(4)

async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    logger.info("Пользователь %s начал общение.", update.message.from_user.first_name)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   parse_mode='Markdown', text=stat_text)
    return MENU

# async def getcomand(update: Update, context: CallbackContext.DEFAULT_TYPE):


async def getinfo(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   parse_mode='Markdown', text='Напишите номер вашего заказа')
    return SEND_ID_INFO

async def gethelp(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   parse_mode='Markdown', text='Какой вопрос вы хотите задать?')
    return SEND_ANSWER

async def getdoc(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   parse_mode='Markdown', text='Номер документа который необходимо загрузить')
    return SEND_DOC

async def send_id_info(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   parse_mode='Markdown', text='Спасибо вот информация по заказу:')
    return MENU

async def send_answer(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   parse_mode='Markdown', text='Ваше сообщение переданно в службу поддержки.\nМыскоро с вами свяжемся')
    return MENU

async def send_doc(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   parse_mode='Markdown', text='Направляем для вас документ:')
    return MENU

async def cancel(update: Update, context: CallbackContext.DEFAULT_TYPE):
    logger.info("User %s canceled the conversation.", update.message.from_user.first_name)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   parse_mode='Markdown', text='Спасибо за общение!')
    return ConversationHandler.END

if __name__ == '__main__':
    application = ApplicationBuilder().token(json.load(open('telegram_conf.json', 'r'))['token']).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start),
                      ],
        states={
            MENU : [
                CommandHandler('getinfo', getinfo),
                CommandHandler('gethelp', gethelp),
                CommandHandler('getdoc', getdoc),
                    ],
            SEND_ID_INFO: [MessageHandler(filters.TEXT, send_id_info)],
            SEND_ANSWER: [MessageHandler(filters.TEXT, send_answer)],
            SEND_DOC: [MessageHandler(filters.TEXT, send_doc)],
        },
        fallbacks = [CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)
    application.run_polling()