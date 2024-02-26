from flask import Flask,  render_template, redirect, url_for, request, session, flash
import bcrypt

from models import app, mysql, CreateForm, AttendanceForm, RegisterForm, LoginForm, EditEmployeeForm
from eap_funcs.dashboard import dashboard
from eap_funcs.login import handle_login
from eap_funcs.create_project import create_project_route
from eap_funcs.create_employee import create_employee_route
from eap_funcs.add_attendance import add_attendance_route
from eap_funcs.update_employee import update_employee_route
from eap_funcs.home import homepage_route
from eap_funcs.employees import employees_route


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

 
@app.route('/dashboard')
def dashboard_route():
    dashboard_data = dashboard(session)
    if dashboard_data:
        return render_template('dashboard.html', **dashboard_data)
    else:
        return redirect(url_for('login'))

@app.route('/create_project', methods=['GET','POST'])
def project():
    return create_project_route()


@app.route('/create_employee', methods=['GET','POST'])
def register():
    return create_employee_route(app)


@app.route('/add_attendance', methods=['GET','POST'])
def attendance():
    return add_attendance_route()


@app.route('/update_employee/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    return update_employee_route(employee_id)

@app.route('/employees', methods=['GET','POST'])
def employees():
    dashboard_data = dashboard(session)
    if dashboard_data:
        return render_template('employees.html', **dashboard_data)
    else:
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
