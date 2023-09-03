import pandas as pd
import yfinance as yf
import datetime
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers
from pytz import timezone

def df_to_windowed_df(dataframe, first_date, last_date, n=5):
    # Convert dates to naive datetime objects if they aren't already
    if not isinstance(first_date, datetime.datetime):
        first_date = first_date.to_pydatetime()

    if not isinstance(last_date, datetime.datetime):
        last_date = last_date.to_pydatetime()

    # Remove time zone information to make them naive
    first_date = first_date.replace(tzinfo=None)
    last_date = last_date.replace(tzinfo=None)
    
    target_date = first_date

    dates = []
    X, Y = [], []

    last_time = False
    while True:
        df_subset = dataframe.loc[:target_date].tail(n+1)

        if len(df_subset) != n+1:
            print(f'Error: Window of size {n} is too large for date {target_date}')
            return

        values = df_subset['Close'].to_numpy()
        x, y = values[:-1], values[-1]

        dates.append(target_date)
        X.append(x)
        Y.append(y)

        # Get the next date for which you have data
        next_date = target_date + datetime.timedelta(days=1)
        
        if last_time:
            break

        target_date = next_date

        if target_date >= last_date:
            last_time = True

    ret_df = pd.DataFrame({})
    ret_df['Target Date'] = dates

    X = np.array(X)
    for i in range(0, n):
        ret_df[f'Target-{n-i}'] = X[:, i]

    ret_df['Target'] = Y

    return ret_df


def windowed_df_to_date_X_y(windowed_dataframe):
    df_as_np = windowed_dataframe.to_numpy()

    dates = df_as_np[:, 0]

    middle_matrix = df_as_np[:, 1:-1]
    X = middle_matrix.reshape((len(dates), middle_matrix.shape[1], 1))

    Y = df_as_np[:, -1]

    return dates, X.astype(np.float32), Y.astype(np.float32)


def str_to_datetime(s):
    split = s.split('-')
    year, month, day = int(split[0]), int(split[1]), int(split[2])
    return datetime.datetime(year=year, month=month, day=day)


def lstmModel(ticker):
    def cleanUpData(data):
        data = data[['Close']]
        # data['Date'] = data['Date'].apply(str_to_datetime)
        return data

    data = cleanUpData(yf.Ticker(ticker).history('1y'))
    data.index = data.index.tz_localize(None)



    first_date_str = data.index[5]
    last_date_str = data.index[-1]
    windowedData = df_to_windowed_df(data, first_date_str, last_date_str)
    dates, X, y = windowed_df_to_date_X_y(windowedData)
    q_80 = int(len(dates) * .8)
    q_90 = int(len(dates) * .9)

    dates_train, X_train, y_train = dates[:q_80], X[:q_80], y[:q_80]
    dates_val, X_val, y_val = dates[q_80:q_90], X[q_80:q_90], y[q_80:q_90]
    dates_test, X_test, y_test = dates[q_90:], X[q_90:], y[q_90:]

    model = Sequential([layers.Input((5, 1)),
                        layers.LSTM(64),
                        layers.Dense(32, activation='relu'),
                        layers.Dense(32, activation='relu'),
                        layers.Dense(1)])

    model.compile(loss='mse',
                  optimizer=Adam(learning_rate=0.001),
                  metrics=['mean_absolute_error'])

    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=100)

    return model


        
def createModels():

    def make_predictions(models):
       def next_five_market_days(start_date):
        start_date = pd.Timestamp(start_date)
    
        all_dates = pd.date_range(start_date, periods=10, freq='B')
    
        next_5_days = all_dates[1:6]
    
        return next_5_days

        for ticker, model in models.items():
            data = yf.Ticker(ticker).history('5d')
            first_date = data.index[0]
            data = data['Close'].values

            data = data.reshape(1, 5, 1)
            five_day_predictions = []

            for i in range(5):  # Step 4: Repeat 5 times for 5 days
                 # Step 2: Make a prediction for the next day
                next_day_prediction = model.predict(data)[0, 0]

                 # Append the prediction to the list
                five_day_predictions.append(next_day_prediction)

                 # Step 3: Update the window
                new_data_window = np.roll(data, shift=-1, axis=1)  # Shift the data window
                new_data_window[0, -1, 0] = next_day_prediction  # Insert the new prediction as the newest day
                data = new_data_window  # Update the data window for the next iteration

            five_day_predictions = [float(x) for x in five_day_predictions]
       
        print('~~~~~~~~~~~~~~')
        print(next_five_market_days(first_date))
        print('~~~~~~~~~~~~~~')
        predictions = {}



            

    aaplModel = lstmModel('AAPL')
    kolModel = lstmModel('KO')
    jpmModel = lstmModel('JPM')

    models = {'AAPL': aaplModel, 'JPM': jpmModel, 'KO': kolModel}

    make_predictions(models)

    return models
