import config
import telebot
import json
from parser import get_schedule

bot = telebot.TeleBot(config.token)
list_links = json.load(open('documents/links.json','r',encoding='utf-8'))

@bot.message_handler(commands=['start'])
def start_handler(message):
    print(message.chat.id, message.chat.username) # вместо print(one + ' ' + two)
    text = 'long long long'
    try:
        msg = "привет {0.first_name} {0.last_name} {1}".format(message.chat, text)
    except:
        msg = "привет {0.username} {1}".format(message.chat, text)
    bot.send_message(message.chat.id, msg)
    
@bot.message_handler(commands=['schedule'])
    bot.send_message(message.chat.id, "schedule")

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    print("alla")
    bot.send_chat_action(message.chat.id,'typing')
    print(list_links['groups'])
    
    if (message.text.strip().lower() in list_links['groups']):
        msg = get_schedule(message.text.strip().lower(),0)
        bot.send_message(message.chat.id, msg)
    elif (message.text.strip().lower() in list_links['lecturers']):
        msg = get_schedule(message.text.strip().lower(),1)
        bot.send_message(message.chat.id, msg)
    
    print("user: %s chat: %s" % (message.chat.username, message.chat.id)) 
    # или print("user: {0.username} chat: {0.id}".format(message.chat))

if __name__ == '__main__':
    bot.polling(none_stop=True)


