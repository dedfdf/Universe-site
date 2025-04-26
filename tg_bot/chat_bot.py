import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
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
    user = update.effective_user
    await update.message.reply_text(f'''Приветствую, я бот-помощник по сайту 
    "Путешествие по вселенной, а так же со мной можно поиграть".''', reply_markup=markup_main)


async def helping(update, context):
    keyboard = [['/statistic', '/game']]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
    await update.message.reply_text(
        '''Этот бот был создан в качестве дополнения к сайту "Путешествие по вселенной".
        Связь с разработчиками: tg//user?id=6911621774, @dedfd3''',
        reply_markup=markup)


async def game(update, context):
    global answer
    answer = choice(list(dict_planets.keys()))
    list_answer = [answer]
    for i in range(3):
        first_wr_answer = choice(list(dict_planets.keys()))
        while first_wr_answer in answer:
            first_wr_answer = choice(list(dict_planets.keys()))
        list_answer.append(first_wr_answer)
    shuffle(list_answer)
    keyboard = [[list_answer[0], list_answer[1]], [list_answer[2], list_answer[3]], ['Сдаться']]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
    await update.message.reply_text('''Что это за планета?''',
                                    reply_markup=markup)
    await update.message.reply_photo(dict_planets[answer], reply_markup=markup)
    return 1


async def get_answer(update, context):
    text = update.message.text
    keyboard = [['/help', '/statistic']]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
    if text == answer:
        await update.message.reply_text(
            f'Совершенно верно, Вы отгадали, теперь можете посмотреть свою статистику (/statistic)',
            reply_markup=markup)
        rez = cur.execute("""SELECT user FROM statistic""").fetchall()
        if str(update.effective_user.id) in [x[0] for x in rez]:
            n = cur.execute("""SELECT count_right FROM statistic WHERE user = ?""",
                            (update.effective_user.id,)).fetchone()
            que = '''UPDATE statistic SET count_right = ? WHERE user = ?'''
            cur.execute(que, (int(n[0]) + 1, update.effective_user.id))
        else:
            que = """INSERT INTO statistic(user, count_right, count_wrong) VALUES(?, 1, 0)"""
            cur.execute(que, (update.effective_user.id,))
        con.commit()
        return ConversationHandler.END
    elif text == 'Сдаться':
        await update.message.reply_text(
            "Эта попытка не будет зачтена в статистику! У вас обязательно получится в другой раз",
            reply_markup=markup)
        return ConversationHandler.END
    await update.message.reply_text(
        f'''Увы, вы не отгадали, не расстраивайтесь у вас обязательно получится в другой раз,
    теперь можете посмотреть свою статистику (/statistic)''',
        reply_markup=markup)
    rez = cur.execute("""SELECT user FROM statistic""").fetchall()
    if str(update.effective_user.id) in [x[0] for x in rez]:
        n = cur.execute("""SELECT count_wrong FROM statistic WHERE user = ?""",
                        (update.effective_user.id,)).fetchone()
        que = '''UPDATE statistic SET count_wrong = ? WHERE user = ?'''
        cur.execute(que, (n + 1, update.effective_user.id))
        con.commit()
    else:
        que = """INSERT INTO statistic(user, count_right, count_wrong) VALUES(?, 0, 1)"""
        cur.execute(que, (update.effective_user.id,))
    con.commit()
    return ConversationHandler.END


async def statistic(update, context):
    keyboard = [['/help', '/game']]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
    user = update.effective_user.id
    rez = list(cur.execute("""SELECT user FROM statistic""").fetchall())
    if str(user) in [x[0] for x in rez]:
        right = list(cur.execute("""SELECT count_right FROM statistic""").fetchone())[0]
        wrong = list(cur.execute("""SELECT count_wrong FROM statistic""").fetchone())[0]
        count = len(
            list(cur.execute("""SELECT user FROM statistic WHERE count_right > ?""", right)))
        await update.message.reply_text(f'''Ваша статистика:
            Всего попыток - {right + wrong}
            Правильных ответов - {right}
            Неправильных ответов - {wrong}
            Ваш процент правильных ответов - {round(right / (right + wrong) * 100, 2)}%
            Вы занимаете {count + 1} место в глобальном списке''', reply_markup=markup)
    else:
        await update.message.reply_text('Извините, но Вы еще не играли!', reply_markup=markup)


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", helping))
    app.add_handler(CommandHandler('statistic', statistic))
    conv_handler = ConversationHandler(entry_points=[CommandHandler('game', game)], states={
        1: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_answer)]},
                                       fallbacks=[CommandHandler('stop', stop)])
    app.add_handler(conv_handler)
    app.run_polling()


if __name__ == '__main__':
    main()
    con.close()
