import os
import uuid # generate random file names
import pandas as pd
from flask import Flask, render_template, request, Response, send_from_directory, jsonify
# request - get requested data
# Response - craft response
# send_from_directory - send file from server storage
# josonify - return json object

# not main , used for tempcode pwd location
from pathlib import Path
script_directory = Path(__file__).resolve().parent # script dir

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
                return "<h1 style='color:green'>Login sucess</h1>"
            else:
                return "<h1 style='color:red'>Incorrect username and password</h1>"
        else:
            return "<h1 style='color:red'>username and password not in form</h1>"

# get file and show in a page
# text file and excel file
# ----------------------------------------------------------
@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('forms/upload-file.html')
    elif request.method == 'POST':
        file = request.files['file']
        
        # Print the content type for debugging
        print(f"Uploaded file content type: {file.content_type}")

        if file.content_type in ['text/plain']:
            return f"<h1> Text file</h1><p>{file.read().decode()}</p>"
        elif file.content_type in [
            'application/vnd.ms-excel', 
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/wps-office.xlsx'  # Added WPS Office content type
        ]:
            try:
                df = pd.read_excel(file.stream)  # Use file.stream
                return f"{df.to_html()}"
            except Exception as e:
                return f"<h1 style='color:red'>Error processing Excel file: {str(e)}</h1>"
        else:
            return "<h1 style='color:red'>Unsupported file type</h1>"
    else:
        return "<h1 style='color:red'>ERROR Occurred!</h1>"
# ----------------------------------------------------------

# convert excel filet to csv 1
@app.route('/convert_csv', methods=['POST'])
def convert_csv():
    file = request.files['file']

    df = pd.read_excel(file.stream)
    response = Response(
        df.to_csv(),
        mimetype="text/csv",
        headers={
            'Content-Disposition': 'attachment; filename=result.csv'
        }
    )

    return response

# convert excel filet to csv 2
# ----------------------------------------------------------
@app.route('/convert_csv2', methods=['POST'])
def convert_csv2():
    file = request.files['file']
    df = pd.read_excel(file.stream)

    if not os.path.exists(f'{script_directory}/downloads'):
        os.makedirs(f'{script_directory}/downloads')

    download_dir = f'{script_directory}/downloads'
    
    # generate random name for csv file
    filename = f'{uuid.uuid4()}.csv'
    df.to_csv(os.path.join(download_dir, filename))

    return render_template('download.html', filename=filename)

@app.route('/download/<filename>')
def download(filename):
    download_dir = f'{script_directory}/downloads'
    return send_from_directory(download_dir, filename, download_name='result.csv')
# ----------------------------------------------------------

# deals with json sample
@app.route('/json_sample', methods=['POST'])
def json_sample():
    greeting = request.json['greeting']
    name = request.json['name']

    with open(f'{script_directory}/file.txt', 'w') as f:
        f.write(f'{greeting}, {name}')

    return jsonify({'message' : 'Successfully written!'})

if __name__ == '__main__':
    app.run(debug=True)