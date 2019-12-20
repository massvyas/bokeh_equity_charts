import pandas_datareader.data as web
import pandas as pd
import datetime

stock_list = pd.read_csv(r'C:\Users\massv\OneDrive\Documents\GitHub\bokeh_equity_charts\bokeh_equity_charts\stock_list.csv')
gsptse = pd.read_csv(r'C:\Users\massv\OneDrive\Documents\Trading\data\^gsptse.csv', parse_dates=True, index_col = 'Date')

start = max(gsptse.index) + datetime.timedelta(days=1)
#start = datetime.datetime(1990, 1, 1)
#end = datetime.datetime(2019,12, 18)
end = datetime.date.today()

for i in range(len(stock_list)):
    df = pd.read_csv(r'C:\Users\massv\OneDrive\Documents\Trading\data\\' + stock_list.loc[i]['Stock_Name'] + '.csv', parse_dates=True, index_col='Date')
    new = web.DataReader(stock_list.loc[i]['Stock_Name'], 'yahoo', start, end)
    df = pd.concat([df,new], axis=0)
    df.to_csv(r'C:\Users\massv\OneDrive\Documents\Trading\data\\' + stock_list.loc[i]['Stock_Name'] + '.csv')