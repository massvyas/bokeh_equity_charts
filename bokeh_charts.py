# Perform necessary imports
import glob
import os
import datetime as dt
from bokeh.io import curdoc, output_file, show, output_notebook
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, DateRangeSlider, Select
from bokeh.layouts import widgetbox, row, column
import pandas as pd

csv_files = glob.glob(r'C:\Users\massv\\OneDrive\Documents\Trading\data\*.csv')
csv_file_names = [os.path.basename(file)[:-4] for file in csv_files]

bars_shown = 200

data = pd.read_csv(r'C:\Users\massv\\OneDrive\Documents\Trading\data\NSEI.csv',parse_dates = True, index_col = 'Date')
data = data.fillna(method='ffill')
data['Bar'] = [i for i in range(len(data))]
data['Colors'] = ['Green' if data.iloc[i].Close > data.iloc[i].Open else 'Red' for i in range(len(data))]

end = max(data.index)
start = end - dt.timedelta(days=bars_shown)
 
# Make the ColumnDataSource: source
source = ColumnDataSource(data={
    'Date'    : data.loc[start:end].index,
    'Open'    : data.loc[start:end].Open.values,
    'High'    : data.loc[start:end].High.values,
    'Low'     : data.loc[start:end].Low.values,
    'Close'   : data.loc[start:end].Close.values,
    'Adj Close': data.loc[start:end,['Adj Close']].values,
    'Bar'     : data.loc[start:end].Bar.values,
    'Colors'  : data.loc[start:end].Colors
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
        'Colors'  : data.loc[start:end].Colors
    }) 
    source.data.update(new_data.data)
    
def update_selector(attr, old, new):
    #Use global data variable
    global data
       
    # Set the yr name to slider.value and new_data to source.data
    new_value = select.value
    idx = csv_file_names.index(new_value)
    
    data = pd.read_csv(csv_files[idx],parse_dates = True, index_col = 'Date')
    data = data.fillna(method='ffill')
    data['Bar'] = [i for i in range(len(data))]
    data['Colors'] = ['Green' if data.iloc[i].Close > data.iloc[i].Open else 'Red' for i in range(len(data))]

    end = max(data.index)
    start = end - dt.timedelta(days=bars_shown)
 
    # Make the ColumnDataSource: source
    new_data = ColumnDataSource(data={
        'Date'    : data.loc[start:end].index,
        'Open'    : data.loc[start:end].Open.values,
        'High'    : data.loc[start:end].High.values,
        'Low'     : data.loc[start:end].Low.values,
        'Close'   : data.loc[start:end].Close.values,
        'Adj Close': data.loc[start:end,['Adj Close']].values,
        'Bar'     : data.loc[start:end].Bar.values,
        'Colors'  : data.loc[start:end].Colors
    })
    
    source.data.update(new_data.data)

# Make a slider object: slider
slider = DateRangeSlider(title="Date Range: ", start=min(data.index), end=max(data.index), 
                         value=(start,end), step=1, width=1000)

# Create the figure: p
p = figure(title='Line chart', x_axis_label='Dates', y_axis_label='Closing Price', 
           x_axis_type='datetime', plot_height=400, plot_width=1300)
p.segment('Bar', 'High', 'Bar', 'Low', source=source, line_width=1, color='black')  # plot the wicks
p.vbar('Bar', 0.7, 'Close', 'Open', source=source, line_color='black', fill_color = 'Colors')

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
    value='NSEI',
    title='Stock Selector'
)

select.on_change('value', update_selector)

# Add the plot to the current document and add a title
layout = column(row(select, widgetbox(slider)), p)
curdoc().add_root(layout)
curdoc().title = 'Stock Chart'

# Output the file and show the figure
#output_file('chart.html')
#show(layout)