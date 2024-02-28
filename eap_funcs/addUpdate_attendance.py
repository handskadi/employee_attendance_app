# attendance.py

from models import mysql, AttendanceForm
from flask import redirect, url_for, session, render_template, jsonify,request
import datetime


def get_attendance_route():
    cursor = mysql.connection.cursor()
    
    #retrieve attendance id from request : 
    attendance_id = request.form['attendance_id']
    print(attendance_id)

    cursor.execute("SELECT a.*,CONCAT(e.lastname,' ', e.firstname) FROM attendance a LEFT JOIN employee e on a.employee_id = e.employee_id WHERE attendance_id=%s ", (attendance_id,))
    attendance = cursor.fetchone()
    #print(attendance)
    attendance += (attendance[2].strftime('%Y-%m-%d'),)
    
    if 'user_id' in session :
        return jsonify(attendance)
    return redirect(url_for('login'))


def update_attendance_route():
    cursor = mysql.connection.cursor()
    
    #retrieve attendance id from request : 
    attendance_id = request.form.get("attendanceId")
    employee_id = request.form.get("employeeId")
    attendance_date = request.form.get("attendanceDate")
    day_shift_hours = request.form.get("day_shift_hours")
    night_shift_hours = request.form.get("night_shift_hours")
    hours_worked = int(day_shift_hours) + int(night_shift_hours)
    comment = request.form.get("comment")
    
    print(attendance_id)
    if 'user_id' in session :
        if attendance_id :
            result = cursor.execute("UPDATE attendance SET attendance_date= %s, day_shift_hours =%s,night_shift_hours =%s, hours_worked =%s, comment =%s WHERE attendance_id=%s", (attendance_date,day_shift_hours,night_shift_hours,hours_worked,comment,attendance_id,))
            a = mysql.connection.commit()
            
        else : 
            # create a new attendance
            result = cursor.execute("INSERT INTO attendance (employee_id, attendance_date, day_shift_hours, night_shift_hours, hours_worked, comment) VALUES (%s,%s,%s,%s,%s,%s)", (employee_id, attendance_date, day_shift_hours, night_shift_hours, hours_worked, comment ))
            mysql.connection.commit()
            
        cursor.close()
        print(result)
        if result :
            return jsonify(result)
        else : 
            return jsonify("An Error has occured !")
    return redirect(url_for('login'))