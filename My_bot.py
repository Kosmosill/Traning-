## Название бота - Krakoko_bot
import json
import requests
import telebot

TOKEN = "7654910009:AAE4Qb9gUXwNq0BCmawwpO6xVkDka4SbTVo"

bot = telebot.TeleBot(TOKEN)
keys = {''
        'Биткоин': 'BTC',
        'Эфириум': 'ETH',
        'Доллар': 'USD',
       }
# https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD&api_key=89982f2d84077d7d517c8978fa8fb34786b245fc3c4f2b878ad2dde60205acb6
class ConvertionExeption(Exception):
    pass


@bot.message_handler(commands=['start'])
def function_Hello(message: telebot.types.Message):
    bot.reply_to(message, f"Hello {message.chat.username} Введите /help для моей работы")
@bot.message_handler(commands=['help'])
def function_Help(message: telebot.types.Message):
    text = ('Чтобы начать работу введите комманду боту в следующем формате: \n<имя валюты>  '
    '<в какую валюту перевести>'
    '<количество валюты> \n Список всех доступных валют: /values ')
    bot.reply_to(message, text)
@bot.message_handler(commands=['values'])
def values(massage: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(massage,text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    quote, baze, amount = values
    quote_ticker, baze_ticker = keys[quote], keys[baze]

    if len(values) > 3:
        raise ConvertionExeption('Слишком много параметров')

    quote, baze, amount = values

    if quote == baze:
        raise ConvertionExeption(f'Невозможно перевести одинаковые валюты {baze}')
    try:
        quote_ticker = keys[quote]
    except KeyError:
        raise ConvertionExeption(f'Не удалось обработать валюту{quote}')
    try:
        baze_ticker = keys[baze]
    except KeyError:
        raise ConvertionExeption(f'Не удалось обработать валюту{baze}')
    try:
        amount = float(amount)
    except ValueError:
        raise ConvertionExeption(f'Не удалось обработать количество {amount}')

    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={baze_ticker}&api_key=89982f2d84077d7d517c8978fa8fb34786b245fc3c4f2b878ad2dde60205acb6 ')
    total_baze = json.loads(r.content)[keys[baze]]
    local_baze = amount*total_baze
    text = f'Цена {amount} {quote} в {baze} - {local_baze}'
    bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)