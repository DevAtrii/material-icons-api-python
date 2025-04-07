from flask import Flask
from flask_cors import CORS

from py_utils.common_utils.file_utils import open_file_as_json

app = Flask(__name__)
CORS(app, resources={
    r"/maker/*": {
        "origins": ["*"],  # Allow all origins for development
        "methods": ["GET", "POST"],  # Allowed methods
        "allow_headers": ["Content-Type"]  # Allowed headers
    }
})

ICONS_DATABASE = open_file_as_json(path='icons_db.json')

# Add global cache headers
@app.after_request
def add_cache_headers(response):
    # Default cache control for API responses (1 hour)
    response.headers['Cache-Control'] = 'public, max-age=3600'
    return response

from api_routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=2005)
