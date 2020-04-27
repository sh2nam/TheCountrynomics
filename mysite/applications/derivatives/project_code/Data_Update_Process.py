# from Scripts.Access_DB import AccessDB
from applications.derivatives.project_code.Access_DB import DownloadDbnomicsAPIData
# from Scripts.Economic_Data import EconomicData
from applications.derivatives.project_code.Economic_Data import EconomicData
import pandas as pd
from datetime import timedelta
import time


class DataUpdateProcess:

    @staticmethod
    def __get_latest_data(table_name='derivatives_economicindicatorstandard'):
        """
        derivatives_economicindicatorcounterparty
        get the latest data from sql database for a given table
        :param table_name: str
        :return: df
        """
        # create query and get data
        query = 'SELECT * FROM ' + table_name
        df = AccessDB().run_read_query(query)

        if table_name == 'derivatives_economicindicatorstandard':
            df = pd.DataFrame(df.groupby(['dbcode', 'indicator', 'country', 'freq', 'flow'])['date'].max())
        else:
            df = pd.DataFrame(df.groupby(['dbcode', 'indicator', 'country', 'freq', 'counter_party'])['date'].max())
        df.reset_index(inplace=True)
        return df

    @staticmethod
    def __call_api_data(row: str, table_name: str):
        """
        get api data
        :param row:
        :param table_name:
        :return:
        """
        if table_name == 'derivatives_economicindicatorstandard':
            df = EconomicData(True).download_api_economic_data(row['country'], [row['indicator']], row['date'], None,
                                                               row['freq'], None,
                                                               row['flow'] if row['flow'] in ['X', 'M'] else None)
        else:
            df = EconomicData(True).download_api_economic_data(row['country'], [row['indicator']], row['date'], None,
                                                               row['freq'], [row['counter_party']], None)
        print(df)
        return df

    def __get_updated_data(self, table_name='derivatives_economicindicatorstandard'):
        """
        get the latest date for each data, then get any data updated later from api
        :param table_name: str
        :return: df
        """
        # get the latest data and add 1 day to date column
        df = self.__get_latest_data(table_name)
        df['date'] = pd.to_datetime(df['date']) + timedelta(days=1)
        df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

        # get updated data
        result = []
        df.apply(lambda row: result.append(self.__call_api_data(row, table_name)), axis=1)
        df = pd.concat(result, sort=True)
        df['Date'] = df['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
        return df

    @staticmethod
    def __get_sql_insert_query_list(df: pd.DataFrame, table_name: str):
        """
        returns list of sql insert queries for the given dataframe
        :param df: pd.DataFrame
        :return: list
        """
        # TODO: check df is unique
        query_list = []
        for index, row in df.iterrows():
            date = row['Date']
            update_date = row['update_date']
            db_code = row['dbcode']
            indicator = row['indicator']
            value = row['value']
            freq = row['freq']
            country = row['country']

            if 'counter_party' in list(row.keys()):
                cp = row['counter_party']
                query = "INSERT INTO {table} (date, dbcode, indicator, country, freq, value, counter_party, update_date) VALUES ('{date}', '{dbcode}', " \
                        "'{indicator}', '{country}', '{freq}', {value}, '{cp}', '{update_date}')". \
                    format(date=date, dbcode=db_code, indicator=indicator, country=country,
                           freq=freq, value=value, table=table_name, cp=cp, update_date=update_date)
            else:
                flow = row['flow']
                query = "INSERT INTO {table} (date, dbcode, indicator, country, freq, value, update_date, flow) VALUES ('{date}', '{dbcode}', " \
                        "'{indicator}', '{country}', '{freq}', {value}, '{update_date}', '{flow}')". \
                    format(date=date, dbcode=db_code, indicator=indicator, country=country,
                           freq=freq, value=value, table=table_name, update_date=update_date, flow=flow)
            query_list.append(query)

        return query_list

    def upload_new_data_sqlite_db(self, table_name: str, function_names: []):
        """
        update new timeseries data to sqlite db input table name and list of function names
        :param table_name:
        :param function_names:
        :return:
        """
        df_list = []
        for func in function_names:
            # TODO: use config file for country names!!!
            for country in ['Argentina', 'Australia', 'Brazil', 'Canada', 'China', 'France', 'Germany', 'India',
                   'Indonesia', 'Italy', 'Japan', 'Mexico', 'Russia', 'Saudi Arabia', 'South Africa', 'South Korea',
                   'Turkey', 'United Kingdom', 'United States']:
                f = 'EconomicIndicatorQuery(api=True, db_format=True).' + func + "('" + country + "')"
                df = eval(f)
                df_list.append(df)
        df = pd.concat(df_list)

        # get list of sql queries to insert to sqlite db
        print('start creating queries')
        q_list = self.__get_sql_insert_query_list(df, table_name)

        # insert data to sqlite
        print('start inserting data')
        AccessDB().run_insert_query(q_list)

        return 'Process Completed'

    def update_updated_data_sqlite_db(self, table_name: str):
        """
        update updated api data to sqlite db
        :param table_name: str
        :return:
        """
        # go through indicators and get updated data in dataframe
        print('start downloading queries')
        df = self.__get_updated_data(table_name)
        print('api download completed')

        # get list of sql queries to insert to sqlite db
        print('start creating queries')
        q_list = self.__get_sql_insert_query_list(df, table_name)

        # insert data to sqlite
        print('start inserting data')
        AccessDB().run_insert_query(q_list)
        return 'Process Completed'

    def update_sqlite_data_pythonanywhere_db(self, table_name: str, update_date: str):
        """
        update sqlite db data to pythonanywhere_db
        :param update_date: str
        :return: df
        """
        q = "SELECT * FROM {table} WHERE update_date='{update_date}'".format(table=table_name, update_date=update_date)
        df = AccessDB().run_read_query(q)
        df.rename(columns={'date': 'Date'}, inplace=True)

        # create insert query list
        insert_q = self.__get_sql_insert_query_list(df, table_name)

        while insert_q:
            if len(insert_q) > 1500:
                insert_list = insert_q[:1500]
                insert_q = insert_q[1500:]
            else:
                insert_list = insert_q
                insert_q = []
            AccessDB(False).run_insert_query(insert_list)
            time.sleep(30)
        return 'Insertion Fully Completed'


if __name__ == "__main__":
    z = []
    a = DataUpdateProcess().update_sqlite_data_pythonanywhere_db('derivatives_economicindicatorstandard', '2019-11-14')
    print(a)
