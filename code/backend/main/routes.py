from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required

from models import Users

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
        return render_template('login.html')



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

    # dashboard page 
    @app.route('/dashboard')
    @login_required
    def dashboard():
        if current_user.role == 'admin':
            return render_template('dashboard.html', username=current_user.username)
        else:
            return "Access Denied"
        
    @app.route('/manage_user', methods=['GET', 'POST'])
    def manage_user():
        if request.method == 'GET':
            return render_template('manage_user.html')
        elif request.method == 'POST':
            if 'username' in request.form.keys() and 'password' in request.form.keys() and 'role' in request.form.keys():
                username = request.form['username']
                password = request.form['password']
                role = request.form['role']

                hashed_password = bcrypt.generate_password_hash(password)

                user = Users(username=username, password=hashed_password, role=role)
                db.session.add(user)
                db.session.commit()

                return f"{username} : User Created!"
