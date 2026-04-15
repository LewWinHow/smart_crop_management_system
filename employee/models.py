from django.db import models
from django.contrib.auth.models import AbstractUser


class Employee(AbstractUser):
    """
    -----AbstractUser-provided fields-----

    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False) //Mean administration account
    is_active = models.BooleanField(default=True) //Mean account status
    is_superuser = models.BooleanField(default=False) //Mean supervisor account
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    """
    permission = models.IntegerField(
        default=3,
        db_comment='1 = Supervisor, 2 = Administrator, 3 = Viewer',
    )
    profile_image = models.ImageField(upload_to='profile_image', null=True, blank=True)
    phone = models.CharField(max_length=12, unique=True, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.IntegerField(
        null=True,
        blank=True,
        default=1,
        db_comment='1 = Male, 2 = Female',
    )
    birth_date = models.DateField(null=True, blank=True)
    updated_date = models.DateField(auto_now=True)

    class Meta:
        db_table = 'employee'
