# update_project.py

from models import mysql, UpdateProjectForm
from flask import redirect, url_for, session, render_template, flash, request

def update_project_route(project_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM project WHERE project_id = %s", (project_id,))
    project = cursor.fetchone()
    cursor.close()

    if not project:
        flash("Project not found", "error")
        return redirect('page_not_found')

    form = UpdateProjectForm()
    if request.method == 'GET':
        form = UpdateProjectForm(
            project_name=project[1],  # Assuming project_name is the second column in your database
            is_active=project[2],     # Assuming is_active is the third column in your database
            description=project[3]    # Assuming description is the fourth column in your database
        )  # Populate the form with existing data

    if form.validate_on_submit():
        project_name = form.project_name.data
        is_active = form.is_active.data
        description = form.description.data

        # Update the database with the new data
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE project
            SET project_name = %s, is_active = %s, description = %s
            WHERE project_id = %s
        """, (project_name, is_active, description, project_id))
        mysql.connection.commit()
        cursor.close()

        flash("Project details updated successfully")
        return redirect(url_for('list_projects'))

    return render_template('update_project.html', form=form, project_id=project_id)
