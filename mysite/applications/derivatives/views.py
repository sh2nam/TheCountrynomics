from django.shortcuts import render
import json
from applications.derivatives.project_code.Downlaod_Dbnomics_API_Data import DownloadDbnomicsAPIData
from applications.derivatives.project_code.Economic_Indicator_Dashboard import EconomicIndicatorDashboard
from applications.derivatives.project_code.Single_Timeseries import SingleTimeSeries
import pandas as pd


# Create your views here.
def derivatives(request):
    country_list = list(DownloadDbnomicsAPIData().country_code.keys())

    if request.method == 'POST':
        country = request.POST['country_list']
        freq = request.POST['freq']
        start_year = request.POST['start_year']
        end_year = request.POST['end_year']

        context = create_context(country_list, country, freq, start_year, end_year)

        return render(request=request,
                      template_name = 'derivatives_base.html',
                      context = context)
    else:
        return render(request=request, template_name = 'derivatives_base.html', context={"country_list": country_list,})

def custom_data(request):
    return render(request=request, template_name = 'custom_data.html')

def gdp_per_cap_report(request):
    indicator_display_list = SingleTimeSeries().get_display_names()
    TS = SingleTimeSeries()
    indicator = 'Debt - Household & NPISHs (% GDP)'
    date = None
    x_axis = 'Real GDP per Capita (USD)'
    title = ""

    if request.method == 'POST':
        indicator = request.POST['indicator_display_list']
        date = request.POST['date']
        date_a, date_b = get_proper_dates(date, date)
        date = date_b

    l = []
    if x_axis != "None" and indicator != "None":
        df_a = TS.get_timeseries_multiple_countries(x_axis, date=date)
        df_b = TS.get_timeseries_multiple_countries(indicator, date=date)
        l = [df_a, df_b]

        title = indicator + ' Comparison by ' + x_axis

    if l:
        df = pd.concat(l, axis=1, sort=False)
        df = df.dropna()
        df.index.name = "Country"
        df.reset_index(inplace=True)
        df = df.pivot(index=x_axis, columns='Country', values=indicator)
        df = df.copy()
        df.reset_index(inplace=True)
        cols = list(df.columns)
        df = df[cols]
        result = [df.columns.values.tolist()] + df.values.tolist()

    else:
        result = []

    return render(request=request, template_name = 'gdp_per_cap_report.html',
    context={"indicator_display_list": indicator_display_list, 'gdp_comp_data': json.dumps(result),
    'title': title})


def compare_contrast(request):
    country_list = SingleTimeSeries().get_g20_countries()
    indicator_display_list = SingleTimeSeries().get_display_names()
    TS = SingleTimeSeries()

    country_1 = "United States"
    country_2 = "Canada"
    indicator_1 = 'Debt - Household & NPISHs (% GDP)'
    indicator_2 = 'Debt - Household & NPISHs (% GDP)'
    start_date = None
    end_date = None
    freq = None

    if request.method == 'POST':
        country_1 = request.POST['country_list_1']
        indicator_1 = request.POST['indicator_display_list_1']
        country_2 = request.POST['country_list_2']
        indicator_2 = request.POST['indicator_display_list_2']
        freq = request.POST['freq']
        start_date, end_date = get_proper_dates(request.POST['start_year'],  request.POST['end_year'])

    l = []

    if country_1 != "None" and indicator_1 != "None":
        l.append(TS.get_timeseries(country_1, indicator_1, start_date, end_date, freq))
    if country_2 != "None" and indicator_2 != "None":
        l.append(TS.get_timeseries(country_2, indicator_2, start_date, end_date, freq))

    if l:
        df = pd.concat(l, axis=1)
        title = ' VS. '.join(df.columns.values.tolist())
        df.reset_index(inplace=True)
        df = df.copy()
        df['Date'] = df['Date'].apply(lambda x: x.strftime('%Y-%m'))
        result = [df.columns.values.tolist()] + df.values.tolist()
    else:
        title = ""
        result = []

    return render(request=request, template_name = 'compare_contrast.html',
    context={"country_list": country_list,
    "indicator_display_list": indicator_display_list,
    'custom_data': json.dumps(result),
    "title": title,})

def get_proper_dates(start_year, end_year):
    try:
        start_year = int(start_year)
        if start_year >=1900 and start_year <= 2100:
            start_year = start_year
        else:
            start_year = 1990
    except:
        start_year = 1990
    start_date = str(start_year) + '-01-01'

    try:
        end_year = int(end_year)
        if end_year >=1900 and end_year <= 2100:
            end_year = end_year
        else:
            end_year = 2100
        end_date = str(end_year) + '-12-31'
        if end_year < start_year:
            end_date = None
    except:
        end_date = None

    return start_date, end_date




