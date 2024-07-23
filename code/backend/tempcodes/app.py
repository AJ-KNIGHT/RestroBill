from flask import Flask, render_template, request

app = Flask(__name__)

# return a .html page
@app.route('/')
def index():
    return render_template("index.html")

# return a .html page with name endpoint
@app.route('/<name>')
def name(name):
    return render_template("name.html", name = name)

# return multiplication table of endpoint num
@app.route('/calc/multi/<int:num>')
def multi(num):
    return render_template('multi.html', num = num)

# app route custome rule
app.add_url_rule('/home','/',index)

# return a str to html page
@app.route('/about')
def about():
    return "<center><h1>about : </h1</center>"

# dynamic route : get name from endpoint
@app.route('/about/<name>')
def about_me(name):
    return f"<center><h1>about :{name} </h1</center>"

# dynamic route get number : int, float
@app.route('/calc/<int:num1>')
def calc_num(num1):
    return f"<center><h1>number is {num1} </h1</center>"


# form access with Get

@app.route('/register-get')# for form page
def register_get():
    return render_template('register-get.html')

@app.route('/register/report', methods=['GET']) # for report page
def report_get():
    username = request.args.get('username')
    password = request.args.get('password')
    email = request.args.get('email')
    method = 'GET'

    return render_template('registered-report.html', username=username ,password=password,
                           email=email, method=method)


# form access with post

@app.route('/register-post')# for form page
def register_post():
    return render_template('register-post.html')

@app.route('/register/report', methods=['POST'])
def report_post():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    method = 'POST'

    return render_template('registered-report.html', username=username, password=password, 
                           email=email, method=method)



if __name__ == '__main__':
    app.run(debug=True) 