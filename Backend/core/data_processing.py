import pandas as pd
import numpy as np
from numpy import concatenate
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error


class DataProcessing:
    def series_to_supervised(self, data, n_in=1, n_out=1, dropnan=True):
        n_vars = 1 if type(data) is list else data.shape[1]
        df = pd.DataFrame(data)
        cols, names = list(), list()
        # input sequence (t-n, ... t-1)
        for i in range(n_in, 0, -1):
            cols.append(df.shift(i))
            names += [("var%d(t-%d)" % (j + 1, i)) for j in range(n_vars)]
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
            last = agg.tail(100)
            agg.dropna(inplace=True)
        return agg, last

    def create_drop_array(self, n_variables, n_out):
        array = []

        for i in range(2, n_variables + 1):
            for j in range(0, n_out):
                if j == 0:
                    row = "var" + str(i) + "(t)"
                else:
                    row = "var" + str(i) + "(t+" + str(j) + ")"
                array.append(row)
        return array

    def inverse_transform(self, scaler, data):
        data_1 = data[:, :2]
        data_2 = data[:, 1:3]
        data_3 = data[:, 2:4]
        data_4 = data[:, 3:5]
        data_5 = concatenate((data[:, 4:], data[:, 4:]), axis=1)

        inv_data_1 = scaler.inverse_transform(data_1)
        inv_data_2 = scaler.inverse_transform(data_2)
        inv_data_3 = scaler.inverse_transform(data_3)
        inv_data_4 = scaler.inverse_transform(data_4)
        inv_data_5 = scaler.inverse_transform(data_5)

        inv_data = concatenate(
            (
                inv_data_1[:, :1],
                inv_data_2[:, :1],
                inv_data_3[:, :1],
                inv_data_4[:, :1],
                inv_data_5[:, :1],
            ),
            axis=1,
        )

        return inv_data
