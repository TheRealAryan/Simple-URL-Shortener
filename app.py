from flask import Flask, request, redirect, render_template, url_for
import string
import random
from storage import save_mapping, load_mapping
from urllib.parse import urlparse, urlunparse

app = Flask(__name__)

url_mapping = load_mapping()  # Load URL mappings from the storage

def generate_short_id(length=6):
    characters = string.ascii_letters + string.digits
    short_id = ''.join(random.choice(characters) for _ in range(length))
    return short_id

def normalize_url(url):
    parsed_url = urlparse(url)
    normalized_path = parsed_url.path.rstrip('/').lower()
    normalized_url = urlunparse((parsed_url.scheme, parsed_url.netloc.lower(), normalized_path, '', '', ''))
    return normalized_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        long_url = normalize_url(long_url)

        # Check for duplicates
        for short_id, existing_long_url in url_mapping.items():
            if existing_long_url == long_url:
                short_url = request.host_url + short_id
                return render_template('index.html', short_url=short_url, url_mapping=url_mapping, message="This URL has already been shortened:")

        # If no duplicate, create a new short URL
        short_id = generate_short_id()
        while short_id in url_mapping:  # Ensures short_id is unique
            short_id = generate_short_id()

        url_mapping[short_id] = long_url
        save_mapping(url_mapping)  # Saves to storage

        short_url = request.host_url + short_id
        return render_template('index.html', short_url=short_url, url_mapping=url_mapping)
    return render_template('index.html', url_mapping=url_mapping)

@app.route('/<short_id>')
def redirect_to_long_url(short_id):
    long_url = url_mapping.get(short_id)
    if long_url:
        return redirect(long_url)
    else:
        return '<h1>URL not found!</h1>', 404

@app.route('/delete/<short_id>', methods=['POST'])
def delete_url(short_id):
    if short_id in url_mapping:
        del url_mapping[short_id]
        save_mapping(url_mapping)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
