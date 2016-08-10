from flask import render_template
from app import app
from app import db,models
from datetime import datetime, timedelta

temperature = {}
electricity = {}
mail = {}

#return given sensors last minute value
def getlastvalue(sensorid):
    delta=(datetime.now()-timedelta(minutes=2)) #get values from last two minutes, just in case
    data=models.Data.query.filter(models.Data.sensorid==sensorid,models.Data.time>delta).all()
    return data[-1].value #return last value
 

@app.route('/')
@app.route('/index')
def index():
    temperature = {'outside': getlastvalue(6)} #sensorid 6 is the outside temperature
#"select mlp.time, mlp.kW mlp_kW, main.kW-mlp.kW main_kw from (select time,value/1.66666 kW from data where sensorid=116 and time>now() - interval 2 minute) mlp,
# (select time,value/16.6666 kW from data where sensorid=115 and time>now() - interval 2 minute) main where mlp.time=main.time order by 1";
    wholeelectricity=float(getlastvalue(115))/16.6666 #1000 pulses per kWh
    heatpumpelectricity=float(getlastvalue(116))/1.66666 #100 pulses per Kwh
    electricity = {'normal': wholeelectricity-heatpumpelectricity,
                   'whole': wholeelectricity,
                   'heatpump': heatpumpelectricity}

    return render_template('index.html',
                           temperature=temperature,
                           electricity=electricity)

