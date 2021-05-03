#!/usr/bin/python3

import requests
import telebot
import json
import sqlite3 as sq
import time
#обработка запроса

with open ('Secret_Token') as myfile:
    list_file=(myfile.readlines())
my_token = list_file [0]

bot = telebot.TeleBot(my_token)


failed_message = 'На данный момент курсы валют не доступны./nПопробуйте через 5 минут.'
Adresses = []
list_values_USD_in = []
request_answer=False
list_dict=[]

while not (request_answer): # это на случай каких либо проблем с запросом
    try:
        r = requests.get('https://belarusbank.by/api/kursExchange')
        # присваиваем переменной полученные значения с сайта.
        list_dict = json.loads(r.text)  # применяем метод .text к r, а потом парсим методом json.loads в список словарей
        request_answer = True

    except requests.ConnectionError:
        @bot.message_handler(commands=['currency'])#не могу пока понять как сделать так, что бы в бот отправлялось сообщение "сервис недоступен".
        def start_message(message):
            bot.send_message(message.chat.id, 'Сервис не доступен, попробуйте через 5 минут')
        time.sleep(1)
        request_answer = False


#код фильтрации request


for i in range(len(list_dict)):  # создаем список значений по ключу USD_in пробегаясь по всем словарям
    list_values_USD_in.append(list_dict[i]['USD_in'])  # добавляем значение по ключу словаря

# создаем пустой список, в котором будут индексы словарей из списка словарей, соответсвующие максимальным курсам USD_in
Max_USD_in_indexes = []
for i in range(len(list_values_USD_in)):
    # сравниваем значение каждого элемента списка с максимальным значением из списка, в случае совпадения, добавляем в новый список индекс элемента
    if list_values_USD_in[i] == max(list_values_USD_in):
        Max_USD_in_indexes.append(i)

keys_adress = ['name_type', 'name', 'home_number', 'filials_text', 'street', 'street_type']

for i in Max_USD_in_indexes:
    k = str()
    for j in keys_adress:
        k = k + list_dict[i][j] + ' '
    Adresses.append(k)

list_telebot_message = ['Лучший курс покупки USD Беларусбанком по стране -', max(list_values_USD_in)]

failed_message = 'На данный момент курсы валют не доступны./nПопробуйте через 5 минут.'

# этап кэширования данных в SQL
with sq.connect("currency_base.db") as con:
    cur = con.cursor()  # cursor
    cur.execute("DROP TABLE IF EXISTS currency_base")
    cur.execute("""CREATE TABLE IF NOT EXISTS currency_base (
       max_currency REAL,
       adress TEXT
       )""")
    for i in Adresses:
        cur.execute(f"INSERT INTO currency_base (max_currency, adress) VALUES ({max(list_values_USD_in)}, '{i}')")


with sq.connect("currency_base.db") as con:
    cur = con.cursor()
    cur.execute("SELECT adress FROM currency_base")
    result_adresses =cur.fetchall()



# сам бот

@bot.message_handler(commands=['currency'])
def start_message(message):
    bot.send_message(message.chat.id, f'Лучший курс покупки USD Беларусбанком по стране - {max(list_values_USD_in)}')
    bot.send_message(message.chat.id, 'отделения банков:')
    for i in result_adresses:
        bot.send_message(message.chat.id,f'{i[0]}')

bot.polling()

