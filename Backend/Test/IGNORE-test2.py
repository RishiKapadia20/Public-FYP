#!/usr/bin/env python3

from core.get_data import DataLoader
from core.model import Model
import pandas as pd
import json
import datetime
from alpha_vantage.timeseries import TimeSeries
from dbhelper.db_handler import DBHandler
from keras import backend as keras
from time import mktime
import GetOldTweets3 as got
from textblob import TextBlob


dl = DataLoader()
md = Model(dl.scaler)


host = "localhost"
port = 8086
user = None
password = None
dbname = "mydb"

db = DBHandler(host, port, user, password, dbname)

df = dl.get_historical_data("AAL")

x_train, y_train = dl.get_train_data(df)

model = md.create_model(x_train, y_train)

md.save_model(model, "test-rest3-model")

keras.clear_session()


# future_days = 20

# _ , _ , valid = dl.split_data(df)

# print(type(valid))

# x_train, y_train = dl.get_train_data(df)

# model = md.create_model(x_train,y_train)

# md.save_model(model,"test-model")

# model = md.load_model("test-rest2-model")

# closing_price = md.predict(df,valid,model,future_days)

# print(closing_price)

# ts = pd.to_datetime("2019-01-16",format='%Y-%m-%d')
# new_row = pd.DataFrame([[None]], columns = ["Close"], index=[ts])
# df = pd.concat([df, pd.DataFrame(new_row)], ignore_index=False)

# ts = pd.to_datetime("2019-01-17",format='%Y-%m-%d')
# new_row = pd.DataFrame([[None]], columns = ["Close"], index=[ts])
# df = pd.concat([df, pd.DataFrame(new_row)], ignore_index=False)

# ts = pd.to_datetime("2019-01-18",format='%Y-%m-%d')
# new_row = pd.DataFrame([[None]], columns = ["Close"], index=[ts])
# df = pd.concat([df, pd.DataFrame(new_row)], ignore_index=False)

# df = dl.df_append_future(df,future_days)


# train = df[:2500]
# valid = df[2500:]
# print(valid)

# valid['Predictions'] = closing_price

# dic = dl.df_to_dic(valid,future_days)


# print(dic)

# print(json.dumps(dic))

# print(array)

# print(json.dumps(array))

# last_value = df.tail(1).index
# print(type(last_value))
# next_day = last_value + datetime.timedelta(days=1)
# print(next_day[0])

# # ts = pd.to_datetime(next_day,format='%Y-%m-%d')
# new_row = pd.DataFrame([[None]], columns = ["Close"], index=[next_day[0]])
# df = pd.concat([df, pd.DataFrame(new_row)], ignore_index=False)

# valid = df[2500:]
# print(valid)


# data = [["2019-02-13", 10], ["2019-02-14", 12], ["2019-02-15", 13]]
# df = pd.DataFrame(data, columns=["Date", "Close"])
# print(df)

# df["Date"] = pd.to_datetime(df.Date, format="%Y-%m-%d")
# df.index = df["Date"]
# df.drop(["Date"], inplace=True, axis=1)

# print(df.info())

# df = dl.get_historical_data("AAL")
# df = dl.initalise_database_scheme(df)
# db.DataFrameToDB(df, "Test2")

# prediction_days = 10

# df = dl.get_historical_data("AAL")

# _, _, valid = dl.split_data(df)

# # dependant on running since it sets up MinMaxScaler used in the predict method
# _, _ = dl.get_train_data(df)

# model = md.load_model("test-rest2-model")

# closing_price = md.predict(df, valid, model, prediction_days)

# df = dl.df_append_future(df, prediction_days)

# valid = df[2500:]

# valid["Prediction"] = closing_price

# # dic = dl.df_to_dic(valid, prediction_days)

# output_df = valid.tail(prediction_days)

# db.DataFrameToDB(output_df, "Test2")

# keras.clear_session()


# db.DataFrameToDB(df, "Test")


# host = "localhost"
# port = 8086
# user = None
# password = None
# dbname = "mydb"

# db = DBHandler(host, port, user, password, dbname)

# dl = DataLoader()

