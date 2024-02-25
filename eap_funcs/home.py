# index.py

from models import mysql
from flask import render_template, session

def homepage_route():
    logged_in_employee = []
    user = None
    if 'user_id' in session:
        user_id = session['user_id']
         # Retrieve user & employer data
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM user where user_id=%s", (user_id,))
        user = cursor.fetchone()
        cursor.execute("SELECT * FROM employee WHERE user_id=%s", (session['user_id'],))
        logged_in_employee = cursor.fetchone()

        cursor.close()
    return render_template('index.html', user=user, logged_in_employee=logged_in_employee)
