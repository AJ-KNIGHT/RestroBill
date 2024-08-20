from flask import render_template, request, jsonify, flash, redirect, url_for
from models import Products, Users
import json

def register_routes(app, db):
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/list_products')
    def list_products():
        products = Products.query.all()
        return render_template('list_products.html', products=products)
    
    @app.route('/list_products_json')
    def list_products_json():
        # products = Products.query.all()
        # print("")
        # print(type(products))
        # print("\n", products)

        # # return jsonify({"product_list": products})
        # # return products
        return render_template('list_products_json.html')
    
    @app.route('/api/products', methods=['GET'])
    def get_products():
        products = Products.query.all()
        products_list = [product.to_dict() for product in products]
        return jsonify(products_list)

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
        

    #  flask_crud
    @app.route('/users')
    def users_index():
        all_data = Users.query.all()

        return render_template('user-mng.html')

    @app.route('/users/get_users')
    def get_users():
        all_users = Users.query.all()
        users_list = [{'uid': user.uid, 'username': user.username} for user in all_users]
        return jsonify(users_list)
    
    @app.route('/users/insert', methods = ['POST'])
    def insert():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            role = 'user'

            my_data = Users(username, password, role)
            db.session.add(my_data)
            db.session.commit()

            flash('Employee inserted successfully')

            return redirect(url_for('users_index'))

    @app.route('/users/update', methods = ['GET', 'POST'])
    def update():

        if request.method == 'POST':
            my_data = Users.query.get(request.form.get('id'))

            my_data.username = request.form['username']
            my_data.password = request.form['password']

            db.session.commit()
            flash('Employee updated successfully')

            return redirect(url_for('users_index'))


    @app.route('/delete/<id>/', methods = ['GET', 'POST'])
    def delete(id):
        my_data = Users.query.get(id)
        db.session.delete(my_data)
        db.session.commit()

        flash('Employee deleted successfully')

        return redirect(url_for('users_index'))

    # live search with list

    # list_items = ["Apple", "Avocado", "Banana", "Blueberry",
    #               "Blackberry", "Cherry", "Coconut", "Orange", "Olive"]

    # @app.route('/search')
    # def product_search():
    #     text = request.args['searchText']
    #     result = [item for item in list_items if str(text).lower() in item.lower()]
    #     # return json.dumps({"results": result})
    #     return jsonify(results=result)

    @app.route('/search-page')
    def product_search_page():
        return render_template('product_search.html')
    @app.route('/search-page/main')
    def product_search_main():
        return render_template('product_search_main.html')
    
    @app.route('/search')
    def product_search():
        products = Products.query.all()
        products_list = [product.to_dict() for product in products]

        # text = request.args['searchText']
        # product_names = [n.name for n in products_list]
        # print(names)
        # result = [item for item in product_names if str(text).lower() in item.lower()]
        # result = [item for item in products_list if str(text).lower() in item['name'].lower()]
        # # print(result)
        # # return ('', 204)

        text = request.args.get('searchText', '').lower()
        result = [item for item in products_list if text in item['name'].lower()]
        return jsonify(results=result)




        # # return json.dumps({"results": result})
        # return jsonify(results=result)

    
