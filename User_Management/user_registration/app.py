import random
import re
import string
from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import flask_sqlalchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config.from_object('config.Config')
db = flask_sqlalchemy.SQLAlchemy(app)
mail = Mail(app)

# Models
from models import User, Token

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if not re.match(r'^[a-zA-Z0-9_.]{3,20}$', username):
            flash('Invalid username. Must be 3-20 characters and can include alphanumeric characters, underscores, and periods.')
            return redirect(url_for('register'))

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            flash('Invalid email address.')
            return redirect(url_for('register'))

        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            flash('Password must be at least 8 characters long, include at least one uppercase letter, one lowercase letter, one number, and one special character.')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.')
            return redirect(url_for('register'))

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already registered.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(username=username, password_hash=hashed_password, email=email, is_verified=False)
        db.session.add(new_user)
        db.session.commit()

        token = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
        expiration = datetime.utcnow() + timedelta(hours=1)
        new_token = Token(user_id=new_user.id, token=token, expires_at=expiration)
        db.session.add(new_token)
        db.session.commit()

        verification_link = url_for('verify_email', token=token, _external=True)
        msg = Message('Email Verification', recipients=[email])
        msg.body = f'Please click the following link to verify your email: {verification_link}'
        mail.send(msg)

        flash('Registration successful! Please check your email to verify your account.')
        return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/verify/<token>')
def verify_email(token):
    token_record = Token.query.filter_by(token=token).first()
    if not token_record or token_record.expires_at < datetime.utcnow():
        flash('Invalid or expired token.')
        return redirect(url_for('register'))

    user = User.query.get(token_record.user_id)
    user.is_verified = True
    db.session.commit()

    db.session.delete(token_record)
    db.session.commit()

    flash('Email verified successfully! You can now log in.')
    return redirect(url_for('register'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
