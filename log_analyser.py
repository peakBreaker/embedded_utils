"Time analysis from the logs"
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import re
import json


def get_log_line(file):
    "Generator for getting unpacked json data from logs one after another"
    with open(file, 'r') as f:
        for line in f:
            data_raw = json.loads(line)
            if "LOGS" in list(data_raw.keys())[0]:
                lognum = re.search("(?<=LOGS_)\d+", list(data_raw.keys())[0])
                lognum = int(lognum.group(0)) if lognum is not None else -1
                data_raw = list(data_raw.values())[0]
                data_raw['lognum'] = lognum
            yield data_raw

def analyse_init_json():
    
    # Get the data from file
    data_gen = get_json_log(get_log(json=True))
    df = pd.DataFrame(data=data_gen)

    # Convert timestamp to time and set index
    print('converting ts to datetime')
    df['ts'] = pd.to_datetime(df['ts'], unit='s')
    df.set_index('ts', inplace=True)
    
    # Lets see how we're doing
    print(df.tail())
    print("min value in init time %s " % str(df['init_time'].min()))
    print("max value in init time %s " % str(df['init_time'].max()))
    print("mean value in init time %s " % str(df['init_time'].mean()))
    print("Shape: %s" % str(df.shape))
    
    # f = plt.figure()
    ymean = df['init_time'].mean()
    
    ax = df.plot(secondary_y='bat_val')
    nan_indices = pd.isnull(df).any(1).nonzero()[0]
    nan_indices = df.iloc[nan_indices].index.tolist()
    # print("indexes of all nans")
    # print()
    ax.vlines(x=nan_indices, ymin=0, ymax=ymean+80, linestyles='dashed', color='r')
    # ax.vlines(x=inds, ymin=df['init_time'].min(), ymax=df['init_time'].min(), color='r')
    plt.show()

def plot_i2c_perf():
    # Get the data from file
    data_gen = get_json_log(get_log(json=True))
    df = pd.DataFrame(data=data_gen)

    # Convert timestamp to time and set index
    print('converting ts to datetime')
    df['ts'] = pd.to_datetime(df['ts'], unit='s')
    df.set_index('ts', inplace=True)

    # Lets see how we're doing
    print(df.tail())
    print("min value in init time %s " % str(df['init_time'].min()))
    print("max value in init time %s " % str(df['init_time'].max()))
    print("mean value in init time %s " % str(df['init_time'].mean()))
    print("Shape: %s" % str(df.shape))
    data_points = len(df.index)
    failures = df[df['init_time'] < 30]
    successes = df[df['init_time'] > 30]
    
    fail_indices = failures.index.tolist()
    success_indices = successes.index.tolist()
    
    print("Data points : %i" % data_points)
    print("Number of failures : %i" % len(fail_indices))
    print("Number of successes : %i" % len(success_indices))
    print("Successrate : %s%%" % round((len(success_indices)*100 / data_points), 2))
    
    df['init_time'] = 30
    ax = df.plot(legend=False, secondary_y='bat_val')

    ax.vlines(x=success_indices, ymin=0, ymax=1, linestyles='dashed', color='g')
    ax.vlines(x=fail_indices, ymin=0, ymax=failures['init_time'], linestyles='solid', color='r')

    plt.show()

def get_time(file):
    "Generator for getting time one by one"
    with open(file, 'r') as f:
        for line in f:
            if line[:2] == 'f_':
                yield np.nan
            else:
                yield line


def calc_stats(file):
    "Calculates modem stats and returns the np array"

    # Getting the data
    timing_generator = get_time(file)
    time_array = np.array([float(time) for time in timing_generator])
    
    # Structuring the data
    modem_stats = {"data_points": len(time_array),
                   "max": np.nanmax(time_array),
                   "min": np.nanmin(time_array),
                   "mean": np.nanmean(time_array)}
    
    # Print and return the stats
    print(modem_stats)
    return time_array


PLOT_TEXT_OFFSET = 10
def plt_stats(stats):
    "Shows a plot of the stats"
    
    # Creating the masked array and getting the indices of invalid values
    mx = np.ma.array(stats, mask=np.isnan(stats))
    nan_indices = np.argwhere(np.isnan(stats)).flatten()
    
    # calculate some intitial values for the plot
    ymax = mx.max()
    ymin = mx.min()
    ymean = mx.mean()
    
    # Create some attributes fot the plot
    
    # Initialize the figure and subplot
    f = plt.figure()
    ax = f.add_subplot(111)

    # Create the plot attributes
    ax.plot(mx)
    ax.vlines(x=nan_indices, ymin=ymean-5, ymax=ymean+5, color='r')
    plt.ylim(ymin - 10, ymax+PLOT_TEXT_OFFSET*3)
    
    plt.title('Plot of initalization time for devices')
    plt.xlabel('Measurement number')
    plt.ylabel('init time(sec)')
    plt.text(len(stats)/5, ymax + PLOT_TEXT_OFFSET, 'max=%s, \nmin=%s, \navg=%s, \ndata points=%s'
             % (ymax, ymin, ymean, len(stats)))
    
    # Save and show the plot
    # plt.savefig("stats.png")
    plt.show()
    return

    ax.imshow(stats, interpolation='nearest', cmap=cmap)
    f.canvas.draw()
    # Save and show the plot
    # 
    plt.show()

if __name__ == '__main__':
    plot_i2c_perf()
