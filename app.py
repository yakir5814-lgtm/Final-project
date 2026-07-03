from flask import Flask, Response
import yfinance as yf

app = Flask(__name__)

# עיצוב מודרני (Glassmorphism)
GLOBAL_STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&display=swap');
    body { background: linear-gradient(135deg, #0f172a, #1e293b); color: #f8fafc; font-family: 'Poppins', sans-serif; margin: 0; padding: 40px; }
    .glass-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 20px; margin-bottom: 10px; transition: 0.3s; }
    .glass-card:hover { background: rgba(255, 255, 255, 0.1); transform: scale(1.01); }
    table { width: 100%; border-collapse: separate; border-spacing: 0 10px; }
    .stock-row { display: flex; justify-content: space-between; align-items: center; width: 100%; }
    .positive { color: #4ade80; font-weight: bold; }
    .negative { color: #f87171; font-weight: bold; }
    a { color: #38bdf8; text-decoration: none; font-weight: 600; }
    h1 { text-align: center; font-size: 3rem; background: linear-gradient(to right, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .music-player { text-align: center; margin-bottom: 30px; }
</style>
"""

@app.route('/')
def index():
    tickers = ["AAPL", "GOOGL", "NVDA", "ANET", "ALAB", "CRDO", "KLIC", "SIMO"]
    rows = ""
    for s in tickers:
        ticker = yf.Ticker(s)
        try:
            hist = ticker.history(period="2d")
            curr_price = hist['Close'].iloc[-1]
            prev_price = hist['Close'].iloc[-2]
            change_pct = ((curr_price - prev_price) / prev_price) * 100
            color_class = "positive" if change_pct >= 0 else "negative"
            
            rows += f"""
            <tr><td>
                <div class='glass-card stock-row'>
                    <a href='/stock/{s}'>{s}</a>
                    <span>${curr_price:.2f} <span class='{color_class}'>({change_pct:+.2f}%)</span></span>
                </div>
            </td></tr>"""
        except:
            rows += f"<tr><td><div class='glass-card'>Error loading {s}</div></td></tr>"
            
    return f"""{GLOBAL_STYLE}
    <h1>Yakir Stocks Market</h1>
    <div class='music-player'>
        <p style='color:#94a3b8;'>Now Playing: Bob Marley - Three Little Birds</p>
        <audio controls autoplay loop>
            <source src='https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3' type='audio/mpeg'>
        </audio>
        <br><br>
        <a href='/game' style='font-size: 1.2rem; border: 1px solid #38bdf8; padding: 10px 20px; border-radius: 10px;'>🎮 LAUNCH SUPER MARIO ARCADE</a>
    </div>
    <table>{rows}</table>"""

@app.route('/game')
def game():
    return f"""{GLOBAL_STYLE}
    <h1>Super Mario Arcade</h1>
    <div style='text-align:center;'>
        <iframe src='https://supermarioplay.com/' width='900' height='600' style='border-radius:20px; border:none;'></iframe>
        <br><br><a href='/'>← Back to Mission Control</a>
    </div>"""

@app.route('/stock/<symbol>')
def stock_details(symbol):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1y")
    info = ticker.info
    return f"""
    {GLOBAL_STYLE}
    <div class='glass-card' style='max-width: 600px; margin: auto;'>
        <h1>{symbol} Details</h1>
        <div style='background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px;'>
            <canvas id='chart'></canvas>
        </div>
        <p><strong>Market Cap:</strong> {info.get('marketCap', 'N/A')}</p>
        <a href='/'>← Back to Market</a>
    </div>
    <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
    <script>
        new Chart(document.getElementById('chart'), {{
            type: 'line',
            data: {{ labels: {hist.index.strftime('%b').tolist()}, datasets: [{{ data: {hist['Close'].tolist()}, borderColor: '#38bdf8', fill: true }}] }}
        }});
    </script>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
