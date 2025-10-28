# E-commerce Project

This is a Django-based web application designed to manage roles, permissions, and modules. It includes features like authentication, role-based access control, and detailed module information.

## Features

-   Authentication for CRUD operations
-   Role-based access control
-   Nested serializers to include related data
-   Bulk deletion of roles
-   Search functionality for roles and permissions

## Requirements

-   Python 3.x
-   Django 3.x or higher
-   Django REST framework
-   PostgreSQL (or any other preferred database)

## Setup Instructions

### Clone the Repository

```sh
git clone git@github.com:rifadul/ecommerce-backend.git
cd palooi_project
```

### Create and Activate Virtual Environment

```sh
python3 -m venv palooi_venv
source palooi_venv/bin/activate  # On Windows use `venv\Scripts\activate`

```

### Deactivate Virtual Environment

```sh
deactivate

```

### Creating the requirements.txt File

```sh
pip freeze > requirements.txt

```

### Install Dependencies

```sh
pip install -r requirements.txt
```

### Configure Environment Variables
Create a `.env` file in the root directory and add the following environment variables:

```env
DJANGO_SECRET_KEY=django_secret_key
DJANGO_DEBUG=True
DB_NAME=your_db
DB_USER=your_admin
DB_PASSWORD=123456
DB_HOST=localhost
DB_PORT=5432
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,192.168.10.39
EMAIL_HOST_USER=youremail@gmail.com
EMAIL_HOST_PASSWORD=yourhostpassword
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
STRIPE_SECRET_KEY=your_stripe_secpet_key
STRIPE_PUBLIC_KEY=your_stripe_secpet_public_key
STRIPE_WEBHOOK_SECRET=your_stripe_secpet_webhook_secret
```

### Configure Database

Could you update the DATABASES setting in project/settings.py with your database credentials?

### Run Migrations

```sh
python3 manage.py makemigrations
python3 manage.py migrate

```

### Create Superuser

```sh
python3 manage.py createsuperuser
```

### Run the Development Server

```sh
python3 manage.py runserver

```

### Access the Application

Open your web browser and go to http://127.0.0.1:8000/ to access the application.

### API Endpoints

-   List Modules: GET /api/modules/
-   Create Module: POST /api/modules/
-   Retrieve Module: GET /api/modules/{id}/
-   Update Module: PUT /api/modules/{id}/
-   Partial Update Module: PATCH /api/modules/{id}/
-   Delete Module: DELETE /api/modules/{id}/

### Permissions

-   List Permissions: GET /api/permissions/
-   Create Permission: POST /api/permissions/
-   Retrieve Permission: GET /api/permissions/{id}/
-   Update Permission: PUT /api/permissions/{id}/
-   Partial Update Permission: PATCH /api/permissions/{id}/
-   Delete Permission: DELETE /api/permissions/{id}/

### Roles

-   List Roles: GET /api/roles/
-   Create Role: POST /api/roles/
-   Retrieve Role: GET /api/roles/{id}/
-   Update Role: PUT /api/roles/{id}/
-   Partial Update Role: PATCH /api/roles/{id}/
-   Delete Role: DELETE /api/roles/{id}/
-   Multiple Roles Delete: POST /api/roles/delete-multiple/?ids=id1,id2, id3...

## Example Requests

### Create a Module

```sh
POST /api/modules/
Content-Type: application/json

{
    "name": "User Management"
}
```

### Create a Permission

```sh
POST /api/permissions/
Content-Type: application/json

{
    "name": "Add User",
    "codename": "add_user",
    "module": "{module_id}"
}
```

### Create a Role

```sh
POST /api/roles/
Content-Type: application/json

{
    "name": "Admin",
    "permissions": ["{permission_id1}", "{permission_id2}"]
}
```
