# from Scripts.Downlaod_Dbnomics_API_Data import DownloadDbnomicsAPIData
from applications.derivatives.project_code.Downlaod_Dbnomics_API_Data import DownloadDbnomicsAPIData
# from Scripts.Access_DB import AccessDB
from applications.derivatives.project_code.Access_DB import AccessDB
import datetime
from multiprocessing import Pool
import itertools
import pandas as pd


class EconomicData:
    def __init__(self, db_format=False):

        # API / DB connection
        self.d_api = DownloadDbnomicsAPIData()
        self.d_db = AccessDB()

        # Output in DB Format
        self.db_format = db_format

        # Quandl list - Indicators from Quandl
        self.quandl_list = ['Real GDP Growth', 'Real GDP (LCU Bil)', 'Real GDP per Capita (LCU)', 'Real GNI (LCU Bil)',
                            'Government Expenditure (% GDP)', 'Savings (% GDP)', 'Investment (% GDP)', 'Net Export (% GDP)']

        # DB Table Name:
        self.table_standard = 'derivatives_economicindicatorstandard'
        self.table_counterparty = 'derivatives_economicindicatorcounterparty'

    def __handle_counterparties(self, country: str, indicator: str, start_date=None, end_date=None, freq='A',
                                counterparty_list=None, flow=None):

        input = list(itertools.product([country], [[indicator]], [start_date], [end_date], [freq], counterparty_list,
                                       [flow]))
        with Pool() as pool:
            result = pool.starmap(self.d_api.get_dbnomics_data, input)
        df = pd.concat(result, axis=0)
        return df

    def download_api_economic_data(self, country: str, indicator_list: list, start_date=None, end_date=None, freq='A',
                                   counterparty_list=None, flow=None):
        """
        download api data from either Quandl or Dbnomics and output in reportable DataFrame format
        :param country:
        :param indicator_list:
        :param freq:
        :param start_date:
        :param end_date:
        :param counterparty_list:
        :param flow:
        :return:
        """
        if counterparty_list:
            # todo: counterparty list should only have one indicator. Raise Error if not!
            df = self.__handle_counterparties(country, indicator_list[0], start_date, end_date, freq, counterparty_list,
                                              flow)
        else:
            quandl_indicator_list = []
            dbnomics_indicator_list = []
            for indicator in indicator_list:
                if indicator in self.quandl_list:
                    quandl_indicator_list.append(indicator)
                else:
                    dbnomics_indicator_list.append(indicator)
            result = []
            if quandl_indicator_list:
                result.append(self.d_api.get_quandl_data(country, quandl_indicator_list, start_date, end_date))
            if dbnomics_indicator_list:
                result.append(self.d_api.get_dbnomics_data(country, dbnomics_indicator_list, start_date, end_date, freq, counterparty_list, flow))
            df = pd.concat(result, axis=0)
        df.reset_index(inplace=True)
        df = self.__reorganize_df_format(df)
        return df

    def __create_db_economic_data_query(self, country: str, indicator_list: [], start_date=None, end_date=None, freq='A',
                                        counterparty_list=None, flow=None) -> str:
        """
        download db economic data query
        :param country:
        :param indicator_list:
        :param freq:
        :param start_date:
        :param end_date:
        :param counterparty_list:
        :param flow:
        :return:
        """
        # Create Data Condition
        date_condition = ''
        if start_date:
            date_condition = date_condition + " AND date >= '{start_date}'".format(start_date=start_date)

        if end_date:
            date_condition = date_condition + " AND date <= '{end_date}'".format(end_date=end_date)

        if counterparty_list:
            db_code = []
            # todo: counterparty list should only have one indicator!!
            for cp in counterparty_list:
                db_code.append(self.d_api.get_dbnomics_code(country, indicator_list[0], freq, cp, flow))
            db_code = tuple(db_code)

            if self.db_format:
                col = '*'
            else:
                col = 'date, value, counter_party'
            q = "SELECT {col} FROM {table} WHERE dbcode IN {dbcode}".format(dbcode=db_code, table=self.table_counterparty,
                                                                            col=col) + date_condition
        else:
            db_code = []
            for indicator in indicator_list:
                if indicator in self.quandl_list:
                    db_code.append(self.d_api.create_quandl_code(country, indicator))
                else:
                    db_code.append(self.d_api.get_dbnomics_code(country, indicator, freq, None, flow))
            if len(db_code) > 1:
                db_code = tuple(db_code)
            else:
                db_code = "('" + db_code[0] + "')"
            if self.db_format:
                col = '*'
            else:
                col = 'date, value, indicator'
            q = "SELECT {col} FROM {table} WHERE dbcode IN {dbcode}".format(dbcode=db_code, table=self.table_standard,
                                                                            col=col) + date_condition
        return q

    def download_db_economic_data(self, country: str, indicator_list: [], start_date=None, end_date=None, freq='A',
                                  counterparty_list=None, flow=None):
        if counterparty_list:
            query = self.__create_db_economic_data_query(country, indicator_list, start_date, end_date, freq, counterparty_list, flow)

        else:
            # counterparty_list should be None # todo: raise error if not!
            query = self.__create_db_economic_data_query(country, indicator_list, start_date, end_date, freq, counterparty_list, flow)

        df = AccessDB().run_read_query(query)
        df.rename(columns={'date': 'Date'}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
        df = self.__reorganize_df_format(df.copy())
        return df

    def __reorganize_df_format(self, df):
        # todo: if db_format include update_date!
        if df.empty:
            return df

        if self.db_format:
            today = datetime.date.today()
            df['update_date'] = today.strftime('%Y-%m-%d')
            return df

        if 'counter_party' in df.columns:
            col_name = 'counter_party'
        else:
            col_name = 'indicator'
        df = df.pivot(index='Date', columns=col_name, values='value')

        return df


if __name__ == "__main__":
    import yaml
    import os

    a = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config_country.yaml')),
              Loader=yaml.FullLoader)
    cp_list = a['g20_country_list']
    cp_list.remove("South Korea")

    b = EconomicData().download_api_economic_data("South Korea", 'Automotive products (USD Mil)'
                                                  )
    print(b)
