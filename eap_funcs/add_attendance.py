# attendance.py

from models import mysql, AttendanceForm
from flask import redirect, url_for, session, render_template

def add_attendance_route():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user WHERE email=%s", ('wafa@marouani.com',))
    user = cursor.fetchone()
    if user and 'user_id' in session and session['user_id'] == 1:
        form = AttendanceForm()
        if form.validate_on_submit():
            employee = form.employee.data
            attendance_date = form.attendance_date.data
            day_shift_hours = form.day_shift_hours.data
            night_shift_hours = form.night_shift_hours.data
            hours_worked = day_shift_hours + night_shift_hours
            comment = form.comment.data

            cursor.execute("INSERT INTO attendance (employee_id, attendance_date, day_shift_hours, night_shift_hours, hours_worked, comment) VALUES (%s,%s,%s,%s,%s,%s)", (employee, attendance_date, day_shift_hours, night_shift_hours, hours_worked, comment ))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('dashboard_route'))
        return render_template('attendance.html', form=form)
    return redirect(url_for('login'))
