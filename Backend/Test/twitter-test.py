#!/usr/bin/env python3

from core.get_data import DataLoader
import pandas as pd
import json
import datetime
from alpha_vantage.timeseries import TimeSeries
from dbhelper.db_handler import DBHandler
from time import mktime
import GetOldTweets3 as got
from textblob import TextBlob


dl = DataLoader()

company = "American Airlines"
time = "2012-09-06"
next_day = "2012-09-07"


tweetCriteria = (
    got.manager.TweetCriteria()
    .setQuerySearch(company)
    .setSince(time)
    .setUntil(next_day)
    .setMaxTweets(1)
)

tweets = got.manager.TweetManager.getTweets(tweetCriteria)
print(tweets)
# data = dict()
# j = 0

for tweet in tweets:
    print(tweet.text)
#     if "http" not in tweet.text:
#         analysis = TextBlob(tweet.text)
#         print(tweet.text)
#         print(analysis.sentiment.polarity)
#         data[j] = {
#             "polarity": analysis.sentiment.polarity,
#             "subjectivity": analysis.sentiment.subjectivity,
#         }
#         j += 1
# polarity_total = 0
# subjectivity_total = 0
# invalid_data_counter = 0
# for index in data:
#     if data[index]["polarity"] == 0 or data[index]["subjectivity"] == 0:
#         invalid_data_counter += 1

#     if invalid_data_counter == len(data):
#         avg_polarity = 0.0
#         avg_subjectivity = 0.0
#     else:
#         polarity_total = polarity_total + data[index]["polarity"]
#         subjectivity_total = subjectivity_total + data[index]["subjectivity"]

# avg_polarity = polarity_total / (len(data) - invalid_data_counter)

# print(avg_polarity)

# print((len(data) - invalid_data_counter))
