#!/usr/bin/python3

import requests
import telebot
import json

with open ('Secret_Token') as myfile:
    list_file=(myfile.readlines())
my_token = list_file [0]

bot = telebot.TeleBot(my_token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, написал мне /start , у тебя получилось!')

#bot.polling()

@bot.message_handler(commands=['currency'])
def start_message(message):
    try:
        r = requests.get('https://belarusbank.by/api/kursExchange')
        # присваиваем переменной полученные значения с сайта.

        list_dict = json.loads(r.text)  # применяем метод .text к r, а потом парсим методом json.loads в список словарей

        list_values_USD_in = []
        for i in range(len(list_dict)):  # создаем список значений по ключу USD_in пробегаясь по всем словарям
            list_values_USD_in.append(list_dict[i]['USD_in'])  # добавляем значение по ключу словаря

        # создаем пустой список, в котором будут индексы словарей из списка словарей, соответсвующие максимальным курсам USD_in
        Max_USD_in_indexes = []
        for i in range(len(list_values_USD_in)):
            # сравниваем значение каждого элемента списка с максимальным значением из списка, в случае совпадения, добавляем в новый список индекс элемента
            if list_values_USD_in[i] == max(list_values_USD_in):
                Max_USD_in_indexes.append(i)

        # keys = list(dict.keys(list_dict[i]))[41:34:-1]
        keys_adress = ['name_type', 'name', 'home_number', 'filials_text', 'street', 'street_type']

        Adresses = []
        #    for i in Max_USD_in_indexes:
        #        k = ' '.join(list(dict.values(list_dict[i]))[41:34:-1])  # преобразуем срез списка с конца по 34 элемент в строку
        #        Adresses.append(k)  # добавляем в список новую строку из предыдущей операции

        for i in Max_USD_in_indexes:
            k = str()
            for j in keys_adress:
                k = k + list_dict[i][j] + ' '
            Adresses.append(k)

        # import pandas as pd
        # pandas_adresses = pd.Series(Adresses)
        # print ("Лучший курсы покупки USD -", max(list_values_USD_in))
        # print ("Адрес отделения")
        # print(pandas_adresses)
        list_telebot_message = ['Лучший курс покупки USD Беларусбанком по стране -', max(list_values_USD_in)]

        message_telebot = ' '.join(list_telebot_message)
        join_Adresses = '\n'.join(Adresses)

        # bot.send_message(message.chat.id, 'Лучший курсы покупки USD -', max(list_values_USD_in), 'Адрес отделения', pandas_adresses)
        bot.send_message(message.chat.id, message_telebot)
        bot.send_message(message.chat.id, 'отделения банков:')
        bot.send_message(message.chat.id, join_Adresses)


    except requests.ConnectionError:
        bot.send_message(message.chat.id, 'На данный момент курсы валют не доступны.')
        bot.send_message(message.chat.id, 'Попробуйте немного позже.')

bot.polling()

