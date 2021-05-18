from tokens import cmc_token

import json

import requests

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

def main():
    #get_cmc_data('BTC')
    print(get_cmc_data('BTC'))


if __name__ == '__main__':
    """
    A module can discover whether or not it is running in the main scope by checking its own __name__, which allows a common idiom for conditionally executing code in a module 
    when it is run as a script or with python -m but not when it is imported:
    """
    main()


