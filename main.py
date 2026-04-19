class CustomException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidUsernameException(CustomException):
    pass

class InvalidPasswordException(CustomException):
    pass

class UserAlreadyExistsException(CustomException):
    pass

class UserNotFoundException(CustomException):
    pass

class UserService:
    def __init__(self):
        self.users = {}

    def register(self, username, password):
        if username in self.users:
            raise UserAlreadyExistsException("User already exists")
        if len(username) < 3:
            raise InvalidUsernameException("Invalid username")
        if len(password) < 8:
            raise InvalidPasswordException("Invalid password")
        self.users[username] = password

    def login(self, username, password):
        if username not in self.users:
            raise UserNotFoundException("User not found")
        if self.users[username] != password:
            raise InvalidPasswordException("Invalid password")

    def get_user(self, username):
        if username not in self.users:
            raise UserNotFoundException("User not found")
        return self.users[username]

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Invalid deposit amount")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Invalid withdrawal amount")
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount

class BankService:
    def __init__(self):
        self.users = {}
        self.accounts = {}

    def create_account(self, username, initial_balance):
        if username in self.users:
            raise UserAlreadyExistsException("User already exists")
        self.users[username] = username
        self.accounts[username] = BankAccount(initial_balance)

    def get_account(self, username):
        if username not in self.users:
            raise UserNotFoundException("User not found")
        return self.accounts[username]

    def deposit(self, username, amount):
        if username not in self.users:
            raise UserNotFoundException("User not found")
        account = self.accounts[username]
        account.deposit(amount)

    def withdraw(self, username, amount):
        if username not in self.users:
            raise UserNotFoundException("User not found")
        account = self.accounts[username]
        account.withdraw(amount)

def main():
    user_service = UserService()
    user_service.register("admin", "password123")
    try:
        user_service.login("admin", "wrong_password")
    except CustomException as e:
        print(e.message)
    bank_service = BankService()
    bank_service.create_account("admin", 1000)
    bank_service.deposit("admin", 500)
    print(bank_service.get_account("admin").balance)

if __name__ == "__main__":
    main()