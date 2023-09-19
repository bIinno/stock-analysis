# Stock Data Analysis Script

This Python script allows you to analyze stock data from AlphaVantage and filter stocks based on custom threshold values for various financial ratios. It reads a list of stock tickers from a text file, fetches data for each ticker, checks if the data meets the specified criteria, and exports the passed stocks to an output file.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python libraries: `requests`

You can install the required libraries using pip:

```bash
pip install requests
```

### AlphaVantage API Key

Before using the script, you need to obtain an [API key](https://www.alphavantage.co/support/#api-key) from AlphaVantage. You can sign up for a free API key on the AlphaVantage website here.

### Usage

Clone or download this repository to your local machine.

Open the script and replace `"API_KEY"` with your AlphaVantage API key.

Add your desired tickers into `ticker.txt`, each on a new line.

Customize the `thresholds` dictionary with your desired threshold values for various financial ratios.

### Run the script

```py
python main.py
```

The script will fetch data for each stock ticker within `ticker.txt`, compare it against the specified thresholds, and export the passed stocks to an output file named `output.txt`.

### Error checking

If it happens that you are getting ratio errors or lack of data, make sure you are accounting for the 5 per minute request limit (on free API keys).
If that isn't the issue, input the ticker causing the error into `get_ticker_data.py` and analyze the input, here you can see if you are receiving the correct data, or referencing said data correctly.

### License

This project is licensed under the __MIT License__

### Acknowledgements

This script uses the AlphaVantage API to fetch stock data. You can find more information about the AlphaVantage API [here](https://www.alphavantage.co/).

Special thanks to the Python community for providing helpful libraries and resources for data analysis and automation.
