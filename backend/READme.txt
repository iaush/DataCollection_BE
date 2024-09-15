# FastAPI Project

## Overview

This FastAPI project includes user registration, login, and retrieval features. 
It utilizes AWS services for email notifications and PostgreSQL on AWS RDS for data storage. 
Custom middleware is implemented for rate limiting and XSS protection.

## Setup Instructions

### 1. Initialize Environment

**Remove the existing virtual environment if needed:**
rm -rf venv

Create a new Python virtual environment:
python -m venv venv

Activate the virtual environment:
.\venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Create a .env file in the /backend folder with the following content:
AWS_ACCESS_KEY_ID=<your_access_key_id>
AWS_SECRET_ACCESS_KEY=<your_secret_access_key>
AWS_DEFAULT_REGION=<your_region>
SECRET_KEY=<your_secret_key>



### 2. AWS Services
AWS SES: Used for sending email notifications. 
Ensure that your AWS account has SES full access on IAM and that you have a verified domain or email address 
to send emails from.

AWS RDS: PostgreSQL database running on AWS. Update the DATABASE_URL variable in src/database/database.py 
if using a different database instance. Send a GET request to /init to initialize the database tables 
if running a new local environment or new instance.

### 3. Running the Application

Activate the virtual environment:
.\venv\Scripts\activate

Run the FastAPI application:
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

### 4. Middleware
Rate Limiting Middleware
Class: RateLimitter
Purpose: Limits the number of requests from a single IP address within a specified time window to prevent abuse and DDoS attacks.
Configuration: Configured with max_requests and time_window.
Usage: Applied globally to the application.

XSS Protection Middleware
Class: XSSMiddleware
Purpose: Provides basic protection against XSS attacks by setting security-related headers.
Configuration: Sets Content-Security-Policy, X-Content-Type-Options, X-Frame-Options, and X-XSS-Protection headers.
Usage: Applied globally to the application.


### 5. API Endpoints

User Registration
Path: /register_user/
Method: POST
Description: Registers a new user. Sends a notification email upon successful registration.
Request Body:
json
{
  "email": "user@example.com",
  "password": "password123",
  "contact_num": "1234567890",
  "company": "Company Name",
  "name": "User Name",
  "is_member": true,
  "role": "user"
}


User Login
Path: /login
Method: POST
Description: Logs in a user and returns a JWT token for authentication.
Request Body:
{
  "username": "user@example.com",
  "password": "password123"
}
Response:
{
  "msg": "Login successful",
  "token": "jwt_token_here"
}


Token Endpoint
Path: /token
Method: POST
Description: OAuth2 endpoint for logging in and receiving a JWT token.

Request Body:
{
  "username": "user@example.com",
  "password": "password123"
}
Response:
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}


Get Users
Path: /get_users/
Method: GET
Description: Retrieves all users from the database. Requires authentication.
Response:
[
  {
    "id": 1,
    "email": "user@example.com",
    "contact_num": "1234567890",
    "company": "Company Name",
    "name": "User Name",
    "is_member": true,
    "role": "user"
  }
]


