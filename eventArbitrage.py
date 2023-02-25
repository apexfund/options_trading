from alpha_vantage.fundamentaldata import FundamentalData
import requests
import json
import time
import pandas as pd
import yfinance as yf
import pytz

# Define the ticker symbol for the company you want to retrieve data for
tickerSymbol = 'AAPL'

# Get the historical data for the last year
historicalData = yf.download(tickerSymbol, period='1y', interval='1d')

# Get the fundamental data for the company as of the last date
tickerData = yf.Ticker(tickerSymbol, validate=False)
fundamentalData = tickerData.history(start='2021/01/01', end='2022/01/01')

# Convert the fundamental data to a pandas DataFrame
fundamentalData = pd.DataFrame(fundamentalData)

# Print the fundamental data
print(fundamentalData.head())

# def calc_row(overview_val, income_val, balance_val, cashflow_val):
#     #Add Overview Values and reset index(its off for some reason)
#     row_data = overview_val[['Symbol','Sector','PercentInsiders','PercentInstitutions','MarketCapitalization',
#                              'RevenueTTM','ReturnOnAssetsTTM','EBITDA','ProfitMargin','OperatingMarginTTM',
#                              'GrossProfitTTM','ForwardAnnualDividendYield']]
#     row_data = row_data.reset_index(drop=True)
    
#     #Add Income (calculate 3yr revenue growth rate or approximation/None)
#     rev_growth_3y = 0
#     try:
#         if(len(income['totalRevenue']) >= 4):
#             rev_growth_3y = (int(income['totalRevenue'][0]) - int(income['totalRevenue'][3])) / int(income['totalRevenue'][3])
#         else:
#             rev_growth_3y = overview['QuarterlyRevenueGrowthYOY'] * 3
#     except:
#         rev_growth_3y = None
   
#     row_data['RevenueGrowth3Yr'] = rev_growth_3y
        
#     #Add Balance values, have to get matrix in correct format
#     balance_cols = ['totalAssets','totalLiabilities','cashAndShortTermInvestments']
#     row_data[balance_cols] = balance_val[balance_cols].iloc[0:1].reset_index(drop=True)
    
     
#     #Add Cashflow
#     row_data[['operatingCashflow','capitalExpenditures']] = cashflow_val[['operatingCashflow','capitalExpenditures']].iloc[0:1].reset_index(drop=True)
    
#     return row_data

# api_key = 'DZ5VY06254N0TGHE'
# ticker = 'TSLA'
# url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol='+ticker+'&apikey='+api_key
# req = requests.get(url)
# data = req.json()

# # fd = FundamentalData(key = api_key, output_format='pandas')
# # api_data, api_meta = fd.get_company_overview(symbol = ticker)
# # api_data.head(1)

# # overview, o_meta = fd.get_company_overview(symbol = ticker)
# # income, i_meta = fd.get_income_statement_annual(symbol = ticker)
# # balance, b_meta = fd.get_balance_sheet_annual(symbol = ticker)
# # cashflow, c_meta = fd.get_cash_flow_annual(symbol = ticker)

# # #Create dataframe, calculate/create each row using helper function and concating to dataframe 
# # test_table = pd.DataFrame()
# # company_row = calc_row(overview, income, balance, cashflow)
# # test_table = pd.concat([test_table, company_row], ignore_index=True)
# # test_table


# symbol = data.get("Symbol")
# sector = data.get("Sector")
# percent_insiders = data.get("PercentInsiders")
# percent_institutions = data.get("PercentInstitutions")
# market_cap = data.get("MarketCapitalization")
# revenue_ttm = data.get("RevenueTTM")
# return_on_assets_ttm = data.get("ReturnOnAssetsTTM")
# ebitda = data.get("EBITDA")
# profit_margin = data.get("ProfitMargin")
# operating_margin_ttm = data.get("OperatingMarginTTM")
# gross_profit_ttm = data.get("GrossProfitTTM")
# forward_annual_dividend_yield = data.get("ForwardAnnualDividendYield")
# revenue_growth_3yr = data.get("RevenueGrowth3Yr")
# total_assets = data.get("totalAssets")
# total_liabilities = data.get("totalLiabilities")
# cash_and_short_term_investments = data.get("cashAndShortTermInvestments")
# operating_cashflow = data.get("operatingCashflow")
# capital_expenditures = data.get("capitalExpenditures")

# print("Symbol: ", symbol)
# print("Sector: ", sector)
# print("PercentInsiders: ", percent_insiders)
# print("PercentInstitutions: ", percent_institutions)
# print("MarketCapitalization: ", market_cap)
# print("RevenueTTM: ", revenue_ttm)
# print("ReturnOnAssetsTTM: ", return_on_assets_ttm)
# print("EBITDA: ", ebitda)
# print("ProfitMargin: ", profit_margin)
# print("OperatingMarginTTM: ", operating_margin_ttm)
# print("GrossProfitTTM: ", gross_profit_ttm)
# print("ForwardAnnualDividendYield: ", forward_annual_dividend_yield)
# print("RevenueGrowth3Yr: ", revenue_growth_3yr)
# print("totalAssets: ", total_assets)
# print("totalLiabilities: ", total_liabilities)
# print("cashAndShortTermInvestments: ", cash_and_short_term_investments)
# print("operatingCashflow: ", operating_cashflow)
# print("capitalExpenditures: ", capital_expenditures) 