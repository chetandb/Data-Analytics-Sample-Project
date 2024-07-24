import random
import string
import datetime

import pytest
from werkzeug.security import generate_password_hash

from app import app, db
from models import User, Token


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['MAIL_SUPPRESS_SEND'] = True  # Prevent actual email sending during tests
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def new_user():
    hashed_password = generate_password_hash('testpassword', method='pbkdf2:sha256')
    user = User(username='testuser', password_hash=hashed_password, email='test@example.com', is_verified=False)
    db.session.add(user)
    db.session.commit()
    return user

def test_register_valid_data(client):
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'NewPassword1!',
        'email': 'newuser@example.com'
    })
    assert response.status_code == 302
    assert response.location == '/register'
    assert b'Registration successful! Please check your email to verify your account.' in response.data

    user = User.query.filter_by(username='newuser').first()
    assert user is not None
    assert user.is_verified is False
    token = Token.query.filter_by(user_id=user.id).first()
    assert token is not None

def test_register_invalid_username(client):
    response = client.post('/register', data={
        'username': 'a',  # Invalid username
        'password': 'ValidPassword1!',
        'email': 'valid@example.com'
    })
    assert response.status_code == 302
    assert response.location == '/register'
    assert b'Invalid username. Must be 3-20 characters and can include alphanumeric characters, underscores, and periods.' in response.data

def test_register_invalid_email(client):
    response = client.post('/register', data={
        'username': 'validuser',
        'password': 'ValidPassword1!',
        'email': 'invalid-email'  # Invalid email
    })
    assert response.status_code == 302
    assert response.location == '/register'
    assert b'Invalid email address.' in response.data

def test_register_existing_username(client):
    client.post('/register', data={
        'username': 'existinguser',
        'password': 'ValidPassword1!',
        'email': 'existinguser@example.com'
    })

    response = client.post('/register', data={
        'username': 'existinguser',
        'password': 'AnotherPassword1!',
        'email': 'newemail@example.com'
    })
    assert response.status_code == 302
    assert response.location == '/register'
    assert b'Username already exists.' in response.data

def test_register_existing_email(client):
    client.post('/register', data={
        'username': 'anotheruser',
        'password': 'ValidPassword1!',
        'email': 'duplicate@example.com'
    })

    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'AnotherPassword1!',
        'email': 'duplicate@example.com'
    })
    assert response.status_code == 302
    assert response.location == '/register'
    assert b'Email already registered.' in response.data

def test_verify_email_valid_token(client, new_user):
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    new_token = Token(user_id=new_user.id, token=token, expires_at=expiration)
    db.session.add(new_token)
    db.session.commit()

    response = client.get(f'/verify/{token}')
    assert response.status_code == 302
    assert response.location == '/register'
    assert b'Email verified successfully! You can now log in.' in response.data

    user = User.query.get(new_user.id)
    assert user.is_verified is True
    token_record = Token.query.filter_by(token=token).first()
    assert token_record is None

def test_verify_email_invalid_token(client):
    response = client.get('/verify/invalidtoken')
    assert response.status_code == 302
    assert response.location == '/register'
    assert b'Invalid or expired token.' in response.data
