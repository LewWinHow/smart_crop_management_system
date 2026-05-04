from django.urls import path

from employee.views import (
    AddEmployee,
    DeleteEmployee,
    EditEmployee,
    GetAllEmployee,
    GetYourInformation,
    ToggleEmployeeActive,
)

app_name = 'employee'

urlpatterns = [
    path('get_all_employee/', GetAllEmployee.as_view(), name='get_all_employee'),
    path('get_all_employee/<int:page>', GetAllEmployee.as_view(), name='get_all_employee'),
    path('add_employee/', AddEmployee.as_view(), name='add_employee'),
    path('edit_employee/<int:id>/', EditEmployee.as_view(), name='edit_employee'),
    path('toggle_employee_active/<int:id>/', ToggleEmployeeActive.as_view(), name='toggle_employee_active'),
    path('delete_employee/<int:id>/', DeleteEmployee.as_view(), name='delete_employee'),
    path('get_your_information/', GetYourInformation.as_view(), name='get_your_information'),
]
