#!/usr/bin/env python3

import pandas as pd
import json
import datetime
from alpha_vantage.timeseries import TimeSeries
from keras import backend as keras
from time import mktime
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, LSTM
import numpy as np
from numpy import concatenate
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot
from math import sqrt
import time

# import plotly.graph_objs as go
# import plotly.offline as py
# import seaborn as sns


def get_historical_data(api_key, ticker, outputsize="full"):
    ts = TimeSeries(key=api_key, output_format="pandas")
    data, test = ts.get_daily(symbol=ticker, outputsize=outputsize)

    #         data.drop(["1. open", "2. high", "3. low", "5. volume"], inplace=True, axis=1)

    #         data.columns = ["Close"]

    data.index = pd.to_datetime(data.index)

    # print(data)

    return data


def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [("var%d(t-%d)" % (j + 1, i)) for j in range(n_vars)]
        print(i)
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [("var%d(t)" % (j + 1)) for j in range(n_vars)]
        else:
            names += [("var%d(t+%d)" % (j + 1, i)) for j in range(n_vars)]
    # put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg


api_key = "BY8JL5USPR4S629O"

data = get_historical_data(api_key, "AAL")

values = data[["4. close"] + ["1. open"] + ["2. high"]].values
values = values.astype("float32")

# print(values)

scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(values)

# print(scaled)

reframed = series_to_supervised(scaled, 1, 3)


reframed.drop(
    ["var2(t)", "var2(t+1)", "var2(t+2)", "var3(t)", "var3(t+1)", "var3(t+2)"],
    axis=1,
    inplace=True,
)
print(reframed.info())
print(reframed.head())

# print(reframed.head())

values = reframed.values
n_train_hours = int(len(values) * 0.7)
train = values[:n_train_hours, :]
test = values[n_train_hours:, :]

# split into input and outputs
train_X, train_y = train[:, :-3], train[:, -3:]
print(train_X)
print(train_y)
test_X, test_y = test[:, :-3], test[:, -3:]
# reshape input to be 3D [samples, timesteps, features]
train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)
