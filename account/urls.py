
from django.contrib import admin
from django.urls import path

from account.views import Login, Logout

app_name = 'account'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
