import pandas as pd
from predictions import getData, predictPrices, checkData
import openpyxl

# To-Do: Verify user input
# range from start-end can also only be <= 5 days as the free polygon api only allows 5 calls/min
ticker = input('Enter a stock ticker: ')
start_date = input('Enter the start date(YYYY-MM-DD): ')
end_date = input('Enter the end date(YYYY-MM-DD): ')
score_predict = input('Enter sentiment score to predict: ')
spreadsheet_name = input('Enter name of output excel file: ')

data = getData(ticker, start_date, end_date)
#data = [prices[],scores[]]
checkData(data[0],data[1])

price_predicted = predictPrices(data[1],data[0],float(score_predict))
print('Predicted Stock Price for ' + ticker + ': ' + str(price_predicted))


scores = data[1]
prices = data[0]
scores.append(score_predict)
prices.append(price_predicted)
spreadsheet_data = {'Sentiment Score' : scores,
                    'Stock Price' : prices}
df = pd.DataFrame(spreadsheet_data)
# optional
#print(df)

#output data to excel spreadsheet
writer = pd.ExcelWriter(spreadsheet_name)
df.to_excel(writer)
writer.save()
print('Data outputted to ' + spreadsheet_name)
