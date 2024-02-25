# update_employee.py

from models import mysql, EditEmployeeForm, app
from flask import redirect, url_for, session, render_template, flash, request

def update_employee_route(employee_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM employee WHERE employee_id = %s", (employee_id,))
    employee = cursor.fetchone()
    cursor.close()

    if not employee:
        flash("Employee not found", "error")
        return redirect('page_not_found')

    form = EditEmployeeForm()
    form.upload_folder = app.config['UPLOAD_FOLDER']
    if request.method == 'GET': 
        form = EditEmployeeForm(
            obj=employee, 
            first_name=employee[6], 
            last_name=employee[7], 
            role=employee[8], 
            hire_date=employee[2], 
            end_employment=employee[3], 
            project=employee[5],
            manager=employee[4],
            image=employee[9])  # Populate the form with existing data
        
    if form.validate_on_submit():
        # Update employee details based on form data
        uploaded_image = form.image.data
        if uploaded_image is None and employee[9] != 'default.png':
            uploaded_image = employee[9]
        elif uploaded_image is None and employee[9] == 'default.png':
            uploaded_image = 'default.png'
        else: 
            uploaded_image = form.image.data.filename
            
        # Save the image and get the filename
        form.save_image(form.image.data)

        updated_data = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'role': form.role.data,
            'hire_date': form.hire_date.data,
            'end_employment': form.end_employment.data,
            'project': form.project.data,
            'manager': form.manager.data,
            'image': uploaded_image
        }

        # Update the database with the new data
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE employee
            SET firstname = %(first_name)s, lastname = %(last_name)s,
                role = %(role)s,  hire_date = %(hire_date)s,
                end_employment = %(end_employment)s, project_id= %(project)s, manager_id = %(manager)s, image_filename = %(image)s
            WHERE employee_id = %(employee_id)s
        """, {**updated_data, 'employee_id': employee_id})
        mysql.connection.commit()
        cursor.close()

        flash("Employee details updated successfully")
        return redirect(url_for('edit_employee', employee_id=employee_id))

    return render_template('edit_employee.html', form=form, employee_id=employee_id)
