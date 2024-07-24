from flask import Flask, render_template, request, make_response

app = Flask(__name__, template_folder="templates")

# return a str to html page
@app.route('/about')
def about():
    return "<center><h1>about : </h1</center>"

# use with curl :
# ------------------------------------------------
# return with status code
# eg:   return "h", status-code
#       200 , 300, 404 ,500 etc
# show in curl command 

@app.route('/status-code')
def status_code():
    return "hello", 400

@app.route('/custom-response')
def cust_res():

    response = make_response()
    response.status_code = 202
    response.headers['content-type'] = "application/octet1-stream"
    return response
# ------------------------------------------------

# return a .html page
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/details')
def pass_details():
    name = "abc"
    age = "30"
    skills = ['Webdev','Python','Javascript','Flask','AI and ML']
    return render_template('details.html', name=name, age=age, skills=skills)

# filters in jina2 explained > filter.html
# --------------------------------------------
@app.route('/filters')
def res_filter():
    text = "Hello World !"
    return render_template('filters.html', text=text)

# custom filter for reverse a string
@app.template_filter('reverse_string')
def reverse_string(s):
    return s[::-1]

# custom filter for repeat a string
@app.template_filter('repeat')
def repeate(s, times=2):
    return s * times

@app.template_filter('alternate_case')
def alternate_case(s):
    return "".join([c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(s)])
# --------------------------------------------

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

# dynamic route : get name from endpoint
@app.route('/about/<name>')
def about_me(name):
    return f"<center><h1>about :{name} </h1</center>"

# dynamic route get number : int, float
@app.route('/calc/<int:num1>')
def calc_num(num1):
    return f"<center><h1>number is {num1} </h1</center>"


#  request method:

# GET -
# url parameters are in a dict = request.args[]
# use :
#     var = request.args['parameter_key']
#     or
#     var = request.args.get('parameter_key')

# POST - 
# data parameters are in a dict = request.form[]
# use :
#     var = request.form['data_key']


# find which method is used and respond acoording to method -
# if request.method == "GET":
#     pass
# elif request.method == "POST":
#     pass
# else:
#     pass


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

@app.route('/register/report', methods=['POST'])# for report page
def report_post():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    method = 'POST'
    return render_template('registered-report.html', username=username, password=password, 
                           email=email, method=method)






if __name__ == '__main__':
    app.run(debug=True) 