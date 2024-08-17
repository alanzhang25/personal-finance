from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd

default_start_amount = 100
default_contribution_amount = 5000
default_month_interval = 12 * 2.5
default_difference = .001

def filter_dataframe_by_date (df, start_date=datetime(1500, 1, 1), end_date=datetime(9999, 1, 1)):
    
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    filtered_df.head()

    return filtered_df.reset_index(drop=True)

def compare_growth_of_diff_leverages (df, start_amount, contributions=default_contribution_amount):
    df.loc[0, "Total Normal Amount"] = start_amount
    df.loc[0, "Total 3x Leveraged Amount"] = start_amount
    df.loc[0, "Total 2.5x Leveraged Amount"] = start_amount
    df.loc[0, "Total 2x Leveraged Amount"] = start_amount
    for i in range(1, len(df)):
        percent_change = df.loc[i, "Percent Change"] - default_difference
        interest_change  = df.loc[i, "Interest"]
        df.loc[i, 'Total Normal Amount'] = df.loc[i - 1, 'Total Normal Amount'] * (1 + percent_change) + contributions
        df.loc[i, 'Total 3x Leveraged Amount'] = df.loc[i - 1, 'Total 3x Leveraged Amount'] * (1 + ((3 * percent_change) - (2 * interest_change))) + contributions
        df.loc[i, 'Total 2.5x Leveraged Amount'] = df.loc[i - 1, 'Total 2.5x Leveraged Amount'] * (1 + ((2.5 * percent_change) - (1.5 * interest_change))) + contributions
        df.loc[i, 'Total 2x Leveraged Amount'] = df.loc[i - 1, 'Total 2x Leveraged Amount'] * (1 + ((2 * percent_change) - (1 * interest_change))) + contributions
    return df

def calculate_diff_leverages_growth(df, month_interval=default_month_interval, startamount=default_start_amount, contributions=default_contribution_amount):
    start_date = datetime(1871, 1, 1)
    end_date = datetime(1906, 1, 1)

    normal_end_amounts = []
    leveraged3x_end_amounts = []
    leveraged25x_end_amounts = []
    leveraged2x_end_amounts = []
    while end_date < datetime(2024, 1, 1):
        new_df = filter_dataframe_by_date(df, start_date, end_date)
        new_df = compare_growth_of_diff_leverages(new_df, startamount, contributions)

        normal_end_amount = new_df["Total Normal Amount"].iloc[-1]
        leveraged3x_end_amount = new_df["Total 3x Leveraged Amount"].iloc[-1]
        leveraged25x_end_amount = new_df["Total 2.5x Leveraged Amount"].iloc[-1]
        leveraged2x_end_amount = new_df["Total 2x Leveraged Amount"].iloc[-1]

        normal_end_amounts.append(normal_end_amount)
        leveraged3x_end_amounts.append(leveraged3x_end_amount)
        leveraged25x_end_amounts.append(leveraged25x_end_amount)
        leveraged2x_end_amounts.append(leveraged2x_end_amount)


        start_date += relativedelta(months=month_interval)
        end_date += relativedelta(months=month_interval)

    print(end_date)
    return normal_end_amounts, leveraged3x_end_amounts, leveraged25x_end_amounts, leveraged2x_end_amounts


### GLIDE PATHS

def calculate_growth_with_glide_path (df, list_of_glide_path_func, start_amount=default_start_amount, contributions=default_contribution_amount,):
    df.loc[0, "Total Normal Amount"] = start_amount
    leverage_amount_str =  "Total Leveraged Amount "
    for i in range(0, len(list_of_glide_path_func)):
        t = leverage_amount_str + str(i)
        df.loc[0, t] = start_amount

    first_occur_arr = [0 for _ in range(len(list_of_glide_path_func))]
    happ = [False for _ in range(len(list_of_glide_path_func))]
    for i in range(1, len(df)):
        percent_change = df.loc[i, "Percent Change"] - default_difference
        interest_change  = df.loc[i, "Interest"]
        df.loc[i, 'Total Normal Amount'] = df.loc[i - 1, 'Total Normal Amount'] * (1 + percent_change) + contributions


        for x, glide_path_func in enumerate(list_of_glide_path_func):
            t = leverage_amount_str + str(x)
            prev_amount = df.loc[i - 1, t]
            glide_path = glide_path_func(prev_amount)
            df.loc[i, t] = max(1, prev_amount * (1 + ((glide_path * percent_change) - ((glide_path - 1) * interest_change))) + contributions)
            if (not happ[x] and df.loc[i, t] > 5000000):
                first_occur_arr[x] = i
                happ[x] = True

    
    return df, first_occur_arr

