from flask import Flask, send_file, render_template_string, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_name', methods=['POST'])
def submit_name():
    name = request.form['name']
    return redirect(url_for('greet', name=name))

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

