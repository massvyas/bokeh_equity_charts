import pandas_datareader.data as web
import pandas as pd
import datetime

stock_list = pd.read_csv(r'C:\Users\massv\OneDrive\Documents\Trading\data\nse_stock_list.csv')

start = datetime.datetime(1995, 1,1)
#end = datetime.datetime(2019,12, 18)
end = datetime.date.today()

for i in range(len(stock_list)):
    df = web.DataReader(stock_list.loc[i]['Stock_Name'], 'yahoo', start, end)
    df.to_csv(r'C:\Users\massv\OneDrive\Documents\Trading\data\Daily\\' + stock_list.loc[i]['Stock_Name'] + '.csv')
    
#Download data for individual stocks
df = web.DataReader('ASHOKLEY.NS', 'yahoo', start, end)
df.to_csv(r'C:\Users\massv\OneDrive\Documents\Trading\data\ASHOLKEY_2019.csv')