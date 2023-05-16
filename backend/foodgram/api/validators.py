import datetime as dt
import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError(
            ('Имя пользователя не может быть <me>.'),
            params={'value': value},
        )
    if re.search(r'^[-a-zA-Z0-9_]+$', value) is None:
        raise ValidationError(
            ('Не допустимые символы '), params={'value': value},)


def validate_year(value):
    year = dt.date.today().year
    if not (value <= year):
        raise ValidationError('Дата указана некорректно!')
    return value
