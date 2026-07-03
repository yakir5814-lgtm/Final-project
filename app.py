from flask import Flask, Response
from prometheus_client import Counter, REGISTRY, generate_latest, CONTENT_TYPE_LATEST
import yfinance as yf

app = Flask(__name__)

CSS = """
<style>
    body { font-family: 'Segoe UI', sans-serif; background-color: #0077be; color: white; padding: 20px; }
    table { width: 80%; margin: 20px auto; background: white; color: black; border-radius: 10px; border-collapse: collapse; }
    th, td { padding: 15px; border-bottom: 1px solid #ddd; text-align: left; }
    .card { background: white; color: black; padding: 20px; border-radius: 10px; width: 500px; margin: auto; }
    .rec-box { background: #f9f9f9; padding: 10px; border-left: 5px solid #0077be; margin-top: 10px; }
</style>
"""

@app.route('/')
def index():
    tickers = ["AAPL", "GOOGL", "NVDA", "ANET", "ALAB", "CRDO", "KLIC", "SIMO"]
    rows = "".join([f"<tr><td><a href='/stock/{s}'>{s}</a></td><td>Check details</td></tr>" for s in tickers])
    return f"{CSS}<h1>📈 Eyal's Market</h1><nav><a href='/game' style='color:white'>🎮 Play Mario</a></nav><table>{rows}</table>"

@app.route('/stock/<symbol>')
def stock_details(symbol):
    ticker = yf.Ticker(symbol)
    info = ticker.info
    hist = ticker.history(period="1y")
    # שליפת המלצות אנליסטים מפורטות
    rec = info.get('recommendationKey', 'N/A').upper()
    return f"""
    {CSS}
    <div class='card'>
        <h1>{symbol} Details</h1>
        <div style='width: 400px; height: 200px;'><canvas id='chart'></canvas></div>
        <h3>Analyst Recommendations</h3>
        <div class='rec-box'><strong>Consensus:</strong> {rec}</div>
        <p>Market Cap: {info.get('marketCap', 'N/A')}</p>
    </div>
    <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
    <script>
        new Chart(document.getElementById('chart'), {{
            type: 'line',
            data: {{ labels: {hist.index.strftime('%m-%d').tolist()}, datasets: [{{ label: 'Price', data: {hist['Close'].tolist()} }}] }}
        }});
    </script>
    <br><a href='/' style='color:white'>Back</a>
    """

@app.route('/game')
def game():
    # הטמעת מנוע משחק מריו מבוסס HTML5/JS
    return f"""
    {CSS}
    <div style='text-align:center;'>
        <h1>Super Mario Bros</h1>
        <iframe src="https://supermarioplay.com/" width="800" height="600" style="border:5px solid white;"></iframe>
        <br><a href='/' style='color:white'>Back to Stocks</a>
    </div>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
