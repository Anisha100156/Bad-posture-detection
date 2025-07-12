from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from backend.app.routes.posture import posture_bp


# Flask app setup
app = Flask(__name__, static_folder='build', static_url_path='')
CORS(app)  # Enable CORS

# Register Blueprint
app.register_blueprint(posture_bp)

# Serve React frontend
@app.route('/')
@app.route('/<path:path>')
def serve_react(path=''):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# ✅ Use dynamic port for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000)) 
    print(f"Running on port {port}")
     # Render sets PORT env var
    app.run(host="0.0.0.0", port=port, debug=True)
