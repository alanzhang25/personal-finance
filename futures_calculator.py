from sympy import symbols, Eq, solve, solve_linear_system, Matrix
import numpy as np

def market_drop(leveraged_x, new_leveraged_x):
    amount = 10000.
    leveraged_amount = amount * leveraged_x

    x = symbols('x')
    equation = Eq((leveraged_amount - x) / (amount - x), new_leveraged_x)
    total_amount_drop = solve(equation, x)[0]
    return total_amount_drop / amount

def test():
    mes = symbols('mes')
    vxus = symbols('vxus')

    system1= Matrix(( (1, 1, 9), (1, -1, 1)))

    return solve_linear_system(system1, mes, vxus)



mes_value = 4800 * 5
mes_maintence = 1200 * 2
mes_safety_net = mes_maintence


vxus_value = 100

def upro_mes_portfolio(ideal_lev, amount):
    total_ideal_eq = ideal_lev * amount
    
    # equation should be
    # 25000 * mes_num

    # 50,000 with 3x lev
    #
    #mes_amount = symbols('mes_amount')
    #vxus_amount = symbols('vsxus_amount')

    
    #ideal_lev = (mes_value * mes_amount + vxus_amount * vxus_value) / amount #calculating how much leverage we have
    #amount - (mes_amount * (mes_maintence +  mes_safety_net)) >= (vxus_amount * vxus_value) # making sure that what we own is less than our current amount of money AND bonds would go on right side of eq
    #also need to bound mes_amount and vxus_amount to whole integers

    best_lev = 0
    portfolio = {}
    num_iterations = int(amount / (mes_maintence + mes_safety_net)) + 2
    for i in range(0, num_iterations):
        mes_curr_amount = mes_value * i
        vxus_curr_amount = amount - (i * (mes_maintence +  mes_safety_net))

        temp_port = {"MES": i, "VXUS": vxus_curr_amount/vxus_value}
        curr_lev = (mes_curr_amount + vxus_curr_amount) / amount
        print(curr_lev, temp_port)
        if (np.abs((curr_lev - ideal_lev)) < np.abs((best_lev - ideal_lev))):
            best_lev = curr_lev
            portfolio = temp_port

    return best_lev, portfolio

res = upro_mes_portfolio(10, 100e3)
print(f"BEST CASE IS => {res}")