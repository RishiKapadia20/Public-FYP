#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from core.get_data import DataLoader
from core.data_processing import DataProcessing
from alpha_vantage.timeseries import TimeSeries
from core.model import Model
from dbhelper.db_handler import DBHandler
from keras import backend as keras
import pandas as pd
import json
from flask_cors import CORS
from sentiment_analysis import sentiment
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)
CORS(app)
api = Api(app)

dl = DataLoader()
md = Model(dl.scaler)
sentiment = sentiment()
dp = DataProcessing()

host = "localhost"
port = 8086
user = None
password = None
dbname = "mydb2"

db = DBHandler(host, port, user, password, dbname)

x = {
    "Companies": [
        {"Name": "American Airline", "Symbol": "AAL"},
        {"Name": "JPMorgan Chase", "Symbol": "JPM"},
    ]
}


class index(Resource):
    def get(self):
        return {"status": "API is running"}


class get_current_price(Resource):
    def get(self, company):
        current_price = dl.get_current_price(company)
        return current_price


class get_company_data(Resource):
    def get(self, company, period):
        query = "Select Close from " + company + " where Close > 0"
        if period == "1Week":
            query = query + " and time > now() - 8d"
        elif period == "2Week":
            query = query + " and time > now() - 15d"
        elif period == "1Month":
            query = query + " and time > now() - 31d"
        elif period == "1Year":
            query = query + " and time > now() - 365d"

        for _ in range(2):
            try:
                data = db.QueryDataFromTable(query)
                break
            except:
                df = dl.get_historical_data(company)
                df = dl.initalise_database_scheme(df)
                db.DataFrameToDB(df, company)
        return data


# class create_model(Resource):
#     def get(self, company):
#         df = dl.get_historical_data(company)

#         x_train, y_train = dl.get_train_data(df)

#         model = md.create_model(x_train, y_train)

#         md.save_model(model, "test-rest3-model")

#         keras.clear_session()

#         return {"Status": "OK"}, 200


# class predict_prices(Resource):
#     def get(self, company, prediction_days):

#         df = dl.get_historical_data(company)

#         _, _, valid = dl.split_data(df)

#         # dependant on running since it sets up MinMaxScaler used in the predict method
#         _, _ = dl.get_train_data(df)

#         model = md.load_model(company + "-model")

#         closing_price = md.predict(df, valid, model, prediction_days)

#         df = dl.df_append_future(df, prediction_days)

#         valid = df[2500:]

#         valid["Prediction"] = closing_price

#         # dic = dl.df_to_dic(valid, prediction_days)

#         output_df = valid.tail(prediction_days)

#         output_df["Polarity"] = 0.0

#         output_df["Subjectivity"] = 0.0

#         db.DataFrameToDB(output_df, company)

#         keras.clear_session()

#         return {"Status": "OK"}, 200


class predict_prices(Resource):
    def get(self, company):

        # data = dl.get_historical_data(company)

        # values = data[["Close"] + ["Open"] + ["High"]].values
        # values = values.astype("float32")

        data = db.QueryDataFromTable("select * from " + company)
        data = dl.db_to_df(data)

        values = data[["Close"] + ["Polarity"]].values
        values = values.astype("float32")

        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled = scaler.fit_transform(values)

        _, last = dp.series_to_supervised(scaled, 5, 5)

        drop_array = dp.create_drop_array(2, 5)

        last.drop(drop_array, axis=1, inplace=True)

        last_values = last.values

        predict_X = last_values[:, :-5]

        predict_X = predict_X.reshape((predict_X.shape[0], 1, predict_X.shape[1]))

        model = md.load_model(company + "-model")
        # model = md.load_model("test")

        output = model.predict(predict_X)

        prediction = dp.inverse_transform(scaler, output)

        prediction = prediction[-1]

        df = dl.df_append_future(data, 5)
        future_days = df.tail(5).index.values

        df = pd.DataFrame(
            columns=["Date", "Close", "Polarity", "Prediction", "Subjectivity"]
        )
        df = df.fillna(0)

        for i in range(5):
            df2 = pd.DataFrame(
                [[future_days[i], 0.0, 0.0, prediction[i], 0.0]],
                columns=["Date", "Close", "Polarity", "Prediction", "Subjectivity"],
            )
            df = df.append(df2)

        df["Date"] = pd.to_datetime(df.Date, format="%Y-%m-%d")
        df.index = df["Date"]
        df.drop(["Date"], inplace=True, axis=1)

        db.DataFrameToDB(df, company)

        keras.clear_session()

        return {"Status": "OK"}, 200


