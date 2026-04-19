class CustomException(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code
        super().__init__(message)

class InvalidUsernameError(CustomException):
    def __init__(self, message="Invalid username", code=400):
        super().__init__(message, code)

class InvalidPasswordError(CustomException):
    def __init__(self, message="Invalid password", code=401):
        super().__init__(message, code)

class InvalidEmailError(CustomException):
    def __init__(self, message="Invalid email", code=402):
        super().__init__(message, code)

class UserExistsError(CustomException):
    def __init__(self, message="User already exists", code=403):
        super().__init__(message, code)

class UserNotFoundError(CustomException):
    def __init__(self, message="User not found", code=404):
        super().__init__(message, code)

class InvalidInputError(CustomException):
    def __init__(self, message="Invalid input", code=405):
        super().__init__(message, code)

class AuthenticationError(CustomException):
    def __init__(self, message="Authentication failed", code=406):
        super().__init__(message, code)

def validate_username(username):
    if not username:
        raise InvalidUsernameError
    if len(username) < 3:
        raise InvalidUsernameError("Username is too short")
    if len(username) > 20:
        raise InvalidUsernameError("Username is too long")

def validate_password(password):
    if not password:
        raise InvalidPasswordError
    if len(password) < 8:
        raise InvalidPasswordError("Password is too short")
    if len(password) > 20:
        raise InvalidPasswordError("Password is too long")

def validate_email(email):
    if not email:
        raise InvalidEmailError
    if "@" not in email:
        raise InvalidEmailError("Invalid email format")

def main():
    try:
        username = input("Enter your username: ")
        validate_username(username)
        password = input("Enter your password: ")
        validate_password(password)
        email = input("Enter your email: ")
        validate_email(email)
    except CustomException as e:
        print(f"Error {e.code}: {e.message}")

if __name__ == "__main__":
    main()