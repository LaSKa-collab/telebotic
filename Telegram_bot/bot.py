from telebot import *
from random import *

bot = TeleBot('7677125815:AAEzziHn5eP0ygem4tvH0UB71R0k3O5h5iA')

message_id = 0
number = 1
self_hp = 1
self_mana = 1
monster_hp = 1
score = 0


@bot.message_handler(content_types=['text'], commands=['start'])
def start(message):
    global self_hp, self_mana, monster_hp, number, score
    score = 0
    number = 1
    keyboard1 = telebot.types.InlineKeyboardMarkup()
    self_hp = randrange(20, 41)
    self_mana = randrange(10, 21)
    monster_hp = randrange(40, 81)
    chat_id = message.chat.id
    button_go = telebot.types.InlineKeyboardButton(text="Новая игра", callback_data='go')
    keyboard1.add(button_go)
    bot.send_message(chat_id, text='Начинаем?', reply_markup=keyboard1)


@bot.callback_query_handler(func=lambda call: call.data == 'go')
def battle(call):
    global self_hp, self_mana, monster_hp, message_id, score
    keyboard2 = telebot.types.InlineKeyboardMarkup()
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    button_attack = telebot.types.InlineKeyboardButton(text="Атака", callback_data='attack')
    button_heal = telebot.types.InlineKeyboardButton(text="Лечение", callback_data='heal')
    button_mana = telebot.types.InlineKeyboardButton(text="Спать", callback_data='mana')
    keyboard2.add(button_attack, button_heal, button_mana)
    if self_hp <= 0:
        lose(message)
        return 0
    elif monster_hp <= 0:
        score += 1
        new(message)
        return 0
    tx = (f'Игрок \n \n \n Здоровье:{self_hp} \n \n Мана:{self_mana} \n \n '
          f'\n -----------------------------------------\n Монстр {number} \n \n Здоровье:{monster_hp}')
    bot.send_message(chat_id, text=tx, reply_markup=keyboard2)


@bot.callback_query_handler(func=lambda call: call.data == 'attack')
def attack(call):
    global self_mana, message_id, self_hp, monster_hp
    message = call.message
    chat_id = message.chat.id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text='tx!')
    monster_hp -= randrange(1, 6)
    monster_turn(call)


@bot.callback_query_handler(func=lambda call: call.data == 'heal')
def heal(call):
    global self_mana, message_id, self_hp, monster_hp
    message = call.message
    chat_id = message.chat.id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text='tx!')
    self_hp += randrange(4, 10)
    self_mana -= 1
    monster_turn(call)


@bot.callback_query_handler(func=lambda call: call.data == 'mana')
def mana(call):
    global self_mana, message_id, self_hp, monster_hp
    self_mana += randrange(1, 4)
    monster_turn(call)


def monster_turn(call):
    global self_hp, message_id
    self_hp -= randrange(1, 6)
    battle(call)


def lose(message):
    global score
    chat_id = message.chat.id
    bot.send_message(chat_id, text=f'Вы проиграли. Ваш рекорд - {score}')
    start(message)


def new(message):
    global score, number, monster_hp
    keyboard = telebot.types.InlineKeyboardMarkup()
    chat_id = message.chat.id
    number += 1
    score += 1
    monster_hp = randrange(40, 81)
    button_go = telebot.types.InlineKeyboardButton(text="Следующий монстр", callback_data='go')
    keyboard.add(button_go)
    bot.send_message(chat_id, text=f'Вы победили монстра №{number}', reply_markup=keyboard)


bot.polling(none_stop=True, interval=2)
