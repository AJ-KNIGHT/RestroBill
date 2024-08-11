from app import db

class Products(db.Model):
    __tablename__ = 'products'

    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return f'{self.pid}{self.name}{self.category}{self.price}'