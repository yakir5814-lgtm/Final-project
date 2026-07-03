from flask import Flask, Response
import yfinance as yf

app = Flask(__name__)

GAME_HTML = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; background: #000; color: #fff; font-family: 'Poppins', sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; overflow: hidden; }
        #canvas { background: linear-gradient(#222, #000); border: 5px solid #38bdf8; border-radius: 15px; }
        .overlay { position: absolute; text-align: center; }
        button { padding: 20px 40px; font-size: 24px; background: #38bdf8; border: none; border-radius: 50px; color: white; cursor: pointer; transition: 0.3s; }
        button:hover { transform: scale(1.1); background: #818cf8; }
    </style>
</head>
<body>
    <audio id="bg-music" loop src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"></audio>
    <div id="ui" class="overlay">
        <h1>CYBER RACE 2026</h1>
        <button onclick="startGame()">START GAME</button>
    </div>
    <canvas id="canvas" width="800" height="600"></canvas>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        let gameActive = false;
        
        // 5 מכוניות עם צבעים שונים
        const cars = [
            {x: 100, y: 100, color: 'red'}, {x: 100, y: 200, color: 'blue'},
            {x: 100, y: 300, color: 'yellow'}, {x: 100, y: 400, color: 'green'},
            {x: 100, y: 500, color: 'purple'}
        ];

        function startGame() {
            document.getElementById('ui').style.display = 'none';
            document.getElementById('bg-music').play();
            gameActive = true;
            animate();
        }

        function animate() {
            if(!gameActive) return;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // ציור מסלול
            ctx.fillStyle = '#333';
            ctx.fillRect(0, 80, 800, 440);
            
            // תנועת מכוניות
            cars.forEach(car => {
                car.x += Math.random() * 5;
                ctx.fillStyle = car.color;
                ctx.fillRect(car.x, car.y, 60, 30);
                if(car.x > 740) car.x = 0;
            });

            requestAnimationFrame(animate);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return "<a href='/game'>Launch Game</a>"

@app.route('/game')
def game():
    return GAME_HTML

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
