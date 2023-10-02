# Import necessary libraries
import logging
import requests
import time
import csv
import os

# Define constants and API key
ALPHA_VANTAGE_API_KEY = "B2IL2274887GVP8O"
ALPHA_VANTAGE_API_URL = "https://www.alphavantage.co/query"
ALPHA_VANTAGE_API_FUNCTION = "OVERVIEW"
ALPHA_VANTAGE_API_TICKER_FILE = "ticker.txt"

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

# Define custom thresholds for ratios
thresholds = {
    "PE Ratio": 15,  # Customize your threshold value here
    "PEG Ratio": 1,  # Customize your threshold value here
    "PriceToBookRatio": 1,  # Customize your threshold value here
    "EV to Revenue": 1,  # Customize your threshold value here for EV to Revenue
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

# Initialize the output file name
output_file = "output.csv"  # Change the file extension to .csv

# Create a set to store tickers from the existing CSV file
existing_tickers = set()

# Check if the output CSV file already exists
if os.path.isfile(output_file):
    with open(output_file, "r") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            existing_tickers.add(row["Symbol"])

# Remove tickers from ticker.txt if they are already in the CSV
tickers = [ticker for ticker in tickers if ticker not in existing_tickers]

def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None
    
# Create a list to store passed stocks
passed_stocks = []

# Open the output file in append mode if it exists, or create a new file if it doesn't
with open(output_file, "a", newline='') as csvfile:
    # Create a CSV writer
    csv_writer = csv.writer(csvfile)
    
    # If the file is newly created, write the header row
    if not os.path.isfile(output_file):
        csv_writer.writerow(["Symbol", "Sector", "PE Ratio", "PEG Ratio", "Price-to-Book Ratio", "EV to Revenue"])

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
            pe_ratio = safe_float(dataset.get('PERatio', 'N/A'))
            peg_ratio = safe_float(dataset.get('PEGRatio', 'N/A'))
            price_to_book_ratio = safe_float(dataset.get('PriceToBookRatio', 'N/A'))
            ev_to_revenue = safe_float(dataset.get('EVToRevenue', 'N/A'))

            # Check if any ratio field failed to convert to float
            if None in [pe_ratio, peg_ratio, price_to_book_ratio, ev_to_revenue]:
                print(f"Error converting ratio(s) to float for {ticker}. Skipping...")
                continue

            # Initialize the missing_ratio flag to False
            missing_ratio = False

            try:
                # Check if each ratio is available and within the thresholds
                if pe_ratio is not None and pe_ratio < thresholds.get('PE Ratio', float('-inf')):
                    missing_ratio = True

                if peg_ratio is not None and peg_ratio < thresholds.get('PEG Ratio', float('-inf')):
                    missing_ratio = True

                if price_to_book_ratio is not None and price_to_book_ratio < thresholds.get('PriceToBookRatio', float('-inf')):
                    missing_ratio = True

                if ev_to_revenue is not None and ev_to_revenue < thresholds.get('EV to Revenue', float('-inf')):
                    missing_ratio = True

                # Check if at least one ratio is available
                if not missing_ratio:
                    print(f"{ticker} meets the threshold criteria.")
                    passed_stocks.append((symbol, sector, pe_ratio, peg_ratio, price_to_book_ratio, ev_to_revenue))
                    
                    # Write the data row to the CSV file
                    csv_writer.writerow([symbol, sector, pe_ratio, peg_ratio, price_to_book_ratio, ev_to_revenue])
                else:
                    print(f"{ticker} does not meet the threshold criteria due to missing or below-threshold ratio(s).")

            except ValueError as ve:
                logging.error(f"Error converting ratio(s) to float for {ticker}: {str(ve)}")
                print(f"Error converting ratio(s) to float for {ticker}. Skipping...")

        if i % 5 == 0 and i < len(tickers):
            print(f"Waiting for 60 seconds to account for API rate limit...")
            time.sleep(60)

# Export passed stocks to a CSV file
with open(output_file, "a", newline='') as csvfile:
    # Create a CSV writer
    csv_writer = csv.writer(csvfile)
    
    # Write the data rows
    for stock in passed_stocks:
        symbol, sector, pe_ratio, peg_ratio, price_to_book_ratio, ev_to_revenue = stock
        csv_writer.writerow([symbol, sector, pe_ratio, peg_ratio, price_to_book_ratio, ev_to_revenue])

print("Passed stocks exported to", output_file)