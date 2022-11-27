import telebot
from telebot import types
import random
import time

count = 0                                          # счётчик для игры
dataclose = open("Play.txt",'w+',encoding="utf-8") # очистка файла для игры во время запуска бота
dataclose.close                                    #
start_play = False                                 # переменная для начала игры
start_calc = False                                 # переменная для вызова калькулятора

bot = telebot.TeleBot("5838924178:AAH7l-u8BC4AQegn8Is-kzHW7-2u_GmdJ8s", parse_mode=None)

markup = types.ReplyKeyboardMarkup(row_width=3)  # Активные кнопки
itembtn1 = types.KeyboardButton('Играть')        
itembtn2 = types.KeyboardButton('Калькулятор')
itembtn3 = types.KeyboardButton('/give_cat')
markup.add(itembtn1, itembtn2, itembtn3)


@bot.message_handler(commands=['start']) # старт программы
def send_welcome(message):
    bot.send_message(message.from_user.id, 'Привет, '+ message.from_user.first_name + ', открой меню', reply_markup=markup)

@bot.message_handler(commands=['give_cat']) # Призыв котика
def Cat(message):
    cat = f'https://cataas.com/cat?t=${time.time()}'
    bot.send_photo(message.chat.id, cat)



@bot.message_handler(content_types=['text']) 
def Play(message):
    print(f'{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}: {message.text}')
    global start_play
    global count
    global start_calc
    if start_play:                      # начало игры
        if message.text.isdigit():
            count= count + 1
            number_user = int(message.text)
            data = open("Play.txt",'r',encoding="utf-8")
            number = data.readline()[:3]
            number = int(number)
            data.close
            if number_user > number:
                bot.send_message(message.from_user.id, 'Бери меньше')
            elif number_user < number:
                bot.send_message(message.from_user.id, 'Бери больше')
            elif number_user == number:
                bot.send_message(message.from_user.id, f'Поздравляю, ты угадал!!\nКоличество попыток: {count}')
                dataclose = open("Play.txt",'w+',encoding="utf-8")
                dataclose.close 
                start_play = False
        else:
            bot.send_message(message.from_user.id, 'Введи число')
    if 'Играть' in message.text:                                        # Игра угадай число
            bot.send_message(message.from_user.id, 'Я загадал число от 1 до 1000, твоя задача угадать моё число, после каждой попытки я буду давать подсказку.\nВ конце игры я выведу количество твоих попыток.\nУдачи!') 
            start_play = True
            count = 0
            number = random.randint(1,1000)
            data = open("Play.txt",'a+',encoding="utf-8")
            data.writelines(str(number)+'\n')
            data.close
    
    
    if start_calc:                                              # Калькулятор
        print(int(eval(message.text)))
        bot.send_message(message.from_user.id, f"{message.text} = {int(eval(message.text))}")
        start_calc = False
    if 'Калькулятор' in message.text:
        start_calc = True
        bot.send_message(message.from_user.id, "Введи уравнение")

    

bot.infinity_polling()