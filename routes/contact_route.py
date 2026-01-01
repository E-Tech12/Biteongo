from flask import Blueprint,redirect,render_template,request,url_for,flash
from models import Feedback
from flask_mail import Message
from extensions import mail,db
contact_auth = Blueprint("contact_auth",__name__)

@contact_auth.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message_body = request.form.get('message')

        if not name or not email or not message_body:
            flash("Please fill out all fields.")  
            return redirect(url_for('contact'))

        feedback = Feedback(name=name, email=email, message=message_body)
        db.session.add(feedback)
        db.session.commit()

        msg = Message(
            subject=f"New Feedback from {name}",
            recipients=['cyberdev203@gmail.com']  
        )

        msg.body = f"""\
Hello,

You have received a new message from your Eatery website (BITE ON GO).

Here are the details:

Name: {name}
Email: {email}

Message:
{message_body}

Please follow up with the user as necessary.

Best regards,
Your Website Notification System
"""

        try:
            mail.send(msg)
            flash("Your message has been sent successfully!")  
        except Exception as e:
            print(e)
            flash("Message saved, but email could not be sent.")  

        return redirect(url_for('contact_auth.contact'))

    return render_template('contact.html') 