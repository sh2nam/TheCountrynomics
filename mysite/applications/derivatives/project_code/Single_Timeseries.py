# from Scripts.Economic_Data import EconomicData
from applications.derivatives.project_code.Economic_Data import EconomicData
import yaml
import os
import pandas as pd


class SingleTimeSeries:

    def __init__(self, api=False, indicator_call_setup=None):

        if indicator_call_setup:
            self.indicator_call_setup = indicator_call_setup
        else:
            self.indicator_call_setup = self.__create_display_name()

        if api:
            self.query = EconomicData().download_api_economic_data
        else:
            self.query = EconomicData().download_db_economic_data

    @staticmethod
    def __create_display_name():
        conf = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config_indicator_call.yaml')),
                      Loader=yaml.FullLoader)
        dic = conf['Single Time Series Setup']
        for ind in dic:
            display_name = ind
            if 'Prefix' in dic[ind].keys():
                display_name = dic[ind]['Prefix'] + ': ' + display_name
            dic[ind]['Display Name'] = display_name
        conf['Single Time Series Setup'] = dic
        return conf

    def get_display_names(self, indicator=None):
        d = self.indicator_call_setup['Single Time Series Setup']
        if indicator:
            return d[indicator]['Display Name']
        else:
            l = []
            for indicator in d:
                l.append(d[indicator]['Display Name'])
            l.sort()
            return l

    def get_g20_countries(self):
        conf = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config_country.yaml')),
                         Loader=yaml.FullLoader)
        return conf['g20_country_list']

    def __get_input(self, display_name: str):
        d = self.indicator_call_setup['Single Time Series Setup']
        country_exception = []
        fixed_freq = None
        flow = None
        ind_name = ''

        for ind in d:
            if d[ind]['Display Name'] == display_name:
                if 'Original Indicator Name' in d[ind].keys():
                    ind_name = d[ind]['Original Indicator Name']
                else:
                    ind_name = ind
                if 'Flow' in d[ind].keys():
                    flow = d[ind]['Flow']
                if 'Country Exception' in d[ind].keys():
                    country_exception = d[ind]['Country Exception']
                if 'Frequency Fix' in d[ind].keys():
                    fixed_freq = d[ind]['Frequency Fix']

        return country_exception, ind_name, fixed_freq, flow

    def get_timeseries(self, country: str, display_name: str, start_date=None, end_date=None, freq='A'):
        # get indicator requirement
        country_exception, ind_name, fixed_freq, flow = self.__get_input(display_name)
        if country in country_exception:
            return pd.DataFrame()
        if fixed_freq:
            freq = fixed_freq

        # call data
        df = self.query(country=country, indicator_list=[ind_name], start_date=start_date, end_date=end_date, freq=freq, flow=flow)
        df.rename(columns={ind_name: country + ' - ' + ind_name}, inplace=True)

        return df

    def get_timeseries_multiple_countries(self, display_name: str, country_list=None, date=None):
        if not country_list:
            # TODO: Need to use external variable file!!
            country_list = ['Argentina', 'Australia', 'Brazil', 'Canada', 'China', 'France', 'Germany', 'India',
                            'Indonesia', 'Italy', 'Japan', 'Mexico', 'Russia', 'Saudi Arabia', 'South Africa',
                            'South Korea', 'Turkey', 'United Kingdom', 'United States']

        l = []

        for country in country_list:
            df = self.get_timeseries(country, display_name, end_date=date)
            if not df.empty:
                df = df.tail(1)
                df.rename(columns={df.columns[0]: country}, inplace=True)
                df = df.T
                df.rename(columns={df.columns[0]: display_name}, inplace=True)
                df.index.name = "Country"
                l.append(df)
        df = pd.concat(l, axis=0)
        df.rename(columns={df.columns[0]: display_name}, inplace=True)

        return df



if __name__ == "__main__":
    count = ['Argentina', 'Australia', 'Brazil', 'Canada', 'China', 'France', 'Germany', 'India',
             'Indonesia', 'Italy', 'Japan', 'Mexico', 'Russia', 'Saudi Arabia', 'South Africa',
             'South Korea', 'Turkey', 'United Kingdom', 'United States']

    print(SingleTimeSeries().get_g20_countries())
    # l = SingleTimeSeries("a").get_display_names()
    # for c in count:
    #     for i in l:
    #         print(i)
    #         print(SingleTimeSeries().get_timeseries(c, i, freq='Q'))
