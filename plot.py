# RFCR Plot
# Radio Frequency Class Registrator
#
# Plots student count over time.

# - - - - - - - - - - - - - - - - - - - - - - - - -
# Import external modules
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, HoverTool
from os.path import dirname, join
import pandas as pd

# Set name of temporary directory where state and log and sound files are stored
TEMP_DIR = 'temp'

# Set name of data file
# Each line is of the form: timestamp, student count
DATA_FILE = join(dirname(__file__), TEMP_DIR, 'rfcr_graph.log')

# Function: Read data from log file
def read_data():
    global df, idx
    data_file = open(DATA_FILE, 'r')
    df = pd.read_csv(data_file, names=['x', 'y', 'name'], parse_dates=['x'], skiprows=idx)
    # Add column containing formatted date/time
    df['x_formatted'] = df['x'].apply(lambda d: d.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    idx += len(df)
    data_file.close()

# Function: Update graph with new data
def update_data():
    global ds
    read_data()
    if (len(df) > 0):
        new_data = df.to_dict(orient='list')
        print(new_data)
        ds.stream(new_data, 30)

    
# Initialize variables
df = pd.DataFrame()
idx = 0


# Initial read of data file
read_data()
print('Read {} existing log records.'.format(len(df)))

# Create data source, plot figure and line graph objects
ds = ColumnDataSource(df.to_dict(orient='list'))
plot = figure(title='RF Class Registrator', x_axis_label='time', x_axis_type='datetime',  y_axis_label='# of students')
circle = plot.circle(x='x', y='y', source=ds, size=6)
line = plot.line(x='x', y='y', source=ds, line_width=2)

# Default tooltips for data points
hover = HoverTool(
    renderers=[circle],
    tooltips=[
        ('Date', '@x_formatted'),
        ('Count', '@y'),
        ('Student', '@name'),
    ]
)
plot.add_tools(hover)

# Add figure to the defailt document, and set the data update callback
curdoc().add_root(plot)
curdoc().add_periodic_callback(update_data, 1000)
