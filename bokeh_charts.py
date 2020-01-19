# Perform necessary imports
import sys
import glob
import os
import datetime as dt
from bokeh.io import curdoc, output_file, show, output_notebook
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, DateRangeSlider, Select
from bokeh.layouts import widgetbox, row, column
import pandas as pd
sys.path.insert(0, 'C:/Users/massv/OneDrive/Documents/GitHub/technical-indicators')
import symphonie_indicators as sym

csv_files = glob.glob(r'C:\Users\massv\OneDrive\Documents\Trading\data\Daily\*.csv')
csv_file_names = [os.path.basename(file)[:-4] for file in csv_files]

bars_shown = 200

data = pd.read_csv(r'C:\Users\massv\OneDrive\Documents\Trading\data\Daily\^GSPTSE.csv',parse_dates = True)
data = data.fillna(method='ffill')
data['Bar'] = [i for i in range(len(data))]
data['Colors'] = ['Green' if data.iloc[i].Close > data.iloc[i].Open else 'Red' for i in range(len(data))]

#Fetching symphonie indicator values, removing unwanted columns and renaming indicator columns
trendline = sym.trendline(data,cciPeriod=63,atrPeriod=18,st=0).drop(['Open','High','Low','Close','trendUp','trendDown','trend'],axis='columns')

emotion = sym.emotion(data,SSP=7,Kmax=50.6).drop(['Open','High','Low','Close'],axis='columns')
emotion.columns = ['emotionUpInd','emotionDownInd']

extreme = sym.extreme(data, r=12,s=12,u=5).drop(['Open','High','Low','Close','TVI'],axis='columns')
extreme['extremeUpInd'] = (extreme['TVITrend']==1)*1
extreme['extremeDownInd'] = (extreme['TVITrend']==-1)*1
extreme.drop(['TVITrend'],axis='columns', inplace=True)

sentiment = sym.sentiment(data, period=12).drop(['Open','High','Low','Close','g_ibuf_80'],axis='columns')
sentiment['sentimentUpInd'] = (sentiment['SentimentTrend']==1)*1
sentiment['sentimentDownInd'] = (sentiment['SentimentTrend']==-1)*1
sentiment.drop(['SentimentTrend'],axis='columns', inplace=True)

#Merging all symphonie indicators into one df
symphonie = pd.concat([trendline,emotion,extreme,sentiment],axis=1)

#Assigning colors for up and down indicators
symphonie['trendUpIndColor'] = ['Blue' if symphonie.iloc[i].trendUpInd == 1 else 'White' for i in range(len(symphonie))]
symphonie['trendDownIndColor'] = ['Red' if symphonie.iloc[i].trendDownInd == 1 else 'White' for i in range(len(symphonie))]
symphonie['emotionUpIndColor'] = ['Blue' if symphonie.iloc[i].emotionUpInd == 1 else 'White' for i in range(len(symphonie))]
symphonie['emotionDownIndColor'] = ['Red' if symphonie.iloc[i].emotionDownInd == 1 else 'White' for i in range(len(symphonie))]
symphonie['extremeUpIndColor'] = ['Blue' if symphonie.iloc[i].extremeUpInd == 1 else 'White' for i in range(len(symphonie))]
symphonie['extremeDownIndColor'] = ['Red' if symphonie.iloc[i].extremeDownInd == 1 else 'White' for i in range(len(symphonie))]
symphonie['sentimentUpIndColor'] = ['Blue' if symphonie.iloc[i].sentimentUpInd == 1 else 'White' for i in range(len(symphonie))]
symphonie['sentimentDownIndColor'] = ['Red' if symphonie.iloc[i].sentimentDownInd == 1 else 'White' for i in range(len(symphonie))]

#Merging data and symphonie
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)
data = pd.concat([data,symphonie], axis=1)

#Setting dates for default display
end = max(data.index).date()
start = end - dt.timedelta(days=bars_shown)

