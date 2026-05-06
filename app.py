from flask import Flask, render_template, redirect, request, flash, url_for, session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message, Mail
import random
import logging

from extensions import db, mail
from models import User, Feedback, PasswordReset

from routes.about_route import about_auth
from routes.auth_route import auth
from routes.contact_route import contact_auth
from routes.home_route import home_auth

# -------------------- APP SETUP --------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biteongo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# -------------------- LOGGING SETUP --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

app.logger.info("Flask application starting...")

# -------------------- DATABASE --------------------
db.init_app(app)
app.logger.info("Database initialized")

# -------------------- LOGIN MANAGER --------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
app.logger.info("LoginManager initialized")

# -------------------- MAIL CONFIG --------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'cyberdev203@gmail.com'
app.config['MAIL_PASSWORD'] = 'gvje rctp ycmv nqdd'
app.config['MAIL_DEFAULT_SENDER'] = 'cyberdev203@gmail.com'

mail = Mail(app)
app.logger.info("Mail service configured")

# -------------------- USER LOADER --------------------
@login_manager.user_loader
def load_user(user_id):
    app.logger.debug(f"Loading user with ID: {user_id}")
    return User.query.get(int(user_id))

# -------------------- BLUEPRINTS --------------------
app.register_blueprint(auth)
app.logger.info("Auth blueprint registered")

app.register_blueprint(home_auth)
app.logger.info("Home blueprint registered")

app.register_blueprint(about_auth)
app.logger.info("About blueprint registered")

app.register_blueprint(contact_auth)
app.logger.info("Contact blueprint registered")

# -------------------- RUN APP --------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.logger.info("Database tables created")

    app.logger.info("Running Flask development server")
    app.run(debug=True)