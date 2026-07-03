from flask import Flask, Response, render_template_string
from prometheus_client import Counter, REGISTRY, generate_latest, CONTENT_TYPE_LATEST
import yfinance as yf

app = Flask(__name__)

MUSIC_URL = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" 

@app.route('/')
def index():
    tickers = ["AAPL", "GOOGL", "NVDA", "ANET", "ALAB", "CRDO", "KLIC", "SIMO"]
    rows = ""
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")
            price = hist['Close'].iloc[-1]
            rows += f"<tr><td><a href='/stock/{symbol}'>{symbol}</a></td><td>{ticker.info.get('shortName', symbol)}</td><td>${round(price, 2)}</td></tr>"
        except:
            rows += f"<tr><td>{symbol}</td><td>N/A</td><td>0.0</td></tr>"
    
    return f"""
    <body onclick="document.getElementById('bg-music').play()">
        <audio id="bg-music" loop src="{MUSIC_URL}"></audio>
        <nav><a href='/'>Dashboard</a> | <a href='/game'>Play Mario</a></nav>
        <h1>📈 Eyal's Stock Market</h1>
        <table>{rows}</table>
    </body>"""

@app.route('/stock/<symbol>')
def stock_details(symbol):
    ticker = yf.Ticker(symbol)
    info = ticker.info
    hist = ticker.history(period="1y")
    # המרת הנתונים לגרף
    dates = hist.index.strftime('%Y-%m-%d').tolist()
    prices = hist['Close'].tolist()
    
    return f"""
    <h1>{symbol} Details</h1>
    <p>Market Cap: {info.get('marketCap', 'N/A')}</p>
    <p>Recommendation: {info.get('recommendationKey', 'N/A')}</p>
    <canvas id="myChart" width="400" height="200"></canvas>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        new Chart(document.getElementById('myChart'), {{
            type: 'line',
            data: {{ labels: {dates}, datasets: [{{ label: 'Price', data: {prices} }}] }}
        }});
    </script>
    <a href='/'>Back</a>
    """

@app.route('/game')
def game():
    return """
    <body style="background:#222; color:white; text-align:center;">
        <h1>Mario Controller</h1>
        <div id="mario" style="width:50px; height:50px; background:red; position:relative; left:0;"></div>
        <script>
            let pos = 0;
            window.addEventListener('keydown', (e) => {
                if(e.key === 'ArrowRight') pos += 20;
                document.getElementById('mario').style.left = pos + 'px';
            });
        </script>
        <p>Use Right Arrow to move!</p>
        <a href='/'>Back</a>
    </body>"""

@app.route('/metrics')
def metrics():
    return Response(generate_latest(REGISTRY), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
