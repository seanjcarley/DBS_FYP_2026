import datetime as dt
import time as t

import pandas as pd
import numpy as np

import KNearestNeighbour as knn
import LinearReg as lr
import SupportVectorMachine as sv

def test_KNN(ml_arr):
    case = 7
    count = 0
    best_result = 1
    best_n = 0
    case_dir = {}

    while case > 0:
        while count < 100:
            # print(f'Run : {count + 1}')
            kn_model = knn.KNearestNeighbour(ml_arr, count + 1)
            result = kn_model.get_training_model(case)
            if result > 0 and result < best_result:
                best_n = count + 1
                best_result = result
            count += 1

        print(f'For case {case} the best number of Neighbours is {best_n}')

        case_dir[case] = [best_n, best_result]

        case -= 1
        count = 0
        best_result = 1
        best_n = 0


    return case_dir