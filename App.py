import telebot
from config import keys, TOKEN
from utils import ConvertionException, CurrencyConverter
import json
import requests
from telebot import types # для указание типов


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start',])
def help(message: telebot.types.Message):
    text = '''Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
    <в какую валюту перевести> \
    <количество переводимой валюты>\nУвидеть список всех доступных валют: /values'''
    bot.reply_to(message,text)

@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Спроси у меня', url='https://t.me/bidgann'
  )
    )
    bot.send_message(
        message.chat.id,
        '1) Чтобы получить список доступных валют нажмите /exchange.\n',
        reply_markup=keyboard
    )

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text='Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)
    text = 'Инструкция по использованию: /help'
    bot.send_message(message.chat.id,text)


@bot.message_handler(commands=['exchange'])
def exchange(message):
    payload = {}
    headers = {
        "apikey": "igMRTbk5TtUFll6a227gxjq71XPwvF2O"
    }
    kolvo = 1
    usdrub = f"https://api.apilayer.com/currency_data/convert?to=RUB&from=USD&amount={kolvo}"
    eurrub = f"https://api.apilayer.com/currency_data/convert?to=RUB&from=EUR&amount={kolvo}"
    cnyrub = f"https://api.apilayer.com/currency_data/convert?to=RUB&from=CNY&amount={kolvo}"
    response = requests.request("GET", usdrub, headers=headers, data=payload)
    response_2 = requests.request("GET", eurrub, headers=headers, data=payload)
    response_3 = requests.request("GET", cnyrub, headers=headers, data=payload)
    result = json.loads(response.content)
    result2 = json.loads((response_2.content))
    result3 = json.loads(response_3.content)
    text1 = f'Цена {kolvo} USD в RUB - {result["result"]}'
    text2 =f'Цена {kolvo} EUR в RUB - {result2["result"]}'
    text3 = f'Цена {kolvo} CNY в RUB - {result3["result"]}'
    text = '\n'.join([text1, text2, text3])
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def convert (message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')
        if len(values) !=3:
            raise ConvertionException('Слишком много/мало параметров')

        quote, base, amount = values
        result = CurrencyConverter.convert(quote,base,amount)
    except ConvertionException as e:
        bot.reply_to(message,f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message,f'не удалось обработать команду\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} - {result["result"]}'
        bot.send_message(message.chat.id,text)

bot.polling(none_stop=True)