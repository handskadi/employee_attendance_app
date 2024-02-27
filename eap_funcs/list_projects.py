# list_projects.py

from models import mysql

def projects_route(session):
    if 'user_id' in session:
        user_id = session['user_id']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM user where user_id=%s", (user_id,))
        user = cursor.fetchone()
        all_employees = []
        all_projects = []
        all_attendance = []
        manager_name = []
        is_manager = False
        logged_in_employee = []

        # Fetch all users' data
        cursor.execute("SELECT * FROM user")
        all_users = cursor.fetchall()
        if session['user_id'] == 1:
            cursor.execute("""
            SELECT 
                    p.*,
                    CONCAT(e.firstname, ' ', e.lastname) AS manager_name
                FROM 
                    project p
                LEFT JOIN 
                    employee e ON p.project_id = e.project_id
                WHERE 
                    e.role = 'project_manager';
                """)
            all_projects = cursor.fetchall()
            print(all_projects)
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

            
            
            cursor.execute("SELECT * FROM employee WHERE user_id=%s", (session['user_id'],))
            logged_in_employee = cursor.fetchone()
            is_manager = True

        else:
            cursor.execute("SELECT * FROM employee where role='project_manager'")
            productManagers = cursor.fetchall()
            for pm in productManagers:
                if pm[8] == 'project_manager':
                    cursor.execute("SELECT employee_id FROM employee WHERE user_id=%s", (session['user_id'],))
                    employee_id = cursor.fetchone()
                    cursor.execute("SELECT * FROM employee WHERE role='employee' AND manager_id=%s  OR user_id=%s", ( employee_id, session['user_id'],))
                    all_employees = cursor.fetchall()

                    cursor.execute("SELECT role FROM employee WHERE user_id=%s", (session['user_id'],))
                    employee_role = cursor.fetchone()
                    if employee_role[0] != 'employee':
                        is_manager = True

                    cursor.execute("SELECT project_id FROM employee WHERE user_id=%s", (session['user_id'],))
                    project_id = cursor.fetchone()
                    cursor.execute("SELECT * FROM project where project_id=%s", (project_id,))
                    all_projects = cursor.fetchall()

                    cursor.execute("SELECT * FROM attendance where employee_id=%s", (employee_id))
                    all_attendance = cursor.fetchall()

                else:
                    cursor.execute("SELECT * FROM attendance WHERE employee_id=%s", (employee_id,))
                    all_attendance = cursor.fetchall()

        cursor.close()

        if user:
            return {
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
                'average_daily_hours': average_daily_hours
            }
