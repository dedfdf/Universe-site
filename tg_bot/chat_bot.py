import logging

from pygame.display import update
from telegram.ext import Application, MessageHandler, filters, CommandHandler
import asyncio
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ConversationHandler
from random import choice, shuffle

TOKEN = '8132858580:AAE7HZhrZC83PuYsonAYMC25E7_50BuVXQE'
dict_planets = {'Меркурий': 'media/Меркурий.jpg', 'Земля': 'media/Земля.jpg',
                'Венера': 'media/Венера.jpg', 'Марс': 'media/Марс.jpg', 'Уран': 'media/Уран.jpg',
                'Нептун': 'media/Нептун.jpg', 'Сатурн': 'media/Сатурн.jpg',
                'Юпитер': 'media/Юпитер.jpg'}
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)
main_keyboard = [['/help', '/game']]
markup_main = ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=False)
answer = 0
conv_handler = ConversationHandler(entry_points=[CommandHandler('game', game)], states={
    1: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_answer)],
    2: [MessageHandler(filters.TEXT & ~filters.COMMAND, right_answer)],
    3: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)]},
                                   fallbacks=[CommandHandler('stop', stop)])


async def close_keyboard(update, context):
    await update.message.reply_text(reply_markup=ReplyKeyboardRemove())


async def start(update, context):
    close_keyboard(update, context)
    await update.message.reply_text('''Приветствую, я бот-помощник по сайту 
    "Путешествие по вселенной".''', reply_markup=markup_main)


async def helping(update, context):
    await update.message.reply_text('''Я пока что не знаю как вам помочь)''',
                                    reply_markup=markup_main)


async def game(update, context):
    global answer
    answer = choice(list(dict_planets.keys()))
    first_wr_answer = choice(list(dict_planets.keys()))
    while first_wr_answer == answer:
        first_wr_answer = choice(list(dict_planets.keys()))
    second_wr_answer = choice(list(dict_planets.keys()))
    while first_wr_answer == answer:
        second_wr_answer = choice(list(dict_planets.keys()))
    third_wr_answer = choice(list(dict_planets.keys()))
    while third_wr_answer == answer:
        third_wr_answer = choice(list(dict_planets.keys()))
    list_answer = [answer, first_wr_answer, third_wr_answer, second_wr_answer]
    shuffle(list_answer)
    keyboard = [[list_answer[0], list_answer[1]], [list_answer[2], list_answer[3]]]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
    await update.message.reply_text('''Что это за планета?''',
                                    reply_markup=markup)
    await update.message.reply_photo(dict_planets[answer], reply_markup=markup)
    return 1


async def get_answer(update, context):
    # global answer
    text = update.message.reply_text
    if text == answer:
        return 2
    return 3


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", helping))
    app.add_handler(CommandHandler('game', game))

    app.run_polling()


if __name__ == '__main__':
    main()
