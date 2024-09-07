# app.py
from flask import Flask, render_template, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from weasyprint import HTML

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bills.db'
db = SQLAlchemy(app)

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    items = db.relationship('BillItem', backref='bill', lazy=True)

class BillItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

@app.route('/create_bill', methods=['POST'])
def create_bill():
    # Retrieve form data
    customer_name = request.form['customer_name']
    total_amount = float(request.form['total_amount'])
    
    # Create bill items
    items = []
    for i in range(int(request.form.getlist('item_count'))[0]):
        item_name = request.form[f'item_{i}_name']
        quantity = int(request.form[f'item_{i}_quantity'])
        price = float(request.form[f'item_{i}_price'])
        items.append(BillItem(item_name=item_name, quantity=quantity, price=price))
    
    # Save bill to database
    bill = Bill(customer_name=customer_name, total_amount=total_amount)
    db.session.add(bill)
    for item in items:
        bill.items.append(item)
    db.session.commit()

    # Generate PDF
    html_content = render_template('bill.html', bill=bill)
    pdf_content = HTML(string=html_content).write_pdf()

    # Send PDF as download
    return send_file(
        io.BytesIO(pdf_content),
        mimetype='application/pdf',
        as_attachment=True,
        attachment_filename=f'bill_{bill.id}.pdf'
    )

if __name__ == '__main__':
    app.run(debug=True)
