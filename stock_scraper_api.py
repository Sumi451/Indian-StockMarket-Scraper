import yfinance as yf
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Stock Scraper API is Running! Try accessing /home-stocks or /stock?symbol=RELIANCE"

# List of popular stocks to show on home screen
POPULAR_STOCKS = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK"]

def get_stock_info(symbol):
    stock = yf.Ticker(symbol + ".NS")
    
    # Fetch latest price
    history = stock.history(period="1d")
    latest_price = history['Close'].iloc[-1]
    
    # Calculate daily change
    previous_close = history['Close'].iloc[-2] if len(history) > 1 else latest_price
    change = latest_price - previous_close
    change_percent = (change / previous_close) * 100 if previous_close else 0
    
    return {
        "symbol": symbol,
        "price": f"₹{latest_price:.2f}",
        "change": f"{change:+.2f} ({change_percent:+.2f}%)"
    }

@app.route('/home-stocks', methods=['GET'])
def home_stocks():
    stocks_data = []
    
    for symbol in POPULAR_STOCKS:
        try:
            stock_info = get_stock_info(symbol)
            stocks_data.append(stock_info)
        except Exception as e:
            stocks_data.append({
                "symbol": symbol,
                "error": str(e)
            })
    
    return jsonify(stocks_data)

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

        img_io = io.BytesIO()
        plt.savefig(img_io, format='png')
        plt.close()
        img_io.seek(0)

        base64_img = base64.b64encode(img_io.read()).decode('utf-8')
        graphs[period_name] = base64_img

    return graphs

@app.route('/stock', methods=['GET'])
def get_stock_data():
    symbol = request.args.get('symbol', '').upper()

    if not symbol:
        return jsonify({'error': 'Symbol parameter is required'}), 400

    try:
        stock_info = get_stock_info(symbol)
        graphs = fetch_and_plot_graphs(symbol)

        return jsonify({
            'symbol': symbol,
            'price': stock_info['price'],
            'change': stock_info['change'],
            'graphs': graphs
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
