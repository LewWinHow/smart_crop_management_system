import re

from django.shortcuts import redirect as redirect_to

from employee.models import Employee
from login_log.models import LoginIP
from utils.hint_message import hint_message


def verify_ip(request):
    current_ip = request.META.get('REMOTE_ADDR')
    login_info = LoginIP.objects.filter(ip=current_ip).first()
    if login_info:
        if login_info.is_blacklist:
            return hint_message(request, 'Your IP has been blocked!', 'account:login')

    return True


def verify_username(username, request, redirect):
    pattern = r"^[A-Za-z0-9_]+$"

    if not username:
        return hint_message(request, "Username cannot be empty.", redirect)
    if len(username) > 150:
        return hint_message(request, "Username cannot be longer than 150 characters.", redirect)
    if not re.match(pattern, username):
        return hint_message(request, "Username must contain only letters, numbers, and underscores.", redirect)
    return True


def verify_password(password, request, redirect):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9\s])[^\s]+$"

    if not password:
        return hint_message(request, "Password cannot be empty.", redirect)
    if len(password) < 8:
        return hint_message(request, "Password must be at least 8 characters long.", redirect)
    if len(password) > 128:
        return hint_message(request, "Password cannot be longer than 128 characters.", redirect)
    if not re.match(pattern, password):
        return hint_message(request, "Password must include uppercase, lowercase, number, and special character.",
                            redirect)
    return True


def verify_password_match(password, confirm_password, request, redirect):
    if password != confirm_password:
        return hint_message(request, "Passwords do not match.", redirect)
    return True


def verify_first_name(first_name, request, redirect):
    if not first_name:
        return hint_message(request, "First name cannot be empty.", redirect)
    if len(first_name) > 150:
        return hint_message(request, "First name cannot be longer than 150 characters.", redirect)
    return True


def verify_last_name(last_name, request, redirect):
    if not last_name:
        return hint_message(request, "Last name cannot be empty.", redirect)
    if len(last_name) > 150:
        return hint_message(request, "Last name cannot be longer than 150 characters.", redirect)
    return True


def verify_phone(phone, request, redirect):
    pattern = r"^[1-9][0-9]{7,14}$"

    if not phone:
        return hint_message(request, "Phone cannot be empty.", redirect)
    if len(phone) > 12:
        return hint_message(request, "Phone numbers cannot be longer than 12 characters.", redirect)
    if not re.match(pattern, phone):
        return hint_message(request, "Phone number format is invalid.", redirect)
    return True


def verify_username_exist(username, request, redirect, id=None):
    employee = Employee.objects.filter(username=username).exclude(id=id)
    if employee:
        return hint_message(request, "Username already exists.", redirect)
    return True


def verify_email_exist(email, request, redirect, id=None):
    employee = Employee.objects.filter(email=email).exclude(id=id)
    if employee:
        return hint_message(request, "Email already exists.", redirect)
    return True


def verify_phone_exist(phone, request, redirect, id=None):
    employee = Employee.objects.filter(phone=phone).exclude(id=id)
    if employee:
        return hint_message(request, "Phone already exists.", redirect)
    return True


def verify_image(image, request, redirect):
    if not image:
        return True
    if not image.content_type.startswith("image/"):
        return hint_message(request, "Image type not supported.", redirect)
    if image.size > 100 * 1024 * 1024:
        return hint_message(request, "Image size too large.", redirect)
    return True


def verify_email(email, request, redirect):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not email:
        return hint_message(request, "Email cannot be empty.", redirect)
    if not re.match(pattern, email):
        return hint_message(request, "Email format is invalid.", redirect)
    return True


def verify_permission(permission, permission_request=1):
    if permission > permission_request:
        return redirect_to("account:logout")
    return True
