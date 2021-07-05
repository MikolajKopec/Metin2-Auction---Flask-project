from os import error, path
from flask import Blueprint, app,render_template,request
from flask.helpers import flash, url_for
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null
from werkzeug.utils import redirect, secure_filename   
from flask_login import current_user,login_required
from .models import Auction,Item
from . import create_app,db
auctioner = Blueprint('auctioner',__name__)

IMAGE_STORAGE = './website/static/auction_images/'
ALLOWED_EXTENSIONS = {'jpeg','png','webp','jpg','gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@auctioner.route('/buy-now/auction_id=<auction_id>')
def end_auction(auction_id):
    Auction.query.filter_by(id = auction_id).delete()
    Item.query.filter_by(auction_id = auction_id).delete()
    db.session.commit()
    # THINGS WITH END AUCTIONS - CONTACT ETC - TO DO
    return redirect(url_for('views.home'))



@auctioner.route('/create_auction',methods=['GET','POST'])
def create_auction():
    info = None
    category = 'error'
    if request.method=="GET":
        pass
    else:
        cw = request.form['cw']
        kt = request.form['kt']
        more = request.form['more']
        if int(cw)<0 or int(kt)<=0:
            info = "Not to cheap? (to low values of price)"
        elif len(more)>300:
            info = "Please make your additional infiormation shorter (max. 300 characters)."
        elif 'img' not in request.files:
            info = "Please upload image"
        else:
            img = request.files['img']
            if img.filename == '':
                img.filename ="auction.png"
            if img and allowed_file(img.filename):
                img_name = secure_filename(img.filename)
                storage = path.join(IMAGE_STORAGE, img_name)
                img.save(storage)
                info = 'Your auction have been posted.'
            else:
                info = "Wrong format of photo. Check your image."

        auction_category = request.form['category']
        if (auction_category=="item"):
            element = '0'
            item = request.form['item']
            upgrade = int(request.form['upgrade'])
            if request.form['element']:
                element = int(request.form['element'])
            bonus_number = int(request.form['bonus_number'])
            bonus = []
            for i in range(1,bonus_number+1):
                text = request.form[f'bonus_name{i}']
                num = request.form[f'bonus{i}']
                bonus.append(f'{text} - {num} / ')
            print(bonus)
            if len(item)>30 or len(item)<6:
                info = "Your item name is too long, or too short (shoud be 6-30 characters)."
                print(item)
            elif upgrade<0 or upgrade>15:
                info = "Make sure you input good level of upgrade"
            else:
                category='success'

        if category=='success':
            bonuses = ''
            for each in bonus:
                bonuses+= f'{each}'
            new_auction = Auction(cw=cw,auction_type = auction_category,item_name = item,kt=kt,informations=more,img = img_name, owner_id = current_user.id)
            db.session.add(new_auction)
            db.session.commit()
            auction_list = Auction.query.all()
            auction_id = auction_list[-1].id
            new_item = Item(upgrade = upgrade,element = element, bonuses = bonuses, auction_id = auction_id )
            db.session.add(new_item)
            db.session.commit()
    if info is not None:
        flash(info,category=category)
    return render_template('create_auction.html', user = current_user)