from flask import Flask, Response
from prometheus_client import REGISTRY, generate_latest, CONTENT_TYPE_LATEST
import yfinance as yf

app = Flask(__name__)

# עיצוב מודרני מרהיב
GLOBAL_STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&display=swap');
    body { background: linear-gradient(135deg, #0f172a, #1e293b); color: #f8fafc; font-family: 'Poppins', sans-serif; margin: 0; padding: 40px; }
    .glass-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 30px; box-shadow: 0 8px 32px 0 rgba(0,0,0,0.37); }
    table { width: 100%; border-collapse: separate; border-spacing: 0 10px; }
    td { padding: 20px; background: rgba(255,255,255,0.03); cursor: pointer; transition: 0.3s; }
    td:hover { background: rgba(59, 130, 246, 0.2); transform: scale(1.02); }
    a { color: #38bdf8; text-decoration: none; font-weight: 600; }
    h1 { text-align: center; font-size: 3rem; background: linear-gradient(to right, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
</style>
"""

@app.route('/')
def index():
    tickers = ["AAPL", "GOOGL", "NVDA", "ANET", "ALAB", "CRDO", "KLIC", "SIMO"]
    rows = "".join([f"<tr><td class='glass-card'><a href='/stock/{s}'>{s} - Market Data</a></td></tr>" for s in tickers])
    return f"{GLOBAL_STYLE}<h1>Eyal's Cyber Dashboard</h1><div style='text-align:center'><a href='/game'>🎮 LAUNCH MARIO ARCADE</a></div><table>{rows}</table>"

@app.route('/stock/<symbol>')
def stock_details(symbol):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1y")
    info = ticker.info
    return f"""
    {GLOBAL_STYLE}
    <div class='glass-card' style='max-width: 600px; margin: auto;'>
        <h1>{symbol}</h1>
        <div style='background: white; padding: 10px; border-radius: 15px;'>
            <canvas id='chart'></canvas>
        </div>
        <div style='margin-top:20px'>
            <p><strong>Market Cap:</strong> {info.get('marketCap', 'N/A')}</p>
            <p><strong>Recommendation:</strong> {info.get('recommendationKey', 'N/A').upper()}</p>
        </div>
        <a href='/'>← Back to Mission Control</a>
    </div>
    <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
    <script>
        new Chart(document.getElementById('chart'), {{
            type: 'line',
            data: {{ labels: {hist.index.strftime('%b').tolist()}, datasets: [{{ data: {hist['Close'].tolist()}, borderColor: '#38bdf8', fill: true }}] }}
        }});
    </script>
    """

@app.route('/game')
def game():
    return f"{GLOBAL_STYLE}<div style='text-align:center;'><h1>Super Mario Arcade</h1><iframe src='https://supermarioplay.com/' width='900' height='600' style='border-radius:20px; border:none;'></iframe><br><a href='/'>Exit Game</a></div>"

@app.route('/metrics')
def metrics():
    return Response(generate_latest(REGISTRY), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
