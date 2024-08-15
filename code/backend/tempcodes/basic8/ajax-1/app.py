from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_text', methods=["POST"])
def get_text():
    if request.method == "POST":
        print(request.form)
        return ('', 204)


if __name__ == '__main__':
    app.run(debug=True)