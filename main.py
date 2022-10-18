from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

import logging
from config.init_logging import init_logging
from config.loggers import get_core_logger

updater = Updater("5668156930:AAFh8yLfdnQ10oPRgDaiLPr7WktA0D0SW6A",
                  use_context=True)

from utils import db_handlers


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello! This is a Penta Organization LLC Bot for restock monitoring.\nPlease type /help for further "
        "exploitation instructions.")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("\n📝 Catalog 📝\n"
                              "/add_to_catalog <link>, <address>: to add products to the catalog\n"
                              "/catalog - to see all products.\n"
                              "/remove_from_catalog <product ID>: to remove a product from the catalog\n"
                              "/clear_list - to reset the catalog\n")


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"Sorry {update.message.text} is not a valid text")


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"Sorry {update.message.text} is not a valid command")


def error(bot, update, err):
    # Log Errors caused by Updates.
    logger.warning(f'Error: {update} caused error {err}')


if __name__ == '__main__':
    init_logging()
    logger = get_core_logger()
    logger.info('start')

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))

    # SQL Reminders (list.db)
    dp.add_handler(CommandHandler('add_to_catalog', db_handlers.add_to_catalog))
    dp.add_handler(CommandHandler('catalog', db_handlers.show_list))
    dp.add_handler(CommandHandler('clear_list', db_handlers.clear_list))
    dp.add_handler(CommandHandler('remove_from_catalog', db_handlers.remove_from_list))

    # Filter unknown commands and text
    dp.add_handler(MessageHandler(Filters.text, unknown_text))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    # Log all errors
    # dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()
