from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'


db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    finished = db.Column(db.Boolean)

    def __init__(self, title, finished):
        self.title = title
        self.finished = finished

@app.route('/')
def index():
    #show todo list
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template("list.html", todo_list=todo_list)

@app.route('/add', methods=['POST'])
def add():
    # add new list
    title = request.form.get("title")
    new_todo = Todo(title=title, finished=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.finished = not todo.finished
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == '__main__':
    db.create_all()
    app.run()