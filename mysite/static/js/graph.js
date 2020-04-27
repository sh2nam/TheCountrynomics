google.charts.load('current', {'packages':['corechart', 'bar', 'timeline']});


google.charts.setOnLoadCallback(drawRealGDP);
google.charts.setOnLoadCallback(drawRealGDPGrowthBreakdown);
google.charts.setOnLoadCallback(drawPopulationLabourForce);
google.charts.setOnLoadCallback(drawPopulationLabourForceGrowth);
google.charts.setOnLoadCallback(drawTradeBal);
google.charts.setOnLoadCallback(drawTradeBalG20);
google.charts.setOnLoadCallback(drawCurrAccBreakdown);
google.charts.setOnLoadCallback(drawFinAccBreakdown);
google.charts.setOnLoadCallback(drawBopInfo);
google.charts.setOnLoadCallback(drawServNetExpBreakdown);
google.charts.setOnLoadCallback(drawGoodNetExpBreakdown);
google.charts.setOnLoadCallback(drawTradePriceIndex);
google.charts.setOnLoadCallback(drawFDIAssetLiabilities);
google.charts.setOnLoadCallback(drawPortfolioAssetLiabilities);
google.charts.setOnLoadCallback(drawPortfolioInvCP);
google.charts.setOnLoadCallback(drawPortfolioAssetsMinusLiabilities);
google.charts.setOnLoadCallback(drawReserveAssetsBreakdown);
google.charts.setOnLoadCallback(drawUnemploymentRate);
google.charts.setOnLoadCallback(drawCPIGrowth);
google.charts.setOnLoadCallback(drawCPIBasketItemsGrowth);
google.charts.setOnLoadCallback(drawYieldGovmtBondInterbank);
google.charts.setOnLoadCallback(drawEffectiveExchangeRates);
google.charts.setOnLoadCallback(drawPorpertyIndexData);
google.charts.setOnLoadCallback(drawDebtRatioData);

google.charts.setOnLoadCallback(drawCustomData);
google.charts.setOnLoadCallback(drawGdpCompData);



function drawRealGDP(){
  var data = google.visualization.arrayToDataTable(real_gdp_data);

  var options = {
    title: 'Real GDP - Local Currency (in Bil)',
    legend: 'none',
    bar: {groupWidth: "90%"},
    height: 350,
    width: 600,
  };

  if (!real_gdp_data.length){
    return;
  }
  var chart = new google.visualization.ColumnChart(document.getElementById("real_gdp"));
  chart.draw(data, options);
};

function drawRealGDPGrowthBreakdown(){
  var data = google.visualization.arrayToDataTable(gdp_growth_contribution_data);

  var options = {
    title: 'Real GDP Growth Contribution',
    bar: {groupWidth: "90%"},
    vAxis: {format: 'percent'},
    height: 350,
    width: 600,
    isStacked: true,
    series: {0: {type: 'line'}},
    legend: {position: 'right', orientation: 'vertical'},
  };
  if (!gdp_growth_contribution_data.length){
    return;
  }
  var chart = new google.visualization.ColumnChart(document.getElementById("real_gdp_breakdown"));
  chart.draw(data, options);
};

function drawPopulationLabourForce(){
  var data = google.visualization.arrayToDataTable(population_labour_force_data);

  var options = {
    title: 'Population and Labour Force Data',
    bar: {groupWidth: "95%"},
    legend: {position: 'right', orientation: 'vertical'},
    height: 350,
    width: 550,
    seriesType: 'bars',
  };
  if (!population_labour_force_data.length){
    return;
  }
  var chart = new google.visualization.ComboChart(document.getElementById("population_labour_force"));
  chart.draw(data, options);
};

function drawPopulationLabourForceGrowth(){
  var data = google.visualization.arrayToDataTable(population_labour_force_growth_data);

  var options = {
    title: 'Population and Labour Force Annual Growth Rate',
    legend: {position: 'right', orientation: 'vertical'},
    vAxis: {format: 'percent'},
    height: 350,
    width: 600,
    seriesType: 'line',
  };
  if (!population_labour_force_growth_data.length){
    return;
  }
  var chart = new google.visualization.ComboChart(document.getElementById("population_labour_force_growth"));
  chart.draw(data, options);
};

