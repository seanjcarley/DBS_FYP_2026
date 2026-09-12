#!/usr/bin/python3
import DBConn


class Queries:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_conn(self):
        db_conn = DBConn.get_conn()

        return db_conn

    def  create_cursor(self):
        db_cur = DBConn.get_cursor()

        return db_cur

    def add_vehicle_counts(event):# add data to the counts table
        # print(event)
        if len(event) == 9:
             return f"insert into counts (COUNT_YEAR , COUNT_MONTH, COUNT_DAY, COUNT_DOW, COUNT_HOUR, COUNT_EVENT_CLASS, COUNT_DIRECTION, COUNT_VEHICLE_CLASS, COUNT) VALUES ({event[0]}, {event[1]}, {event[2]}, {event[3]}, {event[4]}, {event[5]}, {event[6]}, {event[7]}, {event[8]});"
