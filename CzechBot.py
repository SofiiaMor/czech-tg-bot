from random import choice
import telebot
import schedule
import time
import threading

token = ' '
chat_id = ' '
bot = telebot.TeleBot(token)

CzRusDict = {}

HELP = '''
Список доступных команд:
/show  - показать перевод такого-то слова
/show_all - показать все слова, сохранненые в словаре
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
    words = message.text.split()
    if len(words) > 1:  # на случай, если пользователь не указал никакого слова, иначе выскачет ошибка
        _, czword, rusword = message.text.split(maxsplit=2)
        add_word(czword, rusword)
        bot.send_message(message.chat.id, f'Слово {czword} добавлено в словарь')
    else:
        bot.send_message(message.chat.id, 'Для вызова команды добавь связку слов')


@bot.message_handler(commands=['show'])
def show(message):
    words = message.text.split()
    if len(words) > 1:
        word = message.text.split()[1].lower()
        if CzRusDict.get(word) is not None:
            rusword = CzRusDict[word]
        else:
            rusword = 'В словаре еще нет этого слова'
        bot.send_message(message.chat.id, rusword)
    else:
        bot.send_message(message.chat.id, 'Для вызова команды добавь слово')


@bot.message_handler(commands=['show_all'])
def show_all(message):
    if len(CzRusDict) != 0:
        for key, value in CzRusDict.items():
            bot.send_message(message.chat.id, f'{key} : {value}')
    else:
        bot.send_message(message.chat.id, 'В словаре еще нет ни одного слова. Добавь сначала слова.')


# Создадим функцию, чтобы выполнять bot polling отдельно в треде
def bot_polling():
    bot.polling(none_stop=True)


bot_thread = threading.Thread(target=bot_polling)
bot_thread.start()


# Функция, которая будет отправлять 5 рандомных слов по расписанию
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


# Функция с бесконечным циклом для проверки расписания
def schedule_tasks():
    while True:
        schedule.run_pending()
        time.sleep(1)


# Отдельный тред для этой функции
schedule_thread = threading.Thread(target=schedule_tasks)
schedule_thread.start()
