# Palooi Project

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
git clone git@github.com:siam-zaag/palooi-backend.git
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
DJANGO_SECRET_KEY=django-insecure-rw-p-^dbo@)*vuu5)wghu5nt%j+39vf&30+!k@z$v5_oi(mdj5
DJANGO_DEBUG=True
DB_NAME=palooi_db
DB_USER=palooi_admin
DB_PASSWORD=123456
DB_HOST=localhost
DB_PORT=5432
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,192.168.10.39
EMAIL_HOST_USER=youremail@gmail.com
EMAIL_HOST_PASSWORD=yourhostpassword
CLIENT_ID=846693367049-alovjpulpma6ltn4b0iv3kuv8nqmklj7.apps.googleusercontent.com
CLIENT_SECRET=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
STRIPE_SECRET_KEY=sk_test_51PjSEoP56e6hXyY6HbldqvgPrNmpTZFruRa9WqsslFvkRg8X1f95NNwY62Y1mRhOfs3QIarLjybxnDq9qbO1GuTH00fbTmokFM
STRIPE_PUBLIC_KEY=pk_test_51PjSEoP56e6hXyY6LhlZcNvlF8lG5H6aDpRGrMmYbSn78u2qD4LkHGZYeMFCdwiG3O4mV20cZTqUz4c8x3GC0cPL00gmH2BhTG
STRIPE_WEBHOOK_SECRET=whsec_5e62a5c4a67c8645157a8d9b92f2e10c6e2916e547f865eead8bace92bc84077
```

### Configure Database

Update the DATABASES setting in palooi_project/settings.py with your database credentials.

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
-   Multiple Roles Delete : POST /api/roles/delete-multiple/?ids=id1,id2,id2...

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
