# Doctor Account Management and Patient Linking System

## Table of Contents
- [Doctor Account Management and Patient Linking System](#doctor-account-management-and-patient-linking-system)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Technology Stack](#technology-stack)
  - [Project Structure](#project-structure)
  - [Setup and Installation](#setup-and-installation)
  - [API Endpoints](#api-endpoints)
  - [Models](#models)
    - [CustomUser](#customuser)
    - [PDF](#pdf)
    - [Patient](#patient)
    - [DoctorPatient](#doctorpatient)
  - [Authentication](#authentication)
  - [PDF Management](#pdf-management)
  - [Patient Management](#patient-management)
  - [Doctor-Patient Linking](#doctor-patient-linking)
  - [Error Handling](#error-handling)
  - [Future Improvements](#future-improvements)

## Introduction

This project is a backend system for a Doctor Account Management and Patient Linking application. It provides functionality for doctor registration and authentication, PDF file management, patient profile creation, and linking patients to doctors.

## Features

- Doctor account creation and authentication
- PDF upload and management for doctors
- Patient profile creation and management
- Linking patients to doctors
- Secure API endpoints with JWT authentication

## Technology Stack

- Python 3.8+
- Django 3.2+
- Django Rest Framework 3.12+
- PostgreSQL (as the database)
- Simple JWT for authentication

## Project Structure

```
backend/
├── manage.py
├── requirements.txt
├── backend/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── base/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── tests.py
```

## Setup and Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database in `settings.py` and run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

## API Endpoints

- `/api/register/`: POST - Register a new doctor
- `/api/token/`: POST - Obtain JWT token pair
- `/api/token/refresh/`: POST - Refresh JWT token
- `/api/pdf/upload/`: POST - Upload a PDF file
- `/api/pdf/list/`: GET - List uploaded PDFs for the logged-in doctor
- `/api/patients/create/`: POST - Create a new patient profile
- `/api/patients/list/`: GET - List patients associated with the logged-in doctor
- `/api/patients/link/`: POST - Link a patient to the logged-in doctor
- `/api/doctor/patients/`: GET - List all patients linked to the logged-in doctor

## Models

### CustomUser
- Extends Django's AbstractBaseUser
- Fields: email, name, specialty

### PDF
- Fields: doctor (ForeignKey to CustomUser), file, upload_date, title

### Patient
- Fields: name, email, date_of_birth

### DoctorPatient
- Fields: doctor (ForeignKey to CustomUser), patient (ForeignKey to Patient), date_assigned

## Authentication

The system uses JWT (JSON Web Tokens) for authentication. To access protected endpoints, include the access token in the Authorization header:

```
Authorization: Bearer <your-access-token>
```

## PDF Management

Doctors can upload PDF files and view their uploaded files. PDFs are stored in the media directory and associated with the uploading doctor.

## Patient Management

Doctors can create patient profiles and view a list of patients associated with them.

## Doctor-Patient Linking

The system allows linking patients to doctors, creating a many-to-many relationship between doctors and patients.

## Error Handling

The API provides clear error messages for invalid requests or unauthorized access. Check the response status code and message for details on any errors.

## Future Improvements

- Implement PDF deletion and updating functionality
- Add more detailed patient information and medical history
- Create a system for appointment scheduling
- Implement a notification system for doctors and patients

For any questions or issues, please open an issue in the project repository.