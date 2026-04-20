from django.db import models

# Create your models here.
# 天气
class weatherData(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    rainfall = models.FloatField()
    duration = models.FloatField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    record_at = models.DateTimeField(auto_now_add=True)

# 分区
class Zone(models.Model):
    zone_id = models.IntegerField()
    zone_choices =[
        ('A','Zone A'),
        ('B','Zone B'),
        ('C','Zone C'),
        ('D','Zone D'),
    ]
    zone_name = models.CharField(max_length=1, choices=zone_choices, default='A')

# 油棕树
class PalmTree