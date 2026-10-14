"""
Jaden Wiltshire
Oct 13, 2026
lab 10: intro to Flask
"""
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    name = "Jaden Wiltshire"
    fruits = ['apple', 'pineapple', 'oranges']
    return render_template("index.html", username=name, listfruits=fruits)


@app.route('/about')
def about():
    images = ['cockatiel3.jpg', '', 'cockatiel3.jpg']
    return render_template('about.html', images=images)


@app.route('/quotes')
def quotes():
    # Redirect to the index route.
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
