from flask import Flask
import yfinance as yf
import feedparser

app = Flask(__name__)

GLOBAL_STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&display=swap');
    body { background: #0f172a; color: #f8fafc; font-family: 'Poppins', sans-serif; margin: 20px; }
    .container { display: flex; gap: 20px; }
    .stocks-col { flex: 1; max-width: 25%; }
    .news-col { flex: 3; }
    .glass-card { background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 15px; margin-bottom: 10px; border: 1px solid rgba(255, 255, 255, 0.1); }
    .positive { color: #4ade80; font-weight: bold; }
    .negative { color: #f87171; font-weight: bold; }
    h1 { text-align: center; color: #38bdf8; margin-bottom: 20px; }
    a { color: #38bdf8; text-decoration: none; }
</style>
"""

@app.route('/')
def index():
    feed = feedparser.parse("https://finance.yahoo.com/rss/headline?s=AAPL,NVDA,GOOGL,ANET,ALAB")
    news_html = "".join([f"<div class='glass-card'><b>{item.title}</b><br><a href='{item.link}' target='_blank'>קרא עוד...</a></div>" for item in feed.entries[:6]])
    
    tickers = ["AAPL", "GOOGL", "NVDA", "ANET", "ALAB", "CRDO", "KLIC", "SIMO"]
    stocks_html = ""
    for s in tickers:
        ticker = yf.Ticker(s)
        try:
            hist = ticker.history(period="2d")
            curr = hist['Close'].iloc[-1]
            change = ((curr - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100
            stocks_html += f"<div class='glass-card'>{s}: ${curr:.2f} <span class='{'positive' if change>=0 else 'negative'}'>({change:+.2f}%)</span></div>"
        except: stocks_html += f"<div class='glass-card'>{s}: N/A</div>"

    return f"""{GLOBAL_STYLE}
    <h1>Yakir Stocks Market</h1>
    <div style='text-align:center;'>
        <iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/114995779&color=%2338bdf8&auto_play=true"></iframe>
        <br><br><a href='/game' style='font-size: 1.5rem;'>🎮 LAUNCH SUPER MARIO ARCADE</a>
    </div>
    <div class='container'>
        <div class='stocks-col'><h2>My Stocks</h2>{stocks_html}</div>
        <div class='news-col'><h2>Market News</h2>{news_html}</div>
    </div>"""

@app.route('/game')
def game():
    return f"""{GLOBAL_STYLE}
    <h1>Super Mario Arcade</h1>
    <div style='text-align:center;'>
        <iframe src='https://playclassic.games/games/super-mario-bros-online/play/' width='900' height='650'></iframe>
        <br><br><a href='/'>← חזור למסחר</a>
    </div>"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
