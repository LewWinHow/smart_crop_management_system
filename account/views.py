from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View

from login_log.models import LoginIP, LoginRecord
from utils.get_data import get_device_info
from utils.hint_message import hint_message
from utils.verify import *


class Login(View):
    def get(self, request):
        return render(request, 'account/login.html')

    def post(self, request):
        ip = request.META.get('REMOTE_ADDR')
        device_info = get_device_info(request)
        system = device_info['system']
        device = device_info['device']
        is_bot = device_info['is_bot']
        browser = device_info['browser']

        login_ip = LoginIP.objects.filter(ip=ip).first()
        if login_ip:
            if is_bot:
                login_ip.is_blacklist = True
                login_ip.save()
        else:
            if is_bot:
                login_ip = LoginIP(
                    ip=ip,
                    system=system,
                    device=device,
                    is_bot=is_bot,
                    browser=browser,
                    is_blacklist=True
                )
            else:
                login_ip = LoginIP(
                    ip=ip,
                    system=system,
                    device=device,
                    is_bot=is_bot,
                    browser=browser
                )
            login_ip.save()
        username = request.POST.get('username') or None
        password = request.POST.get('password') or None

        if verify_username(username, request, 'account:login') != True:
            return verify_username(username, request, 'account:login')

        if verify_password(password, request, 'account:login') != True:
            return verify_password(password, request, 'account:login')

        employee = authenticate(request, username=username, password=password)

        if employee:
            login(request, employee)

            login_ip.failed_count = 0
            login_ip.save()
            login_record = LoginRecord(
                login_ip=login_ip,
                username=username,
                password=password,
                is_login=True,
            )
            login_record.save()
            return hint_message(
                request, 'Login successful!', 'monitoring:get_crop_zone_data'
            )
        else:
            login_ip.failed_count += 1
            login_ip.save()
            if login_ip.failed_count > 5:
                login_ip.is_blacklist = 1
                login_ip.save()

            login_record = LoginRecord(
                login_ip=login_ip,
                username=username,
                password=password,
                is_login=False,
            )
            login_record.save()
            return hint_message(
                request, 'Login failed!', 'account:login'
            )


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('account:login')
