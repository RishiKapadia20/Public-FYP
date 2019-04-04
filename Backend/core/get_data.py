import urllib.request, json
import pandas as pd
import os
import datetime as dt
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from alpha_vantage.timeseries import TimeSeries


class DataLoader:

    scaler = MinMaxScaler(feature_range=(0, 1))

    api_key = "<Alpha Vantage API KEY>"

    def get_historical_data(self, ticker, outputsize="full"):
        ts = TimeSeries(key=self.api_key, output_format="pandas")
        data, test = ts.get_daily(symbol=ticker, outputsize=outputsize)

        data.drop(["1. open", "2. high", "3. low", "5. volume"], inplace=True, axis=1)
        # data.drop(["3. low", "5. volume"], inplace=True, axis=1)

        # data.columns = ["Open", "High", "Close"]
        data.columns = ["Close"]

        data.index = pd.to_datetime(data.index)

        return data

    def initalise_database_scheme(self, df):
        df["Prediction"] = 0.00
        df["Polarity"] = 0.00
        df["Subjectivity"] = 0.00

        return df

    def get_current_price(self, ticker):
        ts = TimeSeries(key=self.api_key)
        data, _ = ts.get_intraday(symbol=ticker, interval="1min", outputsize="compact")

        most_recent_time = list(data.keys())[0]

        current_price = data[most_recent_time]

        return current_price

    def split_data(self, df):
        dataset = df.values

        train = dataset[0:2500, :]
        valid = dataset[2500:, :]

        return dataset, train, valid

    def get_train_data(self, df):
        dataset, train, _ = self.split_data(df)
        # converting dataset into x_train and y_train
        scaler = self.scaler
        scaled_data = scaler.fit_transform(dataset)

        x_train, y_train = [], []
        for i in range(60, len(train)):
            x_train.append(scaled_data[i - 60 : i, 0])
            y_train.append(scaled_data[i, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)

        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        return x_train, y_train

    def df_to_array(self, df, column, number):

        outcome = df.tail(number)

        timestamp = outcome.index.tolist()
        prediction = outcome[column].values.tolist()

        alist = []
        listoflist = []

        for i in range(len(timestamp)):
            alist.append(str(timestamp[i]))
            alist.append(prediction[i])
            listoflist.append(alist)
            alist = []

        return listoflist

    def df_to_dic(self, df, number):

        outcome = df.tail(number)

        timestamp = outcome.index.tolist()
        prediction = outcome["Prediction"].values.tolist()

        stocks = dict()

        for i in range(len(timestamp)):
            stocks[i] = {"date": str(timestamp[i]), "prediction": prediction[i]}

        return stocks

    def df_append_future(self, df, days):

        for _ in range(days):

            isWeekday = False
            day = 1

            while isWeekday is False:

                last_day = df.tail(1).index[0]
                next_day = last_day + dt.timedelta(days=day)
                day += 1

                if next_day.weekday() <= 4:
                    isWeekday = True

            new_row = pd.DataFrame([[0.00]], columns=["Close"], index=[next_day])
            df = pd.concat([df, pd.DataFrame(new_row)], ignore_index=False)

        return df

    def db_to_df(self, query_output):
        df = pd.DataFrame(
            columns=["Date", "Close", "Polarity", "Prediction", "Subjectivity"]
        )
        df = df.fillna(0)

        for i in query_output:
            df2 = pd.DataFrame(
                [i], columns=["Date", "Close", "Polarity", "Prediction", "Subjectivity"]
            )

            df = df.append(df2)

        df["Date"] = pd.to_datetime(df.Date, format="%Y-%m-%d")
        df.index = df["Date"]
        df.drop(["Date"], inplace=True, axis=1)

        return df

    def df_to_csv(self, df, file_name):
        df.to_csv(file_name)

    def csv_to_df(self, file_name):
        df = pd.read_csv(file_name)
        df["Date"] = pd.to_datetime(df.Date, format="%Y-%m-%d")
        df.index = df["Date"]
        df.drop(["Date"], inplace=True, axis=1)

        return df


##Old Code

# def get_df(self, ticker):
#     api_key = "BY8JL5USPR4S629O"

#     # JSON file with all the stock market data for AAL from the last 20 years
#     url_string = (
#         "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&outputsize=full&apikey=%s"
#         % (ticker, api_key)
#     )

#     # Save data to this file
#     file_to_save = "stock_market_data-%s.csv" % ticker

#     # If you haven't already saved data,
#     # Go ahead and grab the data from the url
#     # And store date, low, high, volume, close, open values to a Pandas DataFrame
#     if not os.path.exists(file_to_save):
#         with urllib.request.urlopen(url_string) as url:
#             data = json.loads(url.read().decode())
#             # extract stock market data
#             data = data["Time Series (Daily)"]
#             df = pd.DataFrame(columns=["Date", "Low", "High", "Close", "Open"])
#             for k, v in data.items():
#                 date = dt.datetime.strptime(k, "%Y-%m-%d")
#                 data_row = [
#                     date.date(),
#                     float(v["3. low"]),
#                     float(v["2. high"]),
#                     float(v["4. close"]),
#                     float(v["1. open"]),
#                 ]
#         print("Data saved to : %s" % file_to_save)
#         df.to_csv(file_to_save)

#     # If the data is already there, just load it from the CSV
#     else:
#         print("File already exists. Loading data from CSV")
#         df = pd.read_csv(file_to_save)

#     df["Date"] = pd.to_datetime(df.Date, format="%Y-%m-%d")
#     df.index = df["Date"]

#     df = df.sort_values("Date")

#     df.drop(["Date", "Open", "Low", "High", "Unnamed: 0"], inplace=True, axis=1)

#     return df