#Creating dataset for monthly OHLC
data['week_start'] = [data.index[i] - dt.timedelta(days=data.index[i].weekday()) for i in range(len(data))]
data['week_current'] = data.index
data['week_open'] = 0
data['week_high'] = 0
data['week_low'] = 0
data['week_volume'] = 0
data['week_close'] = data['Close']
data['week_adjclose'] = data['Adj Close']
weekOpenCol = data.columns.get_loc('week_open')
weekHighCol = data.columns.get_loc('week_high')
weekLowCol = data.columns.get_loc('week_low')
weekCloseCol = data.columns.get_loc('week_close')
weekVolumeCol = data.columns.get_loc('week_volume')
weekAdjCloseCol = data.columns.get_loc('week_adjclose')
weekStartCol = data.columns.get_loc('week_start')
weekCurrentCol = data.columns.get_loc('week_current')

#Calculating weekly OHLC
for i in range(len(data)):
    a = data.loc[data.iloc[i,weekStartCol]:data.iloc[i,weekCurrentCol]]
    data.iloc[i,weekOpenCol] = a['Open'][0]
    data.iloc[i,weekHighCol] = a['High'].max()
    data.iloc[i,weekLowCol] = a['Low'].min()
    data.iloc[i,weekVolumeCol] = a['Volume'].sum()

#Extracting monthly OHLC to a different dataset
data_weekly = data[['week_open','week_high','week_low','week_close','week_adjclose','week_volume']]
data_weekly.columns = ['Open','High','Low','Close','Adj Close','Volume']
data_weekly.reset_index(inplace=True)

#Fetching symphonie indicator values, removing unwanted columns and renaming indicator columns
trendline_weekly = sym.trendline(data_weekly,cciPeriod=315,atrPeriod=90,st=0).drop(['Open','High','Low','Close','trendUp','trendDown','trend'],axis='columns')

emotion_weekly = sym.emotion(data_weekly,SSP=35,Kmax=50.6).drop(['Open','High','Low','Close'],axis='columns')
emotion_weekly.columns = ['emotionUpInd','emotionDownInd']

extreme_weekly = sym.extreme(data_weekly, r=60,s=60,u=25).drop(['Open','High','Low','Close','TVI'],axis='columns')
extreme_weekly['extremeUpInd'] = (extreme_weekly['TVITrend']==1)*1
extreme_weekly['extremeDownInd'] = (extreme_weekly['TVITrend']==-1)*1
extreme_weekly.drop(['TVITrend'],axis='columns', inplace=True)

sentiment_weekly = sym.sentiment(data_weekly, period=60).drop(['Open','High','Low','Close','g_ibuf_80'],axis='columns')
sentiment_weekly['sentimentUpInd'] = (sentiment_weekly['SentimentTrend']==1)*1
sentiment_weekly['sentimentDownInd'] = (sentiment_weekly['SentimentTrend']==-1)*1
sentiment_weekly.drop(['SentimentTrend'],axis='columns', inplace=True)

#Merging all symphonie indicators into one df
symphonie_weekly = pd.concat([trendline_weekly,emotion_weekly,extreme_weekly,sentiment_weekly],axis=1)

#Assigning colors for up and down indicators
symphonie_weekly['trendUpIndColor'] = ['Blue' if symphonie_weekly.iloc[i].trendUpInd == 1 else 'White' for i in range(len(symphonie_weekly))]
symphonie_weekly['trendDownIndColor'] = ['Red' if symphonie_weekly.iloc[i].trendDownInd == 1 else 'White' for i in range(len(symphonie_weekly))]
symphonie_weekly['emotionUpIndColor'] = ['Blue' if symphonie_weekly.iloc[i].emotionUpInd == 1 else 'White' for i in range(len(symphonie_weekly))]
symphonie_weekly['emotionDownIndColor'] = ['Red' if symphonie_weekly.iloc[i].emotionDownInd == 1 else 'White' for i in range(len(symphonie_weekly))]
symphonie_weekly['extremeUpIndColor'] = ['Blue' if symphonie_weekly.iloc[i].extremeUpInd == 1 else 'White' for i in range(len(symphonie_weekly))]
symphonie_weekly['extremeDownIndColor'] = ['Red' if symphonie_weekly.iloc[i].extremeDownInd == 1 else 'White' for i in range(len(symphonie_weekly))]
symphonie_weekly['sentimentUpIndColor'] = ['Blue' if symphonie_weekly.iloc[i].sentimentUpInd == 1 else 'White' for i in range(len(symphonie_weekly))]
symphonie_weekly['sentimentDownIndColor'] = ['Red' if symphonie_weekly.iloc[i].sentimentDownInd == 1 else 'White' for i in range(len(symphonie_weekly))]

