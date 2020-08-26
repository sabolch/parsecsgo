import telebot
import requests

from bs4 import BeautifulSoup

bot = telebot.TeleBot('1089262513:AAEKgwH1drH3vymrnaN79h1jM8JEQ4HRpK0')
player_link = ''

# Запрашиваем URL
#page = requests.get('https://www.hltv.org/stats/players?startDate=all')

# Скачиваем страницу
#soup = BeautifulSoup(page.content, "html.parser")

# Скрапим данные
player_list = []
#for i in range(1, 8):
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

print('https://www.hltv.org/stats/players/matches/'+player_link)

# Запрашиваем URL
page = requests.get('https://www.hltv.org/stats/players/matches/'+player_link)

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




# Декоратор для обработки всех текстовых сообщений
@bot.message_handler(content_types=['text'])
def all_messages(message):

    print('1')

if __name__ == '__main__':
    bot.polling(none_stop=True, timeout=123)
