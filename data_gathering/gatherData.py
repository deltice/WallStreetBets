# gather data to train machine learning model

import praw
import csv
import requests
import datetime
import json
from credentials import credentials
from stockSymbols import symbols


def convertDate(time):
    month = str(time.month)
    day = str(time.day)
    if len(month) < 2: month = "0" + month
    if len(day) < 2: day = "0" + day
    date = str(time.year) + "-" + month + "-" + day
    return date

def goUpNextBusinessDay(ticker, timestamp):
    parameters = {"function": "TIME_SERIES_DAILY", "outputsize": "full", "symbol": ticker, "apikey": credentials["alphavantagekey"]}

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

reddit = praw.Reddit(client_id=credentials["client"],
					 client_secret=credentials["secret"],
					 username=credentials["username"],
					 password=credentials["password"],
					 user_agent="test script")

subreddit = reddit.subreddit('wallstreetbets')

csvfile = open('data.csv', 'wb')
writer = csv.writer(csvfile)

# start: 1478822400
# time = 1507680000
time = 1510012800 - 30*86400
while time < 1510012800:
	stocks = {}
	starttime = datetime.datetime.now()
	print(starttime)
	for submission in subreddit.submissions(time, time + 86400): ## past day
		# check if there is a stock symbol in the title/post or not
		stockFound = False
		allText = submission.title.encode('utf-8') + submission.selftext.encode('utf-8')
		splitData = allText.split(" ")
		for word in splitData:
			word = word.strip()
			if word.startswith("$"):
				word = word[1:].upper()
			elif word != word.upper():
				continue
			if word in symbols:
				stockFound = True
				break
		if not stockFound:
			continue
		# if there is a stock symbol found
		submission.comments.replace_more(limit=0)
		allText = submission.title.encode('utf-8') + submission.selftext.encode('utf-8')
		for comment in submission.comments.list():
			allText = allText + " " + comment.body.encode('utf-8')
		# writer.writerow([word, allText, submission.score, True])

		if word in stocks:
			(text, score, up) = stocks[word]
			stocks[word] = (text + " " + allText, score + int(submission.score), up)
		else:
			up = goUpNextBusinessDay(word, str(int(submission.created)))
			stocks[word] = (allText, int(submission.score), up)

	for stock in stocks:
		(text, score, up) = stocks[stock]
		writer.writerow([stock, text, score, up])	
	time += 86400
	print("finished a day")
	print(datetime.datetime.now() - starttime)

csvfile.close()
