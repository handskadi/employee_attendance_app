# create_employee.py

from models import mysql, RegisterForm, CreateForm
import bcrypt
from flask import redirect, url_for, session, render_template

def create_employee_route(app):
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user WHERE email=%s", ('wafa@marouani.com',))
    user = cursor.fetchone()
    
    if user and 'user_id' in session and session['user_id'] == 1:
        
        cursor.execute("SELECT * FROM user")
        all_users = cursor.fetchall()
        logged_in_employee = []
        cursor.execute("SELECT * FROM employee WHERE user_id=%s", (session['user_id'],))
        logged_in_employee = cursor.fetchone()

        print(logged_in_employee)

        form = RegisterForm()
        form.upload_folder = app.config['UPLOAD_FOLDER']
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            role = form.role.data
            username = form.username.data
            hire_date = form.hire_date.data
            end_employment = form.end_employment.data 
            project = form.project.data
            manager = form.manager.data  
            password = form.password.data 
            image = form.image.data


            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Store data into database
            cursor = mysql.connection.cursor()
            # Store data into user table
            cursor.execute("INSERT INTO user (username, email, password) VALUES (%s,%s,%s)", (username, email, hashed_password))
            cursor.execute("SELECT user_id FROM user where email=%s", (form.email.data,))
            # Store data into user employee table
            user_id_employee = cursor.fetchone()[0]

            # Save the image and get the filename
            if image:
                image_filename = form.save_image(image)
                print("before save: " + image.filename)
            else:
                print("No image uploaded")
                image_filename = 'default.png'

            
            cursor.execute("INSERT INTO employee  (user_id, hire_date, end_employment, manager_id, project_id, firstname, lastname, role, image_filename) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (user_id_employee, hire_date, end_employment, manager, project, first_name, last_name, role, image_filename))

            mysql.connection.commit()


            return redirect(url_for('employees'))

        return render_template('create_employee.html', form=form, user=user, logged_in_employee=logged_in_employee)
    return redirect(url_for('login'))
