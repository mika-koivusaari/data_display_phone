from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    temperature = {'outside': 20.0}
    electricity = {'normal': 1.5}

    return render_template('index.html',
                           temperature=temperature,
                           electricity=electricity)

