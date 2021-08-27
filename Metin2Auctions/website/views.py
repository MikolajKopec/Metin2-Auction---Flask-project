from os import name
from flask import Blueprint,render_template,request
from flask.helpers import flash, url_for
from flask_login import current_user,login_required
from werkzeug.utils import redirect
from . import db
from .models import Auction,Item
views = Blueprint('views',__name__)

@views.route('/',methods =['GET','POST'])
def home():
    auction = None
    item = None
    auction = Auction.query.all()
    item = Item.query.all()
    if request.method == "GET" and request.args:
        item_name = request.args.get("item_name")
        search = f"%{item_name}%"
        auction = Auction.query.filter(Auction.item_name.like(search)).all()
        
    elif request.method == "GET":
        pass
    else:
        bid = request.form['bid']
        id = request.form['auction_id']
        winner = current_user.login
        auction_price = Auction.query.filter_by(id = id).first()
        if int(auction_price.cw)<int(bid) and int(auction_price.kt)>(int(bid)):
            auction_price.cw=bid
            auction_price.winner=winner
            db.session.commit()
        elif int(auction_price.kt)<=int(bid):
            flash('Your bid is too high, use BUY NOW', category='error')
        else:
            flash('Input higher value than actual price',category='error')
        return redirect(f'/#auction_{id}')
    return render_template('home.html', user = current_user,auction = auction, item = item)


@views.route('/sort/')
def sort():
    
    return redirect(url_for('.home', filter_name = x))
