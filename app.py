from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymysql
import pandas as pd

app = Flask(__name__)

# MySQL Database Connection
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "user_management"
}

# Function to connect to MySQL
def get_db_connection():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        cursorclass=pymysql.cursors.DictCursor
    )

# Route for Signup Form
@app.route('/')
def signup_form():
    return render_template('signup.html')

# Handle User Signup
@app.route('/submit', methods=['POST'])
def submit_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, password))
        connection.commit()
    except Exception as e:
        return f"Error: {e}", 500
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('view_users'))

# Route to Display Users
@app.route('/users')
def view_users():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('users.html', users=users)

# API Endpoint for Power BI


# API to provide JSON data for Power BI
@app.route('/api/users')
def api_users():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True, port= 5001)
