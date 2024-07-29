# Task_manager
Flask web application and RESTful API for it

## Development stages
- [x] html templates
- [x] base models
- [x] unit tests
- [x] user credentials processing
- [x] JWT tokens for emails

## How to
### Run the application
1. `cd Task_manager`
2. Create a virtual environment
3. `pip install -r requirements.txt`
4. `flask run`
5. Navigate to `http://127.0.0.1:5000/` in your browser
6. Use the following credentials to log in
```
login: test
password: test
```

### Run the tests
1. Activate the virtual environment
2. `python tests.py`

### Check the password reset feature
1. Run the application
2. Start an emulated email server: `python -m smtpd -n -c DebuggingServer localhost:<your_port>`
3. Set two environment variables
```
export MAIL_SERVER=localhost
export MAIL_PORT=<your_port>
```
4. Navigate to `http://127.0.0.1:5000/reset_password_request` (can be done through the login page)
5. Request password reset for this email: `test@example.com`
6. Check the server for the reset link
