from flask import Flask, render_template_string
from datetime import datetime
import yfinance as yf
import plotly.graph_objects as go
import plotly.io as pio

app = Flask(__name__)

GLOBAL_STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&display=swap');
    body { background: #0f172a; color: #f8fafc; font-family: 'Poppins', sans-serif; margin: 20px; }
    .ticker-bar { background: #1e293b; padding: 10px; border-radius: 10px; margin-bottom: 20px; display: flex; justify-content: space-around; font-size: 0.9em; border: 1px solid #334155; }
    .glass-card { background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 15px; margin-bottom: 10px; border: 1px solid rgba(255, 255, 255, 0.1); }
    .positive { color: #4ade80; } .negative { color: #f87171; }
    .small-graph { height: 300px; }
</style>
"""

def get_market_data():
    # מדדים: Nasdaq, S&P500, Gold, Bitcoin, Silver
    tickers = {"^IXIC": "Nasdaq", "^GSPC": "S&P 500", "GC=F": "Gold", "BTC-USD": "BTC", "SI=F": "Silver"}
    data = []
    for sym, name in tickers.items():
        t = yf.Ticker(sym)
        price = t.fast_info['last_price']
        data.append(f"{name}: ${price:,.2f}")
    return " | ".join(data)

@app.route('/')
def index():
    tickers = ["AAPL", "GOOGL", "NVDA", "ANET", "ALAB", "CRDO"]
    stocks_html = ""
    for s in tickers:
        t = yf.Ticker(s)
        # Pre/Post market logic
        pre = t.info.get('preMarketPrice', 'N/A')
        post = t.info.get('postMarketPrice', 'N/A')
        curr = t.fast_info['last_price']
        
        stocks_html += f"""<div class='glass-card'>
            <a href='/stock/{s}' style='color:#38bdf8; text-decoration:none;'>{s}: ${curr:.2f}</a><br>
            <small>Pre: {pre} | Post: {post}</small>
        </div>"""

    return f"{GLOBAL_STYLE}<div class='ticker-bar'>{get_market_data()}</div><h1>Yakir Stocks Market</h1><div style='flex:1;'>{stocks_html}</div>"

@app.route('/stock/<ticker>')
def stock_detail(ticker):
    t = yf.Ticker(ticker)
    hist = t.history(period="6mo")
    
    # המלצות אנליסטים
    recs = t.recommendations
    rec_html = "<h4>Analyst Recommendations</h4><ul>"
    if recs is not None and not recs.empty:
        # סיכום המלצות אחרונות
        last_rec = recs.tail(5)
        rec_html += f"<li>{last_rec.to_html(classes='table table-dark')}</li>"
    rec_html += "</ul>"

    fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
    fig.update_layout(template="plotly_dark", height=300, margin=dict(l=0, r=0, t=30, b=0))
    
    return f"{GLOBAL_STYLE}<h1>{ticker} Details</h1>{pio.to_html(fig, full_html=False, div_id='small-graph')}{rec_html}<br><a href='/'>← Back</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
