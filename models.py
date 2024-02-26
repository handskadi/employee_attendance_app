import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError
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

class RegisterForm(FlaskForm):
    first_name = StringField("First name", validators=[DataRequired()])
    last_name = StringField("Last name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    role = SelectField('Select role', choices=[('general_manager', 'General Manager'), ('project_manager', 'Project Manager'), ('employee', 'Employee') ], validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Temporary password", validators=[DataRequired()])
    hire_date = DateField('Hire Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_employment = DateField('End of employment', format='%Y-%m-%d', validators=[DataRequired()])

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
    email = StringField("Email address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")    

class EditEmployeeForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    # email = StringField("Email", validators=[DataRequired(), Email()])
    role = SelectField('Select Role', choices=[('general_manager', 'General Manager'), ('project_manager', 'Project Manager'), ('employee', 'Employee') ], validators=[DataRequired()])
    # username = StringField("Username", validators=[DataRequired()])
    # password = PasswordField("Temporary Password", validators=[DataRequired()])
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
    submit = SubmitField("Save Edit")

    # Add UPLOAD_FOLDER to the form instance
    def __init__(self, *args, **kwargs):
        super(EditEmployeeForm, self).__init__(*args, **kwargs)
        self.upload_folder = current_app.config['UPLOAD_FOLDER']

    def save_image(self, image):
        if image:
            filename = secure_filename(image.filename)
            os.makedirs(self.upload_folder, exist_ok=True)  # Create the directory if it doesn't exist
            image_path = os.path.join(self.upload_folder, filename)
            image.save(image_path)
            return filename
        return None
