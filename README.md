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

Create a text file named ticker.txt in the same directory as the script. Add the list of stock tickers (one per line) that you want to analyze.

Open the script and replace `"API_KEY"` with your AlphaVantage API key.

Customize the `thresholds` dictionary with your desired threshold values for various financial ratios.

### Run the script:

```py
python stock_data_analysis.py
```

The script will fetch data for each stock ticker, compare it against the specified thresholds, and export the passed stocks to an output file named `output.txt`.

### License

This project is licensed under the __MIT License__ 

### Acknowledgements

This script uses the AlphaVantage API to fetch stock data. You can find more information about the AlphaVantage API [here](https://www.alphavantage.co/).

Special thanks to the Python community for providing helpful libraries and resources for data analysis and automation.

