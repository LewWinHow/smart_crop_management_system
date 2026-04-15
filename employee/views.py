from datetime import date

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from employee.models import Employee
from utils.verify import (
    verify_email,
    verify_email_exist,
    verify_image,
    verify_name,
    verify_password,
    verify_password_match,
    verify_phone,
    verify_phone_exist,
    verify_username,
    verify_username_exist,
)


class SupervisorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        u = self.request.user
        return bool(u.is_authenticated and getattr(u, 'permission', None) == 1)

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied.')
        return redirect('employee:get_all_employee')


class EmployeeFormMixin:
    permission_options = [(1, 'Supervisor'), (2, 'Administrator'), (3, 'Viewer')]
    gender_options = [('', '-'), ('1', 'Male'), ('2', 'Female')]

    def get_employee_values(self, employee=None, data=None, include_username=False, include_password=False):
        if data is not None:
            values = {
                'first_name': data.get('first_name', '').strip(),
                'last_name': data.get('last_name', '').strip(),
                'email': data.get('email', '').strip(),
                'phone': data.get('phone', '').strip(),
                'age': data.get('age', '').strip(),
                'gender': data.get('gender', ''),
                'birth_date': data.get('birth_date', ''),
                'permission': data.get('permission', str(employee.permission if employee else 3)).strip(),
            }
            if include_username:
                values['username'] = data.get('username', '').strip()
            if include_password:
                values['password1'] = data.get('password1', '')
                values['password2'] = data.get('password2', '')
            return values

        values = {
            'first_name': (employee.first_name or '') if employee else '',
            'last_name': (employee.last_name or '') if employee else '',
            'email': (employee.email or '') if employee else '',
            'phone': (employee.phone or '') if employee else '',
            'age': '' if not employee or employee.age is None else str(employee.age),
            'gender': '' if not employee or employee.gender is None else str(employee.gender),
            'birth_date': '' if not employee or not employee.birth_date else employee.birth_date.strftime('%Y-%m-%d'),
            'permission': str(employee.permission if employee else 3),
        }
        if include_username:
            values['username'] = (employee.username or '') if employee else ''
        if include_password:
            values['password1'] = ''
            values['password2'] = ''
        return values

    def validate_employee_values(self, values, profile_image=None, employee=None, require_username=False, require_password=False):
        error_messages = {}
        age_value = None
        birth_date_value = None

        if require_username:
            username_message = verify_username(values['username'])
            if username_message is not True:
                error_messages['username'] = username_message
            else:
                username_exist_message = verify_username_exist(values['username'], exclude_pk=employee.pk if employee else None)
                if username_exist_message is not True:
                    error_messages['username'] = username_exist_message

        first_name_message = verify_name(values['first_name'])
        if first_name_message is not True:
            error_messages['first_name'] = first_name_message

        last_name_message = verify_name(values['last_name'])
        if last_name_message is not True:
            error_messages['last_name'] = last_name_message

        email_message = verify_email(values['email'])
        if email_message is not True:
            error_messages['email'] = email_message
        else:
            email_exist_message = verify_email_exist(values['email'], exclude_pk=employee.pk if employee else None)
            if email_exist_message is not True:
                error_messages['email'] = email_exist_message

        phone_message = verify_phone(values['phone'])
        if phone_message is not True:
            error_messages['phone'] = phone_message
        else:
            phone_exist_message = verify_phone_exist(values['phone'], exclude_pk=employee.pk if employee else None)
            if phone_exist_message is not True:
                error_messages['phone'] = phone_exist_message

        if require_password:
            password_message = verify_password(values['password1'])
            if password_message is not True:
                error_messages['password1'] = password_message
            password_match_message = verify_password_match(values['password1'], values['password2'])
            if password_match_message is not True:
                error_messages['password2'] = password_match_message

        if profile_image:
            image_message = verify_image(profile_image)
            if image_message is not True:
                error_messages['profile_image'] = image_message

        if values['age']:
            try:
                age_value = int(values['age'])
                if age_value < 0:
                    error_messages['age'] = 'Age cannot be negative.'
            except ValueError:
                error_messages['age'] = 'Age must be a number.'

        if values['permission'] not in {str(key) for key, _ in self.permission_options}:
            error_messages['permission'] = 'Permission is invalid.'

        if values['gender'] not in {'', '1', '2'}:
            error_messages['gender'] = 'Gender is invalid.'

        if values['birth_date']:
            try:
                birth_date_value = date.fromisoformat(values['birth_date'])
            except ValueError:
                error_messages['birth_date'] = 'Birth date is invalid.'

        return error_messages, age_value, birth_date_value

    def apply_employee_values(self, employee, values, age_value, birth_date_value, profile_image=None, clear_profile_image=False, include_username=False, include_password=False):
        if include_username:
            employee.username = values['username']
        employee.first_name = values['first_name']
        employee.last_name = values['last_name']
        employee.email = values['email']
        employee.phone = values['phone']
        employee.age = age_value
        employee.gender = None if values['gender'] == '' else int(values['gender'])
        employee.birth_date = birth_date_value
        employee.permission = int(values['permission'])
        if include_password:
            employee.set_password(values['password1'])
        if clear_profile_image:
            employee.profile_image = None
        elif profile_image:
            employee.profile_image = profile_image
        employee.save()


