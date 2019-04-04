#!/usr/bin/env python3

from influxdb import InfluxDBClient, DataFrameClient
from alpha_vantage.timeseries import TimeSeries
from core.get_data import DataLoader
import json
import pandas as pd
from datetime import datetime
from core.get_data import DataLoader

host = "localhost"
port = 8086
user = None
password = None
dbname = "mydb"

dl = DataLoader()

api_key = "BY8JL5USPR4S629O"

# client = DataFrameClient(host, port, user, password, dbname)

client = InfluxDBClient(host, port, user, password, dbname)

dbs = client.get_list_measurements()


# result = client2.query("select * from AAPL where Close = 0 and time < now() - 1d")

# output = json.dumps(result.raw)
# output = json.loads(output)
# output = output["series"][0]["values"]

# # print(output)

# for i in output:
#     value = 0
#     time = i[0]
#     prediction = i[2]
#     time = time.replace("T00:00:00Z", "")
#     print(time)

#     ts = TimeSeries(key=api_key, output_format="pandas")
#     data, _ = ts.get_daily(symbol="AAPL", outputsize="compact")

#     data.drop(["1. open", "2. high", "3. low", "5. volume"], inplace=True, axis=1)

#     data.columns = ["Close"]

#     data.index = pd.to_datetime(data.index)

#     array = dl.df_to_array(data, "Close", 10)

#     print(array)

#     for i in array:
#         time2 = i[0]
#         time2 = time2.replace(" 00:00:00", "")
#         print(time2)

#         if time == time2:
#             value = i[1]

#     data = [[time, value, prediction]]
#     df = pd.DataFrame(data, columns=["Date", "Close", "Prediction"])

#     df["Date"] = pd.to_datetime(df.Date, format="%Y-%m-%d")
#     df.index = df["Date"]
#     df.drop(["Date"], inplace=True, axis=1)
#     print(df)

#     client.write_points(df, "AAPL", protocol="json")

# data = [["2019-02-15", 170.42, 178.08921813964844]]
# df = pd.DataFrame(data, columns=["Date", "Close", "Prediction"])

# df["Date"] = pd.to_datetime(df.Date, format="%Y-%m-%d")
# df.index = df["Date"]
# df.drop(["Date"], inplace=True, axis=1)
# print(df)

# client.write_points(df, "AAPL", protocol="json")

# print(df)


# # print(df.info())


# result = client.query("Select Close from AAL where Close > 0")

# output = json.dumps(result.raw)
# output = json.loads(output)
# output = output["series"][0]["values"]

# print(json_normalize(output))


# json_body = [
#     {
#         "measurement": "cpu_load_short",
#         # "tags": {"host": "server01", "region": "us-west"},
#         "time": "2009-11-10T23:00:00Z",
#         "fields": {
#             "Float_value": 0.64,
#             "Int_value": 3,
#             "String_value": "Text",
#             "Bool_value": True,
#         },
#     }
# ]


# ts = TimeSeries(key="BY8JL5USPR4S629O", output_format="pandas")
# data, _ = ts.get_daily(symbol="AAL", outputsize="full")

# data.drop(["1. open", "2. high", "3. low", "5. volume"], inplace=True, axis=1)

# data.columns = ["Close"]

# data.index = pd.to_datetime(data.index)

# print(data)

# print(data.info())

# client.write_points(data, "demo", protocol="json")

