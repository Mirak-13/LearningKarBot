import os
from dotenv import load_dotenv, find_dotenv
import telebot
from telebot import types
import proizvod

load_dotenv(find_dotenv())

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

nums = []


@bot.message_handler(commands=['sdsdыв2sdываывмсымsdsdsd!:sdsdsscvxcvxcv'])
def info(message):
    bot.clear_step_handler(message)
    bot.send_message(
        message.chat.id,
        'Жми /go'
    )


@bot.message_handler()
def oklad(message):
    global nums
    nums = []

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("В начало", callback_data='resetData'))
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}{f' {message.from_user.last_name}' if message.from_user.last_name != None else ''}!\nВведи свой оклад",
        reply_markup=markup
    )
    bot.register_next_step_handler(message, month)


def month(message):
    try:
        if message.text.isdigit():
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("В начало", callback_data='resetData'))
            bot.send_message(message.chat.id, "За какой месяц?\nВведи число от 1 до 12", reply_markup=markup)
            nums.append(int(message.text))
            bot.register_next_step_handler(message, result)
        else:
            raise ValueError('Только цифры')
    except ValueError as e:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("В начало", callback_data='resetData'))
        bot.reply_to(message, str(e), reply_markup=markup)


def result(message):
    try:
        if message.text.isdigit():
            if 0 < int(message.text) < 13:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("В начало", callback_data='resetData'))
                nums.append(int(message.text))
                bot.send_message(
                    message.chat.id,
                    f"Оклад: {proizvod.money(nums[0], nums[1])[0]} рублей\nОклад - 13%: {proizvod.money(nums[0], nums[1])[1]} рублей",
                    reply_markup=markup)
            else:
                raise ValueError('Месяц от 1 до 12!')
        else:
            raise ValueError('Только цифры!')
    except ValueError as e:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("В начало", callback_data='resetData'))
        bot.reply_to(message, str(e), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def inline_handler(call):
    if call.data == "resetData":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        info(call.message)


bot.polling(none_stop=True)
