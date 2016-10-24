import config
import telebot
import json
import parser
import usr
import datetime
from peewee import *

bot = telebot.TeleBot(config.token)
queries = json.load(open('documents/links.json', 'r', encoding='utf-8'))
bd = SqliteDatabase('users.db')
Weekdays = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье')


user = {}
class usr:
    id = 0
    status = 0
    options = []

class state:
    null = 0
    gpoup = 1
    select_group = 2
    waiting_answer = 3
    pass


@bot.message_handler(commands=['start'])
def hello_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, "Приветствую, я неинтеллектуально обученная система по рассылке расписания \n Вы можете ввести название группы или часть от ФИО преподавателя "
                                      "и получить его расписание на сегодня (до 18 00) и на завтра (после 18 00)")

@bot.message_handler(commands=['set_group'])
def add_user(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, "Введите нужную группу или имя")

    pass

@bot.message_handler(commands=['schedule'])
def send_schedule_today(message):
    bot.send_chat_action(message.chat.id,'typing')
    msg = ""


    bot.send_message(message.chat.id, msg)
    pass

@bot.message_handler(commands=['schedule_t'])
def send_schedule_tomorrow(message):
    bot.send_chat_action(message.chat.id, 'typing')
    pass

@bot.message_handler(commands=['schedule_w'])
def send_schedule_week(message):
    bot.send_chat_action(message.chat.id, 'typing')
    pass

@bot.message_handler(commands=['distribution'])
def set_distribution(message):
    bot.send_chat_action(message.chat.id, 'typing')
    pass

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_chat_action(message.chat.id,'typing')
    if (message.text.strip().lower() in queries['groups']):
        text = '{0} \n{1}\n'.format(Weekdays[datetime.date.today().weekday()], datetime.date.today())
        msg = parser.get_schedule_today(message.text.strip().lower(), 0)
        for lection in range(0,7):
            #print(msg[0][lection][0] + " " + msg[0][lection][1])
            text += '{0} {1}\n'.format(msg[0][lection][0] , msg[0][lection][1])

        bot.send_message(message.chat.id, text)
    elif (message.text.strip().lower() in queries['lecturers']):
        msg = parser.get_schedule_today(message.text.strip().lower(), 1)
        bot.send_message(message.chat.id, msg)


if __name__ == '__main__':
    bot.polling(none_stop=True)


