import requests, pandas as pd
from datetime import date, datetime, timedelta

api_key = 'INSERT_API_KEY_HERE'

def getPrice(ticker, date):
    base_url = 'https://api.polygon.io/v1/open-close/'
    addtnl_url = '?adjusted=true&apiKey='
    ticker_closing_price = requests.get(base_url + ticker + '/' + date + addtnl_url + api_key)
    if(ticker_closing_price.status_code == 200):
        tcp_dict = ticker_closing_price.json()
        return (tcp_dict['close'])
    else:
        return -1

def getListOfPrices(ticker, start_date, end_date):
    #converts start_date/end_date from string to datetime object
    date_startDate = datetime.strptime(start_date, '%Y-%m-%d').date()
    date_endDate = datetime.strptime(end_date, '%Y-%m-%d').date()
    delta = timedelta(days=1)

    prices_list = []
    while date_startDate <= date_endDate:
        str_startDate = date_startDate.strftime('%Y-%m-%d')
        temp_price = float(getPrice(ticker, str_startDate))
        prices_list.append(temp_price)
        date_startDate += delta
    return prices_list

