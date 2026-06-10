from django.db import models

from employee.models import Employee


class Chat(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    message = models.TextField()
    sender = models.IntegerField(db_comment='1 = employee, 2 = system')

    class Meta:
        db_table = 'chat'
