from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

import logging

updater = Updater("5668156930:AAFh8yLfdnQ10oPRgDaiLPr7WktA0D0SW6A",
                  use_context=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello! This is a Penta Organization LLC Bot for restocking monitoring.\nPlease type /help for proper "
        "start instructions")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("<Instructions will be displayed here>")


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"Sorry {update.message.text} is not a valid command")


if __name__ == '__main__':
    init_logging()
    logger = get_core_logger()
    logger.info('start')

    main()

    logger.info('finish')