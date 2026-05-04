from django.urls import path
from login_log import views
from login_log.views import *

app_name = 'login_log'

urlpatterns = [
    path('get_all_login_ip/', GetAllLoginIP.as_view(), name='get_all_login_ip'),
    path('get_all_login_ip/<int:page>', GetAllLoginIP.as_view(), name='get_all_login_ip'),

    path('get_all_login_record/', GetAllLoginRecord.as_view(), name='get_all_login_record'),
    path('get_all_login_record/<int:page>', GetAllLoginRecord.as_view(), name='get_all_login_record'),

    path('toggle_ip_status/<int:id>', ToggleLoginIPStatus.as_view(), name='toggle_ip_status'),

    path('delete_login_ip/<int:id>', DeleteLoginIP.as_view(), name='delete_login_ip'),
    path('delete_login_record/<int:id>', DeleteLoginRecord.as_view(), name='delete_login_record'),
]
