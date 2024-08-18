from app import db

class Products(db.Model):
    __tablename__ = 'products'

    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)


    def to_dict(self):
        return {
            'pid': self.pid,
            'name': self.name,
            'category': self.category,
            'price': self.price
        }

    def __repr__(self):
        return f'{self.pid} {self.name} {self.category} {self.price}'


class Users(db.Model):
    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String(6))

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role