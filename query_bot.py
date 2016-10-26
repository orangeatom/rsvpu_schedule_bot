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
    lecturer = 2
    select = 3
    waiting_group = 4
    waiting_lecturer = 5
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
    usr = User.get_or_create(User_id=message.chat.id)
    usr[0].State = state.select
    usr[0].save()
    print(usr[0].State)
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row('Группа')
    markup.row('Преподаватель')
    bot.send_message(message.chat.id, "выберите тип необходимого расписания",reply_markup=markup)

@bot.message_handler(commands=['schedule'])
def send_schedule_today(message):
    bot.send_chat_action(message.chat.id,'typing')
    usr = User.get_or_create(User_id=message.chat.id)
    if usr[0].State == state.gpoup:
        try:
            text = '{0} \n{1}\n'.format(Weekdays[datetime.date.today().weekday()], datetime.date.today())
            msg = parser.get_schedule_today(usr[0].Group_id, 0)
            for lection in range(0, 7):
                # print(msg[0][lection][0] + " " + msg[0][lection][1])
                text += '{0} {1}\n'.format(msg[0][lection][0], msg[0][lection][1])
                print('1')
            bot.send_message(message.chat.id, text)
        except:
            bot.send_message(usr.User_id, 'Извините, в данный момент я не могу этого сделать.')
            pass
        pass
    elif usr[0].State == state.lecturer:
        try:
            print('1')
            text = '{0} \n{1}\n'.format(Weekdays[datetime.date.today().weekday()], datetime.date.today())
            print('1')
            msg = parser.get_schedule_today(usr[0].Lecturer_id, 1)
            for lection in range(0, 7):
                # print(msg[0][lection][0] + " " + msg[0][lection][1])
                text += '{0} {1}\n'.format(msg[0][lection][0], msg[0][lection][1])
            bot.send_message(message.chat.id, text)
        except:
            bot.send_message(usr[0].User_id, 'Извините, в данный момент я не могу этого сделать.')
    else:
        bot.send_message(usr[0].User_id, 'Выберите группу или преподавателя для действия этой команды')
    #bot.send_message(message.chat.id, msg)
    pass

@bot.message_handler(commands=['cansel'])

@bot.message_handler(commands=['schedule_t'])
def send_schedule_tomorrow(message):
    bot.send_chat_action(message.chat.id, 'typing')
    usr = User.get_or_create(User_id=message.chat.id)
    if usr[0].State == state.gpoup:
        try:
            dt = datetime.date.today()
            text = '{0} \n{1}\n'.format(Weekdays[datetime.date.today().weekday()], datetime.date.today())
            msg = parser.get_schedule_tomorrow(usr[0].Group_id, 0)
            for lection in range(0, 7):
                # print(msg[0][lection][0] + " " + msg[0][lection][1])
                text += '{0} {1}\n'.format(msg[0][lection][0], msg[0][lection][1])
                print('1')
            bot.send_message(message.chat.id, text)
        except:
            bot.send_message(usr[0].User_id, 'Извините, в данный момент я не могу этого сделать.')
            pass
        pass
    elif usr[0].State == state.lecturer:
        try:
            print('1')
            text = '{0} \n{1}\n'.format(Weekdays[datetime.date.today().weekday()], datetime.date.today())
            print('1')
            msg = parser.get_schedule_tomorrow(usr[0].Lecturer_id, 1)
            for lection in range(0, 7):
                # print(msg[0][lection][0] + " " + msg[0][lection][1])
                text += '{0} {1}\n'.format(msg[0][lection][0], msg[0][lection][1])
            bot.send_message(message.chat.id, text)
        except:
            bot.send_message(usr[0].User_id, 'Извините, в данный момент я не могу этого сделать.')
    else:
        bot.send_message(usr[0].User_id, 'Выберите группу или преподавателя для действия этой команды')
    # bot.send_message(message.chat.id, msg)
    pass

@bot.message_handler(commands=['schedule_w'])
def send_schedule_week(message):
    bot.send_chat_action(message.chat.id, 'typing')
    usr = User.get_or_create(User_id=message.chat.id)
    if usr[0].State == state.gpoup:
        try:
            msg = parser.get_schedule_week(usr[0].Group_id, 0)
            dt = datetime.date.today()
            for days in range(0,7):
                text = '{0} \n{1}\n'.format(Weekdays[dt.weekday()], dt)
                dt += datetime.timedelta(days=1)
                for lection in range(0, 7):
                    # print(msg[0][lection][0] + " " + msg[0][lection][1])
                    text += '{0} {1}\n'.format(msg[days][lection][0], msg[days][lection][1])
                bot.send_message(message.chat.id, text)
        except:
            bot.send_message(usr[0].User_id, 'Извините, в данный момент я не могу этого сделать.')
            pass
        pass
    elif usr[0].State == state.lecturer:
        try:
            msg = parser.get_schedule_week(usr[0].Lecturer_id, 0)
            dt = datetime.date.today()
            for days in range(0,7):
                text = '{0} \n{1}\n'.format(Weekdays[dt.weekday()], dt)
                dt += datetime.timedelta(days=1)
                for lection in range(0, 7):
                    # print(msg[0][lection][0] + " " + msg[0][lection][1])
                    text += '{0} {1}\n'.format(msg[days][lection][0], msg[days][lection][1])
                bot.send_message(message.chat.id, text)
        except:
            bot.send_message(usr[0].User_id, 'Извините, в данный момент я не могу этого сделать.')
            pass
        pass
    else:
        bot.send_message(usr[0].User_id, 'Выберите группу или преподавателя для действия этой команды')
    # bot.send_message(message.chat.id, msg)
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
            user.State = state.waiting_group
            user.save()
            bot.send_message(user.User_id, 'Введите название группы: ',reply_markup = markup)
        elif message.text == 'Преподаватель':
            markup = telebot.types.ReplyKeyboardHide()
            user.State = state.waiting_lecturer
            user.save()
            bot.send_message(user.User_id, 'Введите имя преподавателя: ',reply_markup= markup)
        else:
            bot.send_message(user.User_id, 'Выберите элемент из списка')

    elif user.State == state.waiting_group:
        if message.text.strip().lower() in queries['groups']:
            user.Group_id = queries['groups'][message.text.strip().lower()]
            user.State = state.gpoup
            user.save()
            bot.send_message(message.chat.id, 'Отлично, теперь вы можете получать расписание вашей группы {0} по запросу'.format(message.text))
        else:
            bot.send_message('Попробуйте еще, я не смог найти такую группу')
        pass
    elif user.State == state.waiting_lecturer:
        if message.text.strip().lower() in queries['lecturers']:
            user.Lecturer_id = queries['lecturers'][message.text.strip().lower()]
            user.State = state.lecturer
            user.save()
            bot.send_message(message.chat.id, 'Отлично, теперь вы можете получать ваше расписание по запросу'.format(message.text))
        else:
            bot.send_message('Попробуйте еще, я не смог найти этого преподавателя')
        pass

    elif user.State != state.select:
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


