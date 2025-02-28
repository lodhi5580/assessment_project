Django JWT CRUD with RBAC (Role-Based Access Control)

Project Overview : -

This project is a Django REST Framework (DRF) application with JWT-based authentication and Role-Based Access Control (RBAC).
It includes user registration, login, logout, and CRUD operations on books with different permission levels for admins and users. 
Swagger is also implemented for API documentation.

Features :-

User authentication using JWT (Login, Register, Logout)

Role-Based Access Control (RBAC)

CRUD operations for books

Django Admin Panel

API Documentation using Swagger

Installation:-

1. Clone the repository:-
    git clone <repository-url>
    cd jwt_crud_rbac

2.Create and activate a virtual environment:-
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate     # On Windows

3. Install dependencies:-
    pip install -r req.txt

4. Apply migrations:-
    python manage.py makemigrations
    python manage.py migrate    

5. Create a superuser (optional for admin access):-
    python manage.py createsuperuser

6. Run the development server:-
    python manage.py runserver



API Endpoints

Authentication:

    POST /api/v1/register/ → Register a new user

    POST /api/v1/login/ → Login and get JWT token

    POST /api/v1/logout/ → Logout and blacklist refresh token

    POST /api/token/refresh/ → Refresh access token



Users (Admin Only):

    GET /api/v1/users/ → List all users

    GET /api/v1/users/admin_only/ → List all users (Admin access required)

    GET /api/v1/users/user_only/ → List all regular users

Books:

    GET /api/v1/books/ → Get list of books (Admin: all books, User: only own books)

    POST /api/v1/books/ → Create a book (Authenticated users)

    GET /api/v1/books/{id}/ → Retrieve a book by ID

    PUT /api/v1/books/{id}/ → Update a book by ID

    DELETE /api/v1/books/{id}/ → Delete a book by ID

    GET /api/v1/books/admin_books/ → Admin can view all books

    GET /api/v1/books/user_books/ → Users can view only their books


How to Test the API -

Using Swagger UI:-

    1. Run the server and go to:-
        http://127.0.0.1:8000/swagger/
    2. Authenticate using JWT (Login and copy the access token).
    3. Click Authorize and enter Bearer <your-access-token>.
    4. Test all endpoints directly from the Swagger UI.

Using cURL (Command Line)

    Login and get token:-
        curl -X POST http://127.0.0.1:8000/api/v1/login/ -H "Content-Type: application/json" -d '{"username": "yourusername", "password": "yourpassword"}'
        
        Access protected endpoints (replace <TOKEN> with your access token):
            curl -H "Authorization: Bearer <TOKEN>" http://127.0.0.1:8000/api/v1/books/


Admin Panel

Access Django admin at: http://127.0.0.1:8000/admin/

Login using the superuser credentials created earlier.

Configuration

Update Allowed Hosts

Modify settings.py to allow your domain/IP:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

Enable Swagger UI

Ensure drf_yasg is installed and included in INSTALLED_APPS in settings.py:-

    INSTALLED_APPS = [
    'drf_yasg',
    'rest_framework',
    'rest_framework_simplejwt',
    'crud_api',
    'django.contrib.admin',
    'django.contrib.auth',
    ]

Add the following in urls.py:

    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

        schema_view = get_schema_view(
            openapi.Info(
                title="JWT CRUD API",
                default_version='v1',
                description="API documentation for JWT authentication and CRUD operations",
            ),
            public=True,
            permission_classes=(permissions.AllowAny,),
        )

        urlpatterns += [
            path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        ]



Troubleshooting

"Authentication credentials were not provided."

Ensure you are sending the Authorization: Bearer <TOKEN> header in your requests.

Obtain a token from /api/v1/login/.

Use the token in the Authorization header for subsequent requests.


Foreign Key Constraint Errors

Ensure the referenced user or book exists before creating related records.

Check database constraints with sqlite3 db.sqlite3 and PRAGMA foreign_keys = ON;.

Admin Panel Not Loading

Run python manage.py createsuperuser to create an admin account.

Ensure INSTALLED_APPS includes 'django.contrib.admin'.

License

This project is licensed under the MIT License.
