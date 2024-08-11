from flask import request, render_template, redirect, url_for, Blueprint

from blueprintapp.app import db
from blueprintapp.todos.models import Todo

todos = Blueprint('todos', __name__, template_folder='templates')

@todos.route('/')
def index():
    todos = Todo.query.all()
    return render_template('todos/index.html', todos=todos)