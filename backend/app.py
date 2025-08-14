from flask import Flask, send_from_directory
from flask_cors import CORS

from src.routes.materials import register_routes as register_routes_materials
from src.routes.parameters import register_routes as register_routes_parameters
from src.routes.data import register_routes as register_routes_data

# app
app = Flask(__name__, static_folder='build', static_url_path='')
cors = CORS(app,
    resources={ r"/api/*": { "origins": ["http://localhost:*"] } },
    allow_headers=["*"],
    methods=["GET", "POST", "OPTIONS"],
    supports_credentials=True
)

# Serve the static React files
@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

# Fallback route: Flask serves static files if no other API route matches
@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)



# register all routes
register_routes_materials(app)
register_routes_parameters(app)
register_routes_data(app)


if __name__ == "__main__":
    app.run()
