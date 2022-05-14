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
from mesag_text import mesags
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


MENU, SEND_ID_INFO, SEND_ANSWER, SEND_DOC = range(4)

async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    logger.info("Пользователь %s начал общение.", update.message.from_user.first_name)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   parse_mode='Markdown', text=mesags['start'])
    return MENU


async def getinfo(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   parse_mode='Markdown', text=mesags['getinfo'])
    return SEND_ID_INFO


async def gethelp(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   parse_mode='Markdown', text=mesags['gethelp'])
    return SEND_ANSWER


async def getdoc(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   parse_mode='Markdown', text=mesags['getdoc'])
    return SEND_DOC


async def send_id_info(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   parse_mode='Markdown', text=mesags['send_id_info'].format(update.message.text))
    return MENU


async def send_answer(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   parse_mode='Markdown', text=mesags['send_answer'].format(update.message.text))
    return MENU


async def send_doc(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   parse_mode='Markdown', text=mesags['send_doc'].format(update.message.text))
    return MENU


async def cancel(update: Update, context: CallbackContext.DEFAULT_TYPE):
    logger.info("User %s canceled the conversation.", update.message.from_user.first_name)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   parse_mode='Markdown', text=mesags['cancel'])
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