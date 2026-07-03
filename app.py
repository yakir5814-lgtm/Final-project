from flask import Flask, render_template_string
from datetime import datetime
import yfinance as yf
import feedparser
import plotly.graph_objects as go
import plotly.io as pio

app = Flask(__name__)

GLOBAL_STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&display=swap');
    body { background: #0f172a; color: #f8fafc; font-family: 'Poppins', sans-serif; margin: 20px; }
    .clock { position: fixed; top: 15px; right: 20px; background: rgba(56, 189, 248, 0.2); padding: 10px 20px; border-radius: 20px; border: 1px solid #38bdf8; font-weight: bold; }
    .glass-card { background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 15px; margin-bottom: 10px; border: 1px solid rgba(255, 255, 255, 0.1); }
    .positive { color: #4ade80; font-weight: bold; }
    .negative { color: #f87171; font-weight: bold; }
    .stock-link { text-decoration: none; color: #38bdf8; display: block; }
</style>
<script>
    function updateClock() { document.getElementById('clock').innerText = new Date().toLocaleTimeString(); }
    setInterval(updateClock, 1000);
</script>
"""

@app.route('/')
def index():
    tickers = ["AAPL", "GOOGL", "NVDA", "ANET", "ALAB", "CRDO"]
    stocks_html = ""
    for s in tickers:
        ticker = yf.Ticker(s)
        hist = ticker.history(period="2d")
        curr = hist['Close'].iloc[-1]
        change = ((curr - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100
        color = "positive" if change >= 0 else "negative"
        stocks_html += f"<div class='glass-card'><a href='/stock/{s}' class='stock-link'>{s}: ${curr:.2f} <span class='{color}'>({change:+.2f}%)</span></a></div>"

    feed = feedparser.parse("https://finance.yahoo.com/rss/headline?s=AAPL,NVDA,GOOGL")
    news_html = "".join([f"<div class='glass-card'><b>{item.title}</b><br><a href='{item.link}' target='_blank'>Read more</a></div>" for item in feed.entries[:3]])

    return f"""{GLOBAL_STYLE}
    <div id='clock' class='clock'>{datetime.now().strftime("%H:%M:%S")}</div>
    <h1>Yakir Stocks Market</h1>
    <div style='text-align:center;'>
        <audio controls><source src='https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3' type='audio/mpeg'></audio><br>
        <a href='https://playclassic.games/games/super-mario-bros-online/play/' target='_blank'>🎮 LAUNCH SUPER MARIO</a>
    </div>
    <div style='display:flex; gap:20px; margin-top:20px;'>
        <div style='flex:1;'><h2>My Stocks</h2>{stocks_html}</div>
        <div style='flex:2;'><h2>Market News</h2>{news_html}</div>
    </div>"""

@app.route('/stock/<ticker>')
def stock_detail(ticker):
    t = yf.Ticker(ticker)
    hist = t.history(period="6mo")
    fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
    fig.update_layout(template="plotly_dark", title=f"{ticker} Analysis")
    return f"{GLOBAL_STYLE}<h1>{ticker} Details</h1>{pio.to_html(fig, full_html=False)}<br><a href='/'>← Back</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