#Renaming data and symphonie column names
symphonie_weekly.columns = ['trendUpInd_weekly','trendDownInd_weekly','emotionUpInd_weekly','emotionDownInd_weekly',
                            'extremeUpInd_weekly','extremeDownInd_weekly','sentimentUpInd_weekly','sentimentDownInd_weekly',
                            'trendUpIndColor_weekly','trendDownIndColor_weekly','emotionUpIndColor_weekly','emotionDownIndColor_weekly',
                            'extremeUpIndColor_weekly','extremeDownIndColor_weekly', 'sentimentUpIndColor_weekly', 'sentimentDownIndColor_weekly']

#Merging data_weekly and symphonie_weekly
data_weekly.set_index('Date', inplace=True)
data_weekly = pd.concat([data_weekly,symphonie_weekly], axis=1).drop(['Open','High','Low','Close','Adj Close','Volume'],axis='columns')

#Merging daily and weekly data and symphonie indicators
data = pd.concat([data, data_weekly],axis=1)

# Make the ColumnDataSource: source
source = ColumnDataSource(data={
    'Date'    : data.loc[start:end].index,
    'Open'    : data.loc[start:end].Open.values,
    'High'    : data.loc[start:end].High.values,
    'Low'     : data.loc[start:end].Low.values,
    'Close'   : data.loc[start:end].Close.values,
    'Adj Close': data.loc[start:end,['Adj Close']].values,
    'Bar'     : data.loc[start:end].Bar.values,
    'Colors'  : data.loc[start:end].Colors,
    'trendUpIndColor'  : data.loc[start:end].trendUpIndColor,
    'trendDownIndColor': data.loc[start:end].trendDownIndColor,
    'emotionUpIndColor'  : data.loc[start:end].emotionUpIndColor,
    'emotionDownIndColor': data.loc[start:end].emotionDownIndColor,
    'extremeUpIndColor'  : data.loc[start:end].extremeUpIndColor,
    'extremeDownIndColor': data.loc[start:end].extremeDownIndColor,
    'sentimentUpIndColor'  : data.loc[start:end].sentimentUpIndColor,
    'sentimentDownIndColor': data.loc[start:end].sentimentDownIndColor,
    'trendUpIndColor_weekly'  : data.loc[start:end].trendUpIndColor_weekly,
    'trendDownIndColor_weekly': data.loc[start:end].trendDownIndColor_weekly,
    'emotionUpIndColor_weekly'  : data.loc[start:end].emotionUpIndColor_weekly,
    'emotionDownIndColor_weekly': data.loc[start:end].emotionDownIndColor_weekly,
    'extremeUpIndColor_weekly'  : data.loc[start:end].extremeUpIndColor_weekly,
    'extremeDownIndColor_weekly': data.loc[start:end].extremeDownIndColor_weekly,
    'sentimentUpIndColor_weekly'  : data.loc[start:end].sentimentUpIndColor_weekly,
    'sentimentDownIndColor_weekly': data.loc[start:end].sentimentDownIndColor_weekly
})


