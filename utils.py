import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты{base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        url = f"https://api.apilayer.com/currency_data/convert?to={base_ticker}&from={quote_ticker}&amount={amount}"

        payload = {}
        headers = {
            "apikey": "igMRTbk5TtUFll6a227gxjq71XPwvF2O"
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        result = json.loads(response.content)

        return result