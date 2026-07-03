from flask import Flask, Response
from prometheus_client import Counter, Gauge, Summary, Histogram, Info, Enum, REGISTRY, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily
import time
import random
import threading
import yfinance as yf

app = Flask(__name__)

# --- הגדרת המדדים של Prometheus ---
http_requests_total = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
cpu_usage = Gauge('cpu_usage_percent', 'Simulated CPU usage')
cpu_usage.set_function(lambda: random.uniform(10.0, 90.0))

@app.route('/')
def index():
    # רשימת המניות למעקב
    tickers = ["AAPL", "GOOGL", "NVDA"]
    stocks = []
    
    for symbol in tickers:
        try:
            ticker_obj = yf.Ticker(symbol)
            # משיכת נתוני יום מסחר אחרון
            hist = ticker_obj.history(period="1d")
            price = hist['Close'].iloc[-1]
            prev_price = hist['Open'].iloc[0]
            change = ((price - prev_price) / prev_price) * 100
            
            stocks.append({
                "symbol": symbol, 
                "name": ticker_obj.info.get('shortName', symbol), 
                "price": round(price, 2), 
                "change": f"{change:+.2f}%"
            })
        except Exception as e:
            stocks.append({"symbol": symbol, "name": "Error", "price": 0.0, "change": "0%"})
    
    # יצירת שורות הטבלה עם צבעים דינמיים
    rows = "".join([
        f"<tr><td>{s['symbol']}</td><td>{s['name']}</td><td>${s['price']}</td>"
        f"<td style='color: {'green' if float(s['change'].replace('%','')) >= 0 else 'red'};'>"
        f"{s['change']}</td></tr>" 
        for s in stocks
    ])

    # החזרת דף ה-HTML עם רקע תכלת
    return (
        "<style>body {font-family: Arial; background-color: #e0f7fa; padding: 20px;} " # רקע תכלת
        "table {width: 100%; border-collapse: collapse; background: white;} "
        "th, td {padding: 12px; border: 1px solid #ddd; text-align: left;}</style>"
        "<h1>📈 Eyal's Stock Market Dashboard</h1>"
        "<table><tr><th>Symbol</th><th>Name</th><th>Price</th><th>Change</th></tr>"
        f"{rows}</table>"
        "<p>נתונים אלו מתעדכנים בזמן אמת מ-Yahoo Finance!</p>"
    )

@app.route('/metrics')
def metrics():
    return Response(generate_latest(REGISTRY), mimetype=CONTENT_TYPE_LATEST)

# --- פונקציית סימולציה ברקע ---
def simulate_traffic():
    while True:
        http_requests_total.labels(method='GET', endpoint='/').inc()
        time.sleep(2)

if __name__ == '__main__':
    traffic_thread = threading.Thread(target=simulate_traffic, daemon=True)
    traffic_thread.start()
    app.run(host='0.0.0.0', port=5001)
