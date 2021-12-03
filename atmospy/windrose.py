import numpy as np
import pandas as pd

#   open_air | exp                    | plotly
#   -------------------------------------------
#   mydata   | data frame             | df
#   ws       | column for windspeed   | ws
#   wd       | column for wind dir.   | wd
#   angle    | angle of spokes        | angle
#   ws.int   | interval between color | ws_int
#   type     | var to split data      | cutby
#   ---      | df column for timestamp| time

#TO DO:
# cut_data needs to be improved to allow cutting by user given categories.
# wind_rose needs unique titles when the cutby variable is defined.

def cut_data(df, cutby, timestamp="timestamp"):

    if cutby == "season":
        seasons = ['Winter','Spring','Summer','Fall']
        time = [i.month%12 // 3 for i in df[timestamp]]
        df["season"] = [seasons[i] for i in time]

    elif cutby == "hour":
        df["hour"] = [i.hour for i in df[timestamp]]

    elif cutby == "month":
        df["month"] = [i.month for i in df[timestamp]]

    elif cutby == "year":
        df["year"] = [i.year for i in df[timestamp]]

    elif cutby == "weekday":
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        df["weekday"] = [days[i.weekday()] for i in df[timestamp]]

    return df


def wind_rose(df, wd, ws, time, angle=10, ws_int=2, cutby=None, **kwargs):

    #sort values by windspeed
    df = df.sort_values(by=[ws])

    #calculate bins for wind direction
    num_spokes = 360//angle
    dir_bin = np.linspace(0, num_spokes - 1, num_spokes) * angle

    num_colors = int(df.wind_speed.max() // ws_int)

    speed_bin = np.linspace(0, num_colors - 1, num_colors) * ws_int

    speed_dict = {}
    for i in range(len(speed_bin)):
        if i != len(speed_bin) - 1:
            speed_str = f'{speed_bin[i]:.2f} - {speed_bin[i+1]:.2f}'
        else:
            speed_str = f'{speed_bin[i]:.2f} +'
        speed_dict[speed_bin[i]] = speed_str

    if cutby:

        df = cut_data(df, cutby, time)
        categories = df[cutby].unique()
        plots = []

        for i in categories:
            print(df)
            sub_df = df[df[cutby] == i]
            print(sub_df)

            direction = []
            speed = []
            speed_count = []

            sub_df.wind_dir = dir_bin[np.digitize(sub_df.wind_dir, dir_bin) - 1]
            sub_df.wind_speed = speed_bin[np.digitize(sub_df.wind_speed, speed_bin) - 1]

            for wd in sub_df.wind_dir.unique():
                x = sub_df.wind_speed[df.wind_dir == wd]
                unique, count = np.unique(x, return_counts=True)
                for i in range(len(unique)):
                    direction = np.append(direction, wd)
                    speed = np.append(speed, speed_dict[unique[i]])
                    speed_count = np.append(speed_count, count[i])


            plot_df = pd.DataFrame({'theta':direction, 'speed (m/s)': speed, 'r':speed_count})

            plots.append(px.bar_polar(plot_df, r="r", theta="theta", color="speed (m/s)", **kwargs))

        return plots



    else:

        direction = []
        speed = []
        speed_count = []

        df.wind_dir = dir_bin[np.digitize(df.wind_dir, dir_bin) - 1]
        df.wind_speed = speed_bin[np.digitize(df.wind_speed, speed_bin) - 1]

        for wd in df.wind_dir.unique():
            x = df.wind_speed[df.wind_dir == wd]
            unique, count = np.unique(x, return_counts=True)
            for i in range(len(unique)):
                direction = np.append(direction, wd)
                speed = np.append(speed, speed_dict[unique[i]])
                speed_count = np.append(speed_count, count[i])


        plot_df = pd.DataFrame({'theta':direction, 'speed (m/s)': speed, 'r':speed_count})

        return [px.bar_polar(plot_df, r="r", theta="theta", color="speed (m/s)", **kwargs)]


if __name__ == "__main__":

    import plotly.express as px
    import pandas as pd
    import numpy as np
    import pickle
    from datetime import datetime

    
    df = pd.read_csv("test.csv")
    df.timestamp = [datetime.fromisoformat(i) for i in df.timestamp]

    options = {'template': 'plotly_dark', 'color_discrete_sequence': px.colors.sequential.Plasma_r, 'log_r': False, 'title':'Wind Plot'}

    figs = wind_rose(df, wd="wind_dir", ws="wind_speed", time="timestamp", ws_int=5, cutby="hour", **options)

    for i in figs:
        i.show()