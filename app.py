from flask import Flask, send_file, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import re

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DESKTOP-P2UO69O\SQLEXPRESS/AnimorphsSite?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the User model

class User(db.Model):
    __tablename__ = 'Users'
    pk_user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    col_username = db.Column(db.String(50), nullable=False, unique=True)
    col_user_first_name = db.Column(db.String(50), nullable=False)
    col_user_last_name = db.Column(db.String(50), nullable=False)

# Define the Review model
class Review(db.Model):
    __tablename__ = 'Reviews'
    pk_review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fk_user_id = db.Column(db.Integer, db.ForeignKey('Users.pk_user_id'), nullable=False)
    fk_book_id = db.Column(db.Integer, db.ForeignKey('Books.pk_book_ID'), nullable=False)
    col_review_contents = db.Column(db.Text, nullable=True)
    col_rating = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    book = db.relationship('Book', backref=db.backref('reviews', lazy=True))


# Define the Books model
class Book(db.Model):
    __tablename__ = 'Books'
    pk_book_ID = db.Column(db.Integer, primary_key=True)
    col_book_title = db.Column(db.String(250), nullable=False)
    col_book_path = db.Column(db.String(250), nullable=False)  # PDF file path
    col_book_audio = db.Column(db.String(250), nullable=True)  # Audio file path for listen
    col_book_cover = db.Column(db.String(250), nullable=True)

def clean_filename(filename):
    # Regular expression pattern to match non-alphanumeric characters except '_', '-' and '.'
    cleaned_filename = re.sub(r'[^\w\-\.]', '', filename)
    return cleaned_filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_name', methods=['POST'])
def submit_name():
    username = request.form['name']
    user = User.query.filter_by(col_username=username).first()

    if user:
        return redirect(url_for('greet', name=username))
    else:
        return redirect(url_for('new_user', name=username))



@app.route('/greet/<name>')
def greet(name):
    # Query user by username
    user = User.query.filter_by(col_username=name).first()
    if user:
        # Count of reviews/rankings submitted by the user
        reviews_count = len(user.reviews)

        # Query all books and their respective review counts for the user
        books = Book.query.all()
        book_reviews_count = {book.pk_book_ID: len([review for review in user.reviews if review.fk_book_id == book.pk_book_ID]) for book in books}
    else:
        reviews_count = 0
        book_reviews_count = {}

    return render_template('greet.html', name=name, reviews_count=reviews_count, book_reviews_count=book_reviews_count, books=books)

@app.route('/download/<path:filename>')
def download(filename):
    filename = clean_filename(filename)
    # Adjust filepath for download
    filepath = os.path.join('C:\\Users\\Admin\\MS587 Web and SQL\\MS587-Assignment-3\\MS587-Assignment-3\\Animorphs\\PDF', filename)
    try:
        return send_file(filepath, as_attachment=True)
    except FileNotFoundError:
        return "File not found", 404

@app.route('/read/<path:filename>')
def read(filename):
    # Adjust filepath for read
    filename = clean_filename(filename)
    filepath = os.path.join('C:\\Users\\Admin\\MS587 Web and SQL\\MS587-Assignment-3\\MS587-Assignment-3\\Animorphs\\PDF', filename)
    try:
        with open(filepath, 'rb') as file:
            content = file.read()
        return content, 200, {'Content-Type': 'application/pdf'}
    except FileNotFoundError:
        return "File not found", 404


@app.route('/listen/<path:filename>')
def listen(filename):
    # Clean the filename to remove unwanted characters
    filename = clean_filename(filename)
        # Ensure the filename stops at .mp3 (truncate any characters after .mp3)
    mp3_index = filename.find('.mp3')
    if mp3_index != -1:
        filename = filename[:mp3_index + 4]  # +4 to include .mp3
    
    # Adjust filepath for listen endpoint
    audio_base_path = 'C:\\Users\\Admin\\MS587 Web and SQL\\MS587-Assignment-3\\MS587-Assignment-3\\Animorphs\\story_texts'
    audio_filepath = os.path.join(audio_base_path, filename)

    try:
        return send_file(audio_filepath, as_attachment=True)
    except FileNotFoundError:
        return "Audio file not found", 404


@app.route('/new_user/<name>', methods=['GET', 'POST'])
def new_user(name):
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        # Create a new User object
        new_user = User(col_username=name, col_user_first_name=first_name, col_user_last_name=last_name)

        try:
            # Add new user to the database
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('greet', name=name))  # Redirect to greet page after successful creation
        except Exception as e:
            # Handle any exceptions (e.g., database errors)
            print(f"Error creating user: {e}")
            return "Error creating user. Please try again."

    # Render the new_user.html template for GET requests
    return render_template('new_user.html', name=name)


@app.route('/submit_review', methods=['POST'])
def submit_review():
    username = request.form['username'] 
    user = User.query.filter_by(col_username=username).first()

    if not user:
        return "User not found", 404  # Handle case where user does not exist

    book_id = request.form['book_id']
    review_text = request.form['review_text']
    rating = request.form['rating']

    # Create a new Review object and add it to the database
    new_review = Review(fk_user_id=user.pk_user_id, fk_book_id=book_id, col_review_contents=review_text, col_rating=rating)
    db.session.add(new_review)
    db.session.commit()

    return redirect(url_for('greet', name=username))  # Redirect to greet page with correct username



@app.route('/add_review/<name>', methods=['GET', 'POST'])
def add_review(name):
    if request.method == 'POST':
        username = name  # Assuming username is passed via the URL
        user = User.query.filter_by(col_username=username).first()

        if not user:
            return "User not found", 404  # Handle case where user does not exist

        book_id = request.form['book_id']
        review_text = request.form['review_text']
        rating = request.form['rating']

        # Create a new Review object and add it to the database
        new_review = Review(fk_user_id=user.pk_user_id, fk_book_id=book_id, col_review_contents=review_text, col_rating=rating)
        db.session.add(new_review)
        db.session.commit()

        return redirect(url_for('greet', name=username))  # Redirect to greet page with correct username

    # GET request: Provide the add_review.html form with list of books
    books = Book.query.all()  # Query all books to populate the dropdown
    return render_template('add_review.html', name=name, books=books)

if __name__ == "__main__":
    app.run()
