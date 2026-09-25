import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics

class MachineLearning:
    ''' parent class for machine learning algorithms '''

    def __init__(self, ml_array, columns):
        self.ml_array = ml_array
        self.columns = ['year', 'month', 'day', 'dow', 'woy', 
                        'hour', 'event', 'direction', 'count', 'epoch']
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
        self.epoch = None


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


    def make_prediction(self, details):

        def num_str(num):
            ''' take in integer and convert it to a string '''
            if int(num) < 10:  # add a leading 0 if int < 10
                str_num = '0' + str(num)
            else:
                str_num = str(num)
    
            return str_num

        self.year = num_str(details[0])
        self.month = num_str(details[1])
        self.day = num_str(details[2])
        self.hour = num_str(details[5])

        # get the features that are being used for the predictions
        features = []
        for column in self.required_columns:
            match column:
                case 'year':
                    features.append(details[0])
                case 'month':
                    features.append(details[1])
                case 'day':
                    features.append(details[2])
                case 'dow':
                    features.append(details[3])
                case 'woy':
                    features.append(details[4])
                case 'hour':
                    features.append(details[5])
                case 'event':
                    features.append(details[6])
                case 'direction':
                    features.append(details[7])
                case 'epoch':
                    features.append(details[8])

        # get the data to be used to make the prediction
        predict_df = pd.DataFrame([features], columns=self.required_columns)
        
        self.prediction = self.model.predict(predict_df)


    def print_prediction(self, mtype):
        print(f'\nUsing {mtype}: ')
        print(f'The predicted volume between {self.hour}:00 and {str(int(self.hour) + 1)}:00 on {self.day}/{self.month}/{self.year} is:')
        print(f'\t{int(self.prediction[0])}')
