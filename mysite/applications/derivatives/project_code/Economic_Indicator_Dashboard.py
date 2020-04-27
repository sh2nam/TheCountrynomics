import pandas as pd
# from Scripts.Economic_Indicator_Query import EconomicIndicatorQuery
from applications.derivatives.project_code.Economic_Indicator_Query import EconomicIndicatorQuery
from applications.derivatives.project_code.Economic_Data import EconomicData
from applications.derivatives.project_code.Multipoo_No_Daemon import MyPool


class EconomicIndicatorDashboard:

    def __init__(self, country: str, start_date=None, end_date=None, freq='A', format=False, api=False):
        self.country = country

        if start_date:
            self.start_date = start_date
        else:
            self.start_date = '1990-01-01'
        if end_date:
            self.end_date = end_date
        else:
            self.end_date = None

        if api:
            self.query = EconomicData().download_api_economic_data
        else:
            self.query = EconomicData().download_db_economic_data

        self.freq = freq
        self.eq = EconomicIndicatorQuery(api=api)
        self.format = format

        # Externalized variables
        self.ext_bop_portfolio_investment_assets_breakdown = None
        self.ext_bop_portfolio_investment_liabilities_breakdown = None

    def __format_data(self, df: pd.DataFrame, freq=None):
        """
        reformat dataframe to jason adaptable format
        """
        if df.empty:
            return []

        df.reset_index(inplace=True)
        df = df.copy()

        if not freq or freq == 'A':
            df['Date'] = df['Date'].apply(lambda x: x.strftime('%Y'))
        else:
            df['Date'] = df['Date'].apply(lambda x: x.strftime('%Y-%m'))
        result = [df.columns.values.tolist()] + df.values.tolist()
        return result

    def real_gdp_lcu(self):
        df = self.eq.get_real_gdp_number_lcu(self.country, self.start_date, self.end_date)
        if self.format:
            return self.__format_data(df)
        return df

    def real_gdp_growth_contribution(self):
        indicator_list = ['Real GDP Growth', 'Government Expenditure (% GDP)', 'Savings (% GDP)', 'Investment (% GDP)',
                          'Net Export (% GDP)']
        df = self.query(country=self.country, indicator_list=indicator_list, start_date=self.start_date, end_date=self.end_date)
        df.dropna(inplace=True)

        if not df.empty and len(df.columns)== 5:
            df['Government Expenditure (% GDP)'] = df['Government Expenditure (% GDP)'] - df['Savings (% GDP)']
            comp_df = df[['Government Expenditure (% GDP)', 'Investment (% GDP)', 'Net Export (% GDP)']]
            comp_df = comp_df.copy()
            comp_df['Personal Consumption (% GDP)'] = 1 - comp_df.sum(axis=1)
            df = pd.concat([df['Real GDP Growth'], comp_df], axis=1)
            df.dropna(inplace=True)

            for component in ['Personal Consumption (% GDP)', 'Government Expenditure (% GDP)', 'Investment (% GDP)',
                              'Net Export (% GDP)']:
                df[component] = ((1 + df['Real GDP Growth']) * df[component]) - df[component].shift(1)
            df.dropna(inplace=True)
            df = df[['Real GDP Growth', 'Personal Consumption (% GDP)', 'Government Expenditure (% GDP)',
                     'Investment (% GDP)', 'Net Export (% GDP)']]
        if self.format:
            return self.__format_data(df, self.freq)

        return df

    def dot_trade_bal(self):
        indicator_list = ['Import (USD Mil)', 'Export (USD Mil)']
        df = self.query(country=self.country, indicator_list=indicator_list, start_date=self.start_date,
                        end_date=self.end_date, freq=self.freq)

        if not df.empty:
            df['Net Export (USD Mil)'] = df['Export (USD Mil)'] - df['Import (USD Mil)']
            df = df[['Net Export (USD Mil)', 'Import (USD Mil)', 'Export (USD Mil)']]
        if self.format:
            return self.__format_data(df)

        return df

    def dot_trade_bal_g20countries(self):
        df = self.eq.get_dot_trade_bal_g20cp(self.country, self.start_date, self.end_date, self.freq)
        if not df.empty:
            date_pivot = max(df.index.values)
            # get top/bottom 3 countries
            top_3_countries = list(df.T[date_pivot].nlargest(3).index.values)
            bottom_3_coutries = list(df.T[date_pivot].nsmallest(3).index.values)
            df = df[top_3_countries + bottom_3_coutries]

        if self.format:
            return self.__format_data(df, self.freq)

        return df

    def bop_info(self):
        indicator_list = ['Current Account (USD Mil)', 'Financial Account (USD Mil)', 'Capital Account (USD Mil)']
        df = self.query(country=self.country, indicator_list=indicator_list, start_date=self.start_date,
                        end_date=self.end_date, freq=self.freq)
        if not df.empty:
            df = df[indicator_list]
        if self.format:
            return self.__format_data(df, self.freq)
        return df

    def bop_curr_acc_breakdown(self):
        indicator_list = ['Current Account (USD Mil)', 'Secondary Income (USD Mil)', 'Primary Income (USD Mil)',
        'Services Net Export (USD Mil)',  'Goods Net Export (USD Mil)']
        df = self.query(country=self.country, indicator_list=indicator_list, start_date=self.start_date,
                        end_date=self.end_date, freq=self.freq)
        if not df.empty:
            df = df[indicator_list]
        if self.format:
            return self.__format_data(df, self.freq)
        return df

    def bop_fin_acc_breakdown(self):
        indicator_list = ['Financial Account (USD Mil)', 'Portfolio Investment (USD Mil)', 'Other Investment (USD Mil)',
                          'Reserve Assets (USD Mil)', 'Direct Investment (USD Mil)']
        df = self.query(country=self.country, indicator_list=indicator_list, start_date=self.start_date,
                        end_date=self.end_date, freq=self.freq)
        if not df.empty:
            df['Financial Derivatives & Other (USD Mil)'] = df['Financial Account (USD Mil)'] - \
                                                            df[['Portfolio Investment (USD Mil)',
                                                                'Other Investment (USD Mil)',
                                                                'Reserve Assets (USD Mil)',
                                                                'Direct Investment (USD Mil)']].sum(axis=1)
        df = df[['Financial Account (USD Mil)', 'Reserve Assets (USD Mil)', 'Financial Derivatives & Other (USD Mil)',
        'Other Investment (USD Mil)', 'Direct Investment (USD Mil)', 'Portfolio Investment (USD Mil)']]
        if self.format:
            return self.__format_data(df, self.freq)

        return df

    def bop_services_breakdown(self):
        df = self.eq.get_bop_services_net_export_breakdown(self.country, self.start_date, self.end_date, self.freq)
        df.dropna(how='all', axis=1, inplace=True)
        if not df.empty:
            date_pivot = max(df.index.values)
            top_3_services = list(df.T[date_pivot].nlargest(3).index.values)
            bottom_3_services = list(df.T[date_pivot].nsmallest(3).index.values)
            df = df[top_3_services + bottom_3_services]
        if self.format:
            return self.__format_data(df, self.freq)

        return df

    def wto_goods_breakdown(self):
        df = self.eq.get_wto_goods_net_export_breakdown(self.country, self.start_date, self.end_date)
        if not df.empty:
            date_pivot = max(df.index.values)
            top_3_countries = list(df.T[date_pivot].nlargest(3).index.values)
            bottom_3_coutries = list(df.T[date_pivot].nsmallest(3).index.values)
            df = df[top_3_countries + bottom_3_coutries]
        if self.format:
            return self.__format_data(df)
        return df

    def ifs_trade_price_index(self):
        indicator_list = ['Import Price Index', 'Export Price Index']
        df = self.query(country=self.country, indicator_list=indicator_list, start_date=self.start_date,
                        end_date=self.end_date, freq=self.freq)
        if not df.empty:
            df = df[indicator_list]
        if self.format:
            return self.__format_data(df, self.freq)
        return df

    def bop_fdi_assets_liabilities(self):
        indicator_list = ['FDI - Assets (USD Mil)', 'FDI - Liabilities (USD Mil)']
        df = self.query(country=self.country, indicator_list=indicator_list, start_date=self.start_date,
                        end_date=self.end_date, freq=self.freq)

        if not df.empty:
            try:
                df['FDI - Assets Minus Liabilities (USD Mil)'] = df['FDI - Assets (USD Mil)'] - df[
                    'FDI - Liabilities (USD Mil)']
            except:
                pass
        if self.format:
            return self.__format_data(df, self.freq)
        return df

    def bop_portfolio_assets_liabilities(self):
        indicator_list = ['Portfolio Investment - Assets (USD Mil)', 'Portfolio Investment - Liabilities (USD Mil)']
        df = self.query(country=self.country, indicator_list=indicator_list, start_date=self.start_date,
                        end_date=self.end_date, freq=self.freq)

        if not df.empty:
            try:
                df['Portfolio Investment - Assets Minus Liabilities (USD Mil)'] = df[
                                                                                      'Portfolio Investment - Assets (USD Mil)'] - \
                                                                                  df[
                                                                                      'Portfolio Investment - Liabilities (USD Mil)']
            except:
                pass

        if self.format:
            return self.__format_data(df, self.freq)
        return df

    def bop_portfolio_investment_assets_breakdown(self):
        if self.ext_bop_portfolio_investment_assets_breakdown is not None:
            return self.ext_bop_portfolio_investment_assets_breakdown

        indicator_list = ['Portfolio Investment - Assets (USD Mil)',
        'Assets, Portfolio Investment - Debt Securities (USD Mil)',
        'Assets, Portfolio Investment - Equity (USD Mil)']
        df = self.query(country=self.country, indicator_list=indicator_list, start_date=self.start_date,
                        end_date=self.end_date, freq=self.freq)
        if not df.empty and len(indicator_list) == len(df.columns):
            df = df[indicator_list]
        self.ext_bop_portfolio_investment_assets_breakdown = df
        if self.format:
            return self.__format_data(df.copy(), self.freq)
        return self.ext_bop_portfolio_investment_assets_breakdown

    def bop_portfolio_investment_liabilities_breakdown(self):
        if self.ext_bop_portfolio_investment_liabilities_breakdown is not None:
            return self.ext_bop_portfolio_investment_liabilities_breakdown

        indicator_list = ['Portfolio Investment - Liabilities (USD Mil)',
                          'Liabilities, Portfolio Investment - Debt Securities (USD Mil)',
                          'Liabilities, Portfolio Investment - Equity (USD Mil)']
        df = self.query(country=self.country, indicator_list=indicator_list, start_date=self.start_date,
                        end_date=self.end_date, freq=self.freq)
        if not df.empty:
            df = df[indicator_list]
        self.ext_bop_portfolio_investment_liabilities_breakdown = df

        if self.format:
            return self.__format_data(df.copy(), self.freq)

        return self.ext_bop_portfolio_investment_liabilities_breakdown

    def portfolio_inv_assets_cp(self):
        eq_df = self.eq.get_cpis_portfolio_investment_assets_equity_counter_parties(self.country, self.start_date,
                                                                                    self.end_date)
        db_df = self.eq.get_cpis_portfolio_investment_assets_debt_counter_parties(self.country, self.start_date,
                                                                                  self.end_date)

        if not eq_df.empty:
            eq_date_pivot = max(eq_df.index.values)
            eq_top_3_countries = list(eq_df.T[eq_date_pivot].nlargest(3).index.values)
            eq_df = eq_df[eq_top_3_countries]
            eq_df.columns = 'Equities - ' + eq_df.columns

        if not db_df.empty:
            debt_date_pivot = max(db_df.index.values)
            debt_top_3_countries = list(db_df.T[debt_date_pivot].nlargest(3).index.values)
            db_df = db_df[debt_top_3_countries]
            db_df.columns = 'Debt - ' + db_df.columns
        df = pd.concat([eq_df, db_df], axis=1)
        if self.format:
            return self.__format_data(df)
        return df

    def portfolio_inv_liabilities_cp(self):
        eq_df = self.eq.get_cpis_portfolio_investment_liabilities_equity_counter_parties(self.country, self.start_date,
                                                                                         self.end_date)
        db_df = self.eq.get_cpis_portfolio_investment_liabilities_debt_counter_parties(self.country, self.start_date,
                                                                                       self.end_date)

        if not eq_df.empty:
            eq_date_pivot = max(eq_df.index.values)
            eq_top_3_countries = list(eq_df.T[eq_date_pivot].nlargest(3).index.values)
            eq_df = eq_df[eq_top_3_countries]
            eq_df.columns = 'Equities - ' + eq_df.columns

        if not db_df:
            debt_date_pivot = max(db_df.index.values)
            debt_top_3_countries = list(db_df.T[debt_date_pivot].nlargest(3).index.values)
            db_df = db_df[debt_top_3_countries]
            db_df.columns = 'Debt - ' + db_df.columns

        df = pd.concat([eq_df, db_df], axis=1)
        if self.format:
            return self.__format_data(df)

        return df

    def bop_reserve_assets_breakdown(self):
        indicator_list = ['Assets, Reserve Assets (USD Mil)', 'Reserve Assets - Monetary Gold (USD Mil)',
        'Reserve Assets - Currency, Securities, and Deposits (USD Mil)',
        'Reserve Assets - IMF Reserve (USD Mil)',
        'Reserve Assets - SDR (USD Mil)']
        df = self.query(country=self.country, indicator_list=indicator_list, start_date=self.start_date,
                        end_date=self.end_date, freq=self.freq)
        if not df.empty:
            df = df[indicator_list]
        if self.format:
            return self.__format_data(df, self.freq)
        return df

    def wdi_population_labour(self):
        indicator_list = ['Population', 'Labour Force']
        df = self.query(country=self.country, indicator_list=indicator_list, start_date=self.start_date,
                        end_date=self.end_date, freq=self.freq)
        if not df.empty:
            df = df[indicator_list]
        if self.format:
            return self.__format_data(df)
        return df

    def wdi_population_labour_growth(self):
        indicator_list = ['Population', 'Labour Force']
        df = self.query(country=self.country, indicator_list=indicator_list, start_date=self.start_date,
                        end_date=self.end_date, freq=self.freq)
        if not df.empty:
            df = df[indicator_list]
        if not df.empty:
            df = self.calculate_pct_change(df)
        if self.format:
            return self.__format_data(df)
        return df

    def ifs_unemployment_rate(self):
        df = self.eq.get_unemployment_rate(self.country, self.start_date, self.end_date, self.freq)
        if self.format:
            return self.__format_data(df, self.freq)
        return df

    def calculate_pct_change(self, df):
        result = []
        if df.empty:
            return df
        for col in df.columns:
            growth_df = pd.DataFrame()
            growth_df[col + ' (% Change)'] = (df[col] - df[col].shift(1)) / df[col]
            growth_df.dropna(inplace=True)
            result.append(growth_df)
        df = pd.concat(result, axis=1)
        return df

    def cpi_all_item_growth(self):
        # todo: think about better way to handle data that does not have enough data
        if self.country == 'Argentina':
            df = self.eq.get_cpi_all_items(self.country, self.start_date, self.end_date, 'Q')
        else:
            df = self.eq.get_cpi_all_items(self.country, self.start_date, self.end_date, self.freq)

        df = self.calculate_pct_change(df)

        if self.format:
            if self.country == 'Argentina':
                return self.__format_data(df, 'Q')
            return self.__format_data(df, self.freq)

        return df

    def cpi_basket_items_growth(self):
        df = self.eq.get_cpi_basket_items(self.country, self.start_date, self.end_date)

        if not df.empty:
            df = self.calculate_pct_change(df)

            date_pivot = max(df.index.values)
            top_3 = list(df.T[date_pivot].nlargest(3).index.values)
            bottom_3 = list(df.T[date_pivot].nsmallest(3).index.values)
            df = df[top_3 + bottom_3]
        if self.format:
            return self.__format_data(df)
        return df

    def bop_portfolio_investment_assetsMinusLiabilities(self):
        self.format = False
        assets_df = self.bop_portfolio_investment_assets_breakdown()
        liab_df = self.bop_portfolio_investment_liabilities_breakdown()
        self.format = True

        # Update Names
        assets_df.rename(columns={'Assets, Portfolio Investment - Debt Securities (USD Mil)':
                                      'Assets minus Liabilities, Portfolio Investment - Debt Securities (USD Mil)',
                                  'Assets, Portfolio Investment - Equity (USD Mil)':
                                      'Assets minus Liabilities, Portfolio Investment - Equity (USD Mil)',
                                  'Portfolio Investment - Assets (USD Mil)':
                                      'Portfolio Investment - Assets minus Liabilities (USD Mil)'}, inplace=True)

        liab_df.rename(columns={'Liabilities, Portfolio Investment - Debt Securities (USD Mil)':
                                    'Assets minus Liabilities, Portfolio Investment - Debt Securities (USD Mil)',
                                'Liabilities, Portfolio Investment - Equity (USD Mil)':
                                    'Assets minus Liabilities, Portfolio Investment - Equity (USD Mil)',
                                'Portfolio Investment - Liabilities (USD Mil)':
                                    'Portfolio Investment - Assets minus Liabilities (USD Mil)'}, inplace=True)
        df = assets_df - liab_df
        if self.format:
            return self.__format_data(df, self.freq)
        return df

    def portfolio_inv_cp(self):
        assets_df = self.eq.get_cpis_portfolio_investment_assets_counter_parties(self.country, self.start_date,
                                                                                 self.end_date)
        liabilities_df = self.eq.get_cpis_portfolio_investment_liabilities_counter_parties(self.country,
                                                                                           self.start_date,
                                                                                           self.end_date)
        inters_cols = list(set(assets_df.columns).intersection(set(liabilities_df.columns)))
        df = assets_df[inters_cols] - liabilities_df[inters_cols]

        if not df.empty:
            date_pivot = max(df.index.values)
            top_3_countries = list(df.T[date_pivot].nlargest(3).index.values)
            bottom_3_countries = list(df.T[date_pivot].nsmallest(3).index.values)
            df = df[top_3_countries + bottom_3_countries]

        df.dropna(how='all', inplace=True)
        if self.format:
            return self.__format_data(df)
        return df

    def oecd_10y_3m_yield(self):
        ten_y_df = self.eq.get_oecd_10y_govmt_bond_yield(self.country, self.start_date, self.end_date)
        three_m_df = self.eq.get_oecd_3M_interbank_rates(self.country, self.start_date, self.end_date)
        l = []
        for item in [ten_y_df, three_m_df]:
            if not item.empty:
                l.append(item)
        if not l:
            df = pd.DataFrame()
        else:
            df = pd.concat(l, axis=1)
        if self.format:
            return self.__format_data(df, 'Q')
        return df

    def effective_exchange_rates(self):
        real_df = self.eq.get_real_exchange_rate(self.country, self.start_date, self.end_date)
        nominal_df = self.eq.get_nominal_exchange_rate(self.country, self.start_date, self.end_date)

        l = []
        for item in [real_df, nominal_df]:
            if not item.empty:
                l.append(item)

        if not l:
            df = pd.DataFrame()
        else:
            df = pd.concat(l, axis=1)
        if self.format:
            return self.__format_data(df, 'Q')
        return df

    def property_price_index(self):
        df_a = self.eq.get_bis_property_price_nominal(self.country, self.start_date, self.end_date)
        df_b = self.eq.get_bis_property_price_real(self.country, self.start_date, self.end_date)
        df = pd.concat([df_a, df_b], axis=1)
        print(df)
        if not df.empty:
            df = df.resample(self.freq, convention='end').last()
        if self.format:
            return self.__format_data(df, 'Q')
        return df

    def debt_ratio(self):
        indicator_list = ['Debt - Non-financial Sector (% GDP)', 'Debt - General Government (% GDP)',
                          'Debt - Household & NPISHs (% GDP)', 'Debt - Non-financial Corporations (% GDP)',
                          'Debt - Private Non-financial Sector (% GDP)']
        df = self.query(country=self.country, indicator_list=indicator_list, start_date=self.start_date,
                        end_date=self.end_date, freq='Q')
        if self.format:
            return self.__format_data(df, 'Q')
        return df

    def multi_pool_report(self, x):
        if x == '1':
            return {'1': self.real_gdp_lcu()}
        elif x == '2':
            return {'2': self.real_gdp_growth_contribution()}
        elif x == '3':
            return {'3': self.cpi_all_item_growth()}
        elif x == '4':
            return {'4': self.cpi_basket_items_growth()}
        elif x == '5':
            return {'5': self.wdi_population_labour()}
        elif x == '6':
            return {'6': self.wdi_population_labour_growth()}
        elif x == '7':
            return {'7': self.ifs_unemployment_rate()}
        elif x == '8':
            return {'8': self.bop_info()}
        elif x == '9':
            return {'9': self.bop_curr_acc_breakdown()}
        elif x == '10':
            return {'10': self.bop_fin_acc_breakdown()}
        elif x == '11':
            return {'11': self.dot_trade_bal()}
        elif x == '12':
            return {'12': self.dot_trade_bal_g20countries()}
        elif x == '13':
            return {'13': self.bop_services_breakdown()}
        elif x == '14':
            return {'14': self.wto_goods_breakdown()}
        elif x == '15':
            return {'15': self.ifs_trade_price_index()}
        elif x == '16':
            return {'16': self.bop_fdi_assets_liabilities()}
        elif x == '17':
            return {'17': self.bop_portfolio_assets_liabilities()}
        elif x == '18':
            return {'18': self.bop_portfolio_investment_assetsMinusLiabilities()}
        elif x == '19':
            return {'19': self.portfolio_inv_cp()}
        elif x == '20':
            return {'20': self.bop_reserve_assets_breakdown()}
        elif x == '21':
            return {'21': self.oecd_10y_3m_yield()}
        elif x == '22':
            return {'22': self.effective_exchange_rates()}
        elif x == '23':
            return {'23': self.property_price_index()}
        elif x == '24':
            return {'24': self.debt_ratio()}

    def multiple_pool_report(self, l=[]):
        if not l:
            l = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
                 '18', '19', '20', '21', '22', '23', '24']
        pool = MyPool(4)
        result = pool.map(self.multi_pool_report, l)
        final_result = {}
        for d in result:
            final_result.update(d)
        return final_result



if __name__ == "__main__":
    a = EconomicIndicatorDashboard("Argentina", '2000-01-01', None, 'A')
    d = a.wdi_population_labour_growth()
    print(d)
