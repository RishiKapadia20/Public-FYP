#!/usr/bin/env python3

from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import urllib.request, json
import os
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM

api_key = "BY8JL5USPR4S629O"

ticker = "AAL"

# JSON file with all the stock market data for AAL from the last 20 years
url_string = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&outputsize=full&apikey=%s"%(ticker,api_key)

# Save data to this file
file_to_save = 'stock_market_data-%s.csv'%ticker

# If you haven't already saved data,
# Go ahead and grab the data from the url
# And store date, low, high, volume, close, open values to a Pandas DataFrame
if not os.path.exists(file_to_save):
    with urllib.request.urlopen(url_string) as url:
        data = json.loads(url.read().decode())
        # extract stock market data
        data = data['Time Series (Daily)']
        df = pd.DataFrame(columns=['Date','Low','High','Close','Open'])
        for k,v in data.items():
            date = dt.datetime.strptime(k, '%Y-%m-%d')
            data_row = [date.date(),float(v['3. low']),float(v['2. high']),
                        float(v['4. close']),float(v['1. open'])]            
    print('Data saved to : %s'%file_to_save)        
    df.to_csv(file_to_save)

# If the data is already there, just load it from the CSV
else:
    print('File already exists. Loading data from CSV')
    df = pd.read_csv(file_to_save)

df['Date'] = pd.to_datetime(df.Date,format='%Y-%m-%d')
df.index = df['Date']

df = df.sort_values('Date')

# plt.figure(figsize=(16,8))
# plt.plot(df['Close'], label='Close Price history')
# plt.show()

# print(df.head())
# print(df.info())

df.drop(['Date','Open','Low','High','Unnamed: 0'],inplace=True,axis=1)



# print(df.info())


#creating train and test sets
dataset = df.values

train = dataset[0:2500,:]
valid = dataset[2500:,:]

#converting dataset into x_train and y_train
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

x_train, y_train = [], []
for i in range(60,len(train)):
    x_train.append(scaled_data[i-60:i,0])
    y_train.append(scaled_data[i,0])
x_train, y_train = np.array(x_train), np.array(y_train)

x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))

print(1)

# create and fit the LSTM network
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
model.add(LSTM(units=50))
model.add(Dense(1))
print(2)

model.compile(loss='mean_squared_error', optimizer='adam')
print(3)
model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)
# model.save("model.h5", overwrite=True, include_optimizer=True)
print(4)
inputs = df[len(df) - len(valid) - 60:].values

for i in range(2):
    #using past 60 from the train data
    
    inputs = np.vstack([inputs,0])    

    inputs_trans = inputs.reshape(-1,1)
    inputs_trans  = scaler.transform(inputs_trans)    

    X_test = []

    #iterate starting from 60 since we are using 60 values from training dataset to input.shape[0] is the size of out training data
    for i in range(60,inputs_trans.shape[0]):    
        X_test.append(inputs_trans[i-60:i,0])

    X_test = np.array(X_test)

    X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))

    closing_price = model.predict(X_test)
    closing_price = scaler.inverse_transform(closing_price)


    leng = len(inputs)-1
    # print(leng)

    inputs = np.delete(inputs,(leng),axis=0)    

    inputs = np.vstack([inputs,closing_price[-1]])
    


    # closing_price = np.vstack([closing_price,0])

print(closing_price)
# print(inputs)
print(len(inputs))
print(len(closing_price))

# rms=np.sqrt(np.mean(np.power((valid-closing_price),2)))

# print(rms)

ts = pd.to_datetime("2019-01-16",format='%Y-%m-%d')
new_row = pd.DataFrame([[None]], columns = ["Close"], index=[ts])
df = pd.concat([df, pd.DataFrame(new_row)], ignore_index=False)

ts = pd.to_datetime("2019-01-17",format='%Y-%m-%d')
new_row = pd.DataFrame([[None]], columns = ["Close"], index=[ts])
df = pd.concat([df, pd.DataFrame(new_row)], ignore_index=False)


train = df[:2500]
valid = df[2500:]

valid['Predictions'] = closing_price


plt.plot(train['Close'])
plt.plot(valid[['Close','Predictions']])
plt.show()

print(valid)