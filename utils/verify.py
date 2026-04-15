import re

from employee.models import Employee


def verify_username(username):
    pattern = r'^[A-Za-z0-9_]+$'

    if not username:
        return 'Username cannot be empty.'
    if len(username) > 150:
        return 'Username cannot be longer than 150 characters.'
    if not re.match(pattern, username):
        return 'Username must contain only letters, numbers, and underscores.'
    return True


def verify_password(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9\s])[^\s]+$'

    if not password:
        return 'Password cannot be empty.'
    if len(password) < 8:
        return 'Password must be at least 8 characters long.'
    if len(password) > 128:
        return 'Password cannot be longer than 128 characters.'
    if not re.match(pattern, password):
        return 'Password must include uppercase, lowercase, number, and special character.'
    return True


def verify_password_match(password, confirm_password):
    if password != confirm_password:
        return 'Passwords do not match.'
    return True


def verify_name(name):
    if not name:
        return 'Name cannot be empty.'
    if len(name) > 150:
        return 'Name cannot be longer than 150 characters.'
    return True


def verify_phone(phone):
    pattern = r'^[1-9][0-9]{7,14}$'

    if not phone:
        return 'Phone cannot be empty.'
    if len(phone) > 12:
        return 'Phone numbers cannot be longer than 12 characters.'
    if not re.match(pattern, phone):
        return 'Phone number format is invalid.'
    return True


def verify_username_exist(username, exclude_pk=None):
    queryset = Employee.objects.filter(username=username)
    if exclude_pk is not None:
        queryset = queryset.exclude(pk=exclude_pk)
    if queryset.exists():
        return 'Username already exists.'
    return True


def verify_email_exist(email, exclude_pk=None):
    queryset = Employee.objects.filter(email=email)
    if exclude_pk is not None:
        queryset = queryset.exclude(pk=exclude_pk)
    if queryset.exists():
        return 'Email already exists.'
    return True


def verify_phone_exist(phone, exclude_pk=None):
    queryset = Employee.objects.filter(phone=phone)
    if exclude_pk is not None:
        queryset = queryset.exclude(pk=exclude_pk)
    if queryset.exists():
        return 'Phone already exists.'
    return True


def verify_image(image):
    if not image:
        return True
    if not image.content_type.startswith('image/'):
        return 'Image type not supported.'
    if image.size > 100 * 1024 * 1024:
        return 'Image size too large.'
    return True


def verify_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    if not email:
        return 'Email cannot be empty.'
    if not re.match(pattern, email):
        return 'Email format is invalid.'
    return True
