from flask import Flask
import yfinance as yf

app = Flask(__name__)

GLOBAL_STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&display=swap');
    body { background: #0f172a; color: #f8fafc; font-family: 'Poppins', sans-serif; margin: 0; padding: 20px; }
    .container { display: flex; gap: 20px; }
    .side { flex: 1; }
    .glass-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 20px; margin-bottom: 10px; }
    .positive { color: #4ade80; font-weight: bold; }
    .negative { color: #f87171; font-weight: bold; }
    a { color: #38bdf8; text-decoration: none; }
    h1 { text-align: center; color: #38bdf8; }
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
            curr = hist['Close'].iloc[-1]
            change = ((curr - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100
            color = "positive" if change >= 0 else "negative"
            rows += f"<div class='glass-card'><a href='/stock/{s}'>{s}</a>: ${curr:.2f} <span class='{color}'>({change:+.2f}%)</span></div>"
        except:
            rows += f"<div class='glass-card'>{s}: Error</div>"

    return f"""{GLOBAL_STYLE}
    <h1>Yakir Stocks Market</h1>
    <div style='text-align:center; margin-bottom:20px;'>
        <audio controls autoplay loop><source src='https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3'></audio>
        <br><a href='/game'>🎮 LAUNCH SUPER MARIO</a>
    </div>
    <div class='container'>
        <div class='side'><h2>My Stocks</h2>{rows}</div>
        <div class='side'><h2>Market News</h2>
            <div class='glass-card'>Loading latest Nasdaq updates...</div>
            <div class='glass-card'>Tech sector showing volatility due to AI demand.</div>
        </div>
    </div>"""

@app.route('/game')
def game():
    # פתרון iframe יציב יותר
    return f"""{GLOBAL_STYLE}
    <div style='text-align:center;'>
        <h1>Super Mario Arcade</h1>
        <iframe src='https://www.google.com/logos/2010/pacman10-i.html' width='800' height='600'></iframe>
        <br><a href='/'>Back Home</a>
    </div>"""

# (שמור את stock_details כפי שהיה)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
