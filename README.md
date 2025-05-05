# Gym Management System
A Gym Management System built with **Django (backend)** to streamline and manage operations, including memberships, subscriptions, class schedules, and trainer assignments/info. This system aims to improve administrative efficiency and enhance the user experience for both gym and staff.

## Features
- **User Authentication:** Secure login/logout system for admins and trainers.
- **Membership Management:** Add, update, and delete members.
- **Subscription Plans:** Different billing durations and pricing.
- **Class Scheduling:** Assign trainers, locations, and times for classes.
- **Trainer Management:** View and manage trainer assignments.
- **Admin Panel:** Django Admin integration for easy backend management.

## Technologies Used
- Python & Django REST Framework 
- MySQL Database (Configurable)
- Django Serializers & Views
- JWT Authentication

| Requirements                           |
| ------------                           |
| asgiref >= 3.8.1                       |
| Django >= 5.1.5                        |
| django-cors-headers >= 4.7.0           |
| djangorestframework >= 3.15.2          |
| djangorestframework_simplejwt >= 5.4.0 |
| psycopg2-binary >= 2.9.10              |
| PyJWT >= 2.10.1                        |
| python-dotenv >= 1.0.1                 |
| pytz >= 2025.1                         |
| sqlparse >= 0.5.3                      |
| tzdata >= 2025.1                       |



## Install

1. Clone repository
```
git clone https://github.com/your-username/gym-management-system.git
```

2. Create a virtual environment in PowerShell terminal and activate it:      
``` 
python -m venv .venv
.venv/Scripts/activate 
```

3. Install Required packages
```
pip install -r requirements.txt
```

4. Run project locally
```
python manage.py runserver
```
