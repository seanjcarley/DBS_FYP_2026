import os
from dotenv import load_dotenv
from DBConn import DBConn

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

import datetime as dt
import time as t

import pandas as pd
import numpy as np

import KNearestNeighbour as knn
import LinearReg as lr

def main():

    # access environment variables
    load_dotenv()

    # SQLAlchemy
    # mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
    engine_url = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{int(os.getenv('DB_PORT'))}/{os.getenv('DB_NAME')}"
    # print(int(os.getenv('DB_PORT')))
    # print(engine_url)
    engine = create_engine(engine_url)
    query_columns = 'COUNT_YEAR, COUNT_MONTH, COUNT_DAY, COUNT_DOW, COUNT_HOUR, COUNT_EVENT_CLASS, COUNT_DIRECTION, COUNT_VEHICLE_CLASS, COUNT'

    with engine.begin() as db_conn:
        df = pd.read_sql_query(sa.text(f'select {query_columns} from counts where COUNT_YEAR <> 2021'), db_conn)

    # print(df.head())

    count_arr = np.array(df)
    # print(count_arr[:10])
    for arr in count_arr:
        if len(arr) != 9:
            print(arr)
    vc_1, vc_2, vc_3, vc_4, vc_5, vc_6, vc_7, vc_8, totals = {}, {}, {}, {}, {}, {}, {}, {}, {}

    def num_str(num):
        ''' change int(num) to str(num) and add leading 0 if required '''
        if num < 10:
            str_num = "0" + str(num)
        else:
            str_num = str(num)

        return str_num

    for i in count_arr:
        # set year, month, day, and hour and direction variables
        y = num_str(i[0])
        m = num_str(i[1])
        d = num_str(i[2])
        wd= num_str(i[3])
        h = num_str(i[4]) + ':00'
        if i[6] == 0:
            dir = 'north'
        if i[6] == 4:
            dir = 'south'
 
        # set the date variable
        str_date_dir = f'{y}-{m}-{d} {h} {dir}'

        # add the count to the dictionary
        if i[7] == 0:  # invalid reading
            vc_1[str_date_dir] = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
        elif i[7] == 1:  # motorbike
            vc_2[str_date_dir] = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
        elif i[7] == 2:  # car
            vc_3[str_date_dir] = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
        elif i[7] == 3:  # light goods vehicle
            vc_4[str_date_dir] = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
        elif i[7] == 4:  # bus
            vc_5[str_date_dir] = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
        elif i[7] == 5:  # heavy goods vehicle: rigid
            vc_6[str_date_dir] = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
        elif i[7] == 6:  # heavy goods vehicle: artiulated
            vc_7[str_date_dir] = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
        elif i[7] == 7:  # caravan
            vc_8[str_date_dir] = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
        else:
            pass

    dirs = [vc_1, vc_2, vc_3, vc_4, vc_5, vc_6, vc_7, vc_8]
    totals = {}

    for dir in dirs:
        for k, v in dir.items():
            if k not in totals:
                totals[k] = [v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[8]]
            else:
                totals[k][7] = totals[k][7] + v[8]

    # print(totals)
    # print(totals['2023-05-05 09:00 north'])
    # print(totals['2023-05-05 09:00 south'])

    lst = []

    for k, v in totals.items():
        lst.append([v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7]])

    # print(lst[:50])

    ml_arr = np.array(lst)
    # print(np.shape(ml_arr))

    kn_model = knn.KNearestNeighbour(ml_arr, 2500)
    kn_model.get_training_model()

    lr_model = lr.LinearReg(ml_arr)
    lr_model.get_training_model()

    pred_date = input('\nPlease enter the Date to make a prediction for (DD/MM/YYYY format): ')
    pred_hour = input('Please enter the Hour to make a prediction for (0 - 23): ')
    pred_event = input('Please enter an Event code (0 for no event): ')
    pred_direction = input('Please enter a direction code (0: North, 4: South): ')

    pred_year = int(pred_date[6:])
    pred_month = int(pred_date[3:5])
    pred_day = int(pred_date[:2])
    pred_dow = int(dt.datetime.strptime(pred_date, '%d/%m/%Y').strftime('%w'))

    predicted_kvolume = kn_model.make_prediction(
        pred_year, pred_month, pred_day, pred_dow, 
        pred_hour, pred_event, pred_direction)
    # print(type(predicted_volume))
    print(f'\nUsing K-Nearest Neighbour:')
    print(
        f'The predicted volume for {pred_hour}:00 - {str(int(pred_hour) + 1)}:00 on {pred_date} is: {int(predicted_kvolume[0])}')

    predicted_lvolume = lr_model.make_prediction(
        pred_year, pred_month, pred_day, pred_dow, 
        pred_hour, pred_event, pred_direction)
    print(f'\nUsing Linear Regression:')
    print(
        f'The predicted volume for {pred_hour}:00 - {str(int(pred_hour) + 1)}:00 on {pred_date} is: {int(predicted_lvolume[0])}')

if __name__ == '__main__':
    main()