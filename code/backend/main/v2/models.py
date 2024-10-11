from app import db
from flask_login import UserMixin


# Active Data Database Models

class Users(db.Model, UserMixin):
    __bind_key__ = 'active_data'  # This specifies the database to use
    __tablename__ = "users"

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(6), nullable=False)

    def __repr__(self):
        return f"{self.username}{self.password}{self.role}"

    def get_id(self):
        return self.uid

class Products(db.Model, UserMixin):
    __bind_key__ = 'active_data'
    __tablename__ = "products"

    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "pid": self.pid,
            "name": self.name,
            "category": self.category,
            "price": self.price,
        }

    def get_id(self):
        return self.pid

    def __repr__(self):
        return f"{self.name}{self.category}{self.price}"


# Current Year Data Database Models
class Bill(db.Model):
    __bind_key__ = 'current_year_data'
    __tablename__ = "bills"

    bill_id = db.Column(db.Integer, primary_key=True)
    bill_date = db.Column(db.DateTime, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    bill_items = db.Column(db.JSON, nullable=False)  # Dictionary of items and their prices
    bill_payment = db.Column(db.JSON, nullable=False)  # Payment details
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Bill {self.bill_id} on {self.bill_date} by {self.username}"

class Sales(db.Model):
    __bind_key__ = 'current_year_data'
    __tablename__ = "sales"

    month = db.Column(db.String(10), primary_key=True)  # Name of the month
    total_sales = db.Column(db.Float, nullable=False)  # Total sales amount for the month
    top_products = db.Column(db.JSON, nullable=False)  # JSON of top 5 most sold products

    def __repr__(self):
        return f"Sales for {self.month}: Total Sales - {self.total_sales}, Top Products - {self.top_products}"


# Archived Data Database Models
class ArchivedBill(db.Model):
    __bind_key__ = 'archive_data'
    __tablename__ = "archived_bills"

    bill_id = db.Column(db.Integer, primary_key=True)
    bill_date = db.Column(db.DateTime, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    bill_items = db.Column(db.JSON, nullable=False)
    bill_payment = db.Column(db.JSON, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Archived Bill {self.bill_id} on {self.bill_date} by {self.username}"


class ArchivedSales(db.Model):
    __bind_key__ = 'archive_data'
    __tablename__ = "archived_sales"

    month = db.Column(db.String(10), primary_key=True)  # Name of the month
    total_sales = db.Column(db.Float, nullable=False)  # Total sales amount for the month
    top_products = db.Column(db.JSON, nullable=False)  # JSON of top 5 most sold products

    def __repr__(self):
        return f"Sales for {self.month}: Total Sales - {self.total_sales}, Top Products - {self.top_products}"
