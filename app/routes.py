from app import app
from flask import request, jsonify, redirect
import random
import string

# In-memory key-value store for URL mappings
url_mapping = {}

# Function to generate a random short URL
def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# API to shorten a URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.json.get('long_url')
    if long_url:
        short_url = generate_short_url()
        url_mapping[short_url] = long_url
        return jsonify({"short_url": short_url}), 201
    return jsonify({"error": "Invalid URL"}), 400

# Redirect API to access the long URL from short URL
@app.route('/<short_url>', methods=['GET'])
def redirect_to_url(short_url):
    long_url = url_mapping.get(short_url)
    if long_url:
        return redirect(long_url)
    return jsonify({"error": "Short URL not found"}), 404

