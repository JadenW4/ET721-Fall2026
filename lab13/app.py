from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

import mysql.connector

app = Flask(__name__)

# database connection
def get_db_connection():
    return mysql.connector.connect(
        host = '127.0.0.1',
        user = 'flaskuser',
        password = 'password123',
        database = "blogDB"
    )

@app.route('/')
def index():
    return render_template('index.html')

# collects all data in the blog and users table and displays it on the blogs.html page
@app.route('/blogs')
def blogs():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT blog.id, users.username, blog.title, blog.content, blog.created_at FROM blog JOIN users ON blog.user_id = users.userid")
            data = cursor.fetchall()
        finally:
            cursor.close()
    finally:
        connection.close()

    return render_template('blogs.html', blogs = data)

# add a new blog post to the database
@app.route('/add_blog', methods=['GET', 'POST'])
def add_blog():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        username = request.form['username']
        email = request.form['email']

        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            try:
                cursor.execute("INSERT INTO users(username, email) VALUES (%s, %s)", (username, email))
                connection.commit()

                # store the user_id of the newly inserted user
                user_id = cursor.lastrowid

                # insert the blog post into the blog table with the user_id
                cursor.execute("INSERT INTO blog(user_id, title, content) VALUES (%s, %s, %s)", (user_id, title, content))
                connection.commit()
            finally:
                cursor.close()
        finally:
            connection.close()

        return redirect(url_for('blogs'))


if __name__ == '__main__':
    app.run(debug=True)