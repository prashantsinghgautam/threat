from flask import Flask, render_template, request, redirect, url_for, session
import smtplib
from email.mime.text import MIMEText
import time

app = Flask(__name__)
app.secret_key = 'some_secure_random_key'  # For sessions

ignore_requests = False

@app.route('/')
def input_form():
    return render_template('index.html')

@app.route('/monitor', methods=['POST'])
def process_form():
    global ignore_requests
    if not ignore_requests:
        ignore_requests = True
        print("Ignoring requests for the next 5 minutes.")
        time.sleep(300)  # 300 seconds = 5 minutes
        ignore_requests = False
        print("Now accepting requests.")

        data = request.form
        session['user_data'] = data  # Store in session
        return redirect(url_for('monitor'))
    else:
        return "Requests are currently being ignored. Please try again later.", 403

@app.route('/monitor')
def monitoring():
    if 'user_data' in session:
        user_data = session['user_data']
        return render_template('monitor.html') 
    else:
        return redirect(url_for('input_form')) 

@app.route('/threat', methods=['POST'])
def handle_threat():
    print("Threat detected!")  
    if 'user_data' in session:
        user_data = session['user_data']

        # Extract emergency contacts
        emergency_contact_1 = user_data.get('emergency_email_1', '')
        emergency_contact_2 = user_data.get('emergency_email_2', '')

        # Build email message
        subject = "Accident Alert!"
        body = f"An accident may have occurred involving {user_data['name']}.\n\nPlease see their provided information for further details: {user_data}"

        # Send the email
        recipients = [emergency_contact_1, emergency_contact_2]
        send_email_alert(recipients, subject, body)

    return "Alert received", 200  

def send_email_alert(recipients, subject, body):
    # Replace with your actual SMTP settings
    smtp_server = 'smtp.gmail.com' 
    smtp_port = 587  
    username = 'psg.freel@gmail.com'  
    password = 'rtra xhlx disw yube' 

    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = username
    message['To'] = ', '.join(recipients) 

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls() 
        server.login(username, password)
        server.sendmail(username, recipients, message.as_string())

if __name__ == '__main__':
    app.run(debug=True)
