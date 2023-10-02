# TEST FILE TO CHECK ACCURACY OF MAIN.PY

# Import necessary libraries
import requests

# Define constants and API key
ALPHA_VANTAGE_API_KEY = "P9DSUB7ZTSEV3HIT"
ALPHA_VANTAGE_API_URL = "https://www.alphavantage.co/query"
ALPHA_VANTAGE_API_FUNCTION = "OVERVIEW"
TICKER_SYMBOL = "STX"  # Replace with the desired ticker symbol

# Function to get the JSON data for a specific ticker
def get_ticker_data(ticker):
    # Define parameters
    params = {
        "function": ALPHA_VANTAGE_API_FUNCTION,
        "symbol": ticker,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    # Make the request to AlphaVantage
    response = requests.get(ALPHA_VANTAGE_API_URL, params=params)

    # If the status code is 200, return the JSON data
    if response.status_code == 200:
        return response.json()
    # Otherwise, print an error message
    else:
        print("Error fetching data from AlphaVantage")
        return None

# Fetch and print the JSON data for the specified ticker
ticker_data = get_ticker_data(TICKER_SYMBOL)

if ticker_data:
    # Print the entire JSON dataset
    print(ticker_data)
else:
    print(f"Data for {TICKER_SYMBOL} could not be retrieved.")
