from flask import render_template, request
from models import Products

def register_routes(app, db):
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/list_products')
    def list_products():
        products = Products.query.all()
        return render_template('list_products.html', products=products)
    
    @app.route('/edit_products', methods=['GET', 'POST'])
    def edit_products():
        if request.method == 'GET':
            products = Products.query.all()
            return render_template('edit_products.html', products=products)
        elif request.method == 'POST':
            name = request.form['name']
            category = request.form['category']
            price = request.form['price']

            products_var = Products(name=name, category=category, price=price)
            db.session.add(products_var)
            db.session.commit()

            products = Products.query.all()
            return render_template('edit_products.html', products=products)