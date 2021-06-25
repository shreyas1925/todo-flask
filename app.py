from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todoapp.db"
# Doing this to get rid of warning

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    # I am defining my database schema here
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(550), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Whenever I print Todo object by that it will print the respective

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title} "


@app.route('/', methods=['GET', 'POST'])
def hello_world():

    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']

    # Whenver i go for home
        todo = Todo(title=title, description=description)
        # Creating the instance objects
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template("index.html", alltodo=alltodo)


# @app.route('/products')
# def products_world():
#     return 'Hello,  Products'


# @app.route('/show')
# def show_items():
#     alltodo = Todo.query.all()
#     print(alltodo)
#     return 'Hello,  Products'


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update_items(sno):
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.description = description
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)


@app.route('/delete/<int:sno>')
def delete_items(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
