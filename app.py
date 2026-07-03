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
    .clock { position: fixed; top: 15px; right: 20px; background: rgba(56, 189, 248, 0.2); padding: 10px 20px; border-radius: 20px; border: 1px solid #38bdf8; font-weight: bold; z-index: 1000; }
    .container { display: flex; gap: 20px; margin-top: 50px; }
    .glass-card { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; margin-bottom: 15px; border: 1px solid rgba(255, 255, 255, 0.1); }
    .stock-card { transition: transform 0.2s; cursor: pointer; text-decoration: none; color: white; display: block; }
    .stock-card:hover { transform: scale(1.03); background: rgba(56, 189, 248, 0.1); }
    h1 { text-align: center; color: #38bdf8; }
</style>
"""

@app.route('/')
def index():
    now = datetime.now().strftime("%H:%M:%S")
    tickers = ["AAPL", "GOOGL", "NVDA", "ANET"]
    stocks_html = ""
    for s in tickers:
        ticker = yf.Ticker(s)
        curr = ticker.history(period="1d")['Close'].iloc[-1]
        stocks_html += f"<a href='/stock/{s}' class='glass-card stock-card'>{s}: ${curr:.2f}</a>"

    return f"""{GLOBAL_STYLE}
    <div class='clock'>⏰ {now}</div>
    <h1>Yakir Stocks Market</h1>
    <div style='text-align:center;'>
        <a href='https://www.youtube.com/watch?v=5pidokakU4I' target='_blank'>🎵 מוזיקה</a> | 
        <a href='/game'>🎮 סופר מריו</a>
    </div>
    <div class='container'>
        <div style='flex:1;'><h2>מניות שלי</h2>{stocks_html}</div>
        <div style='flex:2;'><h2>חדשות שוק</h2></div>
    </div>"""

@app.route('/stock/<ticker_symbol>')
def stock_detail(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(period="6mo")
    
    # יצירת גרף פשוט
    fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
    fig.update_layout(template="plotly_dark", title=f"{ticker_symbol} Chart")
    graph_html = pio.to_html(fig, full_html=False)

    return f"{GLOBAL_STYLE}<h1>{ticker_symbol}</h1>{graph_html}<br><a href='/'>← חזור</a>"

@app.route('/game')
def game():
    return f"{GLOBAL_STYLE}<h1>סופר מריו</h1><a href='https://playclassic.games/games/super-mario-bros-online/play/' target='_blank'>לחץ כאן לשחק</a><br><a href='/'>← חזור</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
