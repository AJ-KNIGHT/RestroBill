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
    @app.route('/delete/<pid>', methods=['DELETE'])
    def delete(pid):
        Person.query.filter(Person.pid == pid).delete()

        db.session.commit()
        people = Person.query.all()
        return render_template('index.html', people=people)

    @app.route('/details/<pid>')
    def details(pid):
        person = Person.query.filter(Person.pid == pid).first()

        return render_template('details.html', person=person)
    
    @app.route('/details_table')
    def details_table():
        people = Person.query.all()
        return render_template('details-table.html', people=people)


