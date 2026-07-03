from flask import Flask, Response
from prometheus_client import REGISTRY, generate_latest, CONTENT_TYPE_LATEST
import yfinance as yf

app = Flask(__name__)

GLOBAL_STYLE = """
<style>
    body { background: #0f172a; color: white; font-family: 'Poppins', sans-serif; margin: 0; display: flex; flex-direction: column; align-items: center; }
    canvas { border: 4px solid #38bdf8; border-radius: 10px; background: #000; box-shadow: 0 0 20px rgba(56, 189, 248, 0.5); }
    .ui { margin: 20px; text-align: center; }
</style>
"""

@app.route('/')
def index():
    return f"{GLOBAL_STYLE}<h1>Eyal's Cyber Command</h1><div class='ui'><a href='/game'>🚀 ENTER BATTLEFIELD</a></div>"

@app.route('/game')
def game():
    return f"""
    {GLOBAL_STYLE}
    <div class='ui'>
        <h1>Soldiers vs Monsters</h1>
        <p>Use Arrow Keys to move your soldier. Avoid the green monsters!</p>
    </div>
    <div id='game-container'></div>
    <script src='https://cdn.jsdelivr.net/npm/phaser@3.55.2/dist/phaser.min.js'></script>
    <script>
        const config = {{
            type: Phaser.AUTO, width: 800, height: 400, parent: 'game-container',
            physics: {{ default: 'arcade', arcade: {{ gravity: {{ y: 0 }} }} }},
            scene: {{
                preload: function() {{ this.load.image('soldier', 'https://labs.phaser.io/assets/sprites/phaser-dude.png'); }},
                create: function() {{
                    this.player = this.physics.add.sprite(400, 300, 'soldier');
                    this.cursors = this.input.keyboard.createCursorKeys();
                }},
                update: function() {{
                    if (this.cursors.left.isDown) this.player.setVelocityX(-200);
                    else if (this.cursors.right.isDown) this.player.setVelocityX(200);
                    else this.player.setVelocityX(0);
                    if (this.cursors.up.isDown) this.player.setVelocityY(-200);
                    else if (this.cursors.down.isDown) this.player.setVelocityY(200);
                    else this.player.setVelocityY(0);
                }}
            }}
        }};
        const game = new Phaser.Game(config);
    </script>
    <br><a href='/'>Exit Battlefield</a>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
