from tokens import cmc_token
from telegram_token import token

import json

import requests
from flask import Flask # Because we need to support SSL for the webhook method.
from flask import request
from flask import Response

app = Flask(__name__)



def write_json(data, filename = 'response.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_cmc_data(crypto):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    #symbol=BTC,ETH,XRP,BCH,EOS,LTC, xlm&CONVERT=BTC,ETH,EUR'
    params = {'symbol': crypto, 'convert': 'USD'}
    headers = {'X-CMC_PRO_API_KEY': cmc_token}

    r = requests.get(url, headers = headers, params = params).json()
    price = r['data'][crypto]['quote']['USD']['price']
    #write_json(r)

    #print(r)
    return price

def parse_message(message):
    chat_id = message['message']['chat']['id']
    txt = message['message']['text'] #/btc; or /maid

    pattern = r'/[a-zA-Z]{2,4}'

    ticker = re.findall(pattern, txt) #[...]

    if ticker:
        symbol = ticker[0][1:].upper() # /btc > btc .strip('/')
    else:
        symbol = ''

    return chat_id, symbol

def send_message(chat_id, text = 'bla-bla-bla'):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}

    r = requests.post(url, json=payload)
    return r

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id, symbol = parse_message(msg)

        if not symbol:
            send_message(chat_id, 'Wrong data')
            return Response('Ok', status=200)

        price = get_cmc_data(symbol)
        send_message(chat_id, price)
        #write_json(msg, 'telegram_request.json')

        return Response('Ok', status=200)
        # It will prevent telegram from spamming our bot with its requests.

    else:
        return '<h1>CoinMarketCap bot May18 LA ZCdfsfW</h1>'

def main():
    # TODO BOT

    # 1. Locally create a basic Flask application
    ### 2. Set up a tunnel
    # It allows anyone with internet to access our local host.
    # 3. Set a webhook
    #get_cmc_data('BTC')
    print(get_cmc_data('BTC'))
    #https://api.telegram.org/bot1776387033:AAHMievvzfpB4d04KY_WErp8ceVkRWacw14/getMe


if __name__ == '__main__':
    """
    A module can discover whether or not it is running in the main scope by checking its own __name__, which allows a common idiom for conditionally executing code in a module 
    when it is run as a script or with python -m but not when it is imported:
    """
    #main()
    app.run(debug = True)
    #http://localhost:5000/


