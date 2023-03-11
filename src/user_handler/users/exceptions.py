class UserAlreadyExistsException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"{type(self).__name__}: {self.message}"


class UserInvalidEmailException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"{type(self).__name__}: {self.message}"


class UserNotExistException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"{type(self).__name__}: {self.message}"


class UserWrongPasswordException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"{type(self).__name__}: {self.message}"


class UserWrongTokenSchemaException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"{type(self).__name__}: {self.message}"
