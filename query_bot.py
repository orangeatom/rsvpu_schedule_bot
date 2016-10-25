import config
import telebot
import json
import parser
import datetime
from peewee import *

user_base = SqliteDatabase('documents/users.db')

bot = telebot.TeleBot(config.token)
queries = json.load(open('documents/links.json', 'r', encoding='utf-8'))

Weekdays = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье')

class state:
    null = 0
    gpoup = 1
    select = 2
    waiting_group = 3
    waiting_lecturer = 4
    pass

class User(Model):
    User_id = CharField(unique=True)
    State = IntegerField(null=True)
    # this data need to query to schedule
    Group_id = CharField(null=True)
    Lecturer_id = CharField(null=True)

    Distribution = IntegerField(null=True)
    class Meta:
        database = user_base


def search():
    pass


@bot.message_handler(commands=['start'])
def hello_message(message):
    usr = User.create_or_get(User_id = message.chat.id, State = state.null)
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, "Приветствую, я неинтеллектуально обученная система по рассылке расписания \n Вы можете ввести название группы или часть от ФИО преподавателя "
                                      "и получить его расписание на сегодня (до 18 00) и на завтра (после 18 00)")

@bot.message_handler(commands=['set_group'])
def add_user(message):
    bot.send_chat_action(message.chat.id, 'typing')
    zzz = User.get_or_create(User_id = message.chat.id, State = state.select)
    print(zzz[0].State)
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row('Группа')
    markup.row('Преподаватель')
    bot.send_message(message.chat.id, "выберите тип необходимого расписания",reply_markup=markup)

@bot.message_handler(commands=['schedule'])
def send_schedule_today(message):
    bot.send_chat_action(message.chat.id,'typing')
    msg = ""
    bot.send_message(message.chat.id, msg)
    pass

@bot.message_handler(commands=['cansel'])

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
    #print(User.select().where(User.Id == message.chat.id and User.State == state.select))
    user = User.get(User.User_id == message.chat.id)
    if user.State == state.select:
        if message.text == 'Группа':
            markup =  telebot.types.ReplyKeyboardHide()
            bot.send_message(user.User_id, 'Введите название группы: ',reply_markup = markup)
        elif message.text == 'Преподаватель':
            markup = telebot.types.ReplyKeyboardHide()
            bot.send_message(user.User_id, 'Введите имя преподавателя: ',reply_markup= markup)
        else:
            bot.send_message(user.User_id, 'Выберите элемент из списка')

    elif user.State == state.null:
        if (message.text.strip().lower() in queries['groups']):
            try:
                text = '{0} \n{1}\n'.format(Weekdays[datetime.date.today().weekday()], datetime.date.today())
                msg = parser.get_schedule_today(message.text.strip().lower(), 0)
                for lection in range(0,7):
                    #print(msg[0][lection][0] + " " + msg[0][lection][1])
                    text += '{0} {1}\n'.format(msg[0][lection][0] , msg[0][lection][1])

                bot.send_message(message.chat.id, text)
            except:
                pass
        elif (message.text.strip().lower() in queries['lecturers']):
            try:
                text = '{0} \n{1}\n'.format(Weekdays[datetime.date.today().weekday()], datetime.date.today())
                msg = parser.get_schedule_today(message.text.strip().lower(), 1)
                for lection in range(0,7):
                    #print(msg[0][lection][0] + " " + msg[0][lection][1])
                    text += '{0} {1}\n'.format(msg[0][lection][0] , msg[0][lection][1])
                bot.send_message(message.chat.id, text)
            except:
                pass


if __name__ == '__main__':
    user_base.connect()
    user_base.create_tables([User], safe=True)
    user_base.close()
    bot.polling(none_stop=True)


