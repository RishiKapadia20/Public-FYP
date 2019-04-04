from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, LSTM
import numpy as np


class Model:
    def __init__(self, scaler):
        self.scaler = scaler

    def create_model(self, x_train, y_train):
        model = Sequential()
        model.add(
            LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1))
        )
        model.add(LSTM(units=50))
        model.add(Dense(1))
        model.compile(loss="mean_squared_error", optimizer="adam")
        model.fit(x_train, y_train, epochs=200, batch_size=1, verbose=2)

        return model

    def save_model(self, model, model_name):
        model.save(model_name + ".h5", overwrite=True, include_optimizer=True)

    def load_model(self, model_name):
        model = load_model(model_name + ".h5")

        return model

    def predict(self, df, valid, model, days):
        inputs = df[len(df) - len(valid) - 60 :].values
        for i in range(days):
            # using past 60 from the train data

            inputs = np.vstack([inputs, 0])
            # print(inputs)

            inputs_trans = inputs.reshape(-1, 1)
            inputs_trans = self.scaler.transform(inputs_trans)

            X_test = []

            # iterate starting from 60 since we are using 60 values from training dataset to input.shape[0] is the size of out training data
            for i in range(60, inputs_trans.shape[0]):
                X_test.append(inputs_trans[i - 60 : i, 0])

            X_test = np.array(X_test)

            X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

            closing_price = model.predict(X_test)
            closing_price = self.scaler.inverse_transform(closing_price)

            leng = len(inputs) - 1
            # print(leng)

            inputs = np.delete(inputs, (leng), axis=0)

            inputs = np.vstack([inputs, closing_price[-1]])

        return closing_price

