import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

class MachineLearning:
    ''' parent class for machine learning algorithms '''

    def __init__(self, ml_array, columns=['year', 'month', 'day']):
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

        

