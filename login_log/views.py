from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from utils.get_data import get_data_by_page
from .models import LoginRecord
from utils.verify import *


# Create your views here.
class GetAllLoginIP(LoginRequiredMixin, View):
    def get(self, request, page=1):
        permission = request.user.permission
        order_by = request.GET.get('order_by')

        if order_by == '1':
            all_login_ip = LoginIP.objects.all()
        else:
            all_login_ip = LoginIP.objects.all().order_by('-id')

        all_login_ip = get_data_by_page(all_login_ip, page)[0]
        is_paginated = get_data_by_page(all_login_ip, page)[1]
        return render(request, 'login_log/all_login_ip.html',
                      {'all_login_ip': all_login_ip, 'is_paginated': is_paginated, 'permission': permission,
                       'order_by': order_by})


class GetAllLoginRecord(LoginRequiredMixin, View):
    def get(self, request, page=1):
        permission = request.user.permission
        order_by = request.GET.get('order_by')

        if order_by == '1':
            all_login_record = LoginRecord.objects.all()
        else:
            all_login_record = LoginRecord.objects.all().order_by('-id')

        all_login_record = get_data_by_page(all_login_record, page)[0]
        is_paginated = get_data_by_page(all_login_record, page)[1]
        return render(request, 'login_log/all_login_record.html',
                      {'all_login_record': all_login_record, 'is_paginated': is_paginated, 'permission': permission,
                       'order_by': order_by})


class ToggleLoginIPStatus(LoginRequiredMixin, View):
    def get(self, request, id):
        permission = request.employee.permission
        if verify_permission(permission, 1):
            return verify_permission(permission, 1)

        login_ip = LoginIP.objects.filter(id=id).first()
        if login_ip:
            if login_ip.is_blacklist:
                login_ip.is_blacklist = False
                login_ip.save()
            else:
                login_ip.is_blacklist = True
                login_ip.save()
            return hint_message(request, 'Blacklist/Unbalicklist login IP successful.', 'account:get_all_login_ip')
        else:
            return hint_message(request, 'Login IP not exist.', 'account:get_all_login_ip')


class DeleteLoginIP(LoginRequiredMixin, View):
    def get(self, request, id):
        permission = request.employee.permission
        if verify_permission(permission, 1):
            return verify_permission(permission, 1)

        login_ip = LoginIP.objects.filter(id=id).first()

        if not login_ip:
            return hint_message(request, 'No login IP exist.', 'account:get_all_login_ip')

        login_ip.delete()
        return redirect('login_log:get_all_login_ip')


class DeleteLoginRecord(LoginRequiredMixin, View):
    def get(self, request, id):
        permission = request.employee.permission
        if verify_permission(permission, 1):
            return verify_permission(permission, 1)

        login_record = LoginRecord.objects.get(id=id)
        if login_record:
            login_record.delete()
            return hint_message(request, 'Delete login record successful.', 'account:get_all_login_record')
        else:
            return hint_message(request, 'No login record exist.', 'account:get_all_login_record')
