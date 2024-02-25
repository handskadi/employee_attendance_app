# create_project.py

from models import mysql, CreateForm
from flask import redirect, url_for, session, render_template

def create_project_route():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user WHERE email=%s", ('wafa@marouani.com',))
    user = cursor.fetchone()
    if user and 'user_id' in session and session['user_id'] == 1:
        form = CreateForm()
        if form.validate_on_submit():
            project_name = form.project_name.data
            is_active = form.is_active.data
            description = form.description.data
            cursor.execute("INSERT INTO project (project_name, is_active, description) VALUES (%s,%s,%s)", (project_name, is_active, description))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('dashboard_route'))
        return render_template('project.html', form=form)
    return redirect(url_for('login'))
