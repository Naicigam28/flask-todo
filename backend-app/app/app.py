from flask import Flask, request, redirect
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://usr:pwd@pgsql:5432/todos"
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    description = db.Column(db.String(), nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def obj_to_dict(self):  # for build json format
        return {
            "id": self.id,
            "completed": self.completed,
            "description": self.description,
            "due_date": self.due_date,
            "date_created": self.date_created,
        }

    def __repr__(self):
        return "<todo %r>" % self.id


def dict_helper(objlist):
    result2 = [item.obj_to_dict() for item in objlist]
    return result2


@app.route("/todos", methods=["POST", "GET"])
def todos():
    if request.method == "POST":
        todo_content = request.form["description"]
        new_todo = Todo(description=todo_content)

        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect("http://localhost/")
        except:
            print("FAILED", request)
            return redirect("http://localhost/")

    else:
        todos = Todo.query.order_by(Todo.date_created).all()
        todos = dict_helper(todos)
        return jsonify(todos), 200


with app.app_context():
    db.drop_all()
    db.create_all()
if __name__ == "__main__":
    app.run(port=5000)
