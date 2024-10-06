from app import db
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(6), nullable=False)

    def __repr__(self):
        return f'{self.username}{self.password}{self.role}'
    
    def get_id(self):
        return self.uid

class Products(db.Model, UserMixin):
    __tablename__ = 'products'

    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'pid': self.pid,
            'name': self.name,
            'category': self.category,
            'price': self.price
        }
    
    def get_id(self):
        return self.pid

    def __repr__(self):
        return f'{self.name}{self.category}{self.price}'