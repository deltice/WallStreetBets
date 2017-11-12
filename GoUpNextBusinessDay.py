#EQ36A89Y52SSFKPM
import requests
import datetime

def convertDate(time):
    month = str(time.month)
    day = str(time.day)
    if len(month) < 2: month = "0" + month
    if len(day) < 2: day = "0" + day
    date = str(time.year) + "-" + month + "-" + day
    return date

def goUpNextBusinessDay(ticker, timestamp):
    parameters = {"function": "TIME_SERIES_DAILY", "outputsize": "full", "symbol": ticker, "apikey": "EQ36A89Y52SSFKPM"}

    response = requests.get("https://www.alphavantage.co/query", params=parameters)
    dict = response.json()

    time = datetime.datetime.fromtimestamp(int(timestamp))
    date = convertDate(time)

    while not date in dict["Time Series (Daily)"]:
        time += datetime.timedelta(days=1)
        date = convertDate(time)

    closing1 = (dict["Time Series (Daily)"][date]["4. close"])

    time += datetime.timedelta(days=1)
    date = convertDate(time)

    while not date in dict["Time Series (Daily)"]:
        time += datetime.timedelta(days=1)
        date = convertDate(time)

    closing2 = (dict["Time Series (Daily)"][date]["4. close"])
    if closing2 > closing1: return True
    else: return False


print(goUpNextBusinessDay("MSFT", "1509837783"))