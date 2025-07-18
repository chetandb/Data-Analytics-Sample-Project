from flask import Flask, request, redirect, url_for, flash, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Set a default SECRET_KEY for Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'noreply@example.com'
if app.config.get('TESTING'):
    app.config['MAIL_SUPPRESS_SEND'] = True

db = SQLAlchemy(app)
mail = Mail(app)

# Models
# Ensure the user_roles table is defined before referencing it in the User class
user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.role_id'), primary_key=True)
)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    failed_login_attempts = db.Column(db.Integer, default=0)
    account_locked_until = db.Column(db.DateTime, nullable=True)
    roles = db.relationship('Role', secondary=user_roles, backref='users')
    reset_tokens = db.relationship('ResetToken', backref='user', lazy=True)

class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)

class Permission(db.Model):
    permission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    permission_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)

class UserRole(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), primary_key=True)

class RolePermission(db.Model):
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.permission_id'), primary_key=True)

class ResetToken(db.Model):
    token_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc) + timedelta(hours=1))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

# Create Database
@app.before_request
def create_tables():
    db.create_all()

# Routes

# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        if password != password_confirm:
            flash('Passwords do not match.')
            return redirect(url_for('register'))
        elif len(password) < 8 or not any(c.isupper() for c in password) or not any(c.islower() for c in password) or not any(c.isdigit() for c in password) or not any(c in "!@#$%^&*()_+" for c in password):
            flash('Password does not meet complexity requirements.')
            return redirect(url_for('register'))
        elif User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
            flash('Email or Username already exists.')
            return redirect(url_for('register'))
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please check your email to verify your account.')
            return redirect(url_for('login'))

    # Correct the path to the register.html template
    return render_template('register.html')

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']
        user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()

        if user and check_password_hash(user.password_hash, password):
            if user.is_verified:
                session['user_id'] = user.user_id
                flash('Login successful.')
                return redirect(url_for('dashboard'))
            else:
                flash('Account not verified.')
                return redirect(url_for('login'))
        else:
            flash('Invalid username/email or password.')
            return redirect(url_for('login'))

    return render_template('login.html')

# Role Management
@app.route('/manage_roles', methods=['GET', 'POST'])
def manage_roles():
    if request.method == 'POST':
        role_name = request.form['role_name']
        description = request.form['description']
        if Role.query.filter_by(role_name=role_name).first():
            flash('Role already exists.')
        else:
            new_role = Role(role_name=role_name, description=description)
            db.session.add(new_role)
            db.session.commit()
            flash('Role created successfully.')

    roles = Role.query.all()
    return render_template('manage_roles.html', roles=roles)

@app.route('/assign_role', methods=['POST'])
def assign_role():
    user_id = request.form['user_id']
    role_id = request.form['role_id']
    user_role = UserRole.query.filter_by(user_id=user_id, role_id=role_id).first()

    if not user_role:
        new_user_role = UserRole(user_id=user_id, role_id=role_id)
        db.session.add(new_user_role)
        db.session.commit()
        flash('Role assigned successfully.')
    else:
        flash('Role already assigned to the user.')

    return redirect(url_for('manage_roles'))

# Password Recovery
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            token = secrets.token_urlsafe(32)
            expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)
            reset_token = ResetToken(user_id=user.user_id, token=token, expires_at=expires_at)
            db.session.add(reset_token)
            db.session.commit()

            reset_link = url_for('reset_password', token=token, _external=True)
            msg = Message('Password Reset Request', sender=os.getenv('MAIL_USERNAME'), recipients=[email])
            msg.body = f'Click the link to reset your password: {reset_link}'
            # Suppress email sending in test mode
            if not app.config.get('TESTING', False):
                mail.send(msg)
            flash('Password reset link sent to your email address.')
            return redirect(url_for('forgot_password'))
        else:
            flash('Email address not found.')

    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    reset_token = ResetToken.query.filter_by(token=token).first()
    # Always use timezone-aware UTC for comparison
    now_utc = datetime.now(timezone.utc)
    if not reset_token:
        flash('Reset link is invalid or expired.')
        return redirect(url_for('forgot_password'))
    expires_at = reset_token.expires_at
    if expires_at and expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at <= now_utc:
        flash('Reset link is invalid or expired.')
        return redirect(url_for('forgot_password'))
    if request.method == 'POST':
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        if password != password_confirm:
            flash('Passwords do not match.')
        elif len(password) < 8 or not any(c.isupper() for c in password) or not any(c.islower() for c in password) or not any(c.isdigit() for c in password) or not any(c in "!@#$%^&*()_+" for c in password):
            flash('Password does not meet complexity requirements.')
        else:
            user = User.query.get(reset_token.user_id)
            user.password_hash = generate_password_hash(password)
            db.session.commit()
            db.session.delete(reset_token)
            db.session.commit()
            flash('Password has been updated successfully.')
            return redirect(url_for('login'))
    return render_template('reset_password.html', token=token)

@app.route('/dashboard')
def dashboard():
    return 'Dashboard (Implement your dashboard here)'

if __name__ == '__main__':
    app.run(debug=True)
