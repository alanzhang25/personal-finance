import numpy as np

def calc_quartile_avg (passed_list, log=True):
    if (log):
        passed_list = np.log10(passed_list)
    weight_quartile_1 = 0.4
    weight_quartile_2 = 0.3
    weight_quartile_3 = 0.2
    weight_quartile_4 = 0.1
    weight_quartile_5 = 0

    percentile_20 = np.percentile(passed_list, 20)
    percentile_40 = np.percentile(passed_list, 40)
    percentile_60 = np.percentile(passed_list, 60)
    percentile_80 = np.percentile(passed_list, 80)

    quartile_1 = np.mean(passed_list[passed_list < percentile_20])
    quartile_2 = np.mean(passed_list[(passed_list >= percentile_20) & (passed_list < percentile_40)])
    quartile_3 = np.mean(passed_list[(passed_list >= percentile_40) & (passed_list < percentile_60)])
    quartile_4 = np.mean(passed_list[(passed_list >= percentile_60) & (passed_list < percentile_80)])
    quartile_5 = np.mean(passed_list[passed_list >= percentile_80])
    avg = weight_quartile_1 * quartile_1 + weight_quartile_2 * quartile_2 + weight_quartile_3 * quartile_3 + weight_quartile_4 * quartile_4 + weight_quartile_5 * quartile_5

    return avg
