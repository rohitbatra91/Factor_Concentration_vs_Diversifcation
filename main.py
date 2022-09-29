# Comparison of value portfolio returns by concentration
# Comparing decile to quintile to thirds
# Data is from kenneth french's factor library
# Sep 27 2022
# By Rohit Batra

import numpy as np
import matplotlib.pyplot as plt
import csv

with open('Value-Third-Quintile-Decile.csv', 'r') as file:
    next(file), next(file)  # skipping title and column names
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
    number_of_months = len(monthly_portfolio_returns)
    # Initializing array, starting with 1
    portfolio_growth_arr = np.zeros(number_of_months)
    portfolio_growth_arr[0] = 1
    # Computing growth of portfolio value
    # current month value = last month value * (1 + monthly return / 100)
    for i in range(number_of_months - 1):
        portfolio_growth_arr[i+1] = portfolio_growth_arr[i] * (1 + monthly_portfolio_returns[i] / 100)
    return portfolio_growth_arr


# Function to calculate the geometric growth with from an array of returns
def geometric_mean_calc(returns_arr):
    n = len(returns_arr)
    product = 1
    for i in range(n - 1):
        product = product * (1 + returns_arr[i] / 100)
    geometric_mean = product ** (1/n * 12) - 1
    # Convert back to percent and return
    return geometric_mean * 100


# Calculating rolling returns
# The number of years to roll over
years_to_roll = 10
ROLL_PERIOD = years_to_roll * 12
num_roll_periods = len(dates)-ROLL_PERIOD-1
# Creating the arrays for rolling returns
value_decile_rolling_returns = []
value_quintile_rolling_returns = []
value_third_rolling_returns = []
# Initializing portfolio concentration winning counters
decile_win_count = 0
quintile_win_count = 0
third_win_count = 0

# Calculating the n year rolling returns and adding them to rolling returns array
# The geometric mean is calculated from a slice of the value monthly return arrays
for i in range(0, num_roll_periods):
    value_decile_rolling_returns.append((geometric_mean_calc(value_top_decile[i:i + ROLL_PERIOD])))
    value_quintile_rolling_returns.append((geometric_mean_calc(value_top_quintile[i:i + ROLL_PERIOD])))
    value_third_rolling_returns.append((geometric_mean_calc(value_top_third[i:i + ROLL_PERIOD])))
    # Calculating the winner during the roll period and adding to its count
    # Decile win
    if (value_decile_rolling_returns[i] > value_quintile_rolling_returns[i] and
            value_decile_rolling_returns[i] > value_third_rolling_returns[i]):
        decile_win_count += 1
    # Quintile win
    elif (value_quintile_rolling_returns[i] > value_decile_rolling_returns[i] and
            value_quintile_rolling_returns[i] > value_third_rolling_returns[i]):
        quintile_win_count += 1
    # Third win
    else:
        third_win_count += 1

# Calculating the percentage of times each roll period won
percent_decile_win = decile_win_count/num_roll_periods * 100
percent_quintile_win = quintile_win_count/num_roll_periods * 100
percent_third_win = third_win_count/num_roll_periods * 100

print("Decile wins " + str(percent_decile_win) + " percent of the time.")
print("Quintile wins " + str(percent_quintile_win) + " percent of the time.")
print("Third wins " + str(percent_third_win) + " percent of the time.")

# Calculating portfolio growth
portfolio_value_top_third = portfolio_growth(value_top_third)
portfolio_value_top_quintile = portfolio_growth(value_top_quintile)
portfolio_value_top_decile = portfolio_growth(value_top_decile)

# Plotting Rolling Returns
fig, ax = plt.subplots()
ax.plot(dates[ROLL_PERIOD+1:], value_decile_rolling_returns,
        dates[ROLL_PERIOD+1:], value_quintile_rolling_returns,
        dates[ROLL_PERIOD+1:], value_third_rolling_returns)
# Configuring the plot
ax.set_xticks(np.linspace(0, len(dates)-ROLL_PERIOD - 1, int((len(dates) - ROLL_PERIOD)/12)))
ax.set_xticklabels(dates[ROLL_PERIOD:len(dates) - 1: 12])
plt.xticks(rotation=75)
plt.title(str(years_to_roll) + " year rolling comparison between value portfolios")
plt.gca().legend(('Decile', 'Quintile', 'Third'))
plt.show()

# Too many sampling periods to calculate geometric growth with above calc
# So instead import another function to compute geometric growth
# Plotting overall growth
fig, ax = plt.subplots()
ax.plot(dates, portfolio_value_top_decile,
        dates, portfolio_value_top_quintile,
        dates, portfolio_value_top_third)
# Configuring the plot
# Adjusting the x labels to yearly
ax.set_xticks(np.linspace(0, len(dates), int(len(dates) / 12)))
ax.set_xticklabels(dates[0:len(dates)-1:12])
plt.xticks(rotation=75)
plt.yscale("log")
plt.title("Historical Value Portfolio Growth by Concentration")
plt.gca().legend(("Decile", "Quintile", "Third"))
plt.show()


if __name__ == '__main__':
    print('lol')
