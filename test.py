import config
import telebot
import json
from parser import get_schedule

bot = telebot.TeleBot(config.token)
list_links = json.load(open('documents/links.json','r',encoding='utf-8'))


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    print("alla")
    bot.send_message(message.chat.id, message.chat.id )

if __name__ == '__main__':
    bot.polling(none_stop=True)

