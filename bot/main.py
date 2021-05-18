from tokens import cmc_token
from telegram_token import token

import json

import requests
from flask import Flask # Because we need to support SSL for the webhook method.
from flask import request

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
@app.route('/', methods = ['POST', 'GET'])
def index():
    return '<h1>CoinMarketCap bot</h1>'

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


