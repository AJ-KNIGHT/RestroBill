from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='templates')

items = ["Item 1", "Item 2", "Item 3", "item 4", "item 5", "item 6"]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_data_list', methods=['GET'])
def get_data_list():
    # Example data to send back
    return jsonify(items)

@app.route('/get_data_json', methods=['GET'])
def get_data_json():
    # Example data to send back
    # return jsonify(items=items)
    return jsonify({"items":items})


@app.route('/set_data/<item>')
def set_data(item):
    items.append(item)
    return ('', 204)


if __name__ == '__main__':
    app.run(debug=True)
