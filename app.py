from flask import Flask, render_template, redirect, request, flash, url_for, session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message,Mail
import random

from extensions import db,mail
from models import User,Feedback,PasswordReset
from routes.about_route import about_auth
from routes.auth_route import auth
from routes.contact_route import contact_auth
from routes.home_route import home_auth

app = Flask(__name__)


app.config['SECRET_KEY'] = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Adeoluwa2244@localhost/Biteongo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'cyberdev203@gmail.com'  
app.config['MAIL_PASSWORD'] = 'hozw zipq bvqa lmkj'         
app.config['MAIL_DEFAULT_SENDER'] = 'cyberdev203@gmail.com'

mail = Mail(app)


# ================= LOGIN LOADER =================
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth)
app.register_blueprint(home_auth)
app.register_blueprint(about_auth)
app.register_blueprint(contact_auth)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database tables created.")
    app.run(debug=True)    