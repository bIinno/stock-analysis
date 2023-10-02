# Import necessary libraries
import logging
import requests
import time

# Define constants and API key
ALPHA_VANTAGE_API_KEY = "P9DSUB7ZTSEV3HIT"
ALPHA_VANTAGE_API_URL = "https://www.alphavantage.co/query"
ALPHA_VANTAGE_API_FUNCTION = "OVERVIEW"
ALPHA_VANTAGE_API_TICKER_FILE = "ticker.txt"

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

# Define custom thresholds for ratios
thresholds = {
    "PE Ratio": 1,  # Customize your threshold value here
    "PEG Ratio": 1,  # Customize your threshold value here
    "PriceToBookRatio": 0.7,  # Customize your threshold value here
    "EV to Revenue": 0.5,  # Customize your threshold value here for EV to Revenue
    # Add more ratios and thresholds as needed
}

# Function to get the stock data from AlphaVantage
def get_stock_data(ticker):
    # Define parameters
    params = {
        "function": ALPHA_VANTAGE_API_FUNCTION,
        "symbol": ticker,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    # Make the request to AlphaVantage
    response = requests.get(ALPHA_VANTAGE_API_URL, params=params)

    # If the status code is 200, return the response
    if response.status_code == 200:
        return response.json()
    # Otherwise, print an error message
    else:
        print(f"Error fetching data for {ticker}: {response.status_code}")
        return None

# Initialize the tickers variable as an empty list
tickers = []

# Read tickers from a text file with error handling
try:
    with open(ALPHA_VANTAGE_API_TICKER_FILE, "r") as ticker_file:
        tickers = ticker_file.read().splitlines()
except FileNotFoundError:
    print("Ticker file not found!")
except PermissionError:
    print("Permission denied to read ticker file!")
except Exception as e:
    print(f"Error reading ticker file: {str(e)}")

# Check if tickers were successfully loaded
if not tickers:
    print("No tickers found. Check the ticker file contents.")

# Create a list to store passed stocks
passed_stocks = []

# Loop through the tickers and fetch data for each
for i, ticker in enumerate(tickers, start=1):
    try:
        dataset = get_stock_data(ticker)
    except Exception as e:
        logging.error(f"Error fetching data for {ticker}: {str(e)}")
        print(f"Error fetching data for {ticker}. Skipping...")
        continue

    # Access and print specific parameters and check against thresholds
    if dataset:
        symbol = dataset.get('Symbol', 'N/A')
        sector = dataset.get('Sector', 'N/A')
        pe_ratio = dataset.get('PERatio', 'N/A')
        peg_ratio = dataset.get('PEGRatio', 'N/A')
        price_to_book_ratio = dataset.get('PriceToBookRatio', 'N/A')
        ev_to_revenue = dataset.get('EVToRevenue', 'N/A')

        # Initialize the missing_ratio flag to False
        missing_ratio = False

        # Check if each ratio is available and greater than or equal to the threshold
        if pe_ratio != 'None':
            pe_ratio = float(pe_ratio)
            if pe_ratio < thresholds.get('PE Ratio', float('-inf')):
                missing_ratio = True

        if peg_ratio != 'N/A':
            peg_ratio = float(peg_ratio)
            if peg_ratio < thresholds.get('PEG Ratio', float('-inf')):
                missing_ratio = True

        if price_to_book_ratio != 'N/A':
            price_to_book_ratio = float(price_to_book_ratio)
            if price_to_book_ratio < thresholds.get('PriceToBookRatio', float('-inf')):
                missing_ratio = True

        if ev_to_revenue != 'N/A':
            ev_to_revenue = float(ev_to_revenue)
            if ev_to_revenue < thresholds.get('EV to Revenue', float('-inf')):
                missing_ratio = True

        # Check if at least one ratio is available
        if not missing_ratio:
            print(f"{ticker} meets the threshold criteria.")
            passed_stocks.append((symbol, sector, pe_ratio, peg_ratio, price_to_book_ratio, ev_to_revenue))
        else:
            print(f"{ticker} does not meet the threshold criteria due to missing or below-threshold ratio(s).")

    if i % 5 == 0 and i < len(tickers):
        print(f"Waiting for 60 seconds to account for API rate limit...")
        time.sleep(60)

# Export passed stocks to an output file
output_file = "output.txt"
with open(output_file, "w") as f:
    f.write("Symbol, Sector, PE Ratio, PEG Ratio, Price-to-Book Ratio, EV to Revenue\n")
    for stock in passed_stocks:
        symbol, sector, pe_ratio, peg_ratio, price_to_book_ratio, ev_to_revenue = stock
        f.write(f"{symbol}, {sector}, {pe_ratio}, {peg_ratio}, {price_to_book_ratio}, {ev_to_revenue}\n")

print("Passed stocks exported to", output_file)