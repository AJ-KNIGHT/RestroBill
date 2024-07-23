from flask import Flask, render_template

#tempcodes
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")
    
@app.route('/about')
def about():
    return "<center><h1>about : </h1</center>"
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



if __name__ == '__main__':
    app.run(debug=True) 