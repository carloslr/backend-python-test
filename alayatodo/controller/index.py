
from alayatodo import app
from flask import (
    render_template
)

@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        return render_template('index.html', readme=f.read())