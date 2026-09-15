import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import metrics

class SupportVectorMachine:
    ''' run Support Vector Machine '''

    def __init__ (self, svm_array, columns=['year', 'month', 'day']):
        self.svm_array = svm_array
        self.columns = ['year', 'month', 'day', 'dow', 'woy', 
                        'hour', 'event', 'direction', 'count']
        self.drop_columns = []
        self.required_columns = columns
        self.df = None
        self.svm = None
        self.X = None
        self.y = None


    def get_training_model(self):
        self.df = pd.DataFrame(self.svm_array, columns=self.columns)

        # drop the columns that are not being used
        for column in self.columns:
            if column not in self.required_columns:
                self.drop_columns.append(column)

        self.X = self.df.drop(self.drop_columns, axis=1)
        self.y = self.df['count']

        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.4, random_state=79)

        self.svm = svm.NuSVR()
        self.svm.fit(X_train, y_train)

        predictions = self.svm.predict(X_test)

        self.print_test_metrics(y_test, predictions)


    def print_test_metrics(self, y_test, predictions):
            print(f'Using the data provided:')
            print(f'MAE: {metrics.mean_absolute_error(y_test, predictions)}')
            print(f'MSE: {metrics.mean_squared_error(y_test, predictions)}')
            print(f'RMSE: {np.sqrt(metrics.mean_squared_error(y_test, predictions))}')
            print(f'Explained Variance: {metrics.explained_variance_score(y_test, predictions)}')


    def make_prediction(self, y, m, d, dw, wy, h, e, di, ):
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

        prediction = self.svm.predict(predict_df)
        return prediction
