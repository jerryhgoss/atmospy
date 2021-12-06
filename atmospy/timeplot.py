# Using plotly.express
import plotly.express as px
import pandas as pd
import pickle

df = pd.read_csv('BostonAir.csv')

def time_plot(mydata, x, y, title=None):
    """

    WIP openair timeplot R function adapted into python

    Function thats designed to quickly plot time series of data, 
    for several pollutants/variables. You can choose the time period
    of interest and will show hourly high resolution data, with a lot 
    of customizability in color and width. 

    mydata: The data frame to use to generate the trendLevel plot
        pollutant: The name of the data seriesinmydatato sample to produce the trendLevel plot
        x: The name of the data series to use as the trendLevel x-axis
        y: The name of the data series to use as the trendLevel y-axis
    title: The title of the graph 
    """

    if x not in mydata.columns:
        raise Exception(f'{x} does not exist in df')
    if y not in mydata.columns:
        raise Exception(f'{y} does not exist in df')

    
    fig = px.line(mydata, x, y, title)

    fig.show()


if __name__ == "__main__":

    import plotly.express as px
    import pandas as pd
    import numpy as np
    import pickle
    from datetime import datetime

    
    df = pd.read_csv("test.csv")
