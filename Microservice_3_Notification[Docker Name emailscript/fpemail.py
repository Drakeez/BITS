#!/usr/bin/env python
# coding: utf-8

# In[1]:


import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, jsonify

app = Flask(__name__)
@app.route('/email', methods=['POST'])

def trigger_email():
    # Set up SES SMTP credentials
    smtp_server = 'email-smtp.eu-north-1.amazonaws.com'
    smtp_port = 587
    username = 'AKIAXDRP24V7S46GPFPN'
    password = 'BC27BuJeQtFF0pfdx8eorsQdOfKee8agaBCiMfxJWfJ7'
    
    data = request.json
    recipient_name = data['username']
    recipient_emailid = data['email']
    

    # Set up sender and recipient email addresses
    sender = '2022mt03551@wilp.bits-pilani.ac.in'
    #recipient = recipient

    # Compose the email
    subject = 'Test Email'
    body = 'This is a successful user registration email. Thankyou for registering with us '+ recipient_name
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient_emailid

    try:
    # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(sender, recipient_emailid, msg.as_string())

        print('Email sent successfully!')
        return jsonify({'status': 'success', 'message': 'Email sent successfully'})
    except Exception as e:
        print(f'Error sending email: {e}')
        return jsonify({'status': 'error', 'message': 'Error sending email'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

    
    

