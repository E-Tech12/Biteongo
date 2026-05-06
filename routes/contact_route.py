from flask import Blueprint, render_template, request, flash, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

contact_auth = Blueprint('contact_auth', __name__)

@contact_auth.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Validate inputs
        if not name or not email or not message:
            flash('Please fill in all fields', 'error')
            return redirect(url_for('contact_auth.contact'))
        
        # Send email to YOUR email address
        try:
            # Email configuration
            YOUR_EMAIL = "cyberdev203@gmail.com"
            YOUR_EMAIL_PASSWORD = "gvje rctp ycmv nqdd"
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # === HTML EMAIL FOR ADMIN/YOU ===
            msg = MIMEMultipart('alternative')
            msg['From'] = YOUR_EMAIL
            msg['To'] = YOUR_EMAIL
            msg['Subject'] = f"📧 New Contact Message from {name}"
            
            # HTML version for admin email
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background: white;
                        border-radius: 15px;
                        overflow: hidden;
                        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
                    }}
                    .header {{
                        background: linear-gradient(135deg, #f97316, #ea580c);
                        color: white;
                        padding: 30px;
                        text-align: center;
                    }}
                    .header h1 {{
                        margin: 0;
                        font-size: 28px;
                    }}
                    .header p {{
                        margin: 10px 0 0;
                        opacity: 0.9;
                    }}
                    .content {{
                        padding: 30px;
                    }}
                    .info-box {{
                        background: #fff7ed;
                        border-left: 4px solid #f97316;
                        padding: 15px;
                        margin-bottom: 20px;
                        border-radius: 8px;
                    }}
                    .info-box strong {{
                        color: #f97316;
                    }}
                    .message-box {{
                        background: #f9fafb;
                        padding: 20px;
                        border-radius: 10px;
                        margin: 20px 0;
                        border: 1px solid #e5e7eb;
                    }}
                    .message-box p {{
                        margin: 0;
                        line-height: 1.6;
                        color: #374151;
                    }}
                    .footer {{
                        background: #1f2937;
                        color: #9ca3af;
                        padding: 20px;
                        text-align: center;
                        font-size: 12px;
                    }}
                    .badge {{
                        display: inline-block;
                        background: #f97316;
                        color: white;
                        padding: 5px 12px;
                        border-radius: 20px;
                        font-size: 12px;
                        margin-top: 10px;
                    }}
                    .emoji {{
                        font-size: 24px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <div class="emoji">🍔🍕</div>
                        <h1>New Contact Form Message</h1>
                        <p>BiteOnGo Customer Inquiry</p>
                    </div>
                    <div class="content">
                        <div class="info-box">
                            <strong>📝 Customer Details:</strong><br><br>
                            <strong>Name:</strong> {name}<br>
                            <strong>Email:</strong> {email}<br>
                            <strong>Date:</strong> {current_time}
                        </div>
                        
                        <div class="message-box">
                            <strong>💬 Message:</strong><br><br>
                            <p>"{message}"</p>
                        </div>
                        
                        <div class="badge">
                            ⚡ Action Required
                        </div>
                    </div>
                    <div class="footer">
                        <p>© 2025 BiteOnGo - Delicious Food Delivered Fast</p>
                        <p>This message was sent from your website contact form</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Plain text version as fallback
            text_body = f"""
            NEW CONTACT FORM MESSAGE
            =========================
            
            Customer Details:
            Name: {name}
            Email: {email}
            Date: {current_time}
            
            Message:
            "{message}"
            
            =========================
            Sent from BiteOnGo Contact Form
            """
            
            msg.attach(MIMEText(text_body, 'plain'))
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email to admin
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(YOUR_EMAIL, YOUR_EMAIL_PASSWORD)
                server.send_message(msg)
            
            # === HTML AUTO-REPLY TO USER ===
            auto_reply = MIMEMultipart('alternative')
            auto_reply['From'] = YOUR_EMAIL
            auto_reply['To'] = email
            auto_reply['Subject'] = "✅ Thank you for contacting BiteOnGo!"
            
            # HTML version for user
            user_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 550px;
                        margin: 0 auto;
                        background: white;
                        border-radius: 15px;
                        overflow: hidden;
                        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
                    }}
                    .header {{
                        background: linear-gradient(135deg, #f97316, #ea580c);
                        color: white;
                        padding: 30px;
                        text-align: center;
                    }}
                    .header h1 {{
                        margin: 0;
                        font-size: 24px;
                    }}
                    .content {{
                        padding: 30px;
                    }}
                    .thank-you {{
                        text-align: center;
                        margin-bottom: 20px;
                    }}
                    .thank-you .emoji {{
                        font-size: 50px;
                    }}
                    .message-copy {{
                        background: #f9fafb;
                        padding: 20px;
                        border-radius: 10px;
                        margin: 20px 0;
                        border-left: 4px solid #f97316;
                    }}
                    .message-copy p {{
                        margin: 0;
                        line-height: 1.6;
                        color: #374151;
                        font-style: italic;
                    }}
                    .info {{
                        background: #f0fdf4;
                        padding: 15px;
                        border-radius: 8px;
                        margin: 20px 0;
                        text-align: center;
                    }}
                    .footer {{
                        background: #1f2937;
                        color: #9ca3af;
                        padding: 20px;
                        text-align: center;
                        font-size: 12px;
                    }}
                    .button {{
                        display: inline-block;
                        background: #f97316;
                        color: white;
                        padding: 10px 25px;
                        border-radius: 25px;
                        text-decoration: none;
                        margin-top: 15px;
                    }}
                    .social-icons {{
                        margin-top: 15px;
                    }}
                    .social-icons a {{
                        color: #f97316;
                        text-decoration: none;
                        margin: 0 10px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <div class="emoji">🍔🍕</div>
                        <h1>Thank You for Contacting Us!</h1>
                    </div>
                    <div class="content">
                        <div class="thank-you">
                            <div class="emoji">🙏</div>
                            <h3>Hello {name}!</h3>
                        </div>
                        
                        <p>We have received your message and our customer support team will get back to you within <strong>24-48 hours</strong>.</p>
                        
                        <div class="message-copy">
                            <strong>📝 Your Message:</strong><br><br>
                            <p>"{message}"</p>
                        </div>
                        
                        <div class="info">
                            <strong>💡 Did you know?</strong><br>
                            You can also reach us via WhatsApp at <strong>+234 9011499918</strong> for faster response!
                        </div>
                        
                        <div style="text-align: center;">
                            <a href="https://biteongo.onrender.com" class="button">🍽️ Browse Our Menu</a>
                        </div>
                        
                        <div class="social-icons" style="text-align: center;">
                            <p>Follow us for updates:</p>
                            <a href="#">📘 Facebook</a> | 
                            <a href="#">📸 Instagram</a> | 
                            <a href="#">🐦 Twitter</a>
                        </div>
                    </div>
                    <div class="footer">
                        <p>© 2025 BiteOnGo - Delicious Food Delivered Fast</p>
                        <p>12, Agbede FUNAAB, Abeokuta, Ogun State</p>
                        <p>This is an automated response, please do not reply directly to this email.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Plain text fallback for user
            user_text = f"""
            Thank you for contacting BiteOnGo!
            
            Hello {name},
            
            We have received your message and will get back to you within 24-48 hours.
            
            Your message:
            "{message}"
            
            You can also reach us via WhatsApp at +234 9011499918 for faster response!
            
            Browse our menu: https://biteongo.onrender.com
            
            Follow us:
            Facebook | Instagram | Twitter
            
            © 2025 BiteOnGo - Delicious Food Delivered Fast
            """
            
            auto_reply.attach(MIMEText(user_text, 'plain'))
            auto_reply.attach(MIMEText(user_html, 'html'))
            
            # Send auto-reply to user
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(YOUR_EMAIL, YOUR_EMAIL_PASSWORD)
                server.send_message(auto_reply)
            
            flash('✓ Thank you! Your message has been sent successfully. We will get back to you soon!', 'success')
            
        except Exception as e:
            print(f"Error: {e}")
            flash('✗ Sorry, there was an error sending your message. Please try again later.', 'error')
        
        return redirect(url_for('contact_auth.contact'))
    
    return render_template('contact.html')