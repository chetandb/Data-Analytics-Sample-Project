import pytest
from apps import app, db, User, Role, UserRole, ResetToken
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import secrets
import os

# Configure the app for testing
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['MAIL_SUPPRESS_SEND'] = True  # Disable email sending during tests
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def sample_user(client):
    hashed_password = generate_password_hash('TestPassword123!')
    user = User(username='testuser', email='test@example.com', password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()
    return user

def test_register(client):
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'Password1!',
        'password_confirm': 'Password1!'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert User.query.filter_by(username='newuser').first() is not None

def test_register_password_mismatch(client):
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'Password1!',
        'password_confirm': 'DifferentPassword1!'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_login_success(client, sample_user):
    response = client.post('/login', data={
        'username_or_email': 'testuser',
        'password': 'TestPassword123!'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_login_failure(client):
    response = client.post('/login', data={
        'username_or_email': 'testuser',
        'password': 'WrongPassword'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_manage_roles(client):
    client.post('/manage_roles', data={
        'role_name': 'admin',
        'description': 'Administrator role'
    }, follow_redirects=True)
    role = Role.query.filter_by(role_name='admin').first()
    assert role is not None
    assert role.description == 'Administrator role'

def test_assign_role(client, sample_user):
    role = Role(role_name='admin', description='Administrator role')
    db.session.add(role)
    db.session.commit()
    client.post('/assign_role', data={
        'user_id': sample_user.user_id,
        'role_id': role.role_id
    }, follow_redirects=True)
    user_role = UserRole.query.filter_by(user_id=sample_user.user_id, role_id=role.role_id).first()
    assert user_role is not None

def test_forgot_password(client, sample_user):
    response = client.post('/forgot_password', data={
        'email': 'test@example.com'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert ResetToken.query.filter_by(user_id=sample_user.user_id).count() == 1

def test_reset_password(client, sample_user):
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(minutes=30)
    reset_token = ResetToken(user_id=sample_user.user_id, token=token, expires_at=expires_at)
    db.session.add(reset_token)
    db.session.commit()

    response = client.post(f'/reset_password/{token}', data={
        'password': 'NewPassword1!',
        'password_confirm': 'NewPassword1!'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert check_password_hash(sample_user.password_hash, 'NewPassword1!') is True

def test_reset_password_invalid_token(client):
    response = client.post('/reset_password/invalidtoken', data={
        'password': 'NewPassword1!',
        'password_confirm': 'NewPassword1!'
    }, follow_redirects=True)
    assert response.status_code == 200
