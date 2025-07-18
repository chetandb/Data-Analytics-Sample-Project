import pytest
from app import db, app
from models import User, Token
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta, timezone

@pytest.fixture
def client():
    app.config['TESTING'] = True
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

def test_user_creation(client):
    user = User(username='testuser', password_hash='hashedpassword', email='test@example.com')
    db.session.add(user)
    db.session.commit()

    retrieved_user = User.query.filter_by(username='testuser').first()
    assert retrieved_user is not None
    assert retrieved_user.email == 'test@example.com'
    assert retrieved_user.password_hash == 'hashedpassword'
    assert retrieved_user.is_verified is False

def test_token_creation(client, new_user):
    token_str = 'testtoken1234567890'
    expiration = datetime.now(timezone.utc) + timedelta(hours=1)
    token = Token(user_id=new_user.id, token=token_str, expires_at=expiration)
    db.session.add(token)
    db.session.commit()

    retrieved_token = Token.query.filter_by(token=token_str).first()
    assert retrieved_token is not None
    assert retrieved_token.user_id == new_user.id
    assert retrieved_token.expires_at == expiration

def test_user_token_relationship(client, new_user):
    token_str = 'testtoken1234567890'
    expiration = datetime.now(timezone.utc) + timedelta(hours=1)
    token = Token(user_id=new_user.id, token=token_str, expires_at=expiration)
    db.session.add(token)
    db.session.commit()

    user = User.query.get(new_user.id)
    assert len(user.tokens) == 1
    assert user.tokens[0].token == token_str

def test_user_unique_constraints(client):
    user1 = User(username='uniqueuser', password_hash='hashedpassword1', email='unique@example.com')
    db.session.add(user1)
    db.session.commit()

    with pytest.raises(Exception) as excinfo:
        user2 = User(username='uniqueuser', password_hash='hashedpassword2', email='different@example.com')
        db.session.add(user2)
        db.session.commit()

    assert 'UNIQUE constraint failed' in str(excinfo.value)

def test_token_unique_constraints(client, new_user):
    token_str = 'uniquetoken123'
    expiration = datetime.now(timezone.utc) + timedelta(hours=1)
    token1 = Token(user_id=new_user.id, token=token_str, expires_at=expiration)
    db.session.add(token1)
    db.session.commit()

    with pytest.raises(Exception) as excinfo:
        token2 = Token(user_id=new_user.id, token=token_str, expires_at=expiration)
        db.session.add(token2)
        db.session.commit()

    assert 'UNIQUE constraint failed' in str(excinfo.value)

def test_user_timestamps(client):
    user = User(username='timestampuser', password_hash='hashedpassword', email='timestamp@example.com')
    db.session.add(user)
    db.session.commit()

    assert user.created_at is not None
    assert user.updated_at is not None

def test_token_timestamps(client, new_user):
    expiration = datetime.now(timezone.utc) + timedelta(hours=1)
    token = Token(user_id=new_user.id, token='timestampToken123', expires_at=expiration)
    db.session.add(token)
    db.session.commit()

    assert token.created_at is not None
