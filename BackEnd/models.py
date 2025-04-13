from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    records = db.relationship('DataRecord', backref='user', lazy=True)
    progress = db.relationship('UserProgress', backref='user', lazy=True, uselist=False)  # Один к одному
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_token(self):
        return create_access_token(identity=self.id)

class DataRecord(db.Model):
    __tablename__ = 'data_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    data_key = db.Column(db.String(80), nullable=False)
    data_value = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'data_key', name='unique_user_data_key'),
    )

class UserProgress(db.Model):
    __tablename__ = 'user_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)  # Один к одному
    streak = db.Column(db.Integer, default=0)
    unit = db.Column(db.Integer, default=0)
    lesson = db.Column(db.Integer, default=0)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', name='unique_user_progress'),
    )