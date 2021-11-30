# Implementing openair's trendLevel function in python
import plotly.express as px
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
    
# def trendLevel(mydata, pollutant, x, y, statistic='avg'):
def trendLevel(mydata, pollutant, x, y, type, n_levels=(10, 10, 4), labels=None, breaks=None, statistic='avg', title=None):
    """
    openair trendLevel R function adapted into python.

    The trendLevel function provides a way of rapidly showing a large
    amount of data in a condensed form. In one plot, the variation in
    the concentration of one pollutant can to shown as a function of
    three other categorical properties. The default version of the
    plot uses y = hour of day, x = month of year and type = year to
    provide information on trends, seasonal effects and diurnal
    variations. However, x, y and type and summarising statistics can
    all be modified to provide a range of other similar plots.
    Original: https://github.com/davidcarslaw/openair/blob/master/R/trendLevel.R
    
    Attributes:
        model: A string representing the spaceship model name.
        mass: An int representing the mass of the spaceship in kilograms.
        engine_span: An int representing the distance in meters between the
            spaceship's left and right engines.
        pilot: A string represent the name of the spaceship pilot.
        fuel: An int representing the fuel level of the spaceship.
        angle: A float representing the current angle of the spaceship in
            radians, with 0 being the spaceship nose pointing right.
    """

    pollutant_categorical = False
    if (labels and breaks):
        pollutant_categorical = True

    # Check valid input

    # type cutting
    min_type, max_type = min(mydata[type]), max(mydata[type])
    bins = np.linspace(min_type, max_type, num=n_levels[2])
    print(bins)
    indicies = np.searchsorted(bins, mydata[type])
    facet = []
    # TODO: edge cases where only 1 bin, have to check
    for i in indicies:
        start = i
        if start == len(bins) - 1:
            start -= 1
        facet.append(f"{type} {bins[start]} to {bins[start+1]}")
    mydata['facet'] = facet

    fig = px.density_heatmap(mydata,
                             x,
                             y,
                             z=pollutant,
                             histfunc=statistic,
                             facet_col=facet,
                             facet_col_wrap=3,
                             facet_row_spacing=0.03,
                             facet_col_spacing=0.001,
                             nbinsx=n_levels[0],
                             nbinsy=n_levels[1],
                             title=title)
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
trendLevel(generate_data(), 'pollutant', 'month', 'hour', 'year', n_levels=(12, 24, 6), title='Testing TrendLevel w/ Generated Data')
