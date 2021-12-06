import plotly.express as px
import pandas as pd


df = pd.read_csv('BostonAir.csv')

def scatter_plot(mydata, x, y, title=None):
    """

    WIP openair scatterplot R function adapted into python

    Function thats designed to quickly plot a scatterplot of data, 
    for two pollutants/variables. 

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

    fig = px.scatter(mydata, x, y, title)
    
    fig.show()

if __name__ == "__main__":

    import plotly.express as px
    import pandas as pd
    import numpy as np
    import pickle
    from datetime import datetime

    
    df = pd.read_csv("test.csv")