# Define the callback function: update_plot
def update_plot(attr, old, new):
    # Set the yr name to slider.value and new_data to source.data
    start, end = slider.value
    start = dt.datetime.fromtimestamp(slider.value[0]/1e3)
    end = dt.datetime.fromtimestamp(slider.value[1]/1e3)
    new_data = ColumnDataSource(data={
        'Date'    : data.loc[start:end].index,
        'Open'    : data.loc[start:end].Open.values,
        'High'    : data.loc[start:end].High.values,
        'Low'     : data.loc[start:end].Low.values,
        'Close'   : data.loc[start:end].Close.values,
        'Adj Close': data.loc[start:end,['Adj Close']].values,
        'Bar'     : data.loc[start:end].Bar.values,
        'Colors'  : data.loc[start:end].Colors,
        'trendUpIndColor'  : data.loc[start:end].trendUpIndColor,
        'trendDownIndColor': data.loc[start:end].trendDownIndColor,
        'emotionUpIndColor'  : data.loc[start:end].emotionUpIndColor,
        'emotionDownIndColor': data.loc[start:end].emotionDownIndColor,
        'extremeUpIndColor'  : data.loc[start:end].extremeUpIndColor,
        'extremeDownIndColor': data.loc[start:end].extremeDownIndColor,
        'sentimentUpIndColor'  : data.loc[start:end].sentimentUpIndColor,
        'sentimentDownIndColor': data.loc[start:end].sentimentDownIndColor,
        'trendUpIndColor_weekly'  : data.loc[start:end].trendUpIndColor_weekly,
        'trendDownIndColor_weekly': data.loc[start:end].trendDownIndColor_weekly,
        'emotionUpIndColor_weekly'  : data.loc[start:end].emotionUpIndColor_weekly,
        'emotionDownIndColor_weekly': data.loc[start:end].emotionDownIndColor_weekly,
        'extremeUpIndColor_weekly'  : data.loc[start:end].extremeUpIndColor_weekly,
        'extremeDownIndColor_weekly': data.loc[start:end].extremeDownIndColor_weekly,
        'sentimentUpIndColor_weekly'  : data.loc[start:end].sentimentUpIndColor_weekly,
        'sentimentDownIndColor_weekly': data.loc[start:end].sentimentDownIndColor_weekly
    }) 
    source.data.update(new_data.data)
    
