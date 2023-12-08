import gspread
import telebot
from telebot.types import (InlineKeyboardMarkup, InlineKeyboardButton)

bot = telebot.TeleBot('6547252123:AAG0xQjS-irAC3_JyLHD7thXrGhfMZffJuA')

gc = gspread.service_account(filename="calm-vine-332204-924334d7332a.json")
sh_connection = gc.open_by_url('https://docs.google.com/spreadsheets/d/12JurYo1ywco0zqdtiF-C43U0PFooIJkTShguoPudHfs/edit#gid=956106302')
worksheet1 = sh_connection.sheet1
list_of_lists = worksheet1.get_all_values()


info_dict = {}

for i, sublist in enumerate(list_of_lists[1:]):
    info_dict[i] = sublist

user_data = {}

markup = InlineKeyboardMarkup()
markup.add(InlineKeyboardButton(text='>>>', callback_data='next'))

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.message.chat.id
    if user_id not in user_data:
        user_data[user_id] = 0

    if call.data == 'next':
        user_data[user_id] += 1
        if user_data[user_id] >= len(info_dict.keys()):
            user_data[user_id] = 0
            bot.send_message(call.message.chat.id, "КОНЕЦ! Повторяем сначала!", reply_markup=markup)
        send_info_block(call.message.chat.id)

    elif call.data[1] == 't':
        bot.send_message(call.message.chat.id, info_dict[user_data[user_id]][8], reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, info_dict[user_data[user_id]][9], reply_markup=markup)

        user_data[user_id] += 1
        if user_data[user_id] >= len(info_dict.keys()):
            user_data[user_id] = 0
            bot.send_message(call.message.chat.id, "Вы узнали все, что можно. Повторяем сначала!", reply_markup=markup)
        send_info_block(call.message.chat.id)

def send_info_block(user_id):
    if info_dict[user_data[user_id]][1] and not info_dict[user_data[user_id]][6]:
        bot.send_message(user_id, f'{info_dict[user_data[user_id]][1]}')

    if info_dict[user_data[user_id]][2]:
        pics = info_dict[user_data[user_id]][2].split(';')
        for img in pics:
            image_path = f"./files/{img}"
            with open(image_path, 'rb') as picture:
                bot.send_photo(user_id, picture)

    if info_dict[user_data[user_id]][3]:
        file = info_dict[user_data[user_id]][3]
        file_path = f"./files/{file}"
        bot.send_message(user_id, file)

    if info_dict[user_data[user_id]][4]:
        mp3 = info_dict[user_data[user_id]][4]
        mp3_path = f"./files/{mp3}"
        with open(mp3_path, 'rb') as mp3:
            bot.send_audio(user_id, mp3)

    if info_dict[user_data[user_id]][1] and info_dict[user_data[user_id]][6]:
        markup_answers = InlineKeyboardMarkup()
        for answer in info_dict[user_data[user_id]][6].split(','):
            if answer == info_dict[user_data[user_id]][7]:
                markup_answers.add(InlineKeyboardButton(text=answer, callback_data='at'))
            else:
                markup_answers.add(InlineKeyboardButton(text=answer, callback_data='af'))
        bot.send_message(user_id, info_dict[user_data[user_id]][1], reply_markup=markup_answers)
    else:
        bot.send_message(user_id, info_dict[user_data[user_id]][12], reply_markup=markup)


@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.chat.id
    user_data[user_id] = 0
    image_path = f"./files/{info_dict[0][2]}"
    with open(image_path, 'rb') as photo1:
        if message.text == '/start':
            bot.send_message(message.chat.id, f'{info_dict[0][1]}')
            bot.send_photo(message.chat.id, photo1, reply_markup=markup)

print("Ready")
bot.infinity_polling()
