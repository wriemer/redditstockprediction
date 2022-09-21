import numpy as np, matplotlib.pyplot as plt, wsbdata
from sklearn.svm import SVR
from datetime import date, datetime, timedelta
from polygondata import getListOfPrices
from wsbdata import getListOfWeightedSentimentScores_5Days

def getData(ticker, start_date, end_date):
    prices = getListOfPrices(ticker, start_date, end_date)
    scores = getListOfWeightedSentimentScores_5Days(ticker, start_date, end_date)
    return [prices, scores]

def checkData(prices, scores):
    for i in range(len(prices)-1):
        if prices[i] == float(-1):
            del prices[i]
            del scores[i]

def predictPrices(weighted_sentiment_scores,prices,predict_sent_score):
    weighted_sentiment_scores = np.reshape(weighted_sentiment_scores, (len(weighted_sentiment_scores),1))
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
    svr_rbf.fit(weighted_sentiment_scores, prices)

    # Code below used for data visualization -> not necessary for final program
    '''
    plt.scatter(weighted_sentiment_scores, prices, color='black', label='Data')
    plt.plot(weighted_sentiment_scores, svr_rbf.predict(weighted_sentiment_scores),
             color='red', label='RBF model')
    plt.xlabel('Weighted Sentiment Score')
    plt.ylabel('Price')
    plt.title('Price vs Sentiment Score')
    plt.legend()
    plt.show()'''

    sent_score = [[predict_sent_score]]
    return svr_rbf.predict(sent_score)[0]


