import telebot
import requests
from datetime import datetime, date, time
from bs4 import BeautifulSoup
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import datetime

bot = telebot.TeleBot('1089262513:AAEKgwH1drH3vymrnaN79h1jM8JEQ4HRpK0')
player_link = ''
player_list = []
# d_user = input("date")

d1 = date(2019, 1, 1)
d2 = date.today()


# print(d2.strftime('%Y.%m.%d'))


@bot.message_handler(commands=['.'])
# после подтверждения ника появляются кнопки
def in_date(message):
    # функция календаря, принимает мессендж
    def start(m, v_string):
        calendar, step = DetailedTelegramCalendar().build()
        bot.send_message(m.chat.id,
                         f"{v_string} {LSTEP[step]}",
                         reply_markup=calendar)


        return message.message_id

    # Настройки календаря
    @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
    def cal(c):
        result, key, step = DetailedTelegramCalendar(locale='ru', min_date=d1, max_date=d2).process(c.data)
        if not result and key:
            bot.edit_message_text(f"Select {LSTEP[step]}",
                                  c.message.chat.id,
                                  c.message.message_id,
                                  reply_markup=key)
        elif result:
            bot.edit_message_text(f"Min: {result.strftime('%d.%m.%Y')}",
                                  c.message.chat.id,
                                  c.message.message_id)

            # функция построения диапазона дат от d1 до d2
            def date_range(d1, d2):
                return (d1 + datetime.timedelta(days=i) for i in range((d2 - d1).days + 1))

            first_date = result
            # вывод всех
            for d in date_range(first_date, d2):
                print(d.strftime('%Y.%m.%d'))

    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text='Выбрать начало', callback_data='first_date')
    markup.add(button)
    button = telebot.types.InlineKeyboardButton(text='Выбрать конец', callback_data='second_date')
    markup.add(button)
    bot.send_message(chat_id=message.chat.id, text='Some text', reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: True)
    def query_handler(call):
        if call.data == 'first_date':
            bot.answer_callback_query(callback_query_id=call.id, text='Hello world')
            start(message, v_string='Выберите начальную дату')
        if call.data == 'second_date':
            bot.answer_callback_query(callback_query_id=call.id, text='Sad world')


# Декоратор для обработки всех текстовых сообщений
@bot.message_handler(commands=['start'])
def all_messages(message):
    # функция календаря, принимает мессендж
    def start(m, v_string):
        calendar, step = DetailedTelegramCalendar().build()
        bot.send_message(m.chat.id,
                         f"{v_string} {LSTEP[step]}",
                         reply_markup=calendar)
        return message.message_id

    # Настройки календаря
    @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
    def cal(c):
        result, key, step = DetailedTelegramCalendar(locale='ru', min_date=d1, max_date=d2).process(c.data)
        if not result and key:
            bot.edit_message_text(f"Select {LSTEP[step]}",
                                  c.message.chat.id,
                                  c.message.message_id,
                                  reply_markup=key)
        elif result:
            bot.edit_message_text(f"Min: {result.strftime('%d.%m.%Y')}",
                                  c.message.chat.id,
                                  c.message.message_id)

            # функция построения диапазона дат от d1 до d2
            def date_range(d1, d2):
                return (d1 + datetime.timedelta(days=i) for i in range((d2 - d1).days + 1))

            first_date = result
            # вывод всех
            for d in date_range(first_date, d2):
                print(d.strftime('%Y.%m.%d'))

    start(message, v_string='Выберите начальную дату')

    # need button1-d1 > button2-d2


# Запрашиваем URL
# page = requests.get('https://www.hltv.org/stats/players?startDate=all')

# Скачиваем страницу
# soup = BeautifulSoup(page.content, "html.parser")

# Скрапим данные

# for i in range(1, 8):
#    name = soup.select('tr')[i].select('a')[0]['href']
#    i += 1
#
#    name = name.replace('?startDate=all', '').replace('/stats/players/', '')
#    player_list.append(name)
# print(name)
count_lines = sum(1 for line in open('players.txt', 'r'))  # волшебный подсчет строк в файле

# Формирование списка из ников и айди
for i in range(0, count_lines):
    with open('players.txt', 'r') as f:
        player_list.append(f.readlines()[i].replace('\n', ''))
    i += 0

print(player_list)

# login = input('Введите ник игрока: ')
login = 's1mple'
# поиск по нику среди списка
for j in range(0, len(player_list)):
    if login == player_list[j][-len(login):]:
        player_link = player_list[j]
        print("YES")
        break
    else:
        print("NO")
        j += 1

print('https://www.hltv.org/stats/players/matches/' + player_link)

# Запрашиваем URL
page = requests.get('https://www.hltv.org/stats/players/matches/' + player_link)

# Скачиваем страницу
soup = BeautifulSoup(page.content, "html.parser")
date = soup.select('tbody')[0].select('tr')[2].select('td')[0].find('div').contents[0]
print(date)

usr_date = '23/8/20'

if date == usr_date:
    link_match = soup.select('tbody')[0].select('tr')[2].select('td')[0].find('a')['href']
    print('https://www.hltv.org' + link_match)
else:
    print("Ne naydeno")


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Hello world")


if __name__ == '__main__':
    bot.polling(none_stop=True, timeout=123)
