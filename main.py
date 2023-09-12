from flask import Flask, request, redirect, render_template
import sqlite3
import string
import random

app = Flask(__name__)

# Database initialization
conn = sqlite3.connect('urls.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS urls
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   original_url TEXT,
                   short_url TEXT)''')
conn.commit()

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['original_url']
    if not original_url.startswith('http://') and not original_url.startswith('https://'):
        original_url = 'http://' + original_url

    cursor.execute('SELECT short_url FROM urls WHERE original_url = ?', (original_url,))
    existing_short_url = cursor.fetchone()
    if existing_short_url:
        return render_template('result.html', short_url=existing_short_url[0])

    short_url = generate_short_url()
    cursor.execute('INSERT INTO urls (original_url, short_url) VALUES (?, ?)', (original_url, short_url))
    conn.commit()

    return render_template('result.html', short_url=short_url)

@app.route('/<short_url>')
def redirect_to_original(short_url):
    cursor.execute('SELECT original_url FROM urls WHERE short_url = ?', (short_url,))
    original_url = cursor.fetchone()
    if original_url:
        return redirect(original_url[0])
    else:
        return "Short URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
