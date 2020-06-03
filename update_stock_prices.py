import pandas_datareader.data as web
import pandas as pd
import datetime

stock_list = pd.read_csv(r'C:\Users\massv\OneDrive\Documents\GitHub\bokeh_equity_charts\tse_stock_list.csv')

for i in range(len(stock_list)):
    df = pd.read_csv(r'C:\Users\massv\OneDrive\Documents\Trading\data\Daily\\' + stock_list.loc[i]['Stock_Name'] + '.csv', parse_dates=True, index_col='Date')
    start = max(df.index) + datetime.timedelta(days=1)
    end = datetime.date.today()
    df_weekly = pd.DataFrame(columns=['Open','High','Low','Close','Adj Close','Volume'])
    if end >= start.date():
        new = web.DataReader(stock_list.loc[i]['Stock_Name'], 'yahoo', start, end)
        df = pd.concat([df,new], axis=0)
        df = df.loc[~df.index.duplicated(keep='first')]
        df_weekly['Open'] = df.resample('W')['Open'].first()
        df_weekly['High'] = df.resample('W')['High'].max()
        df_weekly['Low'] = df.resample('W')['Low'].min()
        df_weekly['Close'] = df.resample('W')['Close'].last()
        df_weekly['Adj Close'] = df.resample('W')['Adj Close'].last()
        df_weekly['Volume'] = df.resample('W')['Volume'].sum()
        df.to_csv(r'C:\Users\massv\OneDrive\Documents\Trading\data\Daily\\' + stock_list.loc[i]['Stock_Name'] + '.csv')
        df_weekly.to_csv(r'C:\Users\massv\OneDrive\Documents\Trading\data\Weekly\\' + stock_list.loc[i]['Stock_Name'] + '.csv')
        
#Remove duplicate entries or entries with duplicate row index
stock_list = pd.read_csv(r'C:\Users\massv\OneDrive\Documents\GitHub\bokeh_equity_charts\tse_stock_list.csv')

for i in range(len(stock_list)):
    df = pd.read_csv(r'C:\Users\massv\OneDrive\Documents\Trading\data\Daily\\' + stock_list.loc[i]['Stock_Name'] + '.csv', parse_dates=True, index_col='Date')
    df = df.loc[~df.index.duplicated(keep='first')]
    df.to_csv(r'C:\Users\massv\OneDrive\Documents\Trading\data\Daily\\' + stock_list.loc[i]['Stock_Name'] + '.csv')