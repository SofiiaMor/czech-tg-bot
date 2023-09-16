from random import choice
import telebot
import schedule
import time

token = '6507586626:AAEcnSLXd_SxtO6CX62dmRyoNtWSSYP8wPQ'
chat_id = '555519206'
bot = telebot.TeleBot(token)

CzRusDict = {}

HELP = '''
Список доступных команд:
/show  - показать перевод такого-то слова
/add - добавить слово с переводом в словарь
/random - показать рандомное чешское слово
/help - Напечатать справку по командам
'''


def add_word(cz_word, rus_word):
    cz_word = cz_word.lower()
    if CzRusDict.get(cz_word) is not None:
        CzRusDict[cz_word].append(rus_word)
    else:
        CzRusDict[cz_word] = [rus_word]


@bot.message_handler(commands=['start'])
def start_message(message):
    # chat_id = message.chat.id
    # Приветственное сообщение
    bot.send_message(message.chat.id, "Привет! Я бот для изучения чешских слов. Введи help, чтобы узнать какие команды я выполняю")
    # print(chat_id)

@bot.message_handler(commands=['help'])
def print_help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['random'])
def random(message):
    if len(CzRusDict) != 0:
        word = choice(list(CzRusDict.keys()))
        bot.send_message(message.chat.id, word)
    else:
        bot.send_message(message.chat.id, 'В словаре еще нет ни одного слова')


@bot.message_handler(commands=['add'])
def add(message):
    _, czword, rusword = message.text.split(maxsplit=2)
    add_word(czword, rusword)
    bot.send_message(message.chat.id, f'Слово {czword} добавлено в словарь')


@bot.message_handler(commands=['show'])
def show(message):
    word = message.text.split()[1].lower()
    if CzRusDict.get(word) is not None:
        rusword = CzRusDict[word]
    else:
        rusword = 'В словаре еще нет этого слова'
    bot.send_message(message.chat.id, rusword)


bot.polling(none_stop=True)


# Функция, которая будет отправлять слова по расписанию
def send_5random_words():
    count = 0
    if len(CzRusDict) >= 5:
        while count < 5:
            word = choice(list(CzRusDict.keys()))
            count += 1
            bot.send_message(chat_id, word)
    else:
        bot.send_message(chat_id, 'Добавь больше слов в словарь для изучения')


# Задаем время отправки сообщения
schedule.every().day.at("21:00").do(send_5random_words)

# Бесконечный цикл для проверки расписания
while True:
    schedule.run_pending()
    time.sleep(1)
