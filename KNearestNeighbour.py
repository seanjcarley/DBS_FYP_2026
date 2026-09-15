import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor

class KNearestNeighbour:
    ''' run KNN machine learning algorithm '''

    def __init__(self, kn_array, columns=['year', 'month', 'day'], 
        neighbours=42):
        self.neighbours = neighbours
        self.kn_array = kn_array
        self.columns = ['year', 'month', 'day', 'dow', 'woy', 
                        'hour', 'event', 'direction', 'count']
        self.drop_columns = []
        self.required_columns = columns
        self.df = None
        self.knn = None
        self.X = None
        self.y = None


    def get_training_model(self):
        # create the dataframe to be used
        self.df = pd.DataFrame(self.kn_array, columns=self.columns)

        # print(f'Columns: {self.columns}')
        # print(f'Required Columns: {self.required_columns}')

        # drop the columns that are not being used
        for column in self.columns:
            if column not in self.required_columns:
                self.drop_columns.append(column)

        # print(f'Drop Columns: {self.drop_columns}')

        scaler = StandardScaler()

        scaler.fit(self.df.drop(self.drop_columns, axis=1))
        scaled_features = scaler.transform(
            self.df.drop(self.drop_columns, axis=1)
        )

        self.X = scaled_features
        self.y = self.df['count']

        # split the data in to training and testing subsets
        X_train, X_test, y_train, y_test = train_test_split(
                    self.X, self.y, test_size=0.4, random_state=79)

        # create the regressor object
        self.knn = KNeighborsRegressor(n_neighbors=self.neighbours)
        self.knn.fit(X_train, y_train)  # fit the data to the regressor

        # run predections on the test set
        predictions = self.knn.predict(X_test)

        # get the stats on the model performance
        mae = metrics.mean_absolute_error(y_test, predictions)
        mse = metrics.mean_squared_error(y_test, predictions)
        ev = metrics.explained_variance_score(y_test, predictions)

        result = [mae, mse, ev]

        # print model performance stats
        self.print_test_metrics(y_test, predictions)

        return result


    def make_prediction(self, y, m, d, dw, wy, h, e, di):

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

        # make and return the prediction
        predciction = self.knn.predict(predict_df)

        return predciction


    def print_test_metrics(self, y_test, predictions):
        print(f'Using the data provided and the K-Nearest Neighbours set to {self.neighbours}:')
        print(f'MAE: {metrics.mean_absolute_error(y_test, predictions)}')
        print(f'MSE: {metrics.mean_squared_error(y_test, predictions)}')
        print(f'RMSE: {np.sqrt(metrics.mean_squared_error(y_test, predictions))}')
        print(f'R2 Score: {metrics.r2_score(y_test, predictions)}')
        print(f'Explained Variance: {metrics.explained_variance_score(y_test, predictions)}')
