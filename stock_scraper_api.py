import requests
from bs4 import BeautifulSoup
import yfinance as yf
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

# Function to fetch live price from NSE
def fetch_live_price(symbol):
    url = f"https://www.nseindia.com/get-quotes/equity?symbol={symbol}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/"
    }
    
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)  # Fetch cookies
    response = session.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from NSE. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    price_element = soup.find('span', {'id': 'quoteLtp'})

    if not price_element:
        raise Exception(f"Could not find price element for {symbol}. NSE page structure may have changed.")

    return price_element.text.strip()

# Function to fetch historical data and generate graphs
def fetch_and_plot_graphs(symbol):
    stock = yf.Ticker(symbol + ".NS")

    periods = {
        "1 Day": ("1d", "5m"),
        "1 Week": ("5d", "5m"),
        "1 Month": ("1mo", "1d"),
        "1 Year": ("1y", "1d")
    }

    graphs = {}

    for period_name, (period, interval) in periods.items():
        history = stock.history(period=period, interval=interval)

        if history.empty:
            raise Exception(f"Failed to fetch historical data for {symbol}")

        plt.figure(figsize=(10, 5))
        plt.plot(history.index, history['Close'], label=period_name, color='teal')
        plt.xlabel('Date-Time')
        plt.ylabel('Price (INR)')
        plt.title(f'{symbol} - {period_name} Price Chart')
        plt.legend()
        plt.grid(True)

        # Convert plot to base64 string
        img_io = io.BytesIO()
        plt.savefig(img_io, format='png')
        plt.close()
        img_io.seek(0)

        base64_img = base64.b64encode(img_io.read()).decode('utf-8')
        graphs[period_name] = base64_img

    return graphs

# Flask API Endpoint
@app.route('/stock', methods=['GET'])
def get_stock_data():
    symbol = request.args.get('symbol', '').upper()
    
    if not symbol:
        return jsonify({'error': 'Symbol parameter is required'}), 400

    try:
        live_price = fetch_live_price(symbol)
        graphs = fetch_and_plot_graphs(symbol)

        return jsonify({
            'symbol': symbol,
            'live_price': live_price,
            'graphs': graphs
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
