import pandas_datareader.data as web
import pandas as pd
import datetime

stock_list = pd.read_csv(r'C:\Users\massv\OneDrive\Documents\GitHub\bokeh_equity_charts\bokeh_equity_charts\stock_list.csv')

start = datetime.datetime(2019, 2,27)
#end = datetime.datetime(2019,12, 18)
end = datetime.date.today()

for i in range(len(stock_list)):
    df = web.DataReader(stock_list.loc[i]['Stock_Name'], 'yahoo', start, end)
    df.to_csv(r'C:\Users\massv\OneDrive\Documents\Trading\data\\' + stock_list.loc[i]['Stock_Name'] + '.csv')
    
#Download data for individual stocks
df = web.DataReader('ASHOKLEY.NS', 'yahoo', start, end)
df.to_csv(r'C:\Users\massv\OneDrive\Documents\Trading\data\ASHOLKEY_2019.csv')