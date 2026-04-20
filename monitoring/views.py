from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class GetCropZoneData(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'monitoring/monitoring.html')

    def post(self, request):
        pass