def update_selector(attr, old, new):
    #Use global data variable
    global data
       
    # Set the yr name to slider.value and new_data to source.data
    new_value = select.value
    idx = csv_file_names.index(new_value)
    
    data = pd.read_csv(csv_files[idx],parse_dates = True)
    data = data.fillna(method='ffill')
    data['Bar'] = [i for i in range(len(data))]
    data['Colors'] = ['Green' if data.iloc[i].Close > data.iloc[i].Open else 'Red' for i in range(len(data))]

    #Fetching symphonie indicator values, removing unwanted columns and renaming indicator columns
    trendline = sym.trendline(data,cciPeriod=63,atrPeriod=18,st=0).drop(['Open','High','Low','Close','trendUp','trendDown','trend'],axis='columns')
    
    emotion = sym.emotion(data,SSP=7,Kmax=50.6).drop(['Open','High','Low','Close'],axis='columns')
    emotion.columns = ['emotionUpInd','emotionDownInd']
    
    extreme = sym.extreme(data, r=12,s=12,u=5).drop(['Open','High','Low','Close','TVI'],axis='columns')
    extreme['extremeUpInd'] = (extreme['TVITrend']==1)*1
    extreme['extremeDownInd'] = (extreme['TVITrend']==-1)*1
    extreme.drop(['TVITrend'],axis='columns', inplace=True)
    
    sentiment = sym.sentiment(data, period=12).drop(['Open','High','Low','Close','g_ibuf_80'],axis='columns')
    sentiment['sentimentUpInd'] = (sentiment['SentimentTrend']==1)*1
    sentiment['sentimentDownInd'] = (sentiment['SentimentTrend']==-1)*1
    sentiment.drop(['SentimentTrend'],axis='columns', inplace=True)
    
    #Merging all symphonie indicators into one df
    symphonie = pd.concat([trendline,emotion,extreme,sentiment],axis=1)
    
    #Assigning colors for up and down indicators
    symphonie['trendUpIndColor'] = ['Blue' if symphonie.iloc[i].trendUpInd == 1 else 'White' for i in range(len(symphonie))]
    symphonie['trendDownIndColor'] = ['Red' if symphonie.iloc[i].trendDownInd == 1 else 'White' for i in range(len(symphonie))]
    symphonie['emotionUpIndColor'] = ['Blue' if symphonie.iloc[i].emotionUpInd == 1 else 'White' for i in range(len(symphonie))]
    symphonie['emotionDownIndColor'] = ['Red' if symphonie.iloc[i].emotionDownInd == 1 else 'White' for i in range(len(symphonie))]
    symphonie['extremeUpIndColor'] = ['Blue' if symphonie.iloc[i].extremeUpInd == 1 else 'White' for i in range(len(symphonie))]
    symphonie['extremeDownIndColor'] = ['Red' if symphonie.iloc[i].extremeDownInd == 1 else 'White' for i in range(len(symphonie))]
    symphonie['sentimentUpIndColor'] = ['Blue' if symphonie.iloc[i].sentimentUpInd == 1 else 'White' for i in range(len(symphonie))]
    symphonie['sentimentDownIndColor'] = ['Red' if symphonie.iloc[i].sentimentDownInd == 1 else 'White' for i in range(len(symphonie))]
    
    #Merging data and symphonie
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    data = pd.concat([data,symphonie], axis=1)

    end = max(data.index)
    start = end - dt.timedelta(days=bars_shown)
 
    #Creating dataset for monthly OHLC
    data['week_start'] = [data.index[i] - dt.timedelta(days=data.index[i].weekday()) for i in range(len(data))]
    data['week_current'] = data.index
    data['week_open'] = 0
    data['week_high'] = 0
    data['week_low'] = 0
    data['week_volume'] = 0
    data['week_close'] = data['Close']
    data['week_adjclose'] = data['Adj Close']
    weekOpenCol = data.columns.get_loc('week_open')
    weekHighCol = data.columns.get_loc('week_high')
    weekLowCol = data.columns.get_loc('week_low')
    weekCloseCol = data.columns.get_loc('week_close')
    weekVolumeCol = data.columns.get_loc('week_volume')
    weekAdjCloseCol = data.columns.get_loc('week_adjclose')
    weekStartCol = data.columns.get_loc('week_start')
    weekCurrentCol = data.columns.get_loc('week_current')

    #Calculating weekly OHLC
    for i in range(len(data)):
        a = data.loc[data.iloc[i,weekStartCol]:data.iloc[i,weekCurrentCol]]
        data.iloc[i,weekOpenCol] = a['Open'][0]
        data.iloc[i,weekHighCol] = a['High'].max()
        data.iloc[i,weekLowCol] = a['Low'].min()
        data.iloc[i,weekVolumeCol] = a['Volume'].sum()

    #Extracting monthly OHLC to a different dataset
    data_weekly = data[['week_open','week_high','week_low','week_close','week_adjclose','week_volume']]
    data_weekly.columns = ['Open','High','Low','Close','Adj Close','Volume']
    data_weekly.reset_index(inplace=True)
    
    #Fetching symphonie indicator values, removing unwanted columns and renaming indicator columns
    trendline_weekly = sym.trendline(data_weekly,cciPeriod=315,atrPeriod=90,st=0).drop(['Open','High','Low','Close','trendUp','trendDown','trend'],axis='columns')
    
    emotion_weekly = sym.emotion(data_weekly,SSP=35,Kmax=50.6).drop(['Open','High','Low','Close'],axis='columns')
    emotion_weekly.columns = ['emotionUpInd','emotionDownInd']
    
    extreme_weekly = sym.extreme(data_weekly, r=60,s=60,u=25).drop(['Open','High','Low','Close','TVI'],axis='columns')
    extreme_weekly['extremeUpInd'] = (extreme_weekly['TVITrend']==1)*1
    extreme_weekly['extremeDownInd'] = (extreme_weekly['TVITrend']==-1)*1
    extreme_weekly.drop(['TVITrend'],axis='columns', inplace=True)
    
    sentiment_weekly = sym.sentiment(data_weekly, period=60).drop(['Open','High','Low','Close','g_ibuf_80'],axis='columns')
    sentiment_weekly['sentimentUpInd'] = (sentiment_weekly['SentimentTrend']==1)*1
    sentiment_weekly['sentimentDownInd'] = (sentiment_weekly['SentimentTrend']==-1)*1
    sentiment_weekly.drop(['SentimentTrend'],axis='columns', inplace=True)
    
    #Merging all symphonie indicators into one df
    symphonie_weekly = pd.concat([trendline_weekly,emotion_weekly,extreme_weekly,sentiment_weekly],axis=1)
    
    #Assigning colors for up and down indicators
    symphonie_weekly['trendUpIndColor'] = ['Blue' if symphonie_weekly.iloc[i].trendUpInd == 1 else 'White' for i in range(len(symphonie_weekly))]
    symphonie_weekly['trendDownIndColor'] = ['Red' if symphonie_weekly.iloc[i].trendDownInd == 1 else 'White' for i in range(len(symphonie_weekly))]
    symphonie_weekly['emotionUpIndColor'] = ['Blue' if symphonie_weekly.iloc[i].emotionUpInd == 1 else 'White' for i in range(len(symphonie_weekly))]
    symphonie_weekly['emotionDownIndColor'] = ['Red' if symphonie_weekly.iloc[i].emotionDownInd == 1 else 'White' for i in range(len(symphonie_weekly))]
    symphonie_weekly['extremeUpIndColor'] = ['Blue' if symphonie_weekly.iloc[i].extremeUpInd == 1 else 'White' for i in range(len(symphonie_weekly))]
    symphonie_weekly['extremeDownIndColor'] = ['Red' if symphonie_weekly.iloc[i].extremeDownInd == 1 else 'White' for i in range(len(symphonie_weekly))]
    symphonie_weekly['sentimentUpIndColor'] = ['Blue' if symphonie_weekly.iloc[i].sentimentUpInd == 1 else 'White' for i in range(len(symphonie_weekly))]
    symphonie_weekly['sentimentDownIndColor'] = ['Red' if symphonie_weekly.iloc[i].sentimentDownInd == 1 else 'White' for i in range(len(symphonie_weekly))]
    
    #Renaming data and symphonie column names
    symphonie_weekly.columns = ['trendUpInd_weekly','trendDownInd_weekly','emotionUpInd_weekly','emotionDownInd_weekly',
                                'extremeUpInd_weekly','extremeDownInd_weekly','sentimentUpInd_weekly','sentimentDownInd_weekly',
                                'trendUpIndColor_weekly','trendDownIndColor_weekly','emotionUpIndColor_weekly','emotionDownIndColor_weekly',
                                'extremeUpIndColor_weekly','extremeDownIndColor_weekly', 'sentimentUpIndColor_weekly', 'sentimentDownIndColor_weekly']
    
    #Merging data_weekly and symphonie_weekly
    data_weekly.set_index('Date', inplace=True)
    data_weekly = pd.concat([data_weekly,symphonie_weekly], axis=1).drop(['Open','High','Low','Close','Adj Close','Volume'],axis='columns')
    
    #Merging daily and weekly data and symphonie indicators
    data = pd.concat([data, data_weekly],axis=1)
       
    # Make the ColumnDataSource: source
    new_data = ColumnDataSource(data={
        'Date'    : data.loc[start:end].index,
        'Open'    : data.loc[start:end].Open.values,
        'High'    : data.loc[start:end].High.values,
        'Low'     : data.loc[start:end].Low.values,
        'Close'   : data.loc[start:end].Close.values,
        'Adj Close': data.loc[start:end,['Adj Close']].values,
        'Bar'     : data.loc[start:end].Bar.values,
        'Colors'  : data.loc[start:end].Colors,
        'trendUpIndColor'  : data.loc[start:end].trendUpIndColor,
        'trendDownIndColor': data.loc[start:end].trendDownIndColor,
        'emotionUpIndColor'  : data.loc[start:end].emotionUpIndColor,
        'emotionDownIndColor': data.loc[start:end].emotionDownIndColor,
        'extremeUpIndColor'  : data.loc[start:end].extremeUpIndColor,
        'extremeDownIndColor': data.loc[start:end].extremeDownIndColor,
        'sentimentUpIndColor'  : data.loc[start:end].sentimentUpIndColor,
        'sentimentDownIndColor': data.loc[start:end].sentimentDownIndColor,
        'trendUpIndColor_weekly'  : data.loc[start:end].trendUpIndColor_weekly,
        'trendDownIndColor_weekly': data.loc[start:end].trendDownIndColor_weekly,
        'emotionUpIndColor_weekly'  : data.loc[start:end].emotionUpIndColor_weekly,
        'emotionDownIndColor_weekly': data.loc[start:end].emotionDownIndColor_weekly,
        'extremeUpIndColor_weekly'  : data.loc[start:end].extremeUpIndColor_weekly,
        'extremeDownIndColor_weekly': data.loc[start:end].extremeDownIndColor_weekly,
        'sentimentUpIndColor_weekly'  : data.loc[start:end].sentimentUpIndColor_weekly,
        'sentimentDownIndColor_weekly': data.loc[start:end].sentimentDownIndColor_weekly
    })
    
    source.data.update(new_data.data)

