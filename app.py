from flask import Flask, render_template_string
import yfinance as yf
import plotly.graph_objects as go
import plotly.io as pio

app = Flask(__name__)

# CSS מותאם אישית בסגנון Dark Theme מקצועי
GLOBAL_STYLE = """
<style>
    body { background: #000; color: #fff; font-family: sans-serif; margin: 0; }
    .top-bar { background: #181818; padding: 10px; border-bottom: 1px solid #333; display: flex; justify-content: space-around; font-size: 0.8em; color: #ccc; }
    .main-container { display: grid; grid-template-columns: 300px 1fr; gap: 20px; padding: 20px; }
    .stock-card { border-bottom: 1px solid #222; padding: 10px 0; }
    .price { font-size: 1.2em; font-weight: bold; }
    .market-data { font-size: 0.8em; color: #888; }
    .positive { color: #26bd6c; } .negative { color: #ff3333; }
    .rec-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    .rec-table th, .rec-table td { border: 1px solid #333; padding: 8px; text-align: left; }
</style>
"""

def get_market_bar():
    indices = {"^IXIC": "Nasdaq", "^GSPC": "S&P 500", "BTC-USD": "BTC", "GC=F": "Gold"}
    bar = ""
    for sym, name in indices.items():
        t = yf.Ticker(sym)
        price = t.fast_info['last_price']
        bar += f"<span>{name}: {price:,.2f}</span>"
    return bar

@app.route('/')
def index():
    tickers = ["AAPL", "GOOGL", "NVDA", "ANET", "ALAB", "CRDO"]
    stocks_html = ""
    for s in tickers:
        t = yf.Ticker(s)
        curr = t.fast_info['last_price']
        pre = t.info.get('preMarketPrice', 'N/A')
        post = t.info.get('postMarketPrice', 'N/A')
        stocks_html += f"""<div class='stock-card'>
            <a href='/stock/{s}' style='color:white; text-decoration:none;'>{s}</a><br>
            <span class='price'>${curr:.2f}</span><br>
            <span class='market-data'>Pre: {pre} | Post: {post}</span>
        </div>"""

    return f"{GLOBAL_STYLE}<div class='top-bar'>{get_market_bar()}</div><div class='main-container'><div><h1>My Stocks</h1>{stocks_html}</div><div><h2>Market News</h2>[News placeholder]</div></div>"

@app.route('/stock/<ticker>')
def stock_detail(ticker):
    t = yf.Ticker(ticker)
    hist = t.history(period="3mo")
    
    # גרף קטן וקומפקטי
    fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
    fig.update_layout(template="plotly_dark", height=250, margin=dict(l=0,r=0,t=0,b=0))
    
    # המלצות אנליסטים
    rec_df = t.recommendations.tail(5) if t.recommendations is not None else None
    rec_html = f"<h3>Analyst Recommendations</h3>{rec_df.to_html(classes='rec-table')}" if rec_df is not None else "No data"
    
    return f"{GLOBAL_STYLE}<h1>{ticker}</h1>{pio.to_html(fig, full_html=False, div_id='graph')}{rec_html}<br><a href='/'>← Back</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
