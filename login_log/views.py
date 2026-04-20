from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from utils.get_data import get_data_by_page
from .models import LoginIP, LoginRecord


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return bool(self.request.user.is_authenticated and self.request.user.is_superuser)

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied.')
        return redirect('monitoring:get_crop_zone_data')


class IPOfLogin(LoginRequiredMixin, SuperuserRequiredMixin, View):
    template_name = 'login_log/login_ip.html'

    def get_queryset(self, request):
        queryset = LoginIP.objects.all()
        filter_select = request.POST.get('filter_select') or '1'
        filter_input = (request.POST.get('filter_input') or '').strip()
        blacklist_select = request.POST.get('blacklist_select') or ''
        order_by = request.POST.get('order_by') or '0'

        if filter_select == '2' and filter_input:
            queryset = queryset.filter(id=filter_input)
        elif filter_select == '3' and blacklist_select != '':
            queryset = queryset.filter(is_blacklist=(blacklist_select == '1'))

        queryset = queryset.order_by('id' if order_by == '1' else '-id')
        return queryset, filter_select, filter_input, blacklist_select, order_by

    def render_page(self, request, page):
        queryset, filter_select, filter_input, blacklist_select, order_by = self.get_queryset(request)
        login_ip_list, is_paginated = get_data_by_page(queryset, page)
        return render(
            request,
            self.template_name,
            {
                'login_ip_list': login_ip_list,
                'is_paginated': is_paginated,
                'filter_select': filter_select,
                'filter_input': filter_input,
                'blacklist_select': blacklist_select,
                'order_by': order_by,
            },
        )

    def get(self, request, page=1):
        return self.render_page(request, page)

    def post(self, request, page=1):
        return self.render_page(request, page)


class RecordOfLogin(LoginRequiredMixin, SuperuserRequiredMixin, View):
    template_name = 'login_log/login_record.html'

    def get_queryset(self, request):
        queryset = LoginRecord.objects.select_related('login_ip').all()
        filter_select = request.POST.get('filter_select') or '1'
        filter_input = (request.POST.get('filter_input') or '').strip()
        filter_input_second = (request.POST.get('filter_input_second') or '').strip()
        status_select = request.POST.get('status_select') or ''
        order_by = request.POST.get('order_by') or '0'

        if filter_select == '2' and filter_input:
            queryset = queryset.filter(id=filter_input)
        elif filter_select == '3' and filter_input:
            queryset = queryset.filter(login_ip_id=filter_input)
        elif filter_select == '4' and status_select != '':
            queryset = queryset.filter(is_login=(status_select == '1'))
        elif filter_select == '5':
            if filter_input:
                queryset = queryset.filter(created_time__date__gte=filter_input)
            if filter_input_second:
                queryset = queryset.filter(created_time__date__lte=filter_input_second)

        queryset = queryset.order_by('id' if order_by == '1' else '-id')
        return queryset, filter_select, filter_input, filter_input_second, status_select, order_by

    def render_page(self, request, page):
        queryset, filter_select, filter_input, filter_input_second, status_select, order_by = self.get_queryset(request)
        login_record_list, is_paginated = get_data_by_page(queryset, page)
        return render(
            request,
            self.template_name,
            {
                'login_record_list': login_record_list,
                'is_paginated': is_paginated,
                'filter_select': filter_select,
                'filter_input': filter_input,
                'filter_input_second': filter_input_second,
                'status_select': status_select,
                'order_by': order_by,
            },
        )

    def get(self, request, page=1):
        return self.render_page(request, page)

    def post(self, request, page=1):
        return self.render_page(request, page)


class IPBlacklist(LoginRequiredMixin, SuperuserRequiredMixin, View):
    def post(self, request, id):
        login_ip = get_object_or_404(LoginIP, id=id)
        login_ip.is_blacklist = not login_ip.is_blacklist
        login_ip.save(update_fields=['is_blacklist'])
        messages.success(request, f'Blacklist status updated for {login_ip.ip}.')
        return redirect('login_log:login_ip')


class DeleteLoginIP(LoginRequiredMixin, SuperuserRequiredMixin, View):
    def post(self, request, id):
        login_ip = get_object_or_404(LoginIP, id=id)
        login_ip.delete()
        messages.success(request, 'Login IP record deleted.')
        return redirect('login_log:login_ip')


class DeleteLoginRecord(LoginRequiredMixin, SuperuserRequiredMixin, View):
    def post(self, request, id):
        login_record = get_object_or_404(LoginRecord, id=id)
        login_record.delete()
        messages.success(request, 'Login record deleted.')
        return redirect('login_log:login_record')
