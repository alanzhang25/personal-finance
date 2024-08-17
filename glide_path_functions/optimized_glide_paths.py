import numpy as np



sigmoid_temp = [7.61645333e+00, 1.42234210e-06, 8.68306690e+06, 6.21570943e-01]
piecewise_temp = [-2.17423293e-07,  8.38021564e+00, -4.05258433e-06, 6.39217193e+00, -9.82229827e-06, 
                  9.32770644e+00, -1.10854224e-07,  2.22762317e+00, 
                  4.96697812e+06,  2.43985089e+06,  1.83686376e+06]

max_lev = 9
min_lev = 0.1


# you shouldn't have arbiiratry constarints on the minization funtion becuase how will the optimizer know what is happening
# this makes the function non-smooth I believe, if anything, those constraints need to be included as variables
def sigmoid(amount, arr):
    amplitude, steepness, hort_shift, lower_bound = arr
    exp_input = steepness * (amount - hort_shift)
    safe_exp_input = np.clip(exp_input, None, 700)
    return lower_bound + (amplitude / (1 + np.exp(safe_exp_input)))

def normalized_sigmoid(amount, arr):
    amount = amount / 1000000
    amplitude, steepness, horizontal_shift, lower_bound = arr
    return lower_bound + (amplitude / (1 + np.exp(steepness * (amount - horizontal_shift))))

def sigmoid_default(amount, arr=sigmoid_temp):
    amplitude, steepness, hort_shift, lower_bound = arr
    exp_input = steepness * (amount - hort_shift)
    safe_exp_input = np.clip(exp_input, None, 700)
    return min(max_lev, lower_bound + (amplitude / (1 + np.exp(safe_exp_input))))

def piecewise (amount, arr):
        amount = amount / 1000000
        slope_1, y_1, slope_2, y_2, slope_3, y_3, slope_4, y_4, x1, x2, x3 = arr
        if (amount < x1):
            return slope_1 * amount + y_1
        elif (amount >= x1 and amount < x2):
            return slope_2 * amount + y_2
        elif (amount >= x2 and amount < x3):
            return slope_3 * amount + y_3
        elif (amount >= x3):
            return slope_4 * amount + y_4
        
def piecewise_default (amount, arr=piecewise_temp):
        slope_1, y_1, slope_2, y_2, slope_3, y_3, slope_4, y_4, x1, x2, x3 = arr
        if (amount < x1):
            return slope_1 * amount + y_1
        elif (amount >= x1 and amount < x2):
            return slope_2 * amount + y_2
        elif (amount >= x2 and amount < x3):
            return slope_3 * amount + y_3
        elif (amount >= x3):
            return slope_4 * amount + y_4
        
def polynomial (amount, arr):
     five, four, three, two, one, hort_shift = arr
     amount = (amount / 1e6) - hort_shift
     res = five * amount**5 + four * amount**4 + three * amount**3 + two * amount**2 + one * amount**1
     return np.clip(res, min_lev, max_lev)
        
