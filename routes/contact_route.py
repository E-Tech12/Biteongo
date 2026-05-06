from flask import (
    Blueprint, redirect, render_template,
    request, url_for, flash, current_app
)
from models import Feedback
from flask_mail import Message
from extensions import mail, db

contact_auth = Blueprint("contact_auth", __name__)

@contact_auth.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message_body = request.form.get('message')

        current_app.logger.info(f"Contact form submitted by {email}")

        if not name or not email or not message_body:
            current_app.logger.warning(
                "Contact form submission failed: missing fields"
            )
            flash("Please fill out all fields.")
            return redirect(url_for('contact_auth.contact'))

        feedback = Feedback(  
            name=name,
            email=email,
            message=message_body
        )

        try:
            db.session.add(feedback)
            db.session.commit()
            current_app.logger.info(
                f"Feedback saved to database from {email}"
            )
        except Exception:
            current_app.logger.error(
                "Failed to save feedback to database",
                exc_info=True
            )
            flash("Something went wrong. Please try again.")
            return redirect(url_for('contact_auth.contact'))

        msg = Message(
            subject=f"New Feedback from {name}",
            recipients=['cyberdev203@gmail.com']
        )

        msg.body = f"""\
Hello,

You have received a new message from your Eatery website (BITE ON GO).

Name: {name}
Email: {email}

Message:
{message_body}

Regards,
Website Notification System
"""

        try:
            mail.send(msg)
            current_app.logger.info(
                f"Feedback email sent successfully from {email}"
            )
            flash("Your message has been sent successfully!")
        except Exception:
            current_app.logger.error(
                f"Feedback email failed to send from {email}",
                exc_info=True
            )
            flash("Message saved, but email could not be sent.")

        return redirect(url_for('contact_auth.contact'))

    return render_template('contact.html')
