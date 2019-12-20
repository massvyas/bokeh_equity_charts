import pandas_datareader.data as web
import pandas as pd
import datetime

stock_list = pd.read_csv(r'C:\Users\massv\OneDrive\Documents\GitHub\bokeh_equity_charts\bokeh_equity_charts\stock_list.csv')

for i in range(len(stock_list)):
    df = pd.read_csv(r'C:\Users\massv\OneDrive\Documents\Trading\data\\' + stock_list.loc[i]['Stock_Name'] + '.csv', parse_dates=True, index_col='Date')
    start = max(df.index) + datetime.timedelta(days=1)
    end = datetime.date.today()
    if end >= start.date():
        new = web.DataReader(stock_list.loc[i]['Stock_Name'], 'yahoo', start, end)
        df = pd.concat([df,new], axis=0)
        df.to_csv(r'C:\Users\massv\OneDrive\Documents\Trading\data\\' + stock_list.loc[i]['Stock_Name'] + '.csv')