# Make a slider object: slider
slider = DateRangeSlider(title="Date Range: ", start=min(data.index), end=max(data.index), 
                         value=(start,end), step=1, width=1000)

# Create the figure for the candle stick
p = figure(title='Line chart', x_axis_label='Dates', y_axis_label='Closing Price', 
           x_axis_type='datetime', plot_height=300, plot_width=1300)
p.segment('Bar', 'High', 'Bar', 'Low', source=source, line_width=1, color='black')  # plot the wicks
p.vbar('Bar', 0.7, 'Close', 'Open', source=source, line_color='black', fill_color = 'Colors')

# Creating the figure for symphonie indicators
p1 = figure(title='Symphonie indicators', x_axis_type='datetime', plot_height=150, plot_width=1300)
p1.vbar('Bar', 0.7, 1, 2, source=source, line_color='White', fill_color = 'trendDownIndColor')
p1.vbar('Bar', 0.7, 2, 3, source=source, line_color='White', fill_color = 'trendUpIndColor')

p1.vbar('Bar', 0.7, 5, 6, source=source, line_color='White', fill_color = 'emotionDownIndColor')
p1.vbar('Bar', 0.7, 6, 7, source=source, line_color='White', fill_color = 'emotionUpIndColor')

p1.vbar('Bar', 0.7, 9, 10, source=source, line_color='White', fill_color = 'extremeDownIndColor')
p1.vbar('Bar', 0.7, 10,11, source=source, line_color='White', fill_color = 'extremeUpIndColor')

