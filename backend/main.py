from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from app.routes.posture import posture_bp  
app = Flask(__name__, static_folder='build', static_url_path='')
CORS(app)
app.register_blueprint(posture_bp)
@app.route('/')
@app.route('/<path:path>')
def serve_react(path=''):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
if __name__ == "__main__":
    app.run(debug=True, port=5000)
