from app import db

class Data(db.Model):
    sensorid = db.Column(db.Integer,primary_key=True)
    #timezone needs to false because times in weather db are naive
    time = db.Column(db.DateTime(timezone=False),primary_key=True)
    value = db.Column(db.Float,primary_key=False)

    def __repr__(self):
        return 'Sensorid %d time %s value %f ' % (self.sensorid,self.time.strftime('%Y.%m.%d %H:%M'),self.value)
