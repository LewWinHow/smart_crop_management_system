from django.urls import path

from monitoring.views import GetCropZoneData

app_name = 'monitoring'

urlpatterns = [
    path('get_crop_zone_data/', GetCropZoneData.as_view(), name='get_crop_zone_data'),
]
