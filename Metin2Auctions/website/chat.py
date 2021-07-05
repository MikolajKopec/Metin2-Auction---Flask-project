from flask import Flask,render_template,Blueprint
from flask_login import login_manager,current_user
import socketio
from sqlalchemy.sql.functions import user


chat = Blueprint('chat',__name__)

@chat.route('/chat')
def chat_create():
   return render_template('chat.html', user = current_user)