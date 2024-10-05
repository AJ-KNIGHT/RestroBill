from flask import Flask, render_template
from html2image import Html2Image
import os

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

@app.route('/')
def index():
    return render_template("test.html")

@app.route('/bill')
def bill():
    content = render_template('bill.html')
    from reportlab.pdfgen import canvas


        # Create a new PDF document
    pdf = canvas.Canvas('output.pdf')

        # Add content to the PDF
    pdf.drawString(100, 800, "content")

        # Save the PDF
    pdf.save()
    return content

@app.route('/test-bill')
def testbill():
    return render_template('bill.html')

if __name__ == '__main__':
    app.run(debug=True)