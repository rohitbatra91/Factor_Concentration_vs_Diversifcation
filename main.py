# Comparison of value portfolio returns by concentration
# Comparing decile to quintile to thirds
# Data is from kenneth french's factor library
# Sep 27 2022
# By Rohit Batra

import numpy as np
import matplotlib.pyplot as plt
import csv

with open('Value-Third-Quintile-Decile.csv', 'r') as file:
    next(file)  # skipping headers
    next(file)
    reader = csv.reader(file)
    # Setting initial arrays
    # Dates and spy_real_tr is what the value is at the end of the month
    dates = []
    value_top_third = []
    value_top_quintile = []
    value_top_decile = []

    # Importing the data sets
    for row in reader:
        dates.append(row[0])
        value_top_third.append(float(row[1]))
        value_top_quintile.append(float(row[2]))
        value_top_decile.append(float(row[3]))

# Compute the growth of a portfolio starting with an initial investment of $1
def portfolio_growth(monthly_portfolio_returns):
    # Calculating portfolio growth
    number_of_months = len(monthly_portfolio_returns)
    # Setting array, starting with 1
    portfolio_growth = np.zeros(number_of_months)
    portfolio_growth[0] = 1
    # Computing growth of portfolio value
    for i in range(number_of_months - 1):
        portfolio_growth[i+1] = portfolio_growth[i] * (1 + monthly_portfolio_returns[i] / 100)
    return portfolio_growth


def geometric_mean_calc(return_arr):
    n = len(return_arr)
    product = 1
    for i in range(n - 1):
        product = product * (1 + return_arr[i] / 100)
    geometric_mean = product ** (1 / n * 12) - 1
    return geometric_mean * 100


#The number of years to roll over
years_to_roll = 10
ROLL_PERIOD = years_to_roll * 12
#Creating the arrays for rolling returns
value_decile_rolling_returns = []
value_quintile_rolling_returns = []
value_third_rolling_returns = []

# Calculating the rolling returns
for i in range(0, len(dates) - ROLL_PERIOD-1):
    value_decile_rolling_returns.append((geometric_mean_calc(value_top_decile[i:ROLL_PERIOD + i])))
    value_quintile_rolling_returns.append((geometric_mean_calc(value_top_quintile[i:ROLL_PERIOD + i])))
    value_third_rolling_returns.append((geometric_mean_calc(value_top_third[i:ROLL_PERIOD + i])))

# Plotting Rolling Returns
fig, ax = plt.subplots()
ax.plot(dates[ROLL_PERIOD+1:], value_decile_rolling_returns,
        dates[ROLL_PERIOD+1:], value_quintile_rolling_returns,
        dates[ROLL_PERIOD+1:], value_third_rolling_returns)
plt.gca().legend(('Decile','Quintile', 'Third'))
# Configuring the plot
ax.set_xticks(np.linspace(0, len(dates)-ROLL_PERIOD - 1, int((len(dates) - ROLL_PERIOD)/ 12)))
ax.set_xticklabels(dates[ROLL_PERIOD:len(dates)- 1: 12])
fig.canvas.draw()
plt.xticks(rotation=75)
plt.title(str(years_to_roll) + " year rolling comparison between value portfolios")
plt.show()

# Calculating portfolio growth
portfolio_value_top_third = portfolio_growth(value_top_third)
portfolio_value_top_quintile = portfolio_growth(value_top_quintile)
portfolio_value_top_decile = portfolio_growth(value_top_decile)


# Too many sampling periods to calculate geometric growth with above calc
# So instead import another function to compute geometric growth
# Plotting overall growth
fig, ax = plt.subplots()
ax.plot(dates, portfolio_value_top_decile,
        dates, portfolio_value_top_quintile,
        dates, portfolio_value_top_third)
# Configuring the plot
ax.set_xticks(np.linspace(0, len(dates), int(len(dates)/ 12)))
ax.set_xticklabels(dates[0:len(dates)-1:12])
plt.gca().legend(("Decile", "Quintile", "Third"))
plt.xticks(rotation=75)
plt.yscale("log")
plt.title("Historical Value Portfolio Growth by Concentration")
plt.show()


if __name__ == '__main__':
    print('lol')