function drawTradeBal(){
  var data = google.visualization.arrayToDataTable(trade_bal_data);

  var options = {
    title: 'Goods&Services Import/Export and Net Export (USD Mil)',
    legend: {position: 'right', orientation: 'vertical'},
    height: 350,
    width: 550,
    seriesType: 'bars',
    series: {0: {type: 'line'}},
  };
  if (!trade_bal_data.length){
    return;
  }
  var chart = new google.visualization.ComboChart(document.getElementById("trade_bal"));
  chart.draw(data, options);
};

function drawTradeBalG20(){
  var data = google.visualization.arrayToDataTable(trade_bal_g20_data);

  var options = {
    title: 'Goods Trade Balance: Top/Bottom 3 G20 Counterparty Countries (USD Mil)',
    legend: {position: 'right', orientation: 'vertical'},
    height: 350,
    width: 600,
  };
  if (!trade_bal_g20_data.length){
    return;
  }
  var chart = new google.visualization.LineChart(document.getElementById("trade_bal_g20"));
  chart.draw(data, options);
};

function drawCurrAccBreakdown(){
  var data = google.visualization.arrayToDataTable(curr_acc_breakdown_data);

  var options = {
    title: 'Balance of Payment: Current Account Breakdown (USD Mil)',
    bar: {groupWidth: "90%"},
    height: 350,
    width: 550,
    isStacked: true,
    series: {0: {type: 'line'}},
    legend: {position: 'right', orientation: 'vertical'},
  };
  if (!curr_acc_breakdown_data.length){
    return;
  }
  var chart = new google.visualization.ColumnChart(document.getElementById("curr_acc_breakdown"));
  chart.draw(data, options);
};

function drawFinAccBreakdown(){
  var data = google.visualization.arrayToDataTable(fin_acc_breakdown_data);

  var options = {
    title: 'Balance of Payment: Financial Account Breakdown (USD Mil)',
    bar: {groupWidth: "90%"},
    height: 350,
    width: 600,
    isStacked: true,
    series: {0: {type: 'line'}},
    legend: {position: 'right', orientation: 'vertical'},
  };
  if (!fin_acc_breakdown_data.length){
    return;
  }
  var chart = new google.visualization.ColumnChart(document.getElementById("fin_acc_breakdown"));
  chart.draw(data, options);
};

function drawBopInfo(){
  var data = google.visualization.arrayToDataTable(bop_info_data);

  var options = {
    title: 'Balance of Payment Information',
    legend: {position: 'right', orientation: 'vertical'},
    height: 350,
    width: 600,
  };
  if (!bop_info_data.length){
    return;
  }
  var chart = new google.visualization.LineChart(document.getElementById("bop_info"));
  chart.draw(data, options);
};

function drawServNetExpBreakdown(){
  var data = google.visualization.arrayToDataTable(serv_net_exp_breakdown_data);

  var options = {
    title: 'Services Net Export: Top/Bottom 3 Services (USD Mil)',
    legend: {position: 'right', orientation: 'vertical'},
    height: 350,
    width: 600,
  };
  if (!serv_net_exp_breakdown_data.length){
    return;
  }
  var chart = new google.visualization.LineChart(document.getElementById("serv_net_exp_breakdown"));
  chart.draw(data, options);
};

function drawGoodNetExpBreakdown(){
  var data = google.visualization.arrayToDataTable(good_net_exp_breakdown_data);

  var options = {
    title: 'Goods Net Export: Top/Bottom 3 Goods (USD Mil)',
    legend: {position: 'right', orientation: 'vertical'},
    height: 350,
    width: 550,
  };
  if (!good_net_exp_breakdown_data.length){
    return;
  }
  var chart = new google.visualization.LineChart(document.getElementById("good_net_exp_breakdown"));
  chart.draw(data, options);
};

