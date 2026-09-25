#!/usr/bin/python3

import os
from dotenv import load_dotenv
import datetime as dt
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
import pandas as pd
import numpy as np

load_dotenv()

class GetTrainingData:
    ''' get numpy array to be used for machine learning'''
    def __init__ (self):
        self.pre_proc_data = None
        self.dict_invld_0 = {}  # invalid reading 
        self.dict_mbk_1 = {}  # motorbike
        self.dict_car_2 = {}  # car
        self.dict_lgv_3 = {}  # light goods vehicle (i.e. van)
        self.dict_bus_4 = {}  # bus
        self.dict_hgv_r_5 = {}  # heavy goods vehicle (rigid)
        self.dict_hgv_a_6 = {}  # heavy goods vehicle (articulated)
        self.dict_cvn_7 = {}  # caravan/motorhome
        self.dict_totals = {}  # totals
        self.dirs = [self.dict_invld_0, self.dict_mbk_1, self.dict_car_2, 
                     self.dict_lgv_3, self.dict_bus_4, self.dict_hgv_r_5, 
                     self.dict_hgv_a_6, self.dict_cvn_7]
        self.ml_arr = None


    def get_db_data(self):
        ''' connect to the data base a retrieve the data to be used '''
        # SQLAlchemy
        # mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
        engine_url = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{int(os.getenv('DB_PORT'))}/{os.getenv('DB_NAME')}"
        engine = create_engine(engine_url, poolclass=NullPool)

        query_columns = 'COUNT_YEAR, COUNT_MONTH, COUNT_DAY, COUNT_DOW, COUNT_HOUR, COUNT_EVENT_CLASS, COUNT_DIRECTION, COUNT_VEHICLE_CLASS, COUNT'

        with engine.begin() as db_conn:
            df = pd.read_sql_query(sa.text(
                f'select {query_columns} from counts where COUNT_HOUR between 6 and 19 order by COUNT_YEAR, COUNT_MONTH, COUNT_DAY, COUNT_HOUR;'
            ), db_conn)
            db_conn.close()

        self.pre_proc_data = np.array(df)


    def num_str(self, num):
        ''' take in integer and convert it to a string '''
        if num < 10:  # add a leading 0 if int < 10
            str_num = '0' + str(num)
        else:
            str_num = str(num)

        return str_num


    def process_data(self):
        for a in self.pre_proc_data:
            # create a key to be used in the dicts using date time and direction
            # set year(y), month(m) and day(d) variables to string
            y = self.num_str(a[0])
            m = self.num_str(a[1])
            d = self.num_str(a[2])

            # set data in required format (YYYY-MM-DD) for use in dict keys
            str_date = f'{y}-{m}-{d}'

            # set h variable for use in dict keys
            h = self.num_str(a[4]) + ':00'

            # set epoch value, this allows the time values to be combined into
            # one value
            epoch = int(dt.datetime(a[0], a[1], a[2], a[4], 0).timestamp())


            # set the dir variable to be used in the dict keys
            if a[6] == 0:
                dir = 'north'
            if a[6] == 4:
                dir = 'south'

            # set the week of the year (wy) variable (possible values: 0-53)
            wy = int(dt.datetime.strptime(str_date, '%Y-%m-%d').strftime('%W'))

            # set the key to be used in the dicts
            str_key = f'{str_date} {h} {dir}'

            # add the data to the appropriate dict based on vehicle class a[7]
            # a[0]: y, a[1]: m, a[2]: d, a[3]: wd, wy, a[4]:hr, a[5]: e, 
            # a[6]: dir, a[7]: vc, a[8]: c 
            match a[7]:
                case 0:  # invalid reading 
                    self.dict_invld_0[str_key] = [a[0], a[1], a[2], a[3], wy, 
                        a[4], a[5], a[6], a[7], a[8], epoch]
                case 1:  # motorbike
                    self.dict_mbk_1[str_key] = [a[0], a[1], a[2], a[3], wy, 
                        a[4], a[5], a[6], a[7], a[8], epoch]
                case 2:  # car
                    self.dict_car_2[str_key] = [a[0], a[1], a[2], a[3], wy, 
                        a[4], a[5], a[6], a[7], a[8], epoch]
                case 3:  # light goods vehicle (i.e. van)
                    self.dict_invld_0[str_key] = [a[0], a[1], a[2], a[3], wy, 
                        a[4], a[5], a[6], a[7], a[8], epoch]
                case 4 :  # bus
                    self.dict_bus_4[str_key] = [a[0], a[1], a[2], a[3], wy, 
                        a[4], a[5], a[6], a[7], a[8], epoch]
                case 5 :  # heavy goods vehicle (rigid)
                    self.dict_hgv_r_5[str_key] = [a[0], a[1], a[2], a[3], wy, 
                        a[4], a[5], a[6], a[7], a[8], epoch]
                case 6 :  # heavy goods vehicle (articulated)
                    self.dict_hgv_a_6[str_key] = [a[0], a[1], a[2], a[3], wy, 
                        a[4], a[5], a[6], a[7], a[8], epoch]
                case 7 :  # caravan/motorhome
                        self.dict_cvn_7[str_key] = [a[0], a[1], a[2], a[3], wy, 
                            a[4], a[5], a[6], a[7], a[8], epoch]

        for dir in self.dirs:
            for k, v in dir.items():
                # sum the totals for all vehicle classes and add to 
                # dict_totals dict dropping the vehicle class
                if k not in self.dict_totals:
                    self.dict_totals[k] = [v[0], v[1], v[2], v[3], v[4], v[5],
                                           v[6], v[7], v[9], v[10]]
                else:
                    self.dict_totals[k][8] = self.dict_totals[k][8] + v[9]

        # create an empty list
        lst = []

        # populate the empty list which will be used to create the numpy array
        for k, v in self.dict_totals.items():
            lst.append(v)

        # create the numpy array
        self.ml_arr = np.array(lst)
