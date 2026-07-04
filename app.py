from flask import Flask, render_template_string
import yfinance as yf
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

app = Flask(__name__)

# CSS מתקדם - Dark Blue/Teal Theme
GLOBAL_STYLE = """
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
    body { background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', sans-serif; }
    .navbar-custom { background: #1e293b; border-bottom: 2px solid #38bdf8; }
    .ticker-item { font-size: 0.85rem; margin-right: 15px; }
    .card { background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; border-radius: 12px; backdrop-filter: blur(10px); }
    .price-big { font-size: 2rem; font-weight: bold; }
    .positive { color: #22c55e; } .negative { color: #ef4444; }
    .btn-custom { background: #38bdf8; color: #000; font-weight: bold; }
</style>
"""

def get_market_data():
    indices = {"^IXIC": "Nasdaq", "^GSPC": "S&P 500", "BTC-USD": "BTC", "GC=F": "Gold"}
    res = []
    for sym, name in indices.items():
        t = yf.Ticker(sym)
        data = t.fast_info
        last = data['last_price']
        change = data['change_percent'] * 100
        color = "positive" if change >= 0 else "negative"
        res.append(f"<span class='ticker-item'>{name}: <b>{last:,.2f}</b> <span class='{color}'>{change:+.2f}%</span></span>")
    return "".join(res)

@app.route('/')
def index():
    tickers = ["AAPL", "GOOGL", "NVDA", "ANET", "ALAB", "CRDO"]
    stocks_html = ""
    for s in tickers:
        t = yf.Ticker(s)
        info = t.info
        curr = t.fast_info['last_price']
        pre = info.get('preMarketPrice', curr)
        post = info.get('postMarketChangePercent', 0)
        color = "positive" if post >= 0 else "negative"
        
        stocks_html += f"""
        <div class='col-md-4 mb-3'>
            <div class='card p-3'>
                <h5><a href='/stock/{s}' class='text-decoration-none text-white'>{s}</a></h5>
                <div class='price-big'>${curr:,.2f}</div>
                <div class='small'>Pre: ${pre:,.2f} | Post: <span class='{color}'>{post:+.2f}%</span></div>
            </div>
        </div>"""
    
    return f"{GLOBAL_STYLE}<nav class='navbar-custom p-2'>{get_market_data()}</nav><div class='container mt-4'><h1>Market Overview</h1><div class='row'>{stocks_html}</div></div>"

@app.route('/stock/<ticker>')
def stock_detail(ticker):
    t = yf.Ticker(ticker)
    hist = t.history(period="1y")
    
    # גרף מקצועי
    fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
    fig.update_layout(template="plotly_dark", plot_bgcolor='#0f172a', paper_bgcolor='#0f172a', height=500)
    
    # המלצות אנליסטים
    recs = t.recommendations
    rec_html = "No data"
    if recs is not None and not recs.empty:
        rec_html = recs.tail(10).to_html(classes='table table-dark table-striped')

    return f"""{GLOBAL_STYLE}
    <div class='container mt-5'>
        <a href='/' class='btn btn-custom mb-3'>← Back to Market</a>
        <h1>{ticker} Analysis</h1>
        {pio.to_html(fig, full_html=False)}
        <div class='mt-4'><h3>Analyst Recommendations</h3>{rec_html}</div>
    </div>"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