function drawTradePriceIndex(){
  var data = google.visualization.arrayToDataTable(trade_price_index_data);

  var options = {
    title: 'Export/Import Price Index',
    legend: {position: 'right', orientation: 'vertical'},
    height: 350,
    width: 550,
  };
  if (!trade_price_index_data.length){
    return;
  }
  var chart = new google.visualization.LineChart(document.getElementById("trade_price_index"));
  chart.draw(data, options);
};

function drawFDIAssetLiabilities(){
  var data = google.visualization.arrayToDataTable(fdi_asset_liability_data);

  var options = {
    title: 'Foreign Direct Investment - Assets vs. Liabilities (USD Mil)',
    legend: {position: 'right', orientation: 'vertical'},
    height: 350,
    width: 550,
    seriesType: 'line',
    series: {2: {type: 'bars'}},
  };
  if (!fdi_asset_liability_data.length){
    return;
  }
  var chart = new google.visualization.ComboChart(document.getElementById("fdi_asset_liability"));
  chart.draw(data, options);
};


function drawPortfolioAssetLiabilities(){
  var data = google.visualization.arrayToDataTable(portfolio_asset_liability_data);

  var options = {
    title: 'Portfolio Investment - Assets vs. Liabilities (USD Mil)',
    legend: {position: 'right', orientation: 'vertical'},
    height: 350,
    width: 600,
    seriesType: 'line',
    series: {2: {type: 'bars'}},
  };
  if (!portfolio_asset_liability_data.length){
    return;
  }
  var chart = new google.visualization.ComboChart(document.getElementById("portfolio_asset_liability"));
  chart.draw(data, options);
};

function drawPortfolioInvCP(){
  var data = google.visualization.arrayToDataTable(portfolio_inv_CP_data);

  var options = {
    title: 'Portfolio Investment (Assets minus Liabilities) - Top/Bottom 3 G20 Counterparty Countries (USD Mil)',
    legend: {position: 'right', orientation: 'vertical'},
    height: 350,
    width: 600,
  };
  if (!portfolio_inv_CP_data.length){
    return;
  }
  var chart = new google.visualization.LineChart(document.getElementById("portfolio_inv_CP"));
  chart.draw(data, options);
};

function drawPortfolioAssetsMinusLiabilities(){
  var data = google.visualization.arrayToDataTable(portfolio_assets_minus_liabilities_data);

  var options = {
    title: 'Portfolio Investment (Assets minus Liabilities) - Equities vs. Debts (USD Mil)',
    bar: {groupWidth: "90%"},
    height: 350,
    width: 550,
    isStacked: true,
    series: {0: {type: 'line'}},
    legend: {position: 'right', orientation: 'vertical'},
  };
  if (!portfolio_assets_minus_liabilities_data.length){
    return;
  }
  var chart = new google.visualization.ColumnChart(document.getElementById("portfolio_assets_minus_liabilities"));
  chart.draw(data, options);
};

function drawReserveAssetsBreakdown(){
  var data = google.visualization.arrayToDataTable(reserve_assets_breakdown_data);

  var options = {
    title: 'Reserve Assets Breakdown (USD Mil)',
    bar: {groupWidth: "90%"},
    height: 350,
    width: 550,
    isStacked: true,
    series: {0: {type: 'line'}},
    legend: {position: 'right', orientation: 'vertical'},
  };
  if (!reserve_assets_breakdown_data.length){
    return;
  }
  var chart = new google.visualization.ColumnChart(document.getElementById("reserve_assets_breakdown"));
  chart.draw(data, options);
};

function drawUnemploymentRate(){
  var data = google.visualization.arrayToDataTable(unemployment_rate_data);

  var options = {
    title: 'Unemployment Rate',
    legend: {position: 'right', orientation: 'vertical'},
    vAxis: {format: 'percent'},
    height: 350,
    width: 550,
    seriesType: 'line',
  };
  if (!unemployment_rate_data.length){
    return;
  }
  var chart = new google.visualization.ComboChart(document.getElementById("unemployment_rate"));
  chart.draw(data, options);
};

