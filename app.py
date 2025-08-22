from flask import Flask, render_template, request, redirect, url_for, flash
import string
import random

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for flash messages

# In-memory storage for URLs (use a database in production)
url_mapping = {}

def generate_short_id(length=6):
    """Generate a random short ID."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form.get('url')
        # Basic validation
        if not original_url.startswith(('http://', 'https://')):
            flash('Please enter a valid URL starting with http:// or https://')
            return render_template('index.html', short_url=None)
        
        # Generate unique short ID
        short_id = generate_short_id()
        while short_id in url_mapping:
            short_id = generate_short_id()
        
        # Store mapping
        url_mapping[short_id] = original_url
        short_url = url_for('redirect_url', short_id=short_id, _external=True)
        return render_template('index.html', short_url=short_url)
    
    return render_template('index.html', short_url=None)

@app.route('/<short_id>')
def redirect_url(short_id):
    original_url = url_mapping.get(short_id)
    if original_url:
        return redirect(original_url)
    else:
        flash('Invalid or expired short URL')
        return render_template('index.html', short_url=None)

if __name__ == '__main__':
    app.run(debug=True)