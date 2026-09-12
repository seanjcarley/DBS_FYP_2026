import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

class LinearReg:
    ''' run Linear Regression learning algorithm '''

    def __init__(self, lr_array):
        self.columns = ['year', 'month', 'day', 'dow', 
                        'hour', 'event', 'direction', 'count']
        self.lr_array = lr_array
        self.df = None
        self.lin_reg = None
        self.X = None
        self.y = None


    def get_training_model(self):
        self.df = pd.DataFrame(self.lr_array, columns=self.columns)

        self.X = self.df.drop(['year', 'month', 'day','count'], axis=1)
        self.y = self.df['count']

        X_train, X_test, y_train, y_test = train_test_split(
                            self.X, self.y, test_size=0.4, random_state=79)

        self.lin_reg = LinearRegression()
        self.lin_reg.fit(X_train, y_train)

        coeff = pd.DataFrame(
             self.lin_reg.coef_, self.X.columns, columns=['Coefficient'])

        predictions = self.lin_reg.predict(X_test)

        self.print_test_metrics(y_test, predictions, coeff)


    def make_prediction(self, y, m, d, dw, h, e, di):
            predict_df = pd.DataFrame([[dw, h, e, di]],
                columns=['dow', 
                         'hour', 'event', 'direction'])
        
            predciction = self.lin_reg.predict(predict_df)    
    
            return predciction


    def print_test_metrics(self, y_test, predictions, coeff):
        print(f'Using the data provided:')
        print(f'Coefficient: {coeff}')
        print(f'MAE: {metrics.mean_absolute_error(y_test, predictions)}')
        print(f'MSE: {metrics.mean_squared_error(y_test, predictions)}')
        print(f'RMSE: {np.sqrt(metrics.mean_squared_error(y_test, predictions))}')
        print(f'Explained Variance: {metrics.explained_variance_score(y_test, predictions)}')
