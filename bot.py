from urllib.request import urlopen
from bs4 import BeautifulSoup
import telebot
from telebot import types
from settings import TG_TOKEN

def funfuct():    
    inner_html_code = str(urlopen('https://randstuff.ru/fact/').read(), 'utf-8')
    inner_soup = BeautifulSoup(inner_html_code, "html.parser")    
    inner_soup = inner_soup.find('table', {"class": 'text'})
    fact = inner_soup.get_text()    
    return fact

bot = telebot.TeleBot(TG_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    randfact = types.KeyboardButton('ФАКТ🔎')    
    markup.add(randfact)
    mess = (f'Привет, <b>{message.from_user.first_name} {message.from_user.last_name}</b>!👋'            
            f' Этот бот расскажет тебе много интересных фактов🔎. Нажимай на кнопку "ФАКТ🔎" и полетели!🚀')
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)    
    bot.register_next_step_handler(message, on_click)

def on_click(message):    
    if message.text == 'ФАКТ🔎':
        bot.send_message(message.chat.id, funfuct())        
        bot.register_next_step_handler(message, on_click)
    elif message.text != 'ФАКТ🔎' and message.text != '/start':        
        bot.send_message(message.chat.id, 'Извините, я не понимаю... Нажмите на кнопку "ФАКТ🔎", чтобы получить рандомный факт)')        
        bot.register_next_step_handler(message, on_click)

bot.polling(none_stop=True)