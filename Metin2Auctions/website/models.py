from enum import unique
from sqlalchemy.orm import backref
from sqlalchemy.sql.expression import false, null
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Auction(db.Model):
    id = db.Column(db.Integer,primary_key = True)

    informations = db.Column(db.String(300))
    cw = db.Column(db.Integer)
    kt = db.Column(db.Integer)
    img = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    winner = db.Column(db.String(30))
    item_name = db.Column(db.String(150))
    auction_type = db.Column(db.String(150))

    owner_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    items = db.relationship('Item',backref='auction',lazy='dynamic')
    # characters = db.relationship('Character',backref='auction',lazy='dynamic')

class Item(db.Model):
    id = db.Column(db.Integer,primary_key = True)

    upgrade = db.Column(db.Integer, nullable = false)
    element = db.Column(db.String(150))
    bonuses = db.Column(db.String(500))

    auction_id = db.Column(db.Integer,db.ForeignKey('auction.id'))

# class Character(db.Model):
#     id = db.Column(db.Integer,primary_key = True)

#     item_name = db.Column(db.String(150))
#     element = db.Column(db.String(150))
#     bonus_1 = db.Column(db.String(150))
#     bonus_2 = db.Column(db.String(150))
#     bonus_3 = db.Column(db.String(150))
#     bonus_4 = db.Column(db.String(150))
#     bonus_5 = db.Column(db.String(150))
#     bonus_6 = db.Column(db.String(150))
#     bonus_7 = db.Column(db.String(150))

#     auction_id = db.Column(db.Integer,db.ForeignKey('auction.id'))
    
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)

    email = db.Column(db.String(150),unique = True)
    password = db.Column(db.String(150))
    login = db.Column(db.String(150),unique = True)

    auctions = db.relationship('Auction',backref='user',lazy='dynamic')