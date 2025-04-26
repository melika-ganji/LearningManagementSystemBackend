# LearningManagementSystemBackend

A Django-based Learning Management System where users can enroll in courses, view course content (video, audio, text), and interact through comments.
The system includes user management, courses with categories, a dynamic search feature, and role-based permissions (admin, professor, student).
_____________________________________________________________________________________________________________________________________________________

# Features
Authentication & Authorization

Custom user model with roles: Admin, Professor, Student

Login, registration, and permission-based access control

Course Management

Create, update, list, and delete courses

Support for course content: video, audio, text

Pricing with price change history

Category Management

Organize courses into categories

Comments

Authenticated users can comment on courses

Search System

Search for users, courses, and categories using keywords

Role-based restrictions for searching users

Filtering

Advanced filtering with django-filter

Testing

Unit tests for search functionality

Secure APIs

Built with Django Rest Framework (DRF)
______________________________________________________________________________________________________________________________________________________

# Technologies Used

Python 3.11

Django 5.x

Django Rest Framework

Django Filters

PostgreSQL

JWT

Celery
