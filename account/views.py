from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
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

        error_messages = {}

        error_message_username = verify_username(username)
        if error_message_username != True:
            error_messages['username'] = error_message_username

        error_message_password = verify_password(password)
        if error_message_password != True:
            error_messages['password'] = error_message_password
            print(error_messages['password'])

        if error_messages:
            return render(request, 'account/login.html', {'username': username, 'password': password, 'error_messages': error_messages})

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
