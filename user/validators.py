# validators.py

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 4:
            raise ValidationError(
                _("This password is too short. It must contain at least 4 characters."),
                code='password_too_short',
            )
        # Add more custom validation rules if needed

    def get_help_text(self):
        return _("Your password must contain at least 4 characters.")
