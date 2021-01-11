import os
import requests
 
# Flask imports
from flask import Flask, Response, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy

# Email services
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sparkpost import SparkPost

sp = SparkPost(os.environ.get('SPARKPOST_API_KEY'))
sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
DB_URL = os.environ['POSTGRES_URL']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Email postgres table
class Email(db.Model):
    __tablename__ = 'email'

    email_id = db.Column(db.Integer, primary_key=True)
    sender_name = db.Column(db.String, nullable=False)
    sender_email = db.Column(db.String, nullable=False)
    receiver = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=True)
    body = db.Column(db.String, nullable=False)

    # Here I would usually use an object serializer such as marshmallow (https://marshmallow.readthedocs.io/en/stable/)
    # For simplicity's sake I've made __init__() and to_json() manually
    def __init__(self, sender_name, sender_email, receiver, subject, body):
        self.sender_name = sender_name
        self.sender_email = sender_email
        self.receiver = receiver
        self.subject = subject
        self.body = body

    def to_json(self):
        return {
            'email_id': self.email_id,
            'sender_name': self.sender_name,
            'sender_email': self.sender_email,
            'receiver': self.receiver,
            'subject': self.subject,
            'body': self.body
        }

db.create_all()

SENDER_NAME = 'Torben Albert-Lindqvist'
SENDER_EMAIL = 'mail@torbenal.dk'
SENDER = f'"{SENDER_NAME}" <{SENDER_EMAIL}>'

# Email services in order of priority
SERVICES = {
    'SendGrid': lambda recipient, subject, body: (
        sg.send(Mail(
            from_email=SENDER,
            to_emails=recipient,
            subject=subject,
            html_content=body
        ))
    ),
    'SparkPost': lambda recipient, subject, body: (
        sp.transmissions.send(
            recipients=[recipient],
            html=body,
            from_email=SENDER,
            subject=subject
        )
    )
}

# Endpoint for GET emails
@app.route("/api/emails", methods=['GET'])
def get_emails():
    emails = [e.to_json() for e in Email.query.all()]
    emails.reverse()
    return jsonify(emails), 200

# Endpoint POST email
@app.route("/api/email", methods=['POST'])
def send_email():
    data = request.get_json()

    # Create row in database
    email_obj = Email(
        sender_name=SENDER_NAME,
        sender_email=SENDER_EMAIL,
        receiver=data['recipient'],
        subject=data['subject'],
        body=data['body']
    )
    db.session.add(email_obj)
    db.session.flush()

    # Try email services in their priortity order
    success = False
    for name, method in SERVICES.items():
        try:
            response = method(
                data['recipient'], 
                data['subject'], 
                data['body']
            )
            success = True
            break
        except Exception as e:
            print(f'Service {name} failed. Falling back to alternative service.')

    if success:
        # Commit changes in the database and return success code
        db.session.commit()
        return '', 200
    else: abort(400) 

if __name__ == "__main__":
    app.run(debug=True, port=5000)