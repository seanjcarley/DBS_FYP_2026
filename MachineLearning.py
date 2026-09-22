import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics

class MachineLearning:
    ''' parent class for machine learning algorithms '''

    def __init__(self, ml_array, columns):
        self.ml_array = ml_array
        self.columns = ['year', 'month', 'day', 'dow', 'woy', 
                        'hour', 'event', 'direction', 'count']
        self.drop_columns = []
        self.required_columns = columns
        self.df = None
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.model = None
        self.prediction = None
        self.year = None
        self.month = None
        self.day = None
        self.hour = None


    def get_test_training_dataset(self):

        # create dataframe from ml_array
        self.df = pd.DataFrame(self.ml_array, columns=self.columns)

        # drop the columns that are not being used
        for column in self.columns:
            if column not in self.required_columns:
                self.drop_columns.append(column)

        self.X = self.df.drop(self.drop_columns, axis=1)
        self.y = self.df['count']

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.4, random_state=79)


    def make_prediction(self, y, m, d, dw, wy, h, e, di):

        def num_str(num):
            ''' take in integer and convert it to a string '''
            if int(num) < 10:  # add a leading 0 if int < 10
                str_num = '0' + str(num)
            else:
                str_num = str(num)
    
            return str_num

        self.year = num_str(y)
        self.month = num_str(m)
        self.day = num_str(d)
        self.hour = num_str(h)

        # get the features that are being used for the predictions
        features = []
        for column in self.required_columns:
            match column:
                case 'year':
                    features.append(y)
                case 'month':
                    features.append(m)
                case 'day':
                    features.append(d)
                case 'dow':
                    features.append(dw)
                case 'woy':
                    features.append(wy)
                case 'hour':
                    features.append(h)
                case 'event':
                    features.append(e)
                case 'direction':
                    features.append(di)

        # get the data to be used to make the prediction
        predict_df = pd.DataFrame([features], columns=self.required_columns)
        
        self.prediction = self.model.predict(predict_df)


    def print_test_metrics(self, y_test, predictions):
        print(f'\nUsing {self.ml_type} and K set to {self.neighbors}:')
        print(f'MAE: {metrics.mean_absolute_error(y_test, predictions)}')
        print(f'MSE: {metrics.mean_squared_error(y_test, predictions)}')
        print(f'RMSE: {np.sqrt(metrics.mean_squared_error(y_test, predictions))}')
        print(f'R2 Score: {metrics.r2_score(y_test, predictions)}')
        print(f'Explained Variance: {metrics.explained_variance_score(y_test, predictions)}')


    def print_prediction(self, mtype):
        print(f'\nUsing {mtype}: ')
        print(f'The predicted volume between {self.hour}:00 and {str(int(self.hour) + 1)}:00 on {self.day}/{self.month}/{self.year} is:')
        print(f'\t{int(self.prediction[0])}')
