import requests
import time

ALPHA_VANTAGE_API_KEY = "ME5NSWDBKBB2KK05"
ALPHA_VANTAGE_API_URL = "https://www.alphavantage.co/query"
ALPHA_VANTAGE_API_FUNCTION = "OVERVIEW"
ALPHA_VANTAGE_API_TICKER_FILE = "crazy/ticker.txt"

thresholds = {
    "PE Ratio": 5,
    "PEG Ratio": 2,
    "PriceToBookRatio": 0.7,
    "EV to Revenue": 2,
}

def get_stock_data(ticker):
    params = {
        "function": ALPHA_VANTAGE_API_FUNCTION,
        "symbol": ticker,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    response = requests.get(ALPHA_VANTAGE_API_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data from AlphaVantage")
        return None

tickers = []

try:
    with open(ALPHA_VANTAGE_API_TICKER_FILE, "r") as ticker_file:
        tickers = ticker_file.read().splitlines()
except FileNotFoundError:
    print("Ticker file not found!")
except PermissionError:
    print("Permission denied to read ticker file!")
except Exception as e:
    print(f"Error reading ticker file: {str(e)}")

if not tickers:
    print("No tickers found. Check the ticker file contents.")

passed_stocks = []

for i, ticker in enumerate(tickers, start=1):
    try:
        dataset = get_stock_data(ticker)
    except:
        print(f"Error fetching data for {ticker}")
    else:
        print(f"Fetched data for {ticker}")

    if dataset:
        symbol = dataset.get('Symbol', 'N/A')
        sector = dataset.get('Sector', 'N/A')
        pe_ratio = float(dataset.get('PERatio', '0'))
        peg_ratio = float(dataset.get('PEGRatio', '0'))
        price_to_book_ratio = float(dataset.get('PriceToBookRatio', '0'))
        ev_to_revenue = float(dataset.get('EVToRevenue', '0'))

        if (
            pe_ratio >= thresholds.get('PE Ratio', float('-inf')) and
            peg_ratio >= thresholds.get('PEG Ratio', float('-inf')) and
            price_to_book_ratio >= thresholds.get('PriceToBookRatio', float('-inf')) and
            ev_to_revenue >= thresholds.get('EV to Revenue', float('-inf'))
        ):
            print(f"{ticker} meets the threshold criteria.")
            passed_stocks.append((symbol, sector, pe_ratio, peg_ratio, price_to_book_ratio, ev_to_revenue))
        else:
            print(f"{ticker} does not meet the threshold criteria.")
    
    if i % 5 == 0 and i < len(tickers):
        print(f"Waiting for 60 seconds to account for API rate limit...")
        time.sleep(60)

output_file = "output.txt"
with open(output_file, "w") as f:
    f.write("Symbol, Sector, PE Ratio, PEG Ratio, Price-to-Book Ratio, EV to Revenue\n")
    for stock in passed_stocks:
        symbol, sector, pe_ratio, peg_ratio, price_to_book_ratio, ev_to_revenue = stock
        f.write(f"{symbol}, {sector}, {pe_ratio}, {peg_ratio}, {price_to_book_ratio}, {ev_to_revenue}\n")

print("Passed stocks exported to", output_file)
