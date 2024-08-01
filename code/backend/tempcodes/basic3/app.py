from flask import Flask, render_template

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

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

if __name__ == '__main__':
    app.run(debug=True)