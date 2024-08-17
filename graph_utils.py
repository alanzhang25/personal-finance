from utils import calc_quartile_avg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def line_graph_of_each_glide_path(glide_path_functions):
    amounts = np.linspace(0, 10000000, 1000)  # From 0 to 10,000,000
    # chose glide path function to graph below
    # Plotting
    plt.figure(figsize=(10, 6))
    for label, func in glide_path_functions:
        glide_path_values = [func(amount) for amount in amounts]
        plt.plot(amounts, glide_path_values, label=label)

    scale_factor = 1e6
    ticks = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_factor))
    plt.gca().xaxis.set_major_formatter(ticks)
    plt.title('Glide Path Function Graph')
    plt.xlabel('Amount (in millions)')
    plt.ylabel('Glide Path Value')
    plt.grid(True)
    plt.legend()
    plt.show()

def box_plot_comparison_of_glide_paths(leverage_list, list_of_glide_path_func):
    # Plotting side-by-side boxplots
    series_list = [pd.Series(inner_list) for inner_list in leverage_list]
    plt.figure(figsize=(8, 14))
    plt.boxplot(series_list, positions=[i for i in range(1,len(series_list) + 1)], showfliers=True)

    # Calculate the xth percentile for each dataset
    xth_perc = 3
    for i, series in enumerate(series_list):
        percentile = np.percentile(series, xth_perc)
        mean_mark = np.mean(series)
        quartile_avg = calc_quartile_avg(series, False)
        print(quartile_avg)
        plt.hlines(percentile, i + 0.9, i + 1.1, linestyles='dashed', color='blue')
        plt.hlines(mean_mark, i + 0.9, i + 1.1, linestyles='dashed', color='red')
        plt.hlines(quartile_avg, i + 0.9, i + 1.1, linestyles='dashed', color='green')

    plt.yscale('log')  # Using a logarithmic scale
    func_names = []
    func_names.append
    plt.xticks([i for i in range(1,len(series_list) + 1)], ["Normal"] + [func.__name__ for func in list_of_glide_path_func])
    plt.xticks(rotation=45)
    plt.title('Normal vs Leverage with Glide Returns')
    plt.ylabel('Value (log scale)')
    plt.show()