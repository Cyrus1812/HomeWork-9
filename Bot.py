from telebot import types
import telebot
import random
import os
import time
import requests

count = 0
dataclose = open("Play.txt",'w+',encoding="utf-8")
dataclose.close 
start_play = False
bot = telebot.TeleBot("5838924178:AAH7l-u8BC4AQegn8Is-kzHW7-2u_GmdJ8s", parse_mode=None)

markup = types.ReplyKeyboardMarkup()
itembtn1 = types.KeyboardButton('Играть')
itembtn2 = types.KeyboardButton('/calc')
itembtn3 = types.KeyboardButton('/give_cat')
markup.add(itembtn1, itembtn2, itembtn3)
#tb.send_message(chat_id, 'Choose one letter:', reply_markup=markup)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет, '+ message.from_user.first_name +'\nЧем займёмся?\nМогу посчитать тебе любую задачу,напиши /calc "твоя задача"\nМогу прислать тебе милого котика\n/give_cat\nМожем сыграть в игру, просто напиши Играть', reply_markup=markup)

@bot.message_handler(commands=['calc'],content_types=["text"])
def Calc(message):
    print(message)
    bot.reply_to(message, eval(message.text[6:]))

@bot.message_handler(commands=['give_cat'])
def Cat(message):
    cat = f'https://cataas.com/cat?t=${time.time()}'
    bot.send_photo(message.chat.id, cat)

@bot.message_handler(content_types=['text'])
def Play(message):
    print(f'{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}: {message.text}')
    global start_play
    global count
    if start_play:
        if message.text.isdigit():
            count= count + 1
            number_user = int(message.text)
            data = open("Play.txt",'r',encoding="utf-8")
            number = data.readline()[:3]
            number = int(number)
            data.close
            if number_user > number:
                bot.send_message(message.from_user.id, 'Это число больше моего')
            elif number_user < number:
                bot.send_message(message.from_user.id, 'Это число меньше моего')
            elif number_user == number:
                bot.send_message(message.from_user.id, f'Поздравляю, ты угадал!!\nКоличество попыток: {count}')
                dataclose = open("Play.txt",'w+',encoding="utf-8")
                dataclose.close 
                start_play = False
        else:
            bot.send_message(message.from_user.id, 'Введи число')
    if 'Играть' in message.text:
            bot.send_message(message.from_user.id, 'Я загадал число от 1 до 1000, твоя задача угадать моё число, после каждой попытки я буду давать подсказку.\nВ конце игры я выведу количество твоих попыток.\nУдачи!') 
            start_play = True
            count = 0
            number = random.randint(1,1000)
            data = open("Play.txt",'a+',encoding="utf-8")
            data.writelines(str(number)+'\n')
            data.close
        
    



bot.infinity_polling()