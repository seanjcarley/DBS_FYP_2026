import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pmdarima as pm
import datetime as dt
from MachineLearning import MachineLearning

class TimeSeries(MachineLearning):

    # ['year', 'month', 'day', 'dow', 'woy', 'hour', 'event', 'direction', 'epoch']
    def __init__ (self, ml_array, columns=['epoch'], 
        ml_type='Time Series Analysis'):
        super().__init__(ml_array, columns)
        self.ml_type = ml_type
        self.periods = 0
        self.dates_n = []
        self.dates_s = []
        self.df_n = None
        self.df_s = None
        self.z_n = None
        self.z_s = None
        self.model_n = None
        self.train_n = None
        self.test_n = None
        self.model_s = None
        self.train_s = None
        self.test_s = None
        

    def num_str(self, num):
        ''' 
            take in integer (num) and converts it to a string to be used to 
            create a datatime object. also adds a leading '0' if the value is 
            less than 10.
        '''
        if num < 10:  # add a leading 0 if int < 10
            str_num = '0' + str(num)
        else:
            str_num = str(num)

        return str_num

    def get_data_frame(self):
        ''' 
            create a datetime object and add it, along with the corresponding  
            count value, to a list to be used to create the data frames
        '''
        for i in self.ml_array:
            if i[0] >= 2024:
                i_date = f'{self.num_str(i[0])}-{self.num_str(i[1])}-{self.num_str(i[2])} {self.num_str(i[5])}:00'
                date_time = dt.datetime.strptime(i_date, '%Y-%m-%d %H:%M')
                if i[7] == 0:
                    if date_time not in self.dates_n:
                        self.dates_n.append([date_time, i[8]])
                if i[7] == 4:
                    if date_time not in self.dates_s:
                        self.dates_s.append([date_time, i[8]])

        self.df_n = pd.DataFrame(self.dates_n, columns=['Date', 'Count'])
        self.df_s = pd.DataFrame(self.dates_s, columns=['Date', 'Count'])


    def get_z_score(self):
        ''' 
            get the z-score to identify extreme values relative to the 
            mean/std. Replace any values with a z-score > 3 with the series 
            median
        '''
        self.z_n = np.abs(
            (self.df_n.Count - self.df_n.Count.mean())/self.df_n.Count.std())
        # print(self.z_n)
        self.df_n['Count_clean'] = np.where(
            self.z_n > 3, self.df_n.Count.median(), self.df_n.Count)
        self.z_s = np.abs(
            (self.df_s.Count - self.df_s.Count.mean())/self.df_s.Count.std())
        # print(self.z_s)
        self.df_s['Count_clean'] = np.where(
            self.z_s > 3, self.df_s.Count.median(), self.df_s.Count)


    def adfuller(self):
        self.get_z_score()
        adf_n = adfuller(self.df_n.Count_clean, result_object=True)
        adf_s = adfuller(self.df_s.Count_clean, result_object=True)
        print('North')
        print(f'ADF Statistic: {adf_n[0]}')
        print(f'p-value: {adf_n[1]}')
        if adf_n[1] < 0.05:
            print(f'Series is stationary!')
        else:
            print(f'Series is NOT stationary, Differencing Needed!')
        print('South')
        print(f'ADF Statistic: {adf_s[0]}')
        print(f'p-value: {adf_s[1]}')
        if adf_s[1] < 0.05:
            print(f'Series is stationary!')
        else:
            print(f'Series is NOT stationary, Differencing Needed!')

        

        decomp_n = seasonal_decompose(self.df_n.Count_clean.dropna(), 
            model='additive', period=365)
        decomp_n.plot()
        plt.show()
        decomp_s = seasonal_decompose(self.df_s.Count_clean.dropna(), 
            model='additive', period=365)
        decomp_s.plot()
        plt.show()

    def arima(self):
        print(len(self.df_n.Count_clean))
        self.train_n = self.df_n.Count_clean[:-4380]
        self.test_n = self.df_n.Count_clean[-4380:]
        self.model_n = pm.auto_arima(
            self.train_n,
            seasonal=True,
            m=12,
            trace=True,
            error_action='ignore',
            suppress_warnings=True
        )

        self.model_n.summary()

        forecast = self.model_n.predict(n_periods=48)
        forecast = pd.Series(forecast, index=self.test_n.index)
        print(forecast)


    def plot_data(self):
        plt.figure(figsize=(12, 5))
        plt.plot(self.df_n.Count)
        plt.plot(self.df_s.Count)
        plt.title('Time Series Plot')
        plt.xlabel('Date')
        plt.ylabel('Count')
        plt.legend()
        plt.grid(True)
        plt.show()

    