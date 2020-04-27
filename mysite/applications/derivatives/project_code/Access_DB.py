import pymysql
import sqlite3
import pandas as pd
from django.conf import settings
import sqlite3
import sshtunnel
import time



class AccessDB:
    def __init__(self):
        self.db_setting = settings.DATABASES['default']

    def __create_connection(self):
        """ create a database connection to the SQLite database
            specified by the db_file
        :return: Connection object or None
        """
        conn = None

        try:
            if self.db_setting['ENGINE'] == 'django.db.backends.sqlite3':
                conn = sqlite3.connect(self.db_setting['NAME'])
            else:
                host = self.db_setting['HOST']
                user = self.db_setting['USER']
                pwd = self.db_setting['PASSWORD']
                db = name
                conn = pymysql.connect(host=host, user=user, passwd=pwd, db=db)

        except:
            print('db not connected')
        return conn

    def run_read_query_pythonanywhere(self, query: str):
        with sshtunnel.SSHTunnelForwarder(('ssh.pythonanywhere.com', 22), ssh_username='countrynomics',
                                          ssh_password='shskaa93',
                                          remote_bind_address=(
                                          'countrynomics.mysql.pythonanywhere-services.com', 3306)) as tunnel:

            connection = pymysql.connect(host='127.0.0.1', user='countrynomics', passwd='countsql@',
                                         db='countrynomics$new_indicator',
                                         port=tunnel.local_bind_port)

            try:
                data = pd.read_sql_query(query, connection)
            finally:
                connection.close()
        return data

    def run_insert_query_pythonanywhere(self, query_list: list):
        with sshtunnel.SSHTunnelForwarder(('ssh.pythonanywhere.com', 22), ssh_username='countrynomics',
                                          ssh_password='shskaa93',
                                          remote_bind_address=(
                                                  'countrynomics.mysql.pythonanywhere-services.com', 3306)) as tunnel:

            connection = pymysql.connect(host='127.0.0.1', user='countrynomics', passwd='countsql@',
                                         db='countrynomics$new_indicator',
                                         port=tunnel.local_bind_port)

            try:
                with connection.cursor() as cursor:
                    i = 0
                    for q in query_list:
                        print(i)
                        cursor.execute(query=q)
                        connection.commit()
                        i = i + 1
                    print(i)
                    print('Successful!')
            except:
                time.sleep(60)
                self.run_insert_query_pythonanywhere(query_list)

            finally:
                connection.close()
        return 'successfully uploaded'

    def run_insert_query(self, query_list: list):
        connection = self.__create_connection()
        cursor = connection.cursor()

        i = 0
        for q in query_list:
            cursor.execute(q)
            connection.commit()
            i = i + 1
        connection.close()
        print(str(i) + ' rows added')

    def run_read_query(self, query: str):
        conn = self.__create_connection()
        data = pd.read_sql(query, conn)
        return data


if __name__ == "__main__":
    a = AccessDB().run_read_query('select * from main_email')
    print(a)
