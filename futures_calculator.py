from sympy import symbols, Eq, solve

def market_drop(leveraged_x, new_leveraged_x):
    amount = 10000.
    leveraged_amount = amount * leveraged_x

    x = symbols('x')
    equation = Eq((leveraged_amount - x) / (amount - x), new_leveraged_x)
    total_amount_drop = solve(equation, x)[0]
    return total_amount_drop / amount


#given a ratio of 50/50 for upro and mes
def upro_mes_portfolio(curr_lev):
    amount = 10000.
    

print(market_drop(3, 4))