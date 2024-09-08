from flask import render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_login import login_user, logout_user, current_user, login_required

from weasyprint import HTML

from models import Users, Products

def register_routes(app, db, bcrypt):

    @app.route('/', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            if 'username' in request.form.keys() and 'password' in request.form.keys():
                username = request.form['username']
                password = request.form['password']

                user = Users.query.filter_by(username=username).first()

                if user and bcrypt.check_password_hash(user.password, password):
                    login_user(user)
                    if user.role == 'admin':
                        return redirect(url_for('dashboard'))
                    elif user.role == 'user':
                        return redirect(url_for('billing'))
                else:
                    return "Authentication Error"
            else:
                return "form Error"
    
    @app.route('/logout/')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

# ---------------- billing page -----------------------

    # billing page
    # @app.route('/billig/<uid>')
    # @login_required
    # def billing(uid):
    #     if current_user.role == 'user':
    #         return 'Billing page'
    #     else:
    #         return "Access Denied"
        
    @app.route('/billing')
    @login_required
    def billing():
        if current_user.role == 'user':
            return render_template('billing.html', username=current_user.username)
        else:
            return "Access Denied"

    @app.route('/search')
    def product_search():
        products = Products.query.all()
        products_list = [product.to_dict() for product in products]
        text = request.args.get('searchText', '').lower()
        result = [item for item in products_list if text in item['name'].lower()]
        return jsonify(results=result)

        
    @app.route('/billing-test')
    @login_required
    def billing_test():
        if current_user.role == 'user':
            return render_template('billing.html', username=current_user.username)
        else:
            return "Access Denied"

    @app.route('/print-bill', methods=['POST'])
    @login_required
    def print_bill():
        if current_user.role == 'user':
            if request.is_json:

                # products = Products.query.all()
                cart = request.get_json()
                # print(cart_)
                # return ('print success', 205)
    
                total_amount = 0
                bill_details = []
                
                for si_no, item in cart.items():
                    pid = item['pid']
                    qty = item['qty']
                    
                    # Fetch product details from database
                    product = Products.query.get(pid) 
                    if product:
                        product_data = product.to_dict()
                        product_name = product_data['name']
                        product_price = product_data['price']
                        product_total = qty * product_price
                        
                        # Add product details to bill details
                        bill_details.append({
                            'name': product_name,
                            'qty': qty,
                            'price': product_price,
                            'total': product_total
                        })
                        
                        # Update the total amount
                        total_amount += product_total
                
                # Prepare the response with bill details and total amount
                # response = {
                #     'billDetails': bill_details,
                #     'totalAmount': total_amount
                # }
                # return jsonify(response)

                return jsonify({
                    'message': 'Bill generated successfully.',
                    'billDetails': bill_details  # Send back product details for printing
                })
    

            
            else:
                return ('', 401)
        else:
            return "Access Denied"

    # if request.is_json:

    #     if request.method == 'GET':
    #         seconds = time()
    #         return jsonify({'seconds': seconds})

    #     elif request.method == 'POST':
    #         card_text = json.loads(request.data)['text']        # .form or .json (not used form then use data)
    #         new_text = f"I got : {card_text}"
    #         return jsonify({'data': new_text})
        
    # return render_template('index.html')


# ai code:
    # @app.route('/print-bill', methods=['POST'])
    # @login_required
    # def print_cart():
    #     products = Products.query.all()
    #     products_list = [product.to_dict() for product in products]
    #     cart_data = request.get_json()  # Receive the cart data from the frontend
    #     # Process the cart data and generate the print content
    #     print_content = generate_print_content(cart_data)
    #     # Send the print content to the printer (using a library like PyPDF2 or reportlab)
    #     print_to_printer(print_content)
    #     return jsonify({'message': 'Print initiated successfully'})

    # def generate_print_content(cart_data):
    #     # Generate the print content based on the cart data
    #     # For example, create a formatted string with item details and total
    #     print_content = "**Your Order:**\n"
    #     for si_no, item_data in cart_data.items():
    #         print_content += f"- Item {si_no}: {item_data[0]} (Qty: {item_data[1]})\n"
    #     print_content += f"**Total:** ₹{calculate_total(cart_data)}"
    #     return print_content

    # def calculate_total(cart_data):
    #     total = 0
    #     for item_data in cart_data.values():
    #         total += int(item_data[1]) * int(item_data[0][1])  # Assuming item_data[0][1] is the price
    #     return total

    # def print_to_printer(print_content):
    #     # Replace this with your actual printing logic using a library like PyPDF2 or reportlab
    #     print(print_content)  # For testing, print to console
    #     # ... actual printing code ...


    @app.route('/bill')
    @login_required
    def bill():
        return render_template('bill.html')

    @app.route('/generate_pdf')
    @login_required
    def generate_pdf():

        # Render the HTML template
        rendered_html = render_template('bill.html')
        # Convert the rendered HTML to PDF using WeasyPrint
        # pdf = HTML(string=rendered_html).write_pdf()

        # save pdf
        HTML(string=rendered_html).write_pdf('./output.pdf')


        # Create a response object with the PDF
        # response = make_response(pdf)
        # response.headers['Content-Type'] = 'application/pdf'
        # response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

        # return response

        return "Bill pdf ready"
        

# ---------------- dashboard page -----------------------
    @app.route('/dashboard')
    @login_required
    def dashboard():
        if current_user.role == 'admin':
            return render_template('/dashboard/dashboard.html', username=current_user.username)
        else:
            return "Access Denied"

    # user management
    @app.route('/dashboard/user-management')
    @login_required
    def user_management():
        if current_user.role == 'admin':
            user_data = Users.query.all()
            return render_template('/dashboard/user_managment.html', username=current_user.username, users=user_data)
        else:
            return "Access Denied"
    
    @app.route('/user/insert', methods = ['POST'])
    @login_required
    def user_insert():
        if current_user.role == 'admin':
            if request.method == 'POST':
                if 'username' in request.form.keys() and 'password' in request.form.keys():
                    username = request.form['username']
                    password = request.form['password']
                    role = 'user'

                    hashed_password = bcrypt.generate_password_hash(password)

                    new_user_data = Users(username=username, password=hashed_password, role=role)
                    db.session.add(new_user_data)
                    db.session.commit()

                    flash('User inserted successfully')

                    return redirect(url_for('user_management'))
        else:
            return "Access Denied"
        
    @app.route('/user/update', methods = ['GET', 'POST'])
    @login_required
    def user_update():
        if current_user.role == 'admin':
            if request.method == 'POST':
                if 'username' in request.form.keys() and 'password' in request.form.keys():
                    data = Users.query.get(request.form.get('uid'))

                    if (request.form['username'].strip() != "" and request.form['username'].strip() != data.username):
                        data.username = request.form['username']

                    elif (request.form['password'].strip() != ""):
                        password = request.form['password']
                        hashed_password = bcrypt.generate_password_hash(password)
                        data.password = hashed_password

                    db.session.commit()

                    flash('User data updated successfully')
                    return redirect(url_for('user_management'))
        else:
            return "Access Denied"
    
    @app.route('/user/delete/<uid>/', methods = ['GET', 'POST'])
    @login_required
    def user_delete(uid):
        if current_user.role == 'admin':
            data = Users.query.get(uid)
            if data:
                if uid.strip() != "1" and data.role != "admin":
                    db.session.delete(data)
                    db.session.commit()
                    flash('User deleted successfully')
                    return redirect(url_for('user_management'))
                else:
                    return "Cannot delete admin user"
            else:
                return "User not found"
        else:
            return "Access Denied"


    # product management
    @app.route('/dashboard/product-management')
    @login_required
    def product_management():
        if current_user.role == 'admin':
            product_data = Products.query.all()
            return render_template('/dashboard/product_managment.html', username=current_user.username, products=product_data)
        else:
            return "Access Denied"
    
    @app.route('/product/insert', methods = ['POST'])
    @login_required
    def product_insert():
        if current_user.role == 'admin':
            if request.method == 'POST':
                if 'name' in request.form.keys() and 'category' in request.form.keys() and 'price' in request.form.keys():
                    name = request.form['name']
                    category = request.form['category']
                    price = float(request.form['price'])

                    new_product_data = Products(name=name, category=category, price=price)
                    db.session.add(new_product_data)
                    db.session.commit()

                    flash('Product inserted successfully')

                    return redirect(url_for('product_management'))
        else:
            return "Access Denied"
        
    @app.route('/product/update', methods = ['GET', 'POST'])
    @login_required
    def product_update():
        if current_user.role == 'admin':
            if request.method == 'POST':
                if 'name' in request.form.keys() and 'category' in request.form.keys() and 'price' in request.form.keys():
                    data = Products.query.get(request.form.get('pid'))

                    if (request.form['name'].strip() != "" and request.form['name'].strip() != data.name):
                        data.name = request.form['name']

                    elif (request.form['category'].strip() != "" and request.form['category'].strip() != data.category):
                        data.category = request.form['category']
                    
                    elif (request.form['price'] != 0 and float(request.form['price']) != data.price):
                        data.price = float(request.form['price'])

                    db.session.commit()

                    flash('Product data updated successfully')
                    return redirect(url_for('product_management'))
        else:
            return "Access Denied"
    
    @app.route('/product/delete/<pid>/', methods = ['GET', 'POST'])
    @login_required
    def product_delete(pid):
        if current_user.role == 'admin':
            data = Products.query.get(pid)
            db.session.delete(data)
            db.session.commit()

            flash('Product deleted successfully')
            return redirect(url_for('product_management'))
        else:
            return "Access Denied"


