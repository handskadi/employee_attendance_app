# Employee Attendance App - README

## Project Name and Tagline:
**Name:** Employee Attendance App  
**Tagline:** Streamlining Workforce Tracking and Reporting  
**Description:**
The Employee Attendance App is designed to efficiently track employee time and attendance, providing project managers and general managers with a user-friendly interface. The app categorizes users into General Managers and Project Managers, where each Project Manager has control over their respective projects, manually adding attendance records. General Managers can access all projects and generate comprehensive attendance reports in Excel or PDF formats.

## Team Members:
- **Mohamed KADI**
  - **Role:** Full Stack Developer
  - **Why:** As a solo developer, I can seamlessly manage and implement all facets of the Employee Attendance App, spanning frontend development for user interaction to backend development for data storage and processing.

## Technologies:
- **Languages:**
  - Python (Flask for backend, HTML/CSS/JavaScript for frontend)
- **Database:**
  - MySQL
- **Deployment:**
  - Vagrant, Apache, Nginx
- **Version Control:**
  - Git
- **Other Tools:**
  - Trello for project management

**Alternative Technology Choice:**
- **For Frontend:** React.js instead of plain JavaScript.
- **For Deployment:** ...

**Reasoning:**
I opted for plain JavaScript for simplicity, but React.js could offer more structured and interactive components. Apache and Nginx were chosen for their user-friendly deployment features.

## Challenge Statement:
**Problem:** Automate and streamline the attendance tracking process for workers.  
**Not Solve:** This app will not handle payroll processing or HR functions.  
**Users:** Aimed at managers and team leaders for efficient monitoring of worker attendance.

## Risks:
**Technical Risks:**
- Integration issues with chosen technologies
- Potential bugs in the attendance tracking algorithm

**Non-Technical Risks:**
- Users may resist the transition to a digital attendance system.

## Infrastructure:
- **Branching/Merging:** GitHub flow for version control.
- **Deployment Strategy:** Continuous integration and deployment using Vagrant, Apache, Nginx.
- **Populating App with Data:** Manual entry during the testing phase.

## Architecture

### Diagram Description:
- The Web Client communicates with the Web Server through HTTP requests.
- The Web Server handles incoming requests, authenticates and authorizes users, and processes business logic.
- The Web Server interacts with the Database to store and retrieve data using an Object-Relational Mapping (ORM) tool.
- The API Endpoints expose functionalities related to users, general managers, project managers, projects, employees, and attendance.

## APIs and Methods

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

## Data Modeling

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

## User Stories

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

## Mockups

- View [Mohamad Kadi's Portfolio](https://www.mohamdkadi.com/) in the Portfolio section under Employee Attendance App.

