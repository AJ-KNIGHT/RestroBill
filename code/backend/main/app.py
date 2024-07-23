from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login/login.html')

@app.route('/login-report', methods=['POST'])
def login_report():
    username = request.form['username']
    password = request.form['password']

    return render_template('report.html', username=username, password=password)

if __name__ == '__main__':
    app.run(debug=True)