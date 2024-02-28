# attendance.py

from models import mysql, ListAttendanceForm
from flask import redirect, url_for, session, render_template , request

from datetime import datetime, timedelta

def get_attendance_data(employee_id, date_from, date_to):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM attendance WHERE employee_id = %s AND attendance_date BETWEEN %s AND %s"
    cursor.execute(query, (employee_id, date_from, date_to))
    attendance_list = cursor.fetchall()
    print(attendance_list)
    return attendance_list


def display_dates_between(start_date, end_date, frequency):
    # Convert start_date and end_date strings to datetime objects
    #start_date = datetime.strptime(start_date, '%Y-%m-%d')
    #end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Initialize a list to store the dates
    dates = []

    # Loop through the dates from start_date to end_date
    current_date = start_date
    while current_date <= end_date:
        # Append the current date to the list
        dates.append(current_date.strftime('%Y-%m-%d'))
        
        # Increment the current date based on the frequency
        if frequency == 'daily':
            current_date += timedelta(days=1)
        elif frequency == 'weekly':
            current_date += timedelta(weeks=1)
        elif frequency == 'monthly':
            # Add a month (note: this doesn't keep the same day of the month)
            current_date = current_date.replace(day=1) + timedelta(days=32)
            current_date = current_date.replace(day=1)

    return dates




def list_attendance_route():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user WHERE email=%s", ('wafa@marouani.com',))
    user = cursor.fetchone()
    dates = []
    employees = []
    list_employees = []
    if user and 'user_id' in session :
        form = ListAttendanceForm()
        print('test')
        #if form.validate_on_submit():
        date_from = form.date_from.data
        date_to = form.date_to.data
        if request.method == 'POST' :
            print(date_from)
            print(date_to)
            dates = display_dates_between(date_from, date_to, 'daily')
            print(dates)
                # cursor.execute("INSERT INTO attendance (employee_id, attendance_date, day_shift_hours, night_shift_hours, hours_worked, comment) VALUES (%s,%s,%s,%s,%s,%s)", (employee, attendance_date, day_shift_hours, night_shift_hours, hours_worked, comment ))
                # mysql.connection.commit()
                # cursor.close()
            #return redirect(url_for('dashboard_route'))

            #get the project ID

            #For General manager to do
            # for project manager

            cursor.execute("SELECT * FROM employee WHERE user_id=%s", (session['user_id'],))
            user_informtion = cursor.fetchone()
            
            if user_informtion[8] == 'project_manager' :      
                print("am a PM!")      
                cursor.execute("SELECT * FROM employee WHERE project_id=%s" , (user_informtion[5],))
            
            elif user_informtion[8] == 'employee' :
                cursor.execute("SELECT * FROM employee where user_id=%s", (session['user_id'],))
                # get employees assigned to this project
            else:
                cursor.execute("SELECT * FROM employee")
            
            employees = cursor.fetchall()

            
            #get attendances of each employee in that timeframe
            for employee in employees:
                print("id "+str(employee[0]))
                attendance_list = get_attendance_data(employee[0], date_from,date_to)
                print(attendance_list)
                employee += ( attendance_list,)
                list_employees.append(employee)
            print(list_employees)
            
                # mysql.connection.commit()
                # cursor.close()
        return render_template('list_attendance.html', form=form,dates=dates, employees= list_employees)
    return redirect(url_for('login'))



    

