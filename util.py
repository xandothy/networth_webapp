def calculate_networth(investments, debts, incomes, expenses):
    net_worth = 0
    total_values = investments['amount'] * investments['value']
    net_worth += total_values.sum()
    net_worth += incomes["value"].sum()

    net_worth -= debts['value'].sum()
    net_worth -= expenses['value'].sum()
    return net_worth