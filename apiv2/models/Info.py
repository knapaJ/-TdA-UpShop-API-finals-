from apiv2 import db
import datetime

class Info(db.Model):
    '''
    Info about server has:
    - date
    - cpu_load
    - ram_load
    - net_load
    '''

    __tablename__ = "info"

    _id = db.Column(db.Integer, primary_key=True, name='id')
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    cpu_load = db.Column(db.Float, nullable=False)
    ram_load = db.Column(db.Float, nullable=False)
    net_load = db.Column(db.Float, nullable=False)

    def __init__(self, cpu_load: float, ram_load: float, net_load: float):
        self.cpu_load = cpu_load
        self.ram_load = ram_load
        self.net_load = net_load

    def __repr__(self):
        return f"[INFO] CPU: {self.cpu_load}, RAM: {self.ram_load}, NET: {self.net_load}"