from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f'Task {self.id}'

# with app.app_context():
#     db.create_all()

@app.route(rule='/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST' and request.form['content']:
        try:
            db.session.add(Task(content=request.form['content']))
            db.session.commit()
            return redirect('/')
        except OperationalError:
            return 'There was an error adding the task...'
    else:
        tasks = Task.query.order_by(Task.date_created).all()
        return render_template(template_name_or_list='index.html', tasks=tasks)

@app.route(rule='/delete/<int:task_id>')
def delete(task_id):
    try:
        db.session.delete(Task.query.get_or_404(task_id))
        db.session.commit()
        return redirect('/')
    except OperationalError:
        return 'There was an error deleting the task...'

@app.route(rule='/rename/<int:task_id>', methods=['POST', 'GET'])
def rename(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except OperationalError:
            return 'There was an error renaming the task...'
    else:
        return render_template(template_name_or_list='rename.html', task=task)

if __name__ == '__main__':
    app.run(debug=False)