class get_prediction_prices(Resource):
    def get(self, company):
        data = db.QueryDataFromTable(
            "select Prediction from " + company + " where Prediction > 0"
        )

        return data


class refreshdb(Resource):
    def get(self, company):
        try:
            output = db.QueryDataFromTable(
                "select * from " + company + " where Close = 0 and time < now()"
            )
        except KeyError:
            output = []

        for i in output:
            value = 0.0
            time = i[0]
            polarity = float(i[2])
            prediction = float(i[3])
            subjectivity = float(i[4])

            time = time.replace("T00:00:00Z", "")

            data = dl.get_historical_data(company, "compact")

            array = dl.df_to_array(data, "Close", 10)

            for i in array:
                time2 = i[0]
                time2 = time2.replace(" 00:00:00", "")

                if time == time2:
                    value = i[1]

            data = [[time, value, polarity, prediction, subjectivity]]
            df = pd.DataFrame(
                data,
                columns=["Date", "Close", "Polarity", "Prediction", "Subjectivity"],
            )

            df["Date"] = pd.to_datetime(df.Date, format="%Y-%m-%d")
            df.index = df["Date"]
            df.drop(["Date"], inplace=True, axis=1)

            db.DataFrameToDB(df, company)

        status = False

        i = 1

        output = db.QueryDataFromTable("select * from " + company)

        df = dl.db_to_df(output)

        time = df.tail(1).index[0]

        new_data = dl.get_historical_data(company, outputsize="compact")

        while status is False:
            instance = new_data.iloc[-i]

            if instance.name == time:
                status = True
            else:
                print(instance)

                data = [[instance.name, instance[0], 0.0, 0.0, 0.0]]
                df = pd.DataFrame(
                    data,
                    columns=["Date", "Close", "Polarity", "Prediction", "Subjectivity"],
                )

                df["Date"] = pd.to_datetime(df.Date, format="%Y-%m-%d")
                df.index = df["Date"]
                df.drop(["Date"], inplace=True, axis=1)

                db.DataFrameToDB(df, company)
                i += 1

        return {"Status": "OK"}, 200


# class get_measurements(Resource):
#     def get(self):
#         return db.GetMeasurements()


class get_measurements(Resource):
    def get(self):
        return x


class initalise_sentiment(Resource):
    def get(self, ticker, company):
        # 2018-06-08
        # 2018-08-06
        # 2019-02-21
        # 2016-07-12
        # 2017-02-10
        # 2017-06-08
        sentiment.get_sentiment(ticker, company, "2019-02-21")
        return {"Status": "OK"}, 200


class TEST_db_data(Resource):
    def get(self, company, period):
        query = "Select * from " + company + " where"
        if period == "1Week":
            query = query + " time > now() - 8d"
        elif period == "2Week":
            query = query + " time > now() - 15d"
        elif period == "1Month":
            query = query + " time > now() - 31d"
        elif period == "1Year":
            query = query + " time > now() - 365d"

        for _ in range(2):
            try:
                data = db.QueryDataFromTable(query)
                break
            except:
                df = dl.get_historical_data(company)
                df = dl.initalise_database_scheme(df)
                db.DataFrameToDB(df, company)
        return data


api.add_resource(index, "/")


api.add_resource(predict_prices, "/predict_prices/<string:company>")
api.add_resource(get_current_price, "/current_price/<string:company>")
api.add_resource(get_company_data, "/company_data/<string:company>/<string:period>")
api.add_resource(get_prediction_prices, "/get_predict_price/<string:company>")
api.add_resource(refreshdb, "/refreshdb/<string:company>")
api.add_resource(get_measurements, "/get_measurements")
api.add_resource(
    initalise_sentiment, "/initalise_sentiment/<string:ticker>/<string:company>"
)


api.add_resource(TEST_db_data, "/TEST_db_data/<string:company>/<string:period>")

# api.add_resource(create_model, "/create_model/<string:company>")
if __name__ == "__main__":
    app.run(debug=True)
