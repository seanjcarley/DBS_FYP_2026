import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor

class KNearestNeighbour:
    ''' run KNN machine learning algorithm '''

    def __init__(self, kn_array, neighbours=15):
        self.neighbours = neighbours
        self.kn_array = kn_array
        self.columns = ['year', 'month', 'day', 'dow', 
                        'hour', 'event', 'direction', 'count']
        self.df = None
        self.knn = None
        self.X = None
        self.y = None


    def get_training_model(self):
        self.df = pd.DataFrame(self.kn_array, columns = self.columns)

        scaler = StandardScaler()
        scaler.fit(self.df.drop(['count'], axis=1))
        scaled_features = scaler.transform(
            self.df.drop(['count'], axis=1))

        self.X = scaled_features
        self.y = self.df['count']

        X_train, X_test, y_train, y_test = train_test_split(
                    self.X, self.y, test_size=0.4, random_state=79)

        self.knn = KNeighborsRegressor(n_neighbors=self.neighbours)

        self.knn.fit(X_train, y_train)

        predictions = self.knn.predict(X_test)

        self.print_test_metrics(y_test, predictions)


    def make_prediction(self, y, m, d, dw, h, e, di):
        predict_df = pd.DataFrame([[y, m, d, dw, h, e, di]],
            columns=['year', 'month', 'day', 'dow', 'hour', 'event', 'direction'])

        predciction = self.knn.predict(predict_df)

        return predciction


    def print_test_metrics(self, y_test, predictions):
        print(f'Using the data provided and the K-Nearest Neighbours set to {self.neighbours}:')
        print(f'MAE: {metrics.mean_absolute_error(y_test, predictions)}')
        print(f'MSE: {metrics.mean_squared_error(y_test, predictions)}')
        print(f'RMSE: {np.sqrt(metrics.mean_squared_error(y_test, predictions))}')
        print(f'Explained Variance: {metrics.explained_variance_score(y_test, predictions)}')
