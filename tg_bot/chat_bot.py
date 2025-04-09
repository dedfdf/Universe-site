import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
import asyncio
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from random import choice

TOKEN = '8132858580:AAE7HZhrZC83PuYsonAYMC25E7_50BuVXQE'
dict_planets = {}  # Жду планеты от Валентина
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)
main_keyboard = [['/help', '/game']]
markup_main = ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=False)


async def close_keyboard(update, context):
    await update.message.reply_text(reply_markup=ReplyKeyboardRemove())


async def start(update, context):
    await update.message.reply_text('''Приветствую, я бот-помощник по сайту 
    "Путешествие по вселенной".''', reply_markup=markup_main)


async def helping(update, context):
    await update.message.reply_text('''Я пока что не знаю как вам помочь)''',
                                    reply_markup=markup_main)


async def game(update, context):
    keyboard = [['1', '2'], ['3', '4']]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
    await update.message.reply_text('''Что это за планета?''',
                                    reply_markup=markup)
    await  update.message.reply_photo(
        'media/cezar.jpg')


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", helping))
    app.add_handler(CommandHandler('game', game))

    app.run_polling()


if __name__ == '__main__':
    main()