function drawCPIGrowth(){
  var data = google.visualization.arrayToDataTable(cpi_growth_data);

  var options = {
    title: 'Inflation (% Changes in CPI)',
    legend: {position: 'right', orientation: 'vertical'},
    vAxis: {format: 'percent'},
    height: 350,
    width: 550,
    seriesType: 'line',
  };
  if (!cpi_growth_data.length){
    return;
  }
  var chart = new google.visualization.ComboChart(document.getElementById("cpi_growth"));
  chart.draw(data, options);
};

function drawCPIBasketItemsGrowth (){
  var data = google.visualization.arrayToDataTable(cpi_basket_items_growth_data);

  var options = {
    title: 'Inflation (% Changes in CPI) - Top/Bottom 3 CPI Basket Items',
    legend: {position: 'right', orientation: 'vertical'},
    vAxis: {format: 'percent'},
    height: 350,
    width: 600,
    seriesType: 'line',
  };
  if (!cpi_basket_items_growth_data.length){
    return;
  }
  var chart = new google.visualization.ComboChart(document.getElementById("cpi_basket_items_growth"));
  chart.draw(data, options);
};

function drawYieldGovmtBondInterbank (){
  var data = google.visualization.arrayToDataTable(oecd_ten_y_three_m_yield_data);

  var options = {
    title: '10Y Govmt Bond Yield and 3M Interbank Rates',
    legend: {position: 'right', orientation: 'vertical'},
    vAxis: {format: 'percent'},
    height: 350,
    width: 600,
    seriesType: 'line',
  };
  if (!oecd_ten_y_three_m_yield_data.length){
    return;
  }
  var chart = new google.visualization.ComboChart(document.getElementById("oecd_ten_y_three_m_yield"));
  chart.draw(data, options);
};

function drawEffectiveExchangeRates (){
  var data = google.visualization.arrayToDataTable(effective_exchange_rates_data);

  var options = {
    title: 'Effective Exchange Rates (End of Month): Real vs. Nominal',
    legend: {position: 'right', orientation: 'vertical'},
    height: 350,
    width: 600,
    seriesType: 'line',
  };
  if (!effective_exchange_rates_data.length){
    return;
  }
  var chart = new google.visualization.ComboChart(document.getElementById("effective_exchange_rates"));
  chart.draw(data, options);
};

function drawPorpertyIndexData (){
  var data = google.visualization.arrayToDataTable(porperty_index_data);

  var options = {
    title: 'Property Index: Real vs. Nominal',
    legend: {position: 'right', orientation: 'vertical'},
    height: 350,
    width: 600,
    seriesType: 'line',
  };
  if (!porperty_index_data.length){
    return;
  }
  var chart = new google.visualization.ComboChart(document.getElementById("porperty_index"));
  chart.draw(data, options);
};

function drawDebtRatioData (){
  var data = google.visualization.arrayToDataTable(debt_ratio_data);

  var options = {
    title: 'Debt to GDP Ratios',
    legend: {position: 'right', orientation: 'vertical'},
    vAxis: {format: 'percent'},
    height: 350,
    width: 600,
    seriesType: 'line',
  };
  if (!debt_ratio_data.length){
    return;
  }
  var chart = new google.visualization.ComboChart(document.getElementById("debt_ratio"));
  chart.draw(data, options);
};

function drawCustomData (){
  var data = google.visualization.arrayToDataTable(custom_data);

  var options = {
    legend: {position: 'right', orientation: 'vertical'},
    height: 600,
    width: 1000,
    seriesType: 'line',
  };
  if (!custom_data.length){
    return;
  }
  var chart = new google.visualization.ComboChart(document.getElementById("custom_data"));
  chart.draw(data, options);
};

function drawGdpCompData (){
  var data = google.visualization.arrayToDataTable(gdp_comp_data);

  var options = {
    legend: {position: 'right', orientation: 'vertical'},
    height: 600,
    width: 1000,
    hAxis: {title: 'Real GDP per Capita (USD)'},
  };
  if (!gdp_comp_data.length){
    return;
  }
  var chart = new google.visualization.ScatterChart(document.getElementById("gdp_comp_data"));
  chart.draw(data, options);
};
