class EmailValidationErrror(Exception):
    def __init__(self, message):
        super().__init__(message)


class PhoneNumberVaildationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class FirstNameValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)
