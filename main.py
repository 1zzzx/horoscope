import logging
import sqlite3
import telebot
import pymorphy2

from config import BOT_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '''Привет! Я бот-гороскопщик.
Напиши /info, чтобы начать работу и узнать о своём знаке зодиака больше информации!''')


@bot.message_handler(commands=['info'])
def info(message,):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = telebot.types.KeyboardButton('Калькулятор')
    itembtn2 = telebot.types.KeyboardButton('Характеристика')
    itembtn3 = telebot.types.KeyboardButton('Совместимость')
    itembtn4 = telebot.types.KeyboardButton('Статистика')
    itembtn5 = telebot.types.KeyboardButton('Записки')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
    bot.send_message(message.chat.id, 'Пожалуйста, выберите один из предложенных вариантов',
                     reply_markup=markup)


@bot.message_handler(commands=['back'])
def back(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = telebot.types.KeyboardButton('Калькулятор')
    itembtn2 = telebot.types.KeyboardButton('Характеристика')
    itembtn3 = telebot.types.KeyboardButton('Совместимость')
    itembtn4 = telebot.types.KeyboardButton('Статистика')
    itembtn5 = telebot.types.KeyboardButton('Записки')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
    bot.send_message(message.chat.id, 'Пожалуйста, выберите один из предложенных вариантов',
                     reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    zodiac_signs = ['Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева',
                    'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы']

    if message.text == 'Калькулятор':
        bot.send_message(message.chat.id, 'Введите дату рождения (дд.мм)')
        bot.register_next_step_handler(message, zodiac_calculation)
    elif len(message.text) == 5 and message.text[2] == '.':
        zodiac_calculation(message)
    elif message.text == 'Характеристика':
        markup = telebot.types.ReplyKeyboardMarkup(row_width=3)
        for sign in zodiac_signs:
            markup.add(telebot.types.KeyboardButton(sign))
        markup.add(telebot.types.KeyboardButton('/back'))
        bot.send_message(message.chat.id, "Выберите Ваш знак зодиака:", reply_markup=markup)
        bot.register_next_step_handler(message, character_zodiacsign)
    elif message.text.capitalize() in zodiac_signs:
        character_zodiacsign(message)
    elif message.text == 'Совместимость':
        bot.send_message(message.chat.id, 'Введите Ваши знаки зодиака (м ж):')
        bot.register_next_step_handler(message, compatibility_zodiacsigns)
    elif len(message.text.split()) == 2:
        if message.text.split()[0].capitalize() in zodiac_signs\
                and message.text.split()[1].capitalize() in zodiac_signs:
            compatibility_zodiacsigns(message)
    elif message.text == 'Статистика':
        zodiac_counts(message)
    elif message.text == 'Записки':
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        itembtn1 = telebot.types.KeyboardButton('Создать запись')
        itembtn2 = telebot.types.KeyboardButton('Посмотреть пометки')
        markup.add(itembtn1, itembtn2)
        bot.send_message(message.chat.id, 'Пожалуйста, выберите один из предложенных вариантов',
                         reply_markup=markup)
        bot.register_next_step_handler(message, notes)
    else:
        info(message)


def zodiac_calculation(message):
    data = message.text
    zodiac_sign = ''

    if len(data) == 5:
        if data[2] == '.':
            day, month = data.split('.')
            day, month = int(day), int(month)
            if day > 0 and day < 32 and month > 0 and month < 13:
                if (month == 1 and day >= 20) or (month == 2 and day <= 18):
                    zodiac_sign = "Водолей"
                elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
                    zodiac_sign = "Рыбы"
                elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
                    zodiac_sign = "Овен"
                elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
                    zodiac_sign = "Телец"
                elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
                    zodiac_sign = "Близнецы"
                elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
                    zodiac_sign = "Рак"
                elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
                    zodiac_sign = "Лев"
                elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
                    zodiac_sign = "Дева"
                elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
                    zodiac_sign = "Весы"
                elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
                    zodiac_sign = "Скорпион"
                elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
                    zodiac_sign = "Стрелец"
                else:
                    zodiac_sign = "Козерог"

                symbol = ''
                con = sqlite3.connect('zodiac.sqlite')
                cur = con.cursor()
                symbol = cur.execute("""SELECT zodiac_symbol FROM zodiac_symbol
                                            WHERE zodiac_sign == ?""", (zodiac_sign,)).fetchall()
                symbol = symbol[0][0]
                bot.send_message(message.chat.id, f'Ваш знак зодиака: {zodiac_sign} {symbol}')
                con.close()
                count_mentions(zodiac_sign)
            else:
                bot.send_message(message.chat.id, 'Упс! Проверьте правильность написания даты рождения (дд.мм)')
                bot.register_next_step_handler(message, zodiac_calculation)
        else:
            bot.send_message(message.chat.id, 'Упс! Проверьте правильность написания даты рождения (дд.мм)')
            bot.register_next_step_handler(message, zodiac_calculation)
    else:
        bot.send_message(message.chat.id, 'Упс! Проверьте правильность написания даты рождения (дд.мм)')
        bot.register_next_step_handler(message, zodiac_calculation)


def character_zodiacsign(message):
    zodiac_sign = message.text.capitalize()

    morph = pymorphy2.MorphAnalyzer()
    word = zodiac_sign
    count_mentions(word)
    word = morph.parse(word)[0]
    word = word.inflect({'gent'})[0]
    word = word.capitalize()

    symbol = ''
    con = sqlite3.connect('zodiac.sqlite')
    cur = con.cursor()
    symbol = cur.execute("""SELECT zodiac_symbol FROM zodiac_symbol
                        WHERE zodiac_sign == ?""", (zodiac_sign,)).fetchall()
    symbol = symbol[0][0]
    result = cur.execute("""SELECT character FROM zodiac_signs
                    WHERE zodiac_sign == ?""", (zodiac_sign,)).fetchall()
    result = result[0][0]
    con.close()
    bot.send_message(message.chat.id, f'Характеристика {word}{symbol}: {result}')


def compatibility_zodiacsigns(message):
    zodiac_signs = ['Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева',
                    'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы']
    num = 0
    zodiacs = message.text.split()

    for zodiac in zodiacs:
        zodiacs[num] = zodiac.capitalize()
        num += 1

    if zodiacs[0] in zodiac_signs and zodiacs[1] in zodiac_signs:
        result = ''
        zodiac_sign_m = zodiacs[0]
        zodiac_sign_w = zodiacs[1]
        count_mentions(zodiac_sign_m)
        count_mentions(zodiac_sign_w)
        con = sqlite3.connect('zodiac.sqlite')
        cur = con.cursor()
        result = cur.execute("""SELECT compatibility FROM zodiac_compatibility
                        WHERE zodiac_sign_m = ? and zodiac_sign_w = ?""", (zodiac_sign_m, zodiac_sign_w)).fetchall()
        result = result[0][0]
        con.close()
        bot.send_message(message.chat.id, result)
    else:
        bot.send_message(message.chat.id, 'Упс! Проверьте правильность написания (м ж)')
        bot.register_next_step_handler(message, compatibility_zodiacsigns)


def notes(message):
    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    if message.text == 'Создать запись':
        bot.send_message(message.chat.id, 'Введите знак зодиака и одно имя через пробел:', reply_markup=markup)
        bot.register_next_step_handler(message, zodiac_write_notes)
    elif message.text == 'Посмотреть пометки':
        bot.send_message(message.chat.id, 'Введите знак зодиака, чтобы посмотреть все записи:', reply_markup=markup)
        bot.register_next_step_handler(message, show_zodiac_notes)


def zodiac_write_notes(message):
    zodiac_signs = ['Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева',
                    'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы']

    zodiac_and_name = message.text.split()
    user_id = message.from_user.id

    if len(zodiac_and_name) == 2 and zodiac_and_name[0].capitalize() in zodiac_signs:
        zodiac = zodiac_and_name[0].capitalize()
        name = zodiac_and_name[1].capitalize()
        count_mentions(zodiac)

        con = sqlite3.connect("zodiac.sqlite")
        cursor = con.cursor()
        cursor.execute("SELECT name FROM zodiac_notes WHERE zodiac_sign=? AND name_user=?", (zodiac, user_id))
        row = cursor.fetchone()

        existing_names = row[0] if row else ""
        updated_name = existing_names + ", " + name if existing_names else name
        if row:
            cursor.execute("UPDATE zodiac_notes SET name=? WHERE zodiac_sign=? AND name_user=?", (updated_name, zodiac, user_id))
        else:
            cursor.execute("INSERT INTO zodiac_notes (zodiac_sign, name, name_user) VALUES (?, ?, ?)", (zodiac, name, user_id))

        con.commit()
        con.close()
        bot.send_message(message.chat.id, 'Записано!')
    else:
        bot.send_message(message.chat.id, 'Упс! Проверьте правильность написания знака зодиака и имени через пробел')
        bot.register_next_step_handler(message, zodiac_write_notes)


def show_zodiac_notes(message):
    zodiac = message.text.capitalize()
    user_id = message.from_user.id

    con = sqlite3.connect("zodiac.sqlite")
    cursor = con.cursor()
    cursor.execute("SELECT name FROM zodiac_notes WHERE zodiac_sign=? AND name_user=?", (zodiac, user_id))
    row = cursor.fetchone()

    if row is None:
        bot.send_message(message.chat.id, f"У вас нет имен со знаком зодиака {zodiac}")
    else:
        names_list = row[0].split(", ")
        names_str = "\n".join(names_list)
        bot.send_message(message.chat.id, f"Люди с знаком зодиака {zodiac}:\n{names_str}")

    con.close()


def count_mentions(zodiac):
    con = sqlite3.connect("zodiac.sqlite")
    cursor = con.cursor()
    cursor.execute("SELECT count FROM zodiac_counts WHERE zodiac_sign=?", (zodiac,))
    row = cursor.fetchone()

    if row is None:
        count = 1
        cursor.execute("INSERT INTO zodiac_counts (zodiac_sign, count) VALUES (?, ?)", (zodiac, count))
    else:
        count = row[0] + 1
        cursor.execute("UPDATE zodiac_counts SET count=? WHERE zodiac_sign=?", (count, zodiac))
    con.commit()
    con.close()


def zodiac_counts(message):
    con = sqlite3.connect("zodiac.sqlite")
    cursor = con.cursor()
    cursor.execute("SELECT zodiac_sign, count FROM zodiac_counts ORDER BY zodiac_sign")
    rows = cursor.fetchall()

    if rows:
        popular = max(rows, key=lambda x: x[1])
        unpopular = min(rows, key=lambda x: x[1])
        popular_sign = popular[0]
        pop_count = popular[1]
        unpopular_sign = unpopular[0]
        unpop_count = unpopular[1]

        morph = pymorphy2.MorphAnalyzer()
        word = 'запросы'
        parsed_word = morph.parse(word)
        word1 = parsed_word[0].make_agree_with_number(pop_count).word
        word2 = parsed_word[0].make_agree_with_number(unpop_count).word
        bot.send_message(message.chat.id, f'''Часто запрашиваемый знак - {popular_sign}: {pop_count} {word1}
Непопулярный знак - {unpopular_sign}: {unpop_count} {word2}''')

    con.close()


def main():
    bot.polling()


if __name__ == '__main__':
    main()