def create_context(country_list, country, freq, start_year, end_year):

    start_date, end_date = get_proper_dates(start_year, end_year)
    ER = EconomicIndicatorDashboard(country, start_date, end_date, freq, True, False)
    # rep_dic = ER.multiple_pool_report()

    use_pool = False

    if use_pool:
        gdpData = rep_dic["1"]
    else:
        gdpData = ER.real_gdp_lcu()

    if use_pool:
        gdpGrowthContribution = rep_dic["2"]
    else:
        gdpGrowthContribution = ER.real_gdp_growth_contribution()

    if use_pool:
        cpi_growth = rep_dic["3"]
    else:
        cpi_growth = ER.cpi_all_item_growth()

    if use_pool:
        cpi_basket_items_growth = rep_dic["4"]
    else:
        cpi_basket_items_growth = ER.cpi_basket_items_growth()

    if use_pool:
        populationLabourForce = rep_dic["5"]
    else:
        populationLabourForce = ER.wdi_population_labour()

    if use_pool:
        populationLabourForceGrowth = rep_dic["6"]
    else:
        populationLabourForceGrowth = ER.wdi_population_labour_growth()

    if use_pool:
        unemploymentRate = rep_dic["7"]
    else:
        unemploymentRate = ER.ifs_unemployment_rate()

    if use_pool:
        bopInfo = rep_dic["8"]
    else:
        bopInfo = ER.bop_info()

    if use_pool:
        currAccBreakdown = rep_dic["9"]
    else:
        currAccBreakdown = ER.bop_curr_acc_breakdown()

    if use_pool:
        finAccBreakdown = rep_dic["10"]
    else:
        finAccBreakdown = ER.bop_fin_acc_breakdown()

    if use_pool:
        tradeBal = rep_dic["11"]
    else:
        tradeBal = ER.dot_trade_bal()

    if use_pool:
        tradeBalG20Countries = rep_dic["12"]
    else:
        tradeBalG20Countries = ER.dot_trade_bal_g20countries()

    if use_pool:
        servNetExpBreakdown = rep_dic["13"]
    else:
        servNetExpBreakdown = ER.bop_services_breakdown()

    if use_pool:
        goodNetExpBreakdown = rep_dic["14"]
    else:
        goodNetExpBreakdown = ER.wto_goods_breakdown()

    if use_pool:
        tradePriceIndex = rep_dic["15"]
    else:
        tradePriceIndex = ER.ifs_trade_price_index()

    if use_pool:
        fdiAssetsLiabilities = rep_dic["16"]
    else:
        fdiAssetsLiabilities = ER.bop_fdi_assets_liabilities()

    if use_pool:
        portfolioAssetsLiabilities = rep_dic["17"]
    else:
        portfolioAssetsLiabilities = ER.bop_portfolio_assets_liabilities()

    if use_pool:
        portfolioAssetsMinusLiabilities = rep_dic["18"]
    else:
        portfolioAssetsMinusLiabilities = ER.bop_portfolio_investment_assetsMinusLiabilities()

    if use_pool:
        portfolioInvCP = rep_dic["19"]
    else:
        portfolioInvCP = ER.portfolio_inv_cp()

    if use_pool:
        reserveAssetsBreakdown = rep_dic["20"]
    else:
        reserveAssetsBreakdown = ER.bop_reserve_assets_breakdown()

    if use_pool:
        oecdTenYThreeMYield = rep_dic["21"]
    else:
        oecdTenYThreeMYield = ER.oecd_10y_3m_yield()

    if use_pool:
        effectiveExchangeRates = rep_dic["22"]
    else:
        effectiveExchangeRates = ER.effective_exchange_rates()

    if use_pool:
        porpertyIndex = rep_dic["23"]
    else:
        porpertyIndex = ER.property_price_index()

    if use_pool:
        debtRatio = rep_dic["24"]
    else:
        debtRatio = ER.debt_ratio()

    context = {"country_list": country_list,
    "real_gdp": {"data": json.dumps(gdpData)},
    "real_gdp_growth_contribution":{"data": json.dumps(gdpGrowthContribution)},
    "cpi_growth": {"data": json.dumps(cpi_growth)},
    "cpi_basket_items_growth":{"data": json.dumps(cpi_basket_items_growth)},
    "population_labour_force": {"data": json.dumps(populationLabourForce)},
    "population_labour_force_growth": {"data": json.dumps(populationLabourForceGrowth)},
    "unemployment_rate": {"data": json.dumps(unemploymentRate)},
    "bop_info": {"data": json.dumps(bopInfo)},
    "curr_acc_breakdown": {"data": json.dumps(currAccBreakdown)},
    "fin_acc_breakdown": {"data": json.dumps(finAccBreakdown)},
    "trade_bal": {"data": json.dumps(tradeBal)},
    "trade_bal_g20countries": {"data": json.dumps(tradeBalG20Countries)},
    "serv_net_exp_breakdown": {"data": json.dumps(servNetExpBreakdown)},
    "good_net_exp_breakdown": {"data": json.dumps(goodNetExpBreakdown)},
    "trade_price_index": {"data": json.dumps(tradePriceIndex)},
    "fdi_assets_liabilities": {"data": json.dumps(fdiAssetsLiabilities)},
    "portfolio_assets_liabilities": {"data": json.dumps(portfolioAssetsLiabilities)},
    "portfolio_inv_CP": {"data": json.dumps(portfolioInvCP)},
    "portfolio_assets_minus_liabilities": {"data": json.dumps(portfolioAssetsMinusLiabilities)},
    "reserve_assets_breakdown": {"data": json.dumps(reserveAssetsBreakdown)},
    "oecd_ten_y_three_m_yield": {"data": json.dumps(oecdTenYThreeMYield)},
    "effective_exchange_rates": {"data": json.dumps(effectiveExchangeRates)},
    "porperty_index": {"data": json.dumps(porpertyIndex)},
    "debt_ratio": {"data": json.dumps(debtRatio)},
    }

    return context