class GetAllEmployee(LoginRequiredMixin, View):
    def get(self, request):
        employees = Employee.objects.all().order_by('-id')
        permission = request.user.permission
        return render(request, 'employee/all_employee.html', {'employees': employees, 'permission': permission})


class EditEmployee(LoginRequiredMixin, SupervisorRequiredMixin, EmployeeFormMixin, View):
    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        return render(
            request,
            'employee/edit_employee.html',
            {
                'employee': employee,
                'values': self.get_employee_values(employee),
                'permission_choices': self.permission_options,
                'gender_choices': self.gender_options,
                'error_messages': {},
            },
        )

    def post(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        values = self.get_employee_values(employee, request.POST)
        profile_image = request.FILES.get('profile_image')
        clear_profile_image = request.POST.get('profile_image-clear') == 'on'
        error_messages, age_value, birth_date_value = self.validate_employee_values(values, profile_image=profile_image, employee=employee)

        if error_messages:
            return render(
                request,
                'employee/edit_employee.html',
                {
                    'employee': employee,
                    'values': values,
                    'permission_choices': self.permission_options,
                    'gender_choices': self.gender_options,
                    'error_messages': error_messages,
                },
            )

        self.apply_employee_values(
            employee,
            values,
            age_value,
            birth_date_value,
            profile_image=profile_image,
            clear_profile_image=clear_profile_image,
        )
        messages.success(request, 'Employee updated.')
        return redirect('employee:get_all_employee')


class ToggleEmployeeActive(LoginRequiredMixin, SupervisorRequiredMixin, View):
    def post(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        if employee.pk == request.user.pk:
            messages.error(request, 'You cannot change your own active status here.')
            return redirect('employee:get_all_employee')
        employee.is_active = not employee.is_active
        employee.save(update_fields=['is_active'])
        state = 'enabled' if employee.is_active else 'disabled'
        messages.success(request, f'Account {employee.username} {state}.')
        return redirect('employee:get_all_employee')


class DeleteEmployee(LoginRequiredMixin, SupervisorRequiredMixin, View):
    def post(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        if employee.pk == request.user.pk:
            messages.error(request, 'You cannot delete your own account.')
            return redirect('employee:get_all_employee')
        username = employee.username
        employee.delete()
        messages.success(request, f'Employee {username} deleted.')
        return redirect('employee:get_all_employee')


class AddEmployee(LoginRequiredMixin, SupervisorRequiredMixin, EmployeeFormMixin, View):
    def get(self, request):
        return render(
            request,
            'employee/add_employee.html',
            {
                'values': self.get_employee_values(include_username=True, include_password=True),
                'permission_choices': self.permission_options,
                'gender_choices': self.gender_options,
                'error_messages': {},
            },
        )

    def post(self, request):
        values = self.get_employee_values(data=request.POST, include_username=True, include_password=True)
        profile_image = request.FILES.get('profile_image')
        error_messages, age_value, birth_date_value = self.validate_employee_values(
            values,
            profile_image=profile_image,
            require_username=True,
            require_password=True,
        )

        if error_messages:
            return render(
                request,
                'employee/add_employee.html',
                {
                    'values': values,
                    'permission_choices': self.permission_options,
                    'gender_choices': self.gender_options,
                    'error_messages': error_messages,
                },
            )

        employee = Employee()
        self.apply_employee_values(
            employee,
            values,
            age_value,
            birth_date_value,
            profile_image=profile_image,
            include_username=True,
            include_password=True,
        )
        messages.success(request, f'Employee {employee.username} created.')
        return redirect('employee:get_all_employee')


class GetMyInformation(LoginRequiredMixin, EmployeeFormMixin, View):
    def get(self, request):
        employee = request.user
        return render(
            request,
            'employee/my_information.html',
            {
                'employee': employee,
                'values': self.get_employee_values(employee, include_username=True),
                'permission_choices': self.permission_options,
                'gender_choices': self.gender_options,
                'error_messages': {},
            },
        )

    def post(self, request):
        employee = request.user
        values = self.get_employee_values(employee, request.POST, include_username=True)
        profile_image = request.FILES.get('profile_image')
        clear_profile_image = request.POST.get('profile_image-clear') == 'on'
        error_messages, age_value, birth_date_value = self.validate_employee_values(
            values,
            profile_image=profile_image,
            employee=employee,
            require_username=True,
        )

        if error_messages:
            return render(
                request,
                'employee/my_information.html',
                {
                    'employee': employee,
                    'values': values,
                    'permission_choices': self.permission_options,
                    'gender_choices': self.gender_options,
                    'error_messages': error_messages,
                },
            )

        self.apply_employee_values(
            employee,
            values,
            age_value,
            birth_date_value,
            profile_image=profile_image,
            clear_profile_image=clear_profile_image,
            include_username=True,
        )
        messages.success(request, 'Your information has been updated.')
        return redirect('employee:get_my_information')
