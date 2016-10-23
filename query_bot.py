import config
import telebot
import json
from parser import get_schedule

bot = telebot.TeleBot(config.token)
list_links = json.load(open('documents/links.json','r',encoding='utf-8'))


@bot.message_handler(commands=['start'])
def hello_message(message):
    #TODO need actual text
    bot.send_message(message.chat.id, "Приветствую, я неинтеллектуально обученная система по рассылке расписания \n Вы можете ввести название группы или часть от ФИО преподавателя "
                                      "и получить его расписание на сегодня (до 18 00) и на завтра (после 18 00)")

@bot.message_handler(commands=['set_group'])
def add_user(message):
    bot.send_message(message.chat.id, "Введите вашу группу, или Ваше имя, если вы являетесь преподавателем")
    #todo need to add user and his status
    pass

@bot.message_handler(commands=['schedule'])
def get_schedule_today(message):
    #todo
    pass

@bot.message_handler(commands=['schedule_t'])
def get_schedule_tommorow(message):
    #todo
    pass

@bot.message_handler(commands=['schedule_w'])
def get_schedule_week(message):
    #todo
    pass

@bot.message_handler(commands=['distribution'])
def set_distribution(message):
    #todo
    pass

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_chat_action(message.chat.id,'typing')
    if (message.text.strip().lower() in list_links['groups']):
        msg = get_schedule(message.text.strip().lower(),0)
        bot.send_message(message.chat.id, msg)
    elif (message.text.strip().lower() in list_links['lecturers']):
        msg = get_schedule(message.text.strip().lower(),1)
        bot.send_message(message.chat.id, msg)

if __name__ == '__main__':
    bot.polling(none_stop=True)


