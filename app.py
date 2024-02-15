import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt
from flask_mysqldb import MySQL

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# MySQL Configuration
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.secret_key = os.getenv('SECRET_KEY')

mysql = MySQL(app)


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Add User")

    def validate_email(self, field):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users where email=%s", (field.data,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            raise ValidationError('Email Already Taken')


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    # Read data From database
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s", ('handskadi@gmail.com',))
    user = cursor.fetchone()
    if user and 'user_id' in session and session['user_id'] == 1:

        form = RegisterForm()
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            password = form.password.data 

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Store data into database
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)", (name, email, hashed_password))
            mysql.connection.commit()
            cursor.close()

            return redirect(url_for('dashboard'))

        return render_template('register.html', form=form)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))  # Redirect to dashboard if already logged in

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data 

        # Read data From database
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            flash("Login fail. Pleae check your email and password")
            return redirect(url_for('login'))
    
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users where id=%s", (user_id,))
        user = cursor.fetchone()

        # Fetch all users' data
        cursor.execute("SELECT * FROM users")
        all_users = cursor.fetchall()
        cursor.close()

        if user:
            return render_template('dashboard.html', user=user, all_users=all_users)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out successfully.")
    return redirect(url_for('login'))

# Custom error handler for 404 errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
