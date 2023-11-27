from genderTracker.setup import app
from flask import send_from_directory
import os

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, 'dist', path)):
        return send_from_directory(os.path.join(app.static_folder, 'dist'), path)
    else:
        return send_from_directory(os.path.join(app.static_folder, 'dist'), 'index.html')

# Set the static_folder to your 'static' directory and static_url_path to serve from the root '/'
app.static_folder = 'static'
app.static_url_path = '/'

