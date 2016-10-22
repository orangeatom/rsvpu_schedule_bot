import config
import telebot
import json
from parser import get_schedule

bot = telebot.TeleBot(config.token)
list_links = json.load(open('documents/links.json','r',encoding='utf-8'))


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    print("alla")
    bot.send_chat_action(message.chat.id,'typing')
    print(list_links['groups'])
    if(message.text == "/start"):
        print(str(message.chat.id) + " " + message.chat.username + " ")
        text = 'long long long'
        try:
            bot.send_message(message.chat.id, "привет " + message.chat.first_name + " " + message.chat.last_name + text)
        except:
            bot.send_message(message.chat.id, "привет " + message.chat.username + text)
    if (message.text == "/schedule"):
        bot.send_message(message.chat.id, "schedule")
    if (message.text.strip().lower() in list_links['groups']):
        msg = get_schedule(message.text.strip().lower(),0)
        bot.send_message(message.chat.id, msg)
    elif (message.text.strip().lower() in list_links['lecturers']):
        msg = get_schedule(message.text.strip().lower(),1)
        bot.send_message(message.chat.id, msg)


    print("user: " + str(message.chat.username) + " chat: " + str(message.chat.id))

if __name__ == '__main__':
    bot.polling(none_stop=True)


