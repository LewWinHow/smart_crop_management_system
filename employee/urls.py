from django.urls import path

from employee.views import (
    GetAllEmployee,
    AddEmployee,
    DeleteEmployee,
    EditEmployee,
    GetMyInformation,
    ToggleEmployeeActive,
)

app_name = 'employee'

urlpatterns = [
    path('get_all_employee/', GetAllEmployee.as_view(), name='get_all_employee'),
    path('add/', AddEmployee.as_view(), name='add_employee'),
    path('edit/<int:pk>/', EditEmployee.as_view(), name='edit_employee'),
    path('toggle_active/<int:pk>/', ToggleEmployeeActive.as_view(), name='toggle_employee_active'),
    path('delete/<int:pk>/', DeleteEmployee.as_view(), name='delete_employee'),
    path('my_information/', GetMyInformation.as_view(), name='get_my_information'),
]
