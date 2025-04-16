Django Authentication System
This is a Django-based RESTful API for user authentication, supporting login, signup with OTP (One-Time Password), profile completion, and account blocking for security. It uses Django REST Framework to provide endpoints for user management.
Features

User Signup with OTP: New users can sign up using their phone number and verify with a one-time password.
User Login: Registered users can log in with their phone number and password.
Profile Completion: Users can complete their profile with first name, last name, email, and password after OTP verification.
Account Blocking: Blocks users after three failed login or OTP attempts for one hour to prevent brute-force attacks.
RESTful Endpoints: Clean and secure API endpoints for all operations.

Tech Stack

Backend: Python, Django, Django REST Framework
Database: SQLite (default, configurable for PostgreSQL/MySQL)
Dependencies: django, djangorestframework, python-decouple

Project Structure
auth_system/
├── auth_system/
│   ├── settings.py      # Project settings
│   ├── urls.py         # Main URL routing
│   └── ...
├── users/
│   ├── models.py       # CustomUser, OTPCode, Block models
│   ├── serializers.py  # Serializers for API validation
│   ├── views.py        # API logic
│   ├── urls.py         # API endpoint routing
│   └── ...
├── db.sqlite3          # SQLite database
├── manage.py           # Django management script
└── requirements.txt    # Project dependencies

Installation

Clone the repository:
git clone https://github.com/your-username/auth-system.git
cd auth-system


Create a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:
pip install -r requirements.txt


Apply migrations:
python manage.py makemigrations
python manage.py migrate


Create a superuser (optional):
python manage.py createsuperuser


Run the server:
python manage.py runserver

The API will be available at http://localhost:8000.


API Endpoints



Endpoint
Method
Description
Authentication



/api/login/
POST
Login with phone and password
None


/api/otp/request/
POST
Request OTP for signup
None


/api/otp/verify/
POST
Verify OTP and create user
None


/api/profile/
POST
Complete user profile
Required


Example Requests

Request OTP:
curl -X POST http://localhost:8000/api/otp/request/ \
-H "Content-Type: application/json" \
-d '{"phone_number": "09198765432"}'

Response:
{"message": "کد OTP برای شماره 09198765432: 123456"}


Verify OTP:
curl -X POST http://localhost:8000/api/otp/verify/ \
-H "Content-Type: application/json" \
-c cookies.txt \
-d '{"phone_number": "09198765432", "code": "123456"}'

Response:
{"message": "تأیید شماره 09198765432 موفقیت‌آمیز است. لطفاً پروفایل خود را تکمیل کنید."}


Complete Profile:
curl -X POST http://localhost:8000/api/profile/ \
-H "Content-Type: application/json" \
-b cookies.txt \
-d '{"first_name": "Ali", "last_name": "Mohammadi", "email": "ali@example.com", "password": "newpassword123"}'

Response:
{"message": "پروفایل شماره 09198765432 با موفقیت تکمیل شد."}


Login:
curl -X POST http://localhost:8000/api/login/ \
-H "Content-Type: application/json" \
-d '{"phone_number": "09198765432", "password": "newpassword123"}'

Response:
{"message": "ورود با شماره 09198765432 موفقیت‌آمیز است."}



Testing
A test script (curl_test_commands.sh) is provided to test all scenarios, including successful signup, failed OTP attempts, blocking, profile completion, and login.

Make the script executable:
chmod +x curl_test_commands.sh


Run the script:
./curl_test_commands.sh



The script tests:

Signup with OTP for a new user (09198765432).
Three failed OTP attempts and blocking for another number (09198765433).
Profile completion for the successful user.
Login with password and failed login attempts.

Security Features

Account Blocking: Users are blocked for one hour after three failed login or OTP attempts.
OTP Validation: OTPs are time-sensitive and single-use.
Unique Phone Numbers: Ensures no duplicate registrations.

Configuration

Database: Uses SQLite by default. To use PostgreSQL or MySQL, update settings.py.
Environment Variables: Use python-decouple for sensitive settings (e.g., SECRET_KEY).

Contributing

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit your changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request.

License
This project is licensed under the MIT License.
Contact
For issues or suggestions, open an issue on GitHub or contact [your-email@example.com].
