from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    entries = Entry.query.all()
    return render_template('index.html', entries=entries)

@app.route('/add_entry', methods=['POST'])
def add_entry():
    title = request.form['title']
    content = request.form['content']
    new_entry = Entry(title=title, content=content)
    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit_entry/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    entry = Entry.query.get(id)
    if request.method == 'POST':
        entry.title = request.form['title']
        entry.content = request.form['content']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_entry.html', entry=entry)

@app.route('/delete_entry/<int:id>')
def delete_entry(id):
    entry = Entry.query.get(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
