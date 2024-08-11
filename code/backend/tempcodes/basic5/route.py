from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required

from models import Users


def register_routes(app, db, bcrypt):
    @app.route('/')
    def index():
        return render_template('index.html')
        # if current_user.is_authenticated:
        #     return str(current_user.username)
        # else:
        #     return "No user logged in"
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'GET':
            return render_template('signup.html')
        elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            hashed_password = bcrypt.generate_password_hash(password)

            user = Users(username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('index'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = Users.query.filter(Users.username == username).first()
            #  or user = Users.query.filter_by(username = username).first()
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                return "Authentication Error"
            
    @app.route('/logout/')
    @login_required
    def logout():
        logout_user()
        return render_template('index.html')
    
    # protect the endpoit with login 1
    # ----------------------------------------
    # @app.route('/secret')
    # def secret():
    #     if current_user.role == 'admin':
    #         return 'My secret msg'
    #     else:
    #         return "Access Denied"


    # protect the endpoit with login 22
    @app.route('/secret')
    @login_required
    def secret():
        return 'My secret msg'
    # ----------------------------------------
