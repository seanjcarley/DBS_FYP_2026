#!/usr/bin/python3

from dotenv import load_dotenv
import datetime as dt

import KNearestNeighbour as knn
import LinearReg as lr
import SupportVectorMachine as sv
import TimeSeries as ts
import GetTrainingData as gtd


def main():
    # access environment variables
    load_dotenv()

    # get the training data from the db and process it to be used by the 
    # maching learning algorithms
    td = gtd.GetTrainingData()  # create the training data object
    td.get_db_data()  # get the data from the db
    td.process_data()  # process the data into a numpy array

    # train the various models
    kn_model = knn.KNearestNeighbour(td.ml_arr)  # create KNN object
    kn_model.get_test_training_dataset()  # get and split the data to be used 
    kn_model.get_training_model()  # train the KNN model
    # lr_model = lr.LinearReg(td.ml_arr)  # create Linear Regression object
    # lr_model.get_test_training_dataset()  # get and split the data to be used 
    # lr_model.get_training_model()  # train the LR model
    # svm_model = sv.SupportVectorMachine(td.ml_arr)  # create SVM object
    # svm_model.get_training_model()  # train the SVM model
    # ts_model = ts.TimeSeries(td.ml_arr)
    # ts_model.get_data_frame()
    # ts_model.plot_data()
    # ts_model.adfuller()
    # ts_model.arima()

    # ask for the date time and direction for making a prediction
    pred_date = input('\nPlease enter the Date to make a prediction for (DD/MM/YYYY format): ')
    pred_hour = input('Please enter the Hour to make a prediction for (0 - 23): ')
    pred_event = input('Please enter an Event code (0 for no event): ')
    pred_direction = input('Please enter a direction code (0: North, 4: South): ')

    # create variables to be used in retrieving the prediction
    pred_year = int(pred_date[6:])
    pred_month = int(pred_date[3:5])
    pred_day = int(pred_date[:2])
    pred_dow = int(dt.datetime.strptime(pred_date, '%d/%m/%Y').strftime('%w'))
    pred_woy = int(dt.datetime.strptime(pred_date, '%d/%m/%Y').strftime('%W'))

    # get the predictions from the required model
    # KNN
    kn_model.make_prediction(pred_year, pred_month, pred_day, pred_dow, 
        pred_woy, pred_hour, pred_event, pred_direction)
    kn_model.print_prediction(kn_model.ml_type)
    
    # Linear Regression
    # lr_model.make_prediction(pred_year, pred_month, pred_day, pred_dow, 
    #     pred_woy, pred_hour, pred_event, pred_direction)
    # lr_model.print_prediction(lr_model.ml_type)

    # SVM
    # predicted_svolume = svm_model.make_prediction(
    #     pred_year, pred_month, pred_day, pred_dow, pred_woy, 
    #     pred_hour, pred_event, pred_direction)
    # print(f'\nUsing Support Vector Machine:')
    # print(
    #         f'The predicted volume for {pred_hour}:00 - {str(int(pred_hour) + 1)}:00 on {pred_date} is: {int(predicted_svolume[0])}')

if __name__ == '__main__':
    main()