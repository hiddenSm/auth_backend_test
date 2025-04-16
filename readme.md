# Django Authentication System

A Django-based RESTful API for user authentication, providing signup with OTP (One-Time Password), login with password, profile completion, and account blocking for security. Built with Django REST Framework, it ensures secure and scalable user management.

## Features

- **OTP Signup**: Register new users via phone number with OTP verification.
- **Password Login**: Authenticate registered users using phone number and password.
- **Profile Completion**: Allow users to set first name, last name, email, and password post-OTP verification.
- **Account Blocking**: Block users for 1 hour after 3 failed login or OTP attempts to prevent brute-force attacks.
- **IP Tracking**: Supports unique IP tracking per phone number using `X-Forwarded-For` header for testing.
- **CSRF Exemption**: Custom session authentication to disable CSRF checks for API endpoints.

## Tech Stack

- **Backend**: Python, Django, Django REST Framework
- **Database**: SQLite (default, configurable for PostgreSQL/MySQL)
- **Dependencies**: django, djangorestframework, jq (for test script)

## Project Structure

```
auth_system/
├── auth_system/
│   ├── settings.py      # Project settings (REST Framework, custom user model)
│   ├── urls.py          # Main URL routing
│   └── ...
├── users/
│   ├── models.py        # CustomUser, OTPCode, Block models
│   ├── serializers.py   # Serializers for API validation
│   ├── views.py         # API logic with IP tracking and CSRF exemption
│   ├── urls.py          # API endpoint routing
│   └── ...
├── db.sqlite3           # SQLite database
├── manage.py            # Django management script
├── curl_test_commands.sh # Test script for API endpoints
└── requirements.txt     # Project dependencies
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/auth-system.git
   cd auth-system
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Run the server:
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000`.

## API Endpoints

| Endpoint            | Method | Description                             |
|---------------------|--------|-----------------------------------------|
| `/api/login/`       | POST   | Login with phone number and password    |
| `/api/otp/request/` | POST   | Request OTP for signup                  |
| `/api/otp/verify/`  | POST   | Verify OTP and create user              |
| `/api/profile/`     | POST   | Complete user profile (Session required)|

## Example Requests

### Request OTP
```bash
curl -X POST http://localhost:8000/api/otp/request/ \
-H "Content-Type: application/json" \
-H "X-Forwarded-For: 192.168.1.100" \
-d '{"phone_number": "09191111111"}'
```

Response:
```json
{"message": "OTP code for phone number 09191111111: 123456"}
```

### Verify OTP
```bash
curl -X POST http://localhost:8000/api/otp/verify/ \
-H "Content-Type: application/json" \
-H "X-Forwarded-For: 192.168.1.100" \
-c cookies.txt \
-d '{"phone_number": "09191111111", "code": "123456"}'
```

Response:
```json
{"message": "verifying OTP for 09191111111 is susuccessful. please complete your profile."}
```

### Complete Profile
```bash
curl -X POST http://localhost:8000/api/profile/ \
-H "Content-Type: application/json" \
-H "X-Forwarded-For: 192.168.1.100" \
-b cookies.txt \
-d '{"first_name": "Ali", "last_name": "Mohammadi", "email": "ali@example.com", "password": "newpassword123"}'
```

Response:
```json
{"message": "09191111111 profile is susuccessfully complete."}
```

### Login
```bash
curl -X POST http://localhost:8000/api/login/ \
-H "Content-Type: application/json" \
-H "X-Forwarded-For: 192.168.1.100" \
-d '{"phone_number": "09191111111", "password": "newpassword123"}'
```

Response:
```json
{"message": "09191111111 is logged in."}
```

## Testing

A comprehensive test script (`curl_test_commands.sh`) is included to verify all API functionalities. It requires `jq` for parsing JSON responses.

### Install jq (if not installed):
- On Ubuntu/Debian:
  ```bash
  sudo apt-get install jq
  ```
- On macOS:
  ```bash
  brew install jq
  ```

### Run the script:
```bash
chmod +x curl_test_commands.sh
./curl_test_commands.sh
```

### The script tests the following scenarios:
1. **Successful Signup**: OTP request and verification for `09191111111` (IP: `192.168.1.100`).
2. **Failed Attempts & Blocking**: Three failed OTP attempts for `09190000000` (IP: `192.168.1.101`), leading to a 1-hour block.
3. **Profile Completion**: Completing the profile for `09191111111`.
4. **Login with Password**: Successful login and three failed login attempts for `09191111111`.

## Security Features

- **Account Blocking**: Blocks users for 1 hour after 3 failed login or OTP attempts.
- **IP Tracking**: Uses `X-Forwarded-For` header for unique IP assignment per phone number in testing.
- **OTP Validation**: OTPs are single-use and time-sensitive (expires after a set period).
- **CSRF Exemption**: Custom `CSRFExemptSessionAuthentication` for seamless API usage.
- **Unique Phone Numbers**: Prevents duplicate registrations with the same phone number.

<!-- ## Configuration

- **Database**: SQLite by default. Update `settings.py` for PostgreSQL or MySQL.
- **IP Handling**: Supports `X-Forwarded-For` for testing; in production, ensure proper proxy configuration.
- **Authentication**: Session-based authentication for `/api/profile/`; no CSRF checks required.

## Contributing

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a pull request.

## License

This project is licensed under the MIT License.

## Contact

For issues or suggestions, open an issue on GitHub or contact [your-email@example.com]. -->
