import telebot

bot = telebot.TeleBot("6990612590:AAHDdIF97AcwOa3-ueWTQmQhHeZ2EituXGI", parse_mode=None)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)