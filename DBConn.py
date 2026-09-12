#!/usr/bin/python3

import os
import mysql.connector
from dotenv import load_dotenv

class DBConn:
    ''' create a connection to the database '''

    def __init__(self, host, user, password, port, database):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = database
        self.conn = None
        self.cur = None


    def get_conn(self):
        if self.conn == None:
            self.conn = mysql.connector.connect(
                host = self.host,
                port = self.port,
                user = self.user,
                password = self.password,
                database = self.database
            )

        return self.conn


    def get_cursor(self):
        self.cur = self.conn.cursor()

        return self.cur

    