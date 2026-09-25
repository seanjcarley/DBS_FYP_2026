#!/usr/bin/python3

from dotenv import load_dotenv
import datetime as dt

import KNearestNeighbour as knn
import LinearReg as lr
import SupportVectorMachine as sv
import DecisionTree as d3
import TimeSeries as ts
import GetTrainingData as gtd
from testKNN import test_KNN


def get_prediction():
    # access environment variables
    load_dotenv()

    # get the training data from the db and process it to be used by the 
    # maching learning algorithms
    td = gtd.GetTrainingData()  # create the training data object
    td.get_db_data()  # get the data from the db
    td.process_data()  # process the data into a numpy array

    def choose_model():
        print('\nWhich model you would like to use: \n')
        print('1. Linear Regression...')
        print('2. K Nearest Neighbour (KNN)...')
        print('3. Support Vector Machine (SVM)...')
        print('4. Time Series...')
        print('5. Decision Tree...')
        print('6. Exit...')


        choice = int(input('Enter your choice: '))

        return choice

    def get_details():
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
        pred_epoch = int(dt.datetime(pred_year, pred_month, pred_day, 
            int(pred_hour), 0).timestamp())

        # return the required variables
        return [pred_year, pred_month, pred_day, pred_dow, pred_woy, 
                pred_hour, pred_event, pred_direction, pred_epoch]

    choice = choose_model()
    

    while 0 < choice < 6:
        match choice:

            case 1:  # Linear Regression
                # create Linear Regression object
                lr_model = lr.LinearReg(
                    td.ml_arr, ['direction', 'epoch'])
                # get and split the data to be used   
                lr_model.get_test_training_dataset()  
                # train the LR model
                lr_model.get_training_model()

                while keep_going:
                    details = get_details()

                    lr_model.make_prediction(details)
                    input('Press Enter to continue...')

                    lr_model.print_prediction(lr_model.ml_type)
                    input('Press Enter to continue...')

                    again = input('Would you like to try for a different time (yes/no): ')

                    if again == 'no':
                        keep_going = False
                        
            case 2:  # K Nearest Neighbour (KNN)
                # create KNN object
                kn_model = knn.KNearestNeighbour(
                    td.ml_arr, ['direction', 'epoch'], 45)  # 0.002
                # kn_model = knn.KNearestNeighbour(td.ml_arr, ['year', 'month', 'day'], 14) # 0.003
                # kn_model = knn.KNearestNeighbour(td.ml_arr, ['epoch'], 90)  # 0.006
                # get and split the data to be used 
                kn_model.get_test_training_dataset()
                # train the KNN model
                kn_model.get_training_model()
                # print(test_KNN(td.ml_arr))
                details = get_details()
                kn_model.make_prediction(details)
                kn_model.print_prediction(kn_model.ml_type)

            case 3:  # Support Vector Machine (SVM)
                # create SVM object
                svm_model = sv.SupportVectorMachine(td.ml_arr)
                # train the SVM model
                svm_model.get_training_model()

            case 4:  # Time Series
                ts_model = ts.TimeSeries(td.ml_arr)
                ts_model.get_data_frame()
                ts_model.plot_data()
                ts_model.adfuller()
                ts_model.arima()

            case 5:  # Decision Tree
                d3_model = d3.DecisionTree(td.ml_arr)
                d3_model.get_test_training_dataset()
                d3_model.get_training_model()

                d3_model.make_prediction(details)
                d3_model.print_prediction(d3_model.ml_type)
                # d3_model.plot_tree()
    

    # SVM
    # predicted_svolume = svm_model.make_prediction(
    #     pred_year, pred_month, pred_day, pred_dow, pred_woy, 
    #     pred_hour, pred_event, pred_direction, pred_epoch)
    # print(f'\nUsing Support Vector Machine:')
    # print(
    #         f'The predicted volume for {pred_hour}:00 - {str(int(pred_hour) + 1)}:00 on {pred_date} is: {int(predicted_svolume[0])}')
    
# if __name__ == '__main__':
#     main()