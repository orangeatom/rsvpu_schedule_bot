import schedule
import time
import config
import telebot


bot = telebot.TeleBot(config.token)

def job(t):
    bot.send_message(237514032,"hi nigger")
    return

schedule.every().day.at("15:55").do(job,'It is 01:00')

while True:
    schedule.run_pending()
    time.sleep(60)

