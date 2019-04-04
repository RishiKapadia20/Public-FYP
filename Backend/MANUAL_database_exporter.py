#!/usr/bin/env python3


from core.get_data import DataLoader
from core.data_processing import DataProcessing
from alpha_vantage.timeseries import TimeSeries
from core.model import Model
from dbhelper.db_handler import DBHandler
import pandas as pd
import json

dl = DataLoader()
dp = DataProcessing()

host = "localhost"
port = 8086
user = None
password = None
dbname = "mydb2"

db = DBHandler(host, port, user, password, dbname)

output = db.QueryDataFromTable("select * from AAL")


new_output = dl.db_to_df(output)

print(new_output)

dl.df_to_csv(new_output, "AAL.csv")
