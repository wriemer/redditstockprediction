import requests, pandas as pd
from datetime import date, datetime, timedelta


def getWSBSentiment(startDate): #returns pd.DataFrame
    wsb_base_url = 'https://tradestie.com/api/v1/apps/reddit?date='
    start_date_param = str(startDate)
    wsb_api_output = requests.get(wsb_base_url + start_date_param)
    stocks_list = wsb_api_output.json()
    #stocks_df form: [ index 0 - total # of stocks ][no_of_comments][sentiment][sentiment_score][ticker]
    #                [       0 - 50ish             ][125 or 3 or 42][bear/bull][0.333 or -0.199][ MSFT ]
    stocks_df = pd.DataFrame(stocks_list)
    return stocks_df

#convert dataframe to dict{date:dict{ticker:list[sentimentscore,numberofcomments]}}
def convertToDict(input_df,date):
    temp_stocks_as_list = input_df.values.tolist()
    #temp_stocks_as_list has form [numberofcomments,sentiment,sentimentscore,ticker]

    ticker_dict = {}
    #ticker_dict should have form {tickername : [sentiment_score, number_of_comments]}
    for stock in temp_stocks_as_list:
        scores_list = []
        scores_list.append(stock[2])
        scores_list.append(stock[0])
        ticker_dict[stock[3]] = scores_list

    output_dict = {}
    #output_dict should have form {date : {tickername1 : [ss, noc], tickername2 : [ss, noc]}}
    output_dict[date] = ticker_dict
    return output_dict

#get list of sentiment scores for one specific ticker over five day period starting at start date
def getListOfWeightedSentimentScores_5Days(ticker, start_date, end_date):
    date_startDate = datetime.strptime(start_date, '%Y-%m-%d').date()
    date_endDate = datetime.strptime(end_date, '%Y-%m-%d').date()
    scores_list = []

    delta = timedelta(days=1)
    while date_startDate <= date_endDate:
        str_startDate = date_startDate.strftime('%Y-%m-%d')
        stocks = convertToDict(getWSBSentiment(str_startDate),str_startDate)
        if not ticker in stocks[str_startDate]:
            print('Error, ticker was not mentioned on wsb')
            return;
        scores_list.append(stocks[str_startDate][ticker][0]*stocks[str_startDate][ticker][1])
        date_startDate += delta
    return scores_list






