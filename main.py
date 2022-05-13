from datetime import datetime, timedelta
from mongodb_manager import DataBaseManagerUser
import telebot
from telebot import types
import os

TOKEN = "5346501666:AAG-1onYl17JJlYBgQYatuTc8iqhBj5rTGw"
bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=["start"])
def service1_command(message):
    bot.send_message(message.chat.id, f"Hello {message.from_user.first_name}")


@bot.message_handler(commands=["help"])
def service1_command(message):
    bot.send_message(message.chat.id,
                     f"You Can Use /register To Register In This Bot & After Register , You Can Send Your Texts Or Images To Bot For Translate !")


@bot.message_handler(commands=["register"])
def service2_command(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Send phone",
                                        request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(message.chat.id, 'Send Your Phone Number :', reply_markup=keyboard)


@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        if message.from_user.id == message.contact.user_id:
            if not DataBaseManagerUser.check_login(user_id=message.from_user.id):
                DataBaseManagerUser.insert_user_data(user_id=message.from_user.id, phone=message.contact.phone_number)
                bot.send_message(message.chat.id, f'Successful | {message.contact.phone_number} Registered')
            else:
                bot.send_message(message.chat.id, f'You Are Already Registered')
        else:
            bot.send_message(message.chat.id, 'Failed ! Please Send Your Own Number !')


@bot.message_handler(commands=['check'])
def check_login(message):
    user_id = message.from_user.id
    if DataBaseManagerUser.check_login(user_id):
        bot.send_message(message.chat.id, 'You Are Registered')
    else:
        bot.send_message(message.chat.id, 'Please Use /register for register in this bot')


@bot.message_handler(commands=["users_list"])
def users_list(message):
    user_id = message.from_user.id
    if DataBaseManagerUser.check_login(user_id):
        if user_id == 1727224717:
            msg = ""
            for user in DataBaseManagerUser.users_list():
                msg += f"Phone : {user['phone']}\n"
            bot.send_message(message.chat.id, msg)
        else:
            bot.send_message(message.chat.id, 'Only Admin Can Use This Command !')
    else:
        bot.send_message(message.chat.id, 'Only Admin Can Use This Command !')


@bot.message_handler(commands=["shutdown"])
def service_handler(message):
    user_id = message.from_user.id
    if DataBaseManagerUser.check_login(user_id):
        now = datetime.now()
        add = timedelta(minutes=1)
        final_time = now + add
        bot.send_message(message.chat.id,
                         f'Shutdown scheduled for {final_time} +0430, use "/cancel" to cancel.')
        os.system("shutdown -h +1")
    else:
        bot.send_message(message.chat.id, 'Please Use /register for login in this bot')


@bot.message_handler(commands=["cancel"])
def service_handler(message):
    user_id = message.from_user.id
    if DataBaseManagerUser.check_login(user_id):
        os.system("shutdown -c now")
        bot.send_message(message.chat.id, 'Canceled !')
    else:
        bot.send_message(message.chat.id, 'Please Use /register for login in this bot')


@bot.message_handler(commands=["restart"])
def service_handler(message):
    user_id = message.from_user.id
    if DataBaseManagerUser.check_login(user_id):
        now = datetime.now()
        add = timedelta(minutes=1)
        final_time = now + add
        bot.send_message(message.chat.id,
                         f'Reboot scheduled for {final_time} +0430, use "/cancel" to cancel.')
        os.system("shutdown -r +1")
    else:
        bot.send_message(message.chat.id, 'Please Use /register for login in this bot')


bot.polling()
