from flask import Flask, send_file,  render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
username = 'CaiNowicki'
password = 'databasepassword'
hostname = 'CaiNowicki.mysql.pythonanywhere-services.com'
database_name = 'CaiNowicki$AnimorphsUsers'

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{hostname}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

# Create the database and the User table if it doesn't exist
with app.app_context():
    if not db.engine.has_table('user'):
        db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_name', methods=['POST'])
def submit_name():
    name = request.form['name']
    user = User.query.filter_by(name=name).first()
    if user:
        return redirect(url_for('greet', name=name))
    else:
        return redirect(url_for('new_user', name=name))

@app.route('/new_user/<name>', methods=['GET', 'POST'])
def new_user(name):
    if request.method == 'POST':
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('greet', name=name))
    return render_template('new_user.html', name=name)


@app.route('/greet/<name>')
def greet(name):
    books = []
    with open('books_modified.txt', 'r') as file:
        for line in file:
            title, path = line.strip().split(',')
            books.append({'title': title, 'path': path})
    return render_template('greet.html', name=name, books=books)

@app.route('/download/<path:filename>')
def download(filename):
    # Remove leading backslash from the filename
    if filename.startswith('\\'):
        filename = filename[1:]

    filepath = os.path.normpath(os.path.join('Animorphs', 'PDF', filename))
    print(filepath)  # Print the filepath for debugging purposes
    try:
        return send_file(filepath, as_attachment=True)
    except FileNotFoundError:
        return "File not found", 404

@app.route('/read/<path:filename>')
def read(filename):
    # Remove leading backslash from the filename
    if filename.startswith('\\'):
        filename = filename[1:]

    filepath = os.path.normpath(os.path.join('Animorphs', 'PDF', filename))
    print(filepath)  # Print the filepath for debugging purposes
    try:
        with open(filepath, 'rb') as file:
            content = file.read()
        return content, 200, {'Content-Type': 'application/pdf'}
    except FileNotFoundError:
        return "File not found", 404

@app.route('/listen/<path:filename>')
def listen(filename):
    # Remove leading backslash from the filename
    if filename.startswith('\\'):
        filename = filename[1:]

    # Change the extension to .mp3
    filename = os.path.splitext(filename)[0] + ".mp3"

    filepath = os.path.normpath(os.path.join('Animorphs', 'PDF', 'story_texts', filename))
    print(filepath)  # Print the filepath for debugging purposes
    try:
        return send_file(filepath, as_attachment=True)
    except FileNotFoundError:
        return "File not found", 404



if __name__ == "__main__":
    app.run()

