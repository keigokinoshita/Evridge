from sqlalchemy import Column, Integer, String, Text, DateTime
from model.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    user_id = Column(String(128), primary_key=True)
    address= Column(String(100))
    tel = Column(String(20))
    hashed_password = Column(String(128))

    def __init__(self, user_id=None, address=None, tel=None, hashed_password=None):
        self.user_id = user_id
        self.address = address
        self.tel = tel
        self.hashed_password = hashed_password

    def __repr__(self):
        return '<Name %r>' % (self.id)

class Event(Base):
    __tablename__ = 'events'
    event_id = Column(Integer, primary_key=True,autoincrement=True)
    user_id = Column(String(128))
    img_path = Column(String(128))
    host = Column(String(128))
    address= Column(String(100))
    tel = Column(String(20))
    title = Column(String(128))
    date = Column(DateTime)
    place = Column(String(128))
    body = Column(Text)
    url = Column(String(256))
    is_adv = Column(Integer)
   

    def __init__(self, user_id=None, img_path=None,host=None,address=None,tel=None, \
                                                        title=None,date=None,place=None,body=None,url=None,is_adv=None):
        self.user_id = user_id
        self.img_path = img_path
        self.host = host
        self.address = address
        self.tel = tel
        self.title = title
        self.date = date
        self.place = place
        self.body = body
        self.url = url
        self.is_adv = is_adv

    def __repr__(self):
        return '<Title %r>' % (self.title)