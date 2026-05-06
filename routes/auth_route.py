from flask import (
    Flask, redirect, render_template, Blueprint,
    request, url_for, flash, session, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user
from models import User, PasswordReset
from flask_mail import Message
from extensions import db, mail
import random

auth = Blueprint("auth", __name__)


# -------------------- LOGIN --------------------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        current_app.logger.info(f"Login attempt for email: {email}")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            current_app.logger.info(f"User logged in successfully: {email}")
            return redirect(url_for('home_auth.home'))
        else:
            current_app.logger.warning(f"Failed login attempt for email: {email}")
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

    return render_template("login.html")

# -------------------- REGISTER --------------------
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')

        current_app.logger.info(f"Registration attempt for email: {email}")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            current_app.logger.warning(f"Registration failed – user exists: {email}")
            flash('User already exists, Please login!')
            return redirect(url_for('auth.login'))

        new_user = User(
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            email=email
        )
        new_user.set_password(request.form.get('password'))

        db.session.add(new_user)
        db.session.commit()

        current_app.logger.info(f"New user registered: {email}")
        flash('Registration successful! Please log in.')
        return redirect(url_for('auth.login'))

    return render_template("signup.html")

# -------------------- FORGOT PASSWORD --------------------
@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        current_app.logger.info(f"Password reset requested for email: {email}")

        user = User.query.filter_by(email=email).first()
        if not user:
            current_app.logger.warning(f"Password reset failed – email not found: {email}")
            flash("No user found with this email.")
            return redirect(url_for('auth.forgot_password'))

        otp = str(random.randint(100000, 999999))
        reset_request = PasswordReset(user_id=user.id, otp=otp)
        db.session.add(reset_request)
        db.session.commit()

        msg = Message(
        subject="Your OTP for Password Reset - BITE ON GO",
        recipients=[email],
        html=f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Password Reset OTP</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
            </style>
        </head>
        <body style="margin: 0; padding: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #0A0A0A 0%, #1A1A1A 100%); color: #FFFFFF;">
            <div style="max-width: 550px; margin: 0 auto; padding: 40px 20px;">
                <!-- Main Card -->
                <div style="background: rgba(15, 15, 15, 0.95); border-radius: 24px; border: 1px solid rgba(247, 147, 26, 0.3); overflow: hidden; backdrop-filter: blur(10px); box-shadow: 0 20px 40px rgba(0,0,0,0.5);">
                    
                    <!-- Header with Gradient -->
                    <div style="background: linear-gradient(135deg, #F7931A 0%, #E67E22 100%); padding: 35px 20px; text-align: center;">
                        <div style="font-size: 48px; margin-bottom: 10px;">🍔</div>
                        <h1 style="margin: 0; font-size: 32px; font-weight: 800; color: #000000; letter-spacing: -1px;">BITE ON GO</h1>
                        <p style="margin: 10px 0 0 0; color: #000000; opacity: 0.8; font-weight: 500;">Password Reset Request</p>
                    </div>
                    
                    <!-- Content Area -->
                    <div style="padding: 40px 30px;">
                        <!-- Greeting -->
                        <h2 style="margin: 0 0 10px 0; font-size: 24px; font-weight: 600;">Hello {user.first_name}! 👋</h2>
                        <p style="margin: 0 0 25px 0; color: #AAAAAA; line-height: 1.6; font-size: 15px;">
                            We received a request to reset your password for your <strong style="color: #F7931A;">BITE ON GO</strong> account. Use the OTP below to complete the process.
                        </p>
                        
                        <!-- OTP Box -->
                        <div style="background: #0A0A0A; border-radius: 16px; padding: 25px; text-align: center; border: 1px solid rgba(247, 147, 26, 0.2); margin: 25px 0;">
                            <p style="margin: 0 0 10px 0; color: #888888; font-size: 12px; text-transform: uppercase; letter-spacing: 2px;">Your One-Time Password</p>
                            <div style="font-size: 48px; font-weight: 800; color: #F7931A; letter-spacing: 8px; font-family: monospace; background: rgba(247, 147, 26, 0.1); padding: 15px 20px; border-radius: 12px; display: inline-block;">
                                {otp}
                            </div>
                            <p style="margin: 20px 0 0 0; color: #666666; font-size: 12px;">⏰ Valid for 30 seconds</p>
                        </div>
                        
                        <!-- Security Warning -->
                        <div style="background: rgba(247, 147, 26, 0.05); border-left: 3px solid #F7931A; padding: 15px; border-radius: 8px; margin: 25px 0;">
                            <p style="margin: 0; font-size: 13px; color: #FFB347;">
                                <strong>🔒 Security Alert:</strong> Never share this OTP with anyone. BITE ON GO staff will NEVER ask for your OTP.
                            </p>
                        </div>
                        
                        <!-- Instructions -->
                        <div style="margin: 25px 0; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 25px;">
                            <p style="margin: 0 0 15px 0; font-weight: 600; color: #FFFFFF;">What to do next:</p>
                            <ol style="margin: 0; padding-left: 20px; color: #AAAAAA; line-height: 1.8; font-size: 14px;">
                                <li>Enter this OTP in the password reset page</li>
                                <li>Create your new password</li>
                                <li>Login and continue enjoying your meals! 🍕</li>
                            </ol>
                        </div>
                        
                        <!-- Did not request section -->
                        <div style="background: rgba(255,68,68,0.05); border-radius: 12px; padding: 15px; margin-top: 20px;">
                            <p style="margin: 0; font-size: 12px; color: #FF8888;">
                                ❌ <strong>Didn't request this?</strong> Ignore this email or contact support immediately at <a href="mailto:support@biteongo.com" style="color: #F7931A; text-decoration: none;">support@biteongo.com</a>
                            </p>
                        </div>
                    </div>
                    
                    <!-- Footer -->
                    <div style="background: rgba(0,0,0,0.3); padding: 20px 30px; text-align: center; border-top: 1px solid rgba(255,255,255,0.05);">
                        <p style="margin: 0 0 10px 0; font-size: 12px; color: #666666;">
                            BITE ON GO — Fast food delivered fresh 🚀
                        </p>
                        <p style="margin: 0; font-size: 11px; color: #555555;">
                            This is an automated message, please do not reply.
                        </p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
    )

        try:
            mail.send(msg)
            current_app.logger.info(f"OTP sent successfully to {email}")
            flash("OTP sent to your email.")
            return redirect(url_for('auth.verify_otp'))
        except Exception as e:
            current_app.logger.error(
                f"Failed to send OTP to {email}", exc_info=True
            )
            flash("Failed to send OTP. Try again later.")
            return redirect(url_for('auth.forgot_password'))

    return render_template("forgot_password.html")

# -------------------- VERIFY OTP --------------------
@auth.route("/verify-otp", methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form.get('otp')
        current_app.logger.info("OTP verification attempt")

        reset_request = PasswordReset.query.filter_by(
            otp=entered_otp,
            is_used=False
        ).order_by(PasswordReset.created_at.desc()).first()

        if not reset_request:
            current_app.logger.warning("Invalid OTP entered")
            flash("Invalid OTP.")
            return redirect(url_for('auth.verify_otp'))

        if reset_request.is_expired():
            current_app.logger.warning("Expired OTP used")
            flash("OTP expired.")
            return redirect(url_for('auth.forgot_password'))

        reset_request.is_used = True
        db.session.commit()

        session['reset_user_id'] = reset_request.user_id
        current_app.logger.info("OTP verified successfully")

        flash("OTP verified successfully!")
        return redirect(url_for('auth.reset_password'))

    return render_template("verify_otp.html")

# -------------------- RESET PASSWORD --------------------
@auth.route("/reset-password", methods=['GET', 'POST'])
def reset_password():
    user_id = session.get('reset_user_id')

    if not user_id:
        current_app.logger.warning("Reset password session expired")
        flash("Session expired.")
        return redirect(url_for('auth.forgot_password'))

    user = User.query.get(user_id)
    if not user:
        current_app.logger.error("User not found during password reset")
        flash("User not found.")
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        user.password = generate_password_hash(request.form.get('password'))
        db.session.commit()

        session.pop('reset_user_id', None)
        current_app.logger.info(f"Password reset successful for user ID {user_id}")

        flash("Password updated successfully!")
        return redirect(url_for('auth.login'))

    return render_template("reset_password.html")

# -------------------- LOGOUT --------------------
@auth.route("/logout")
@login_required
def logout():
    current_app.logger.info("User logged out")
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("auth.login"))
