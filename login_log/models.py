from datetime import datetime

from django.db import models


class LoginIP(models.Model):
    ip = models.GenericIPAddressField()
    system = models.CharField(max_length=150)
    device = models.CharField(max_length=150)
    is_bot = models.BooleanField(default=False)
    browser = models.CharField(max_length=150)
    failed_count = models.IntegerField(default=0)
    is_blacklist = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'login_ip'


class LoginRecord(models.Model):
    login_ip = models.ForeignKey('LoginIP', on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    is_login = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'login_record'
