import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField, FileAllowed
from flask import current_app
from wtforms.validators import NumberRange


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

# Define the upload folder within the static directory
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



class CreateForm(FlaskForm):
    project_name = StringField("Project Name", validators=[DataRequired()])
    is_active = BooleanField("Active")
    description = StringField("Description", validators=[DataRequired()])
    submit = SubmitField("Create Project")

class AttendanceForm(FlaskForm):
    # retive all employees
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM employee WHERE role='employee'")
        employees = cursor.fetchall()  
        cursor.close()
        employee_choices =  [(str(employee[0]), employee[6] +' '+ employee[7]) for employee in employees]
        employee = SelectField('Select Employee', choices=employee_choices, validators=[DataRequired()])
    attendance_date = DateField('Attendance Date', format='%Y-%m-%d', validators=[DataRequired()])
    day_shift_hours = IntegerField('Day Shift Hours', default=3, validators=[DataRequired(), NumberRange(min=1, max=8)])
    night_shift_hours = IntegerField('Night Shift Hours', validators=[DataRequired(), NumberRange(min=1, max=8)])
    hours_worked = IntegerField('Hours Worked')
    comment = StringField("Comment", validators=[DataRequired()])
    submit = SubmitField("Commit")

@app.route('/attendance', methods=['GET','POST'])
def attendance():
    # Read data From database
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user WHERE email=%s", ('wafa@marouani.com',))
    user = cursor.fetchone()
    if user and 'user_id' in session and session['user_id'] == 1:
        form = AttendanceForm()
        print("outside of if")
        if form.validate_on_submit():
            print("Got here")
            employee = form.employee.data
            attendance_date = form.attendance_date.data
            day_shift_hours = form.day_shift_hours.data
            night_shift_hours = form.night_shift_hours.data
            hours_worked = day_shift_hours + night_shift_hours
            comment = form.comment.data

            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO attendance (employee_id, attendance_date, day_shift_hours, night_shift_hours, hours_worked, comment) VALUES (%s,%s,%s,%s,%s,%s)", (employee, attendance_date, day_shift_hours, night_shift_hours, hours_worked, comment ))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('dashboard'))
        return render_template('attendance.html', form=form)
    return redirect(url_for('login'))

class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    role = SelectField('Select Role', choices=[('general_manager', 'General Manager'), ('project_manager', 'Project Manager'), ('employee', 'Employee') ], validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Temporary Password", validators=[DataRequired()])
    hire_date = DateField('Hire Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_employment = DateField('End of Employment', format='%Y-%m-%d', validators=[DataRequired()])

    # retrive all projects
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM project WHERE is_active='1'")
        projects = cursor.fetchall()  
        cursor.close()
        project_choices =  [(str(project[0]), project[1]) for project in projects]
        project = SelectField('Assign Project', choices=project_choices, validators=[DataRequired()])
    
    # retive all managers
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM employee WHERE role='project_manager'")
        managers = cursor.fetchall()  
        cursor.close()
        manager_choices =  [(str(manager[0]), manager[6] +' '+ manager[7]) for manager in managers]
        manager = SelectField('Assign Manager', choices=manager_choices, validators=[DataRequired()])
    
    image = FileField("Upload Image", validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField("Add Employee")

    # Add UPLOAD_FOLDER to the form instance
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.upload_folder = current_app.config['UPLOAD_FOLDER']

    def validate_email(self, field):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM user where email=%s", (field.data,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            raise ValidationError('Email Already Taken')
    
    def save_image(self, image):
        if image:
            filename = secure_filename(image.filename)
            os.makedirs(self.upload_folder, exist_ok=True)  # Create the directory if it doesn't exist
            image_path = os.path.join(self.upload_folder, filename)
            image.save(image_path)
            return filename
        return None

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")    

@app.route('/')
def index():
    return render_template('index.html')

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
        cursor.execute("SELECT * FROM user WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
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
        cursor.execute("SELECT * FROM user where user_id=%s", (user_id,))
        user = cursor.fetchone()
        all_employees = []
        all_projects = []
        all_attendance = []
        is_manager = False

        # Fetch all users' data
        cursor.execute("SELECT * FROM user")
        all_users = cursor.fetchall()
        if session['user_id'] == 1:
            cursor.execute("SELECT * FROM employee")
            all_employees = cursor.fetchall()
            cursor.execute("SELECT * FROM project")
            all_projects = cursor.fetchall()
            cursor.execute("SELECT * FROM attendance")
            all_attendance = cursor.fetchall()
            is_manager = True

        else:
            cursor.execute("SELECT * FROM employee where role='project_manager'")
            productManagers = cursor.fetchall()
            for pm in productManagers:
                if pm[8] == 'project_manager':
                    # Get Employees
                    cursor.execute("SELECT employee_id FROM employee WHERE user_id=%s", (session['user_id'],))
                    employee_id = cursor.fetchone()
                    cursor.execute("SELECT * FROM employee WHERE role='employee' AND manager_id=%s  OR user_id=%s", ( employee_id, session['user_id'],))
                    all_employees = cursor.fetchall()
                    
                    # Get User role
                    cursor.execute("SELECT role FROM employee WHERE user_id=%s", (session['user_id'],))
                    employee_role = cursor.fetchone()
                    print(employee_role[0])
                    if employee_role[0] != 'employee':
                        is_manager = True

                    # Get Projects
                    cursor.execute("SELECT project_id FROM employee WHERE user_id=%s", (session['user_id'],))
                    project_id = cursor.fetchone()
                    cursor.execute("SELECT * FROM project where project_id=%s", (project_id,))
                    all_projects = cursor.fetchall()

                     # Fetch attendance data for the manager's employees
                    cursor.execute("SELECT * FROM attendance")
                    all_attendance = cursor.fetchall()
                else:
                    pass
        cursor.close()

        if user:
            return render_template('dashboard.html', user=user, all_users=all_users, all_employees=all_employees, all_projects=all_projects,  all_attendance=all_attendance, is_manager=is_manager)
    return redirect(url_for('login'))

@app.route('/project', methods=['GET','POST'])
def project():
    # Read data From database
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user WHERE email=%s", ('wafa@marouani.com',))
    user = cursor.fetchone()
    if user and 'user_id' in session and session['user_id'] == 1:
        form = CreateForm()
        if form.validate_on_submit():
            project_name = form.project_name.data
            is_active = form.is_active.data
            description = form.description.data
            cursor = mysql.connection.cursor()
            print("I got here")
            cursor.execute("INSERT INTO project (project_name, is_active, description) VALUES (%s,%s,%s)", (project_name, is_active, description))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('dashboard'))
        return render_template('project.html', form=form)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    # Read data From database
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user WHERE email=%s", ('wafa@marouani.com',))
    user = cursor.fetchone()
    if user and 'user_id' in session and session['user_id'] == 1:
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
            image_filename = form.save_image(image)

            cursor.execute("INSERT INTO employee  (user_id, hire_date, end_employment, manager_id, project_id, firstname, lastname, role, image_filename) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (user_id_employee, hire_date, end_employment, manager, project, first_name, last_name, role, image_filename))
            mysql.connection.commit()
            cursor.close()

            return redirect(url_for('dashboard'))

        return render_template('register.html', form=form)
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
