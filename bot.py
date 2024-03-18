import ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup
import telebot
from telebot import types
from settings import TG_TOKEN

ssl._create_default_https_context = ssl._create_unverified_context

def funfact():    
    inner_html_code = str(urlopen('https://randstuff.ru/fact/').read(), 'utf-8') 
    inner_soup = BeautifulSoup(inner_html_code, "html.parser")    
    inner_soup = inner_soup.find('table', {"class": 'text'})
    fact = inner_soup.get_text()    
    return fact

bot = telebot.TeleBot(TG_TOKEN)
bot_states = {}  # Словарь для хранения состояний бота для каждого пользователя

@bot.message_handler(commands=['start'])
def start(message):    
    chat_id = message.chat.id
    bot_states[chat_id] = True  # Устанавливаем начальное состояние бота для данного пользователя
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    random_fact = types.KeyboardButton('ФАКТ🔎')    
    markup.add(random_fact)
    mess = (f'Привет, <b>{message.from_user.first_name} {message.from_user.last_name}</b>!👋'            
            f' Этот бот расскажет тебе много интересных фактов🔎. Нажимай на кнопку "ФАКТ🔎" и полетели!🚀')
    bot.send_message(chat_id, mess, parse_mode='html', reply_markup=markup)    

@bot.message_handler(func=lambda message: message.text == 'ФАКТ🔎')
def send_fact(message):
    fact = funfact()
    bot.send_message(message.chat.id, fact)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    if bot_states.get(chat_id, True):  # Проверяем состояние бота перед отправкой сообщения
        if message.text != '/start' and message.text != 'ФАКТ🔎':
            bot.send_message(chat_id, 'Извините, я не понимаю... Нажмите на кнопку "ФАКТ🔎", чтобы получить рандомный факт')

bot.polling(none_stop=True)