from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from employee.models import Employee
from utils.get_data import get_data_by_page
from utils.save_profile_image import save_profile_image
from utils.verify import verify_permission, verify_username, verify_password, verify_password_match, verify_first_name, \
    verify_last_name, verify_email, verify_phone, verify_image, verify_username_exist, verify_email_exist, \
    verify_phone_exist
from utils.hint_message import hint_message


class GetAllEmployee(LoginRequiredMixin, View):
    def get(self, request, page=1):
        permission = request.user.permission
        if verify_permission(permission, 2) != True:
            return verify_permission(permission, 2)

        order_by = request.GET.get('order_by') or None
        if order_by == '1':
            employees = Employee.objects.all()
        else:
            employees = Employee.objects.all().order_by('-id')

        employees = get_data_by_page(employees, page)[0]
        is_paginated = get_data_by_page(employees, page)[1]
        return render(request, 'employee/all_employee.html',
                      {'employees': employees, 'is_paginated': is_paginated, 'permission': permission,
                       'order_by': order_by})


class AddEmployee(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'employee/add_employee.html')

    def post(self, request):
        redirect = 'employee:add_employee'

        permission = request.user.permission
        if verify_permission(permission, 1) != True:
            return verify_permission(permission, 1)

        username = request.POST.get('username') or None
        if verify_username(username, request, redirect) != True:
            return verify_username(username, request, redirect)

        if verify_username_exist(username, request, redirect, id=None) != True:
            return verify_username_exist(username, request, redirect, id=None)

        password = request.POST.get('password') or None
        if verify_password(password, request, redirect) != True:
            return verify_password(password, request, redirect)

        confirm_password = request.POST.get('confirm_password') or None
        if verify_password(confirm_password, request, redirect) != True:
            return verify_password(confirm_password, request, redirect)

        if verify_password_match(password, confirm_password, request, redirect) != True:
            return verify_password_match(password, confirm_password, request, redirect)

        first_name = request.POST.get('first_name') or None
        if verify_first_name(first_name, request, redirect) != True:
            return verify_first_name(first_name, request, redirect)

        last_name = request.POST.get('last_name') or None
        if verify_last_name(last_name, request, redirect) != True:
            return verify_last_name(last_name, request, redirect)

        email = request.POST.get('email') or None
        if verify_email(email, request, redirect) != True:
            return verify_email(email, request, redirect)

        if verify_email_exist(email, request, redirect) != True:
            return verify_email_exist(email, request, redirect)

        phone = request.POST.get('phone') or None
        if verify_phone(phone, request, redirect) != True:
            return verify_phone(phone, request, redirect)

        if verify_phone_exist(phone, request, redirect) != True:
            return verify_phone_exist(phone, request, redirect)

        birth_date = request.POST.get('birth_date') or None

        age = request.POST.get('age') or None

        gender = request.POST.get('gender') or None

        permission = request.POST.get('permission') or None

        is_active = request.POST.get('is_active') or None

        profile_image = request.POST.get('profile_image') or None
        if verify_image(profile_image, request, redirect) != True:
            return verify_image(profile_image, request, redirect)

        profile_image_path = save_profile_image(profile_image, 'profile_image')

        employee = Employee(username=username, first_name=first_name, last_name=last_name, email=email,
                            phone=phone, birth_date=birth_date, age=age, gender=gender,
                            permission=permission, is_active=is_active, profile_image=profile_image_path)
        employee.set_password(password)
        employee.save()
        return hint_message(request, 'Add employee successful.', 'employee:get_all_employee')


class EditEmployee(LoginRequiredMixin, View):
    def get(self, request, id):
        permission = request.user.permission
        if verify_permission(permission, 1) != True:
            return verify_permission(permission, 1)
        employee = Employee.objects.get(id=id)
        if employee:
            return render(request, 'employee/edit_employee.html', {'employee': employee})
        else:
            return hint_message(request, 'No employee exist.', 'employee:get_all_employee')

    def post(self, request, id):
        redirect = 'employee:edit_employee'

        permission = request.user.permission
        if verify_permission(permission, 1) != True:
            return verify_permission(permission, 1)

        username = request.POST.get('username') or None
        if verify_username(username, request, redirect) != True:
            return verify_username(username, request, redirect)

        if verify_username_exist(username, request, redirect, id=id) != True:
            return verify_username_exist(username, request, redirect, id=id)

        password = request.POST.get('password') or None
        confirm_password = request.POST.get('confirm_password') or None

        if password or confirm_password:

            if verify_password(password, request, redirect) != True:
                return verify_password(password, request, redirect)

            if verify_password(confirm_password, request, redirect) != True:
                return verify_password(confirm_password, request, redirect)

            if verify_password_match(password, confirm_password, request, redirect) != True:
                return verify_password_match(password, confirm_password, request, redirect)

        first_name = request.POST.get('first_name') or None
        if verify_first_name(first_name, request, redirect) != True:
            return verify_first_name(first_name, request, redirect)

        last_name = request.POST.get('last_name') or None
        if verify_last_name(last_name, request, redirect) != True:
            return verify_last_name(last_name, request, redirect)

        email = request.POST.get('email') or None
        if verify_email(email, request, redirect) != True:
            return verify_email(email, request, redirect)

        if verify_email_exist(email, request, redirect, id=id) != True:
            return verify_email_exist(email, request, redirect, id=id)

        phone = request.POST.get('phone') or None
        if verify_phone(phone, request, redirect) != True:
            return verify_phone(phone, request, redirect)

        if verify_phone_exist(phone, request, redirect, id=id) != True:
            return verify_phone_exist(phone, request, redirect, id=id)

        birth_date = request.POST.get('birth_date') or None

        age = request.POST.get('age') or None

        gender = request.POST.get('gender') or None

        permission = request.POST.get('permission') or None

        is_active = request.POST.get('is_active') or None

        profile_image = request.POST.get('profile_image') or None
        profile_image_path = None
        profile_image_clear = request.POST.get('profile_image-clear') or None
        if profile_image and not profile_image_clear:

            if verify_image(profile_image, request, redirect) != True:
                return verify_image(profile_image, request, redirect)

            profile_image_path = save_profile_image(profile_image, 'profile_image')

        employee = Employee.objects.get(id=id)
        if employee:
            employee.username = username
            if password or confirm_password:
                employee.set_password(password)
            employee.first_name = first_name
            employee.last_name = last_name
            employee.email = email
            employee.phone = phone
            employee.birth_date = birth_date
            employee.age = age
            employee.gender = gender
            employee.permission = permission
            employee.is_active = is_active
            if profile_image_clear:
                employee.profile_image = None
            elif profile_image:
                employee.profile_image = profile_image_path
        employee.save()
        return hint_message(request, 'Edit employee successful.', 'employee:get_all_employee')


