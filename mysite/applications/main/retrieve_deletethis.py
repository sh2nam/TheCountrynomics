import pymysql
import sqlite3
import pandas as pd
import os

class Query:
    def __init__(self):

        self.db_setting =  {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'C:\Sang Nam\Coding\PythonDjangoProject\mysite\db.sqlite3',
        }
        # self.db_setting = {'ENGINE': 'django.db.backends.sqlite3',
        #                    'NAME': 'C:\Sang Nam\Coding\PythonDjangoProject\mysite\db.sqlite3'}

        # self.engine = django.db.backends.sqlite3

    def create_connection(self, ):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        name = self.db_setting['NAME']
        try:
            if self.db_setting['ENGINE'] == 'django.db.backends.sqlite3':
                conn = sqlite3.connect(name)
            else:
                host = self.db_setting['HOST']
                user = self.db_setting['USER']
                pwd = self.db_setting['PASSWORD']
                db = name
                conn = pymysql.connect(host=host, user=user, passwd=pwd, db=db)

        except:
            print('db not connected')
        return conn

    def get_email_list(self):
        conn = self.create_connection()
        q = 'select * from main_email'
        data = pd.read_sql(q, conn)
        conn.close()
        return data

if __name__ == "__main__":

    a = Query().get_email_list()
    print(a)
