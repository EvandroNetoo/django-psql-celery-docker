from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


no_whitespaces = RegexValidator(regex=r'\s', message=_('Do not use whitespaces.'), inverse_match=True)

special_characters = RegexValidator(regex=r'[*&%$#@_\-!]', message=_('Use at least one special character.'))

uppercase_letters = RegexValidator(regex=r'[A-Z]', message=_('Use at least one uppercase letter.'))

lowercase_letters = RegexValidator(regex=r'[a-z]', message=_('Use at least one lowercase letter.'))

number_validator = RegexValidator(regex=r'\d+', message=_('Use at least one number.'))


def min_length_6_validator(value: str) -> bool:
    if len(value) < 6:
        raise ValidationError(_('The minimum length is 6 characters.'))
