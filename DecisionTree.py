import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.tree import DecisionTreeRegressor, export_text, plot_tree
import matplotlib.pyplot as plt 
from MachineLearning import MachineLearning

class DecisionTree(MachineLearning):

    def __init__(self, ml_array, columns=['epoch'],
                 ml_type='Decision Tree'):
        super().__init__(ml_array, columns)
        self.ml_type = ml_type


    
    def get_training_model(self):
        # create the regressor object
        self.model = DecisionTreeRegressor(max_depth=4, random_state=79)
        self.model.fit(self.X_train, self.y_train)

        # run predictions on the test set
        self.predictions = self.model.predict(self.X_test)

        # get the ststs on the model performance
        mse = metrics.mean_squared_error(self.y_test, self.predictions)

        # print model performance
        self.print_test_metrics(self.y_test, self.predictions)


    def print_test_metrics(self, y_test, predictions):
        print(f'\nUsing {self.ml_type}:')
        print(f'MAE: {metrics.mean_absolute_error(y_test, predictions)}')
        print(f'MSE: {metrics.mean_squared_error(y_test, predictions)}')
        print(f'RMSE: {np.sqrt(metrics.mean_squared_error(y_test, predictions))}')
        print(f'Explained Variance: {metrics.explained_variance_score(y_test, predictions)}')

    def plot_tree(self):
        plt.figure(figsize=(20, 10))
        plot_tree(
            self.model,
            feature_names=self.columns,
            filled=True,
            rounded=True,
            fontsize=10
        )
        plt.title('Decision Tree')
        plt.show()