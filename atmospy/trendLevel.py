# Implementing openair's trendLevel function in python
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import time, timedelta, datetime

def generate_data(years=6):
    # Create dataframe with hour, month, year, and pollutant cols
    np.random.seed(1)
    
    base = datetime.combine(datetime.today(), time.min)
    dates = base - np.arange(360*years) * timedelta(days=1)
    dates += np.random.rand(len(dates)) * timedelta(days=1)
    dates = pd.DatetimeIndex(dates)
    df = pd.DataFrame({
        'hour': dates.hour,
        'month': dates.month,
        'year': dates.year,
        'pollutant': np.random.random(len(dates)) * 500
    })
    return df.iloc[::-1].reset_index(drop=True)

def add_common_date_time(df):
    # Utility to add to dataframe individual second, minute, hour, month, year time measurments
    dates = pd.DatetimeIndex(df['timestamp'])
    df['second'] = dates.second
    df['minute'] = dates.minute
    df['hour'] = dates.hour
    df['month'] = dates.month
    df['year'] = dates.year
    
def trendLevel(mydata, pollutant, x, y, category_type, n_levels=(10, 10, 4), statistic='avg', title=None):
    """
    openair trendLevel R function adapted into python.

    The trendLevel function provides a way of rapidly showing a large
    amount of data in a condensed form. In one plot, the variation in
    the concentration of one pollutant can to shown as a function of
    three other categorical properties.

    Currently does not have provide custom statistic method or categorical color scale

    Original: https://github.com/davidcarslaw/openair/blob/master/R/trendLevel.R
    
    Attributes:
        mydata: The data frame to use to generate the trendLevel plot
        pollutant: The name of the data seriesinmydatato sample to produce the trendLevel plot
        x: The name of the data series to use as the trendLevel x-axis
        y: The name of the data series to use as the trendLevel y-axis
        category_type: partitions data by specific data series 
        n_levels: The number of levels to split x, y and category_type data into if numeric
        statistic: The statistic method to be use to summarise locally binned pollutant
        measurements with. Possible statistic methods are 'count', 'sum', 'avg', 'min', or 'max'
        title: The title of the graph
    """

    # Check valid input
    if x not in mydata.columns:
        raise Exception(f'{x} does not exist in df')
    if y not in mydata.columns:
        raise Exception(f'{y} does not exist in df')
    if pollutant not in mydata.columns:
        raise Exception(f'{pollutant} does not exist in df')
    if category_type not in mydata.columns:
        raise Exception(f'{category_type} does not exist in df')
    if not len(set([x, y, category_type])) == len([x, y, category_type]):
        raise Exception(f'x, y and type cannot match')

    plot_parameters = {
        'data_frame': mydata,
        'x': x,
        'y': y,
        'z': pollutant,
        'histfunc': statistic,
        'nbinsx': n_levels[0],
        'nbinsy': n_levels[1],
        'title': title
    }

    # Type cutting/binning
    if n_levels[2] > 1:
        min_type, max_type = min(mydata[category_type]), max(mydata[category_type])
        bins = np.linspace(min_type, max_type, num=n_levels[2]+1)
        indicies = np.searchsorted(bins, mydata[category_type])
        facet = []
        for i in indicies:
            start = i
            if start == len(bins) - 1:
                start -= 1
            begin, end = round(bins[start], 4), round(bins[start+1], 4)
            if bins[start].is_integer() and bins[start+1].is_integer():
                begin, end = int(bins[start]), int(bins[start+1])
            facet.append(f"{category_type} {begin} to {end}")
        mydata['facet'] = facet

        plot_parameters.update({'facet_col': facet,
                                'facet_col_wrap': 3,
                                'facet_row_spacing': 0.03,
                                'facet_col_spacing': 0.001})
    
    fig = px.density_heatmap(**plot_parameters)

    if 'facet_col' in plot_parameters:
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig.update_xaxes(title='')
        fig.update_yaxes(title='')
        fig.add_annotation(x=0.5, y=-.08, text=x,
                        xref="paper", yref="paper")
        fig.add_annotation(x=-0.01, y=0.5,
                        text=y, textangle=-90,
                        xref="paper", yref="paper")

    fig.show()

# df = pd.read_pickle('tests/datafiles/test_csvs/test.pckl')
# add_common_date_time(df)
# trendLevel(df, 'no2', 'hour', 'minute', 'year', n_levels=(24, 60, 2), title='Test Air Data')

trendLevel(generate_data(), 'pollutant', 'month', 'hour', 'year', n_levels=(12, 24, 1), statistic='avg', title='Testing TrendLevel w/ Generated Data')
