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
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone