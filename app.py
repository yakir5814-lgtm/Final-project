from flask import Flask

app = Flask(__name__)

GAME_3D_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>School Journey 3D</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>body { margin: 0; overflow: hidden; } canvas { display: block; }</style>
</head>
<body>
    <script>
        // 1. הגדרת זירת המשחק
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // 2. יצירת "הילד" (דמות פשוטה כרגע, אפשר להחליף במודל 3D)
        const geometry = new THREE.BoxGeometry(0.5, 1.5, 0.5);
        const material = new THREE.MeshPhongMaterial({ color: 0x38bdf8 });
        const player = new THREE.Mesh(geometry, material);
        scene.add(player);

        // 3. תאורה (בשביל איכות של סרט אנימציה)
        const light = new THREE.DirectionalLight(0xffffff, 1);
        light.position.set(5, 5, 5);
        scene.add(light);
        scene.add(new THREE.AmbientLight(0x404040));

        // 4. מסלול הליכה (הרחוב)
        const ground = new THREE.Mesh(new THREE.PlaneGeometry(100, 100), new THREE.MeshPhongMaterial({ color: 0x222222 }));
        ground.rotation.x = -Math.PI / 2;
        scene.add(ground);

        camera.position.set(0, 2, 5);
        player.add(camera); // המצלמה עוקבת אחרי השחקן (GTA style)

        // 5. לוגיקת תנועה
        document.addEventListener('keydown', (e) => {
            if(e.key === 'ArrowUp') player.position.z -= 0.1;
            if(e.key === 'ArrowDown') player.position.z += 0.1;
            if(e.key === 'ArrowLeft') player.position.x -= 0.1;
            if(e.key === 'ArrowRight') player.position.x += 0.1;
        });

        function animate() {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return GAME_3D_HTML

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
