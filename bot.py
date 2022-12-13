import telebot
import requests as rt
import settings as st
from bs4 import BeautifulSoup as bs

bot = telebot.TeleBot(st.TOKEN)
url = st.URL


def get_img_url(url, pair):
    my_obj = {'pair': pair, 'timeframe': '1h', 'candles': '1000',
              'ma': '50', 'tp': '10', 'sl': '10'}
    response = rt.post(url, data=my_obj)
    soup = bs(response.content, 'html.parser')
    images = soup.select('img')
    if not images:
        return ''
    return url + images[0]['src'][2:]


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, 'Enter the trading pair (for example BTCUSDT)')


@bot.message_handler(content_types=['text'])
def send_img(message):
    img_url = get_img_url(url, message.text.upper())
    if not img_url:
        bot.send_message(message.chat.id, 'Incorrect trading pair. Enter for example BTCUSDT')
    else:
        bot.send_photo(message.chat.id, get_img_url(url, message.text.upper()))


def main():
    bot.polling()


main()
