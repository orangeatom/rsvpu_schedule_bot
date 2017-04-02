import config
import telebot
import parser
import datetime
import locale
from peewee import *


DB = SqliteDatabase('documents/users.db')
bot = telebot.TeleBot(config.token_test)
Weekdays = ('🌕 *Понедельник*',
            '🌖 *Вторник*',
            '🌗 *Среда*',
            '🌘 *Четверг*',
            '🌑 *Пятница*',
            '🌒 *Суббота*',
            '🌓 *Воскресенье*',)

class state:
    null = 0
    gpoup = 1
    lecturer = 2
    select = 3
    waiting_group = 4
    waiting_lecturer = 5

class User(Model):
    user_id = CharField(unique=True)
    State = IntegerField(null=True)
    # this data need to query to schedule
    Group_id = CharField(null=True)
    Lecturer_id = CharField(null=True)
    #request_data = CharField(null=True)
    class Meta:
        database = DB


class Group(Model):
    group_name = CharField(unique=True)
    group_id = CharField(null=True)

    class Meta:
        database = DB

class Teacher(Model):
    teacher_name = CharField(unique=True)
    teacher_id = IntegerField(null=True)

    class Meta:
        database = DB

class search_type:
    all = 0
    teachers = 1
    groups = 2


def search(str, type = 0):
    """search values for user text"""
    choice = []
    if type != 2:
        for teacher in Teacher.select().where(Teacher.teacher_name.contains(str)).order_by():
            choice.append(teacher.teacher_name)
            print(teacher.teacher_name)
    choice.sort()
    if type != 1:
        for group in Group.select().where(Group.group_name.contains(str)).order_by():
            choice.append(group.group_name)
            print(group.group_name)
    return choice
    
# todo rename count
def format_day(container,day,count):
    """return day in readable form"""
    text = ' {0}. _{1}_\n'.format(Weekdays[day.weekday()], day.strftime('%d %B'))
    for lecture in range(0, 7):
        text += '*{0}* {1}\n'.format(container[count][lecture][0], container[count][lecture][1])
    return text

@bot.message_handler(commands=['start'])
def hello_message(message):
    usr = User.create_or_get(user_id = message.chat.id, State = state.null)
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, "Приветствую, я неинтеллектуально обученная система по рассылке расписания \n Вы можете ввести название группы или часть от ФИО преподавателя "
                                      "и получить его расписание на сегодня (до 18 00) и на завтра (после 18 00)")

@bot.message_handler(commands=['set_group'])
def add_user(message):
    """this handler set user state to select, and send him custom keyboard"""
    bot.send_chat_action(message.chat.id, 'typing')
    usr = User.get_or_create(user_id=message.chat.id)
    usr[0].State = state.select
    usr[0].save()
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row('Группа')
    markup.row('Преподаватель')
    bot.send_message(message.chat.id, "выберите тип необходимого расписания",reply_markup=markup)

@bot.message_handler(commands=['schedule'])
def send_schedule_today(message):
    bot.send_chat_action(message.chat.id,'typing')
    usr = User.get_or_create(user_id=message.chat.id)
    if usr[0].State == state.gpoup:
        try:
            text = format_day(parser.get_schedule_today(usr[0].Group_id,0),datetime.date.today(), 0)
            bot.send_message(message.chat.id, text, parse_mode='Markdown')
        except:
            bot.send_message(usr[0].user_id, 'Извините, в данный момент я не могу этого сделать.')

    elif usr[0].State == state.lecturer:
        try:
            text = format_day(parser.get_schedule_today(usr[0].Lecturer_id,1),datetime.date.today(), 0)
            bot.send_message(message.chat.id, text ,parse_mode='Markdown')
        except:
            bot.send_message(usr[0].user_id, 'Извините, в данный момент я не могу этого сделать.')
    else:
        bot.send_message(usr[0].user_id, 'Выберите группу или преподавателя для действия этой команды')


@bot.message_handler(commands=['schedule_t'])
def send_schedule_tomorrow(message):
    bot.send_chat_action(message.chat.id, 'typing')
    usr = User.get_or_create(user_id=message.chat.id)
    dt = datetime.date.today() + datetime.timedelta(days=1)
    if usr[0].State == state.gpoup:
        try:
            text = format_day(parser.get_schedule_tomorrow(usr[0].Group_id,0),dt,0)
            bot.send_message(message.chat.id, text, parse_mode='Markdown')
        except:
            bot.send_message(usr[0].user_id, 'Извините, в данный момент я не могу этого сделать.')

    elif usr[0].State == state.lecturer:
        try:
            text = format_day(parser.get_schedule_tomorrow(usr[0].Lecturer_id,1),dt,0)
            bot.send_message(message.chat.id, text, parse_mode='Markdown')
        except:
            bot.send_message(usr[0].user_id, 'Извините, в данный момент я не могу этого сделать.')
    else:
        bot.send_message(usr[0].user_id, 'Выберите группу или преподавателя для действия этой команды')

