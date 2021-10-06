#!/usr/bin/env python
import logging
from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    Filters,
    MessageHandler
)

''' Imports the environment variables '''
load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')

''' Enable logging '''
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

REPLY_MSG = r'''
Benvenuto in BIT PoliMi\!🚀

🎓 Siamo la prima associazione del Politecnico di Milano che si occupa di Bitcoin e crypto\. Ti consigliamo di leggere i messaggi pinnati in alto\.

📱Seguici sui nostri social e gruppi Telegram che trovi cliccando [qui](https://linktr.ee/BitPolimi)

📚 Se non sei un esperto, non ti preoccupare\! Sul nostro Mega troverai materiale utile per capire le basi di Bitcoin\.

📝 Ci sono poche regole da seguire:
\- No scam
\- No trading e finanza 
\- No politica
'''


def start(update: Update, context: CallbackContext):
    ''' /start handler '''
    update.message.reply_text('Hello!')


def help(update: Update, context: CallbackContext):
    ''' /help handler '''
    update.message.reply_text('Just add the bot to the group to start')


def new_user_handler(update: Update, context: CallbackContext):
    ''' When a new user joins the group, send them all the necessary information about Bit PoliMi '''
    for member in update.message.new_chat_members:
        message = update.message.reply_markdown_v2(
            f'Ciao {member.mention_markdown_v2()} ' + REPLY_MSG, disable_web_page_preview=True)

        try:
            context.job_queue.run_once(callback=delete_message, when=120,
                                       context=message.chat_id, name=(str(message.chat_id) + '.' + str(message.message_id)))

        except Exception as e:
            print("Scheduler Error: " + str(e))


def delete_message(context: CallbackContext):
    ''' Deletes the message sent by the bot '''
    chat_id, message_id = map(int, context.job.name.split('.'))
    context.bot.delete_message(chat_id, message_id)


def main():
    updater = Updater(token=BOT_TOKEN)

    dp = updater.dispatcher.add_handler

    dp(MessageHandler(Filters.status_update.new_chat_members, new_user_handler))
    dp(CommandHandler('start', start))
    dp(CommandHandler('help', help))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
