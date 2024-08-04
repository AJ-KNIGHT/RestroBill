from flask import Flask, render_template, session, make_response, request, flash

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
# for session key
app.secret_key = 'SOME KEY'


# home
@app.route('/')
def index():
    return render_template('index.html')

# alert onload page
@app.route('/alert')
def alert():
    return render_template('alert.html')

# bootstrap basic
@app.route('/bootstrap_basics')
def bootstrap_basic():
    return render_template('bootstrap-basic.html')

# session, cookies test page
@app.route('/data')
def data():
    return render_template('data.html', status_session='')

# session
# --------------------------------------------
# set session
@app.route('/set_session')
def set_session():
    session['name'] = 'user120'
    session['role'] = 'admin'
    return render_template('data.html', status_session=f'Session data set')

# get session
@app.route('/get_session')
def get_session():
    if 'name' in session.keys() and 'role' in session.keys():
        name = session['name']
        role = session['role']
        return render_template('data.html', status_session=f'Name: {name}, Role: {role}')
    else:
        return render_template('data.html', status_session='No session found.')
    
# clear session
@app.route('/clear_session')
def clear_session():
    session.clear()
    # session.pop('name') remove name key pair
    return render_template('data.html', status_session='session cleared')
# --------------------------------------------

# cookies
# --------------------------------------------
# set session
@app.route('/set_cookie')
def set_cookie():
    response = make_response(render_template('data.html', status_cookie='cookie set.', status_session='----'))
    response.set_cookie('cookie_name','cookie_value')
    return response

# get session
@app.route('/get_cookie')
def get_cookie():
    if 'cookie_name' in request.cookies.keys():
        cookie_value = request.cookies['cookie_name']
        return render_template('data.html', status_cookie=f'cookie_name : {cookie_value}', status_session='----')
    else:
        return render_template('data.html', status_cookie='cookie not found.', status_session='----')

# clear session
@app.route('/remove_cookie')
def remove_cookie():
    response = make_response(render_template('data.html', status_cookie='cookie removed.', status_session='----'))
    response.set_cookie('cookie_name', expires=0)
    return response
# --------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "admin" and password == '123':
            flash('Successful Login')
            return render_template('login.html')
        else:
            flash('Login Failed')
            return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)