from app import db
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String)

    def __repr__(self):
        return f'{self.uid}{self.username}{self.role}'
    
    def get_id(self):
        return self.uid
    