from flask import render_template
from app import app
from app import db,models
from datetime import datetime, timedelta
from sqlalchemy.exc import OperationalError
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print('Connected with result code '+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('/house/mail')

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global mailstatus
    print ('Topic: '+ msg.topic+'\nMessage: '+str(msg.payload))
    mailstatus=msg.payload.decode('UTF-8')
    print(mailstatus)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('roope.local', 1883, 60)

# NonBlocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()

mailstatus=''
temperature = {}
electricity = {}
mail = {}

#return given sensors last minute value
def getlastvalue(sensorid):
    delta=(datetime.now()-timedelta(minutes=2)) #get values from last two minutes, just in case
    try:
        data=models.Data.query.filter(models.Data.sensorid==sensorid,models.Data.time>delta).all()
    except OperationalError: #db connection has closed, return nan
        db.session.rollback()
        return float('NaN')
    if len(data)==0: #check fi there is data, if not, return error
        return float('NaN')
    return data[-1].value #return last value

def getlastontimeforheatpump(sensorid):

    try:
        time=db.session.query(db.func.max(models.Data.time)).filter(models.Data.sensorid==sensorid,models.Data.value>5).all()
    except OperationalError: #db connection has closed, return nan
        db.session.rollback()
        return float('NaN')
    if len(time)==0: #check fi there is data, if not, return error
        return float('NaN')
    return time[0][0] #return last value


@app.route('/')
@app.route('/index')
def index():
    temperature = {'outside': getlastvalue(6)} #sensorid 6 is the outside temperature
    wholeelectricity=float(getlastvalue(115))/16.6666 #1000 pulses per kWh
    heatpumpelectricity=float(getlastvalue(116))/1.66666 #100 pulses per Kwh
    electricity = {'normal': wholeelectricity-heatpumpelectricity,
                   'whole': wholeelectricity,
                   'heatpump': heatpumpelectricity}
    heatpumplastontime=getlastontimeforheatpump(116)
    heatpumpstatus='on' if heatpumpelectricity > 5 else 'off'
    heatpump = {'laston':heatpumplastontime,
                'status':heatpumpstatus}
    mail=''
    if mailstatus=='you have mail':
        mail='Mail!!'
    return render_template('index.html',
                           temperature=temperature,
                           electricity=electricity,
                           mailstatus=mail,
                           heatpump=heatpump)

