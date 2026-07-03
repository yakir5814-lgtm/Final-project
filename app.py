from flask import Flask, Response
from prometheus_client import Counter, REGISTRY, generate_latest, CONTENT_TYPE_LATEST
import yfinance as yf

app = Flask(__name__)

# --- הגדרת המדדים ---
http_requests_total = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])

# כאן עליך לשים קישור ישיר לקובץ MP3 של 9PM (Till I Come)
# הלינק חייב להסתיים ב-.mp3 או להיות לינק להורדה ישירה
MUSIC_URL = "https://example.com/path-to-your-9pm-song.mp3" 

@app.route('/')
def index():
    tickers = ["AAPL", "GOOGL", "NVDA", "ANET", "ALAB", "CRDO", "KLIC", "SIMO"]
    stocks = []
    
    for symbol in tickers:
        try:
            ticker_obj = yf.Ticker(symbol)
            hist = ticker_obj.history(period="1d")
            price = hist['Close'].iloc[-1]
            prev_price = hist['Open'].iloc[0]
            change = ((price - prev_price) / prev_price) * 100
            stocks.append({
                "symbol": symbol, 
                "name": ticker_obj.info.get('shortName', symbol), 
                "price": round(price, 2), 
                "change": f"{change:+.2f}%"
            })
        except:
            stocks.append({"symbol": symbol, "name": "N/A", "price": 0.0, "change": "0%"})
    
    rows = "".join([
        f"<tr><td>{s['symbol']}</td><td>{s['name']}</td><td>${s['price']}</td>"
        f"<td style='color: {'green' if float(s['change'].replace('%','')) >= 0 else 'red'};'>"
        f"{s['change']}</td></tr>" 
        for s in stocks
    ])

    return f"""
    <html>
    <head>
        <script>
            // הפעלת מוזיקה בלחיצה הראשונה של המשתמש
            window.addEventListener('click', () => {{
                const audio = document.getElementById('bg-music');
                if(audio.paused) {{ audio.play(); }}
            }}, {{ once: true }});
        </script>
    </head>
    <body>
        <audio id="bg-music" loop>
            <source src="{MUSIC_URL}" type="audio/mpeg">
        </audio>

        <style>
            body {{font-family: Arial; background-color: #e0f7fa; padding: 20px;}} 
            nav {{margin-bottom: 20px;}} a {{margin-right: 15px; font-size: 20px;}}
            table {{width: 100%; border-collapse: collapse; background: white;}}
            th, td {{padding: 12px; border: 1px solid #ddd; text-align: left;}}
        </style>

        <nav><a href='/'>Dashboard</a> <a href='/game'>Play Mario</a></nav>
        <h1>📈 Eyal's Stock Market Dashboard</h1>
        <p>לחץ על כל מקום באתר כדי להתחיל את המוזיקה 🎶</p>
        <table><tr><th>Symbol</th><th>Name</th><th>Price</th><th>Change</th></tr>{rows}</table>
    </body>
    </html>
    """

@app.route('/game')
def game():
    return """
    <html>
    <body style="text-align: center; background: #222; color: white; font-family: Arial;">
        <h1>Super Mario Mini</h1>
        <div id="game" style="width:600px; height:400px; background: skyblue; margin: 20px auto; border: 5px solid white;">
            <p style="padding-top: 150px;">Mario Game Placeholder</p>
        </div>
        <a href='/' style="color: white; font-size: 20px;">Back to Stocks</a>
    </body>
    </html>
    """

@app.route('/metrics')
def metrics():
    return Response(generate_latest(REGISTRY), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
