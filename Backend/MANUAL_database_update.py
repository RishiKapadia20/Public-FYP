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
from pandas.io.json import json_normalize

host = "localhost"
port = 8086
user = None
password = None
dbname = "mydb"

db = DBHandler(host, port, user, password, dbname)

dl = DataLoader()

status = False

i = 1

ticker = "JPM"

output = db.QueryDataFromTable("select * from " + ticker)

df = dl.db_to_df(output)

print(df)

# time = df.tail(1).index[0]

# new_data = dl.get_historical_data("AAL", outputsize="compact")

# while status is False:
#     instance = new_data.iloc[-i]

#     if instance.name == time:
#         status = True
#     else:
#         print(instance)

#         data = [[instance.name, instance[0], 0.0, 0.0, 0.0]]
#         df = pd.DataFrame(
#             data, columns=["Date", "Close", "Polarity", "Prediction", "Subjectivity"]
#         )

#         df["Date"] = pd.to_datetime(df.Date, format="%Y-%m-%d")
#         df.index = df["Date"]
#         df.drop(["Date"], inplace=True, axis=1)

#         db.DataFrameToDB(df, "AAL")
#         i += 1
