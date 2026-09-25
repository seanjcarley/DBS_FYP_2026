import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import matplotlib.pyplot as plt
from MachineLearning import MachineLearning

class LinearReg(MachineLearning):
    ''' run Linear Regression machine learning algorithm '''

    def __init__(self, ml_array, columns=['epoch'], 
                ml_type='Linear Regression'):
        super().__init__(ml_array, columns)
        self.ml_type = ml_type


    def get_training_model(self):
        self.model = LinearRegression()
        self.model.fit(self.X_train, self.y_train)

        coeff = pd.DataFrame(self.model.coef_, self.X.columns, 
            columns=['Coefficient'])

        predictions = self.model.predict(self.X_test)

        self.print_test_metrics(self.y_test, predictions, coeff)


    def print_test_metrics(self, y_test, predictions, coeff):
        print(f'\nUsing {self.ml_type}:')
        print(f'Coefficient: {coeff}')
        print(f'MAE: {metrics.mean_absolute_error(y_test, predictions)}')
        print(f'MSE: {metrics.mean_squared_error(y_test, predictions)}')
        print(f'RMSE: {np.sqrt(metrics.mean_squared_error(y_test, predictions))}')
        print(f'Explained Variance: {metrics.explained_variance_score(y_test, predictions)}')


    def plot_reg_line(self):
        plt.figure(figsize=(10, 8))
        plt.scatter(self.X_train, self.y_train, color='blue', label='Data Points')
        plt.plot(self.X_test, self.model.predict(self.X_test), 
                 color='red', label='Reg Line')
        plt.title('Linear Regression')
        plt.legend()
        plt.grid(True)
        plt.show()
        