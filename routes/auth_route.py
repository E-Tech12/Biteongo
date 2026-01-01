from flask import Flask,redirect,render_template,Blueprint,request,url_for,flash,session
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import login_user,login_required,logout_user
from models import User,PasswordReset
from flask_mail import Mail,Message 
from extensions import db,mail
from random import random, randint

auth = Blueprint("auth",__name__)
@auth.route('/', methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home_auth.home'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

    return render_template("login.html")

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('User already exists,Please login!!')
            return redirect(url_for('auth.login'))

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.')
        return redirect(url_for('auth.login'))

    return render_template("signup.html")
@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("No user found with this email.")
            return redirect(url_for('auth.forgot_password'))

        otp = str(random.randint(100000, 999999))

        reset_request = PasswordReset(user_id=user.id, otp=otp)
        db.session.add(reset_request)
        db.session.commit()

        msg = Message(
            subject="Your OTP for Password Reset",
            recipients=[email]
        )
        msg.body = f"Hello {user.first_name},\n\nYour OTP for password reset is: {otp}\nIt is valid for 10 minutes.\n\nBITE ON GO"

        try:
            mail.send(msg)
            flash("OTP sent to your email. Check your inbox!")
            return redirect(url_for('verify_otp'))
        except Exception as e:
            print(e)
            flash("Failed to send OTP. Try again later.")
            return redirect(url_for('auth.forgot_password'))

    return render_template("forgot_password.html")
@auth.route("/verify-otp", methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form.get('otp')

        reset_request = PasswordReset.query.filter_by(
            otp=entered_otp,
            is_used=False
        ).order_by(PasswordReset.created_at.desc()).first()

        if not reset_request:
            flash("Invalid OTP.")
            return redirect(url_for('verify_otp'))

        if reset_request.is_expired():
            flash("OTP expired. Please request a new one.")
            return redirect(url_for('auth.forgot_password'))

        # Mark OTP as used
        reset_request.is_used = True
        db.session.commit()

        session['reset_user_id'] = reset_request.user_id

        flash("OTP verified successfully!")
        return redirect(url_for('auth.reset_password'))

    return render_template("verify_otp.html")
@auth.route("/reset-password", methods=['GET', 'POST'])
def reset_password():
    user_id = session.get('reset_user_id')
    if not user_id:
        flash("Session expired. Start again.")
        return redirect(url_for('auth.forgot_password'))

    user = User.query.get(user_id)
    if not user:
        flash("User not found.")
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        new_password = request.form.get('password')
        user.password = generate_password_hash(new_password)
        db.session.commit()


        session.pop('reset_user_id', None)

        flash("Password updated successfully! You can now log in.")
        return redirect(url_for('login'))

    return render_template("reset_password.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("auth.login"))