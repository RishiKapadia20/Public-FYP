#!/usr/bin/env python3

from influxdb import InfluxDBClient, DataFrameClient
import json
import datetime
from time import mktime


class DBHandler:
    def __init__(self, host, port, user, password, dbname):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname

    def DataFrameToDB(self, df, company):
        client = DataFrameClient(
            self.host, self.port, self.user, self.password, self.dbname
        )

        client.write_points(df, company, protocol="json")

    def QueryDataFromTable(self, query):
        client = InfluxDBClient(
            self.host, self.port, self.user, self.password, self.dbname
        )

        result = client.query(query)

        output = json.dumps(result.raw)
        output = json.loads(output)
        output = output["series"][0]["values"]

        return output

    def GetRowFromTable(self, ticker, time):
        time = mktime(datetime.datetime.strptime(time, "%Y-%m-%d").timetuple())
        str_time = "{:f}".format((time) * 1000000000)

        try:
            query = (
                "select Close, Prediction from " + ticker + " where time = " + str_time
            )
            output = self.QueryDataFromTable(query)
        except KeyError:
            str_time = "{:f}".format((time + 3600) * 1000000000)
            query = (
                "select Close, Prediction from " + ticker + " where time = " + str_time
            )
            output = self.QueryDataFromTable(query)

        return output

    def GetMeasurements(self):
        client = InfluxDBClient(
            self.host, self.port, self.user, self.password, self.dbname
        )

        dbs = client.get_list_measurements()

        return dbs
