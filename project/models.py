"""Database models."""
# from app import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from project.app import db

class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),nullable=False,unique=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(200),primary_key=False,unique=False,nullable=False)
    isAdmin = db.Column(db.Boolean)
    created_on = db.Column(db.DateTime,index=False,unique=False,nullable=True)
    last_login = db.Column(db.DateTime,index=False,unique=False,nullable=True)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

