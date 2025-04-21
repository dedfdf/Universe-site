import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from random import choice, shuffle
from tkn import TOKEN
from planets import dict_planets
import sqlite3

# Логируем
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)
# Создание главной клавиатуры
main_keyboard = [['/help', '/game', '/statistic']]
markup_main = ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=False)

answer = 0
# Подключение к базе данных
con = sqlite3.connect("statistic_users.sqlite")
cur = con.cursor()


async def close_keyboard(update, context):
    await update.message.reply_text(reply_markup=ReplyKeyboardRemove())


async def start(update, context):
    close_keyboard(update, context)
    user = update.effective_user
    await update.message.reply_text(f'''Приветствую, я бот-помощник по сайту 
    "Путешествие по вселенной, {user.id}".''', reply_markup=markup_main)


async def helping(update, context):
    keyboard = [['/statistic', '/game']]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
    await update.message.reply_text('''Я пока что не знаю как вам помочь)''',
                                    reply_markup=markup)


async def statistic(update, context):
    keyboard = [['/help', '/game']]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
    user = update.effective_user.id
    rez = cur.execute("""SELECT user FROM statistic""").fetchall()
    if user in rez:
        right = cur.execute("""SELECT count_right FROM statistic""").fetchone()
        wrong = cur.execute("""SELECT count_wrong FROM statistic""").fetchone()
        await update.message.reply_text(f'''Ваша статистика:
            Всего попыток - {right + wrong}
            Правильных ответов - {right}
            Неправильных ответов - {wrong}''', reply_markup=markup)
    else:
        await update.message.reply_text('Извините, но Вы еще не играли!', reply_markup=markup)


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


async def right_answer(update, context):
    keyboard = [['/help', '/statistic']]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
    rez = cur.execute("""SELECT user FROM statistic""").fetchall()
    if update.effective_user.id in rez:
        n = cur.execute("""SELECT count_right FROM statistic WHERE user = ?""",
                        (update.effective_user.id,)).fetchone()
        que = '''UPDATE statistic SET count_right = ? WHERE user = ?'''
        cur.execute(que, (n + 1, update.effective_user.id))
    else:
        que = """INSERT INTO statistic(user, count_right, count_wrong) VALUES(?, 1, 0)"""
        cur.execute(que, (update.effective_user.id,))
    con.commit()
    await update.message.reply_text(
        f'Совершенно верно, Вы отгадали, теперь можете посмотреть свою статистику (/statistic)',
        reply_markup=markup)
    return ConversationHandler.END


async def wrong_answer(update, context):
    keyboard = [['/help', '/statistic']]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
    rez = cur.execute("""SELECT user FROM statistic""").fetchall()
    if update.effective_user.id in rez:
        n = cur.execute("""SELECT count_wrong FROM statistic WHERE user = ?""",
                        (update.effective_user.id,)).fetchone()
        que = '''UPDATE statistic SET count_wrong = ? WHERE user = ?'''
        cur.execute(que, (n + 1, update.effective_user.id))
        con.commit()
    else:
        que = """INSERT INTO statistic(user, count_right, count_wrong) VALUES(?, 0, 1)"""
        cur.execute(que, (update.effective_user.id,))
    con.commit()
    await update.message.reply_text(
        f'''Увы, вы не отгадали, не расстраивайтесь у вас обязательно получится в другой раз,
        теперь можете посмотреть свою статистику (/statistic)''',
        reply_markup=markup)
    return ConversationHandler.END


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", helping))
    app.add_handler(CommandHandler('game', game))
    app.add_handler(CommandHandler('statistic', statistic))
    conv_handler = ConversationHandler(entry_points=[CommandHandler('game', game)], states={
        1: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_answer)],
        2: [MessageHandler(filters.TEXT & ~filters.COMMAND, right_answer)],
        3: [MessageHandler(filters.TEXT & ~filters.COMMAND, wrong_answer)]},
                                       fallbacks=[CommandHandler('stop', stop)])
    app.add_handler(conv_handler)
    app.run_polling()


if __name__ == '__main__':
    main()
    con.close()
