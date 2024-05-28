import yfinance as yf
import pandas as pd
import talib
import matplotlib.pyplot as plt
import numpy as np
import datetime

# Fetch historical stock data from yfinance
ticker = input('Ticker: ')  # Example ticker symbol for Apple Inc.

end_date = datetime.datetime.now().strftime('%Y-%m-%d')
# DEFINE TIME PERIOD
start_date = (datetime.datetime.now() - datetime.timedelta(days=365*1)).strftime('%Y-%m-%d')
print(start_date)

data = yf.download(ticker, start=start_date, end=end_date)

# Extract the high and low prices from the historical data
high_prices = data['High'].values
low_prices = data['Low'].values

# Generate all possible price points between the high and low for each day
all_prices = []
for high, low in zip(high_prices, low_prices):
    if high != low:  # Avoid division by zero for days where high equals low
        prices = np.linspace(low, high, num=100)  # Adjust 'num' for more granularity
        all_prices.extend(prices)

# Convert list to numpy array for histogram calculation
all_prices = np.array(all_prices)

# Define the number of bins for the histogram
num_bins = len(data)  # Adjust the number of bins as needed

# Create the histogram using numpy
counts, bin_edges = np.histogram(all_prices, bins=num_bins)

# Plot the histogram as a horizontal bar chart
plt.figure(figsize=(10, 6))
plt.barh(bin_edges[:-1], counts, height=bin_edges[1] - bin_edges[0], edgecolor='black')
plt.xlabel('Frequency')
plt.ylabel('Price')
plt.title(f'Horizontal Histogram of {ticker} Price Frequencies')

# Enable cross pointer
plt.grid(True)
plt.gca().set_aspect('auto')

# Define a variable to store the axhline object
horizontal_line = None

# Function to update horizontal line
def update_horizontal_line(event):
    global horizontal_line
    if event.inaxes:
        if horizontal_line:
            horizontal_line.set_ydata(event.ydata)
        else:
            horizontal_line = plt.axhline(y=event.ydata, color='gray', linestyle='--')
        plt.draw()

# Connect the update function to the figure
plt.gcf().canvas.mpl_connect('motion_notify_event', update_horizontal_line)

plt.show()