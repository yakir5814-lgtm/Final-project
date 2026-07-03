from flask import Flask

app = Flask(__name__)

FULL_GAME_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>School Journey: The Game</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
    <style>
        body { margin: 0; background: #000; font-family: 'Arial'; }
        #overlay { position: absolute; top: 20px; left: 20px; color: white; pointer-events: none; }
    </style>
</head>
<body>
    <div id="overlay"><h1>School Journey: GTA Style</h1><p>Arrows to walk | Space to Interact</p></div>
    <audio id="bg-music" src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" loop></audio>

    <script>
        // אתחול סצינה
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x87CEEB);
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // תאורה ריאליסטית
        scene.add(new THREE.AmbientLight(0xffffff, 0.7));
        const dirLight = new THREE.DirectionalLight(0xffffff, 1);
        dirLight.position.set(10, 20, 10);
        scene.add(dirLight);

        // יצירת רצפת עולם
        const ground = new THREE.Mesh(new THREE.PlaneGeometry(500, 500), new THREE.MeshPhongMaterial({ color: 0x228B22 }));
        ground.rotation.x = -Math.PI / 2;
        scene.add(ground);

        // יצירת "מכולת" (בניין)
        const shop = new THREE.Mesh(new THREE.BoxGeometry(10, 5, 10), new THREE.MeshPhongMaterial({ color: 0x8B4513 }));
        shop.position.set(20, 2.5, 0);
        scene.add(shop);

        // דמות השחקן (הילד)
        const player = new THREE.Mesh(new THREE.BoxGeometry(0.5, 1.7, 0.5), new THREE.MeshPhongMaterial({ color: 0xff0000 }));
        player.position.set(0, 0.85, 0);
        scene.add(player);

        // מצלמה (גוף שלישי)
        camera.position.set(0, 3, 7);
        player.add(camera);

        // תנועה
        const keys = {};
        document.addEventListener('keydown', (e) => keys[e.code] = true);
        document.addEventListener('keyup', (e) => keys[e.code] = false);

        function update() {
            if(keys['ArrowUp']) player.position.z -= 0.1;
            if(keys['ArrowDown']) player.position.z += 0.1;
            if(keys['ArrowLeft']) player.position.x -= 0.1;
            if(keys['ArrowRight']) player.position.x += 0.1;
            
            // הפעלת מוזיקה בהתחלה
            if(keys['ArrowUp']) document.getElementById('bg-music').play();
        }

        function animate() {
            update();
            renderer.render(scene, camera);
            requestAnimationFrame(animate);
        }
        animate();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return FULL_GAME_HTML

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
