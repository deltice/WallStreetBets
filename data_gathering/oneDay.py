# gather post data from past 24 hours

import praw
import csv
import json
from credentials import credentials
from stockSymbols import symbols

reddit = praw.Reddit(client_id=credentials["client"],
					 client_secret=credentials["secret"],
					 username=credentials["username"],
					 password=credentials["password"],
					 user_agent="test script")

subreddit = reddit.subreddit('wallstreetbets')

stocks = {}
for submission in subreddit.top('day'):
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

posts = []
for stock in stocks:
	(text, score) = stocks[stock]
	posts.append(text)
	print(stock)
	print(score)

file = open('onedayposts.json', 'w')
file.write(json.dumps(posts))

# [true,false,false,false,false,false,false,true,false,false]
