

# Employee Attendance App 

## 1. Rename the document
- Employee Attendance App 

## 2. Architecture

### Diagram Description:
- The Web Client communicates with the Web Server through HTTP requests.
- The Web Server handles incoming requests, authenticates and authorizes users, and processes business logic.
- The Web Server interacts with the Database to store and retrieve data using an Object-Relational Mapping (ORM) tool.
- The API Endpoints expose functionalities related to users, general managers, project managers, projects, employees, and attendance.

## 3. APIs and Methods

### For Web Client Communication:
1. **/api/users**
   - GET: Retrieve information about users based on roles.
   - POST: Create a new user.
   
2. **/api/projects**
   - GET: Retrieve a list of projects and their details.
   - POST: Create a new project.
   
3. **/api/attendance**
   - GET: Retrieve attendance records for a specific employee.
   - POST: Log attendance for an employee.
   
### Internal Methods for External Clients:
4. **Class: EmployeeAttendanceAPI**
   - Method: `getEmployeeAttendance(employee_id)`
     - Returns attendance records for a specific employee.
   - Method: `logEmployeeAttendance(employee_id, date, shift_type, hours_worked)`
     - Logs attendance for an employee.
   - Method: `getProjects()`
     - Returns a list of projects and their details.

## 4. Data Modeling

### A. Database Relationships in Employee Attendance App Schema

1. **Employees Table:**
   - user_id (Primary Key)
   - username
   - password
   - role (General Manager, Project Manager, Employee)
   - name
   - cin
   - photo
   - project_id (Foreign Key referencing project_id in Project Table for Project Managers)
   - general_manager_id (Foreign Key referencing user_id in Users Table for General Managers)
   
2. **Project Table:**
   - project_id (Primary Key)
   - project_name
   - project_manager_id (Foreign Key referencing user_id in Users Table for Project Managers)
   
3. **Attendance Table:**
   - attendance_id (Primary Key)
   - employee_id (Foreign Key referencing user_id in Users Table for Employees)
   - date
   - shift_type (Day Shift, Night Shift)
   - shift_start_time
   - hours_worked
   - calculated_hours

### B. Database Relationships in Employee Management System

1. **Employees Table:**
   - One-to-Many Relationship with Project Table
   - One-to-Many Relationship with Attendance Table
   - Many-to-One Relationship with Employee Table (for General Manager)
   - Many-to-One Relationship with Employee Table (for Project Manager)
   
2. **Project Table:**
   - One-to-Many Relationship with Employees Table
   - Many-to-One Relationship with Employees Table (for Project Manager)
   
3. **Attendance Table:**
   - Many-to-One Relationship with Employees Table
   - Many-to-One Relationship with Project Table
   - Many-to-One Relationship with Users Table (for General Manager)
   - Many-to-One Relationship with Users Table (for Project Manager)

## 5. User Stories

1. **As a General Manager:**
   - View attendance reports for all projects.
   - Acceptance Criteria: Accessible from the dashboard, ability to filter reports, downloadable in Excel or PDF format.

2. **As a Project Manager:**
   - Add attendance records for employees in assigned projects.
   - Acceptance Criteria: Secure login, intuitive interface, notifications for errors.

3. **As an Employee:**
   - View own attendance records.
   - Acceptance Criteria: Accessible after login, clear display, ability to view records for specific time periods.

4. **As a General Manager:**
   - Assign Project Managers to specific projects.
   - Acceptance Criteria: Accessible through the admin panel, ability to assign or reassign Project Managers.

5. **As a Project Manager:**
   - Receive automated notifications for missing attendance records.
   - Acceptance Criteria: Customizable notification settings, real-time alerts, links within notifications.

## 6. Mockups

- View [Mohamad Kadi's Portfolio](https://www.mohamdkadi.com/) in the Portfolio section under Employee Attendance App.