def calculate_all_amounts_with_glide_paths(df, list_of_glide_path_func, month_interval=default_month_interval, start_amount=default_start_amount, contributions=default_contribution_amount):
    # 30 year time period
    start_date = datetime(1871, 1, 1)
    end_date = datetime(1901, 1, 1)

    array_of_amounts = []
    for _ in range(len(list_of_glide_path_func) + 1):
        array_of_amounts.append([])

    months_arr = []
    for _ in range(len(list_of_glide_path_func) ):
        months_arr.append([])

    while end_date < datetime(2024, 1, 1):
        new_df = filter_dataframe_by_date(df, start_date, end_date)
        new_df, index_of_months = calculate_growth_with_glide_path(new_df, list_of_glide_path_func, start_amount, contributions)

        for i in range(0, len(list_of_glide_path_func) + 1):
            if (i == 0):
                normal_end_amount = new_df["Total Normal Amount"].iloc[-1]
                array_of_amounts[i].append(normal_end_amount)
            else :
                leverage_amount_str =  "Total Leveraged Amount "
                temp_str = leverage_amount_str + str(i - 1)
                array_of_amounts[i].append(max(1, new_df[temp_str].iloc[-1]))

        for index, value in enumerate(index_of_months):
            months_arr[index].append(value)
    
        start_date += relativedelta(months=month_interval)
        end_date += relativedelta(months=month_interval)

    print(end_date)
    return months_arr, array_of_amounts


# Visualize the 30-year growth periods to see how volatile  
def visualize(df, list_of_glide_path_func, month_interval=default_month_interval, start_amount=default_start_amount, contributions=default_contribution_amount):
    # 30 year time period
    start_date = datetime(1871, 1, 1)
    end_date = datetime(1901, 1, 1)

    single_df = pd.DataFrame()
    idx = 0
    happ = True
    while end_date < datetime(2024, 1, 1):
        new_df = filter_dataframe_by_date(df, start_date, end_date)
        new_df, index_of_months = calculate_growth_with_glide_path(new_df, list_of_glide_path_func, start_amount, contributions)

        if (happ & idx < 40):
            single_df[f"Line {idx + 1}"] = new_df[["Total Leveraged Amount 0"]]
            idx = idx + 1

        happ = not happ
    
        start_date += relativedelta(months=month_interval)
        end_date += relativedelta(months=month_interval)

    print(end_date)
    return single_df
    


def calculate_growth_with_glide_path_opt (df, glide_func, start_amount=default_start_amount, contributions=default_contribution_amount):
    df.loc[0, "Total Leveraged Amount"] = start_amount

    for i in range(1, len(df)):
        percent_change = df.loc[i, "Percent Change"] - default_difference
        interest_change  = df.loc[i, "Interest"]

        prev_amount = df.loc[i - 1, "Total Leveraged Amount"]
        glide_path = glide_func(prev_amount)
        df.loc[i, 'Total Leveraged Amount'] = max(1, prev_amount * (1 + ((glide_path * percent_change) - ((glide_path - 1) * interest_change))) + contributions)

    
    return df

def calculate_amount_with_glide_path_opt(df, glide_func, month_interval=default_month_interval, start_amount=default_start_amount, contributions=default_contribution_amount):
    start_date = datetime(1871, 1, 1)
    end_date = datetime(1901, 1, 1)

    leverage_amount = []

    while end_date < datetime(2024, 1, 1):
        new_df = filter_dataframe_by_date(df, start_date, end_date)
        new_df = calculate_growth_with_glide_path_opt(new_df, glide_func, start_amount, contributions)

        leverage_amount.append(max(1, new_df['Total Leveraged Amount'].iloc[-1]))
    
        start_date += relativedelta(months=month_interval)
        end_date += relativedelta(months=month_interval)

    #print(end_date)
    return np.array(leverage_amount)