class ToggleEmployeeActive(LoginRequiredMixin, View):
    def get(self, request, id):
        employee = Employee.objects.get(id=id)
        if employee:
            employee.is_active = 0
            employee.save()
            return hint_message(request, 'Toggle employee active successful.', 'employee:get_all_employee')
        else:
            return hint_message(request, 'Toggle employee active failed.', 'employee:get_all_employee')


class DeleteEmployee(LoginRequiredMixin, View):
    def get(self, request, id):
        employee = Employee.objects.get(id=id)
        if employee:
            employee.delete()
            return hint_message(request, 'Delete employee successful.', 'employee:get_all_employee')
        else:
            return hint_message(request, 'No employee exist.', 'employee:get_all_employee')


class GetYourInformation(LoginRequiredMixin, View):
    def get(self, request):
        employee = request.user
        permission = employee.permission
        return render(request, 'employee/your_information.html', {'employee': employee, 'permission': permission})

    def post(self, request):
        id = request.user.id
        permission = request.user.permission
        redirect = 'employee:get_your_information'

        username = request.POST.get('username') or None
        if verify_username(username, request, redirect) != True:
            return verify_username(username, request, redirect)

        if verify_username_exist(username, request, redirect, id=id) != True:
            return verify_username_exist(username, request, redirect, id=id)

        password = request.POST.get('password') or None
        confirm_password = request.POST.get('confirm_password') or None

        if password or confirm_password:

            if verify_password(password, request, redirect) != True:
                return verify_password(password, request, redirect)

            if verify_password(confirm_password, request, redirect) != True:
                return verify_password(confirm_password, request, redirect)

            if verify_password_match(password, confirm_password, request, redirect) != True:
                return verify_password_match(password, confirm_password, request, redirect)

        first_name = request.POST.get('first_name') or None
        if verify_first_name(first_name, request, redirect) != True:
            return verify_first_name(first_name, request, redirect)

        last_name = request.POST.get('last_name') or None
        if verify_last_name(last_name, request, redirect) != True:
            return verify_last_name(last_name, request, redirect)

        email = request.POST.get('email') or None
        if verify_email(email, request, redirect) != True:
            return verify_email(email, request, redirect)

        if verify_email_exist(email, request, redirect, id=id) != True:
            return verify_email_exist(email, request, redirect, id=id)

        phone = request.POST.get('phone') or None
        if verify_phone(phone, request, redirect) != True:
            return verify_phone(phone, request, redirect)

        if verify_phone_exist(phone, request, redirect, id=id) != True:
            return verify_phone_exist(phone, request, redirect, id=id)

        birth_date = request.POST.get('birth_date') or None

        age = request.POST.get('age') or None

        gender = request.POST.get('gender') or None

        permission = request.POST.get('permission') or None

        is_active = request.POST.get('is_active') or None

        profile_image = request.POST.get('profile_image') or None
        profile_image_path = None
        profile_image_clear = request.POST.get('profile_image-clear') or None
        if profile_image and not profile_image_clear:

            if verify_image(profile_image, request, redirect) != True:
                return verify_image(profile_image, request, redirect)

            profile_image_path = save_profile_image(profile_image, 'profile_image')

        employee = Employee.objects.get(id=id)
        if employee:
            employee.username = username
            if password or confirm_password:
                employee.set_password(password)
            employee.first_name = first_name
            employee.last_name = last_name
            employee.email = email
            employee.phone = phone
            employee.birth_date = birth_date
            employee.age = age
            employee.gender = gender
            if permission == 1:
                employee.permission = permission
                employee.is_active = is_active
            if profile_image_clear:
                employee.profile_image = None
            elif profile_image:
                employee.profile_image = profile_image_path
        employee.save()
        return hint_message(request, 'Edit employee successful.', 'employee:get_all_employee')
