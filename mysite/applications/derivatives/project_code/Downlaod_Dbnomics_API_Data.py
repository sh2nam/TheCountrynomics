import quandl
import pandas as pd
import dbnomics
import os
import yaml


class DownloadDbnomicsAPIData:
    def __init__(self):
        # Quandl key
        self.quandl_api_key = 'rzeAfzNCd2KwEkfV_i1U'

        # Load two config files
        self.config_country = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config_country.yaml')),
                                        Loader=yaml.FullLoader)
        self.config_indicator = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config_indicator.yaml')),
                                          Loader=yaml.FullLoader)

        # Get country, indicator codes and country-indicator mapping
        self.country_code = self.config_country['country_code']
        self.source_country_code_mapping = self.config_country['source_country_code_mapping']
        self.indicator_info = self.config_indicator['indicator_setting']

    def create_quandl_code(self, country: str, indicator: str) -> str:
        """
        returns Quandl code
        :param country: str
        :param indicator: str
        :return: str
        """
        provider_code = self.indicator_info[indicator]['provider_code']
        country_code = self.__get_country_code(country, provider_code)
        indicator_code = self.indicator_info[indicator]['indicator_code']
        return provider_code + '/' + country_code + "_" + indicator_code

    def get_dbnomics_code(self, country: str, indicator: str, freq='A', counterparty=None, flow=None) -> str:
        """
        create dbnomics code to fetch data
        :param country: str
        :param indicator: str
        :param freq: 'A', 'Q', or 'M'
        :param counterparty: str
        :param flow: M for import, X for export
        :return: str
        """
        # get all required codes
        provider_code = self.indicator_info[indicator]['provider_code']
        if 'source_code' in list(self.indicator_info[indicator].keys()):
            source_code = self.indicator_info[indicator]['source_code']
        else:
            source_code = None
        indicator_code = self.indicator_info[indicator]['indicator_code']
        country_code = self.__get_country_code(country, provider_code)

        if provider_code == 'WTO':
            freq = 'a2'
            code = provider_code + '/' + freq + '/' + country_code + '.' + flow + '.' + indicator_code
        elif source_code == "WDI":
            code = provider_code + '/' + source_code + '/' + indicator_code + '-' + country_code
        elif source_code == 'MEI':
            code = provider_code + "/" + source_code + "/" + country_code + "." + indicator_code + "." + freq
        else:
            code = provider_code + "/" + source_code + "/" + freq + "." + country_code + "." + indicator_code
            if counterparty:
                cp_code = self.__get_country_code(counterparty, provider_code)
                code = code + '.' + cp_code
        return code

    def __get_country_code(self, country: str, provider_code: str):
        """
        determine country code using country name and source code
        :param country: str
        :param provider_code: str
        :return:
        """
        country_code_lookup = self.source_country_code_mapping[provider_code]
        return self.country_code[country][country_code_lookup]

    @ staticmethod
    def __get_appropriate_date(start_date=None, end_date=None):
        """
        produce appropriate start date and end date
        :param start_date:
        :param end_date:
        :return:
        """
        # set start_date as min date and end_date as max date
        if not start_date:
            start_date = '1930-01-01'
        if not end_date:
            end_date = '2100-01-01'
        return pd.to_datetime(start_date), pd.to_datetime(end_date)

    def __update_fetched_data(self, df: pd.DataFrame(), indicator: str, start_date=None, end_date=None, freq='A') -> pd.DataFrame():
        """
        normalize fetched data: update column names, scale, date format
        :param df: DataFrame
        :param indicator: str
        :return: DataFrame
        """
        # update column names, drop values other than date/value, set date as index, update date format,
        # resample, filter on dates, drop na
        df.rename(columns={'period': 'Date'}, inplace=True)
        df = df[['Date', 'value']]
        df.set_index(['Date'], inplace=True)
        df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
        df = df.resample(freq, convention='end').last()
        start_date, end_date = self.__get_appropriate_date(start_date, end_date)
        df = df[(df.index >= start_date) & (df.index <= end_date)]
        df = df.dropna()
        df.sort_index(ascending=True, inplace=True)

        # scale values
        if 'scale' in self.indicator_info[indicator].keys():
            df = df.copy()
            df['value'] = df['value'] * self.indicator_info[indicator]['scale']

        return df

    @staticmethod
    def __format_dataframe(df: pd.DataFrame(), country: str, indicator: str, db_code: str, freq='A', counterparty=None):
        """
        transform data to df to db uploadable format
        :param country:
        :param indicator:
        :param db_code:
        :param freq:
        :return:
        """
        if df.empty:
            return df
        df['dbcode'] = db_code
        df['indicator'] = indicator
        df['freq'] = freq
        df['country'] = country
        if counterparty:
            df['counter_party'] = counterparty
        return df

    def get_quandl_data(self, country: str, indicator_list: list, start_date=None, end_date=None) -> pd.DataFrame:
        """
        :param country: one of the country name from G20 country
        :param indicator_list: indicator list
        :param start_date: str
        :param end_date: str
        :return: DataFrame
        """
        result = []
        for indicator in indicator_list:
            quandl_code = self.create_quandl_code(country, indicator)

            try:
                df = quandl.get(quandl_code, authtoken=self.quandl_api_key, start_date=start_date, end_date=end_date)
                df.reset_index(inplace=True)
                df.rename(columns={'Value': 'value'}, inplace=True)

            except:
                raise Exception("Cannot find " + country + " - " + indicator + " data from Quandl")

            # update date type, column name, and scale value
            df = self.__update_fetched_data(df, indicator, start_date=start_date, end_date=end_date)
            df = self.__format_dataframe(df, country, indicator, quandl_code, 'A')
            result.append(df)
        return pd.concat(result, axis=0)

    def get_dbnomics_data(self, country: str, indicator_list: list, start_date=None, end_date=None, freq='A',
                          counterparty=None, flow=None) -> pd.DataFrame:
        """
        get api data from dbnomics website
        :param country: str
        :param indicator_list: str
        :param freq: 'Q', 'A', or 'M'
        :param start_date: 'yyyy-mm-dd'
        :param end_date: 'yyyy-mm-dd'
        :param counterparty: str
        :param flow: 'M' for import, 'X' for export
        :return: Data Frame
        """
        result = []
        for indicator in indicator_list:
            dbnomics_code = self.get_dbnomics_code(country, indicator, freq, counterparty, flow)

            # fetch data from dbnomics, update fetched data
            try:
                df = dbnomics.fetch_series(dbnomics_code)
                df = self.__update_fetched_data(df, indicator, start_date, end_date, freq=freq)

            except:
                if dbnomics_code in ['IMF/BOP/A.CA.BSM_BP6_USD', 'IMF/BOP/A.ID.BSTV_BP6_USD', 'IMF/BOP/A.SA.BSR_BP6_USD',
                                     'IMF/BOP/A.SA.BSM_BP6_USD', 'IMF/BOP/A.SA.BSOPCR_BP6_USD',
                                     'IMF/BOP/Q.CA.BSM_BP6_USD', 'IMF/BOP/Q.ID.BSTV_BP6_USD', 'IMF/BOP/Q.SA.BSR_BP6_USD',
                                     'IMF/BOP/Q.SA.BSM_BP6_USD', 'IMF/BOP/Q.SA.BSOPCR_BP6_USD'
                                     ]:
                    pass
                else:
                    # TODO: use pass when dbnomics connection is stable!
                    return self.get_dbnomics_data(country, indicator, start_date, end_date, freq, counterparty, flow)
            df = self.__format_dataframe(df, country, indicator, dbnomics_code, freq, counterparty)
            result.append(df)
        return pd.concat(result, axis=0)


if __name__ == "__main__":

    a = DownloadDbnomicsAPIData(True).get_quandl_data("South Korea", 'Real GDP (LCU Bil)', None, None)
    print(a)
