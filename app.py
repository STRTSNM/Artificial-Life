from flask import Flask, render_template, send_from_directory
import os
import re

app = Flask(__name__)


IMAGE_DIR = 'patterns_images'

def extract_number(filename):
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else 0

@app.route('/')
def index():
    images = [f for f in os.listdir(IMAGE_DIR) if os.path.isfile(os.path.join(IMAGE_DIR, f))]
    
    images.sort(key=extract_number)
    
    return render_template('index.html', images=images)

@app.route('/patterns_images/<filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

if __name__ == '__main__':
    app.run(debug=False, port=8000)

