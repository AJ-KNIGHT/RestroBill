# routes
from flask import render_template, request
from models import Person

def register_routes(app, db):
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'GET':
            people = Person.query.all()
            # return str(people)
            return render_template('index.html', people=people)
        elif request.method == 'POST':
            name = request.form['name']
            age = int(request.form['age'])
            job = request.form['job']

            person = Person(name=name, age=age, job=job)

            db.session.add(person)
            db.session.commit()

            people = Person.query.all()
            # return str(people)
            return render_template('index.html', people=people)