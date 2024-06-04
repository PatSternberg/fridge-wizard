# file: ./backend/backend/middleware/authenticator
import re
from django.core.exceptions import ValidationError

class Validator:

    # Set minimum password length, defaults to 8
    def __init__(self, password_min_length=8):
        self.password_min_length = password_min_length

    def validate_password(self, password, User=None):
        if len(password) < self.password_min_length:
            raise ValidationError(
                ("This password must contain at least %(min_length)d characters."),
                code="password_too_short",
                params={"min_length": self.password_min_length},
            )

        special_characters = "!@#$%^&*()-_+={}[]|\:"

        if not any(char in special_characters for char in password):
            raise ValidationError(
                ("This password must contain at least one special character."),
                code="password_no_special_character",
            )

    def validate_email(self, email, user=None):
        if not re.match(r'^[\w\.-]+@[\w\.-]+$', email):
            raise ValidationError(
                ("Invalid email format."),
                code="invalid_email_format",
            )