from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# form login - normal
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('forms/login.html')
    elif request.method == 'POST':
        if 'username' in request.form.keys() and 'password' in request.form.keys():
            username = request.form['username']
            password = request.form['password']

            if username == 'admin' and password == '123':
                return "<h1>Login sucess</h1>"
            else:
                return "<h1>Incorrect username and password</h1>"
        else:
            return "<h1>username and password not in form</h1>"


@app.route('/file-upload', methods=['POST'])
def file_upload():
    pass

if __name__ == '__main__':
    app.run(debug=True)