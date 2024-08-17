import numpy as np


# This is a list of manual glide path functions we wrote

# amplitude (1, 10)
# steepness (0.5, 10)
# horitonzal shift (1, 10)
# lower bound (0, 2)
def normalized_sigmoid(amount):
    amount = amount / 1000000
    amplitude, steepness, horizontal_shift = 5, 1.42234210, 5
    return amplitude / (1 + np.exp(steepness * (amount - horizontal_shift)))

def sigmoid_glide_path(amount):
    max_amount = 10000000
    steepness = 0.0000015
    # The logistic sigmoid function scaled to range from 1 to 3
    sigmoid = 1 / (1 + np.exp(-steepness * (amount - max_amount / 2)))
    return 5 - 4 * sigmoid

def linear_glide_path(amount, start_value=5, end_value=1, max_amount=10000000):
    if (amount > max_amount):
        return 1
    slope = (end_value - start_value) / max_amount
    return start_value + slope * amount

def other_glide_path (amount):
    amount = amount/1000000
    if amount < 2:
        return 5
    elif 2 <= amount <= 10:  # Adjusted curve to start from glide path of 5
        # Using a logarithmic curve for a smoother transition from 5
        return 5 - 4 * np.log10(1 + amount - 2) / np.log10(9)
    else:
        return 1
    
def other2_glide_path (amount):
    lev = 4000000/(amount+1)
    return max(1, min(3, lev+.3))

def constant_leverage (amount, lev=3):
    return lev


def book_path (amount):
    if amount < 100000:
        return -1/50000 * amount + 5
    elif amount < 250000:
        return -1/150000 * amount + 3.67
    elif amount < 1000000:
        return -1/750000*amount + 2.33
    else:
        return 1
