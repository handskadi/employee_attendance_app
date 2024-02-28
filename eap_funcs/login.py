# login.py

from models import mysql
import bcrypt
from flask import flash


def handle_login(form, session, flash_message):
    email = form.email.data
    password = form.password.data

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user WHERE email=%s", (email,))
    user = cursor.fetchone()
    cursor.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        session['user_id'] = user[0]
        return True
    else:
        flash(flash_message)
        return False
