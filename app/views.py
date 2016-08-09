from flask import render_template
from app import app
from app import db,models
from datetime import datetime, timedelta

temperature = {}
electricity = {}
mail = {}

@app.route('/')
@app.route('/index')
def index():
    delta=(datetime.now()-timedelta(minutes=2))
    temps=models.Data.query.filter(models.Data.sensorid==6,models.Data.time>delta).all()
    last_temp=temps[-1]
    temperature = {'outside': last_temp.value}
    electricity = {'normal': 1.5}

    return render_template('index.html',
                           temperature=temperature,
                           electricity=electricity)

