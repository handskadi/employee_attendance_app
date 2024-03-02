# dashboard.py

from models import mysql
from flask import Flask,  render_template, redirect, url_for

def dashboard(session):
    user = None
    user_id = session['user_id']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user where user_id=%s", (user_id,))
    user = cursor.fetchone()
    all_employees = []
    all_projects = []
    all_attendance = []
    manager_name = []
    is_manager = False
    logged_in_employee = None
    total_projects = 0
    active_projects  = 0
    inactive_projects = 0
    total_all_employees = 0
    total_general_managers  = 0
    total_project_managers  = 0
    total_employees = 0
    total_day_shift_hours  = 0
    total_days = 0
    total_night_shift_hours  = 0
    average_daily_hours =  0
    role = 'employee'
    employee_id = None
    project_id = None
    if 'user_id' in session:
        
        

        # Fetch all users' data
        # cursor.execute("SELECT * FROM user WHERE user_id=%s", (session['user_id'],))
        # user = cursor.fetchone()

        cursor.execute("SELECT * FROM user")
        all_users = cursor.fetchall()

        
        cursor.execute("SELECT * FROM employee WHERE user_id=%s", (session['user_id'],))
        logged_in_employee = cursor.fetchone()
        #print(logged_in_employee)
        role = logged_in_employee[8]
        #print("role"+ role)
        employee_id = logged_in_employee[0]
        if role == 'general_manager': 

            cursor.execute("""SELECT
                    e1.*,
                    CONCAT(e2.firstname, ' ', e2.lastname) AS manager_name,
                    p.project_name
                FROM
                    employee e1
                LEFT JOIN employee e2 ON
                    e1.manager_id = e2.employee_id
                LEFT JOIN project p ON
                    e1.project_id = p.project_id;""")

            all_employees = cursor.fetchall()

            cursor.execute("""
                SELECT 
                    COUNT(*) AS total_projects,
                    SUM(CASE WHEN is_active = 1 THEN 1 ELSE 0 END) AS active_projects,
                    SUM(CASE WHEN is_active = 0 THEN 1 ELSE 0 END) AS inactive_projects
                FROM project;
            """)
            total_projects, active_projects, inactive_projects = cursor.fetchone()

            cursor.execute("""
                SELECT 
                    COUNT(*) AS total_all_employees,
                    SUM(CASE WHEN role = 'general_manager' THEN 1 ELSE 0 END) AS total_general_managers,
                    SUM(CASE WHEN role = 'project_manager' THEN 1 ELSE 0 END) AS total_project_managers,
                    SUM(CASE WHEN role = 'employee' THEN 1 ELSE 0 END) AS total_employees
                FROM employee
            """)

            # Fetch the result
            employee_result = cursor.fetchone()
            total_all_employees, total_general_managers, total_project_managers, total_employees = employee_result

            cursor.execute("""
                SELECT 
                    SUM(day_shift_hours) AS total_day_shift_hours,
                    SUM(night_shift_hours) AS total_night_shift_hours,
                    COUNT(*) AS total_days, 
                    ROUND((SUM(day_shift_hours) + SUM(night_shift_hours)) / COUNT(*)) AS average_daily_hours
                FROM attendance;
            """)

            # Fetch the result
            attendance_result = cursor.fetchone()

            # Extracting values from the result
            total_day_shift_hours, total_night_shift_hours, total_days, average_daily_hours= attendance_result

            # print(total_projects)
            cursor.execute("SELECT * FROM project")
            all_projects = cursor.fetchall()
            cursor.execute("SELECT * FROM attendance")
            all_attendance = cursor.fetchall()
            cursor.execute("SELECT * FROM employee WHERE user_id=%s", (session['user_id'],))
            #logged_in_employee = cursor.fetchone()
            is_manager = True        

        elif role == 'project_manager':
            project_id = logged_in_employee[5]
            #print(project_id)
            # cursor.execute("SELECT * FROM employee where role='project_manager'")
            # productManagers = cursor.fetchall()
            
            # cursor.execute("SELECT employee_id FROM employee WHERE user_id=%s", (session['user_id'],))
            # employee_id = cursor.fetchone()
            cursor.execute("SELECT e.*,p.project_name FROM employee e LEFT JOIN project p on e.project_id=p.project_id WHERE e.role='employee' AND e.project_id=%s", ( project_id,))
            all_employees = cursor.fetchall()
            print(all_employees)
            # cursor.execute("SELECT role FROM employee WHERE user_id=%s", (session['user_id'],))
            # employee_role = cursor.fetchone()
            # if employee_role[0] != 'employee':
            #     is_manager = True

            # cursor.execute("SELECT project_id FROM employee WHERE user_id=%s", (session['user_id'],))
            # project_id = cursor.fetchone()
            cursor.execute("SELECT * FROM project where project_id=%s", (project_id,))
            all_projects = cursor.fetchall()
            
            cursor.execute("SELECT * FROM attendance where employee_id in (select employee_id from employee where project_id=%s) ", (project_id,))
            all_attendance = cursor.fetchall()

            cursor.execute("""
                SELECT 
                    COUNT(*) AS total_projects,
                    SUM(CASE WHEN is_active = 1 THEN 1 ELSE 0 END) AS active_projects,
                    SUM(CASE WHEN is_active = 0 THEN 1 ELSE 0 END) AS inactive_projects
                FROM project
                WHERE project_id=%s
            """, (project_id,))
            total_projects, active_projects, inactive_projects = cursor.fetchone()

            cursor.execute("""
                SELECT 
                    COUNT(*) AS total_all_employees,
                    SUM(CASE WHEN role = 'general_manager' THEN 1 ELSE 0 END) AS total_general_managers,
                    SUM(CASE WHEN role = 'project_manager' THEN 1 ELSE 0 END) AS total_project_managers,
                    SUM(CASE WHEN role = 'employee' THEN 1 ELSE 0 END) AS total_employees
                FROM employee WHERE project_id=%s;
            """, (project_id,))

            # Fetch the result
            employee_result = cursor.fetchone()
            total_all_employees, total_general_managers, total_project_managers, total_employees = employee_result

            cursor.execute("""
                SELECT
    SUM(a.day_shift_hours) AS total_day_shift_hours,
    SUM(a.night_shift_hours) AS total_night_shift_hours,
    COUNT(*) AS total_days,
    ROUND(
        (
            SUM(a.day_shift_hours) + SUM(a.night_shift_hours)
        ) / COUNT(*)
    ) AS average_daily_hours
FROM
    attendance a
LEFT JOIN employee e ON
    a.employee_id = e.employee_id
WHERE
    e.project_id = %s;
            """, (project_id,))
            # Fetch the result
            attendance_result = cursor.fetchone()

            # Extracting values from the result
            total_day_shift_hours, total_night_shift_hours, total_days, average_daily_hours= attendance_result

            #attendance


        else:
            #print("employee")
            cursor.execute("SELECT * FROM attendance WHERE employee_id=%s", (employee_id,))
            all_attendance = cursor.fetchall()
            


        cursor.close()
        # print(logged_in_employee)
        

        
        json =  {
                'user': user,
                'all_users': all_users,
                'all_employees': all_employees,
                'all_projects': all_projects,
                'all_attendance': all_attendance,
                'is_manager': is_manager,
                'logged_in_employee': logged_in_employee,
                'total_projects': total_projects,
                'active_projects': active_projects, 
                'inactive_projects': inactive_projects,
                'total_all_employees':total_all_employees,
                'total_general_managers': total_general_managers, 
                'total_project_managers': total_project_managers,
                'total_employees': total_employees,
                'total_day_shift_hours': total_day_shift_hours,
                'total_night_shift_hours': total_night_shift_hours, 
                'total_days': total_days,
                'average_daily_hours': average_daily_hours,
            }

        #print(all_employees[0])
        return json
    return redirect(url_for('login'))
