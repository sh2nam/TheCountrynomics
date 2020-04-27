# from Scripts.Economic_Data import EconomicData
from applications.derivatives.project_code.Economic_Data import EconomicData
import pandas as pd
import yaml
import os



class EconomicIndicatorQuery:
    def __init__(self, api=True, db_format=False):
        if api:
            self.query = EconomicData(db_format=db_format).download_api_economic_data
        else:
            self.query = EconomicData(db_format=db_format).download_db_economic_data

        self.config_country = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config_country.yaml')),
                                        Loader=yaml.FullLoader)
        self.g20_country_list = self.config_country['g20_country_list']

        self.db_format = db_format

        # Frequently Repeated functions:
        self.population_number = None
        self.labour_force_number = None
        self.bop_import = None
        self.bop_export = None
        self.bop_current_account = None
        self.bop_financial_account = None
        self.bop_services_net_export = None
        self.bop_portfolio_investment = None
        self.bop_direct_investment = None
        self.bop_other_investment = None
        self.bop_reserve_assets = None
        self.bop_portfolio_investment_assets = None
        self.bop_portfolio_investment_liabilities = None

    def get_unemployment_rate(self, country: str, start_date=None, end_date=None, freq='A'):
        exclusion_list = ['India']
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Unemployment Rate (% Labour Force)'], start_date=start_date,
                            end_date=end_date, freq=freq)
        else:
            df = pd.DataFrame()

        return df

    def get_population_number(self, country: str, start_date=None, end_date=None):
        if self.population_number is not None:
            return self.population_number
        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Population'], start_date=start_date, end_date=end_date)
        else:
            df = pd.DataFrame()

        self.population_number = df

        return self.population_number

    def get_labour_force_number(self, country: str, start_date=None, end_date=None):
        if self.labour_force_number is not None:
            return self.labour_force_number
        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Labour Force'], start_date=start_date, end_date=end_date)
        else:
            df = pd.DataFrame()
        self.labour_force_number = df
        return self.labour_force_number

    def get_real_gdp_growth(self, country: str, start_date=None, end_date=None):

        # TODO: create a separate growth function and use that!!
        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Real GDP Growth'], start_date=start_date, end_date=end_date)
        else:
            df = pd.DataFrame()

        return df

    def get_savings_gdp(self, country: str, start_date=None, end_date=None):
        exclusion_list = []
        if country in exclusion_list:
            return pd.DataFrame()
        df = self.query(country=country, indicator_list=['Savings (% GDP)'], start_date=start_date, end_date=end_date)

        return df

    def get_govmt_expenditure_gdp(self, country: str, start_date=None, end_date=None):

        # TODO: create a separate growth function and use that!!
        exclusion_list = []
        if country in exclusion_list:
            return pd.DataFrame()
        df = self.query(country=country, indicator_list=['Government Expenditure (% GDP)'], start_date=start_date, end_date=end_date)
        return df

    def get_investment_gdp(self, country: str, start_date=None, end_date=None):

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Investment (% GDP)'], start_date=start_date, end_date=end_date)
        else:
            df = pd.DataFrame()

        return df

    def get_net_export_gdp(self, country: str, start_date=None, end_date=None):

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Net Export (% GDP)'], start_date=start_date, end_date=end_date)
        return df

    def get_personal_consumption_gdp(self, country: str, start_date=None, end_date=None):
        """
        get personal consumption (% of GDP)
        :return: Data Frame
        """
        # get %GDP of government expenditure, investment, and net export
        govmt_exp = self.get_govmt_expenditure_gdp(country=country, start_date=start_date, end_date=end_date)
        investment = self.get_investment_gdp(country=country, start_date=start_date, end_date=end_date)
        net_export = self.get_net_export_gdp(country=country, start_date=start_date, end_date=end_date)

        # use other components of GDP to calculate personal consumption
        df = pd.concat([govmt_exp, investment, net_export], axis=1)
        df.dropna(inplace=True)
        df['Personal Consumption (% GDP)'] = 1 - df.sum(axis=1)
        return pd.DataFrame(df['Personal Consumption (% GDP)'])

    def get_real_gdp_number_lcu(self, country: str, start_date=None, end_date=None):

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Real GDP (LCU Bil)'], start_date=start_date, end_date=end_date)
        else:
            df = pd.DataFrame()
        return df

    def get_real_gni_number_lcu(self, country: str, start_date=None, end_date=None):

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Real GNI (LCU Bil)'], start_date=start_date, end_date=end_date)
        else:
            df = pd.DataFrame()

        return df

    def get_real_gdp_per_capita_lcu(self, country: str, start_date=None, end_date=None):

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Real GDP per Capita (LCU)'], start_date=start_date, end_date=end_date)
        else:
            df = pd.DataFrame()

        return df

    def get_dot_trade_bal_g20cp(self, country: str, start_date=None, end_date=None, freq='A', cp_list=[]):

        exclusion_list = []

        # if empty cp list use g20 country list
        if not cp_list:
            cp_list = self.g20_country_list
        if country in cp_list:
            cp_list.remove(country)

        df = self.query(country=country, indicator_list=['Goods Trade Balance (USD Mil)'], start_date=start_date,
                        end_date=end_date, freq=freq, counterparty_list=cp_list)
        return df

    def get_bop_current_account(self, country: str, start_date=None, end_date=None, freq='A'):
        if self.bop_current_account is not None:
            return self.bop_current_account

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Current Account (USD Mil)'], start_date=start_date,
                            end_date=end_date, freq=freq)
        else:
            df = pd.DataFrame()
        self.bop_current_account = df
        return self.bop_current_account

    def get_bop_financial_account(self, country: str, start_date=None, end_date=None, freq='A'):
        if self.bop_financial_account is not None:
            return self.bop_financial_account

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Financial Account (USD Mil)'], start_date=start_date,
                            end_date=end_date, freq=freq)
        else:
            df = pd.DataFrame()
        self.bop_financial_account = df
        return self.bop_financial_account

    def get_bop_portfolio_investment(self, country: str, start_date=None, end_date=None, freq='A'):
        if self.bop_portfolio_investment is not None:
            return self.bop_portfolio_investment
        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Portfolio Investment (USD Mil)'], start_date=start_date,
                            end_date=end_date, freq=freq)
        else:
            df = pd.DataFrame()

        self.bop_portfolio_investment = df
        return self.bop_portfolio_investment

    def get_bop_other_investment(self, country: str, start_date=None, end_date=None, freq='A'):
        if self.bop_other_investment is not None:
            return self.bop_other_investment
        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Other Investment (USD Mil)'], start_date=start_date,
                            end_date=end_date, freq=freq)
        else:
            df = pd.DataFrame()
        self.bop_other_investment = df
        return self.bop_other_investment

    def get_bop_direct_investment(self, country: str, start_date=None, end_date=None, freq='A'):

        if self.bop_direct_investment is not None:
            return self.bop_direct_investment

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Direct Investment (USD Mil)'], start_date=start_date,
                            end_date=end_date, freq=freq)
        else:
            df = pd.DataFrame()
        self.bop_direct_investment = df
        return self.bop_direct_investment

    def get_bop_reserve_assets(self, country: str, start_date=None, end_date=None, freq='A'):
        if self.bop_reserve_assets is not None:
            return self.bop_reserve_assets
        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Reserve Assets (USD Mil)'], start_date=start_date,
                            end_date=end_date, freq=freq)
        else:
            df = pd.DataFrame()
        self.bop_reserve_assets = df
        return self.bop_reserve_assets

    def get_bop_financial_derivatives_and_other(self, country: str, start_date=None, end_date=None, freq='A'):

        # get other elements of financial account
        fin_act_df = self.get_bop_financial_account(country=country, start_date=start_date, end_date=end_date, freq=freq)
        port_inv_df = self.get_bop_portfolio_investment(country=country, start_date=start_date, end_date=end_date, freq=freq)
        dir_inv_df = self.get_bop_direct_investment(country=country, start_date=start_date, end_date=end_date, freq=freq)
        other_inv_df = self.get_bop_other_investment(country=country, start_date=start_date, end_date=end_date, freq=freq)
        reserve_df = self.get_bop_reserve_assets(country=country, start_date=start_date, end_date=end_date, freq=freq)
        df = pd.concat([port_inv_df, dir_inv_df, other_inv_df, reserve_df], axis=1)
        if not df.empty:
            df['Sum'] = df.sum(axis=1)
            df = pd.concat([df, fin_act_df], axis=1)
            df['Financial Derivatives & Other (USD Mil)'] = df[fin_act_df.columns[0]] - df['Sum']
            df = df[['Financial Derivatives & Other (USD Mil)']]
        return df

    def get_bop_capital_account(self, country: str, start_date=None, end_date=None, freq='A'):

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Capital Account (USD Mil)'], start_date=start_date,
                            end_date=end_date, freq=freq)
        else:
            df = pd.DataFrame()

        return df

    def get_bop_primary_income(self, country: str, start_date=None, end_date=None, freq='A'):

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Primary Income (USD Mil)'], start_date=start_date,
                            end_date=end_date, freq=freq)
        else:
            df = pd.DataFrame()

        return df

    def get_bop_secondary_income(self, country: str, start_date=None, end_date=None, freq='A'):

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Secondary Income (USD Mil)'], start_date=start_date,
                            end_date=end_date, freq=freq)
        else:
            df = pd.DataFrame()

        return df

    def get_bop_goods_net_export(self, country: str, start_date=None, end_date=None, freq='A'):

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Goods Net Export (USD Mil)'], start_date=start_date,
                            end_date=end_date, freq=freq)
        else:
            df = pd.DataFrame()

        return df

    def get_bop_services_net_export(self, country: str, start_date=None, end_date=None, freq='A'):
        if self.bop_services_net_export is not None:
            return self.bop_services_net_export
        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Services Net Export (USD Mil)'], start_date=start_date,
                            end_date=end_date, freq=freq)
        else:
            df = pd.DataFrame()
        self.bop_services_net_export = df
        return self.bop_services_net_export

    def get_bop_net_export(self, country: str, start_date=None, end_date=None, freq='A'):

        exclusion_list = []

        # todo: externalize variables??
        bop_import = self.get_bop_import(country=country, start_date=start_date, end_date=end_date, freq=freq)
        bop_export = self.get_bop_export(country=country, start_date=start_date, end_date=end_date, freq=freq)
        df = pd.concat([bop_import, -bop_export], axis=1)
        df = pd.DataFrame(df.sum(axis=1))
        df.columns = ['Net Export (USD Mil)']

        return df

    def get_bop_import(self, country: str, start_date=None, end_date=None, freq='A'):

        if self.bop_import is not None:
            return self.bop_import

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Import (USD Mil)'], start_date=start_date, end_date=end_date,
                            freq=freq)
        else:
            df = pd.DataFrame()
        self.bop_import = df
        return self.bop_import

    def get_bop_export(self, country: str, start_date=None, end_date=None, freq='A'):
        if self.bop_export is not None:
            return self.bop_export

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Export (USD Mil)'], start_date=start_date, end_date=end_date,
                            freq=freq)
        else:
            df = pd.DataFrame()
        self.bop_export = df
        return self.bop_export

    def get_bop_services_net_export_breakdown(self, country: str, start_date=None, end_date=None, freq='A', breakdown_list=[]):
        """
        get services net export breakdown
        :param freq:
        :return:
        """
        if not breakdown_list:
            breakdown_list = ['Intellectual Property Charges (USD Mil)', 'Construction (USD Mil)',
                              'Financial Services (USD Mil)', 'Government Goods & Services (USD Mil)',
                              'Insurance and Pension Services (USD Mil)', 'Maintainence and Repair Services (USD Mil)',
                              'Manufacturing Services (USD Mil)',
                              'Other Business (Consulting, R&D, etc.) Services (USD Mil)',
                              'Personal, Cultural, and Recreational Services (USD Mil)',
                              'Telecommunications, Computer, and Info Services (USD Mil)', 'Transport (USD Mil)',
                              'Travel (USD Mil)']

        df = self.query(country, breakdown_list, start_date, end_date, freq)

        return df

    def get_wto_goods_import_breakdown(self, country: str, start_date=None, end_date=None, breakdown_list=[]):
        if not breakdown_list:
            breakdown_list = ['Automotive products (USD Mil)', 'Chemicals (USD Mil)', 'Clothing (USD Mil)',
                              'Electronic data processing and office equipment (USD Mil)',
                              'Food and Agricultural products (USD Mil)', 'Fuels and mining products (USD Mil)',
                              'Integrated circuits and electronic components (USD Mil)', 'Iron and steel (USD Mil)',
                              'Machinery and transport equipment (USD Mil)', 'Manufactures (USD Mil)',
                              'Office and telecom equipment (USD Mil)', 'Pharmaceuticals (USD Mil)',
                              'Telecommunications equipment (USD Mil)', 'Textiles (USD Mil)']
        df = self.query(country, breakdown_list, start_date, end_date, 'A', None, 'M')
        return df

    def get_wto_goods_export_breakdown(self, country: str, start_date=None, end_date=None, breakdown_list=[]):
        if not breakdown_list:
            breakdown_list = ['Automotive products (USD Mil)', 'Chemicals (USD Mil)', 'Clothing (USD Mil)',
                              'Electronic data processing and office equipment (USD Mil)',
                              'Food and Agricultural products (USD Mil)', 'Fuels and mining products (USD Mil)',
                              'Integrated circuits and electronic components (USD Mil)', 'Iron and steel (USD Mil)',
                              'Machinery and transport equipment (USD Mil)', 'Manufactures (USD Mil)',
                              'Office and telecom equipment (USD Mil)', 'Pharmaceuticals (USD Mil)',
                              'Telecommunications equipment (USD Mil)', 'Textiles (USD Mil)']
        df = self.query(country, breakdown_list, start_date, end_date, 'A', None, 'X')
        return df

    def get_wto_goods_net_export_breakdown(self, country: str, start_date=None, end_date=None, breakdown_list=[]):
        exp_df = self.get_wto_goods_export_breakdown(country, start_date, end_date, breakdown_list)
        imp_df = self.get_wto_goods_import_breakdown(country, start_date, end_date, breakdown_list)

        # net export df
        df = pd.DataFrame()
        if not exp_df.empty:
            df = exp_df - imp_df
        return df

    def get_ifs_import_price_index(self, country: str, start_date=None, end_date=None, freq='A'):

        exclusion_list = ['Argentina', 'China', 'India', 'Italy', 'Russia', 'Saudi Arabia', 'Turkey']
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Import Price Index'], start_date=start_date, end_date=end_date,
                            freq=freq)
        else:
            df = pd.DataFrame()

        return df

    def get_ifs_export_price_index(self, country: str, start_date=None, end_date=None, freq='A'):

        exclusion_list = ['Argentina', 'China', 'India', 'Italy', 'Russia', 'Saudi Arabia', 'Turkey']
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Export Price Index'], start_date=start_date, end_date=end_date,
                            freq=freq)
        else:
            df = pd.DataFrame()

        return df

    def get_bop_direct_investment_assets(self, country: str, start_date=None, end_date=None, freq='A'):

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['FDI - Assets (USD Mil)'], start_date=start_date, end_date=end_date,
                            freq=freq)
        else:
            df = pd.DataFrame()

        return df

    def get_bop_direct_investment_liabilities(self, country: str, start_date=None, end_date=None, freq='A'):

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['FDI - Liabilities (USD Mil)'], start_date=start_date, end_date=end_date,
                            freq=freq)
        else:
            df = pd.DataFrame()

        return df

    def get_bop_portfolio_investment_assets(self, country: str, start_date=None, end_date=None, freq='A'):
        if self.bop_portfolio_investment_assets is not None:
            return self.bop_portfolio_investment_assets
        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Portfolio Investment - Assets (USD Mil)'], start_date=start_date, end_date=end_date,
                            freq=freq)
        else:
            df = pd.DataFrame()
        self.bop_portfolio_investment_assets = df
        return self.bop_portfolio_investment_assets

    def get_bop_portfolio_investment_liabilities(self, country: str, start_date=None, end_date=None, freq='A'):
        if self.bop_portfolio_investment_liabilities is not None:
            self.bop_portfolio_investment_liabilities
        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Portfolio Investment - Liabilities (USD Mil)'], start_date=start_date, end_date=end_date,
                            freq=freq)
        else:
            df = pd.DataFrame()
        self.bop_portfolio_investment_liabilities = df
        return self.bop_portfolio_investment_liabilities

    def get_bop_portfolio_investment_assets_eq(self, country: str, start_date=None, end_date=None, freq='A'):

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Assets, Portfolio Investment - Equity (USD Mil)'], start_date=start_date, end_date=end_date,
                            freq=freq)
        else:
            df = pd.DataFrame()

        return df

    def get_bop_portfolio_investment_assets_debt(self, country: str, start_date=None, end_date=None, freq='A'):

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Assets, Portfolio Investment - Debt Securities (USD Mil)'], start_date=start_date, end_date=end_date,
                            freq=freq)
        else:
            df = pd.DataFrame()

        return df

    def get_bop_portfolio_investment_liabilities_eq(self, country: str, start_date=None, end_date=None, freq='A'):

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Liabilities, Portfolio Investment - Equity (USD Mil)'], start_date=start_date, end_date=end_date,
                            freq=freq)
        else:
            df = pd.DataFrame()

        return df

    def get_bop_portfolio_investment_liabilities_debt(self, country: str, start_date=None, end_date=None, freq='A'):

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Liabilities, Portfolio Investment - Debt Securities (USD Mil)'], start_date=start_date, end_date=end_date,
                            freq=freq)
        else:
            df = pd.DataFrame()

        return df

    def get_cpis_portfolio_investment_assets_equity_counter_parties(self, country: str, start_date=None, end_date=None, cp_list=None):

        exclusion_list = []

        # if empty cp list use g20 country list
        if not cp_list:
            cp_list = self.g20_country_list
        if country in cp_list:
            cp_list.remove(country)

        df = self.query(country=country, indicator_list=['Counter Party, Assets, Portfolio Investment - Equity (USD Mil)'], start_date=start_date,
                        end_date=end_date, counterparty_list=cp_list)
        return df

    def get_cpis_portfolio_investment_liabilities_equity_counter_parties(self, country: str, start_date=None, end_date=None, cp_list=None):

        exclusion_list = []

        # if empty cp list use g20 country list
        if not cp_list:
            cp_list = self.g20_country_list
        if country in cp_list:
            cp_list.remove(country)

        df = self.query(country=country, indicator_list=['Counter Party, Liabilities, Portfolio Investment - Equity (USD Mil)'], start_date=start_date,
                        end_date=end_date, counterparty_list=cp_list)
        return df

    def get_cpis_portfolio_investment_assets_debt_counter_parties(self, country: str, start_date=None, end_date=None, cp_list=None):

        exclusion_list = []

        # if empty cp list use g20 country list
        if not cp_list:
            cp_list = self.g20_country_list
        if country in cp_list:
            cp_list.remove(country)

        df = self.query(country=country, indicator_list=['Counter Party, Assets, Portfolio Investment - Debt Securities (USD Mil)'], start_date=start_date,
                        end_date=end_date, counterparty_list=cp_list)
        return df

    def get_cpis_portfolio_investment_liabilities_debt_counter_parties(self, country: str, start_date=None, end_date=None, cp_list=None):

        exclusion_list = []

        # if empty cp list use g20 country list
        if not cp_list:
            cp_list = self.g20_country_list
        if country in cp_list:
            cp_list.remove(country)

        df = self.query(country=country, indicator_list=['Counter Party, Liabilities, Portfolio Investment - Debt Securities (USD Mil)'], start_date=start_date,
                        end_date=end_date, counterparty_list=cp_list)
        return df

    def get_cpis_portfolio_investment_assets_counter_parties(self, country: str, start_date=None, end_date=None, cp_list=None):

        exclusion_list = []

        # if empty cp list use g20 country list
        if not cp_list:
            cp_list = self.g20_country_list
        if country in cp_list:
            cp_list.remove(country)

        df = self.query(country=country, indicator_list=['Counter Party, Assets, Portfolio Investment (USD Mil)'], start_date=start_date,
                        end_date=end_date, counterparty_list=cp_list)
        return df

    def get_cpis_portfolio_investment_liabilities_counter_parties(self, country: str, start_date=None, end_date=None, cp_list=None):

        exclusion_list = []

        # if empty cp list use g20 country list
        if not cp_list:
            cp_list = self.g20_country_list
        if country in cp_list:
            cp_list.remove(country)

        df = self.query(country=country, indicator_list=['Counter Party, Liabilities, Portfolio Investment (USD Mil)'], start_date=start_date,
                        end_date=end_date, counterparty_list=cp_list)
        return df

    def get_bop_reserve_assets_total(self, country: str, start_date=None, end_date=None, freq='A'):

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Assets, Reserve Assets (USD Mil)'], start_date=start_date, end_date=end_date,
                            freq=freq)
        else:
            df = pd.DataFrame()

        return df

    def get_bop_reserve_assets_gold(self, country: str, start_date=None, end_date=None, freq='A'):

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Reserve Assets - Monetary Gold (USD Mil)'], start_date=start_date, end_date=end_date,
                            freq=freq)
        else:
            df = pd.DataFrame()
        return df

    def get_bop_reserve_assets_sdr(self, country: str, start_date=None, end_date=None, freq='A'):

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Reserve Assets - SDR (USD Mil)'], start_date=start_date, end_date=end_date,
                            freq=freq)
        return df

    def get_bop_reserve_assets_imf(self, country: str, start_date=None, end_date=None, freq='A'):

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Reserve Assets - IMF Reserve (USD Mil)'], start_date=start_date, end_date=end_date,
                            freq=freq)
        else:
            df = pd.DataFrame()
        return df

    def get_bop_reserve_assets_currency_securities(self, country: str, start_date=None, end_date=None, freq='A'):

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Reserve Assets - Currency, Securities, and Deposits (USD Mil)'], start_date=start_date, end_date=end_date,
                            freq=freq)
        else:
            df = pd.DataFrame()
        return df

    def get_cpi_all_items(self, country: str, start_date=None, end_date=None, freq='A'):

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['CPI - All Items'], start_date=start_date, end_date=end_date,
                            freq=freq)
        else:
            df = pd.DataFrame()

        return df

    def get_cpi_basket_items(self, country: str, start_date=None, end_date=None, breakdown_list=[]):
        exclusion_list = ['Indonesia', 'China', 'Brazil']
        if country in exclusion_list:
            return pd.DataFrame()

        if not breakdown_list:
            breakdown_list = ['CPI - Clothing', 'CPI - Communication', 'CPI - Education', 'CPI - Food&Beverages',
                              'CPI - Furnishings, Household Equipment&Maintenance', 'CPI - Health',
                              'CPI - Housing, Water, Gas, Electricity, Fuels', 'CPI - Miscellaneous Goods&Services',
                              'CPI - Recreation&Culture', 'CPI - Restaurants & Hotels', 'CPI - Transport']
        df = self.query(country, breakdown_list, start_date, end_date, 'A', None)

        return df

    def get_oecd_10y_govmt_bond_yield(self, country: str, start_date=None, end_date=None):

        exclusion_list = ['Argentina', 'Brazil', 'China', 'Indonesia', 'Saudi Arabia', 'Turkey']
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['10Y Govmt Bond Yield'], start_date=start_date, end_date=end_date, freq='M')
        else:
            df = pd.DataFrame()

        return df

    def get_oecd_3M_interbank_rates(self, country: str, start_date=None, end_date=None):

        exclusion_list = ['Argentina', 'Brazil', 'China', 'Indonesia', 'Saudi Arabia', 'Turkey']
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['3M Interbank Rates'], start_date=start_date, end_date=end_date, freq='M')
        else:
            df = pd.DataFrame()

        return df

    def get_monetary_policy_base_rate(self, country: str, start_date=None, end_date=None):

        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Monetary Policy Base Rate'], start_date=start_date, end_date=end_date, freq='M')
        else:
            df = pd.DataFrame()

        return df

    def get_nominal_exchange_rate(self, country: str, start_date=None, end_date=None):

        exclusion_list = ['Argentina', 'Brazil', 'China', 'India', 'Indonesia', 'Mexico', 'Russia', 'Saudi Arabia',
                          'South Africa', 'Turkey']
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Nominal Effective Exchange Rate'], start_date=start_date, end_date=end_date, freq='M')
        else:
            df = pd.DataFrame()
        return df

    def get_real_exchange_rate(self, country: str, start_date=None, end_date=None):

        exclusion_list = ['Argentina', 'Brazil', 'China', 'India', 'Indonesia', 'Mexico', 'Russia', 'Saudi Arabia',
                          'South Africa', 'Turkey']
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Real Effective Exchange Rate'], start_date=start_date, end_date=end_date, freq='M')
        else:
            df = pd.DataFrame()
        return df

    def get_bis_property_price_nominal(self, country: str, start_date=None, end_date=None):
        exclusion_list = ['Argentina', 'Saudi Arabia']
        if country in exclusion_list:
            return pd.DataFrame()
        df = self.query(country=country, indicator_list=['Property Price Index - Nominal'], start_date=start_date, end_date=end_date, freq='Q')

        return df

    def get_bis_property_price_real(self, country: str, start_date=None, end_date=None):
        exclusion_list = ['Argentina', 'Saudi Arabia']
        if country in exclusion_list:
            return pd.DataFrame()
        df = self.query(country=country, indicator_list=['Property Price Index - Real'], start_date=start_date,
                        end_date=end_date, freq='Q')
        return df

    def get_bis_debt_ratio_nonfinancial(self, country: str, start_date=None, end_date=None):
        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Debt - Non-financial Sector (% GDP)'], start_date=start_date,
                            end_date=end_date, freq='Q')
        return df

    def get_bis_debt_ratio_generalgovmt(self, country: str, start_date=None, end_date=None):
        exclusion_list = ['Argentina', 'Brazil', 'China', 'India', 'Indonesia', 'Mexico',
                          'Russia', 'Saudi Arabia', 'South Africa']
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Debt - General Government (% GDP)'], start_date=start_date,
                            end_date=end_date, freq='Q')
        else:
            return pd.DataFrame()
        return df

    def get_bis_debt_ratio_householdNPISHs(self, country: str, start_date=None, end_date=None):
        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Debt - Household & NPISHs (% GDP)'], start_date=start_date,
                            end_date=end_date, freq='Q')
        return df

    def get_bis_debt_ratio_nonfinancialcorp(self, country: str, start_date=None, end_date=None):
        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Debt - Non-financial Corporations (% GDP)'], start_date=start_date,
                            end_date=end_date, freq='Q')
        return df

    def get_bis_debt_ratio_privnonfinancialsec(self, country: str, start_date=None, end_date=None):
        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Debt - Private Non-financial Sector (% GDP)'], start_date=start_date,
                            end_date=end_date, freq='Q')
        return df

    def get_real_gdp_per_cap_usd(self, country: str, start_date=None, end_date=None):
        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Real GDP per Capita (USD)'],
                            start_date=start_date,
                            end_date=end_date, freq='A')
        return df

    def get_real_gdp_usd_bil(self, country: str, start_date=None, end_date=None):
        exclusion_list = []
        if country not in exclusion_list:
            df = self.query(country=country, indicator_list=['Real GDP (in USD Bil)'],
                            start_date=start_date,
                            end_date=end_date, freq='A')
        return df



if __name__ == "__main__":

    a = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config_country.yaml')),
              Loader=yaml.FullLoader)
    cp_list = a['g20_country_list']

    for cp in cp_list:
        print(cp)
        a = EconomicIndicatorQuery().get_dot_trade_bal_g20cp(cp)
        print(a)
