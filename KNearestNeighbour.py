import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from MachineLearning import MachineLearning

class KNearestNeighbour(MachineLearning):
    ''' run KNN machine learning algorithm '''

    def __init__(self, ml_array, columns=['year', 'month', 'day'], 
        neighbors=42, ml_type='K Nearest Neighbors (KNN)'):
        super().__init__(ml_array, columns)
        self.neighbors = neighbors
        self.ml_type = ml_type


    def get_test_training_dataset(self):
        # create the dataframe to be used
        self.df = pd.DataFrame(self.ml_array, columns=self.columns)

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
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                    self.X, self.y, test_size=0.4, random_state=79)

        # self.plot_data()


    def plot_data(self):
        plt.figure(figsize=(12, 5))
        plt.plot(self.y_train.count)
        plt.ylabel('count')
        plt.grid(True)
        plt.show()


    def get_training_model(self):        
        # create the regressor object
        self.model = KNeighborsRegressor(n_neighbors=self.neighbors)
        self.model.fit(self.X_train, self.y_train)  # fit the data to the regressor

        # run predections on the test set
        predictions = self.model.predict(self.X_test)

        # get the stats on the model performance
        mae = metrics.mean_absolute_error(self.y_test, predictions)
        mse = metrics.mean_squared_error(self.y_test, predictions)
        ev = metrics.explained_variance_score(self.y_test, predictions)

        result = [mae, mse, ev]

        # print model performance stats
        self.print_test_metrics(self.y_test, predictions)

        return result


    def print_test_metrics(self, y_test, predictions):
        print(f'\nUsing {self.ml_type} and K set to {self.neighbors}:')
        print(f'MAE: {metrics.mean_absolute_error(y_test, predictions)}')
        print(f'MSE: {metrics.mean_squared_error(y_test, predictions)}')
        print(f'RMSE: {np.sqrt(metrics.mean_squared_error(y_test, predictions))}')
        print(f'R2 Score: {metrics.r2_score(y_test, predictions)}')
        print(f'Explained Variance: {metrics.explained_variance_score(y_test, predictions)}')