p1.vbar('Bar', 0.7, 13, 14, source=source, line_color='White', fill_color = 'sentimentDownIndColor')
p1.vbar('Bar', 0.7, 14, 15, source=source, line_color='White', fill_color = 'sentimentUpIndColor')

p2 = figure(title='Symphonie indicators', x_axis_type='datetime', plot_height=150, plot_width=1300)
p2.vbar('Bar', 0.7, 1, 2, source=source, line_color='White', fill_color = 'trendDownIndColor_weekly')
p2.vbar('Bar', 0.7, 2, 3, source=source, line_color='White', fill_color = 'trendUpIndColor_weekly')

p2.vbar('Bar', 0.7, 5, 6, source=source, line_color='White', fill_color = 'emotionDownIndColor_weekly')
p2.vbar('Bar', 0.7, 6, 7, source=source, line_color='White', fill_color = 'emotionUpIndColor_weekly')

p2.vbar('Bar', 0.7, 9, 10, source=source, line_color='White', fill_color = 'extremeDownIndColor_weekly')
p2.vbar('Bar', 0.7, 10,11, source=source, line_color='White', fill_color = 'extremeUpIndColor_weekly')

p2.vbar('Bar', 0.7, 13, 14, source=source, line_color='White', fill_color = 'sentimentDownIndColor_weekly')
p2.vbar('Bar', 0.7, 14, 15, source=source, line_color='White', fill_color = 'sentimentUpIndColor_weekly')

hover = HoverTool(tooltips=[
        ('bar', '@Bar'),
        ('date', '@Date{%F %T}'),
        ('open', '@Open{0.0000f}'),
        ('high', '@High{0.0000f}'),
        ('low', '@Low{0.0000f}'),
        ('close', '@Close{0.0000f}')
    ],
        formatters={'Date': 'datetime'})
p.add_tools(hover)

# Attach the callback to the 'value' property of slider
slider.on_change('value',update_plot)

# Create a dropdown Select widget for the x data: x_select
select = Select(
    options=csv_file_names,
    value='^GSPTSE',
    title='Stock Selector'
)

select.on_change('value', update_selector)

# Add the plot to the current document and add a title
layout = column(row(select, widgetbox(slider)), p, p1, p2)
curdoc().add_root(layout)
curdoc().title = 'Stock Chart'

# Output the file and show the figure
#output_file('chart.html')
#show(layout)