@bot.message_handler(commands=['schedule_w'])
def send_schedule_week(message):
    bot.send_chat_action(message.chat.id, 'typing')
    usr = User.get_or_create(user_id=message.chat.id)
    dt = datetime.date.today()
    if usr[0].State == state.gpoup:
        try:
            msg = parser.get_schedule_week(usr[0].Group_id, 0)
            for days in range(0,7):
                text = format_day(msg,dt,days)
                dt += datetime.timedelta(days=1)
                bot.send_message(message.chat.id, text, disable_notification=True, parse_mode='Markdown',disable_web_page_preview=True)
        except:
            bot.send_message(usr[0].user_id, 'Извините, в данный момент я не могу этого сделать.')

    elif usr[0].State == state.lecturer:
        try:
            msg = parser.get_schedule_week(usr[0].Lecturer_id, 1)
            for days in range(0,7):
                text = format_day(msg,dt,days)
                dt += datetime.timedelta(days=1)
                bot.send_message(message.chat.id, text,disable_notification=True, parse_mode='Markdown')
        except:
            bot.send_message(usr[0].user_id, 'Извините, в данный момент я не могу этого сделать.')

    else:
        bot.send_message(usr[0].user_id, 'Выберите группу или преподавателя для действия этой команды')

@bot.message_handler(commands=['distribution'])
def set_distribution(message):
    bot.send_message(message.chat.id, "В ближайшем будующем.")

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_chat_action(message.chat.id,'typing')
    user = User.get(User.user_id == message.chat.id)
    hide_markup = telebot.types.ReplyKeyboardHide()

    if user.State == state.select:
        if message.text == 'Группа':
            user.State = state.waiting_group
            user.save()
            bot.send_message(user.user_id, 'Введите название группы: ', reply_markup=hide_markup)
        elif message.text == 'Преподаватель':
            user.State = state.waiting_lecturer
            user.save()
            bot.send_message(user.user_id, 'Введите имя преподавателя: ', reply_markup=hide_markup)
        else:
            bot.send_message(user.user_id, 'Выберите элемент из списка')

    elif user.State == state.waiting_group:
        if Group.select().where(Group.group_name == message.text.strip().lower()).exists():
            user.Group_id = Group.select().where(Group.group_name == message.text.strip().lower()).get().group_id
            user.State = state.gpoup
            user.save()
            bot.send_message(message.chat.id, 'Отлично, теперь вы можете получать расписание вашей группы {0} по запросу'.format(message.text), reply_markup=hide_markup)
        else:
            custom_keyboard = telebot.types.ReplyKeyboardMarkup()
            choice = search(message.text.strip().lower(),search_type.groups)
            if len(choice) > 0:
                for temp in choice:
                    custom_keyboard.row(temp)
                bot.send_message(message.chat.id, "Выберите из списка: ", reply_markup=custom_keyboard)
            else:
                bot.send_message(message.chat.id, "Я ничего не смог найти...")

    elif user.State == state.waiting_lecturer:
        if Teacher.select().where(Teacher.teacher_name == message.text.strip().lower()).exists():
            user.Lecturer_id = Teacher.select().where(Teacher.teacher_name == message.text.strip().lower()).get().teacher_id
            user.State = state.lecturer
            user.save()
            bot.send_message(message.chat.id, 'Отлично, теперь вы можете получать ваше расписание по запросу'.format(message.text), reply_markup=hide_markup)
        else:
            choice = search(message.text.strip().lower(),search_type.teachers)
            if len(choice) > 0:
                custom_keyboard = telebot.types.ReplyKeyboardMarkup()
                for temp in choice:
                    custom_keyboard.row(temp.title())
                bot.send_message(message.chat.id, "Выберите из предложенных вариантов или попробуйте ввести заного", reply_markup=custom_keyboard)
            else:
                bot.send_message(message.chat.id, "Извините, я ничего не смог найти. Попробуйте заного.",reply_markup=hide_markup)

    elif user.State != state.select:
        if Group.select().where(Group.group_name == message.text.strip().lower()).exists():
            try:
                id = Group.select().where(Group.group_name == message.text.strip().lower())
                text = format_day(parser.get_schedule_today(id[0].group_id.strip().lower(), 0), datetime.date.today(), 0)
                bot.send_message(message.chat.id, text, reply_markup=hide_markup, parse_mode='MARKDOWN')
            except:
                bot.send_message(message.chat.id, "Возникла ошибка ")

        elif Teacher.select().where(Teacher.teacher_name == message.text.strip().lower()).exists():
            try:
                id = Teacher.select().where(Teacher.teacher_name == message.text.strip().lower())
                text = format_day(parser.get_schedule_today(id[0].teacher_id, 1), datetime.date.today(), 0)
                bot.send_message(message.chat.id, text, reply_markup=hide_markup, parse_mode='MARKDOWN')
            except:
                bot.send_message(message.chat.id, "Возникла непредвиденная ошибка")
        else:
            choice = search(message.text.strip().lower())
            custom_keyboard = telebot.types.ReplyKeyboardMarkup()
            if len(choice) > 1:
                for temp in choice:
                    custom_keyboard.row(temp.title())
                bot.send_message(message.chat.id, "Выберите из предложенных вариантов или попробуйте ввести заного", reply_markup=custom_keyboard)
            if len(choice) == 1:
                try:
                    id = Group.select().where(Group.group_name == choice[0])
                    text = format_day(parser.get_schedule_today(id[0].group_id,0), datetime.date.today(),0)
                    markup_hide = telebot.types.ReplyKeyboardHide()
                    bot.send_message(message.chat.id, text, reply_markup=markup_hide, parse_mode='MARKDOWN')
                except:
                    id = Teacher.select().where(Teacher.teacher_name == choice[0])
                    text = format_day(parser.get_schedule_today(id[0].teacher_id,1),datetime.date.today(),0)
                    markup_hide = telebot.types.ReplyKeyboardHide()
                    bot.send_message(message.chat.id, text,reply_markup=markup_hide, parse_mode='MARKDOWN')


locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))

if __name__ == '__main__':
    bot.polling(none_stop=True)
