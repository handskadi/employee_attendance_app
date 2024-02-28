from flask import Flask,  render_template, redirect, url_for, request, session, flash
import bcrypt

from models import app, mysql, CreateForm, AttendanceForm, RegisterForm, LoginForm, EditEmployeeForm
from eap_funcs.login import handle_login
from eap_funcs.dashboard import dashboard
from eap_funcs.create_project import create_project_route
from eap_funcs.create_employee import create_employee_route
from eap_funcs.add_attendance import add_attendance_route
from eap_funcs.update_employee import update_employee_route
from eap_funcs.home import homepage_route
from eap_funcs.list_employees import employees_route
from eap_funcs.update_project import update_project_route
from eap_funcs.list_attendance import list_attendance_route
from eap_funcs.addUpdate_attendance import get_attendance_route,update_attendance_route
from functools import wraps

# Function to check if the user is logged in (decorator)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Main Dashboard 
@app.route('/dashboard')
@login_required
def dashboard_route(): 
    dashboard_data = dashboard(session)
    return render_template('dashboard.html', **dashboard_data)


# Employee CRUD
@app.route('/create_employee', methods=['GET','POST'])
@login_required
def create_employee():
    return create_employee_route(app)

@app.route('/employees', methods=['GET','POST'])
@login_required
def list_employees():
    dashboard_data = dashboard(session)
    return render_template('list_employees.html', **dashboard_data)
    

@app.route('/update_employee/<int:employee_id>', methods=['GET', 'POST'])
@login_required
def update_employee(employee_id):
    return update_employee_route(employee_id)

# Project CRUD
@app.route('/create_project', methods=['GET','POST'])
@login_required
def create_project():
    return create_project_route()

@app.route('/projects', methods=['GET','POST'])
@login_required
def list_projects():
    dashboard_data = dashboard(session)
    return render_template('list_projects.html', **dashboard_data)
    
@app.route('/update_project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    return update_project_route(project_id)

# Attendance App
@app.route('/add_attendance', methods=['GET','POST'])
@login_required
def add_attendance():
    return add_attendance_route()


# Attendance App
@app.route('/attendances', methods=['GET','POST'])
@login_required
def list_attendance():
    return list_attendance_route()


# get attendance with Ajax
@app.route('/get_attendance', methods=['POST'])
@login_required
def get_attendance():
    return get_attendance_route()


# get attendance with Ajax
@app.route('/update_attendance', methods=['POST'])
@login_required
def update_attendance():
    return update_attendance_route()

# Index, login, logout  & 404
@app.route('/')
def index():
    return homepage_route()
    
@app.route('/login', methods=['GET','POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard_route'))  # Redirect to dashboard if already logged in

    form = LoginForm()
    if form.validate_on_submit():
        if handle_login(form, session, "Login fail. Please check your email and password"):
            return redirect(url_for('dashboard_route'))
        else:
            return redirect(url_for('login'))
    
    return render_template('login.html', form=form)

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
