from django.urls import path

from login_log.views import DeleteLoginIP, DeleteLoginRecord, IPBlacklist, IPOfLogin, RecordOfLogin

app_name = 'login_log'

urlpatterns = [
    path('login_ip/', IPOfLogin.as_view(), name='login_ip'),
    path('login_ip/<int:page>/', IPOfLogin.as_view(), name='login_ip_page'),
    path('login_record/', RecordOfLogin.as_view(), name='login_record'),
    path('login_record/<int:page>/', RecordOfLogin.as_view(), name='login_record_page'),
    path('blacklist_ip/<int:id>/', IPBlacklist.as_view(), name='blacklist_ip'),
    path('delete_login_ip/<int:id>/', DeleteLoginIP.as_view(), name='delete_login_ip'),
    path('delete_login_record/<int:id>/', DeleteLoginRecord.as_view(), name='delete_login_record'),
]
