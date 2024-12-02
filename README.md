
# Department Management System

A Django-based application for managing departments in an organization. Users can create, edit, and delete department records with a user-friendly interface.

## Features
- Add new departments with a name and description.
- Edit existing department details.
- Soft-delete departments to deactivate them without removing them from the database.
- User-friendly web interface with responsive design.

## Project Structure
```
DepartmentManagement/
│
├── Department/
│   ├── migrations/
│   ├── templates/
│   │   ├── index.html
│   │   ├── createdepartment.html
│   │   ├── updatedepartment.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
├── db.sqlite3
└── README.md
```

## Prerequisites
- Python 3.8+
- Django 4.2+

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```

2. Navigate to the project directory:
   ```bash
   cd DepartmentManagement
   ```

3. Install required Python packages:
   ```bash
   pip install django
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Open the application in your browser at `http://127.0.0.1:8000/`.

## Usage

### Home Page
- Displays a list of active departments with their names and descriptions.
- Provides options to edit or delete a department.

### Create Department
- Navigate to `Create Department` in the sidebar.
- Fill in the department name and description and click `Create`.

### Edit Department
- Click `Edit` next to a department in the table.
- Update the details in the form and submit.

### Delete Department
- Click `Delete` next to a department in the table to deactivate it.

## Code Overview

### `models.py`
Defines the `Department` model with the following fields:
- `dept_id` (Primary Key)
- `dept_name` (Department Name)
- `description` (Description)
- `created_at` (Auto-generated timestamp)
- `updated_at` (Auto-updated timestamp)
- `status` (Boolean for active/inactive)

### `views.py`
Contains views for:
- Displaying the home page (`home`)
- Creating a new department (`createDepartment`)
- Editing a department (`updateDepartment`)
- Soft-deleting a department (`Deletedepartment`)

### `urls.py`
Maps URLs to views.

### Templates
- `index.html`: Home page with a list of departments.
- `createdepartment.html`: Form to add a new department.
- `updatedepartment.html`: Form to update department details.

## Styling
The templates include responsive designs using CSS to enhance the user interface.

## License
This project is licensed under the MIT License.
