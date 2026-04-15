from django import forms

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


class EmployeeEditForm(forms.ModelForm):
    permission = forms.ChoiceField(
        label='Permission',
        choices=Employee.PERMISSION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    gender = forms.ChoiceField(
        label='Gender',
        choices=[('', '-'), ('1', 'Male'), ('2', 'Female')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = Employee
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'age',
            'birth_date',
            'permission',
            'profile_image',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        permission = self.instance.permission if self.instance.pk else self.initial.get('permission', 3)
        self.initial['permission'] = str(permission)
        if self.instance.pk:
            gender = self.instance.gender
            self.initial['gender'] = '' if gender is None else str(gender)

    def clean_first_name(self):
        first_name = (self.cleaned_data.get('first_name') or '').strip()
        result = verify_name(first_name)
        if result is not True:
            raise forms.ValidationError(result)
        return first_name

    def clean_last_name(self):
        last_name = (self.cleaned_data.get('last_name') or '').strip()
        result = verify_name(last_name)
        if result is not True:
            raise forms.ValidationError(result)
        return last_name

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip()
        result = verify_email(email)
        if result is not True:
            raise forms.ValidationError(result)
        result = verify_email_exist(email, exclude_pk=self.instance.pk if self.instance.pk else None)
        if result is not True:
            raise forms.ValidationError(result)
        return email

    def clean_phone(self):
        phone = (self.cleaned_data.get('phone') or '').strip()
        result = verify_phone(phone)
        if result is not True:
            raise forms.ValidationError(result)
        result = verify_phone_exist(phone, exclude_pk=self.instance.pk if self.instance.pk else None)
        if result is not True:
            raise forms.ValidationError(result)
        return phone

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        result = verify_image(image)
        if result is not True:
            raise forms.ValidationError(result)
        return image

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.permission = int(self.cleaned_data['permission'])
        raw_gender = self.cleaned_data.get('gender')
        if raw_gender in (None, ''):
            instance.gender = None
        else:
            instance.gender = int(raw_gender)
        if commit:
            instance.save()
        return instance


class EmployeeCreateForm(EmployeeEditForm):
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta(EmployeeEditForm.Meta):
        model = Employee
        fields = ['username', 'password1', 'password2'] + EmployeeEditForm.Meta.fields

    def clean_username(self):
        username = (self.cleaned_data.get('username') or '').strip()
        result = verify_username(username)
        if result is not True:
            raise forms.ValidationError(result)
        result = verify_username_exist(username)
        if result is not True:
            raise forms.ValidationError(result)
        return username

    def clean(self):
        cleaned = super().clean()
        password1 = cleaned.get('password1')
        password2 = cleaned.get('password2')
        password_result = verify_password(password1)
        if password_result is not True:
            self.add_error('password1', password_result)
        match_result = verify_password_match(password1, password2)
        if match_result is not True:
            self.add_error('password2', match_result)
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.username = self.cleaned_data['username']
        instance.set_password(self.cleaned_data['password1'])
        if commit:
            instance.save()
        return instance


class MyInformationForm(EmployeeEditForm):
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta(EmployeeEditForm.Meta):
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'age',
            'birth_date',
            'permission',
            'profile_image',
        ]

    def clean_username(self):
        username = (self.cleaned_data.get('username') or '').strip()
        result = verify_username(username)
        if result is not True:
            raise forms.ValidationError(result)
        result = verify_username_exist(username, exclude_pk=self.instance.pk)
        if result is not True:
            raise forms.ValidationError(result)
        return username

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.username = self.cleaned_data['username']
        if commit:
            instance.save()
        return instance
