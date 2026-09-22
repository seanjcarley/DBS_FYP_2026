import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from KNearestNeighbour import KNearestNeighbour

class GetOptimumK(KNearestNeighbour):

    def __init__(self, ml_array, columns,
        ml_type='K Nearest Neighbors (KNN)'):
        super().__init__(ml_array, columns)
        self.neighbours = 10
        self.ml_type = ml_type


    def get_best_k(self):
        self.get_test_training_dataset()
        self.get_training_model()
        

    def get_training_model(self, cse=1):
        self.df = pd.DataFrame(self.ml_array, columns = self.columns)

        scaler = StandardScaler()

        match cse:  # use to select required columns 
            case 1:  # use all columns
                scaler.fit(self.df.drop(['count'], axis=1))
                scaled_features = scaler.transform(
                    self.df.drop(['count'], axis=1))
            case 2:  # use year month and day columns
                scaler.fit(self.df.drop(['dow', 'woy', 'hour', 'event', 
                    'direction','count'], axis=1))
                scaled_features = scaler.transform(self.df.drop(['dow', 'woy', 
                    'hour', 'event', 'direction','count'], axis=1))
            case 3:  # use dow and woy columns
                scaler.fit(self.df.drop(['year', 'month', 'day', 'hour', 
                    'event', 'direction', 'count'], axis=1))
                scaled_features = scaler.transform(self.df.drop(['year', 
                    'month', 'day', 'hour', 'event', 'direction', 'count'], 
                    axis=1))
            case 4:  # use hour and direction columns
                scaler.fit(self.df.drop(['year', 'month', 'day', 'dow', 'woy', 
                    'event', 'count'], axis=1))
                scaled_features = scaler.transform(self.df.drop(['year', 
                    'month', 'day', 'dow', 'woy', 'event', 'count'], axis=1))
            case 5:  # use dow and hour columns
                scaler.fit(self.df.drop(['year', 'month', 'day', 'woy', 
                    'event', 'direction', 'count'], axis=1))
                scaled_features = scaler.transform(self.df.drop(['year', 
                    'month', 'day', 'woy', 'event', 'direction', 'count'], 
                    axis=1))
            case 6:  # use year, month day and hour columns
                scaler.fit(self.df.drop(['dow', 'woy', 'event', 
                    'direction','count'], axis=1))
                scaled_features = scaler.transform(self.df.drop(['dow', 'woy', 
                    'event', 'direction','count'], axis=1))
            case 7:  # use year, dow, woy, and direction columns
                scaler.fit(self.df.drop(['month', 'day', 'hour', 'event', 
                    'count'], axis=1))
                scaled_features = scaler.transform(self.df.drop(['month', 
                    'day', 'hour', 'event','count'], axis=1))

        self.X = scaled_features
        self.y = self.df['count']

        X_train, X_test, y_train, y_test = train_test_split(
                    self.X, self.y, test_size=0.4, random_state=79)

        self.knn = KNeighborsRegressor(n_neighbors=self.neighbours)

        self.knn.fit(X_train, y_train)

        predictions = self.knn.predict(X_test)

        result = metrics.explained_variance_score(y_test, predictions)

        self.print_test_metrics(y_test, predictions)

        return result

    def print_test_metrics(self, y_test, predictions):
            print(f'Using the data provided and the K-Nearest Neighbours set to {self.neighbours}:')
            print(f'MAE: {metrics.mean_absolute_error(y_test, predictions)}')
            print(f'MSE: {metrics.mean_squared_error(y_test, predictions)}')
            print(f'RMSE: {np.sqrt(metrics.mean_squared_error(y_test, predictions))}')
            print(f'R2 Score: {metrics.r2_score(y_test, predictions)}')
            print(f'Explained Variance: {metrics.explained_variance_score(y_test, predictions)}')