from flask import Blueprint,render_template,request,flash,redirect
from flask.helpers import url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user,logout_user,current_user,login_required

auth = Blueprint('auth',__name__)

@auth.route('/login',methods = ['GET','POST'])
def login():
    if request.method =="POST":
        login = request.form.get('login')
        password = request.form.get('password')

        user = User.query.filter_by(login=login).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in!',category = 'success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again',category = 'error')
        else:
            flash('There is no user with that login',category = 'error')
    return render_template('login.html', user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register',methods=['GET','POST'])
def register():
    info = None
    success = 'error'
    if request.method=='POST':
        email = request.form['email']
        login = request.form['login']
        password = request.form['password']
        password_chck = request.form['password_chck']
        user_login = User.query.filter_by(login=login).first()
        user_email = User.query.filter_by(email=email).first()
        if user_login:
            info = 'User with that login already exist'
        elif user_email:
            info = 'User with that email already exist'
        elif(len(login)<6 or len(login)>16):
            info = "Wrong login lenght, check it and try again."
        elif(len(password)<6 or len(password)>16):
            info = "Wrong password lenght, check it and try again."
        elif(password!=password_chck):
            info = "Both passwords are different, check it and try again."
        elif(len(email)<4):
            info = "Wrong email, check it and try again."
        else:
            new_user = User(email = email,login = login, password = generate_password_hash(password,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            info="You are registred succesfully!"
            success = 'success'
        flash(info,category=success)
        if success=='success':
            return redirect(url_for('auth.login',info = info, success = success))
    return render_template('register.html',user = current_user , success = success, )