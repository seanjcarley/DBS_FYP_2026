import datetime as dt
import time as t

import pandas as pd
import numpy as np

import KNearestNeighbour as knn
import LinearReg as lr
import SupportVectorMachine as sv
from GetTrainingData import GetTrainingData

def test_KNN():

    count = 0
    best_result = 1
    best_n = 0

    td = GetTrainingData()  # create the training data object
    td.get_db_data()  # get the data from the db
    td.process_data()  # process the data into a numpy array


    while count < 150:  # 45:.002, 108:.02, 568:.05, 16246:.01
        # print(f'Run : {count + 1}')
        kn_model = knn.KNearestNeighbour(td.ml_arr, ['year', 'month', 'day'], 
            count+1)
        kn_model.get_test_training_dataset()
        result = kn_model.get_training_model()
        if result[2] > 0 and result[2] < best_result:
            best_n = count + 1
            best_result = result[2]
        count += 1
    print(f'The best number of Neighbours is {best_n}')

    count = 0

    return [best_n, best_result]

if __name__ == '__main__':
    test_KNN()