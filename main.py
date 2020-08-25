import telebot
import requests

from bs4 import BeautifulSoup

bot = telebot.TeleBot('1089262513:AAEKgwH1drH3vymrnaN79h1jM8JEQ4HRpK0')
player_link = ''

# Запрашиваем URL
page = requests.get('https://www.hltv.org/stats/players?startDate=all')

# Скачиваем страницу
soup = BeautifulSoup(page.content, "html.parser")

# Скрапим данные
player_list = []
for i in range(1, 8):
    name = soup.select('tr')[i].select('a')[0]['href']
    i += 1

    name = name.replace('?startDate=all', '').replace('/stats/players/', '')
    player_list.append(name)
    # print(name)

login = input('Введите ник игрока: ')

for j in range(0, len(player_list)):
    if login == player_list[j][-len(login):]:
        player_link = player_list[j]
        break
    else:
        j += 1

print('https://www.hltv.org/stats/players/'+player_link)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Hello world")




# Декоратор для обработки всех текстовых сообщений
@bot.message_handler(content_types=['text'])
def all_messages(message):

    print('1')

if __name__ == '__main__':
    bot.polling(none_stop=True, timeout=123)
