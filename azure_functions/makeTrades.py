import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'venv/Lib/site-packages')))

import json
import ita
import praw
import requests
from credentials import credentials
from stockSymbols import symbols

reddit = praw.Reddit(client_id=credentials["client"],
					 client_secret=credentials["secret"],
					 username=credentials["username"],
					 password=credentials["password"],
					 user_agent="get top posts of day from wsb")

subreddit = reddit.subreddit("wallstreetbets")

stocks = {}
for submission in subreddit.top("day"):
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

	if word in stocks:
		(text, score) = stocks[word]
		stocks[word] = (text + " " + allText, score + int(submission.score))
	else:
		stocks[word] = (allText, int(submission.score))

symbols = []
scores = []
posts = []
for stock in stocks:
    symbols.append(stock)
    (text, score) = stocks[word]
    scores.append(score)
    posts.append(text)

r = requests.post("https://wsbprediction.azurewebsites.net/api/HttpTriggerPython31?code=OEqYAv/oDzpeYPRbLeQxU4ismYixlOU8DlLUALlsFdvjaw/a0Q2tug==",
    data=json.dumps({"redditPosts": posts})
)
predictions = json.loads(r.text)

client = ita.Account(credentials["invest_email"], credentials["invest_password"])
portfolio = client.get_current_securities()

for bought in portfolio.bought:
    client.trade(bought.symbol, ita.Action.sell, bought.quantity)
for shorted in portfolio.shorted:
    client.trade(shorted.symbol, ita.Action.cover, shorted.quantity)

status = client.get_portfolio_status()
buyingPower = status.buying_power

totalScore = 0
for score in scores:
    totalScore += score

trades = []
for idx, sym in enumerate(symbols):
    proportion = float(scores[idx]) / totalScore
    toSpend = proportion * buyingPower    
    price = ita.get_quote(sym)
    quantity = int(math.floor(toSpend / price))
    if predictions[idx]:
        action = ita.Action.buy
        message = "Bought"
    else:
        action = ita.Action.short
        message = "Shorted"
    client.trade(sym, action, quantity)
    message = message + " " + quantity + " shares of " + sym + "."
    trades.append(message)

response = open(os.environ['res'], 'w')
response.write(json.dumps(trades))
response.close()